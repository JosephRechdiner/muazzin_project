from fastapi import APIRouter, Request, Depends, HTTPException
from shared.kafka.kafka_producer import KafkaProducer
from app.metadata_extractor import extract_metadata
from shared.models.metadata import FileMetadata
from app.ingestion_config import IngestionConfig
import glob


def get_kafka_producer(request: Request):
    return request.app.state.kafka_producer

def get_ingestion_config(request: Request):
    return request.app.state.config

router = APIRouter()

@router.get("/trigger")
def start_process(config: IngestionConfig = Depends(get_ingestion_config), kafka_producer: KafkaProducer = Depends(get_kafka_producer)):
    """
    This route is responsible for getting metadata for .wav files and sending data to kafka.
    Libraries: glob, pathlib.
    """
    all_metadatas = []

    podcasts_paths = glob.glob(f'{config.podcasts_dir_path}/*.wav')
    for podcast_path in podcasts_paths:

        cur_metadata = extract_metadata(podcast_path)
        
        validated_metadata = FileMetadata(**cur_metadata)

        kafka_producer.send_to_kafka(validated_metadata.model_dump())
        
        all_metadatas.append(validated_metadata.model_dump())

        if not all_metadatas:
            raise HTTPException(status_code=404, detail=f"Could not process data")

    return {
        "Status": "Metadatas Sent!",
        "Metadatas": all_metadatas
    }