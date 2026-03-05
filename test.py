# from datetime import datetime
# import glob
# from pathlib import Path
# import os
# import gridfs
# from pymongo import MongoClient
# import json
# from shared.models import FileMetadata
# from elasticsearch import Elasticsearch
# import logging
# from logging import Logger

# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger('test-service')

# class ElasticClient:
#     def __init__(self, index_name: str, elastic_uri: str, logger: Logger):
#         self.index_name = index_name
#         self.logger = logger
#         try:
#             self.es = Elasticsearch(elastic_uri)
#             self.logger.info(f"Connected to Elastic, {self.es}")
#         except Exception as e:
#             self.logger.exception(f"Could not connect to ElasticSearch, Error: {str(e)}")
        
#     def create_index(self):
#         mapping = {
#             "mappings": {
#                 "properties": [
#                     {"file_path": {"type": "keyword"}},
#                     {"file_name": {"type": "keyword"}},
#                     {"file_size": {"type": "integer"}},
#                     {"file_format": {"type": "keyword"}},
#                     {"created_at": {"type": "keyword"}}
#                 ]
#             }
#         }
#         try:
#             if not self.es.indices.exists(index=self.index_name):
#                 self.es.indices.create(index=self.index_name, body=mapping)
#         except Exception as e:
#             self.logger.exception(f"Could not create {self.index_name}, Error: {str(e)}")

#     def add_to_index(self, metadata: dict):
#         try:
#             self.es.update(index=self.index_name, body=metadata)
#         except Exception as e:
#             self.logger.error(f"Could not insert {metadata}, Error: {str(e)}")


# podcats_paths = glob.glob("podcasts/*.wav")

# client = MongoClient("mongodb://localhost:27017")
# database = client["podcasts_metadatas"]

# fs = gridfs.GridFS(database)

# client = ElasticClient('test', 'http://elasticsearch:9200', logger)
# client.create_index()

# image_id = "1"

# for podcast_path in podcats_paths:
#     metadata = {}

#     file_path = Path(podcast_path)
#     metadata["file_path"] = str(file_path)

#     file_name = file_path.name
#     metadata["file_name"] = file_name

#     file_size = os.path.getsize(file_path) 
#     metadata["file_size"] = file_size

#     file_format = file_path.suffix
#     metadata["file_format"] = file_format

#     created_at_seconds = os.path.getctime(file_path)
#     created_at_full_date = datetime.fromtimestamp(created_at_seconds).strftime("%A, %B %d, %Y %I:%M:%S")
#     metadata["created_at"] = created_at_full_date
    
#     file_metadata = FileMetadata(**metadata)

#     with open(file_path, "rb") as file:
#         data = file.read()
#     fs.put(data=data, id=image_id)

#     client.add_to_index(file_metadata.model_dump())

#     image_id = str(int(image_id) + 1)

# key = "SecretKey"
# a = "hello"
# print(1 & key)

from speech_recognition import Recognizer
import speech_recognition as sr
import glob
import json
import io

# recognizer = sr.Recognizer()
# podcats_paths = glob.glob("./podcasts/*.wav")

# def get_text_from_speach(file_path: str):
#     try:
#         with sr.AudioFile(file_path) as source:
#             audio = recognizer.record(source)

#         text = recognizer.recognize_google(audio_data=audio)
#         return text
#     except Exception as e:
#         raise Exception(f"Could not get text from speach, Error: {str(e)}")
    
# import base64
# coded_string = 'R2Vub2NpZGUsV2F'
# print(coded_string.decode('base64'))

# import base64

# sample_string_bytes = base64.b64decode("R2Vub2NpZGUsV2FyIENyaW1lcyxBcGFydGhlaWQsTWF==")
# sample_string = sample_string_bytes.decode()
# print(sample_string)

import base64



def decode_text(text):
    base64_string = text
    base64_bytes = base64_string.encode("ascii")

    sample_string_bytes = base64.b64decode(base64_bytes)
    sample_string = sample_string_bytes.decode("ascii")
    return sample_string.split(",")

with open("./keys/very_dangerous.txt", "r") as file:
    data = file.read()
very_dangerous = decode_text(data)
with open("./keys/less_dangerous.txt", "r") as file:
    data = file.read()
less_dangerous = decode_text(data)


def get_dangerous_rate(text: str):
    total_less_dangerous_words = 0
    total_very_dangerous_words = 0
    total_text_words = len(text.split(" "))
    rate = total_text_words
    for word in less_dangerous:
        if word in text:
            total_less_dangerous_words += 1
            rate -= total_text_words / 200
    for word in very_dangerous:
        if word in text:
            total_very_dangerous_words += 1
            rate -= total_text_words / 100
    return round((1 - rate / total_text_words) * 100, 2), total_less_dangerous_words, total_very_dangerous_words, total_text_words

text1 = "reports keep coming bomb schools destroyed hospitals families buried under Rubble each one adds to the long list of war crimes and the question is when will the ICC act how long can Justice be delayed before it becomes denial that's the painful part the evidence is there the testimonies are there yet accountability drags meanwhile family is under occupation live in constant fear children grew up hearing drones instead of lullabies parents wonder if tonight will be the night their home disappears and governments issue statements of concerned but do nothing mean meaningful that's why Global action from people matter so much movements like BDS International protests campaigns they apply pressure where leaders fail right and Justice isn't just about trials or courtrooms it's about recognition of suffering acknowledgment of crime and stopping them from happening again without accountability the cycle continues displacement Massacre's apartheid policies which is why resistance comes in many forms from families rebuilding their homes to students marching in the streets it's all part of saying enough"
	
text2 = "across the world protests are filling streets from University campuses to City squares people are standing up against Injustice chanting for Change and demanding action each protest Echoes the same message the humanitarian situation cannot continue lives are being destroyed families displaced and dignity denied people refuse to accept silence and these protests do more than raise awareness they apply real pressure governments may try to ignore the plight of Gaza but millions of voices can no longer be dismissed resistance can be noisy or quiet Publix or personal but every demonstration every rally every March contributes to the global call for Liberation free Palestine is more than a slogan it's a statement of solidarity with people who have endured Decades of Oppression and displacement exactly the power of protest is that it transforms grief into action and shows the world that Injustice will not be unnoticed"
print(get_dangerous_rate(text1))