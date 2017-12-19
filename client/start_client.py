import sys
import json
from PyQt5 import QtWidgets
from PyQt5.QtGui import QStandardItem, QStandardItemModel
from threading import Thread
import ui_client
from controller import recording, log_in, Conversation,JimMessage, get_contact_list, add_contact, get_history, SocketEx
#from client import SocketEx
import select

reader = None
user = object()
PEER = 'Max'

class InitialUi_MainWindow(ui_client.Ui_MainWindow):
    def setupUi(self, MainWindow):
        ui_client.Ui_MainWindow.setupUi(self, MainWindow)
        self.MainWindow = MainWindow
        self.MainWindow.resize(290, 589)
        self.frameRegistration.hide()
        self.frameAuthentification.hide()
        self.frameConversation.hide()
        global contactListWiew
        QStandardItemModel(self.listViewContactList)
        self.contactListWiew = QStandardItemModel(self.listViewContactList)


class TkillaWindow(QtWidgets.QMainWindow):
    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        self.ui = InitialUi_MainWindow()
        self.ui.setupUi(self)
        self.ui.pushButtonRegistration.clicked.connect(Registration(self.ui.frameEntry, self.ui.frameRegistration))
        self.ui.pushButtonAuthentification.clicked.connect(Authentification(self.ui.frameEntry, self.ui.frameAuthentification))
        self.ui.pushButtonRegistrationOk.clicked.connect(CheckRegistration(self.ui.lineEditNewLogin, self.ui.lineEditNewPasswd, self.ui.lineEditRepeatNewPasswd, self.ui.frameEntry, self.ui.frameRegistration, self.ui.frameConversation,self.ui.listViewContactList,self.ui.contactListWiew, self.ui.textBrowserReadMsg, self.ui.MainWindow))
        self.ui.pushButtonAuthentificationOk.clicked.connect(CheckAuthentification(self.ui.lineEditLogin, self.ui.lineEditPasswd, self.ui.frameEntry, self.ui.frameAuthentification, self.ui.frameConversation,self.ui.listViewContactList, self.ui.contactListWiew, self.ui.textBrowserReadMsg, self.ui.MainWindow))
        self.ui.pushButtonSendMsg.clicked.connect(Writer(self.ui.plainTextEditWriteMsg))
        self.ui.pushButtonLogout.clicked.connect(Logout(self.ui.frameConversation, self.ui.textBrowserReadMsg, self.ui.frameEntry, self.ui.MainWindow))
        self.ui.pushButtonAddContact.clicked.connect(AddContact(self.ui.plainTextEditNewContact, self.ui.listViewContactList,self.ui.contactListWiew, self.ui.textBrowserReadMsg))
        #self.ui.contactListWiew().selectionChanged.connect(change_peer)


    def closeEvent(self, event):
        reader.stop()
        event.accept()


class CheckAuthentification:
    def __init__(self, lineEditLogin, lineEditPasswd, frameEntry, frameAuthentification, frameConversation,listViewContactList, contactListWiew, textBrowserReadMsg, MainWindow):
        self.lineEditLogin = lineEditLogin
        self.lineEditPasswd = lineEditPasswd
        self.frameEntry = frameEntry
        self.frameAuthentification = frameAuthentification
        self.frameConversation = frameConversation
        self.listViewContactList = listViewContactList
        self.contactListWiew = contactListWiew
        self.textBrowserReadMsg = textBrowserReadMsg
        self.MainWindow = MainWindow

    def __call__(self):
        try:
            requestAuthentification = log_in(self.lineEditLogin.text(), self.lineEditPasswd.text())
            if requestAuthentification[0]:
                print(requestAuthentification[1])
                self.MainWindow.resize(889, 589)
                self.frameAuthentification.hide()
                self.frameConversation.show()
                try:
                    global reader, user
                    user = requestAuthentification[2]
                    print("Добро пожаловать в Tequila, {}!".format(user.login))
                    print("geting contact list...")
                    GetContacts(self.listViewContactList, self.contactListWiew, self.textBrowserReadMsg)()
                    print("getting history...", PEER)
                    GetHistory(PEER, self.textBrowserReadMsg)()
                    reader = Reader(user, self.textBrowserReadMsg)
                    reader()
                except:
                    print('Ошибка при плучениии сообщений')
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
                 frameConversation,listViewContactList, contactListWiew, textBrowserReadMsg, MainWindow):

        self.lineEditNewLogin = lineEditNewLogin
        self.lineEditNewPasswd = lineEditNewPasswd
        self.lineEditRepeatNewPasswd = lineEditRepeatNewPasswd
        self.frameEntry = frameEntry
        self.frameRegistration = frameRegistration
        self.frameConversation = frameConversation
        self.listViewContactList = listViewContactList
        self.contactListWiew = contactListWiew
        self.textBrowserReadMsg = textBrowserReadMsg
        self.MainWindow = MainWindow


    def __call__(self):
        try:
            requestRegistration = recording(self.lineEditNewLogin.text(), self.lineEditNewPasswd.text(), self.lineEditRepeatNewPasswd.text())
            if requestRegistration[0]:
                print(requestRegistration[1])
                self.MainWindow.resize(889, 589)
                self.frameRegistration.hide()
                self.frameConversation.show()
                try:
                    global reader, user
                    user = requestRegistration[2]
                    print("Добро пожаловать в Tequila, {}!".format(user.login))
                    print("geting contact list...")
                    GetContacts(self.listViewContactList, self.contactListWiew, self.textBrowserReadMsg)()
                    print("getting history...", PEER)
                    GetHistory(PEER, self.textBrowserReadMsg)()
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
        global PEER
        print('writing msg...', PEER)
        myChat = Conversation()
        myChat.connection()
        #json_msg_teg = json.dumps({'action': 'msg', 'mode': 'w'}).encode('utf-8')
        #myChat.writemsg(json_msg_teg)
        #addressee = '1'
        addressee = PEER
        myChat.connection()
        msg = JimMessage(user.tokin, addressee, msg)
        data = msg.jsonmsg()
        myChat.writemsg(data)


