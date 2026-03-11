from shared.logger.logger import Logger
from shared.models.metadata import FileMetadata
import hashlib
import json

class ProcessorHandler:
    """
    supposed to get event from kafka and handle the service functions 
    """
    def __init__(self, save_in_mongo_callback, save_in_elastic_callback, send_to_kafka, logger: Logger):
        self.logger = logger
        self.save_in_mongo_callback = save_in_mongo_callback
        self.save_in_elastic_callback = save_in_elastic_callback
        self.send_to_kafka = send_to_kafka

    def handle_event(self, event):
        """
        handles kafka event
        """
        try:
            pydantic_validated_value = FileMetadata(**event)
        except Exception as e:
            self.logger.error(f"Could not validate pydantic types, Error: {str(e)}")

        event = pydantic_validated_value.model_dump()

        dhash = hashlib.md5()
        encoded = json.dumps(event, sort_keys=True).encode()
        dhash.update(encoded)
        file_id = dhash.hexdigest()
        event["file_id"] = file_id

        try:
            response = self.save_in_mongo_callback(file_id, event["file_path"])
            if response:
                self.logger.info(f"Inserted to MongoDB: %s", event)
        except Exception as e:
            self.logger.error(f"Could not save data in mongo, Error: {str(e)}")
        
        try:
            response = self.save_in_elastic_callback(file_id, event)
            if response:
                self.logger.info(f"Inserted to Elastic Search: %s", event)
        except Exception as e:
            self.logger.error(f"Could not save data in Elastic, Error: {str(e)}")

        try:
            self.send_to_kafka(event)
        except Exception as e:
            self.logger.error(f"Could not send data in Kafka, Error: {str(e)}")
