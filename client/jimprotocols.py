import socket
import json
import time

class JimMessage:
    '''
    Класс, который реализует создание сообщению по JIM протоколу.
    Получает на вход отправителя, адресата и само сообщение.
    '''
    def __init__(self, tokin, peer,  message):
        self.tokin = tokin
        self.peer = peer
        self.message = message
        self.response = dict()


    def msgcompose(self):
        '''
        Функция, которая составляет JSON сообщение
        '''
        self.response = {
            'action': 'msg',
            'tokin': self.tokin,
            'to': self.peer,
            'time': time.ctime(),
            'message': self.message
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


class JimAuthentication:
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


class JimHistory:
    '''
    Класс, который реализует создание сообщения для регистрации по JIM протоколу.
    Получает на вход login и password.
    '''
    def __init__(self, tokin, peer):
        self.tokin = tokin
        self.peer = peer
        self.response = dict()


    def msgcompose(self):
        '''
        Функция, которая составляет JSON сообщение
        '''
        self.response = {
            'action': 'history',
            'tokin': self.tokin,
            'to': self.peer
        }


    def jsonmsg(self):
        '''
        Функция, которая возвращает json объект закодированый в utf-8
        '''
        self.msgcompose()
        return json.dumps(self.response).encode('utf-8')


class JimAddContact:
    '''
    Класс, который реализует создание сообщения для регистрации по JIM протоколу.
    Получает на вход login и password.
    '''
    def __init__(self, tokin, contactLogin):
        self.tokin = tokin
        self.contactLogin = contactLogin
        self.response = dict()


    def msgcompose(self):
        '''
        Функция, которая составляет JSON сообщение
        '''
        self.response = {
            'action': 'add_contact',
            'tokin': self.tokin,
            'contact': self.contactLogin
        }

    def jsonmsg(self):
        '''
        Функция, которая возвращает json объект закодированый в utf-8
        '''
        self.msgcompose()
        return json.dumps(self.response).encode('utf-8')


class JimGetContact:
    '''
    Класс, который реализует создание сообщения для регистрации по JIM протоколу.
    Получает на вход login и password.
    '''
    def __init__(self, tokin):
        self.tokin = tokin
        self.response = dict()


    def msgcompose(self):
        '''
        Функция, которая составляет JSON сообщение
        '''
        self.response = {
            'action': 'get_contacts',
            'tokin': self.tokin,
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