from datetime import datetime
import glob
from pathlib import Path
import os
import gridfs
from pymongo import MongoClient
import json
from shared.models import FileMetadata
from elasticsearch import Elasticsearch
import logging
from logging import Logger

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('test-service')

class ElasticClient:
    def __init__(self, index_name: str, elastic_uri: str, logger: Logger):
        self.index_name = index_name
        self.logger = logger
        try:
            self.es = Elasticsearch(elastic_uri)
            self.logger.info(f"Connected to Elastic, {self.es}")
        except Exception as e:
            self.logger.exception(f"Could not connect to ElasticSearch, Error: {str(e)}")
        
    def create_index(self):
        mapping = {
            "mappings": {
                "properties": [
                    {"file_path": {"type": "keyword"}},
                    {"file_name": {"type": "keyword"}},
                    {"file_size": {"type": "integer"}},
                    {"file_format": {"type": "keyword"}},
                    {"created_at": {"type": "keyword"}}
                ]
            }
        }
        try:
            if not self.es.indices.exists(index=self.index_name):
                self.es.indices.create(index=self.index_name, body=mapping)
        except Exception as e:
            self.logger.exception(f"Could not create {self.index_name}, Error: {str(e)}")

    def add_to_index(self, metadata: dict):
        try:
            self.es.update(index=self.index_name, body=metadata)
        except Exception as e:
            self.logger.error(f"Could not insert {metadata}, Error: {str(e)}")


podcats_paths = glob.glob("podcasts/*.wav")

client = MongoClient("mongodb://localhost:27017")
database = client["podcasts_metadatas"]

fs = gridfs.GridFS(database)

client = ElasticClient('test', 'http://elasticsearch:9200', logger)
client.create_index()

image_id = "1"

for podcast_path in podcats_paths:
    metadata = {}

    file_path = Path(podcast_path)
    metadata["file_path"] = str(file_path)

    file_name = file_path.name
    metadata["file_name"] = file_name

    file_size = os.path.getsize(file_path) 
    metadata["file_size"] = file_size

    file_format = file_path.suffix
    metadata["file_format"] = file_format

    created_at_seconds = os.path.getctime(file_path)
    created_at_full_date = datetime.fromtimestamp(created_at_seconds).strftime("%A, %B %d, %Y %I:%M:%S")
    metadata["created_at"] = created_at_full_date
    
    file_metadata = FileMetadata(**metadata)

    with open(file_path, "rb") as file:
        data = file.read()
    fs.put(data=data, id=image_id)

    client.add_to_index(file_metadata.model_dump())

    image_id = str(int(image_id) + 1)
