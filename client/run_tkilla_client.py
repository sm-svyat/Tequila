import sys
from subprocess import Popen, CREATE_NEW_CONSOLE

from tkilla_client import authenticate, check_tokin, registration


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
        print(instruction)
        print('Данная иструкция не существует. Используйте \\help, чтобы узнать полный список.\n')
        run()


def print_help():
    print('\\help - получение справки')
    print('\\reg - зарегестрироваться')
    print('\\log in - войти в систему')
    print('\\chat - создать чат')
    print('\\presence - проверить токин')
    print('\\q - выйти из приложения')
    run()


def recording(login, password, second_passwd):
    #login = input('Введите login\n')
    #password = input('Введите password\n')
    #second_passwd = input('Повторите password\n')
    print(login)
    if password == second_passwd:
        global user
        user = Client(login, password)
        try:
            response = registration(login, password)
            if 'tokin' in response.keys():
                user.change_tokin(response['tokin'])
                presence()
            elif 'error' in response.keys():
                print(response['error'])

            else:
                print('Пришел некоректный ответ.')

        except ConnectionRefusedError:
            print("Сервер не отвечает")

    else:
        print('Пароли не совпадают.\nПройдите регистрацию заново.')
    #run()


def log_in(login, password):
#def log_in():
    #login = input('Введите login\n')
    #password = input('Введите password\n')
    global user
    user = Client(login, password)
    try:
        response = authenticate(user.login, user.password)
        if 'tokin' in response.keys():
            user.change_tokin(response['tokin'])
            presence()
        elif 'error' in response.keys():
            print(response['error'])

        else:
            print('Пришел некоректный ответ.')

    except ConnectionRefusedError:
        print("Чет сервер не отвечает :с")
    print('Bye!')
    #run()


def chat():
    try:
        addressee = 'You'
        Popen('python tkilla_client.py w {} {}'.format(user.login, addressee), creationflags=CREATE_NEW_CONSOLE)
        Popen('python tkilla_client.py r', creationflags=CREATE_NEW_CONSOLE)
    except NameError:
        print('Вы пока не вошли в систему.\nИспользуйте команду \"\\log in\" для аунтентификации\n')
    run()


def presence():
    try:
        print('Проверка токина')
        print(check_tokin(user.tokin))
    except NameError:
        print('Вы пока не вошли в систему.\nИспользуйте команду \"\\log in\" для аунтентификации\n')
    #run()


def stop_client():
    print('Выход из Tkilla')
    sys.exit()


if __name__ == '__main__':

    do = {
        "\\help": print_help,
        '\\reg': recording,
        '\\log in': log_in,
        '\\chat': chat,
        '\\presence': presence,
        '\\q': stop_client,
    }
    print('Добро пожаловать в Tkilla.\n')
    run()