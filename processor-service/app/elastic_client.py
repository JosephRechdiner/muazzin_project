from logger import Logger
from elasticsearch import Elasticsearch

class ElasticClient:
    """ 
    ElasticClient class supposed to manage all elsticshearch connection
    """
    def __init__(self, index_name: str, elastic_uri: str, logger: Logger):
        self.logger = logger
        self.index_name = index_name
        try:
            self.es = Elasticsearch(elastic_uri)
            self.logger.info(f"Elastic client has connnected to Elastic Search")
        except Exception as e:
            self.logger.exception(f"Could not connect to ElasticSearch, Error: {str(e)}")
        
    def create_index(self):
        """ 
        Supposed to create index if not exists in elsticshearch
        """
        mapping = {
            "mappings": {
                "properties": {
                    "file_path": {"type": "keyword"},
                    "file_name": {"type": "keyword"},
                    "file_size": {"type": "integer"},
                    "file_format": {"type": "keyword"},
                    "created_at": {"type": "keyword"}
                }
            }
        }
        try:
            if not self.es.indices.exists(index=self.index_name):
                self.es.indices.create(self.index_name, body=mapping)
        except Exception as e:
            self.logger.exception(f"Could not create {self.index_name}, Error: {str(e)}")

    def add_to_index(self, file_id: str, metadata: dict):
        """ 
        Supposed to insert on document in index
        """
        try:
            res = self.es.index(index=self.index_name, id=file_id, document=metadata)
            if res:
                return True
        except Exception as e:
            self.logger.error(f"Could not insert {metadata}, Error: {str(e)}")
