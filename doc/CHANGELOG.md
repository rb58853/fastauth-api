# Changelog

## version 0.0.2 ⚙️

- **🔌Master Token WebSocket integration**: Master token integration for using the WebSocket decorator. You can now choose between access or master token. [see example](../examples/apps/websocket_api/api.py)

## version 0.0.1 (Start Project) 🌟

- **🔐 Token-based authentication system (Access + Refresh) with endpoints ready:** check the `/auth` router and the `/token/new` and `/token/refresh` endpoints in [auth.py](src/fastauth/routers/auth.py).
- **⚙️ Easy integration with `FastAPI`:** function [`Fastauth().set_auth(app)`](src/fastauth/quick_app.py) applies middleware, registers routes and replaces the OpenAPI with FastauthOpenAPI.
- **🛡 Configurable middleware:** Master / Access level protection based on routes defined in the configuration. Supports validation of MASTER-TOKEN and ACCESS-TOKEN headers.
- **🧾 Flexible configuration:** values from `fastauth.config.json` or environment variables (`.env`).
- **🔑 Basic key management and utilities:**
  - Generate `CRYPTOGRAPHY_KEY` with `generate_cryptography_key()`.
  - Read/write variables in `.env` using `writekey2env(...)`.
- 🧠 JWT tokens signed with HS256 and payloads containing `client_id`, `type`, `iat`, `exp`.
- **💾 Decoupled token persistence:** `save_token` / `load_access_token` interact with an external API configurable via `"database_api_path"` in the configuration file.
- **🔌 WebSocket support:** authentication decorator for websockets (checks ACCESS-TOKEN in headers).
- **🧰 Extensible:** `TokenRouter` can be extended to customize token generation/renewal; middleware and OpenAPI are easily replaceable/adjustable.
