# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\Research\physics\workspace\mosi_app_mgtools\motion_analysis\GUI\layout\.\animated_mesh_widget.ui',
# licensing of 'D:\Research\physics\workspace\mosi_app_mgtools\motion_analysis\GUI\layout\.\animated_mesh_widget.ui' applies.
#
# Created: Wed Jan 15 17:42:03 2020
#      by: pyside2-uic  running on PySide2 5.13.1
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(444, 87)
        self.gridLayout = QtWidgets.QGridLayout(Form)
        self.gridLayout.setObjectName("gridLayout")
        self.playerBar = QtWidgets.QHBoxLayout()
        self.playerBar.setObjectName("playerBar")
        self.visibleCheckBox = QtWidgets.QCheckBox(Form)
        self.visibleCheckBox.setChecked(True)
        self.visibleCheckBox.setObjectName("visibleCheckBox")
        self.playerBar.addWidget(self.visibleCheckBox)
        self.renderModeComboBox = QtWidgets.QComboBox(Form)
        self.renderModeComboBox.setObjectName("renderModeComboBox")
        self.playerBar.addWidget(self.renderModeComboBox)
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setObjectName("label_2")
        self.playerBar.addWidget(self.label_2)
        self.scaleLineEdit = QtWidgets.QLineEdit(Form)
        self.scaleLineEdit.setMaximumSize(QtCore.QSize(40, 16777215))
        self.scaleLineEdit.setObjectName("scaleLineEdit")
        self.playerBar.addWidget(self.scaleLineEdit)
        self.applyScaleButton = QtWidgets.QToolButton(Form)
        self.applyScaleButton.setObjectName("applyScaleButton")
        self.playerBar.addWidget(self.applyScaleButton)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.playerBar.addItem(spacerItem)
        self.gridLayout.addLayout(self.playerBar, 0, 0, 1, 1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QtWidgets.QApplication.translate("Form", "Form", None, -1))
        self.visibleCheckBox.setText(QtWidgets.QApplication.translate("Form", "Render Mesh", None, -1))
        self.label_2.setText(QtWidgets.QApplication.translate("Form", "Scale", None, -1))
        self.scaleLineEdit.setText(QtWidgets.QApplication.translate("Form", "1.0", None, -1))
        self.applyScaleButton.setText(QtWidgets.QApplication.translate("Form", "Apply", None, -1))

