import sys
import json
from PyQt5 import QtWidgets
from threading import Thread
import scheme_gui_client
#from tkilla_client import Conversation,JimMessage
from run_tkilla_client import recording, log_in, Conversation,JimMessage
from client import SocketEx
import select

reader = None
user = object()

class InitialUi_MainWindow(scheme_gui_client.Ui_MainWindow):
    def setupUi(self, MainWindow):
        scheme_gui_client.Ui_MainWindow.setupUi(self, MainWindow)
        self.frameRegistration.hide()
        self.frameAuthentification.hide()
        self.frameConversation.hide()


class TkillaWindow(QtWidgets.QMainWindow):
    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        self.ui = InitialUi_MainWindow()
        self.ui.setupUi(self)
        self.ui.pushButtonRegistration.clicked.connect(Registration(self.ui.frameEntry, self.ui.frameRegistration))
        self.ui.pushButtonAuthentification.clicked.connect(Authentification(self.ui.frameEntry, self.ui.frameAuthentification))
        self.ui.pushButtonRegistrationOk.clicked.connect(CheckRegistration(self.ui.lineEditNewLogin, self.ui.lineEditNewPasswd, self.ui.lineEditRepeatNewPasswd, self.ui.frameEntry, self.ui.frameRegistration, self.ui.frameConversation, self.ui.textBrowserReadMsg))
        self.ui.pushButtonAuthentificationOk.clicked.connect(CheckAuthentification(self.ui.lineEditLogin, self.ui.lineEditPasswd, self.ui.frameEntry, self.ui.frameAuthentification, self.ui.frameConversation, self.ui.textBrowserReadMsg))
        self.ui.pushButtonSendMsg.clicked.connect(Writer(self.ui.plainTextEditWriteMsg))
        self.ui.pushButtonLogout.clicked.connect(Logout(self.ui.frameConversation, self.ui.textBrowserReadMsg, self.ui.frameEntry))


    def closeEvent(self, event):
        reader.stop()
        event.accept()


class CheckAuthentification:
    def __init__(self, lineEditLogin, lineEditPasswd, frameEntry, frameAuthentification, frameConversation, textBrowserReadMsg):
        self.lineEditLogin = lineEditLogin
        self.lineEditPasswd = lineEditPasswd
        self.frameEntry = frameEntry
        self.frameAuthentification = frameAuthentification
        self.frameConversation = frameConversation
        self.textBrowserReadMsg = textBrowserReadMsg

    def __call__(self):
        try:
            requestAuthentification = log_in(self.lineEditLogin.text(), self.lineEditPasswd.text())
            if requestAuthentification[0]:
                print(requestAuthentification[1])
                self.frameAuthentification.hide()
                self.frameConversation.show()
                try:
                    global reader, user
                    user = requestAuthentification[2]
                    print("Добро пожаловать в Tequila, {}!".format(user.login))
                    reader = Reader(user, self.textBrowserReadMsg)
                    reader()
                except:
                    print('Ощибка при плучениии сообщений')
            else:
                print(requestAuthentification[1])
                self.frameAuthentification.hide()
                self.frameEntry.show()
        except:
            print("Ошибка авторизации на стороне клиента")
        self.lineEditLogin.clear()
        self.lineEditPasswd.clear()


class CheckRegistration:
    def __init__(self, lineEditNewLogin, lineEditNewPasswd, lineEditRepeatNewPasswd, frameEntry, frameRegistration,
                 frameConversation, textBrowserReadMsg):

        self.lineEditNewLogin = lineEditNewLogin
        self.lineEditNewPasswd = lineEditNewPasswd
        self.lineEditRepeatNewPasswd = lineEditRepeatNewPasswd
        self.frameEntry = frameEntry
        self.frameRegistration = frameRegistration
        self.frameConversation = frameConversation
        self.textBrowserReadMsg = textBrowserReadMsg


    def __call__(self):
        try:
            requestRegistration = recording(self.lineEditNewLogin.text(), self.lineEditNewPasswd.text(), self.lineEditRepeatNewPasswd.text())
            if requestRegistration[0]:
                print(requestRegistration[1])
                self.frameRegistration.hide()
                self.frameConversation.show()
                try:
                    global reader, user
                    user = requestRegistration[2]
                    print("Добро пожаловать в Tequila, {}!".format(user.login))
                    reader = Reader(user, self.textBrowserReadMsg)
                    reader()
                except:
                    print('Ошибка при плучениии сообщений')

            else:
                print(requestRegistration[1])
                self.frameRegistration.hide()
                self.frameEntry.show()

        except:
            print("Ошибка регистрации на стороне клиента")
        self.lineEditNewLogin.clear()
        self.lineEditNewPasswd.clear()
        self.lineEditRepeatNewPasswd.clear()


