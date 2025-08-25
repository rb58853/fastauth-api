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

Fastauth-api es un middleware de autenticación diseñado para integrarse con aplicaciones `FastAPI`. Proporciona generación y manejo de tokens de acceso y refresh, así como utilidades para cifrado y gestión segura de claves. Está pensado para facilitar la implementación de políticas de autenticación basadas en tokens y su almacenamiento en un backend genérico expuesto por una API REST.

Resumen de características principales:

- Generación de Access Tokens y Refresh Tokens.
- Integración con una API externa para persistencia de tokens.
- Soporte para una "master token" que habilita operaciones privilegiadas.
- Utilidades para generar y almacenar claves de cifrado seguras.
- Middleware configurable para proteger rutas por niveles (master / access).

## Instalación

Instale desde PyPI:

```bash
pip install fasauth-api
```

<!-- ## Requisitos y consideraciones

- Definir un endpoint (API) donde se guarden y recuperen tokens persistidos. La URL de esa API se especifica en la configuración.
- Decidir si usará una "master token" para operaciones administrativas (recomendado para emisión inicial de tokens).
- Proveer una clave de cifrado (32 bytes) para proteger payloads y tokens en reposo. -->

## Archivo de configuración

Cree en la raíz del proyecto un archivo llamado `fastauth.config.json` con la estructura mínima:

```json
{
    "app-name": "fastauth",
    "database-api-url": "http://127.0.0.1:8000/mydb/data",
    "master-token": "<your-master-token>",
    "criptografy-key": "<your-32-byte-criptografy-key>",
    "master-token-paths": [
        "/master/*"
    ],
    "access-token-paths": [
        "/access/*"
    ]
}
```

En esta configuración:

- `app-name`: nombre identificador de la aplicación.
- `database-api-url`: endpoint de la API encargada de persistir tokens.
- `master-token`: (opcional) token con privilegios para operaciones administrativas.
- `criptografy-key`: (opcional) clave usada para cifrar/decrifrar payloads.
- `master-token-paths` y `access-token-paths`: patrones de rutas que exigen validación por tipo de token.

Si no incluye `master-token` o `criptografy-key` en el archivo, puede definirlas mediante variables de entorno (ver siguiente sección).

Consulte el archivo de ejemplo: [`fastauth.config.example.json`](./fastauth.config.example.json)

### Variables de entorno (alternativa)

Puede definir las claves sensibles en su `.env`:

```
CRIPTOGRAFY_KEY=kAON......................A6N4=
MASTER_TOKEN=kAON......................A6N4=
```

Cuando ambas fuentes (archivo config y variables de entorno) estén disponibles, se prioriza el valor del archivo de configuración.

## Generación de claves y tokens (utilidades)

Fastauth incluye utilidades para generar claves seguras y escribir variables al entorno:

- Generar una CRIPTOGRAFY_KEY:

```python
from fastauth.utils import generate_criptografy_key
generate_criptografy_key()
```

- Generar y escribir una MASTER_TOKEN en el archivo de entorno:

```python
from cryptography.fernet import Fernet
from fastauth.utils import writekey2env

key = Fernet.generate_key().decode()
writekey2env(key=key, name="MASTER_TOKEN")
```

Estas utilidades permiten crear claves seguras compatibles con el sistema interno de cifrado.

## Uso básico (integración con FastAPI)

Ejemplo de integración mínima:

```python
from fastapi import FastAPI
from fastauth import set_auth

app = FastAPI(root_path="/test-api")
set_auth(app)

@app.get("/health")
async def health_check():
        return {"status": "healthy"}

@app.get("/access/health")
async def access_health_check():
        return {"service": "access health that need access token", "status": "healthy"}

@app.get("/master/health")
async def master_health_check():
        return {"service": "master health that need master token", "status": "healthy"}
```

`set_auth(app)` aplica el middleware y los routers necesarios para la emisión y verificación de tokens según la configuración.

[ver mas ejemplos](./examples/EXAMPLES.md)

## Uso del endpoint /auth/token

El endpoint de tokens es el mecanismo central para emitir y, opcionalmente, persistir tokens. A continuación se describe su propósito, comportamiento esperado y ejemplos de uso. Para la implementación concreta, puede consultar el archivo de código en: `./src/fastauth/routers/auth.py`.

Propósito

- Emitir pares de tokens (access token + refresh token) para un sujeto (usuario, servicio o entidad).
- Almacenar metadatos asociados al token (según la API de base de datos configurada).
- Sugerir flujos para refrescar tokens y revocarlos.

