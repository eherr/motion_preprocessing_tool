# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'upload_motion_dialog.ui'
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
        Dialog.resize(363, 288)
        self.gridLayout = QGridLayout(Dialog)
        self.gridLayout.setObjectName(u"gridLayout")
        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.label = QLabel(Dialog)
        self.label.setObjectName(u"label")

        self.horizontalLayout_7.addWidget(self.label)

        self.urlLineEdit = QLineEdit(Dialog)
        self.urlLineEdit.setObjectName(u"urlLineEdit")

        self.horizontalLayout_7.addWidget(self.urlLineEdit)

        self.horizontalSpacer_11 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_7.addItem(self.horizontalSpacer_11)


        self.gridLayout.addLayout(self.horizontalLayout_7, 0, 0, 1, 1)

        self.collectionTreeWidget = QTreeWidget(Dialog)
        self.collectionTreeWidget.setObjectName(u"collectionTreeWidget")

        self.gridLayout.addWidget(self.collectionTreeWidget, 4, 0, 1, 1)

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


        self.gridLayout.addLayout(self.horizontalLayout_2, 5, 0, 1, 1)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.isProcessedCheckBox = QCheckBox(Dialog)
        self.isProcessedCheckBox.setObjectName(u"isProcessedCheckBox")

        self.horizontalLayout_3.addWidget(self.isProcessedCheckBox)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_2)


        self.gridLayout.addLayout(self.horizontalLayout_3, 3, 0, 1, 1)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label_2 = QLabel(Dialog)
        self.label_2.setObjectName(u"label_2")

        self.horizontalLayout.addWidget(self.label_2)

        self.skeletonModelComboBox = QComboBox(Dialog)
        self.skeletonModelComboBox.setObjectName(u"skeletonModelComboBox")

        self.horizontalLayout.addWidget(self.skeletonModelComboBox)

        self.newSkeletonButton = QPushButton(Dialog)
        self.newSkeletonButton.setObjectName(u"newSkeletonButton")

        self.horizontalLayout.addWidget(self.newSkeletonButton)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_4)


        self.gridLayout.addLayout(self.horizontalLayout, 2, 0, 1, 1)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.label_3 = QLabel(Dialog)
        self.label_3.setObjectName(u"label_3")

        self.horizontalLayout_4.addWidget(self.label_3)

        self.projectComboBox = QComboBox(Dialog)
        self.projectComboBox.setObjectName(u"projectComboBox")

        self.horizontalLayout_4.addWidget(self.projectComboBox)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer_3)


        self.gridLayout.addLayout(self.horizontalLayout_4, 1, 0, 1, 1)


        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Upload Motion", None))
        self.label.setText(QCoreApplication.translate("Dialog", u"URL", None))
        ___qtreewidgetitem = self.collectionTreeWidget.headerItem()
        ___qtreewidgetitem.setText(1, QCoreApplication.translate("Dialog", u"Type", None));
        ___qtreewidgetitem.setText(0, QCoreApplication.translate("Dialog", u"Name", None));
        self.selectButton.setText(QCoreApplication.translate("Dialog", u"Select", None))
        self.cancelButton.setText(QCoreApplication.translate("Dialog", u"Cancel", None))
        self.isProcessedCheckBox.setText(QCoreApplication.translate("Dialog", u"Is Processed", None))
        self.label_2.setText(QCoreApplication.translate("Dialog", u"Skeleton Model", None))
        self.newSkeletonButton.setText(QCoreApplication.translate("Dialog", u"New Skeleton", None))
        self.label_3.setText(QCoreApplication.translate("Dialog", u"Project", None))
    # retranslateUi

