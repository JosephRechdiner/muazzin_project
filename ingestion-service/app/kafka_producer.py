from app.logger import Logger
from confluent_kafka import Producer
import json

class KafkaProducer:
    """ 
    KafkaProducer class supposed to manage all kafka communication
    """
    def __init__(self, bootstrap_servers: str, send_topic: str, logger: Logger):
        self.logger = logger
        self.send_topic = send_topic
        try:
            self.producer = Producer({'bootstrap.servers': bootstrap_servers})
            self.logger.info(f"Producer has connnected to Kafka")
        except Exception as e:
            self.logger.exception(f"Could not connect to Kafka, Error %s", str(e))

    def delivery_report(self, msg, error):
        """ 
        Serves as confirm messege for produce method
        """
        if error:
            self.logger.error(f"Could not send msg to kafka %s", error.value())
        else:
            self.logger.info(f"Sent to kafka: %s", msg.value())

    def send_to_kafka(self, podcast_metadata: dict):
        """ 
        Accual sending the podcast_metadata to kafka
        """
        try:
            value = json.dumps(podcast_metadata).encode('utf-8')
            self.producer.produce(topic=self.send_topic, value=value, callback=self.delivery_report)
            self.producer.poll(1.0)
        except Exception as e:
            self.logger.error(f"Could not send data to kafka, Error: %s", str(e))
