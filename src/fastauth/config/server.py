import os


class ConfigServer:
    MASTER_TOKEN: str | None = os.getenv("MASTER_TOKEN", None)

    # En modo desarrollo, todas las path requieren master key
    MASTER_PATHS: list[str] = ["/token"]
    ACCESS_TOKEN_PATHS: list[str] = []
    REFRESH_TOKEN_PATHS: list[str] = []
