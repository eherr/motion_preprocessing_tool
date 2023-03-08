# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'data_transform_dialog.ui'
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
        Dialog.resize(553, 284)
        self.gridLayout = QGridLayout(Dialog)
        self.gridLayout.setObjectName(u"gridLayout")
        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.label = QLabel(Dialog)
        self.label.setObjectName(u"label")

        self.horizontalLayout_3.addWidget(self.label)

        self.userLineEdit = QLineEdit(Dialog)
        self.userLineEdit.setObjectName(u"userLineEdit")

        self.horizontalLayout_3.addWidget(self.userLineEdit)

        self.label_3 = QLabel(Dialog)
        self.label_3.setObjectName(u"label_3")

        self.horizontalLayout_3.addWidget(self.label_3)

        self.passwordLineEdit = QLineEdit(Dialog)
        self.passwordLineEdit.setObjectName(u"passwordLineEdit")
        self.passwordLineEdit.setEchoMode(QLineEdit.Password)

        self.horizontalLayout_3.addWidget(self.passwordLineEdit)

        self.useClusterCheckBox = QCheckBox(Dialog)
        self.useClusterCheckBox.setObjectName(u"useClusterCheckBox")

        self.horizontalLayout_3.addWidget(self.useClusterCheckBox)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_2)


        self.gridLayout.addLayout(self.horizontalLayout_3, 6, 0, 1, 1)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.label_4 = QLabel(Dialog)
        self.label_4.setObjectName(u"label_4")

        self.horizontalLayout_4.addWidget(self.label_4)

        self.urlLineEdit = QLineEdit(Dialog)
        self.urlLineEdit.setObjectName(u"urlLineEdit")

        self.horizontalLayout_4.addWidget(self.urlLineEdit)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer_3)


        self.gridLayout.addLayout(self.horizontalLayout_4, 7, 0, 1, 1)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label_2 = QLabel(Dialog)
        self.label_2.setObjectName(u"label_2")

        self.horizontalLayout.addWidget(self.label_2)

        self.dataTransformComboBox = QComboBox(Dialog)
        self.dataTransformComboBox.setObjectName(u"dataTransformComboBox")
        self.dataTransformComboBox.setMinimumSize(QSize(200, 0))

        self.horizontalLayout.addWidget(self.dataTransformComboBox)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_4)


        self.gridLayout.addLayout(self.horizontalLayout, 1, 0, 1, 1)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.label_5 = QLabel(Dialog)
        self.label_5.setObjectName(u"label_5")

        self.horizontalLayout_5.addWidget(self.label_5)

        self.nameLineEdit = QLineEdit(Dialog)
        self.nameLineEdit.setObjectName(u"nameLineEdit")

        self.horizontalLayout_5.addWidget(self.nameLineEdit)

        self.storeLogCheckBox = QCheckBox(Dialog)
        self.storeLogCheckBox.setObjectName(u"storeLogCheckBox")

        self.horizontalLayout_5.addWidget(self.storeLogCheckBox)

        self.horizontalSpacer_5 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_5.addItem(self.horizontalSpacer_5)


        self.gridLayout.addLayout(self.horizontalLayout_5, 2, 0, 1, 1)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label_6 = QLabel(Dialog)
        self.label_6.setObjectName(u"label_6")

        self.verticalLayout.addWidget(self.label_6)

        self.parametersTextEdit = QTextEdit(Dialog)
        self.parametersTextEdit.setObjectName(u"parametersTextEdit")

        self.verticalLayout.addWidget(self.parametersTextEdit)


        self.gridLayout.addLayout(self.verticalLayout, 5, 0, 1, 1)

        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.label_7 = QLabel(Dialog)
        self.label_7.setObjectName(u"label_7")

        self.horizontalLayout_7.addWidget(self.label_7)

        self.outputSkeletonComboBox = QComboBox(Dialog)
        self.outputSkeletonComboBox.setObjectName(u"outputSkeletonComboBox")

        self.horizontalLayout_7.addWidget(self.outputSkeletonComboBox)

        self.horizontalSpacer_6 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_7.addItem(self.horizontalSpacer_6)


        self.gridLayout.addLayout(self.horizontalLayout_7, 3, 0, 1, 1)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer)

        self.selectButton = QPushButton(Dialog)
        self.selectButton.setObjectName(u"selectButton")

        self.horizontalLayout_2.addWidget(self.selectButton)

        self.cancelButton = QPushButton(Dialog)
        self.cancelButton.setObjectName(u"cancelButton")

        self.horizontalLayout_2.addWidget(self.cancelButton)


        self.gridLayout.addLayout(self.horizontalLayout_2, 8, 0, 1, 1)


        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Data Transform", None))
        self.label.setText(QCoreApplication.translate("Dialog", u"User", None))
        self.label_3.setText(QCoreApplication.translate("Dialog", u"Password", None))
        self.useClusterCheckBox.setText(QCoreApplication.translate("Dialog", u"Use Cluster", None))
        self.label_4.setText(QCoreApplication.translate("Dialog", u"Cluster URL", None))
        self.label_2.setText(QCoreApplication.translate("Dialog", u"Data Transform", None))
        self.label_5.setText(QCoreApplication.translate("Dialog", u"Name", None))
        self.storeLogCheckBox.setText(QCoreApplication.translate("Dialog", u"Store Log", None))
        self.label_6.setText(QCoreApplication.translate("Dialog", u"Parameters", None))
        self.label_7.setText(QCoreApplication.translate("Dialog", u"Output Skeleton", None))
        self.selectButton.setText(QCoreApplication.translate("Dialog", u"Run", None))
        self.cancelButton.setText(QCoreApplication.translate("Dialog", u"Cancel", None))
    # retranslateUi