Autenticación requerida

- Emisión inicial: en escenarios administrativos la emisión puede requerir la MASTER_TOKEN. Esto se transmite normalmente a través del encabezado:
  - Authorization: Bearer <MASTER_TOKEN>
  - o mediante un encabezado personalizado, por ejemplo X-Master-Token.
- Uso normal (refresh / introspección): operaciones con refresh tokens usan el refresh token en el cuerpo de la petición o en Authorization según el diseño.

Métodos y rutas (convenciones)

- POST /auth/token — emitir un nuevo par (access + refresh) o persistir/registrar un token.
- POST /auth/refresh — intercambiar un refresh token por un nuevo access token (y opcionalmente nuevo refresh token).
- POST /auth/revoke — revocar un token (access o refresh), marcándolo en la capa de persistencia.

Request (ejemplos indicativos)

- Emisión por master token (administrativo):

Headers:

```
Authorization: Bearer <MASTER_TOKEN>
Content-Type: application/json
```

Body:

```json
{
    "sub": "user:1234",
    "scopes": ["read", "write"],
    "expires_in": 3600,
    "meta": {
        "ip": "198.51.100.1",
        "device": "web"
    }
}
```

- Refresh (cliente con refresh token):

Headers:

```
Content-Type: application/json
```

Body:

```json
{
    "refresh_token": "<existing-refresh-token>"
}
```

Responses (estructura típica)

- Éxito emisión (HTTP 201 o 200):

```json
{
    "access_token": "<jwt-or-encrypted-token>",
    "token_type": "bearer",
    "expires_in": 3600,
    "refresh_token": "<refresh-token>",
    "issued_at": "2025-08-25T12:00:00Z",
    "meta": {
        "sub": "user:1234",
        "scopes": ["read", "write"]
    }
}
```

- Éxito refresh:

```json
{
    "access_token": "<new-access-token>",
    "expires_in": 3600,
    "refresh_token": "<new-or-same-refresh-token>"
}
```

- Error (ejemplo):

HTTP 401 / 400 con payload:

```json
{
    "detail": "Master token inválido o expirado"
}
```

Persistencia

- Cuando la configuración incluye `database-api-url`, el router intentará registrar tokens y metadatos en ese endpoint. La estructura y contract de la API remota depende de la implementación de backend; Fastauth espera un endpoint REST que acepte POST/GET/DELETE para gestionar tokens.

Buenas prácticas de uso

- Mantener la CRIPTOGRAFY_KEY fuera del control de versiones y solo en entornos seguros.
- Limitar la difusión de MASTER_TOKEN: usarlo únicamente para operaciones administrativas centralizadas.
- Configurar expiraciones sensatas para access tokens y refresh tokens.
- Implementar revocación en la capa de persistencia para invalidar tokens comprometidos.
- Proteger la ruta de la API de persistencia mediante autenticación y listado blanco de IPs si es posible.

Ejemplos prácticos (cURL)

- Solicitar token (emisión con master token):

```bash
curl -X POST "https://api.example.com/auth/token" \
    -H "Authorization: Bearer <MASTER_TOKEN>" \
    -H "Content-Type: application/json" \
    -d '{"sub":"user:1234", "scopes":["read"], "expires_in":3600}'
```

- Refrescar token:

```bash
curl -X POST "https://api.example.com/auth/refresh" \
    -H "Content-Type: application/json" \
    -d '{"refresh_token":"<refresh-token>"}'
```

Seguridad y consideraciones finales

- Los tokens deben transmitirse siempre por HTTPS.
- Guardar refresh tokens en almacenamiento seguro (por ejemplo, cookies HttpOnly en navegadores o almacenamiento cifrado en clientes).
- Rotación periódica de CRIPTOGRAFY_KEY puede requerir migración de tokens almacenados; el README incluye este ítem como TODO.

## TODO / Roadmap

- Implementar migración segura de la base de datos al rotar la CRIPTOGRAFY_KEY.
- Ampliar compatibilidad con distintos formatos de payloads cifrados.
- Reestructurar y escalar la implementación del decorador para websockets.
- Documentar exhaustivamente cada endpoint para que esté disponible en Swagger/OpenAPI.

## Licencia

Proyecto bajo licencia MIT. Consulte el archivo LICENSE para detalles.

Si necesita ejemplos específicos de payloads o adaptar los endpoints a su API de persistencia, proporcione la especificación de esa API y se entregarán ejemplos concretos de integración.
