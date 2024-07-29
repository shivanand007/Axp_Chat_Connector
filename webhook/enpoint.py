import base64
import json
from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from utils import logger
import uuid
from fastapi import WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from utils import connect_client, disconnect_client, send_message_middleware, find_client_id_by_dialog_id, save_uploaded_file
from jinja2 import Environment, FileSystemLoader, select_autoescape
import socket

webhook_router = APIRouter()

# Define a dictionary to store WebSocket connections for each client
websocket_connections = {}
# for axp details
connected_clients = {}

# Configure Jinja2
templates_dir = "./templates/client_templates"
env = Environment(
    loader=FileSystemLoader(templates_dir),
    autoescape=select_autoescape(["html", "xml"])
)


@webhook_router.get("/sample_client")
async def get_1():
    headers = {
        "Cache-Control": "no-store, max-age=0, must-revalidate",
    }

    # get the current ip address of the server
    server_ip_address = socket.gethostbyname(socket.gethostname())
    logger.info(f'Ip address of host machine is : {server_ip_address}')

    # Render the template with dynamic data
    template = env.get_template("test_client.html")
    html_content = template.render(ip_address=server_ip_address)

    return HTMLResponse(content=html_content, headers=headers)


@webhook_router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    client_id = str(uuid.uuid4())
    logger.info(f"Client connected with client id: {client_id} || Creating connection with AXP")

    if connect_client(client_id, connected_clients):
        logger.info(f"Connected to AXP")

    websocket_connections[client_id] = websocket

    try:
        while True:
            data = await websocket.receive_json()
            print('data : ', data)
            # check if the data is dict else if simple text then neglect it
            if isinstance(data, dict) and data.get('type') == 'file':
                data_url = data['data']
                # Remove the "data:image/png;base64," prefix
                base64_data = data_url.split(",")[-1]
                # Decode the base64-encoded image data
                image_data = base64.b64decode(base64_data)

                # Modify 'save_uploaded_file' to handle the saving logic
                saved_file_link = save_uploaded_file(image_data)

                ''' sending the url to agent '''
                if send_message_middleware(client_id, saved_file_link, connected_clients):
                    logger.info(f"attachment url {saved_file_link} sent to axp")

            else:
                #parse the data
                content = data['content']
                if send_message_middleware(client_id, content, connected_clients):
                    logger.info(f"{client_id} Message received: {content} and sent to axp")

    except WebSocketDisconnect:
        disconnect_client(client_id, connected_clients)
        logger.error(f"Socket disconnected: client_id={client_id}")
        del websocket_connections[client_id]


@webhook_router.post('/events')
async def webhook_handler(request: Request):
    data = await request.json()
    try:
        logger.info(f"Received webhook event data: {data}")

        messageId = str(data["messageId"])
        senderParticipantType = str(data["senderParticipantType"])
        engagementId = str(data["engagementId"])
        dialogId = str(data["dialogId"])
        message = str(data["body"]["elementText"]["text"])
        correlationId = str(data["correlationId"])
        timestamp = str(data["receivedAt"])

        if senderParticipantType != "CUSTOMER":

            """ first find which client to send the message"""
            client_id = find_client_id_by_dialog_id(dialogId, connected_clients)

            logger.info(f"message from AXP to client {client_id} is {message} || {senderParticipantType}")

            logger.info(f"websocket connections object : --> {websocket_connections}")

            if client_id in websocket_connections:
                """ Take websocket object for that client and send it back"""
                websocket = websocket_connections[client_id]
                """ send axp message back to client """
                await websocket.send_text(message)
                logger.info(f"response sent back to client {client_id}: {message}")
            return JSONResponse(content=message, status_code=200)
        else:
            logger.info(f"Skipping Customer message not adding to db or file:")

    except Exception as e:
        logger.error(f"Error processing webhook event: {e}")
        return JSONResponse(content={"error": "An error occurred"}, status_code=500)
