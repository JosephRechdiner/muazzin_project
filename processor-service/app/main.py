from app.processor_config import ProcessorConfig
from app.elastic_client import ElasticClient
from app.mongo_connector import MongoManager
from app.kafka_consumer import KafkaConsumer
from shared.logger import Logger
from shared.kafka_producer import KafkaProducer

logger = Logger.get_logger(name="processor-service")

def main():
    config = ProcessorConfig(logger)
    config.validate()

    es = ElasticClient(
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

    consumer.start(
        mongo_manager.insert_metadata,
        es.add_to_index,
        producer.send_to_kafka
    )

if __name__ == "__main__":
    main()