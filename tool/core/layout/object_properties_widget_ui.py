# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\Research\physics\workspace\mosi_app_mgtools\motion_analysis\GUI\layout\.\object_properties_widget.ui',
# licensing of 'D:\Research\physics\workspace\mosi_app_mgtools\motion_analysis\GUI\layout\.\object_properties_widget.ui' applies.
#
# Created: Wed Jan 15 17:42:10 2020
#      by: pyside2-uic  running on PySide2 5.13.1
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(381, 157)
        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_5 = QtWidgets.QLabel(Form)
        self.label_5.setObjectName("label_5")
        self.horizontalLayout_2.addWidget(self.label_5)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.nameLineEdit = QtWidgets.QLineEdit(Form)
        self.nameLineEdit.setObjectName("nameLineEdit")
        self.horizontalLayout_2.addWidget(self.nameLineEdit)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(Form)
        self.label.setMaximumSize(QtCore.QSize(80, 16777215))
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout.addWidget(self.label_2)
        self.posXLineEdit = QtWidgets.QLineEdit(Form)
        self.posXLineEdit.setMaximumSize(QtCore.QSize(80, 16777215))
        self.posXLineEdit.setObjectName("posXLineEdit")
        self.horizontalLayout.addWidget(self.posXLineEdit)
        self.label_3 = QtWidgets.QLabel(Form)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout.addWidget(self.label_3)
        self.posYLineEdit = QtWidgets.QLineEdit(Form)
        self.posYLineEdit.setMaximumSize(QtCore.QSize(80, 16777215))
        self.posYLineEdit.setObjectName("posYLineEdit")
        self.horizontalLayout.addWidget(self.posYLineEdit)
        self.label_4 = QtWidgets.QLabel(Form)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout.addWidget(self.label_4)
        self.posZLineEdit = QtWidgets.QLineEdit(Form)
        self.posZLineEdit.setMaximumSize(QtCore.QSize(80, 16777215))
        self.posZLineEdit.setObjectName("posZLineEdit")
        self.horizontalLayout.addWidget(self.posZLineEdit)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label_6 = QtWidgets.QLabel(Form)
        self.label_6.setObjectName("label_6")
        self.horizontalLayout_4.addWidget(self.label_6)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem2)
        self.scaleLineEdit = QtWidgets.QLineEdit(Form)
        self.scaleLineEdit.setObjectName("scaleLineEdit")
        self.horizontalLayout_4.addWidget(self.scaleLineEdit)
        self.verticalLayout.addLayout(self.horizontalLayout_4)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.updateButton = QtWidgets.QToolButton(Form)
        self.updateButton.setObjectName("updateButton")
        self.horizontalLayout_3.addWidget(self.updateButton)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem3)
        self.verticalLayout.addLayout(self.horizontalLayout_3)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QtWidgets.QApplication.translate("Form", "Form", None, -1))
        self.label_5.setText(QtWidgets.QApplication.translate("Form", "Name", None, -1))
        self.label.setText(QtWidgets.QApplication.translate("Form", "Position", None, -1))
        self.label_2.setText(QtWidgets.QApplication.translate("Form", "X", None, -1))
        self.label_3.setText(QtWidgets.QApplication.translate("Form", "Y", None, -1))
        self.label_4.setText(QtWidgets.QApplication.translate("Form", "Z", None, -1))
        self.label_6.setText(QtWidgets.QApplication.translate("Form", "Scale", None, -1))
        self.updateButton.setText(QtWidgets.QApplication.translate("Form", "Update", None, -1))

