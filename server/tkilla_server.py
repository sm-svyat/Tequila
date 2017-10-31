import json
import socket

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database.bd import User


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
        self.clients = list()
        self.chat = Chat()
        self.user = User
        self.tokin_dict = dict()
        self.users_list = list()
        self.accounts_dict = dict()
        self.responses_dict = {"authenticate": self.authenticate,
                             "msg": self.conversation, "presence": self.presence,
                             "registration": self.registration}

    def connect(self):

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((self.ip, self.port))
        self.sock.listen(15)
        self.run()

    def run(self):
        while True:
            self.client, self.addr = self.sock.accept()
            self.clients.append(self.client)

            try:
                self.data = self.client.recv(1024)
                self.json_data = json.loads(self.data.decode('utf-8'))
                self.response_generator()
            except IndentationError:
                print('Error 400. Wrong JSON-object.')
                continue
            except json.decoder.JSONDecodeError:
                print('Error 400. Wrong JSON-object. 2')
                continue
            except UnicodeDecodeError:
                print('\'utf-8\' codec can\'t decode byte 0xc3 in position 7: invalid continuation byte')
                continue

    def response_generator(self):
        try:
            self.responses_dict[self.json_data['action']]()

        except KeyError:
            error_response = {
                "response": 400,
                "error": "Bad request"
                }
            self.send_response(error_response)

    def send_response(self, response):
        self.string = json.dumps(response)
        self.client.send(self.string.encode('utf-8'))
        self.client.close()

    def registration(self):
        if session.query(User).filter_by(login = self.json_data['user']['account_name']).first():
            print('Попытка зарегестрировать существующий login - {}'.format(self.json_data['user']['account_name']))

            error_response = {
                "response": 402,
                "error": "The user with this login already exists"
            }
            self.send_response(error_response)

        else:
            try:
                self.user = User(self.json_data['user']['account_name'], self.json_data['user']['password'])
                session.add(self.user)
                self.user.create_tokin()
                session.commit()
                print("Пользователь с ником %s прошел регистрацию %s" % (self.json_data['user']['account_name'], self.json_data['time']))

            except:
                print('Что-то пошло не так при регистрации, глянь что там')

            self.users_list.append(self.user)
            self.accounts_dict[self.json_data['user']['account_name']] = self.user
            self.tokin_dict[self.user.tokin] = self.user
            response = {
                "response": 200,
                "alert": "Registration is successful",
                "tokin": self.user.tokin
            }
            print(self.users_list)
            self.send_response(response)

    def authenticate(self):
        #if self.json_data['user']['account_name'] in users.keys():
        if session.query(User).filter_by(login = self.json_data['user']['account_name']).first():
            bd_user = session.query(User).filter_by(login = self.json_data['user']['account_name']).first()
            #if self.json_data['user']['password'] == users[self.json_data['user']['account_name']]:
            if self.json_data['user']['password'] == bd_user.password:
                print("Пользователь с ником %s прошел аунтентификацию %s" % (self.json_data['user']['account_name'], self.json_data['time']) )
                #self.user = User(self.json_data['user']['account_name'], self.json_data['user']['password'])
                if self.json_data['user']['account_name'] in [user.login for user in self.users_list]:
                    response = {
                        "response": 200,
                        "alert": "Authentication is successful",
                        "tokin": self.accounts_dict[self.json_data['user']['account_name']].tokin
                    }
                else:
                    #self.user = User(self.json_data['user']['account_name'], self.json_data['user']['password'])
                #Создание токина
                    #self.user.create_tokin()
                    bd_user.create_tokin()
                    session.commit()
                    #self.users_list.append(self.user)
                    self.users_list.append(bd_user)
                    #self.accounts_dict[self.json_data['user']['account_name']] = self.user
                    self.accounts_dict[self.json_data['user']['account_name']] = bd_user
                    #self.tokin_dict[self.user.tokin] = self.user
                    self.tokin_dict[self.user.tokin] = bd_user
                    response = {
                        "response": 200,
                        "alert": "Authentication is successful",
                        "tokin": bd_user.tokin
                    }
                print(self.users_list)
                self.send_response(response)

            else:
                error_response = {
                    "response": 402,
                    "error": "Wrong password or no account with that name"
                    }
                print("Ошибка 402, \"Wrong password\"")
                self.send_response(error_response)

        else:
            error_response = {
                "response": 402,
                "error": "No account with that name"
            }
            print("Ошибка 402, \"Wrong password or no account with that name\"")
            self.send_response(error_response)

    def conversation(self):
        #self.chat = Chat()
        try:
            if self.json_data['mode'] == 'w':
                self.chat.add_writing_client(self.client)
                return

            elif self.json_data['mode'] == 'r':
                self.chat.add_reading_client(self.client)
                print(self.chat.reading_clients)
                return

            else:
                print('Неверный режим запуска {}. Режим запуска должен быть r - чтение или w - запись'.format(self.json_data['mode']))
        except KeyError:
            pass
            print('Некорректное подключение к чату')

        #print(self.json_data['message'])
        self.chat.chat_history.append(self.json_data)
        #self.chat.read_requests()  # Получаем входные сообщения
        print(self.chat.chat_history)
        self.chat.write_requests() # Выполним отправку входящих сообщений

    def presence(self):
        #if self.json_data['tokin'] in self.tokin_dict.keys():
        if session.query(User).filter_by(tokin = self.json_data['tokin']).first():
            self.user = session.query(User).filter_by(tokin = self.json_data['tokin']).first()
            #print('Вот все мои токины\n', self.tokin_dict.keys())
            #u = self.tokin_dict[self.json_data['tokin']]
            response = {
                "response": 400,
                "alert": self.user.login,
                "tokin": self.user.tokin
            }
            self.send_response(response)
        else:
            print('Неверный токин клиента.')
            response = {
                "response": 403,
                "alert": "Неверный токин. Пройди аунтентификацию.",
            }
            self.send_response(response)

class Chat:
    def __init__(self):
        self.chat_history = list()
        self.instant_messages = list()
        self.clients = list()
        self.writing_clients = list()
        self.reading_clients = list()

    def add_writing_client(self, client):
        self.writing_clients.append(client)

    def add_reading_client(self, client):
        self.reading_clients.append(client)

    def read_requests(self):
        """
        Чтение сообщений, которые будут посылать клиенты
        """
        self.instant_messages = list()
        for sock in self.writing_clients:
            try:
                self.data = sock.recv(1024).decode('utf-8')
                self.chat_history.append(self.data)
                self.instant_messages.append(self.data)
            except:
                print('Какие-то проблемы при чтении сообщений отправленных в чат')
                #Реализовать отключение клиента TODO

    def write_requests(self):
        """
        Отправка сообщений тем клиентам, которые их ждут
        """
        for sock in self.reading_clients:
        #    for message in self.chat_history:
            message = self.chat_history[-1]
            try:
                message = json.dumps(message)
                resp = message.encode('utf-8')
                sock.send(resp)

            except ConnectionResetError:
                print('Удаленный хост принудительно разорвал существующее подключение')

                #    print('Какие-то проблемы при записи сообщений отправленных в чат')
                    # Реализовать отключение клиента

if __name__ == '__main__':

    engine = create_engine('sqlite:///database/tkilla_database.db', echo=False)
    pool_recycle = 7200  # переустановление соединения с бд через каждые 2 часа

    Session = sessionmaker(bind=engine)
    session = Session()

    server = MainServer('', 7777)
    server.connect()