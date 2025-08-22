"""
Cliente que conecta con la base de datos. Es imprescindible que la base de datos posea los endpoints:
`POST`: ```path/to/url/root/token/save?client_id=<client_id>```
`GET`: ```path/to/url/root/token/load?client_id=<client_id>```
"""

DATABASE_API_URL: str = ""


async def save_token(
    client_id: str,
    access_token: str,
    refresh_token: str,
) -> bool:
    pass


def load_access_token(client_id: str) -> str:
    pass


def load_refresh_token(client_id: str) -> str:
    pass
