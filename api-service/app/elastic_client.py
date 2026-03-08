from elasticsearch import Elasticsearch
from logger import Logger


class ElasticManager:
    """
    class responsible for managing elasticsearch connection
    """
    def __init__(self, elastic_uri: str, logger: Logger):
        self.logger = logger
        try:
            self.es = Elasticsearch(elastic_uri)
        except Exception as e:
            self.logger.exception(f"Could not connect to elastic, Error: {str(e)}")

    