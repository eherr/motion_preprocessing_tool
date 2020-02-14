# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\Research\physics\workspace\mosi_app_mgtools\motion_analysis\GUI\layout\.\upload_motion_dialog.ui',
# licensing of 'D:\Research\physics\workspace\mosi_app_mgtools\motion_analysis\GUI\layout\.\upload_motion_dialog.ui' applies.
#
# Created: Wed Jan 15 17:42:12 2020
#      by: pyside2-uic  running on PySide2 5.13.1
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(363, 288)
        self.verticalLayout = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setObjectName("label")
        self.horizontalLayout_7.addWidget(self.label)
        self.urlLineEdit = QtWidgets.QLineEdit(Dialog)
        self.urlLineEdit.setObjectName("urlLineEdit")
        self.horizontalLayout_7.addWidget(self.urlLineEdit)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_7.addItem(spacerItem)
        self.verticalLayout.addLayout(self.horizontalLayout_7)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout.addWidget(self.label_2)
        self.skeletonModelComboBox = QtWidgets.QComboBox(Dialog)
        self.skeletonModelComboBox.setObjectName("skeletonModelComboBox")
        self.horizontalLayout.addWidget(self.skeletonModelComboBox)
        self.newSkeletonButton = QtWidgets.QPushButton(Dialog)
        self.newSkeletonButton.setObjectName("newSkeletonButton")
        self.horizontalLayout.addWidget(self.newSkeletonButton)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.isProcessedCheckBox = QtWidgets.QCheckBox(Dialog)
        self.isProcessedCheckBox.setObjectName("isProcessedCheckBox")
        self.horizontalLayout_3.addWidget(self.isProcessedCheckBox)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem1)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.collectionTreeWidget = QtWidgets.QTreeWidget(Dialog)
        self.collectionTreeWidget.setObjectName("collectionTreeWidget")
        self.verticalLayout.addWidget(self.collectionTreeWidget)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem2)
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
        Dialog.setWindowTitle(QtWidgets.QApplication.translate("Dialog", "Upload Motion", None, -1))
        self.label.setText(QtWidgets.QApplication.translate("Dialog", "URL", None, -1))
        self.label_2.setText(QtWidgets.QApplication.translate("Dialog", "Skeleton Model", None, -1))
        self.newSkeletonButton.setText(QtWidgets.QApplication.translate("Dialog", "New Skeleton", None, -1))
        self.isProcessedCheckBox.setText(QtWidgets.QApplication.translate("Dialog", "Is Processed", None, -1))
        self.collectionTreeWidget.headerItem().setText(0, QtWidgets.QApplication.translate("Dialog", "Name", None, -1))
        self.collectionTreeWidget.headerItem().setText(1, QtWidgets.QApplication.translate("Dialog", "Type", None, -1))
        self.selectButton.setText(QtWidgets.QApplication.translate("Dialog", "Select", None, -1))
        self.cancelButton.setText(QtWidgets.QApplication.translate("Dialog", "Cancel", None, -1))

