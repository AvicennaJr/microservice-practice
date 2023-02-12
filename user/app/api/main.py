from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.db.session import engine

from .endpoints import user

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user.router)  # add users routes
