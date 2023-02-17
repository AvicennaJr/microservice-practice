from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.models import Base
from db import engine

Base.metadata.create_all(bind=engine)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def hello():
    return {"hello": "world"}
