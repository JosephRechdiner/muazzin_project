from shared.logger import Logger
from app.stt_config import SttConfig
from app.elastic_client import ElasticManager
from app.kafka_consumer import KafkaConsumer
from app.stt_handler import get_text_from_speach
from shared.kafka_producer import KafkaProducer
import speech_recognition as sr

logger = Logger.get_logger(name="stt-service")

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

    producer = KafkaProducer(
        bootstrap_servers=config.bootstrap_servers,
        send_topic=config.send_topic,
        logger=logger
    )

    recognizer = sr.Recognizer()

    consumer.start(
        recognizer=recognizer,
        sr=sr,
        stt_extractor=get_text_from_speach,
        update_in_elastic=es.update_text_in_elastic,
        send_to_kafka=producer.send_to_kafka
    )

if __name__ == "__main__":
    main()