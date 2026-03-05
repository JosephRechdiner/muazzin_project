FROM python:3.11-slim

WORKDIR /app

COPY ./analytics-service/requirements.txt .

RUN pip install -r requirements.txt

COPY ./keys /app/keys

COPY ./shared /app/shared

COPY ./analytics-service .

CMD [ "python", "-m", "app.main" ]