from fastapi import FastAPI, WebSocket
import uuid


app = FastAPI()

# List to store connected WebSocket clients
connected_clients = set()


# WebSocket endpoint for clients to connect
@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: int):
    await websocket.accept()
    connected_clients.add(websocket)

    try:
        while True:
            # Receive a message from the WebSocket client
            message = await websocket.receive_text()

            # Send the received message to all connected clients
            for client in connected_clients:
                await client.send_text(f"Client {client_id}: {message}")
    except Exception:
        connected_clients.remove(websocket)



async def generate_unique_id():
    unique_id = str(uuid.uuid4())  # Generate a random UUID
    return {"unique_id": unique_id}