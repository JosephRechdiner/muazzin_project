FROM python:3.11-slim

WORKDIR /app

RUN apt-get update & apt-get install -y tesseract-ocr

COPY ./analytics-service/requirements.txt .

RUN pip install -r requirements.txt

COPY ./images /app/images

COPY ./analytics-service .

CMD [ "python", "-m", "app.main" ]