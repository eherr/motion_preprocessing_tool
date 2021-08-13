# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\Research\physics\workspace\mosi_app_mgtools\tool\GUI\layout\.\nav_agent_widget.ui',
# licensing of 'D:\Research\physics\workspace\mosi_app_mgtools\tool\GUI\layout\.\nav_agent_widget.ui' applies.
#
# Created: Wed Jan 15 17:42:09 2020
#      by: pyside2-uic  running on PySide2 5.13.1
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_NavAgentWidget(object):
    def setupUi(self, NavAgentWidget):
        NavAgentWidget.setObjectName("NavAgentWidget")
        NavAgentWidget.resize(604, 362)
        self.verticalLayout = QtWidgets.QVBoxLayout(NavAgentWidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.SelectWalkTargetButton = QtWidgets.QPushButton(NavAgentWidget)
        self.SelectWalkTargetButton.setMaximumSize(QtCore.QSize(100, 16777215))
        self.SelectWalkTargetButton.setObjectName("SelectWalkTargetButton")
        self.horizontalLayout.addWidget(self.SelectWalkTargetButton)
        self.removeWalkTargetButton = QtWidgets.QPushButton(NavAgentWidget)
        self.removeWalkTargetButton.setObjectName("removeWalkTargetButton")
        self.horizontalLayout.addWidget(self.removeWalkTargetButton)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.actionComboBox = QtWidgets.QComboBox(NavAgentWidget)
        self.actionComboBox.setObjectName("actionComboBox")
        self.horizontalLayout_2.addWidget(self.actionComboBox)
        self.keyframeComboBox = QtWidgets.QComboBox(NavAgentWidget)
        self.keyframeComboBox.setObjectName("keyframeComboBox")
        self.horizontalLayout_2.addWidget(self.keyframeComboBox)
        self.performActionButton = QtWidgets.QPushButton(NavAgentWidget)
        self.performActionButton.setMaximumSize(QtCore.QSize(100, 16777215))
        self.performActionButton.setObjectName("performActionButton")
        self.horizontalLayout_2.addWidget(self.performActionButton)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label = QtWidgets.QLabel(NavAgentWidget)
        self.label.setObjectName("label")
        self.horizontalLayout_3.addWidget(self.label)
        self.toleranceLineEdit = QtWidgets.QLineEdit(NavAgentWidget)
        self.toleranceLineEdit.setMaximumSize(QtCore.QSize(40, 16777215))
        self.toleranceLineEdit.setObjectName("toleranceLineEdit")
        self.horizontalLayout_3.addWidget(self.toleranceLineEdit)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem2)
        self.verticalLayout.addLayout(self.horizontalLayout_3)

        self.retranslateUi(NavAgentWidget)
        QtCore.QMetaObject.connectSlotsByName(NavAgentWidget)

    def retranslateUi(self, NavAgentWidget):
        NavAgentWidget.setWindowTitle(QtWidgets.QApplication.translate("NavAgentWidget", "Form", None, -1))
        self.SelectWalkTargetButton.setText(QtWidgets.QApplication.translate("NavAgentWidget", "Select Walk Target", None, -1))
        self.removeWalkTargetButton.setText(QtWidgets.QApplication.translate("NavAgentWidget", "Remove Walk Target", None, -1))
        self.performActionButton.setText(QtWidgets.QApplication.translate("NavAgentWidget", "PerformAction", None, -1))
        self.label.setText(QtWidgets.QApplication.translate("NavAgentWidget", "tolerance", None, -1))

