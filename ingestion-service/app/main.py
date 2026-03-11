from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.routes import router
from shared.kafka.kafka_producer import KafkaProducer
from app.ingestion_config import IngestionConfig
from shared.logger.logger import Logger

logger = Logger.get_logger(name="ingestion-service")

@asynccontextmanager
async def lifespan(app: FastAPI):
    """ 
    Lifespan function, activated as server comes up
    """
    app.state.config = IngestionConfig(logger)
    app.state.config.validate()
    app.state.kafka_producer = KafkaProducer(app.state.config.bootstrap_servers, app.state.config.send_topic, logger)
    yield

app = FastAPI(lifespan=lifespan)
app.include_router(router)
