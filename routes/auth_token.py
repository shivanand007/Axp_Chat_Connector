import os
import requests
from fastapi import APIRouter,HTTPException
from dotenv import load_dotenv
from utils import logger
import functools
from utils import handle_api_response

# Load variables from .env file
load_dotenv()
# setting router 
auth_router = APIRouter()


@auth_router.get("/auth")
def authentication() -> str:
    # Replace with your actual Account ID and any necessary authentication data
    account_id = os.getenv('account_id')
    client_id = os.getenv('clientId')
    client_secret = os.getenv('clientSecret')
    labFQDN = os.getenv('labFQDN')

    url = f"https://{labFQDN}/auth/realms/{account_id}/protocol/openid-connect/token"

    logger.info(f"url -- > {url}")

    # Request payload
    payload = {
        "grant_type": "client_credentials",
        "client_id": client_id,
        "client_secret": client_secret
    }

    try:
        response = requests.post(url, data=payload)
        response = handle_api_response(response)
        if response["status"]:
            token = response['data']['access_token']
            logger.info(f"API Token --> {token}")
            return token
        else:
            logger.info(f"Token failed --> {response['error_code']} || {response['error_message']}")
            return response

    except requests.exceptions.RequestException as e:
        logger.error("An error occurred: %s", e)


# Define a decorator function that handles token expiration and reauthentication
def token_refresh_decorator(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        global access_token
        logger.info("entered filter calling authentication funcation for checking validity of token")
        access_token = authentication()  # Call your authentication function to get the initial token
        response = func(*args, **kwargs)  # Call the wrapped function

        if response.status_code == 401:
            logger.info(f"token expired refreshing to get new token")
            # Token might have expired, attempt to refresh it
            access_token = authentication()
            if access_token:
                # Update the Authorization header with the new token
                headers = kwargs.get('headers', {})
                headers['Authorization'] = f'Bearer {access_token}'
                kwargs['headers'] = headers
                # Call the wrapped function again with the updated token
                response = func(*args, **kwargs)
                logger.info(f"successfully recalled the funcation")
        return response
    return wrapper

"""access_token = authentication()
print(access_token)"""











