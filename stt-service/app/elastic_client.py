from elasticsearch import Elasticsearch
from app.logger import Logger

class ElasticManager:
    """ 
    ElasticClient class supposed to manage all elsticshearch connection
    """
    def __init__(self, elastic_uri: str, index_name: str, logger: Logger):
        self.logger = logger
        self.index_name = index_name
        try:
            self.es = Elasticsearch(elastic_uri)
        except Exception as e:
            self.logger.exception(f"Could not connect to ElasticSearch, Error: {str(e)}")

    def update_text_in_elastic(self, file_id: str, metadata: dict):
        """ 
        Supposed to update the raw text field in index
        """
        try:
            self.es.update(index=self.index_name, id=file_id, body={"doc": metadata, "doc_as_upsert": True})
            self.logger.info(f"Elastic text field updated: %s", metadata["text"])
        except Exception as e:
            self.logger.error(f"Could not updata text in ElasticSearch, Error: {str(e)}")