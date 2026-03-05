from confluent_kafka import Producer
from app.logger import Logger
import json

class KafkaProducer:
    """ 
    KafkaProducer class supposed to manage all kafka communication
    """
    def __init__(self, bootstrap_servers: str, send_topic:str, logger: Logger):
        self.send_topic = send_topic
        self.logger = logger
        try:
            self.producer = Producer({"bootstrap.servers": bootstrap_servers})
            self.logger.info(f"Producer has connnected to Kafka")
        except Exception as e:
            self.logger.exception(f"Could not connect producer to kafka, Error: {str(e)}")

    def delivery_report(self, error, msg):
        """ 
        Serves as confirm messege for produce method
        """
        if error: 
            self.logger.error(f"Could not send data to kafka, Error: %s", error.value())
        else:
            self.logger.info(f"Send to kafka: %s", msg.value())

    def send_to_kafka(self, value: dict):
        """ 
        Actual sending the podcast_metadata to kafka
        """
        try:
            value = json.dumps(value).encode('utf-8')
            self.producer.produce(topic=self.send_topic, value=value, callback=self.delivery_report)
            self.producer.poll(1.0)
        except Exception as e:
            self.logger.error(f"Could not send msg to kafka, Error: {str(e)}")