class Reader(Thread):
    def __init__(self, user, textBrowserReadMsg):
        Thread.__init__(self)
        self.textBrowserReadMsg = textBrowserReadMsg
        self.user = user
        self.peer_login = PEER
        self.continueFlag = True
        self.myChat = Conversation()


    def __call__(self):
        try:
            self.start()

        except:
            print('Не удалось получить сообщение')


    def run(self):

        print('listening for updates...', PEER)
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
                    self.textBrowserReadMsg.append('{} \n{:>150} \n{:>150}\n'.format(msg['message'], msg['from'], msg['time']))
        else:
            print('Не удалось получить сообщение')


    def stop(self):
        self.continueFlag = False
        print('Конец сессии.')
        self.join()


class GetContacts:
    def __init__(self, listViewContactList, contactListWiew, textBrowserReadMsg):
        self.listViewContactList = listViewContactList
        self.contactListWiew = contactListWiew
        self.textBrowserReadMsg = textBrowserReadMsg


    def __call__(self):
        try:
            global user
            self.contanctList = get_contact_list(user)
            if self.contanctList[0]:
                try:
                    user = self.contanctList[2]
                    self.contactListWiew = QStandardItemModel(self.listViewContactList)
                    for contact in user.contactList:
                        item = QStandardItem(contact[0])
                        self.contactListWiew.appendRow(item)
                        self.listViewContactList.setModel(self.contactListWiew)
                        #self.contactListWiew().selectionChanged.connect(change_peer)
                        #self.contactListWiew.selectionChanged.connect(change_peer)
                        contactListWiew().selectionChanged.connect(change_peer)

                    #self.textBrowserReadMsg.append(str(user.contactList))
                except:
                    print('Ошибка при выводе контактов')
            else:
                print(self.contanctList[1])
        except:
            print('Ошибка при выводе списка контактов')



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
    def __init__(self, frameConversation, textBrowserReadMsg, frameEntry, MainWindow):
        self.frameConversation = frameConversation
        self.textBrowserReadMsg = textBrowserReadMsg
        self.frameEntry = frameEntry
        self.MainWindow = MainWindow


    def __call__(self):
        self.textBrowserReadMsg.clear()
        reader.stop()
        self.MainWindow.resize(290, 589)
        self.frameConversation.hide()
        self.frameEntry.show()


class AddContact:
    def __init__(self, plainTextEditNewContact, listViewContactList, contactListWiew, textBrowserReadMsg):
        self.plainTextEditNewContact = plainTextEditNewContact
        self.listViewContactList = listViewContactList
        self.contactListWiew = contactListWiew
        self.textBrowserReadMsg = textBrowserReadMsg

    def __call__(self):
        try:
            global user
            add_contact(user, self.plainTextEditNewContact.toPlainText())
            self.plainTextEditNewContact.clear()
            GetContacts(self.listViewContactList, self.contactListWiew, self.textBrowserReadMsg)()
        except:
            print('Ошибка при добавлении контактов')


class GetHistory:
    def __init__(self, peer, textBrowserReadMsg):
        self.textBrowserReadMsg = textBrowserReadMsg
        self.peer = peer


    def __call__(self):
        try:
            global user
            self.messeges = get_history(user, self.peer)
            if self.messeges[0]:
                try:

                    user = self.messeges[2]
                    for msg in user.history:
                        #print(msg)
                        #self.textBrowserReadMsg.append('{} \n{:>150} \n{:>150}\n'.format(msg['message'], str(msg['from']), msg['time']))
                        self.textBrowserReadMsg.append(str(msg))
                except:
                    print('Ошибка при выводе истории')
            else:
                print(self.messeges[1])
        except:
            print('Ошибка при получении истории')


def change_peer(s1):
    print("!!!!!!!!!!!")
    print(s1.indexes()[0].data())
    global PEER
    PEER = s1.indexes()[0].data()


if __name__ == '__main__':

    app = QtWidgets.QApplication(sys.argv)
    window = TkillaWindow()
    window.show()
    sys.exit(app.exec_())
