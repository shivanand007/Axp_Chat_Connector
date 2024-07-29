import os
import time
from routes import authentication,create_session,create_engagement,disconnect_engagement,delete_session,send_message
from utils.logger import logger
from utils.random_name_generator import generate_random_name

def connect_client(client_id,connected_clients):
    try:
        # setting SID in .env file for sharing this other files and function

        logger.info("Session Id Set in Environment file")

        logger.info(f"FT CHAT CONNECTOR SESSION ID : {client_id} connected")

        logger.info(f"authenticating user invoking authentication api")
        token = authentication()
        logger.info(f"auth token acquired : {token}")
        os.environ["axp_auth_token"] = token
        time.sleep(1)

        logger.info(f"creating session In AXP")
        displayname = generate_random_name()
        logger.info(f"Random name generated for this session chat : - {displayname}")

        sessionId = create_session(access_token=token,displayname=displayname)
        logger.info(f"session created In AXP with sessionID : {sessionId}")

        logger.info(f"creating engagement")
        data = create_engagement(token, sessionId)

        engagementId = data["engagementId"]
        dialog_id = data["dialog_id"]

        logger.info(f"Engagement Created with Engagement ID : {engagementId} \n and with dialog_id : {dialog_id}")

        connected_clients[client_id] = {"engagementId": engagementId, "dialogId": dialog_id, "sessionId": sessionId,
                                  "token": token}

        logger.info(f"connected clients object : {connected_clients}")

        logger.info(f"Number of clients connected at this time : {len(connected_clients.keys())}")

        return True
    except Exception as e:
        logger.error(f"connection failed with axp! : {e}")



def disconnect_client(sid,connected_clients):

    try:
        logger.info(f"Session Id : {sid} Disconnected \n")
        token = connected_clients[sid]["token"]
        engagementId = connected_clients[sid]["engagementId"]
        sessionId = connected_clients[sid]["sessionId"]
        dialogId = connected_clients[sid]["dialogId"]

        logger.info(f"terminating engagement for session Id  : {sid}")
        disconnect_engagement(token, engagementId, sessionId, dialogId)
        logger.info(f"engagement terminated for session Id  : {sid}")

        logger.info(f"terminating session for session Id : {sid}")
        delete_session(token, sessionId)
        logger.info(f"session terminated for session Id  : {sid}")

        if sid in connected_clients:
            del connected_clients[sid]
        else:
            logger.error("Session ID NOT FOUND in mappings")

    except Exception as e:
        logger.error(f"An exception Occurred While Disconnecting Session: {e}\n")



def send_message_middleware(sid,message,connected_clients):
    try:
        logger.info(f"Received message from {sid} : {message} \n")
        engagementId = connected_clients[sid]["engagementId"]
        token = connected_clients[sid]["token"]
        dialogId = connected_clients[sid]["dialogId"]
        sessionId = connected_clients[sid]["sessionId"]

        logger.info(f"engagementId id for sid={sid} is : {engagementId} \n")

        logger.info(f"sending message to agent \n")

        send_message(token, engagementId, message, sessionId, dialogId)

        logger.info(f"message sent to AXP for SID : {sid} --> message Content : {message}")

        return True

    except Exception as e:
        logger.error(f"Failed to send or receive message: {e} \n")
        return False
