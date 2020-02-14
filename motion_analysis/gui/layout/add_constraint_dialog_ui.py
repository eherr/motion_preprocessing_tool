# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\Research\physics\workspace\mosi_app_mgtools\motion_analysis\GUI\layout\.\add_constraint_dialog.ui',
# licensing of 'D:\Research\physics\workspace\mosi_app_mgtools\motion_analysis\GUI\layout\.\add_constraint_dialog.ui' applies.
#
# Created: Wed Jan 15 17:42:03 2020
#      by: pyside2-uic  running on PySide2 5.13.1
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(393, 84)
        self.gridLayout = QtWidgets.QGridLayout(Dialog)
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setMaximumSize(QtCore.QSize(40, 16777215))
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.jointComboBox = QtWidgets.QComboBox(Dialog)
        self.jointComboBox.setObjectName("jointComboBox")
        self.horizontalLayout.addWidget(self.jointComboBox)
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout.addWidget(self.label_2)
        self.annotationComboBox = QtWidgets.QComboBox(Dialog)
        self.annotationComboBox.setObjectName("annotationComboBox")
        self.horizontalLayout.addWidget(self.annotationComboBox)
        self.setConstraintButton = QtWidgets.QPushButton(Dialog)
        self.setConstraintButton.setObjectName("setConstraintButton")
        self.horizontalLayout.addWidget(self.setConstraintButton)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.verticalLayout_2.addLayout(self.verticalLayout)
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
        Dialog.setWindowTitle(QtWidgets.QApplication.translate("Dialog", "Add Constraint", None, -1))
        self.label.setText(QtWidgets.QApplication.translate("Dialog", "Joint", None, -1))
        self.label_2.setText(QtWidgets.QApplication.translate("Dialog", "Annotation", None, -1))
        self.setConstraintButton.setText(QtWidgets.QApplication.translate("Dialog", "Select Constraint Object", None, -1))
        self.acceptButton.setText(QtWidgets.QApplication.translate("Dialog", "OK", None, -1))
        self.rejectButton.setText(QtWidgets.QApplication.translate("Dialog", "Cancel", None, -1))

