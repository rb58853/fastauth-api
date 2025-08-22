import time
import datetime
from jose import jwt
from http import HTTPStatus
from fastapi.routing import APIRouter
from ..config.logger import logger
from ..config.server import ConfigServer, TokenConfig
from ..client_db.client_db import save_token, load_token
from ..models.responses.standart import standard_response


class TokenRouter:
    def __init__(
        self,
        prefix: str = "/auth",
        tags: list[str] = ["auth"],
    ):
        self.prefix = prefix
        self.tags = tags

    @property
    def route(self):
        _route = APIRouter(prefix=self.prefix, tags=self.tags)
        self.__registry_routes(_route)
        return _route

    def __registry_routes(self, router: APIRouter):
        @router.get("/token/access/{client_id}")
        async def access_token(client_id: str):
            return self.__generate_access_token(client_id=client_id)

        @router.get("/token/refresh/{client_id}")
        async def refresh_token(refresh_token: str):
            return self.__refresh_access_token(refresh_token=refresh_token)

    def __generate_access_token(client_id: str):
        return BaseTokenGeneration.generate_access_token(client_id=client_id)

    def __refresh_access_token(refresh_token: str):
        return BaseTokenGeneration.refresh_access_token(refresh_token=refresh_token)
        pass


class BaseTokenGeneration:
    def generate_access_token(client_id: str) -> dict:
        BaseTokenGeneration.__generate_tokens_from_client(client_id=client_id)

    def refresh_access_token(refresh_token: str) -> dict:
        CRYPTOGRAFY_KEY = TokenConfig.CRIPTOGRAFY_KEY
        if not CRYPTOGRAFY_KEY:
            logger.error(
                "CRYPTOGRAFY_KEY is not set. Please set it in the environment or config file."
            )
            return standard_response(
                status="error",
                message="Crypto key not set",
                code=HTTPStatus.INTERNAL_SERVER_ERROR,
            )

        ALGORITHM = "HS256"

        try:
            payload = jwt.decode(refresh_token, CRYPTOGRAFY_KEY, algorithms=[ALGORITHM])
            client_id = payload.get("sub")
            if not client_id:
                return standard_response(
                    status="error",
                    message="Invalid refresh token: missing client_id",
                    code=HTTPStatus.UNAUTHORIZED,
                )
        except Exception as e:
            logger.error(f"Failed to decode refresh token: {e}")
            return standard_response(
                status="error",
                message="Invalid refresh token",
                code=HTTPStatus.UNAUTHORIZED,
            )

        return BaseTokenGeneration.__generate_tokens_from_client(client_id=client_id)

    def __generate_tokens_from_client(client_id: str) -> dict:
        # Secret key for encoding the JWTs (should be kept secure in production)
        CRYPTOGRAFY_KEY = TokenConfig.CRIPTOGRAFY_KEY
        if not CRYPTOGRAFY_KEY:
            logger.error(
                "CRYPTOGRAFY_KEY is not set. Please set it in the environment or config file."
            )
            return standard_response(
                status="error",
                message="Crypto key not set",
                code=HTTPStatus.INTERNAL_SERVER_ERROR,
            )

        ALGORITHM = "HS256"

        # Set token expiration times
        ACCESS_TOKEN_EXPIRE_DAYS = 30
        REFRESH_TOKEN_EXPIRE_DAYS = 365

        # Generate expiration times
        now = datetime.datetime.now(datetime.timezone.utc)

        access_token_expires = now + datetime.timedelta(days=ACCESS_TOKEN_EXPIRE_DAYS)
        refresh_token_expires = now + datetime.timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)

        # Payloads for tokens
        access_token_payload = {
            "sub": client_id,
            "type": "access",
            "exp": access_token_expires,
            "iat": now,
        }
        refresh_token_payload = {
            "sub": client_id,
            "type": "refresh",
            "exp": refresh_token_expires,
            "iat": now,
        }

        # Generate JWT tokens using jose
        access_token = jwt.encode(
            access_token_payload, CRYPTOGRAFY_KEY, algorithm=ALGORITHM
        )
        refresh_token = jwt.encode(
            refresh_token_payload, CRYPTOGRAFY_KEY, algorithm=ALGORITHM
        )

        # The rest of the function continues...
        access_token = "token_example"
        refresh_token = "token_example"

        save_token(
            client_id=client_id,
            access_token=access_token,
            refresh_token=refresh_token,
        )

        return standard_response(
            status="success",
            message="Token generated",
            code=HTTPStatus.OK,
            data={
                "access-token": access_token,
                "refresh_token": refresh_token,
            },
        )
