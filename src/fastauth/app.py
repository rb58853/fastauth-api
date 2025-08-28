from fastapi import FastAPI, APIRouter
from .middleware import AccessTokenMiddleware
from .openapi import FastauthOpenAPI
from .routers import TokenRouter
from .config import DatabaseConfig, ConfigServer, TokenConfig


class Fastauth:
    def __init__(self, config: dict | None = None):
        self.__update_config(config)

    def __update_config(self, config: dict | None):
        if config is not None:
            database_path = config.get("database-api-path", None)
            master_token = config.get("master-token", None)
            cryptography_key = config.get("cryptography-key", None)
            headers = config.get("headers", None)
            master_token_paths = config.get("master-token-paths", [])
            access_token_paths = config.get("access-token-paths", [])

            DatabaseConfig.PATH = database_path or DatabaseConfig.PATH
            ConfigServer.MASTER_TOKEN = master_token or ConfigServer.MASTER_TOKEN
            TokenConfig.CRYPTOGRAPHY_KEY = (
                cryptography_key or TokenConfig.CRYPTOGRAPHY_KEY
            )
            ConfigServer.MASTER_PATHS = master_token_paths + ConfigServer.MASTER_PATHS
            ConfigServer.ACCESS_TOKEN_PATHS = (
                access_token_paths + ConfigServer.ACCESS_TOKEN_PATHS
            )

    def set_auth(
        self,
        fastapp: FastAPI,
        routers: list[APIRouter] = [TokenRouter().route],
    ) -> None:
        """
        Configure authentication for a FastAPI application.
        Adds AccessTokenMiddleware, installs FastauthOpenAPI, and includes the given routers.

        Args:
            fastapp : FastAPI
                The FastAPI application to configure.
            routers : list[APIRouter], optional
                Routers to include (default: TokenRouter().route).

        """
        fastapp.add_middleware(AccessTokenMiddleware)
        openapi: FastauthOpenAPI = FastauthOpenAPI(app=fastapp)
        fastapp.openapi = lambda: openapi()
        for router in routers:
            fastapp.include_router(router=router)
