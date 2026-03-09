from shared.logger import Logger
from redis import Redis

class RedisManager:
    """
    class responsible for managing all redis connection
    """
    def __init__(self, redis_host: str, logger: Logger):
        self.logger = logger
        try:
            self.r = Redis(host=redis_host, decode_responses=True)
        except Exception as e:
            self.logger.exception(f"Could not connect to redis, Error: {str(e)}")