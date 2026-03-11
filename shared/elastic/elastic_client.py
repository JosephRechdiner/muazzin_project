from elasticsearch import Elasticsearch
from shared.logger.logger import Logger


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

    def update_analyzed_info(self, file_id, analyzed_info):
        """
        function responsible for adding analyzed info to an existing document 
        """
        try:
            self.es.update(index=self.index_name, id=file_id, body={"doc": analyzed_info, "doc_as_upsert": True})
            self.logger.info(f"Updated in elastic: {analyzed_info}")
        except Exception as e:
            self.logger.error(f"Could not update in elastic, Error: {str(e)}")

    def update_text_in_elastic(self, file_id: str, metadata: dict):
        """ 
        Supposed to update the raw text field in index
        """
        try:
            self.es.update(index=self.index_name, id=file_id, body={"doc": metadata, "doc_as_upsert": True})
            self.logger.info(f"Elastic text field updated: {metadata['file_text']}")
        except Exception as e:
            self.logger.error(f"Could not updata text in ElasticSearch, Error: {str(e)}")
            
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
            }
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
            }
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
            }
        }
        response = self.es.search(index=self.index_name, body=query)
        return self.get_hits(response)

    def get_avg_bds(self):
        """
        function responsible for getting the average of bds over all metadatas
        """
        query = {
            "aggs": {
                "bds_percent_average":
                    { "avg": { "field": "bds_percent" }
                }
            }
        }
        response = self.es.search(index=self.index_name, body=query)
        return {"avg_bds": response["aggregations"]["bds_percent_average"]["value"]}