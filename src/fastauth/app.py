from fastapi import FastAPI, APIRouter
from .middleware import AccessTokenMiddleware, websocket_middleware
from .openapi import FastauthOpenAPI
from .routers import TokenRouter, jsondb_router


def set_auth(
    fastapp: FastAPI,
    routes: list[APIRouter] = [
        TokenRouter().route,
        jsondb_router,
    ],
) -> None:
    """
    Genera middleware, token routes y openapi automaticamente con los valores default.
    """
    fastapp.add_middleware(AccessTokenMiddleware)
    openapi: FastauthOpenAPI = FastauthOpenAPI(app=fastapp)
    fastapp.openapi = lambda: openapi()
    for route in routes:
        fastapp.add_route(route=route)
