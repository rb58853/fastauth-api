# Fastauth — Official Documentation

Last updated: 2025-08-25  
Format: comprehensive, professional, and structured documentation based on the source code and provided examples.

---

## Table of Contents

- [Overview](#overview)
- [Key Features](#key-features)
- [Architecture & Components](#architecture--components)
- [Quick Install](#quick-install)
- [Configuration](#configuration)
  - [fastauth.config.json (example)](#1-configuration-file--fastauthconfigjson)
  - [Environment variables (.env)](#2-environment-variables-alternative--precedence)
- [Quick Start (FastAPI integration)](#quick-start-fastapi-integration)
- [Public Endpoints](#public-endpoints)
  - /auth/token/new
  - /auth/token/refresh
- [Middleware & WebSocket Protection](#middleware--websocket)
- [Token Persistence (expected contract)](#token-persistence-expected-contract)
- [Utilities (key generation and .env helpers)](#utilities)
- [OpenAPI / Swagger integration](#openapi--swagger)
- [Included Examples](#included-examples)
  - apps/basic_api
  - databases/json_database
- [Security Best Practices](#security-best-practices)
- [Roadmap / TODO](#roadmap--todo)

---

## Overview

Fastauth is a lightweight FastAPI library/middleware that simplifies issuing, validating and managing tokens (access + refresh), provides cryptographic key utilities, and integrates with an external token persistence API. It is configurable, easy to integrate, and designed for production use.

## Key Features

- Access and refresh token generation (JWT, HS256).
- Middleware enforcing two token types: `MASTER-TOKEN` and `ACCESS-TOKEN`.
- Token storage and retrieval via a configurable external REST API.
- Custom OpenAPI that adds security schemes for token headers.
- Utilities to generate and persist cryptographic keys into `.env`.
- WebSocket protection decorator based on Access Token.
- Logger with rotation and customizable formatting.

## Architecture & Components

Project layout (high-level):

- `fastauth/` (main package)
  - `quick_app.py` — helper to apply middleware and routers to a FastAPI app.
  - `routers/auth.py` — token generation and refresh router (`TokenRouter`, `BaseTokenGeneration`).
  - `middleware/middleware.py` — HTTP middleware (`AccessTokenMiddleware`) for token validation.
  - `middleware/websocket.py` — `websocket_middleware` decorator for WS protection.
  - `middleware/utils.py` — helpers for path checks, key validation and reading tokens from DB.
  - `utils/`
    - `cryptography_key.py` — generates a Fernet key and optionally writes to `.env`.
    - `envfile.py` — read/write helpers for `.env` variables.
    - `decode_token.py` — JWT encode/decode (uses `jose`).
  - `client_db/client_db.py` — HTTP client for external token persistence (GET/POST).
  - `openapi/openapi.py` — custom OpenAPI builder that injects security schemes.
  - `config/`
    - `server.py` — loads `fastauth.config.json` and environment variables; exposes `ConfigServer`, `TokenConfig`, `DatabaseConfig`.
    - `logger.py` — logger configuration and rotating file handler.
  - `models/responses/standart.py` — helper for standardized JSON responses.

## Quick Install

From PyPI (hypothetical package name):

```bash
pip install fastauth-api
```

From local repository:

```bash
pip install -e .
```

## Configuration

### 1) Configuration file — `fastauth.config.json`

Place at project root (default `fastauth.config.json`). If absent, `logger` will report an error.

Example (`fastauth.config.example.json`):

```json
{
    "app_name": "fastauth-api",
    "database_api_path": "http://127.0.0.1:6789/mydb/data",
    "master_token": "<your-master-token>",
    "cryptography_key": "<your-32-byte-cryptography-key>",
    "master_token_paths": [ "/master" ],
    "access_token_paths": [ "/access" ]
}
```

Primary fields:

- `database-api-path`: base URL of the token persistence service (`GET`/`POST /token?client_id=...`).
- `master-token`: privileged token for administrative routes.
- `cryptography-key`: key used for signing/verifying JWTs (can also be provided via env var `CRYPTOGRAPHY_KEY`).
- `master-token-paths`: route prefixes that require `MASTER-TOKEN`.
- `access-token-paths`: route prefixes that require `ACCESS-TOKEN`.

### 2) Environment variables (alternative / precedence)

- `CRYPTOGRAPHY_KEY` — key used for JWT signing (used if not present in config file).
- `MASTER_TOKEN` — master token (used if not present in config file).

Example `.env` (included in `examples/apps/basic_api/.env`):

```
CRYPTOGRAPHY_KEY=kAONxbkATfyk3...A6N4=
MASTER_TOKEN=kAONxbkATfyk3...A6N4=
```

Precedence: values in the configuration file take precedence. If missing there, environment variables are used.

## Quick Start (FastAPI integration)

Minimal example (`examples/apps/basic_api/api.py`):

```py
from fastapi import FastAPI
from fastauth import Fastauth

app = FastAPI(root_path="/test-api")
auth=Fastauth()
auth.set_auth(app)  # applies middleware, routers and custom OpenAPI

@app.get("/")
async def root():
        return RedirectResponse(url="/docs")
```

`auth.set_auth` performs:

- Adds `AccessTokenMiddleware` to the app.
- Replaces `app.openapi` with Fastauth's OpenAPI builder.
- Includes the default `TokenRouter` under `/auth`.

## Public Endpoints

Provided by `TokenRouter`:

- `GET /auth/token/new?client_id=<client_id?>`
  - Generates a new `access_token` and `refresh_token`.
  - If `client_id` is omitted, a UUID is generated.
  - Saves tokens using `client_db.save_token`.
  - Returns a standardized JSON response with `{ client_id, access_token, refresh_token }`.

- `GET /auth/token/refresh?refresh_token=<token>`
  - Validates the provided refresh token (decodes with `CRYPTOGRAPHY_KEY`).
  - If valid, issues a new token pair for the `client_id` contained in the refresh token.
  - Uses standard HTTP codes and structured error messages on failure.

Notes:

- Encoding/decoding uses `jose.jwt` with algorithm `HS256`.
- Tokens include `exp` (expiration) and `iat` (issued at), using UTC timestamps.
- Default expirations: access = 30 days, refresh = 365 days (configurable by changing code).

## Middleware & WebSocket

### 1) AccessTokenMiddleware (based on `BaseHTTPMiddleware`)

For each request:

- Logs the requested path.
- Checks if the path requires `MASTER-TOKEN` (via `ConfigServer.MASTER_PATHS`):
  - If so, compares header `MASTER-TOKEN` against `ConfigServer.MASTER_TOKEN`.
- Checks if the path requires `ACCESS-TOKEN` (via `ConfigServer.ACCESS_TOKEN_PATHS`):
  - If so, reads header `ACCESS-TOKEN`, decodes JWT (`TokenCriptografy.decode`) and verifies it matches the token stored in the persistence API (`client_db.load_access_token`).
- Returns `401` or `500` JSON responses when validation fails.

### 2) `websocket_middleware` (decorator)

- Reads `ACCESS-TOKEN` header from the WebSocket connection.
- Decodes the token payload using `TokenCriptografy.decode`.
- Extracts `client_id` and verifies the received token against the persisted token.
- On failure, accepts the connection, sends a JSON message with `disconnected`, and closes with code `1008`.

## Token Persistence (expected contract)

Fastauth delegates token storage to an external REST service. Example implementation available in `examples/databases/json_database`.

API contract:

- Base path: `/mydb/data`
- Resource: `/data/token`
  - `GET /data/token?client_id=<client_id>` → returns standardized JSON with `data` containing `{ access_token, refresh_token }`.
  - `POST /data/token?client_id=<client_id>` with body `{"data": {"access_token": "...", "refresh_token": "..."}}` to save tokens.

Client usage (`client_db.client_db`):

- `save_token` performs `POST {DATABASE_API_URL}/token?client_id={client_id}` with `{ "data": { access_token, refresh_token } }`.
- `load_access_token` performs `GET` and expects a JSON whose `data` contains `access_token`.

## Utilities

- `generate_cryptography_key(add2env: bool = True)` (`fastauth.utils.cryptography_key`)
  - Generates a Fernet key (`Fernet.generate_key().decode()`).
  - Optionally writes the key to a `.env` file using `utils.envfile.write_key`.
  - If the key already exists, the interactive tool prompts for replacement when run interactively.

- `.env` helpers (`fastauth.utils.envfile`)
  - `write_key(key, name, file_path=".env", override=True)` — writes or replaces a variable in a `.env`.
  - `read_key(name, file_path=".env")` — reads a variable value from a `.env`.
  - `key_in(name, file_path=".env")` — returns `True` if the variable exists.

- `TokenCriptografy` (`fastauth.utils.decode_token`)
  - `encode(payload)` and `decode(token)` using `jose.jwt` with `TokenConfig.CRYPTOGRAPHY_KEY`.
  - If the key is not configured, an error is logged and an exception is raised.

## OpenAPI / Swagger

`FastauthOpenAPI` (`openapi/openapi.py`) builds a custom OpenAPI schema:

- Adds `components.securitySchemes`:
  - `AccessTokenHeader` — `apiKey`, in: `header`, name: `ACCESS-TOKEN`
  - `MasterTokenHeader` — `apiKey`, in: `header`, name: `MASTER-TOKEN`
- Applies the security scheme to all endpoints by default (both headers).
- `auth.set_auth(app)` overrides `app.openapi` with this implementation.

## Included Examples

1. `examples/apps/basic_api`
     - Minimal app demonstrating `set_auth`.
     - Uses `root_path="/test-api"`.
     - Routes protected by prefixes `/access/*` and `/master/*` per `fastauth.config.json` or `.env`.
     - Includes example `fastauth.config.json` and `.env`.

2. `examples/databases/json_database`
     - Minimal token persistence API saving tokens into `examples/databases/json_database/data/simple_db.json`.
     - Endpoint: `/mydb/data/token`
     - Thread-safe implementation using a `Lock`.
     - Standardized responses: `{ status, message, code, data, details }`.

## Security Best Practices

- Always deploy behind HTTPS to protect tokens in transit.
- Keep `CRYPTOGRAPHY_KEY` and `MASTER_TOKEN` out of version control (use `.env` or secret manager).
- Limit the use of `MASTER_TOKEN` to administrative operations only.
- Plan and document key rotation and migration for persisted tokens if `CRYPTOGRAPHY_KEY` changes.
- Store refresh tokens securely on clients (e.g., HttpOnly cookies for browsers).
- Protect the token persistence API with authentication, IP whitelisting or firewall rules.

## Roadmap / TODO

- Secure migration of persisted tokens when rotating `CRYPTOGRAPHY_KEY`.
- Support for multiple token payload formats.
- Improve and document the WebSocket decorator.
- Add automated tests and CI.
- Make token expirations and JWT algorithm configurable.
- Token revocation (blacklists / revocation lists).

## Contribution

- Open issues with traces and reproduction steps.
- Follow code style and open pull requests for fixes and features.
- Maintain semantic compatibility for public APIs (routers / middleware).

## License

This project is licensed under the MIT License. Keep attribution and respect the license when forking or redistributing.
