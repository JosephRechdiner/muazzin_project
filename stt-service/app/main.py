from logger import Logger
from stt_config import SttConfig
from elastic_client import ElasticManager
from kafka_consumer import KafkaConsumer
from stt_handler import get_text_from_speach
import speech_recognition as sr

logger = Logger.get_logger()

def main():
    config = SttConfig(logger=logger)
    config.validate()

    es = ElasticManager(
        elastic_uri=config.elsatic_uri,
        index_name=config.index_name,
        logger=logger
    )
    
    consumer = KafkaConsumer(
        bootstrap_servers=config.bootstrap_servers,
        group_id=config.group_id,
        listen_topic=config.listen_topic,
        logger=logger
    )
    recognizer = sr.Recognizer()

    consumer.start(
        recognizer=recognizer,
        sr=sr,
        stt_extractor=get_text_from_speach,
        update_in_elastic=es.update_text_in_elastic
    )

if __name__ == "__main__":
    main()