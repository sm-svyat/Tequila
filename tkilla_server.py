import socket
import json
from bd import response_list, users

class MainServer:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.client = object()
        self.addr = str()
        self.data = str()
        self.json_data = str()
        self.string = str()
        self.sock = str()

    def connect(self):

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((self.ip, self.port))
        self.sock.listen()
        self.run()

    def run(self):
        while True:
            #try:
            self.client, self.addr = self.sock.accept()
            try:
                self.data = self.client.recv(1024)
                self.json_data = json.loads(self.data.decode('utf-8'))
                self.respons_generator()
            except:
                print('Error 400. Wrong JSON-object.')
                self.run()

    def respons_generator(self):
        if self.json_data['action'] == "authenticate":
            self.authenticate()
        elif self.json_data['action'] == "msg":
            self.conversation()
        elif self.json_data['action'] == "presence":
            self.presence()
        else:
            error_response = {
                "response": 400,
                "error": "Bad request"
                }
            self.string = json.dumps(error_response)
            self.client.send(self.string)
            self.client.close()

    def authenticate(self):
        if self.json_data['user']['account_name'] in users.keys():
            if self.json_data['user']['password'] == users[self.json_data['user']['account_name']]:
                print("Пользователь с ником %s прошел аунтентификацию %s" % (self.json_data['user']['account_name'], self.json_data['time']) )
                respons = {
                    "response": 200,
                    "alert": "Authentication is successful"
                }
                self.string = json.dumps(respons)
                self.client.send(self.string.encode('utf-8'))
                self.client.close()
            else:
                error_response = {
                    "response": 402,
                    "error": "Wrong password or no account with that name"
                    }
                print("Ошибка 402, \"Wrong password\"")
                self.string = json.dumps(error_response)
                self.client.send(self.string.encode('utf-8'))
                self.client.close()

        else:
            error_response = {
                "response": 402,
                "error": "No account with that name"
            }
            print("Ошибка 402, \"Wrong password or no account with that name\"")
            self.string = json.dumps(error_response)
            self.client.send(self.string.encode('utf-8'))
            self.client.close()

    def conversation(self):
        #Здесь будет реализовано общение между пользователями, однажды...
        print('Здесь будет реализовано общение между пользователями, однажды...')
        msg_response = {
            "action": "msg",
            "time": '<unix timestamp>',
            "to": "#room_name",
            "from": "account_name",
            "message": "Hello World"
            }

        join_response = {
            "action": "join",
            "time": '< unixtimestamp >',
            "room": "#room_name"
            }

        leave_response = {
            "action": "leave",
            "time": '< unixtimestamp >',
            "room": "#room_name"
            }

if __name__ == '__main__':

    server = MainServer('', 8888)
    server.connect()