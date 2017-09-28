import socket
import json

def connection(json_object):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('localhost', 8888))


msg = s.recv(1024)
s.close()

presens = {
    "action": "presence",
    "time": "<unix timestamp>",
    "type": "status",
    "user": {
    "account_name": "C0deMaver1ck",
    "status": "Yep, I am here!"
    }
    }



j = json.loads(msg.decode('utf-8'))
print(j['response'])