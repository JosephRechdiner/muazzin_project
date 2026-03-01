from fastapi import FastAPI
from contextlib import asynccontextmanager
from routes import router
from kafka_producer import KafkaProducer
from ingestion_config import IngestionConfig
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('ingestion-service')

@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.config = IngestionConfig(logger)
    app.state.config.validate()
    app.state.kafka_producer = KafkaProducer()
    yield

app = FastAPI(lifespan=lifespan)
app.include_router(router)
