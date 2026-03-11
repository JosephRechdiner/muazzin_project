from shared.logger.logger import Logger
from shared.models.metadata import FileMetadataText
from shared.logger.logger import Logger

class analyticsHandler:
    """
    supposed to get event from kafka and handle the service functions 
    """
    def __init__(self,analyze, update_analyzed_info_in_elastic, logger: Logger):
        self.logger = logger
        self.analyze = analyze
        self.update_analyzed_info_in_elastic = update_analyzed_info_in_elastic

    def handle_event(self, event):
        """
        handles kafka event
        """
        try:
            validated_pydantic_value = FileMetadataText(**event)
        except Exception:
            self.logger.error(f"Could not validate pydantic types")
        event = validated_pydantic_value.model_dump()
        
        try:
            event["analyzed_info"] = self.analyze(event["file_text"])
            self.logger.info(f"Analyzed info: {event['analyzed_info']}")
        except Exception as e:
            self.logger.error(f"Could not analyze text, Error: {str(e)}")

        try:
            self.update_analyzed_info_in_elastic(event["file_id"], event["analyzed_info"])
        except Exception as e:
            self.logger.error(f"Could not update analyed info in elastic, Error: {str(e)}")
