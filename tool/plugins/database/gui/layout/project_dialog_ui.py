# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'project_dialog.ui'
##
## Created by: Qt User Interface Compiler version 5.14.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import (QCoreApplication, QMetaObject, QObject, QPoint,
    QRect, QSize, QUrl, Qt)
from PySide2.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QFont,
    QFontDatabase, QIcon, QLinearGradient, QPalette, QPainter, QPixmap,
    QRadialGradient)
from PySide2.QtWidgets import *


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(380, 244)
        self.verticalLayout = QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label = QLabel(Dialog)
        self.label.setObjectName(u"label")

        self.horizontalLayout.addWidget(self.label)

        self.nameLineEdit = QLineEdit(Dialog)
        self.nameLineEdit.setObjectName(u"nameLineEdit")

        self.horizontalLayout.addWidget(self.nameLineEdit)

        self.publicCheckBox = QCheckBox(Dialog)
        self.publicCheckBox.setObjectName(u"publicCheckBox")

        self.horizontalLayout.addWidget(self.publicCheckBox)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_2)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer)

        self.acceptButton = QPushButton(Dialog)
        self.acceptButton.setObjectName(u"acceptButton")

        self.horizontalLayout_2.addWidget(self.acceptButton)

        self.rejectButton = QPushButton(Dialog)
        self.rejectButton.setObjectName(u"rejectButton")

        self.horizontalLayout_2.addWidget(self.rejectButton)


        self.verticalLayout.addLayout(self.horizontalLayout_2)


        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Collection Properties", None))
        self.label.setText(QCoreApplication.translate("Dialog", u"Name", None))
        self.publicCheckBox.setText(QCoreApplication.translate("Dialog", u" Public", None))
        self.acceptButton.setText(QCoreApplication.translate("Dialog", u"Accept", None))
        self.rejectButton.setText(QCoreApplication.translate("Dialog", u"Cancel", None))
    # retranslateUi

