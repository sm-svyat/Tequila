import sys
import socket
import json
import time
from jimprotocols import JimMessage, JimAuthenticate

def authenticate(login, password):
    '''
    Функция аутентификации
    :param login:
    :param password:
    :return:
    '''

    msg = JimAuthenticate(login, password)
    request = msg.jsonmsg()

    #authenticate_request = {
    #                "action": "authenticate",
    #                "time": "<unix timestamp>",
    #                "user": {
    #                    "account_name": "C0deMaver1ck",
    #                    "password": "CorrectHorseBatteryStaple"
    #                }
    #            }

    #authenticate_request['time'] = time.ctime()
    #request = json.dumps(authenticate_request)

    data = connection(request)

    json_data = json.loads(data.decode('utf-8'))
    #print(json_data['response'])
    if json_data['response'] // 100 == 4:
        print(json_data['error'])
    return json_data

def check_tokin(tokin):

    check_tokin_request = {
                    "action": "presence",
                    "time": "<unix timestamp>",
                    "tokin": tokin
                }
    check_tokin_request['time'] = time.ctime()
    request = json.dumps(check_tokin_request)
    data = connection(request.encode('utf-8'))
    return(json.loads(data.decode('utf-8')))

def connection(json_object, host='localhost', port=8888):
    '''
    Функция соединения с сервером
    :param json_object:
    :return:
    '''
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))
    #sock.send(json_object.encode('utf-8'))
    sock.send(json_object)

    data = sock.recv(1024)
    sock.close()
    return data

class Conversation:
    def __init__(self, host='localhost', port=8888):
        self.host = host
        self.port = port
        self.sock = object()
        self.chat = list()

    def connection(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.host, self.port))


    def readmsg(self):
        #self.connection()
        self.data = self.sock.recv(1024)
        self.chat.append(json.loads(self.data.decode('utf-8')))

    def writemsg(self, json_object):
        #self.connection()
        self.chat.append(json_object)
        self.sock.send(json_object)



if __name__ == "__main__":

    try:
        mode = sys.argv[1]
        if mode not in ('r', 'w'):
            print('Режим должен быть r - чтение, w - запись')
            sys.exit(0)
    except IndexError:
        mode = 'r'

    my_chat = Conversation()
    my_chat.connection()

    if mode == 'w':
        json_msg_teg = json.dumps({'action': 'msg', 'mode': 'w'}).encode('utf-8')
        my_chat.writemsg(json_msg_teg)
        while True:
            msg = input(':) >')
            my_chat.connection()
            msg = JimMessage('Me', 'You', msg)
            data = msg.jsonmsg()
            my_chat.writemsg(data)


    elif mode == 'r':
        json_msg_teg = json.dumps({'action': 'msg', 'mode': 'r'}).encode('utf-8')
        my_chat.writemsg(json_msg_teg)
        while True:
            my_chat.readmsg()
            msg = my_chat.chat[-1]
            print('{} \n{:>80} \n{:>80}\n'.format(msg['message'], msg['from'], msg['time']))

    else:
        print('Неверный режим запуска {}. Режим запуска должен быть r - чтение или w - запись'.format(mode))