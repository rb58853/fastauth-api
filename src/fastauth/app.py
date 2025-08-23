from fastapi import FastAPI, APIRouter
from .routers.jsondb import router as jsondb_router
from .middleware import AccessTokenMiddleware
from .openapi import FastauthOpenAPI
from .routers import TokenRouter


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
