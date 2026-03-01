from datetime import datetime
import glob
from pathlib import Path
import os

podcats_paths = glob.glob("podcasts/*.wav")

for podcats_path in podcats_paths:
    path = Path(podcats_path)
    seconds = os.path.getctime(podcats_path)
    size = os.path.getsize(podcats_path) 

    print(datetime.fromtimestamp(seconds).strftime("%A, %B %d, %Y %I:%M:%S"))
    print(size)
    print(path)
    print(path.name)
    print(path.suffix)
    print(path.__sizeof__())



