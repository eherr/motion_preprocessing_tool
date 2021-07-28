# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\Research\physics\workspace\mosi_app_mgtools\motion_analysis\GUI\layout\.\copy_motion_dialog.ui',
# licensing of 'D:\Research\physics\workspace\mosi_app_mgtools\motion_analysis\GUI\layout\.\copy_motion_dialog.ui' applies.
#
# Created: Wed Jan 15 17:42:05 2020
#      by: pyside2-uic  running on PySide2 5.13.1
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(446, 140)
        self.gridLayout = QtWidgets.QGridLayout(Dialog)
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.nameLineEdit = QtWidgets.QLineEdit(Dialog)
        self.nameLineEdit.setObjectName("nameLineEdit")
        self.horizontalLayout.addWidget(self.nameLineEdit)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_3.addWidget(self.label_2)
        self.startFrameSlider = QtWidgets.QSlider(Dialog)
        self.startFrameSlider.setOrientation(QtCore.Qt.Horizontal)
        self.startFrameSlider.setObjectName("startFrameSlider")
        self.horizontalLayout_3.addWidget(self.startFrameSlider)
        self.startFrameSpinBox = QtWidgets.QSpinBox(Dialog)
        self.startFrameSpinBox.setObjectName("startFrameSpinBox")
        self.horizontalLayout_3.addWidget(self.startFrameSpinBox)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem1)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label_3 = QtWidgets.QLabel(Dialog)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_4.addWidget(self.label_3)
        self.endFrameSlider = QtWidgets.QSlider(Dialog)
        self.endFrameSlider.setOrientation(QtCore.Qt.Horizontal)
        self.endFrameSlider.setObjectName("endFrameSlider")
        self.horizontalLayout_4.addWidget(self.endFrameSlider)
        self.endFrameSpinBox = QtWidgets.QSpinBox(Dialog)
        self.endFrameSpinBox.setObjectName("endFrameSpinBox")
        self.horizontalLayout_4.addWidget(self.endFrameSpinBox)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem2)
        self.verticalLayout.addLayout(self.horizontalLayout_4)
        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem3)
        self.selectButton = QtWidgets.QPushButton(Dialog)
        self.selectButton.setObjectName("selectButton")
        self.horizontalLayout_2.addWidget(self.selectButton)
        self.cancelButton = QtWidgets.QPushButton(Dialog)
        self.cancelButton.setObjectName("cancelButton")
        self.horizontalLayout_2.addWidget(self.cancelButton)
        self.gridLayout.addLayout(self.horizontalLayout_2, 1, 0, 1, 1)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtWidgets.QApplication.translate("Dialog", "Select scene object", None, -1))
        self.label.setText(QtWidgets.QApplication.translate("Dialog", "Name", None, -1))
        self.label_2.setText(QtWidgets.QApplication.translate("Dialog", "start", None, -1))
        self.label_3.setText(QtWidgets.QApplication.translate("Dialog", "end", None, -1))
        self.selectButton.setText(QtWidgets.QApplication.translate("Dialog", "Accept", None, -1))
        self.cancelButton.setText(QtWidgets.QApplication.translate("Dialog", "Cancel", None, -1))

