from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
from manager import WebSocketManager

app = FastAPI()

templates = Jinja2Templates(directory="templates")
manager = WebSocketManager()

@app.get("/")
async def root(request: Request):
    return templates.TemplateResponse(request, "index.html",{})

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            message = await websocket.receive_json()
            print(f"Received message: {message}")
            await manager.broadcast(websocket, message)
    except WebSocketDisconnect:
        await manager.disconnect(websocket)
