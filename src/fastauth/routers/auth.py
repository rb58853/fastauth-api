from fastapi.routing import APIRouter


class TokenRouter:
    def __init__(self, prefix: str = "/auth", tags: list[str] = ["auth"]):
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
            return self.__access_token(client_id=client_id)

        @router.get("/token/refresh/{client_id}")
        async def refresh_token(client_id: str):
            return self.__refresh_token(client_id)

    def __access_token(client_id: str):
        pass

    def __refresh_token(client_id: str):
        pass
