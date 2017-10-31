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
        "time": time.ctime(),
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
    Класс, который реализует создание сообщения по JIM протоколу.
    Получает на вход тип ответа и сообщение.
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

class JimAuthenticate:
    '''
    Класс, который реализует создание сообщения для входа в систему по JIM протоколу.
    Получает на вход login и password.
    '''
    def __init__(self, login, password):
        self.login = login
        self.password = password
        self.response = dict()

    def msgcompose(self):
        '''
        Функция, которая составляет JSON сообщение
        '''
        self.response = {
            "action": "authenticate",
            "time": time.ctime(),
            "user": {
                "account_name": self.login,
                "password": self.password
            }
        }

    def jsonmsg(self):
        '''
        Функция, которая возвращает json объект закодированый в utf-8
        '''
        self.msgcompose()
        return json.dumps(self.response).encode('utf-8')

class JimRegistration:
    '''
    Класс, который реализует создание сообщения для регистрации по JIM протоколу.
    Получает на вход login и password.
    '''
    def __init__(self, login, password):
        self.login = login
        self.password = password
        self.response = dict()

    def msgcompose(self):
        '''
        Функция, которая составляет JSON сообщение
        '''
        self.response = {
            "action": "registration",
            "time": time.ctime(),
            "user": {
                "account_name": self.login,
                "password": self.password
            }
        }

    def jsonmsg(self):
        '''
        Функция, которая возвращает json объект закодированый в utf-8
        '''
        self.msgcompose()
        return json.dumps(self.response).encode('utf-8')

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