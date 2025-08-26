from functools import wraps
from fastapi import HTTPException, WebSocket
from proto import Enum
from .utils import Params, match_key, get_access_token
from ..utils import TokenCriptografy
from ..config import logger, ConfigServer


class TokenType(Enum):
    ACCESS = "access"
    MASTER = "master"


def websocket_middleware(token_type: TokenType = TokenType.ACCESS):
    def decorator(func):
        @wraps(func)
        async def wrapper(websocket: WebSocket, *args, **kwargs):
            disconnected: bool = False
            if token_type == TokenType.ACCESS:
                token = websocket.headers.get("ACCESS-TOKEN")
                try:
                    payload = TokenCriptografy.decode(token)
                    client_id = payload.get("client_id")
                    client_key = get_access_token(client_id)
                    if token is None or not match_key(token, client_key):
                        await disconnect(websocket=websocket)
                        disconnected = True

                except Exception:
                    await disconnect(websocket=websocket)

            if token_type == TokenType.MASTER:
                token = websocket.headers.get("MASTER-TOKEN")
                master_token: str = ConfigServer.MASTER_TOKEN

                if token is None or master_token != token:
                    await disconnect(
                        websocket=websocket, detail="Unauthorized Master Token"
                    )
                    disconnected = True

            if not disconnected:
                return await func(websocket, *args, **kwargs)

        return wrapper

    return decorator


async def disconnect(websocket: WebSocket, detail: str = "Unauthrized ACCESS-TOKEN"):
    await websocket.accept()
    await websocket.send_json({"status": "disconnected", "detail": detail})
    await websocket.close(code=1008)
    raise HTTPException(status_code=401, detail=detail)
