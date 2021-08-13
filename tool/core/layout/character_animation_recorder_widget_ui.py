# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\Research\physics\workspace\mosi_app_mgtools\motion_analysis\GUI\layout\.\character_animation_recorder_widget.ui',
# licensing of 'D:\Research\physics\workspace\mosi_app_mgtools\motion_analysis\GUI\layout\.\character_animation_recorder_widget.ui' applies.
#
# Created: Wed Jan 15 17:42:04 2020
#      by: pyside2-uic  running on PySide2 5.13.1
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(527, 255)
        self.gridLayout = QtWidgets.QGridLayout(Form)
        self.gridLayout.setObjectName("gridLayout")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.recordFramesButton = QtWidgets.QToolButton(Form)
        self.recordFramesButton.setObjectName("recordFramesButton")
        self.horizontalLayout_4.addWidget(self.recordFramesButton)
        self.clearFramesButton = QtWidgets.QToolButton(Form)
        self.clearFramesButton.setObjectName("clearFramesButton")
        self.horizontalLayout_4.addWidget(self.clearFramesButton)
        self.saveFramesButton = QtWidgets.QToolButton(Form)
        self.saveFramesButton.setObjectName("saveFramesButton")
        self.horizontalLayout_4.addWidget(self.saveFramesButton)
        self.loadFramesButton = QtWidgets.QToolButton(Form)
        self.loadFramesButton.setObjectName("loadFramesButton")
        self.horizontalLayout_4.addWidget(self.loadFramesButton)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem)
        self.gridLayout.addLayout(self.horizontalLayout_4, 0, 0, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.setConstraintsButton = QtWidgets.QToolButton(Form)
        self.setConstraintsButton.setObjectName("setConstraintsButton")
        self.horizontalLayout.addWidget(self.setConstraintsButton)
        self.removeConstraintsButton = QtWidgets.QToolButton(Form)
        self.removeConstraintsButton.setObjectName("removeConstraintsButton")
        self.horizontalLayout.addWidget(self.removeConstraintsButton)
        spacerItem1 = QtWidgets.QSpacerItem(187, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.gridLayout.addLayout(self.horizontalLayout, 1, 0, 1, 1)
        self.playerBar = QtWidgets.QHBoxLayout()
        self.playerBar.setObjectName("playerBar")
        self.animationToggleButton = QtWidgets.QToolButton(Form)
        self.animationToggleButton.setObjectName("animationToggleButton")
        self.playerBar.addWidget(self.animationToggleButton)
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
        self.gridLayout.addLayout(self.playerBar, 2, 0, 1, 1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QtWidgets.QApplication.translate("Form", "Form", None, -1))
        self.recordFramesButton.setText(QtWidgets.QApplication.translate("Form", "Record Joint Angles", None, -1))
        self.clearFramesButton.setText(QtWidgets.QApplication.translate("Form", "Clear Joint Angles", None, -1))
        self.saveFramesButton.setText(QtWidgets.QApplication.translate("Form", "Save To File", None, -1))
        self.loadFramesButton.setText(QtWidgets.QApplication.translate("Form", "Load From File", None, -1))
        self.setConstraintsButton.setText(QtWidgets.QApplication.translate("Form", "Set Constraints", None, -1))
        self.removeConstraintsButton.setText(QtWidgets.QApplication.translate("Form", "Remove Constraints", None, -1))
        self.animationToggleButton.setText(QtWidgets.QApplication.translate("Form", "Play", None, -1))
        self.loopAnimationCheckBox.setText(QtWidgets.QApplication.translate("Form", "Loop", None, -1))
        self.label_2.setText(QtWidgets.QApplication.translate("Form", "Speed", None, -1))
        self.label_3.setText(QtWidgets.QApplication.translate("Form", "x", None, -1))

