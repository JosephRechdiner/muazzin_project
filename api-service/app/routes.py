from fastapi import APIRouter, Depends, Request, HTTPException
from app.logger import Logger
from app.redis_client import RedisManager
from app.elastic_client import ElasticManager
import json

def get_redis_manager(request: Request):
    return request.app.state.redis_manager

def get_elastic_manager(request: Request):
    return request.app.state.elastic_manager

route = APIRouter()

@route.get("/metadatas/get-all-metadatas")
def get_all_metadatas(
    elastic_manager: ElasticManager = Depends(get_elastic_manager) 
):
    return elastic_manager.get_all_metadatas()

@route.get("/metadatas/get-metadata-by-id/{file_id}")
def get_metadata_by_id(
    file_id: str, 
    redis_manager: RedisManager = Depends(get_redis_manager), 
    elastic_manager: ElasticManager = Depends(get_elastic_manager) 
):
    redis_metadata = redis_manager.r.get(file_id)
    if redis_metadata:
        return {"Source": "Redis", "metadatas": json.loads(redis_metadata)}
    
    elsatic_metadata = elastic_manager.get_metadata_by_id(file_id)
    redis_manager.r.set(name=file_id, value=json.dumps(elsatic_metadata))
    if elsatic_metadata:
        return {"Source": "ElasticSearch", "metadatas": elsatic_metadata}
    
    raise HTTPException(status_code=404, detail="File id not found")

@route.get("/metadatas/get-top-5-bds-percent")
def get_top_5_bds_percent(
    redis_manager: RedisManager = Depends(get_redis_manager), 
    elastic_manager: ElasticManager = Depends(get_elastic_manager) 
):
    redis_metadata = redis_manager.r.get("top-5-bds-percent")
    if redis_metadata:
        return {"Source": "Redis", "metadatas": json.loads(redis_metadata)}
    
    elsatic_metadata = elastic_manager.get_top_5_bds_percent()
    redis_manager.r.set(name="top-5-bds-percent", value=json.dumps(elsatic_metadata))
    if elsatic_metadata:
        return {"Source": "ElasticSearch", "metadatas": elsatic_metadata}
    
    raise HTTPException(status_code=404, detail="No files metadatas found")

@route.get("/metadatas/get-all-bds")
def get_all_bds(
    redis_manager: RedisManager = Depends(get_redis_manager), 
    elastic_manager: ElasticManager = Depends(get_elastic_manager) 
):
    redis_metadata = redis_manager.r.get("all-bds")
    if redis_metadata:
        return {"Source": "Redis", "metadatas": json.loads(redis_metadata)}
    
    elsatic_metadata = elastic_manager.get_all_bds()
    redis_manager.r.set(name="all-bds", value=json.dumps(elsatic_metadata))
    if elsatic_metadata:
        return {"Source": "ElasticSearch", "metadatas": elsatic_metadata}
    
    raise HTTPException(status_code=404, detail="No files metadatas found")

@route.get("/metadatas/get-bds-greater-then-threshold/{threshold}")
def get_bds_greater_then_threshold(
    threshold: str,
    redis_manager: RedisManager = Depends(get_redis_manager), 
    elastic_manager: ElasticManager = Depends(get_elastic_manager) 
):
    redis_metadata = redis_manager.r.get("bds-greater-then-threshold")
    if redis_metadata:
        return {"Source": "Redis", "metadatas": json.loads(redis_metadata)}
    
    elsatic_metadata = elastic_manager.get_bds_greater_then_threshold(int(threshold))
    redis_manager.r.set(name="bds-greater-then-threshold", value=json.dumps(elsatic_metadata))
    if elsatic_metadata:
        return {"Source": "ElasticSearch", "metadatas": elsatic_metadata}
    
    raise HTTPException(status_code=404, detail="No files metadatas found")

@route.get("/metadatas/get-metadatas-with-word-in-text/{word}")
def get_metadatas_with_word_in_text(
    word: str,
    redis_manager: RedisManager = Depends(get_redis_manager), 
    elastic_manager: ElasticManager = Depends(get_elastic_manager) 
):
    redis_metadata = redis_manager.r.get("metadatas-with-word-in-text")
    if redis_metadata:
        return {"Source": "Redis", "metadatas": json.loads(redis_metadata)}
    
    elsatic_metadata = elastic_manager.get_metadatas_with_word_in_text(word)
    redis_manager.r.set(name="metadatas-with-word-in-text", value=json.dumps(elsatic_metadata))
    if elsatic_metadata:
        return {"Source": "ElasticSearch", "metadatas": elsatic_metadata}
    
    raise HTTPException(status_code=404, detail="No files metadatas found")