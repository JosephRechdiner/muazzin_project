from fastapi import Fastapi
from contextlib import asynccontextmanager
from app.routes import route
from app.elastic_client import ElasticManager
from app.redis_client import RedisManager
from app.api_config import ApiConfig
from app.logger import Logger

@asynccontextmanager
async def lifespan(app: Fastapi):
    """
    function responsible for init all app.state varibles on app start
    """
    app.state.logger = Logger().get_logger()
    app.state.config = ApiConfig(logger=app.state.logger)
    app.state.config.validate()
    app.state.redis_manager = RedisManager(redis_host=app.state.config.redis_host, logger=app.state.logger)
    app.state.elastic_manager = ElasticManager(elastic_uri=app.state.config.elastic_uri, logger=app.state.logger)
    yield

app = Fastapi(lifespan=lifespan)
app.include_router(route)