import asyncio
import websockets


async def connect_websocket():
    uri = "wss://eu.cc.avayacloud.com/ix-notification-dispatchers/notification-websocket/notifications/SXCMXA/5ce46db4-f8f6-4639-9a81-61585d0a0417"

    async with websockets.connect(uri) as websocket:
        print("WebSocket connection established")

        while True:
            message = await websocket.recv()
            print(f"Received message: {message}")


asyncio.get_event_loop().run_until_complete(connect_websocket())
