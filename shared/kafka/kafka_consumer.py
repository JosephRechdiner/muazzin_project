from confluent_kafka import Consumer
from shared.logger.logger import Logger
import json

class KafkaConsumer:
    """
    class responsible for managing kafka consumer
    """
    def __init__(self, bootstrap_servers: str, listen_topic: str, group_id: str, logger: Logger):
        self.logger = logger
        self.listen_topic = listen_topic
        self._is_running = True
        try:
            self.consumer = Consumer({"bootstrap.servers": bootstrap_servers, "group.id": group_id})
            self.logger.info(f"Consumer is connected to kafka")
        except Exception as e:
            self.logger.exception(f"Consumer could not connect to kafka, Error: {str(e)}")

    def start(self, callback):
        """
        function responsible for looping until server is down and polling msgs from kafka
        """
        self.consumer.subscribe([self.listen_topic])
        self.logger.info(f"Consumer is now listennig to {self.listen_topic}...")

        while self._is_running:
            msg = self.consumer.poll(1.0)
            if not msg:
                continue

            if msg.error():
                self.logger.error(f"Error polling msg, Error: %s", msg.error())
                continue
            
            try:
                value = json.loads(msg.value().decode('utf-8'))
            except Exception:
                self.logger.error(f"Could not decode kafka msg")
                continue

            callback(value)

    def stop(self):
        """
        function responsible for closing consumer at server shotdown
        """
        self._is_running = False
        self.consumer.close()