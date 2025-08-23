from typing import Any
from fastapi.routing import Match
import os
from ..client_db.client_db import load_access_token


class Params:
    def __init__(self, req) -> None:
        self.req = req
        self.path_params = self.get_path_params()

    def get_path_params(self) -> Any:
        path_params: dict = {}
        routes = self.req.app.router.routes
        for route in routes:
            match, scope = route.matches(self.req)
            if match == Match.FULL:
                path_params = scope["path_params"]
        return path_params

    def get_param(self, paramname):
        return self.path_params[paramname] if paramname in self.path_params else None


def match_key(recived_key, key):
    return key == recived_key


def get_key(client_id: str):
    return load_access_token(client_id=client_id)
