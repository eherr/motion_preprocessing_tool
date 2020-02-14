# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\Research\physics\workspace\mosi_app_mgtools\motion_analysis\GUI\layout\.\group_animation_player_widget.ui',
# licensing of 'D:\Research\physics\workspace\mosi_app_mgtools\motion_analysis\GUI\layout\.\group_animation_player_widget.ui' applies.
#
# Created: Wed Jan 15 17:42:07 2020
#      by: pyside2-uic  running on PySide2 5.13.1
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(632, 472)
        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setObjectName("verticalLayout")
        self.animationControllerListWidget = QtWidgets.QListWidget(Form)
        self.animationControllerListWidget.setObjectName("animationControllerListWidget")
        self.verticalLayout.addWidget(self.animationControllerListWidget)
        self.playerBar = QtWidgets.QHBoxLayout()
        self.playerBar.setObjectName("playerBar")
        self.animationButton = QtWidgets.QToolButton(Form)
        self.animationButton.setObjectName("animationButton")
        self.playerBar.addWidget(self.animationButton)
        self.animationFrameSlider = QtWidgets.QSlider(Form)
        self.animationFrameSlider.setOrientation(QtCore.Qt.Horizontal)
        self.animationFrameSlider.setObjectName("animationFrameSlider")
        self.playerBar.addWidget(self.animationFrameSlider)
        self.animationFrameSpinBox = QtWidgets.QSpinBox(Form)
        self.animationFrameSpinBox.setObjectName("animationFrameSpinBox")
        self.playerBar.addWidget(self.animationFrameSpinBox)
        self.loopAnimationCheckBox = QtWidgets.QCheckBox(Form)
        self.loopAnimationCheckBox.setChecked(False)
        self.loopAnimationCheckBox.setObjectName("loopAnimationCheckBox")
        self.playerBar.addWidget(self.loopAnimationCheckBox)
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setObjectName("label_2")
        self.playerBar.addWidget(self.label_2)
        self.animationSpeedDoubleSpinBox = QtWidgets.QDoubleSpinBox(Form)
        self.animationSpeedDoubleSpinBox.setSingleStep(0.1)
        self.animationSpeedDoubleSpinBox.setProperty("value", 1.0)
        self.animationSpeedDoubleSpinBox.setObjectName("animationSpeedDoubleSpinBox")
        self.playerBar.addWidget(self.animationSpeedDoubleSpinBox)
        self.label_3 = QtWidgets.QLabel(Form)
        self.label_3.setObjectName("label_3")
        self.playerBar.addWidget(self.label_3)
        self.verticalLayout.addLayout(self.playerBar)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(Form)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.drawModeComboBox = QtWidgets.QComboBox(Form)
        self.drawModeComboBox.setObjectName("drawModeComboBox")
        self.horizontalLayout.addWidget(self.drawModeComboBox)
        spacerItem = QtWidgets.QSpacerItem(371, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QtWidgets.QApplication.translate("Form", "Form", None, -1))
        self.animationButton.setText(QtWidgets.QApplication.translate("Form", "Play", None, -1))
        self.loopAnimationCheckBox.setText(QtWidgets.QApplication.translate("Form", "Loop", None, -1))
        self.label_2.setText(QtWidgets.QApplication.translate("Form", "Speed", None, -1))
        self.label_3.setText(QtWidgets.QApplication.translate("Form", "x", None, -1))
        self.label.setText(QtWidgets.QApplication.translate("Form", "Draw Mode", None, -1))

