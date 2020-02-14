# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\Research\physics\workspace\mosi_app_mgtools\motion_analysis\GUI\layout\.\new_skeleton_dialog.ui',
# licensing of 'D:\Research\physics\workspace\mosi_app_mgtools\motion_analysis\GUI\layout\.\new_skeleton_dialog.ui' applies.
#
# Created: Wed Jan 15 17:42:09 2020
#      by: pyside2-uic  running on PySide2 5.13.1
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(320, 102)
        self.gridLayout = QtWidgets.QGridLayout(Dialog)
        self.gridLayout.setObjectName("gridLayout")
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
        self.gridLayout.addLayout(self.horizontalLayout, 0, 0, 1, 1)
        self.skeletonHorizontalLayout = QtWidgets.QHBoxLayout()
        self.skeletonHorizontalLayout.setObjectName("skeletonHorizontalLayout")
        self.loadBVHButton = QtWidgets.QPushButton(Dialog)
        self.loadBVHButton.setObjectName("loadBVHButton")
        self.skeletonHorizontalLayout.addWidget(self.loadBVHButton)
        self.loadASFButton = QtWidgets.QPushButton(Dialog)
        self.loadASFButton.setObjectName("loadASFButton")
        self.skeletonHorizontalLayout.addWidget(self.loadASFButton)
        self.loadSkeletonModelButton = QtWidgets.QPushButton(Dialog)
        self.loadSkeletonModelButton.setObjectName("loadSkeletonModelButton")
        self.skeletonHorizontalLayout.addWidget(self.loadSkeletonModelButton)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.skeletonHorizontalLayout.addItem(spacerItem1)
        self.gridLayout.addLayout(self.skeletonHorizontalLayout, 1, 0, 1, 1)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem2)
        self.acceptButton = QtWidgets.QPushButton(Dialog)
        self.acceptButton.setObjectName("acceptButton")
        self.horizontalLayout_2.addWidget(self.acceptButton)
        self.rejectButton = QtWidgets.QPushButton(Dialog)
        self.rejectButton.setObjectName("rejectButton")
        self.horizontalLayout_2.addWidget(self.rejectButton)
        self.gridLayout.addLayout(self.horizontalLayout_2, 2, 0, 1, 1)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtWidgets.QApplication.translate("Dialog", "Enter Name", None, -1))
        self.label.setText(QtWidgets.QApplication.translate("Dialog", "Name", None, -1))
        self.loadBVHButton.setText(QtWidgets.QApplication.translate("Dialog", "Load BVH File", None, -1))
        self.loadASFButton.setText(QtWidgets.QApplication.translate("Dialog", "Load ASF File", None, -1))
        self.loadSkeletonModelButton.setText(QtWidgets.QApplication.translate("Dialog", "Load Model", None, -1))
        self.acceptButton.setText(QtWidgets.QApplication.translate("Dialog", "Accept", None, -1))
        self.rejectButton.setText(QtWidgets.QApplication.translate("Dialog", "Cancel", None, -1))

