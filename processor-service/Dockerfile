FROM python:3.11-slim

WORKDIR /app

COPY ./processor-service/requirements.txt .

RUN pip install -r requirements.txt

COPY ./podcasts /app/podcasts
COPY ./shared /app/shared

COPY ./processor-service .

CMD [ "python", "-m", "app.main" ]
