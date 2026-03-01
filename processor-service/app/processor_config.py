from logging import Logger
import os

class ProcessorConfig:
    def __init__(self, logger: Logger):
        self.logger = logger
        self.bootstrap_servers = os.getenv("BOOTSTRAP_SERVERS")
        self.listen_topic = os.getenv("LISTEN_TOPIC")
        self.group_id = os.getenv("GROUP_ID")
        self.database_name = os.getenv("DATABASE_NAME")
        self.collection_name = os.getenv("COLLECTION_NAME")
        self.elastic_uri = os.getenv("ELASTIC_URI") 
        
    def validate(self):
        missing = []

        if not self.bootstrap_servers:
            missing.append("BOOTSTRAP_SERVERS")
        if not self.listen_topic:
            missing.append("LISTEN_TOPIC")
        if not self.group_id:
            missing.append("GROUP_ID")
        if not self.database_name:
            missing.append("DATABASE_NAME")
        if not self.collection_name:
            missing.append("COLLECTION_NAME")
        if not self.elastic_uri:
            missing.append("ELASTIC_URI")

        if missing:
            msg = "|".join(missing) + " missing"
            self.logger.exception(msg)
            raise ValueError(msg)