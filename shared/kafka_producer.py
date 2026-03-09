from confluent_kafka import Producer
from shared.logger import Logger
import json

class KafkaProducer:
    def __init__(self, bootstrap_servers: str, send_topic: str, logger: Logger):
        self.logger = logger
        self.send_topic = send_topic
        try:
            self.producer = Producer({"bootstrap.servers": bootstrap_servers})
        except Exception as e:
            self.logger.exception(f"Could not connect Producer to Kafka, Error: {str(e)}")
            raise
            
    def delivery_report(self, error, msg):
        if error:
            self.logger.error(f"Could not send to kafka, Error: %s", error.value())
        else:
            self.logger.info(f"Sent to Kafka: %s", msg.value())
        
    def send_to_kafka(self, metadata: dict):
        try:
            value = json.dumps(metadata).encode("utf-8")
            self.producer.produce(topic=self.send_topic, value=value, callback=self.delivery_report)
            self.producer.poll(1.0)
        except Exception as e:
            self.logger.error(f"Could not send data to kafka, Error: %s", str(e))