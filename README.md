# Fastauth-api

## Instalacion

```shell
pip install fasauth-api
```

## Requisitos

- Usar la ruta de endpoint especifica para guardar y cargar tokens de acceso y actualización desde una base de datos

## Config File

Debes crear un archivo llamado `fastauth.config.json` en la direccion raiz del proyecto. Luego llenarlo con los siguientes datos:

```json
{
    "app-name": "fastauth",
    "database-api-url": "http://127.0.0.1:8000/my_db/data",
    "master-token": "<your-master-token>",
    "crypto-key": "<your-32-byte-crypto-key>",
    "master-token-paths": [
        "list of your root endpoints that need master token for use",
        "...",
        "..."
    ],
    "access-token-paths": [
        "list of your root endpoints that need access token for use",
        "...",
        "..."
    ]
}
```

## Tokens Genaration utils

### Criptografy key

```python
# CRIPTOGRAFY_KEY auto generation
from fastauth.utils import generate_criptografy_key
generate_criptografy_key()
```

### Master Token

```python
# Master Token auto generation
from cryptography.fernet import Fernet
from fastauth.utils import writekey2env

key = Fernet.generate_key().decode()
writekey2env(key=key, name="MASTER_TOKEN")
```

## Usage example

```python
from fastapi import FastAPI
from fastauth import set_auth

app = FastAPI(root_path="/test-api")
set_auth(app)


@app.get(
    "/health",
)
async def health_check():
    return {"status": "healthy"}


@app.get(
    "/access/health",
)
async def access_health_check():
    return {
        "service": "access health that need access token",
        "status": "healthy",
    }


@app.get(
    "/master/health",
)
async def access_health_check():
    return {
        "service": "master health that need master token",
        "status": "healthy",
    }
```
