from confluent_kafka import Consumer
from logging import Logger
import json

class KafkaConsumer:
    """ 
    KafkaConsumer class supposed to manage all kafka communication
    """
    def __init__(self, bootstrap_servers: str, group_id: str, listen_topic: str, logger: Logger):
        self.logger = logger
        self._is_running = True
        self.listen_topic = listen_topic
        try:
            self.consumer = Consumer({
                "bootstrap.servers": bootstrap_servers,
                "group.id": group_id
            }) 
        except Exception as e:
            self.logger.exception(f"Could not connect to Kafka, Error: {str(e)}")
            raise

    def start(self, save_in_mongo_callback, save_in_elastic_callback):
        """ 
        Supposed to start listening to kafka topic
        """
        self.consumer.subscribe([self.listen_topic])
        self.logger.info(f"Consumer is now listennig to {self.listen_topic}...")

        file_id = "1"
        while self._is_running:
            msg = self.consumer.poll(1.0)
            if msg is None:
                continue
            if msg.error():
                self.logger.error(f"Error while pulling msg, %s", msg.error())
                continue

            try:
                value = json.loads(msg.value().decode('utf-8'))
            except Exception:
                self.logger.error(f"Could not decode msg")


            try:
                response = save_in_mongo_callback(value["file_path"], file_id)
                if response:
                    self.logger.info(f"Inserted to MongoDB: %s", value)
            except Exception as e:
                self.logger.error(f"Could save data in mongo, Error: {str(e)}")

            try:
                response = save_in_elastic_callback(file_id, value)
                if response:
                    self.logger.info(f"Inserted to Elastic Search: %s", value)
            except Exception as e:
                self.logger.error(f"Could not save data in elastic, Error: {str(e)}")

            file_id = str(int(file_id) + 1)

    def stop(self):
        """ 
        Stop consumer's listening to kafka topic
        """
        self.consumer.stop()
        self._is_running = False