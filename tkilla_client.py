import sys
import socket
import json
import time
from jimprotocols import JimMessage

#def connection(json_object):

#    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#    sock.connect(('localhost', 8888))
#    sock.send(json_object.encode('utf-8'))


#    data = sock.recv(1024)
#    sock.close()
#    return data

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

#            authenticate_request = {
#            "action": "authenticate",
#            "time": "<unix timestamp>",
#            "user": {
#                "account_name": "C0deMaver1ck",
#                "password": "CorrectHorseBatteryStaple"
#            }
#        }

#        authenticate_request['time'] = time.ctime()
#        request = json.dumps(authenticate_request)
#        data = connection(request)

#        json_data = json.loads(data.decode('utf-8'))
#        print(json_data['response'])
#        if json_data['response'] // 100 == 4:
#            print(json_data['error'])

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
            #print('Здесь сообщение ', msg)
            print('{} \n{:>80} \n{:>80}\n'.format(msg['message'], msg['from'], msg['time']))

    else:
        print('Неверный режим запуска {}. Режим запуска должен быть r - чтение или w - запись'.format(mode))