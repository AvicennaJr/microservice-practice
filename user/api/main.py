from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import models
from db.session import engine

from .endpoints import user

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user.router)
