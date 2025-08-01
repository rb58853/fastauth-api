from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi


class CustomOpenAPI:
    def __init__(self, app: FastAPI):
        self.app = app

    def __call__(self):
        if self.app.openapi_schema:
            return self.app.openapi_schema

        openapi_schema = get_openapi(
            title="Cliniscript API",
            version="0.0.1",
            description="Custom OpenAPI schema with token authorization",
            routes=self.app.routes,
        )

        openapi_schema["components"]["securitySchemes"] = {
            "AccessTokenHeader": {
                "type": "apiKey",
                "name": "ACCESS-TOKEN",
                "in": "header",
            },
            "MasterTokenHeader": {
                "type": "apiKey",
                "name": "MASTER-TOKEN",
                "in": "header",
            },
        }

        for path in openapi_schema["paths"].values():
            for method in path.values():
                method["security"] = [
                    {
                        "AccessTokenHeader": [],
                        "MasterTokenHeader": [],
                    }
                ]

        self.app.openapi_schema = openapi_schema
        return self.app.openapi_schema
