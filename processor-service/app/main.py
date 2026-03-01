import logging
from processor_config import ProcessorConfig
from elastic_client import ElasticClient
from mongo_connector import MongoManager
from kafka_consumer import KafkaConsumer

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('processor-service')

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

    consumer = KafkaConsumer(
        bootstrap_servers=config.bootstrap_servers,
        group_id=config.group_id,
        listen_topic=config.listen_topic,
        logger=logger
    )

    consumer.start(
        mongo_manager.insert_metadata,
        es.add_to_index
    )

if __name__ == "__main__":
    main()