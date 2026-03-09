from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.routes import route
from app.elastic_client import ElasticManager
from app.redis_client import RedisManager
from app.api_config import ApiConfig
from shared.logger import Logger

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    function responsible for init all app.state varibles on app start
    """
    app.state.logger = Logger().get_logger(name="api-service")
    app.state.config = ApiConfig(logger=app.state.logger)
    app.state.config.validate()
    app.state.redis_manager = RedisManager(
        redis_host=app.state.config.redis_host,
        logger=app.state.logger
        )
    app.state.elastic_manager = ElasticManager(
        elastic_uri=app.state.config.elastic_uri,
        index_name=app.state.config.index_name,
        logger=app.state.logger
        )
    yield

app = FastAPI(lifespan=lifespan)
app.include_router(route)