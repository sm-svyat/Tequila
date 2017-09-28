import socket
import json

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 8888))
s.listen()

while True:
    client, addr = s.accept()
    respons = {
        "response": 200,
        "alert":"Необязательное сообщение/уведомление"
    }

    string = json.dumps(respons)
    client.send(string.encode('utf-8'))

    client.close()
