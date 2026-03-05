from confluent_kafka import Consumer
from app.logger import Logger
from shared.models import FileMetadataText
import json

class KafkaConsumer:
    def __init__(self, bootstrap_server: str, listen_topic: str, group_id: str, logger: Logger):
        self.logger = logger
        self.listen_topic = listen_topic
        self._is_running = True
        try:
            self.consumer = Consumer({"bootstrap.servers": bootstrap_server, "group.id": group_id})
            self.logger.info(f"Consumer is connected to kafka")
        except Exception as e:
            self.logger.exception(f"Consumer could not connect to kafka, Error: {str(e)}")

    def start(self, analyze, update_analyzed_info_in_elastic):
        self.consumer.subscribe([self.listen_topic])
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

            try:
                validated_pydantic_value = FileMetadataText(**value)
            except Exception:
                self.logger.error(f"Could not validate pydantic types")
            
            value = validated_pydantic_value.model_dump()
            try:
                value["analyzed_info"] = analyze(value["file_text"])
                self.logger.info(f"Analyzed info: {value['analyzed_info']}")
            except Exception as e:
                self.logger.error(f"Could not analyze text, Error: {str(e)}")

            try:
                update_analyzed_info_in_elastic(value["file_id"], value["analyzed_info"])
            except Exception as e:
                self.logger.error(f"Could not update analyed info in elastic, Error: {str(e)}")

    def stop(self):
        self._is_running = False
        self.consumer.close()