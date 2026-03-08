from elasticsearch import Elasticsearch
from app.logger import Logger


class ElasticManager:
    """
    class responsible for managing elasticsearch connection
    """
    def __init__(self, elastic_uri: str, index_name: str, logger: Logger):
        self.logger = logger
        self.index_name = index_name
        try:
            self.es = Elasticsearch(elastic_uri)
        except Exception as e:
            self.logger.exception(f"Could not connect to elastic, Error: {str(e)}")

    @staticmethod
    def get_hits(response):
        """
        function responsible for extraction actual data from elastic response
        """
        return [hit["_source"] for hit in response["hits"]["hits"]]

    def get_all_metadatas(self):
        """
        function responsible for getting all metadatas in elastic index
        """
        query = {
            "query": {
                "match_all": {}
            },
            "size": 100
        }
        response = self.es.search(index=self.index_name, body=query)
        return self.get_hits(response)
    
    def get_metadata_by_id(self, file_id: str):
        """
        function responsible for getting file metadata by chosen id
        """
        response = self.es.get(index=self.index_name, id=file_id)["_source"]
        return response
    
    def get_top_5_bds_percent(self):
        """
        function responsible for getting top 5 metadata by bds_percent rating
        """
        query = {
            "query": {
                "match_all": {}
            },
            "sort": [{"bds_percent": "desc"}],
            "size": 5
        }
        response = self.es.search(index=self.index_name, body=query)
        return self.get_hits(response)
    
    def get_all_bds(self):
        """
        function responsible for getting all bds files metadats
        """
        query = {
            "query": {
                "term": {"is_bds": True} 
            },
            "size": 100
        }
        response = self.es.search(index=self.index_name, body=query)
        return self.get_hits(response)
    
    def get_bds_greater_then_threshold(self, threshold: int):
        """
        function responsible for getting all bds files that their bds_percentage gt threshold
        """
        query = {
            "query": {
                "bool": {
                    "filter": [
                        {"term": {"is_bds": True}},
                        {"range": {"bds_percent": {"gte": threshold}}},
                    ]
                }
            },
            "size": 100
        }
        response = self.es.search(index=self.index_name, body=query)
        return self.get_hits(response)
    
    def get_metadatas_with_word_in_text(self, word: str):
        """
        function responsible for getting all bds files that their bds_percentage gt threshold
        """
        query = {
            "query": {
                "match": {"file_text": word}
            },
            "size": 100
        }
        response = self.es.search(index=self.index_name, body=query)
        return self.get_hits(response)