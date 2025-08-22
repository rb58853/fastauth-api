from fastapi import FastAPI
from .middleware import AccessTokenMiddleware
from .openapi import CustomOpenAPI
from .routers import TokenRouter


def set_auth(
    fastapp: FastAPI,
    route=TokenRouter().route,
) -> None:
    """
    Genera middleware, token routes y openapi automaticamente con los valores default.
    """
    fastapp.add_middleware(AccessTokenMiddleware)
    fastapp.add_route(route=route)
