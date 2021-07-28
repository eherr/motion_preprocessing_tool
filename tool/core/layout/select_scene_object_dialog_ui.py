# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\Research\physics\workspace\mosi_app_mgtools\motion_analysis\GUI\layout\.\select_scene_object_dialog.ui',
# licensing of 'D:\Research\physics\workspace\mosi_app_mgtools\motion_analysis\GUI\layout\.\select_scene_object_dialog.ui' applies.
#
# Created: Wed Jan 15 17:42:11 2020
#      by: pyside2-uic  running on PySide2 5.13.1
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(412, 353)
        self.verticalLayout = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.sceneObjectListWidget = QtWidgets.QListWidget(Dialog)
        self.sceneObjectListWidget.setObjectName("sceneObjectListWidget")
        self.verticalLayout.addWidget(self.sceneObjectListWidget)
        self.settingsVerticalLayout = QtWidgets.QVBoxLayout()
        self.settingsVerticalLayout.setObjectName("settingsVerticalLayout")
        self.verticalLayout.addLayout(self.settingsVerticalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.selectButton = QtWidgets.QPushButton(Dialog)
        self.selectButton.setObjectName("selectButton")
        self.horizontalLayout_2.addWidget(self.selectButton)
        self.cancelButton = QtWidgets.QPushButton(Dialog)
        self.cancelButton.setObjectName("cancelButton")
        self.horizontalLayout_2.addWidget(self.cancelButton)
        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtWidgets.QApplication.translate("Dialog", "Select scene object", None, -1))
        self.selectButton.setText(QtWidgets.QApplication.translate("Dialog", "Select", None, -1))
        self.cancelButton.setText(QtWidgets.QApplication.translate("Dialog", "Cancel", None, -1))

