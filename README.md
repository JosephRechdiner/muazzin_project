#  muazzin_project

##  First part

The first part presents the flow of a podcast metadata extraction,  
including saving the raw file into MongoDB and indexing metadata in Elastic Search.

Of coures all logs are gonna be saved in ElasticSearch as an independent index.

---

##  Services Architecture

Two services are involved in this process, ingestion serivce and processor service.  
both services are containerized in docker containers, act independently, and using kafka for communicating with each other.

---

##  Ingestion Service

Ingestion service is exposed to the outside world using fastapi and uvicorn.  
A single fastapi route acts as a trigger to start the process.

---

##  Processor Service

Processor service acts as a kafka consumer in order to get all podcasts metadata one by one,  
and responsible for actual saving into MongoDB and indexing in ElasticSearch