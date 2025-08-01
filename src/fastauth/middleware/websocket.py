from fastapi import HTTPException, WebSocket
from .utils import Params, match_key, get_key
from functools import wraps


def websocket_middleware(func):
    @wraps(func)
    async def wrapper(websocket: WebSocket, *args, **kwargs):
        params = Params(websocket)
        client_id = params.get_param("client_id")
        request_api_key = websocket.headers.get("API-KEY")
        client_key = get_key(client_id)

        print(f"api_key: {request_api_key}")
        print(f"client-key: {client_key}")

        if request_api_key is None or not match_key(request_api_key, client_key):
            await websocket.accept()
            await websocket.send_json(
                {"status": "disconnected", "detail": "Unauthrized api-key"}
            )
            await websocket.close(code=1008)
            raise HTTPException(status_code=401, detail="Unauthrized api-key")

        else:
            return await func(websocket, *args, **kwargs)

    return wrapper


