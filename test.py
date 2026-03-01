from datetime import datetime
import glob
from pathlib import Path
import os
import gridfs
from pymongo import MongoClient
import json

podcats_paths = glob.glob("podcasts/*.wav")

client = MongoClient("mongodb://localhost:27017")
database = client["podcasts_metadatas"]

fs = gridfs.GridFS(database)

image_id = "1"

for podcast_path in podcats_paths:
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
    
    with open(file_path, "rb") as file:
        data = file.read()
    fs.put(data=data, id=image_id)
    image_id = str(int(image_id) + 1)



