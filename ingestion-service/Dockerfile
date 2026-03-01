FROM python:3.11-slim

WORKDIR /app

COPY ./ingestion-service/requirements.txt .

RUN pip install -r requirements.txt

COPY  ./podcasts /app/podcasts
COPY  ./shared /app/shared

COPY ./ingestion-service .

EXPOSE 8000

CMD [ "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000" ]