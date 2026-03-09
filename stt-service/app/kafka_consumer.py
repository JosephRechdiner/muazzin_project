from confluent_kafka import Consumer
from shared.logger import Logger
from shared.models import FileMetadataId
import json

class KafkaConsumer:
    """ 
    KafkaConsumer class supposed to manage all kafka communication
    """
    def __init__(self, bootstrap_servers: str, group_id: str, listen_topic: str, logger: Logger):
        self.logger = logger
        self.listen_topic = listen_topic
        self._is_running = True
        try:
            self.consumer = Consumer({
                "bootstrap.servers": bootstrap_servers,
                "group.id": group_id
            })
        except Exception as e:
            self.logger.exception(f"Could not connect Consumer to Kafka, Error: {str(e)}")
            raise

    def start(self, sr, recognizer, stt_extractor, update_in_elastic, send_to_kafka):
        """ 
        Supposed to start listening to kafka topic and send data to stt extractor and elastic update callbacks
        """
        self.consumer.subscribe([self.listen_topic])
        self.logger.info(f"Consumer is now listening to topic: {self.listen_topic}...")
        
        while self._is_running:
            msg = self.consumer.poll(1.0)
            if not msg:
                continue
            if msg.error():
                self.logger.error(f"kafka Error: %s", msg.error())
                continue
        
            try:
                value = json.loads(msg.value().decode("utf-8"))
            except Exception as e:
                self.logger.error(f"Could not decode msg, Error: {str(e)}")
                continue

            try:
                pydantic_validated_value = FileMetadataId(**value)
            except Exception as e:
                self.logger.error(f"Could not validate pydantic types, Error: {str(e)}")
                continue

            value = pydantic_validated_value.model_dump()
            try:
                speach_in_text = stt_extractor(sr, recognizer, value["file_path"])
                self.logger.info(f"Extract text: {speach_in_text}")
            except Exception as e:
                self.logger.error(f"Could not get text from speach, Error: {str(e)}")
                continue       

            try:
                value["file_text"] = speach_in_text
                response = update_in_elastic(value["file_id"], value)
                if response:
                    self.logger.info(f"Updated text in Elastic Search: %s", value)
            except Exception as e:
                self.logger.error(f"Could not update text in Elastic, Error: {str(e)}")
                continue

            try:
                send_to_kafka(value)
            except Exception as e:
                self.logger.error(f"Could not send raw text dict to kafka, Error: {str(e)}") 

    def stop(self):
        """ 
        Stop consumer's listening to kafka topic
        """
        self._is_running = False
        self.consumer.close()