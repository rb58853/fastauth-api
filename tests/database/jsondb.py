import os
import json
from threading import Lock
from typing import Any, Dict
from pydantic import BaseModel
from fastapi import APIRouter, status
from utils.standart_response import standard_response
from http import HTTPStatus

router = APIRouter(prefix="/data", tags=["data"])
DB_FILE = "data/simple_db.json"
db_lock = Lock()


class DataModel(BaseModel):
    data: Dict[str, Any] | None


def load_db() -> Dict[str, Any]:
    """Load the JSON database from file."""
    dir_path = "/".join(DB_FILE.split("/")[:-1])
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

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


@router.get("/token")
async def get_data(client_id: str):
    """
    Retrieve data for a given client_id from the JSON database.
    """
    with db_lock:
        db = load_db()
        if client_id not in db:
            return standard_response(
                status="error",
                message="Client ID not found",
                code=HTTPStatus.NOT_FOUND,
                details={"client_id": client_id},
            )
        return standard_response(
            status="success",
            message="Data retrieved successfully",
            code=HTTPStatus.OK,
            data={"client_id": db[client_id]},
        )


@router.post("/token", response_model=DataModel)
async def save_data(client_id: str, payload: DataModel):
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
        code=HTTPStatus.OK,
        data={"client_id": client_id} | payload.data,
    )
