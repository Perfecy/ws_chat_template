from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
import uvicorn

app = FastAPI()

connections = {}

# Статика монтируется явно на '/static', а не на '/'
app.mount("/static/", StaticFiles(directory="static"), name="static")

@app.get("/")
async def root():
    return {"message": "Server is running!"}

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    client_id = id(websocket)
    connections[client_id] = []

    try:
        while True:
            message = await websocket.receive_text()
            connections[client_id].append(message)

            if len(connections[client_id]) == 2:
                reversed_messages = " | ".join(connections[client_id][::-1])
                await websocket.send_text(f"Перевернутые сообщения: {reversed_messages}")
                connections[client_id] = []

    except WebSocketDisconnect:
        connections.pop(client_id, None)

uvicorn.run(
    app,
    ssl_keyfile='PATH_TO_SERVER_KEYFILE',
    ssl_certfile='PATH_TO_SERVER_CRTFILE',
    ssl_ca_certs='PATH_TO_CA_CRT',
    ssl_cert_reqs=2
)