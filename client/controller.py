import json
import socket
import sys
import time
from jimprotocols import JimMessage, JimAuthentication, JimRegistration, JimHistory, JimAddContact, JimGetContact

HOST = 'localhost'
PORT = 7777

class Client:
    def __init__(self, login, password):
        self.login = login
        self.password = password


    def change_tokin(self, tokin):
        self.tokin = tokin


    def add_contact_list(self, contact_list):
        self.contactList = contact_list


    def add_history(self, history):
        self.history = history


    def __repr__(self):
        return self.login


    def toPlainText(self):
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


def get_contact_list(user):
    try:
        response = get_contacts(user.tokin)
        try:
            user.add_contact_list(response['contacts'])
            return (True, 'Получен список контактов', user)
        except:
            print('Некоректный ответ сервера')
        return (True, 'Получен список контактов', response)
    except ConnectionRefusedError:
        return (False, 'Сервер не отвечает')


def add_contact(user, peer):
    try:
        response = addcontact(user.tokin, peer)
        if response['response'] // 100 == 4:
            print(response['error'])
    except ConnectionRefusedError:
        print('Сервер не отвечает')
    except:
        print('Неизвестная ошибка')


def get_history(user, peer):
    try:
        response = gethistory(user.tokin, peer)
        if response['response'] // 100 == 4:
            print(response['error'])
        else:
            user.add_history(response['messages'])
            return (True, 'Получена история сообщений', user)
    except ConnectionRefusedError:
        return (False, 'Сервер не отвечает')
    except json.decoder.JSONDecodeError:
        return (False, 'Слишком большая история сообщений')
    except:
        return (False, 'Неизвестная ошибка')


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


def get_contacts(tokin):
    '''
    Функция получения контактов
    :param tokin:
    :return:
    '''
    msg = JimGetContact(tokin)
    request = msg.jsonmsg()
    data = connection(request)
    json_data = json.loads(data.decode('utf-8'))
    return json_data


def addcontact(tokin, peer):
    msg = JimAddContact(tokin, peer)
    request = msg.jsonmsg()
    data = connection(request)
    json_data = json.loads(data.decode('utf-8'))
    return json_data


def gethistory(tokin, peer):
    msg = JimHistory(tokin, peer)
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


class SocketEx:
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((HOST, 7777))

    def send(self, request):
        self.sock.send(json.dumps(request).encode('utf-8'))

    def recv(self):
        return self.sock.recv(1024)

    def close(self):
        self.sock.close()


if __name__ == '__main__':
    print('Добро пожаловать в Tkilla.\n')
