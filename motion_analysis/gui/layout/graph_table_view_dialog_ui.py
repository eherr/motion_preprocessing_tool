# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'graph_table_view_dialog.ui',
# licensing of 'graph_table_view_dialog.ui' applies.
#
# Created: Tue Feb 11 15:24:02 2020
#      by: pyside2-uic  running on PySide2 5.13.1
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(469, 355)
        self.verticalLayout = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_4.addWidget(self.label_2)
        self.skeletonListComboBox = QtWidgets.QComboBox(Dialog)
        self.skeletonListComboBox.setObjectName("skeletonListComboBox")
        self.horizontalLayout_4.addWidget(self.skeletonListComboBox)
        spacerItem = QtWidgets.QSpacerItem(128, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem)
        self.verticalLayout.addLayout(self.horizontalLayout_4)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.graphListWidget = QtWidgets.QListWidget(Dialog)
        self.graphListWidget.setObjectName("graphListWidget")
        self.verticalLayout.addWidget(self.graphListWidget)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.addButton = QtWidgets.QPushButton(Dialog)
        self.addButton.setObjectName("addButton")
        self.horizontalLayout_3.addWidget(self.addButton)
        self.copyButton = QtWidgets.QPushButton(Dialog)
        self.copyButton.setObjectName("copyButton")
        self.horizontalLayout_3.addWidget(self.copyButton)
        self.editButton = QtWidgets.QPushButton(Dialog)
        self.editButton.setObjectName("editButton")
        self.horizontalLayout_3.addWidget(self.editButton)
        self.removeButton = QtWidgets.QPushButton(Dialog)
        self.removeButton.setObjectName("removeButton")
        self.horizontalLayout_3.addWidget(self.removeButton)
        self.loadButton = QtWidgets.QPushButton(Dialog)
        self.loadButton.setObjectName("loadButton")
        self.horizontalLayout_3.addWidget(self.loadButton)
        self.exportButton = QtWidgets.QPushButton(Dialog)
        self.exportButton.setObjectName("exportButton")
        self.horizontalLayout_3.addWidget(self.exportButton)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem2)
        self.verticalLayout.addLayout(self.horizontalLayout_3)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtWidgets.QApplication.translate("Dialog", "Graph Table View", None, -1))
        self.label_2.setText(QtWidgets.QApplication.translate("Dialog", "Skeleton", None, -1))
        self.label.setText(QtWidgets.QApplication.translate("Dialog", "Graph List", None, -1))
        self.addButton.setText(QtWidgets.QApplication.translate("Dialog", "Add", None, -1))
        self.copyButton.setText(QtWidgets.QApplication.translate("Dialog", "Copy", None, -1))
        self.editButton.setText(QtWidgets.QApplication.translate("Dialog", "Edit", None, -1))
        self.removeButton.setText(QtWidgets.QApplication.translate("Dialog", "Remove", None, -1))
        self.loadButton.setText(QtWidgets.QApplication.translate("Dialog", "Load", None, -1))
        self.exportButton.setText(QtWidgets.QApplication.translate("Dialog", "Export", None, -1))

