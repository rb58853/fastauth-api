from fastapi import FastAPI
from http import HTTPStatus
from pydantic import BaseModel

app = FastAPI(root_path="/test-api")


@app.get(
    "/health",
)
async def health_check():
    return {"status": "healthy"}


@app.get(
    "/access/health",
)
async def access_health_check():
    return {
        "service": "access health that need access token",
        "status": "healthy",
    }


@app.get(
    "/master/health",
)
async def access_health_check():
    return {
        "service": "master health that need master token",
        "status": "healthy",
    }
