from shared.logger.logger import Logger
from shared.models.metadata import FileMetadataId

class SttHandler:
    """
    supposed to get event from kafka and handle the service functions 
    """
    def __init__(self, recognizer, sr, stt_extractor, update_in_elastic, send_to_kafka, logger: Logger):
        self.recognizer = recognizer
        self.sr = sr
        self.stt_extractor = stt_extractor
        self.update_in_elastic = update_in_elastic
        self.send_to_kafka = send_to_kafka
        self.logger = logger

    def handle_event(self, event):
        """
        handles kafka event
        """
        try:
            pydantic_validated_value = FileMetadataId(**event)
        except Exception as e:
            self.logger.error(f"Could not validate pydantic types, Error: {str(e)}")

        event = pydantic_validated_value.model_dump()
        try:
            speach_in_text = self.stt_extractor(self.sr, self.recognizer, event["file_path"])
            self.logger.info(f"Extract text: {speach_in_text}")
        except Exception as e:
            self.logger.error(f"Could not get text from speach, Error: {str(e)}")

        try:
            event["file_text"] = speach_in_text
            response = self.update_in_elastic(event["file_id"], event)
            if response:
                self.logger.info(f"Updated text in Elastic Search: %s", event)
        except Exception as e:
            self.logger.error(f"Could not update text in Elastic, Error: {str(e)}")

        try:
            self.send_to_kafka(event)
        except Exception as e:
            self.logger.error(f"Could not send raw text dict to kafka, Error: {str(e)}") 


        