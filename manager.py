from fastapi.websockets import WebSocket


class WebSocketManager:
    def __init__(self):
        self.connected_clients = []

    async def connect(self, websocket: WebSocket):
        client_ip = f"{websocket.client.host} : {websocket.client.port}"

        # Client has connected
        await websocket.accept()
        print(f"client {client_ip} connected")

        # add client to list of connected clients
        self.connected_clients.append(websocket)
        print(f"connected clients: {self.connected_clients}")

        message = {"client": client_ip, "message": "Welcome"}
        await websocket.send_json(message)

    async def broadcast(self, sender: WebSocket, message: dict):
        print(f"message from sender {sender.client.host}:{sender.client.port} : {message}")
        for websocket in self.connected_clients:
            await websocket.send_json({
                "client": f"{sender.client.host} : {sender.client.port}",
                "message": message['content']
            })

    async def disconnect(self, websocket: WebSocket):
        self.connected_clients.remove(websocket)
        print(f"client {websocket.client.host} : {websocket.client.port} disconnected")
        print(f"connected clients: {self.connected_clients}")
