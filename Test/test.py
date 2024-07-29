from routes.auth_token import authentication
from routes.engagements import create_engagement,disconnect_engagement,send_message
from routes.sessions import create_session,delete_session
from routes.digital_subcriptions import update_subscription
import time


access_token = authentication()
#update_subscription(access_token)


time.sleep(3)

session_id = create_session(access_token)

obj = create_engagement(access_token,session_id)
engagementId = obj["engagementId"]
dialog_id = obj["dialog_id"]

time.sleep(3)


while True:

    message = input("Enter your message (or type 'exit' to stop): ")

    if message.lower() == 'exit':
        break
    res = send_message(access_token, engagementId, message, session_id, dialog_id)
    print("Response:", res)

