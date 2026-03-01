FROM python:3.11-slim

WORKDIR /app

COPY processor-service/requirement.txt .

RUN pip install -r requirement.txt

COPY ./podcasts /app/podcasts

COPY ./shared /app/shared

CMD [ "python", "app/main.py" ]
