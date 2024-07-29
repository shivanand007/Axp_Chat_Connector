from routes import authentication,update_subscription


access_token = authentication()
update_subscription(access_token)