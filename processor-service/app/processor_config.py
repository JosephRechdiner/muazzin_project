from logger import Logger
import os

class ProcessorConfig:
    """
    Config class is supposed to load env variables that are needed for this service
    """
    def __init__(self, logger: Logger):
        self.logger = logger
        self.bootstrap_servers = os.getenv("BOOTSTRAP_SERVERS")
        self.listen_topic = os.getenv("LISTEN_TOPIC")
        self.group_id = os.getenv("GROUP_ID")
        self.database_name = os.getenv("DATABASE_NAME")
        self.elastic_uri = os.getenv("ELASTIC_URI") 
        self.index_name = os.getenv("INDEX_NAME") 
        self.mongo_uri = os.getenv("MONGO_URI") 
        self.send_topic = os.getenv("SEND_TOPIC")
        
    def validate(self):
        """
        Validating env variables exist
        """
        missing = []

        if not self.bootstrap_servers:
            missing.append("BOOTSTRAP_SERVERS")
        if not self.listen_topic:
            missing.append("LISTEN_TOPIC")
        if not self.send_topic:
            missing.append("SEND_TOPIC")
        if not self.group_id:
            missing.append("GROUP_ID")
        if not self.database_name:
            missing.append("DATABASE_NAME")
        if not self.elastic_uri:
            missing.append("ELASTIC_URI")
        if not self.index_name:
            missing.append("INDEX_NAME")
        if not self.mongo_uri:
            missing.append("MONGO_URI")

        if missing:
            msg = "|".join(missing) + " missing"
            self.logger.exception(msg)
            raise ValueError(msg)