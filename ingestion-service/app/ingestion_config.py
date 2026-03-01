from logging import Logger
import os

class InsegtionConfig:
    def __init__(self, logger: Logger):
        self.bootstrap_servers = os.getenv("BOOTSTRAP_SERVERS")
        self.podcasts_dir_path = os.getenv("PODCASTS_DIR_PATH")
        self.logger = logger

    def validate(self):
        missing = []

        if not self.bootstrap_servers:
            missing.append("BOOTSTRAP_SERVERS")
        if not self.podcasts_dir_path:
            missing.append("PODCASTS_DIR_PATH")

        if missing:
            msg = "|".join(missing) + " missing"
            self.logger.exception(msg)
            raise