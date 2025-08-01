"""
Cliente que conecta con la base de datos. Es imprescindible que la base de datos posea los endpoints:
`POST`: ```path/to/url/root/token/save?client_id=<client_id>```
`GET`: ```path/to/url/root/token/load?client_id=<client_id>```
"""

DATABASE_API_URL: str = ""


async def save_token(client_id: str, token: str) -> bool:
    pass


def load_token(client_id: str) -> str:
    pass