class Writer:
    def __init__(self, plainTextEditWriteMsg):
        self.plainTextEditWriteMsg = plainTextEditWriteMsg

    def __call__(self):
        try:
            msg = self.plainTextEditWriteMsg.toPlainText()
            self.plainTextEditWriteMsg.clear()
            self.write_msg(msg)
        except:
            print('Что-то сломалось при отправке сообщения на стороне клиента')


    def write_msg(self, msg):
        print('Пытаюсь писать')
        myChat = Conversation()
        myChat.connection()
        #json_msg_teg = json.dumps({'action': 'msg', 'mode': 'w'}).encode('utf-8')
        #myChat.writemsg(json_msg_teg)
        addressee = 'dron'
        myChat.connection()
        msg = JimMessage(user.tokin, addressee, msg)
        data = msg.jsonmsg()
        myChat.writemsg(data)


class Reader(Thread):
    def __init__(self, user, textBrowserReadMsg):
        Thread.__init__(self)
        self.textBrowserReadMsg = textBrowserReadMsg
        self.user = user
        self.peer_login = 'dron'
        self.continueFlag = True
        #self.myChat = Conversation('194.67.222.96', 7777)
        self.myChat = Conversation('localhost', 7777)


    def __call__(self):
        try:
            self.start()

        except:
            print('Что-то сломалось при попытке прочесть сообщение')


    def run(self):
        '''self.continueFlag = True
        self.myChat.connection()
        #json_msg_teg = json.dumps({'action': 'msg', 'mode': 'r'}).encode('utf-8')
        #self.myChat.writemsg(json_msg_teg)
        while self.continueFlag:
            self.myChat.readmsg()
            msg = self.myChat.chat[-1]
            self.textBrowserReadMsg.append('{} \n{:>80} \n{:>80}\n'.format(msg['message'], msg['from'], msg['time']))
            print('{} \n{:>80} \n{:>80}\n'.format(msg['message'], msg['from'], msg['time']))
            '''
        print('listening for updates...')
        request = {
            'action': 'updates',
            'tokin': self.user.tokin,
            'peer': self.peer_login
        }
        sock = SocketEx()
        sock.send(request)
        response = sock.recv()
        json_data = json.loads(response.decode('utf-8'))
        if json_data['response'] // 100 == 2:
            while self.continueFlag:
                r, _, _ = select.select([sock.sock], [], [], 1)
                if r:
                    response = sock.recv()
                    msg = json.loads(response.decode('utf-8'))
                    print(msg)
                    if len(response) == 0:
                        break
                    #self.textBrowserReadMsg.append(str(msg))
                    self.textBrowserReadMsg.append('{} \n{:>150} \n{:>150}\n'.format(msg['message'], msg['from'], msg['time']))
                    #print('response:', response.decode('utf-8'))
        else:
            print('Некоректный ответ')


    def stop(self):
        self.continueFlag = False
        print('Конец сессии.')
        self.join()


class Authentification:
    def __init__(self, frameEntry, frameAuthentification):
        self.frameEntry = frameEntry
        self.frameAuthentification = frameAuthentification

    def __call__(self):
        print("Переход в окно авторизации")
        self.frameEntry.hide()
        self.frameAuthentification.show()


class Registration:
    def __init__(self, frameEntry, frameRegistration):
        self.frameEntry = frameEntry
        self.frameRegistration = frameRegistration

    def __call__(self):
        print("Переход в окно регистрации")
        self.frameEntry.hide()
        self.frameRegistration.show()


class Logout:
    def __init__(self, frameConversation, textBrowserReadMsg, frameEntry):
        self.frameConversation = frameConversation
        self.textBrowserReadMsg = textBrowserReadMsg
        self.frameEntry = frameEntry


    def __call__(self):
        self.textBrowserReadMsg.clear()
        reader.stop()
        self.frameConversation.hide()
        self.frameEntry.show()


if __name__ == '__main__':

    app = QtWidgets.QApplication(sys.argv)
    window = TkillaWindow()
    window.show()
    sys.exit(app.exec_())
