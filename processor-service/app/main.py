from app.processor_config import ProcessorConfig
from shared.elastic.elastic_client import ElasticManager
from shared.mongo.mongo_connector import MongoManager
from shared.kafka.kafka_consumer import KafkaConsumer
from shared.logger.logger import Logger
from shared.kafka.kafka_producer import KafkaProducer
from app.processor_handler import ProcessorHandler

logger = Logger.get_logger(name="processor-service")

def main():
    config = ProcessorConfig(logger)
    config.validate()

    es = ElasticManager(
        index_name=config.index_name,
        elastic_uri=config.elastic_uri,
        logger=logger
    )

    mongo_manager = MongoManager(
        mongo_uri=config.mongo_uri,
        database_name=config.database_name,
        logger=logger
    )

    producer = KafkaProducer(
        bootstrap_servers=config.bootstrap_servers,
        send_topic=config.send_topic,
        logger=logger
    )

    consumer = KafkaConsumer(
        bootstrap_servers=config.bootstrap_servers,
        group_id=config.group_id,
        listen_topic=config.listen_topic,
        logger=logger
    )

    handler = ProcessorHandler(
        save_in_mongo_callback=mongo_manager.insert_metadata,
        save_in_elastic_callback=es.add_to_index,
        send_to_kafka=producer.send_to_kafka,
        logger=logger
    )

    consumer.start(
        handler.handle_event
    )

if __name__ == "__main__":
    main()