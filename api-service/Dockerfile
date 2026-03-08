FROM python:3.11-slim

WORKDIR /app

COPY api-service/requirements.txt .

RUN pip install -r requirements.txt

COPY ./shared /app/shared

COPY ./api-service .

EXPOSE 8050

CMD [ "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8050" ]