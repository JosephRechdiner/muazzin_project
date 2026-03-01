from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.routes import router
from app.kafka_producer import KafkaProducer
from app.ingestion_config import IngestionConfig
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('ingestion-service')

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
