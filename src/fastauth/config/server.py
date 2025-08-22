import os
import json
from .logger import logger

config: dict = {}
try:
    with open(".fastauth.config.json", "r") as f:
        config = json.load(f)
except FileNotFoundError:
    logger.error("Configuration file not found. Please create .fastauth.config.json.")


class ConfigServer:
    MASTER_TOKEN: str | None = os.getenv("MASTER_TOKEN", None) | config.get(
        "master-token", None
    )

    MASTER_PATHS: list[str] = ["/token/access"] + config.get("master-token-paths", [])
    ACCESS_TOKEN_PATHS: list[str] = config.get("access-token-paths", [])

class TokenConfig:
    CRIPTOGRAFY_KEY: str = os.getenv("CRYPTOGRAFY_KEY", None) or config.get(
        "crypto-key", None
    )