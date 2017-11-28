import sys
from PyQt5 import QtWidgets
import scheme_gui_client
from run_tkilla_client import recording, log_in

class InitialUi_MainWindow(scheme_gui_client.Ui_MainWindow):
    def setupUi(self, MainWindow):
        scheme_gui_client.Ui_MainWindow.setupUi(self, MainWindow)
        self.pushButtonRegistration.clicked.connect(self.frameRegistration.raise_)
        self.pushButtonRegistrationOk.clicked.connect(self.frameEntry.raise_)
        self.pushButtonAuthentificationOk.clicked.connect(self.frameEntry.raise_)
        self.pushButtonAuthentificationOk.clicked.connect(self.frameConversation.raise_)
        self.pushButtonLogout.clicked.connect(self.frameEntry.raise_)
        self.frameRegistration.hide()
        self.frameAuthentification.hide()
        self.frameConversation.hide()


class TkillaWindow(QtWidgets.QMainWindow):
    def __init__(self, reg, auth, creg, cauth):
        QtWidgets.QWidget.__init__(self)
        self.ui = InitialUi_MainWindow()
        self.ui.setupUi(self)
        self.ui.pushButtonRegistration.clicked.connect(reg())
        self.ui.pushButtonAuthentification.clicked.connect(auth())
        self.ui.pushButtonRegistrationOk.clicked.connect(creg(self.ui.lineEditNewLogin, self.ui.lineEditNewPasswd, self.ui.lineEditRepeatNewPasswd))
        self.ui.pushButtonAuthentificationOk.clicked.connect(cauth(self.ui.lineEditLogin, self.ui.lineEditPasswd))


class CheckAuth:
    def __init__(self, lineEditLogin, lineEditPasswd):
        self.lineEditLogin = lineEditLogin
        self.lineEditPasswd = lineEditPasswd

    def __call__(self):
        try:
            log_in(self.lineEditLogin.text(), self.lineEditPasswd.text())
        except:
            print("Ошибка авторизации на стороне клиента")
        self.lineEditLogin.clear()
        self.lineEditPasswd.clear()


class CheckReg:
    def __init__(self, lineEditNewLogin, lineEditNewPasswd, lineEditRepeatNewPasswd):
        self.lineEditNewLogin = lineEditNewLogin
        self.lineEditNewPasswd = lineEditNewPasswd
        self.lineEditRepeatNewPasswd = lineEditRepeatNewPasswd

    def __call__(self):
        print(self.lineEditNewLogin.text(), self.lineEditNewPasswd.text(), self.lineEditRepeatNewPasswd.text())
        try:
            recording(self.lineEditNewLogin.text(), self.lineEditNewPasswd.text(), self.lineEditRepeatNewPasswd.text())
            print('Пользователь с логином {} прошел регистрацию'.format(self.lineEditNewLogin.text()))
        except:
            print("Ошибка регистрации на стороне клиента")
        self.lineEditNewLogin.clear()
        self.lineEditNewPasswd.clear()
        self.lineEditRepeatNewPasswd.clear()


class Auth:
    def __call__(self):
        print("Авторизация")


class Reg:
    def __call__(self):
        print("Регистрация")

if __name__ == '__main__':

    reg = Reg
    auth = Auth
    creg = CheckReg
    cauth = CheckAuth
    app = QtWidgets.QApplication(sys.argv)
    window = TkillaWindow(reg, auth, creg, cauth)
    window.show()
    sys.exit(app.exec_())
