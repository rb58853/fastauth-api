from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import RedirectResponse
from fastauth import set_auth

app = FastAPI(root_path="/test-api")
set_auth(app)


@app.get("/")
async def root():
    return RedirectResponse(url="/docs")


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


@app.websocket("/ws")
async def websocket_chat(
    websocket: WebSocket,
):
    await websocket.accept()
    try:
        while True:
            query = await websocket.receive_text()
            await websocket.send_text(f"Received query: {query}")

    except WebSocketDisconnect:
        pass


def get_history(chat_id: str) -> list:
    """Select history from database using chat_id"""
    return []
