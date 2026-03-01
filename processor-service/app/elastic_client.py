from logging import Logger
from elasticsearch import Elasticsearch

class ElasticClient:
    def __init__(self, logger: Logger, elastic_uri: str):
        self.logger = logger
        self.es = Elasticsearch()