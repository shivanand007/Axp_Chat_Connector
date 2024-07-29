"""from websocket_server import WebsocketServer
from webscoket import *


host = '127.0.0.1'
port = 13254
server = WebsocketServer(host=host, port=port)
print(f"server started at {port}")

server.set_fn_new_client(connect)
server.set_fn_message_received(client_msg_received)
server.set_fn_client_left(client_disconnected)

server.run_forever()
client = {
        'id': 1,
        'handler' : connect,
        'address' : ("127.0.0.1", "13254")
         }

server.send_message(client,"helllo from server")"""