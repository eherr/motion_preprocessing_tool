# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'graph_table_view_dialog.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(621, 355)
        self.verticalLayout = QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.label_2 = QLabel(Dialog)
        self.label_2.setObjectName(u"label_2")

        self.horizontalLayout_4.addWidget(self.label_2)

        self.skeletonListComboBox = QComboBox(Dialog)
        self.skeletonListComboBox.setObjectName(u"skeletonListComboBox")

        self.horizontalLayout_4.addWidget(self.skeletonListComboBox)

        self.horizontalSpacer_4 = QSpacerItem(128, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer_4)


        self.verticalLayout.addLayout(self.horizontalLayout_4)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label = QLabel(Dialog)
        self.label.setObjectName(u"label")

        self.horizontalLayout.addWidget(self.label)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_3)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.graphListWidget = QListWidget(Dialog)
        self.graphListWidget.setObjectName(u"graphListWidget")

        self.verticalLayout.addWidget(self.graphListWidget)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.addButton = QPushButton(Dialog)
        self.addButton.setObjectName(u"addButton")

        self.horizontalLayout_3.addWidget(self.addButton)

        self.copyButton = QPushButton(Dialog)
        self.copyButton.setObjectName(u"copyButton")

        self.horizontalLayout_3.addWidget(self.copyButton)

        self.editButton = QPushButton(Dialog)
        self.editButton.setObjectName(u"editButton")

        self.horizontalLayout_3.addWidget(self.editButton)

        self.removeButton = QPushButton(Dialog)
        self.removeButton.setObjectName(u"removeButton")

        self.horizontalLayout_3.addWidget(self.removeButton)

        self.exportButton = QPushButton(Dialog)
        self.exportButton.setObjectName(u"exportButton")

        self.horizontalLayout_3.addWidget(self.exportButton)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_2)


        self.verticalLayout.addLayout(self.horizontalLayout_3)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.loadStateMachineButton = QPushButton(Dialog)
        self.loadStateMachineButton.setObjectName(u"loadStateMachineButton")

        self.horizontalLayout_2.addWidget(self.loadStateMachineButton)

        self.loadGeneratorButton = QPushButton(Dialog)
        self.loadGeneratorButton.setObjectName(u"loadGeneratorButton")

        self.horizontalLayout_2.addWidget(self.loadGeneratorButton)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer)


        self.verticalLayout.addLayout(self.horizontalLayout_2)


        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Graph Table View", None))
        self.label_2.setText(QCoreApplication.translate("Dialog", u"Skeleton", None))
        self.label.setText(QCoreApplication.translate("Dialog", u"Graph List", None))
        self.addButton.setText(QCoreApplication.translate("Dialog", u"Create", None))
        self.copyButton.setText(QCoreApplication.translate("Dialog", u"Copy", None))
        self.editButton.setText(QCoreApplication.translate("Dialog", u"Edit", None))
        self.removeButton.setText(QCoreApplication.translate("Dialog", u"Remove", None))
        self.exportButton.setText(QCoreApplication.translate("Dialog", u"Export", None))
        self.loadStateMachineButton.setText(QCoreApplication.translate("Dialog", u"Load as State Machine", None))
        self.loadGeneratorButton.setText(QCoreApplication.translate("Dialog", u"Load as Generator", None))
    # retranslateUi

