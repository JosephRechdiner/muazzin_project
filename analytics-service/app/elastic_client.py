from app.logger import Logger
from elasticsearch import Elasticsearch

class ElasticClient:
    def __init__(self, elastic_uri: str, index_name: str, logger: Logger):
        self.logger = logger
        self.index_name = index_name
        try:
            self.es = Elasticsearch(elastic_uri)
        except Exception as e:
            self.logger.exception(f"Could not connect to ElasticSearch, Error: %s", str(e)) 

    def update_analyzed_info(self, file_id, analyzed_info):
        try:
            self.es.update(index=self.index_name, id=file_id, body={"doc": analyzed_info, "doc_as_upsert": True})
            self.logger.info(f"Updated in elastic: {analyzed_info}")
        except Exception as e:
            self.logger.error(f"Could not update in elastic, Error: {str(e)}")