import json
import socket
import sys
import time
from jimprotocols import JimMessage, JimAuthentication, JimRegistration, JimHistory, JimAddContact, JimGetContact

HOST = 'localhost'
PORT = 7777
#host='194.67.222.96', port=7777

class Client:
    def __init__(self, login, password):
        self.login = login
        self.password = password
        self.tokin = str()

    def change_tokin(self, tokin):
        self.tokin = tokin

    def __repr__(self):
        return self.login


def recording(login, password, second_passwd):
    if login and password and password:
        if password == second_passwd:
            #global user
            user = Client(login, password)
            try:
                response = registration(login, password)
                if 'tokin' in response.keys():
                    user.change_tokin(response['tokin'])
                    print(response)
                    return (True, 'Регистрация прошла успешно.', user)
                elif 'error' in response.keys():
                    print(response['error'])
                    return (False, 'Ошибка при регистриции.')
                else:
                    print('Пришел некоректный ответ.')
                    return (False, 'Ошибка при регистриции.')
            except ConnectionRefusedError:
                return (False, 'Сервер не отвечает')
        else:
            return (False, 'Пароли не совпадают')
    else:
        return (False, 'В форме заполнены не все поля')


def log_in(login, password):
    if login and password and password:
        #global user
        user = Client(login, password)
        try:
            response = authenticate(user.login, user.password)
            if 'tokin' in response.keys():
                user.change_tokin(response['tokin'])
                return (True, 'Авторизация прошла успешно.', user)
            elif 'error' in response.keys():
                return (False, response['error'])
            else:
                return (False, 'Пришел некоректный ответ.')
        except ConnectionRefusedError:
            return (False, 'Сервер не отвечает')
    else:
        return (False, 'В форме заполнены не все поля')


def write_msg(self, tokin, peer, msg):
    myChat = Conversation()
    myChat.connection()
    json_msg_teg = json.dumps({'action': 'msg', 'mode': 'w'}).encode('utf-8')
    myChat.writemsg(json_msg_teg)
    login = 'Leo'
    addressee = 'Max'
    myChat.connection()
    msg = JimMessage(login, addressee, msg)
    data = msg.jsonmsg()
    myChat.writemsg(data)


def authenticate(login, password):
    '''
    Функция аутентификации
    :param login:
    :param password:
    :return:
    '''
    msg = JimAuthentication(login, password)
    request = msg.jsonmsg()
    data = connection(request)
    json_data = json.loads(data.decode('utf-8'))
    if json_data['response'] // 100 == 4:
        print(json_data['error'])
    return json_data


def registration(login, password):
    '''
    Функция регистрации
    :param login:
    :param password:
    :return:
    '''
    msg = JimRegistration(login, password)
    request = msg.jsonmsg()
    data = connection(request)
    json_data = json.loads(data.decode('utf-8'))
    return json_data


def connection(json_object, host=HOST, port=PORT):
    '''
    Функция соединения с сервером
    :param json_object:
    :return:
    '''
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))
    sock.send(json_object)

    data = sock.recv(1024)
    sock.close()
    return data


class Conversation:
    def __init__(self, host=HOST, port=PORT):
        self.host = host
        self.port = port
        self.sock = object()
        self.chat = list()


    def connection(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.host, self.port))


    def readmsg(self):
        self.data = self.sock.recv(1024)
        self.chat.append(json.loads(self.data.decode('utf-8')))


    def writemsg(self, json_object):
        self.chat.append(json_object)
        self.sock.send(json_object)


if __name__ == '__main__':
    print('Добро пожаловать в Tkilla.\n')