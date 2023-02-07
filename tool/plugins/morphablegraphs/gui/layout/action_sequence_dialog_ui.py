# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\Research\physics\workspace\mosi_app_mgtools\tool\GUI\layout\.\action_sequence_dialog.ui',
# licensing of 'D:\Research\physics\workspace\mosi_app_mgtools\tool\GUI\layout\.\action_sequence_dialog.ui' applies.
#
# Created: Wed Jan 15 17:42:02 2020
#      by: pyside2-uic  running on PySide2 5.13.1
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(436, 297)
        self.gridLayout = QtWidgets.QGridLayout(Dialog)
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_3.addWidget(self.label_2)
        self.setStartNodeButton = QtWidgets.QPushButton(Dialog)
        self.setStartNodeButton.setObjectName("setStartNodeButton")
        self.horizontalLayout_3.addWidget(self.setStartNodeButton)
        self.verticalLayout_2.addLayout(self.horizontalLayout_3)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.actionComboBox = QtWidgets.QComboBox(Dialog)
        self.actionComboBox.setObjectName("actionComboBox")
        self.horizontalLayout.addWidget(self.actionComboBox)
        self.addButton = QtWidgets.QPushButton(Dialog)
        self.addButton.setObjectName("addButton")
        self.horizontalLayout.addWidget(self.addButton)
        self.clearButton = QtWidgets.QPushButton(Dialog)
        self.clearButton.setObjectName("clearButton")
        self.horizontalLayout.addWidget(self.clearButton)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.verticalLayout_2.addLayout(self.verticalLayout)
        self.actionTableWidget = QtWidgets.QTableWidget(Dialog)
        self.actionTableWidget.setColumnCount(2)
        self.actionTableWidget.setObjectName("actionTableWidget")
        self.actionTableWidget.setColumnCount(2)
        self.actionTableWidget.setRowCount(0)
        self.verticalLayout_2.addWidget(self.actionTableWidget)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.acceptButton = QtWidgets.QPushButton(Dialog)
        self.acceptButton.setObjectName("acceptButton")
        self.horizontalLayout_2.addWidget(self.acceptButton)
        self.rejectButton = QtWidgets.QPushButton(Dialog)
        self.rejectButton.setObjectName("rejectButton")
        self.horizontalLayout_2.addWidget(self.rejectButton)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        self.gridLayout.addLayout(self.verticalLayout_2, 0, 0, 1, 1)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtWidgets.QApplication.translate("Dialog", "Set Action Sequence", None, -1))
        self.label_2.setText(QtWidgets.QApplication.translate("Dialog", "Select Start Node", None, -1))
        self.setStartNodeButton.setText(QtWidgets.QApplication.translate("Dialog", "Set", None, -1))
        self.label.setText(QtWidgets.QApplication.translate("Dialog", "Action", None, -1))
        self.addButton.setText(QtWidgets.QApplication.translate("Dialog", "Add", None, -1))
        self.clearButton.setText(QtWidgets.QApplication.translate("Dialog", "Clear", None, -1))
        self.acceptButton.setText(QtWidgets.QApplication.translate("Dialog", "OK", None, -1))
        self.rejectButton.setText(QtWidgets.QApplication.translate("Dialog", "Cancel", None, -1))

