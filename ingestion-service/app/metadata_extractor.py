from datetime import datetime
from pathlib import Path
import os

def extract_metadata(podcast_path: str):
    """
    The function is responsible for extracting metadata for the current podcast path
    """
    metadata = {}

    file_path = Path(podcast_path)
    metadata["file_path"] = str(file_path)

    file_name = file_path.name
    metadata["file_name"] = file_name

    file_size = os.path.getsize(file_path) 
    metadata["file_size"] = file_size

    file_format = file_path.suffix
    metadata["file_format"] = file_format

    created_at_seconds = os.path.getctime(file_path)
    created_at_full_date = datetime.fromtimestamp(created_at_seconds).strftime("%A, %B %d, %Y %I:%M:%S")
    metadata["created_at"] = created_at_full_date

    return metadata
