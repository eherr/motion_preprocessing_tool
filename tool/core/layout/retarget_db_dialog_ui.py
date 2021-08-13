# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\Research\physics\workspace\mosi_app_mgtools\motion_analysis\GUI\layout\.\retarget_db_dialog.ui',
# licensing of 'D:\Research\physics\workspace\mosi_app_mgtools\motion_analysis\GUI\layout\.\retarget_db_dialog.ui' applies.
#
# Created: Wed Jan 15 17:42:10 2020
#      by: pyside2-uic  running on PySide2 5.13.1
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(603, 447)
        self.verticalLayout = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_3.addWidget(self.label_2)
        self.sourceModelComboBox = QtWidgets.QComboBox(Dialog)
        self.sourceModelComboBox.setObjectName("sourceModelComboBox")
        self.horizontalLayout_3.addWidget(self.sourceModelComboBox)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label_3 = QtWidgets.QLabel(Dialog)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_4.addWidget(self.label_3)
        self.targetModelComboBox = QtWidgets.QComboBox(Dialog)
        self.targetModelComboBox.setObjectName("targetModelComboBox")
        self.horizontalLayout_4.addWidget(self.targetModelComboBox)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem1)
        self.verticalLayout.addLayout(self.horizontalLayout_4)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.scaleLineEdit = QtWidgets.QLineEdit(Dialog)
        self.scaleLineEdit.setMaximumSize(QtCore.QSize(40, 16777215))
        self.scaleLineEdit.setObjectName("scaleLineEdit")
        self.horizontalLayout.addWidget(self.scaleLineEdit)
        self.placeOnGroundRadioButton = QtWidgets.QRadioButton(Dialog)
        self.placeOnGroundRadioButton.setObjectName("placeOnGroundRadioButton")
        self.horizontalLayout.addWidget(self.placeOnGroundRadioButton)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem2)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.label_4 = QtWidgets.QLabel(Dialog)
        self.label_4.setObjectName("label_4")
        self.verticalLayout.addWidget(self.label_4)
        self.collectionTreeWidget = QtWidgets.QTreeWidget(Dialog)
        self.collectionTreeWidget.setObjectName("collectionTreeWidget")
        self.verticalLayout.addWidget(self.collectionTreeWidget)
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
        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtWidgets.QApplication.translate("Dialog", "Retarget Motion", None, -1))
        self.label_2.setText(QtWidgets.QApplication.translate("Dialog", "Source skeleton", None, -1))
        self.label_3.setText(QtWidgets.QApplication.translate("Dialog", "Target skeleton", None, -1))
        self.label.setText(QtWidgets.QApplication.translate("Dialog", "Scale", None, -1))
        self.scaleLineEdit.setText(QtWidgets.QApplication.translate("Dialog", "1", None, -1))
        self.placeOnGroundRadioButton.setText(QtWidgets.QApplication.translate("Dialog", "Place On Ground", None, -1))
        self.label_4.setText(QtWidgets.QApplication.translate("Dialog", "Select Destination", None, -1))
        self.collectionTreeWidget.headerItem().setText(0, QtWidgets.QApplication.translate("Dialog", "Name", None, -1))
        self.collectionTreeWidget.headerItem().setText(1, QtWidgets.QApplication.translate("Dialog", "Type", None, -1))
        self.selectButton.setText(QtWidgets.QApplication.translate("Dialog", "Select", None, -1))
        self.cancelButton.setText(QtWidgets.QApplication.translate("Dialog", "Cancel", None, -1))

