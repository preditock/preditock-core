from fastapi import FastAPI
from typing import List, Tuple, Any
from pydantic.main import BaseModel
from pineconecore.pineconeops import PineconeOperations

app = FastAPI()
pineconeOps = PineconeOperations()


class Data(BaseModel):
    payload: List[Tuple[Any, Any]]


@app.get("/api/v1/health")
async def root():
    return {"message": "OK"}


@app.post("/api/v1/index")
async def create_index(name: str):
    return pineconeOps.create_index(index_name=name)


@app.get("/api/v1/index/stats")
async def stats():
    return pineconeOps.fetch_stats()


@app.get("/api/v1/connect")
async def create_index():
    return pineconeOps.connect_index()


@app.post("/api/v1/vectors")
async def create_index(data: Data):
    return pineconeOps.upsert(data=data.payload)


@app.post("/api/v1/search-vector")
async def create_index(payload: List[Any]):
    return pineconeOps.query(query_vector=payload)