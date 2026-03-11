from shared.logger.logger import Logger
import os

class ApiConfig:
    """
    class responsible for loading all env variables from docker compose 
    """
    def __init__(self, logger: Logger):
        self.logger = logger
        self.redis_host = os.getenv("REDIS_HOST")
        self.elastic_uri = os.getenv("ELASTIC_URI")
        self.index_name = os.getenv("INDEX_NAME")

    def validate(self):
        """
        function responsible for validating all env variables exist and raise vlue error otherwise
        """
        missing = []

        if not self.redis_host:
            missing.append("REDIS_HOST")
        if not self.elastic_uri:
            missing.append("ELASTIC_URI")
        if not self.index_name:
            missing.append("INDEX_NAME")

        if missing:
            msg = "|".join(missing) + " missing"
            self.logger.exception(msg)
            raise ValueError(msg)