# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'tkilla.ui'
#
# Created by: PyQt5 UI code generator 5.9
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(877, 598)
        MainWindow.setAutoFillBackground(True)
        MainWindow.setStyleSheet("")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.frameEntry = QtWidgets.QFrame(self.centralwidget)
        self.frameEntry.setGeometry(QtCore.QRect(270, 250, 331, 51))
        self.frameEntry.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frameEntry.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frameEntry.setObjectName("frameEntry")
        self.pushButtonAuthentification = QtWidgets.QPushButton(self.frameEntry)
        self.pushButtonAuthentification.setGeometry(QtCore.QRect(200, 10, 110, 31))
        self.pushButtonAuthentification.setObjectName("pushButtonAuthentification")
        self.pushButtonRegistration = QtWidgets.QPushButton(self.frameEntry)
        self.pushButtonRegistration.setEnabled(True)
        self.pushButtonRegistration.setGeometry(QtCore.QRect(20, 10, 110, 31))
        self.pushButtonRegistration.setObjectName("pushButtonRegistration")
        self.frameAuthentification = QtWidgets.QFrame(self.centralwidget)
        self.frameAuthentification.setEnabled(True)
        self.frameAuthentification.setGeometry(QtCore.QRect(340, 120, 211, 321))
        self.frameAuthentification.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frameAuthentification.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frameAuthentification.setObjectName("frameAuthentification")
        self.pushButtonAuthentificationOk = QtWidgets.QPushButton(self.frameAuthentification)
        self.pushButtonAuthentificationOk.setGeometry(QtCore.QRect(50, 230, 111, 50))
        self.pushButtonAuthentificationOk.setObjectName("pushButtonAuthentificationOk")
        self.lineEditLogin = QtWidgets.QLineEdit(self.frameAuthentification)
        self.lineEditLogin.setGeometry(QtCore.QRect(20, 60, 171, 21))
        self.lineEditLogin.setInputMask("")
        self.lineEditLogin.setText("")
        self.lineEditLogin.setObjectName("lineEditLogin")
        self.lineEditPasswd = QtWidgets.QLineEdit(self.frameAuthentification)
        self.lineEditPasswd.setGeometry(QtCore.QRect(20, 120, 171, 21))
        self.lineEditPasswd.setText("")
        self.lineEditPasswd.setObjectName("lineEditPasswd")
        self.labelLogin = QtWidgets.QLabel(self.frameAuthentification)
        self.labelLogin.setGeometry(QtCore.QRect(20, 30, 47, 13))
        self.labelLogin.setObjectName("labelLogin")
        self.labelPasswd = QtWidgets.QLabel(self.frameAuthentification)
        self.labelPasswd.setGeometry(QtCore.QRect(20, 100, 47, 13))
        self.labelPasswd.setObjectName("labelPasswd")
        self.frameRegistration = QtWidgets.QFrame(self.centralwidget)
        self.frameRegistration.setEnabled(True)
        self.frameRegistration.setGeometry(QtCore.QRect(340, 120, 231, 291))
        self.frameRegistration.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frameRegistration.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frameRegistration.setObjectName("frameRegistration")
        self.lineEditNewLogin = QtWidgets.QLineEdit(self.frameRegistration)
        self.lineEditNewLogin.setGeometry(QtCore.QRect(20, 60, 171, 21))
        self.lineEditNewLogin.setInputMask("")
        self.lineEditNewLogin.setText("")
        self.lineEditNewLogin.setObjectName("lineEditNewLogin")
        self.lineEditNewPasswd = QtWidgets.QLineEdit(self.frameRegistration)
        self.lineEditNewPasswd.setGeometry(QtCore.QRect(20, 120, 171, 21))
        self.lineEditNewPasswd.setText("")
        self.lineEditNewPasswd.setObjectName("lineEditNewPasswd")
        self.labelNewLogin = QtWidgets.QLabel(self.frameRegistration)
        self.labelNewLogin.setGeometry(QtCore.QRect(20, 30, 47, 13))
        self.labelNewLogin.setObjectName("labelNewLogin")
        self.labelNewPasswd = QtWidgets.QLabel(self.frameRegistration)
        self.labelNewPasswd.setGeometry(QtCore.QRect(20, 100, 47, 13))
        self.labelNewPasswd.setObjectName("labelNewPasswd")
        self.pushButtonRegistrationOk = QtWidgets.QPushButton(self.frameRegistration)
        self.pushButtonRegistrationOk.setGeometry(QtCore.QRect(50, 230, 111, 50))
        self.pushButtonRegistrationOk.setObjectName("pushButtonRegistrationOk")
        self.lineEditRepeatNewPasswd = QtWidgets.QLineEdit(self.frameRegistration)
        self.lineEditRepeatNewPasswd.setGeometry(QtCore.QRect(20, 180, 171, 21))
        self.lineEditRepeatNewPasswd.setText("")
        self.lineEditRepeatNewPasswd.setObjectName("lineEditRepeatNewPasswd")
        self.labelRepeatNewPasswd = QtWidgets.QLabel(self.frameRegistration)
        self.labelRepeatNewPasswd.setGeometry(QtCore.QRect(20, 160, 91, 16))
        self.labelRepeatNewPasswd.setObjectName("labelRepeatNewPasswd")
        self.frameConversation = QtWidgets.QFrame(self.centralwidget)
        self.frameConversation.setGeometry(QtCore.QRect(280, 10, 581, 541))
        self.frameConversation.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frameConversation.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frameConversation.setObjectName("frameConversation")
        self.textBrowserReadMsg = QtWidgets.QTextBrowser(self.frameConversation)
        self.textBrowserReadMsg.setGeometry(QtCore.QRect(10, 10, 551, 431))
        self.textBrowserReadMsg.setObjectName("textBrowserReadMsg")
        self.plainTextEditWriteMsg = QtWidgets.QPlainTextEdit(self.frameConversation)
        self.plainTextEditWriteMsg.setGeometry(QtCore.QRect(10, 450, 551, 41))
        self.plainTextEditWriteMsg.setObjectName("plainTextEditWriteMsg")
        self.pushButtonSendMsg = QtWidgets.QPushButton(self.frameConversation)
        self.pushButtonSendMsg.setGeometry(QtCore.QRect(450, 500, 111, 31))
        self.pushButtonSendMsg.setObjectName("pushButtonSendMsg")
        self.pushButtonLogout = QtWidgets.QPushButton(self.frameConversation)
        self.pushButtonLogout.setGeometry(QtCore.QRect(10, 500, 111, 31))
        self.pushButtonLogout.setObjectName("pushButtonLogout")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 877, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        #self.pushButtonRegistration.clicked.connect(self.frameEntry.hide)
        #self.pushButtonRegistrationOk.clicked.connect(self.frameAuthentification.show)
        #self.pushButtonRegistration.clicked.connect(self.frameRegistration.show)
        #self.pushButtonRegistrationOk.clicked.connect(self.frameRegistration.hide)
        #self.pushButtonRegistration.clicked.connect(self.lineEditNewLogin.clear)
        #self.pushButtonRegistration.clicked.connect(self.lineEditNewPasswd.clear)
        #self.pushButtonAuthentification.clicked.connect(self.frameEntry.hide)
        #self.pushButtonAuthentification.clicked.connect(self.frameAuthentification.show)
        #self.pushButtonAuthentificationOk.clicked.connect(self.frameAuthentification.hide)
        #self.pushButtonAuthentification.clicked.connect(self.lineEditLogin.clear)
        #self.pushButtonAuthentificationOk.clicked.connect(self.frameConversation.show)
        #pushButtonLogout.clicked.connect(self.frameConversation.hide)
        #self.pushButtonLogout.clicked.connect(self.frameEntry.show)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButtonAuthentification.setText(_translate("MainWindow", "Authentification"))
        self.pushButtonRegistration.setText(_translate("MainWindow", "Registration"))
        self.pushButtonAuthentificationOk.setText(_translate("MainWindow", "Ок"))
        self.pushButtonAuthentificationOk.setShortcut(_translate("MainWindow", "Return"))
        self.labelLogin.setText(_translate("MainWindow", "Login"))
        self.labelPasswd.setText(_translate("MainWindow", "Password"))
        self.labelNewLogin.setText(_translate("MainWindow", "Login"))
        self.labelNewPasswd.setText(_translate("MainWindow", "Password"))
        self.pushButtonRegistrationOk.setText(_translate("MainWindow", "Ок"))
        self.pushButtonRegistrationOk.setShortcut(_translate("MainWindow", "Return"))
        self.labelRepeatNewPasswd.setText(_translate("MainWindow", "Repeat password"))
        self.pushButtonSendMsg.setText(_translate("MainWindow", "Send"))
        self.pushButtonLogout.setText(_translate("MainWindow", "Log out"))

