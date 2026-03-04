from logger import Logger
import os

class SttConfig:
    """
    Config class is supposed to load env variables that are needed for this service
    """
    def __init__(self, logger: Logger):
        self.logger = logger
        self.mongo_uri = os.getenv("MONGO_URI")
        self.elsatic_uri = os.getenv("ELASTIC_URI") 
        self.index_name = os.getenv("INDEX_NAME")
        self.database_name = os.getenv("DATABASE_NAME")

    def validate(self):
        """
        Validating env variables exist
        """
        missing = []

        if not self.mongo_uri:
            missing.append("MONGO_URI")
        if not self.elsatic_uri:
            missing.append("ELASTIC_URI")
        if not self.index_name:
            missing.append("INDEX_NAME")
        if not self.database_name:
            missing.append("DATABASE_NAME")

        if missing:
            msg = "|".join(missing) + " missing"
            self.logger.exception(msg)
            raise ValueError(msg)
