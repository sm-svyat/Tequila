import sys
from subprocess import Popen, CREATE_NEW_CONSOLE
from tkilla_client import authenticate, check_tokin


class Client:
    def __init__(self, login, password):
        self.login = login
        self.password = password
        self.tokin = str()

    def change_tokin(self, tokin):
        self.tokin = tokin

    def __repr__(self):
        return self.login


def run():
    instruction = input('Введите инструкцию:\n')
    try:
        do[instruction]()
    except KeyError:
        print('Данная иструкция не существует. Используйте \\help, чтобы узнать полный список.\n')
        run()

def print_help():
    print('\\help - получение справки')
    print('\\log in - войти в систему')
    print('\\chat - создать чат')
    print('\\presence - проверить токин')
    print('\\q - выйти из приложения')
    run()

def log_in():
    login = input('Введите login\n')
    password = input('Введите password\n')
    global user
    user = Client(login, password)
    try:
        response = authenticate(user.login, user.password)
        print(response)
        user.change_tokin(response['tokin'])

    except ConnectionRefusedError:
        print("Чет сервер не отвечает :с")
    run()

def chat():
    try:
        addressee = 'You'
        Popen('python tkilla_client.py w {} {}'.format(user.login, addressee), creationflags=CREATE_NEW_CONSOLE)
        Popen('python tkilla_client.py r', creationflags=CREATE_NEW_CONSOLE)
    except NameError:
        print('Вы пока не вошли в систему.\nИспользуйте команду \"\\log in\" для аунтентификации\n')
    run()

def presence():
    print(user.login, user.tokin)
    print(check_tokin(user.tokin))
    run()

def stop_client():
    print('Выход из Tkilla')
    sys.exit()

if __name__ == '__main__':

    do = {
        "\\help": print_help,
        '\\log in': log_in,
        '\\chat': chat,
        '\\presence': presence,
        '\\q': stop_client,
    }
    print('Добро пожаловать в Tkilla.\n')
    run()