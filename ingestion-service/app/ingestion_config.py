from logging import Logger
import os

class IngestionConfig:
    """
    Config class is supposed to load env variables that are needed for this service
    """
    def __init__(self, logger: Logger):
        self.bootstrap_servers = os.getenv("BOOTSTRAP_SERVERS")
        self.podcasts_dir_path = os.getenv("PODCASTS_DIR_PATH")
        self.send_topic = os.getenv("SEND_TOPC")
        self.logger = logger

    def validate(self):
        """
        Validating env variables exist
        """
        missing = []

        if not self.bootstrap_servers:
            missing.append("BOOTSTRAP_SERVERS")
        if not self.podcasts_dir_path:
            missing.append("PODCASTS_DIR_PATH")
        if not self.send_topic:
            missing.append("SEND_TOPC")

        if missing:
            msg = "|".join(missing) + " missing"
            self.logger.exception(msg)
            raise ValueError(msg)