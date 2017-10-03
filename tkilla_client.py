import socket
import json
import time

def connection(json_object):

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(('localhost', 8888))
    sock.send(json_object.encode('utf-8'))


    data = sock.recv(1024)
    sock.close()
    return data

authenticate_request = {
    "action": "authenticate",
    "time": "<unix timestamp>",
    "user": {
    "account_name": "C0deMaver1ck",
    "password": "CorrectHorseBatteryStaple"
    }
    }

authenticate_request['time'] = time.ctime()
request = json.dumps(authenticate_request)
data = connection(request)


json_data = json.loads(data.decode('utf-8'))
print(json_data['response'])
if json_data['response'] // 100 == 4:
    print(json_data['error'])