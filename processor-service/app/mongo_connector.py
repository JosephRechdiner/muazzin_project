import gridfs
from pymongo import MongoClient
from logging import Logger
import json

class MongoManager:
    def __init__(self, mongo_uri: str, database_name: str, logger: Logger):
        self.logger = logger
        self.database_name = database_name
        try:
            self.client = MongoClient(mongo_uri)
        except Exception as e:
            self.logger.exception(f"Could not connect to MongoDB, Error: {str(e)}")

    def insert_metadata(self, file_path: dict, file_id: str):
        try:
            database = self.client[self.database_name]
            fs = gridfs.GridFS(database)

            with open(file_path, "rb") as file:
                data = file.read()
            fs.put(data=data, id=file_id)
        except Exception as e:
            self.logger.error(f"Could not insert {file} to MongoDB, Error: {str(e)}")