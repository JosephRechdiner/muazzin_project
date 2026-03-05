from confluent_kafka import Producer
from app.logger import Logger
import json

class KafkaProducer:
    def __init__(self, bootstrap_servers: str, send_topic:str, logger: Logger):
        self.send_topic = send_topic
        self.logger = logger
        try:
            self.producer = Producer({"bootstrap.severs": bootstrap_servers})
        except Exception as e:
            self.logger.exception(f"Could not connect producer to kafka, Error: {str(e)}")

    def delivery_report(self, msg, error):
        if error: 
            self.logger.error(f"Could not send data to kafka, Error: %s", error.value())
        else:
            self.logger.info(f"Send to kafka: %s", msg.value())

    def send_to_kafka(self, value: dict):
        try:
            value = json.dumps(value).encode('utf-8')
            self.producer.produce(topic=self.send_topic, value=value, callback=self.delivery_report)
            self.producer.poll(1.0)
        except Exception as e:
            self.logger.error(f"Could not send msg to kafka, Error: {str(e)}")