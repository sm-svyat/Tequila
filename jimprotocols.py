import socket
import json
import time

class JimMessage:
    '''
    Класс, который реализует создание сообщению по JIM протоколу.
    Получает на вход отправителя, адресата и само сообщение.
    '''
    def __init__(self, sender, addressee,  message):
        self.sender = sender
        self.addressee = addressee
        self.message = message
        self.response = dict()

    def msgcompose(self):
        '''
        Функция, которая составляет JSON сообщение
        '''
        self.response = {
        "action": "msg",
        "time": str(time.ctime()),
        "to": str(self.addressee),
        "from": str(self.sender),
        "message": self.message
        }

    def jsonmsg(self):
        '''
        Функция, которая возвращает json объект закодированый в utf-8
        '''
        self.msgcompose()
        return json.dumps(self.response).encode('utf-8')

class JimResponse:
    '''
    Класс, который реализует создание сообщению по JIM протоколу.
    Получает на тип ответа, и сообщение.
    '''
    def __init__(self, response_type, alert = None):
        self.resp_type = response_type
        self.alert = alert
        self.response = dict()

    def msgcompose(self):
        '''
        Функция, которая составляет JSON сообщение
        '''
        self.response = {
            "response": self.resp_type,
            "alert": self.alert
        }

    def jsonmsg(self):
        '''
        Функция, которая возвращает json объект закодированый в utf-8
        '''
        self.msgcompose()
        return json.dumps(self.response).encode('utf-8')

class Client:
    def __init__(self, client, addr):
        self.client = client
        self.addr = addr
        self.username = str()
        self.client_message = str()

    def __str__(self):
        return self.username

    def __repr__(self):
        return self.addr

    def getmsg(self):
        return self.client_message




if __name__ == '__main__':

    # test
    msg = JimMessage('Me', 'You', 'Hello!')
    data = msg.jsonmsg()
    json_data = json.loads(data.decode('utf-8'))
    print(json_data)

    # test
    msg = JimResponse(200, 'It\'s OK!')
    data = msg.jsonmsg()
    json_data = json.loads(data.decode('utf-8'))
    print(json_data)

    # test
    client = Client("Svyat")
    print(client)