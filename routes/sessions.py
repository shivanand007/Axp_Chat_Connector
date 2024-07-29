import os
import requests
from fastapi import APIRouter,HTTPException
from dotenv import load_dotenv
from utils import logger
from utils import handle_api_response


# Load variables from .env file
load_dotenv()
# setting router
sessions_router = APIRouter()


@sessions_router.post("/create_session")
def create_session(access_token,displayname) -> str:
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

        url = f"{base_url}/digital/channel/v1beta/accounts/{account_id}/sessions"

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {access_token}"
        }

        payload = {
            "channelProviderId": f"{channelProviderId}",
            "customerIdentifiers": {
                "email": [
                    "rahul9123@gmail.com"
                ]
            },
            "displayName": f"{displayname}"
        }

        try:
            response = requests.post(url, json=payload, headers=headers)
            response = handle_api_response(response)
            if response['status']:
                logger.info(f"session data --> {response['data']}")
                sessionId = response['data']['sessionId']
                logger.info(f"session created -->{sessionId}")
                return sessionId
            else:
                logger.info(f"failed to create Session --> {response['error_code']} || {response['error_message']}")
                return response

        except requests.RequestException as e:
            print("Error:", e)
            return None


@sessions_router.post("/delete_session")
def delete_session(access_token,session_id):
    """
    Make a DELETE request to the specified URL with the given Bearer token.

    Args:
        url (str): The URL to which the DELETE request is to be made.
        token (str): The Bearer token to include in the request header.

    Returns:
        requests.Response: The response object from the DELETE request.
    """
    sessionId = session_id
    # Endpoint URL with placeholders for accountId and sessionId
    url = f"https://eu.cc.avayacloud.com/api/digital/channel/v1beta/accounts/SXCMXA/sessions/{sessionId}"


    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    try:
        response = requests.delete(url, headers=headers)
        # Process the response
        if response is not None:
            if response.status_code == 204:
                logger.info("DELETE request was successful.")
            else:
                logger.info("DELETE request failed.")
                logger.info("Error code:", response.status_code)
                logger.info("Error message:", response.text)
        return response
    except requests.RequestException as e:
        print("Error:", e)
        return None