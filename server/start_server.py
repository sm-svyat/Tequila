import json
import socket

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database.bd import User, Message, Contact

class DB:
    def __init__(self, session):
        self.session = session

    def get_user_by_tokin(self, tokin):
        return session.query(User).filter_by(tokin=tokin).first()

    def get_user(self, login):
        return session.query(User).filter_by(login = login).first()

    def get_user_nickname(self, user_id):
        return session.query(User).filter_by(id=user_id).first().login

    def commit(self):
        self.session.commit()

    def add_user(self, user):
        user.create_tokin()
        self.session.add(user)

    def get_messages(self, user1, user2):
        messages = self.session.query(Message).filter_by(from_id=user1, to_id=user2)
        for message in messages:
            yield message
        messages = self.session.query(Message).filter_by(from_id=user2, to_id=user1)
        for message in messages:
            yield message

    def add_message(self, from_id, to_id, time, message):
        message = Message(from_id, to_id, time, message)
        self.session.add(message)
        self.commit()

    def add_contact(self, user_id, contact_id):
        if self.session.query(Contact).filter_by(user_id=user_id, contact_id=contact_id).first():
            print('trying to add existing contact')
            return
        contact = Contact(user_id, contact_id)
        self.session.add(contact)
        self.commit()

    def get_contacts(self, user_id):
        for contact in self.session.query(Contact).filter_by(user_id=user_id):
            if self.session.query(Contact).filter_by(user_id=contact.contact_id, contact_id=user_id).first():
                contact.accepted = True
            else:
                contact.accepted = False
            yield contact

    def has_contact(self, user_id, peer_id):
        if not self.session.query(Contact).filter_by(user_id=user_id, contact_id=peer_id).first():
            return False
        if not self.session.query(Contact).filter_by(user_id=peer_id, contact_id=user_id).first():
            return False
        return True

class DummyClient:
    def __init__(self, data):
        self.data = data

    def recv(self, len):
        return self.data

    def send(self, response):
        print("response: ", response)

class UserServer:
    def __init__(self, chat, client):
        self.client = client
        self.chat = chat
        self.do_close_socket = True
        self.responsers = {
            'authenticate': self.authenticate,
            'msg':          self.conversation,
            'registration': self.registration,
            'history'     : self.get_history,
            'updates'     : self.get_updates,
            'add_contact' : self.add_contact,
            'get_contacts': self.get_contacts,
        }


    def serve(self):
        error_response = {
            "response": 400,
            "error": "Bad request"
        }
        try:
            data = self.client.recv(1024)
            self.request = json.loads(data.decode('utf-8'))
            action = self.request['action']
            print('action:', action)
            response = self.responsers[action]()
            if response is None:
                response = error_response
            self.send_response(response)
            return self.do_close_socket
        except IndentationError:
            print('Error 400. Wrong JSON-object.')
        except json.decoder.JSONDecodeError:
            print('Error 400. Wrong JSON-object. 2')
        except UnicodeDecodeError:
            print('\'utf-8\' codec can\'t decode byte 0xc3 in position 7: invalid continuation byte')
        #except KeyError:
        #    print('Key error in request')
        #except Exception as e:
        #except Exception as e:
            #print('Unknown exception during serving a client: {}'.format(e))
        self.send_response(error_response)
        return self.do_close_socket

    def send_response(self, response):
        #print(response)
        response = json.dumps(response)
        self.client.send(response.encode('utf-8'))

    def add_contact(self):
        '''
        request:
        {
            action: 'add_contact',
            tokin: 'xxx',
            contact: 'contact_nickname'
        }
        response:
        {
            'response': 200
        }
        or an ordinary error response
        '''
        try:
            user = db.get_user_by_tokin(self.request['tokin'])
            contact = db.get_user(self.request['contact'])
            if not user or not contact:
                print('add_contact: no such users')
                return {
                'response': 402,
                "error": "no such users"
            }
            user_id = user.id
            contact_id = contact.id
            db.add_contact(user_id, contact_id)
            return {
                'response': 200
            }
        except KeyError:
            print('key error in add_contact')
            return None

    def get_contacts(self):
        '''
        {
            'action': 'get_contacts',
            'tokin': 'xxx'
        }
        '''
        print('...getting contacts...')
        try:
            user = db.get_user_by_tokin(self.request['tokin'])
            if not user:
                print('get_contacts: no such user')
                return None
        except KeyError:
            print('key error in get_contacts')
            return None
        contacts = []
        for contact in db.get_contacts(user.id):
            contacts.append((db.get_user_nickname(contact.contact_id), contact.accepted))
        return {
            'response': 200,
            'contacts': contacts
        }

    def get_history(self):
        '''
        Request must have the following schema:
        {
            tokin: "xxx",
            from: "from_nickname"
            to: "to_nickname"
        }
        '''
        from_user = db.get_user_by_tokin(self.request['tokin'])
        to_user = db.get_user(self.request['to'])
        if not from_user or not to_user:
            print('No user')
            return None
        messages = []
        for message in db.get_messages(from_user.id, to_user.id):
            messages.append((message.id, message))
        messages.sort(key=lambda x: x[0])
        response = {
            'response': 200,
            'messages': []
        }
        for message in messages:
            response['messages'].append(str(message[1]))
        return response



    def authenticate(self):
        '''
        Request:
        {
            'action': 'authenticate',
            'time': 'time'
            'user': {
                'account_name': 'name',
                'password': 'password'
            }
        }
        Successful response:
        {
            'response': 200,
            'tokin': 'xxx'
        }
        '''
        login = self.request['user']['account_name']
        db_user = db.get_user(login)
        if not db_user:
            print("Ошибка 402, \"Wrong password or no account with that name\"")
            return {
                "response": 402,
                "error": "No account with that name"
            }
        if self.request['user']['password'] == db_user.password:
            print("Пользователь с ником {} прошел аунтентификацию {}"
                    .format(self.request['user']['account_name'], self.request['time']))
        else:
            print("Ошибка 402, \"Wrong password\"")
            return {
                "response": 402,
                "error": "Wrong password or no account with that name"
            }
        db_user.create_tokin()
        db.commit()
        return {
            "response": 200,
            "alert": "Authentication is successful",
            "tokin": db_user.tokin
        }

    def get_updates(self):
        ok_response = {
            'response': 200
        }
        try:
            user = db.get_user_by_tokin(self.request['tokin'])
            if not user:
                print('no such user')
                return None
            self.chat.add_reading_client(self.client, user.login, self.request['peer'])
            self.do_close_socket = False
            return ok_response
        except KeyError:
            print('key error for get_updates')
            return None


    def conversation(self):
        ok_response = {
            'response': 200
        }
        if self.chat.add_message(self.request):
            return ok_response
        return None

    def registration(self):
        login = self.request['user']['account_name']
        user = db.get_user(login)
        if user:
            print('Попытка зарегестрировать существующий login - {}'.format(login))
            return {
                "response": 402,
                "error": "The user with this login already exists"
            }
        try:
            user = User(login, self.request['user']['password'])
            db.add_user(user)
            db.commit()
            print("Пользователь с ником %s прошел регистрацию %s" % (login, self.request['time']))
            return {
                "response": 200,
                "alert": "Registration is successful",
                "tokin": user.tokin
            }
        except:
            print('Что-то пошло не так при регистрации, глянь что там')
            return None


