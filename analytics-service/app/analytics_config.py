from shared.logger.logger import Logger
import os

class AnalyticsConfig:
    """
    Config class is supposed to load env variables that are needed for this service
    """
    def __init__(self, logger: Logger):
        self.logger = logger
        self.elsatic_uri = os.getenv("ELASTIC_URI") 
        self.index_name = os.getenv("INDEX_NAME")
        self.group_id = os.getenv("GROUP_ID")
        self.bootstrap_servers = os.getenv("BOOTSTRAP_SERVERS")
        self.listen_topic = os.getenv("LISTEN_TOPIC")

    def validate(self):
        """
        Validating env variables exist
        """
        missing = []

        if not self.elsatic_uri:
            missing.append("ELASTIC_URI")
        if not self.listen_topic:
            missing.append("LISTEN_TOPIC")
        if not self.bootstrap_servers:
            missing.append("BOOTSTRAP_SERVERS")
        if not self.index_name:
            missing.append("INDEX_NAME")
        if not self.group_id:
            missing.append("GROUP_ID")

        if missing:
            msg = "|".join(missing) + " missing"
            self.logger.exception(msg)
            raise ValueError(msg)
