import os
import requests
import json
from utils import logger
from utils import handle_api_response
from dotenv import load_dotenv
from fastapi import APIRouter,HTTPException

# Load variables from .env file
load_dotenv()
# setting router
engagements_router = APIRouter()


@engagements_router.post("/create_engagement")
def create_engagement(access_token,session_id) -> str:
    """
    Make a POST request to the specified URL with the given payload and Bearer token.

    Args:
        url (str): The URL to which the POST request is to be made.
        payload (dict): The data to be sent in the request body.
        token (str): The Bearer token to include in the request header.

    Returns:
        requests.Response: The response object from the POST request.
    """
    account_id = os.getenv('account_id')
    base_url = os.getenv('base_url')
    channelProviderId = os.getenv("channelProviderId")

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}"
    }

    # Endpoint URL and payload
    url = f"{base_url}/digital/channel/v1beta/accounts/{account_id}/engagements"

    payload = {
        "sessionId": session_id,
        "channelId": "Chat",
        "conversation": "sell car",
        "engagementParameters": {"active": "yes"}
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        response = handle_api_response(response)
        if response['status']:
            logger.info(f"engagement data --> {response['data']}")
            engagementId = response['data']['engagementId']
            dialog_id = response['data']["dialogs"][0]["dialogId"]
            logger.info(f"engagement created --> {engagementId}")

            obj = {"engagementId": engagementId,
                   "dialog_id" : dialog_id}
            return obj

        else:
            logger.info(f"sending msg failed creation failed --> {response['error_message']}")
    except requests.RequestException as e:
        logger.error("Error while executing engagement:", e)
        return None


@engagements_router.post("/disconnect_engagement")
def disconnect_engagement(access_token, engagement_id,session_id,dialogId,reason = "USER_CLOSED"):
    """
    Disconnect an engagement using a POST request to the specified URL with the given payload and Bearer token.

    Args:
        bearer_token (str): The Bearer token for authentication.
        engagement_id (str): The ID of the engagement to disconnect.
        payload (dict): The data to be sent in the request body.

    Returns:
        requests.Response: The response object from the POST request.
    """
    url = f"https://eu.cc.avayacloud.com/api/digital/channel/v1beta/accounts/SXCMXA/engagements/{engagement_id}:disconnect"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}"
    }

    payload = {
        "sessionId": session_id,
        "dialogId": dialogId,
        "reason": reason
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        response = handle_api_response(response)
        if response['status']:
            logger.info(f"engagement data --> {response['data']}")
            logger.info(f"enagement disconnected --> {response['data']}")
            return response
        else:
            logger.error(f"enagegment failed to disconnect --> {response['error_message']}")
    except requests.RequestException as e:
        print("Error:", e)
        return None


def join_engagement():
    pass

@engagements_router.post("/send_message")
def send_message(access_token, engagement_id, message, sessionId, dialogId, fallbackText="Demo", app_name="web browser"):

    account_id = os.getenv('account_id')
    base_url = os.getenv('base_url')

    url = f"{base_url}/digital/channel/v1beta/accounts/{account_id}/engagements/{engagement_id}/messages"

    logger.info(f" URL : {url}")

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}"
    }

    logger.info(f'header : {headers}')

    payload = {
        "body": {
            "elementText": {
                "text": message,
                "textFormat": "PLAINTEXT"
            },
            "elementType": "test",
            "payload": "Testing with python"
        },
        "headers": {
            "priority": "5",
            "from": app_name
        },
        "sessionId": sessionId,
        "dialogId": dialogId,
        "fallbackText": fallbackText
    }

    logger.info(f"send message body : {payload}")

    try:
        response = requests.post(url, json=payload, headers=headers)
        #calling response handler
        response = handle_api_response(response)

        if response["status"]:
            logger.info(f"message sent --> {response['data']}")
            return True
        else:
            logger.error(f"failed to send message --> {response['error_message']}")

    except requests.RequestException as e:
        logger.error("failed to send message:", e)
        return HTTPException(status_code=500,detail="message delivery failed")

