import socket
import json
import time
import threading
import select


def get_reg_request(time, name, password):
    return {
        'action': 'registration',
        'time': time,
        'user': {
            'account_name': name,
            'password': password
        }
    }

def get_auth_request(time, name, password):
    return {
        'action': 'authenticate',
        'time': time,
        'user': {
            'account_name': name,
            'password': password
        }
    }

def get_send_msg_request(time, tokin, to_id, message):
    return {
        'action': 'msg',
        'tokin': tokin,
        'to': to_id,
        'time': time,
        'message': message
    }

def get_add_contact_request(tokin, contact_id):
    return {
        'action': 'add_contact',
        'tokin': tokin,
        'contact': contact_id
    }

def get_get_contacts_request(tokin):
    return {
        'action': 'get_contacts',
        'tokin': tokin,
    }

class SocketEx:
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect(('127.0.0.1', 7777))

    def send(self, request):
        self.sock.send(json.dumps(request).encode('utf-8'))

    def recv(self):
        return self.sock.recv(1024)

    def close(self):
        self.sock.close()

def get_get_history_request(tokin, peer):
    return {
        'action': 'history',
        'tokin': tokin,
        'to': peer
    }


class Listener(threading.Thread):
    def __init__(self, tokin, peer_id):
        threading.Thread.__init__(self)
        self.tokin = tokin
        self.peer_id = peer_id
        self.continue_flag = True

    def stop(self):
        self.continue_flag = False

    def run(self):
        print('listening for updates...')
        request = {
            'action': 'updates',
            'tokin': self.tokin,
            'peer': self.peer_id
        }
        sock = SocketEx()
        sock.send(request)
        while self.continue_flag:
            r, _, _ = select.select([sock.sock], [], [], 1)
            if r:
                response = sock.recv()
                if len(response) == 0:
                    break
                print('response:', response.decode('utf-8'))

def get_json(bytes_data):
    return json.loads(bytes_data.decode('utf-8'))

def main():
    sock = SocketEx()
    sock.send(get_auth_request('today', 'dron', '1234'))
    response = get_json(sock.recv())
    sock.close()
    if response['response'] != 200:
        print('auth failed!')
        print(response)
        return
    tokin = response['tokin']
    test_requests = [
        get_reg_request(time.ctime(), 'mr_dick_{}'.format(int(time.time()) % 1000),
            'passwd_{}'.format(int(time.time()) % 10)),
        #get_auth_request('today', '2', '2'),
        #get_get_history_request(tokin, 'svyat'),
        #get_send_msg_request(time.ctime(), tokin, 'svyat', 'hello uassa'),
        #get_send_msg_request(time.ctime(), tokin, '1', 'hello uassa 1'),
        #get_send_msg_request(time.ctime(), tokin, '2', 'hello uassa 2'),
        #get_add_contact_request(tokin, '1'),
        #get_add_contact_request('dron', 'svyat'),
        #get_add_contact_request('svyat', 'dron'),
        get_get_contacts_request(tokin),
        #get_get_contacts_request('1'),
    ]
    for request in test_requests:
        sock = SocketEx()
        print('request:', request)
        sock.send(request)
        response = sock.recv()
        print('response:', response.decode('utf-8'))
        sock.close()
    listener = Listener(tokin, 'svyat')
    listener.start()

    # Stop this motherfucker! (does work, you can take it to the bank)
    # time.sleep(5)
    # listener.stop()

    listener.join()

if __name__ == "__main__":
    main()
