import os
import json
from threading import Lock
from typing import Any, Dict
from pydantic import BaseModel
from fastapi.responses import JSONResponse
from fastapi import APIRouter, HTTPException, status
from ..models.responses.standart import standard_response

router = APIRouter(prefix="/my_db", tags=["data"])
DB_FILE = "simple_db.json"
db_lock = Lock()


class DataModel(BaseModel):
    data: Dict[str, Any]


def load_db() -> Dict[str, Any]:
    """Load the JSON database from file."""
    if not os.path.exists(DB_FILE):
        with open(DB_FILE, "w") as f:
            json.dump({}, f)
        return {}
    with open(DB_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_db(db: Dict[str, Any]) -> None:
    """Save the JSON database to file."""
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(db, f, indent=4)


@router.get("/data/token", response_model=DataModel)
def get_data(client_id: str):
    """
    Retrieve data for a given client_id from the JSON database.
    """
    with db_lock:
        db = load_db()
        if client_id not in db:
            return standard_response(
                status="error",
                message="Client ID not found",
                status_code=status.HTTP_404_NOT_FOUND,
            )
        return standard_response(
            status="success",
            message="Data retrieved successfully",
            status_code=status.HTTP_200_OK,
            data={"data": db[client_id]},
        )


@router.post("/data/token", response_model=DataModel)
def save_data(client_id: str, payload: DataModel):
    """
    Save or update data for a given client_id in the JSON database.
    """
    with db_lock:
        db = load_db()
        db[client_id] = payload.data
        save_db(db)
    return standard_response(
        status="success",
        message="Data saved successfully",
        status_code=status.HTTP_200_OK,
        data=payload.data,
    )
