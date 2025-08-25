# Fastauth-api

<div align = center>

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)
[![Stars](https://img.shields.io/github/stars/rb58853/fastauth-api?style=flat&logo=github)](https://github.com/rb58853/fastauth-api/stargazers)
[![Forks](https://img.shields.io/github/forks/rb58853/fastauth-api?style=flat&logo=github)](https://github.com/rb58853/fastauth-api/network/members)
[![Watchers](https://img.shields.io/github/watchers/rb58853/fastauth-api?style=flat&logo=github)](https://github.com/rb58853/fastauth-api)
[![Contributors](https://img.shields.io/github/contributors/rb58853/fastauth-api)](https://github.com/rb58853/fastauth-api/graphs/contributors)
[![Commit activity](https://img.shields.io/github/commit-activity/m/rb58853/fastauth-api)](https://github.com/rb58853/fastauth-api/commits)
[![Last commit](https://img.shields.io/github/last-commit/rb58853/fastauth-api.svg?style=flat)](https://github.com/rb58853/fastauth-api/commits)

<!-- [![PyPI Downloads](https://static.pepy.tech/badge/fastauth-api)](https://pepy.tech/projects/fastauth-api) -->
<!-- [![Version](https://img.shields.io/pypi/v/fastauth-api?color=%2334D058&label=Version)](https://pypi.org/project/fastauth-api) -->

</div>

Fastauth es un middleware personalizado para usarse con tokens autogenerados, con sistema de generacion de tokens y de refresh tokens. El objetivo es facilitar el desarrollo de middlewares ajustables a cualquier proyecto de python en `Fastapi`.

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
    "database-api-url": "http://127.0.0.1:8000/mydb/data",
    "master-token": "<your-master-token>",
    "criptografy-key": "<your-32-byte-criptografy-key>",
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

[ver config.example](fastauth.config.example.json)

### Details

- `"master-token"` es un campo opcional, en caso de no tenerlo en esta configuracion, entonces es obligado tener una variable llamada `MASTER_TOKEN` en el archivo de entorno `.env`.
- `"criptografy-key"` es un campo opcional, en caso de no tenerlo en esta configuracion, entonces es obligado tener una variable llamada `CRIPTOGRAFY_KEY` en el archivo de entorno `.env`.

```.env
CRIPTOGRAFY_KEY=kAON......................A6N4=
MASTER_TOKEN=kAON......................A6N4=
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

## TODO

- Migracion de base de datos al cambiar criptografy key
- Mejorar la compatibilidad con cualquier payload que se encripte
- Escalar la estructura del codigo del websocket decorator
- Documentar detalladamente el codigo y los endpoints para el swagguer