class MainServer:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.chat = Chat()

    def connect(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Avoid 'adress already in use' error
        # https://stackoverflow.com/a/6380198
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.ip, self.port))
        self.sock.listen(15)
        self.run()

    def run(self):
        '''
        # tests start...
        datas = [
                b'{"action": "authenticate", "time": "time", "user": {"account_name": "1", "password": "1"}}',
                b'{"action": "msg", "mode": "r"}',
                b'{"action": "msg", "tokin": "xxx", "from": "1", "to": "2", "time": "time", "message": "hello"}',
                b'{"action": "history", "from": "1", "to": "2"}'
                ]
        for data in datas:
            client = DummyClient(data)
            server = UserServer(self.chat, client)
            server.serve()
        return
        # tests finished.
        '''
        while True:
            print('waiting for a client...')
            client, self.addr = self.sock.accept()
            print('accepted!')
            server = UserServer(self.chat, client)
            if server.serve():
                client.close()


class Chat:
    def __init__(self):
        self.reading_clients = list()

    def add_reading_client(self, client, user_nick, peer_nick):
        print('add reading client')
        self.reading_clients.append((user_nick, peer_nick, client))

    def add_message(self, request):
        '''
        message must have the following schema:
        {
            tokin: "xxx",
            to: "to_nickname"
            time: "time"
            message: "message"
        }
        '''
        try:
            from_user = db.get_user_by_tokin(request['tokin'])
            to_user = db.get_user(request['to'])
            if not from_user or not to_user:
                print('No user')
                return False
            if not db.has_contact(from_user.id, to_user.id):
                print('Not in contact list')
                return False
            from_id = from_user.id
            to_id = to_user.id
            db.add_message(from_id, to_id, request['time'], request['message'])
            request.pop('tokin')
            request['from'] = from_user.login
            self.write_requests(request)
            return True
        except KeyError:
            print('key error in message')
            return False

    def write_requests(self, request):
        """
        Отправка сообщений тем клиентам, которые их ждут
        """
        for target_user, target_peer, sock in self.reading_clients:
            message = request
            print(target_user, target_peer, message)
            if ((message['from'], message['to']) != (target_user, target_peer) and
                (message['from'], message['to']) != (target_peer, target_user)):
                    continue
            try:
                print('send message to reader')
                message = json.dumps(message)
                resp = message.encode('utf-8')
                sock.send(resp)
            except (BrokenPipeError, ConnectionResetError):
                print('Удаленный хост принудительно разорвал существующее подключение')

                #    print('Какие-то проблемы при записи сообщений отправленных в чат')
                    # Реализовать отключение клиента

if __name__ == '__main__':

    engine = create_engine('sqlite:///database/tkilla_database.db', echo=False)
    pool_recycle = 7200  # переустановление соединения с бд через каждые 2 часа

    Session = sessionmaker(bind=engine)
    session = Session()
    db = DB(session)

    server = MainServer('', 7777)
    server.connect()
