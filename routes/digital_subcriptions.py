import os
import requests
from utils import logger
from utils import handle_api_response
from dotenv import load_dotenv
from fastapi import APIRouter,HTTPException

# Load variables from .env file
load_dotenv()
# setting router
subcriptions_router = APIRouter()

@subcriptions_router.post("/create_subcription")
def create_subscription(access_token) -> str:
    account_id = os.getenv('account_id')
    base_url = os.getenv('base_url')
    webhook = os.getenv("webhook_url")
    channelProviderId = os.getenv("channelProviderId")

    url = f"{base_url}/digital/webhook/v1beta/accounts/{account_id}/subscriptions"

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    # Payload for the subscription request
    payload = {
        "eventTypes": ["MESSAGES"],
        "channelProviderId": f"{channelProviderId}",
        "callbackUrl": f"{webhook}"
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        response = handle_api_response(response)
        if response["status"]:
            logger.info(f"Subcription Created and storing subscriptionId--> {response['data']}")
            subscriptionId = response["data"]["subscriptionId"]

            # setting subscriptionId in env file
            os.environ["subscriptionId"] = subscriptionId
            return subscriptionId
        else:
            logger.info(f"Subcription Creation failed --> {response['error_code']} || {response['error_message']}")
            return HTTPException(status_code=500)

    except requests.exceptions.RequestException as e:
        return str(e)


@subcriptions_router.get("/get_subcription_list")
def get_subscription_list(access_token) -> dict:
    account_id = os.getenv('account_id')
    url = f"https://eu.cc.avayacloud.com/api/digital/webhook/v1beta/accounts/{account_id}/subscriptions"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    try:
        response = requests.get(url, headers=headers)
        response = handle_api_response(response)
        if response['status']:
            logger.info(f"subcription list -->{response['data']} ")
            print(response['data'])
            return response['data']
        else:
            logger.info(f"failed to get subcription list --> {response['error_code']} || {response['error_message']}")
            return response

    except requests.exceptions.RequestException as e:
        return str(e)


@subcriptions_router.put("/update_subcription_list")
def update_subscription(access_token,eventTypes : str = "MESSAGES") -> dict:
    account_id = os.getenv('account_id')
    subcriptionId = os.getenv("subscriptionId")
    channelProviderId = os.getenv("channelProviderId")
    webhook = os.getenv("webhook_url")

    url = f"https://eu.cc.avayacloud.com/api/digital/webhook/v1beta/accounts/{account_id}/subscriptions/{subcriptionId}"

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}"
    }

    # Payload for the subscription request
    payload = {
        "eventTypes": [eventTypes],
        "channelProviderId": f"{channelProviderId}",
        "callbackUrl": f"{webhook}"
    }

    try:
        response = requests.put(url, headers=headers, json=payload)
        response = handle_api_response(response)
        if response['status']:
            logger.info(f"subcription updated --> {response['data']}")
            return response['data']
        else:
            logger.info(f"failed to UPDATE subcription --> {response['error_code']} || {response['error_message']}")
            return response

    except requests.exceptions.RequestException as e:
        return str(e)


#t = "eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICIwd1kzWEVkajY3TTZmZjJBNHk5Z0MxTkQ1SmdseTlWV0xPQjE1SnlLQVhRIn0.eyJleHAiOjE2OTMyMTg5NjMsImlhdCI6MTY5MzIxODA2MywianRpIjoiYTZmYjJlZDMtYjY1ZC00NjZiLThiNmEtZjExM2NjMzliNmJkIiwiaXNzIjoiaHR0cHM6Ly9ldS5jYy5hdmF5YWNsb3VkLmNvbS9hdXRoL3JlYWxtcy9TWENNWEEiLCJhdWQiOlsiYWNjb3VudCIsImNsaWVudGlkZnV0dXJlIl0sInN1YiI6InNlcnZpY2UtYWNjb3VudC1jbGllbnRpZGZ1dHVyZSIsInR5cCI6IkJlYXJlciIsImF6cCI6ImNsaWVudGlkZnV0dXJlIiwiYWNyIjoiMSIsInJlYWxtX2FjY2VzcyI6eyJyb2xlcyI6WyJ0cnVzdGVkX2NsaWVudCIsIm9mZmxpbmVfYWNjZXNzIiwiZGVmYXVsdC1yb2xlcy0wOGY5ZjI3ZS0xNjU5LTQ0MGUtYWUyNS0xOWQwY2Q0NjRmMGEiLCJ0cmFuc2NyaXB0cy1xdWVyeSIsInVtYV9hdXRob3JpemF0aW9uIiwidHJ1c3RlZF9jbGllbnQgIiwidXNlciJdfSwicmVzb3VyY2VfYWNjZXNzIjp7ImNsaWVudGlkZnV0dXJlIjp7InJvbGVzIjpbInVtYV9wcm90ZWN0aW9uIl19LCJhY2NvdW50Ijp7InJvbGVzIjpbIm1hbmFnZS1hY2NvdW50IiwibWFuYWdlLWFjY291bnQtbGlua3MiLCJ2aWV3LXByb2ZpbGUiXX19LCJzY29wZSI6ImVtYWlsIHByb2ZpbGUiLCJjbGllbnRIb3N0IjoiMTAuMjAuMTEuMzMiLCJjbGllbnRJZCI6ImNsaWVudGlkZnV0dXJlIiwiZW1haWxfdmVyaWZpZWQiOmZhbHNlLCJpZHAiOiJmbGV4IiwidGVuYW50SWQiOiJTWENNWEEiLCJncm91cHMiOltdLCJwcmVmZXJyZWRfdXNlcm5hbWUiOiJzZXJ2aWNlLWFjY291bnQtY2xpZW50aWRmdXR1cmUiLCJjbGllbnRBZGRyZXNzIjoiMTAuMjAuMTEuMzMifQ.iWwQZ1LT0K2uuLg7vfPo9SJAhlvaFKfBemJE3AJnTGkeOSjevbmMy9MW1MgqIyCTcWhRw8DJH2PUZl8FOEFiiE7uZLZP5L1XSsGtW3wjksogBtsY-PfhX0De4YoReGLhSp-l6rDMhUiGPaa9TKPAMIANFRGQW2WxVveHSPvHLIaf60YBMR6ihSdTRat5ISX1kBa89o4gCaio8GgbP9gRJP88oGhAM1daLutiARy3arxX77da2eXhkM6-nrqsnuDmhHlbI-sPNaXIngapY8JSlanPJKvx93cuNAHUHeL8fuPbcNKbWh2d5FoNjF-Njvj5jbZztfjeF5yFGMvwT9EFKQ"
#create_subscription(t)

#update_subscription(t)
#get_subscription_list(t)