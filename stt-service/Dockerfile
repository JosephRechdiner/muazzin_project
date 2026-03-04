FROM python:3.11-slim

WORKDIR /app

COPY ./stt-service/requirements.txt .

RUN pip install -r requirements.txt

COPY ./podcasts /app/podcasts
COPY ./shared /app/shared

COPY ./stt-service .

CMD [ "python", "app/main.py" ]