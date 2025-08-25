from ..config import TokenConfig, logger
from jose import jwt

ALGORITHM = "HS256"


class TokenCriptografy:
    def decode(token):
        if not TokenConfig.CRIPTOGRAFY_KEY:
            raise Exception(
                "CRYPTOGRAFY_KEY is not set. Please set it in the environment or config file."
            )
        try:
            return jwt.decode(
                token,
                TokenConfig.CRIPTOGRAFY_KEY,
                algorithms=[ALGORITHM],
            )
        except Exception as e:
            raise Exception(f"Error decoding token: {e}")

    def encode(payload):
        return jwt.encode(
            payload,
            TokenConfig.CRIPTOGRAFY_KEY,
            algorithm=ALGORITHM,
        )
