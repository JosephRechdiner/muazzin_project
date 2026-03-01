from fastapi import APIRouter, Request, Depends
from kafka_producer import KafkaProducer
from metadata_extractor import get_metadata
import glob


def get_kafka_producer(request: Request):
    return request.app.state.kafka_producer

router = APIRouter()

@router.get("/trigger")
def start_process(kafka_producer: KafkaProducer = Depends(get_kafka_producer)):
    """
    This route is responsible for getting metadata for .wav files and sending data to kafka.
    Libraries: glob, pathlib.
    """
    all_metadatas = []

    podcasts_paths = glob.glob("./podcasts/*.wav")
    for podcast_path in podcasts_paths:
        cur_metadata = get_metadata(podcast_path)

        

        kafka_producer.send_to_kafka(cur_metadata)