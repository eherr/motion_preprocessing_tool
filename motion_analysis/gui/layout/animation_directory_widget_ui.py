# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'animation_directory_widget.ui'
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


class Ui_Form(object):
    def setupUi(self, Form):
        if Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(632, 472)
        self.verticalLayout = QVBoxLayout(Form)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.label_4 = QLabel(Form)
        self.label_4.setObjectName(u"label_4")

        self.horizontalLayout_2.addWidget(self.label_4)

        self.directoryLineEdit = QLineEdit(Form)
        self.directoryLineEdit.setObjectName(u"directoryLineEdit")

        self.horizontalLayout_2.addWidget(self.directoryLineEdit)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_2)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.animationFileListWidget = QListWidget(Form)
        self.animationFileListWidget.setObjectName(u"animationFileListWidget")

        self.verticalLayout.addWidget(self.animationFileListWidget)

        self.playerBar = QHBoxLayout()
        self.playerBar.setObjectName(u"playerBar")
        self.animationButton = QToolButton(Form)
        self.animationButton.setObjectName(u"animationButton")

        self.playerBar.addWidget(self.animationButton)

        self.animationFrameSlider = QSlider(Form)
        self.animationFrameSlider.setObjectName(u"animationFrameSlider")
        self.animationFrameSlider.setOrientation(Qt.Horizontal)

        self.playerBar.addWidget(self.animationFrameSlider)

        self.animationFrameSpinBox = QSpinBox(Form)
        self.animationFrameSpinBox.setObjectName(u"animationFrameSpinBox")

        self.playerBar.addWidget(self.animationFrameSpinBox)

        self.loopAnimationCheckBox = QCheckBox(Form)
        self.loopAnimationCheckBox.setObjectName(u"loopAnimationCheckBox")
        self.loopAnimationCheckBox.setChecked(False)

        self.playerBar.addWidget(self.loopAnimationCheckBox)

        self.label_2 = QLabel(Form)
        self.label_2.setObjectName(u"label_2")

        self.playerBar.addWidget(self.label_2)

        self.animationSpeedDoubleSpinBox = QDoubleSpinBox(Form)
        self.animationSpeedDoubleSpinBox.setObjectName(u"animationSpeedDoubleSpinBox")
        self.animationSpeedDoubleSpinBox.setSingleStep(0.100000000000000)
        self.animationSpeedDoubleSpinBox.setValue(1.000000000000000)

        self.playerBar.addWidget(self.animationSpeedDoubleSpinBox)

        self.label_3 = QLabel(Form)
        self.label_3.setObjectName(u"label_3")

        self.playerBar.addWidget(self.label_3)


        self.verticalLayout.addLayout(self.playerBar)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label = QLabel(Form)
        self.label.setObjectName(u"label")

        self.horizontalLayout.addWidget(self.label)

        self.drawModeComboBox = QComboBox(Form)
        self.drawModeComboBox.setObjectName(u"drawModeComboBox")

        self.horizontalLayout.addWidget(self.drawModeComboBox)

        self.loadButton = QPushButton(Form)
        self.loadButton.setObjectName(u"loadButton")

        self.horizontalLayout.addWidget(self.loadButton)

        self.horizontalSpacer = QSpacerItem(371, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)


        self.verticalLayout.addLayout(self.horizontalLayout)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.label_4.setText(QCoreApplication.translate("Form", u"Directory", None))
        self.animationButton.setText(QCoreApplication.translate("Form", u"Play", None))
        self.loopAnimationCheckBox.setText(QCoreApplication.translate("Form", u"Loop", None))
        self.label_2.setText(QCoreApplication.translate("Form", u"Speed", None))
        self.label_3.setText(QCoreApplication.translate("Form", u"x", None))
        self.label.setText(QCoreApplication.translate("Form", u"Draw Mode", None))
        self.loadButton.setText(QCoreApplication.translate("Form", u"Load", None))
    # retranslateUi

