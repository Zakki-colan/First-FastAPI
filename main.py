from contextlib import asynccontextmanager

from fastapi import FastAPI

import models
from database import Base, engine
from routers import tasks


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create missing tables at application startup.
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title="Task Manager API",
    description="A sample API with FastAPI and SQLAlchemy",
    version="1.0.0",
    lifespan=lifespan,
)

app.include_router(tasks.router)


@app.get("/")
def home():
    return {
        "message": "Welcome to the Task Manager API",
        "docs": "/docs",
    }


@app.get("/health")
def health():
    return {"status": "healthy"}