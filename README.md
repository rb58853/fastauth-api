# Fastauth-api

## Instalacion

```shell
pip install fasauth-api
```

## Requisitos

s- Usar la ruta de endpoint especifica para guardar y cargar tokens de acceso y actualización desde una base de datos

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

## Usage example
