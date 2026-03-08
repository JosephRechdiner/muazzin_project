from app.logger import Logger
import base64

class DangerousWordsExtractor:
    """
    class responsible for extracting words from text files
    """
    def __init__(self, logger: Logger):
        self.logger = logger
    
    def decode_text(self, file_path):
        """
        decoding not readable text
        """
        try:
            with open(file_path, "r") as file:
                text = file.read()

            base64_string = text
            base64_bytes = base64_string.encode("ascii")

            sample_string_bytes = base64.b64decode(base64_bytes)
            sample_string = sample_string_bytes.decode("ascii")
            return sample_string.split(",")
        except Exception as e:
            self.logger.error(f"Could not decode text, Error: {str(e)}")