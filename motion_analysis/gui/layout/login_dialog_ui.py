# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\Research\physics\workspace\mosi_app_mgtools\motion_analysis\GUI\layout\.\login_dialog.ui',
# licensing of 'D:\Research\physics\workspace\mosi_app_mgtools\motion_analysis\GUI\layout\.\login_dialog.ui' applies.
#
# Created: Wed Jan 15 17:42:07 2020
#      by: pyside2-uic  running on PySide2 5.13.1
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_LoginDialog(object):
    def setupUi(self, LoginDialog):
        LoginDialog.setObjectName("LoginDialog")
        LoginDialog.resize(340, 102)
        self.verticalLayout = QtWidgets.QVBoxLayout(LoginDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(LoginDialog)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.userLineEdit = QtWidgets.QLineEdit(LoginDialog)
        self.userLineEdit.setObjectName("userLineEdit")
        self.horizontalLayout.addWidget(self.userLineEdit)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label_3 = QtWidgets.QLabel(LoginDialog)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_4.addWidget(self.label_3)
        self.passwordLineEdit = QtWidgets.QLineEdit(LoginDialog)
        self.passwordLineEdit.setEchoMode(QtWidgets.QLineEdit.Password)
        self.passwordLineEdit.setObjectName("passwordLineEdit")
        self.horizontalLayout_4.addWidget(self.passwordLineEdit)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem1)
        self.verticalLayout.addLayout(self.horizontalLayout_4)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem2)
        self.acceptButton = QtWidgets.QPushButton(LoginDialog)
        self.acceptButton.setObjectName("acceptButton")
        self.horizontalLayout_2.addWidget(self.acceptButton)
        self.rejectButton = QtWidgets.QPushButton(LoginDialog)
        self.rejectButton.setObjectName("rejectButton")
        self.horizontalLayout_2.addWidget(self.rejectButton)
        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.retranslateUi(LoginDialog)
        QtCore.QMetaObject.connectSlotsByName(LoginDialog)

    def retranslateUi(self, LoginDialog):
        LoginDialog.setWindowTitle(QtWidgets.QApplication.translate("LoginDialog", "Login", None, -1))
        self.label.setText(QtWidgets.QApplication.translate("LoginDialog", "User", None, -1))
        self.label_3.setText(QtWidgets.QApplication.translate("LoginDialog", "Password", None, -1))
        self.acceptButton.setText(QtWidgets.QApplication.translate("LoginDialog", "Accept", None, -1))
        self.rejectButton.setText(QtWidgets.QApplication.translate("LoginDialog", "Cancel", None, -1))

