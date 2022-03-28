# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'animation_editor_dialog.ui'
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

from tool.core.widgets.time_line_label_view import TimeLineLabelView


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(778, 641)
        self.gridLayout = QGridLayout(Dialog)
        self.gridLayout.setObjectName(u"gridLayout")
        self.leftViewerLayout = QGridLayout()
        self.leftViewerLayout.setObjectName(u"leftViewerLayout")

        self.gridLayout.addLayout(self.leftViewerLayout, 0, 0, 1, 1)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout_10 = QHBoxLayout()
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.label_8 = QLabel(Dialog)
        self.label_8.setObjectName(u"label_8")

        self.horizontalLayout_10.addWidget(self.label_8)

        self.leftDisplayFrameSlider = QSlider(Dialog)
        self.leftDisplayFrameSlider.setObjectName(u"leftDisplayFrameSlider")
        self.leftDisplayFrameSlider.setOrientation(Qt.Horizontal)

        self.horizontalLayout_10.addWidget(self.leftDisplayFrameSlider)

        self.leftDisplayFrameSpinBox = QSpinBox(Dialog)
        self.leftDisplayFrameSpinBox.setObjectName(u"leftDisplayFrameSpinBox")

        self.horizontalLayout_10.addWidget(self.leftDisplayFrameSpinBox)

        self.horizontalSpacer_8 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_10.addItem(self.horizontalSpacer_8)


        self.verticalLayout.addLayout(self.horizontalLayout_10)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.label_2 = QLabel(Dialog)
        self.label_2.setObjectName(u"label_2")

        self.horizontalLayout_3.addWidget(self.label_2)

        self.leftStartFrameSlider = QSlider(Dialog)
        self.leftStartFrameSlider.setObjectName(u"leftStartFrameSlider")
        self.leftStartFrameSlider.setOrientation(Qt.Horizontal)

        self.horizontalLayout_3.addWidget(self.leftStartFrameSlider)

        self.leftStartFrameSpinBox = QSpinBox(Dialog)
        self.leftStartFrameSpinBox.setObjectName(u"leftStartFrameSpinBox")

        self.horizontalLayout_3.addWidget(self.leftStartFrameSpinBox)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_3)


        self.verticalLayout.addLayout(self.horizontalLayout_3)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.label_3 = QLabel(Dialog)
        self.label_3.setObjectName(u"label_3")

        self.horizontalLayout_4.addWidget(self.label_3)

        self.leftEndFrameSlider = QSlider(Dialog)
        self.leftEndFrameSlider.setObjectName(u"leftEndFrameSlider")
        self.leftEndFrameSlider.setOrientation(Qt.Horizontal)

        self.horizontalLayout_4.addWidget(self.leftEndFrameSlider)

        self.leftEndFrameSpinBox = QSpinBox(Dialog)
        self.leftEndFrameSpinBox.setObjectName(u"leftEndFrameSpinBox")

        self.horizontalLayout_4.addWidget(self.leftEndFrameSpinBox)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer_4)


        self.verticalLayout.addLayout(self.horizontalLayout_4)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.jointLabel = QLabel(Dialog)
        self.jointLabel.setObjectName(u"jointLabel")

        self.horizontalLayout.addWidget(self.jointLabel)

        self.horizontalSpacer_5 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_5)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.label = QLabel(Dialog)
        self.label.setObjectName(u"label")

        self.horizontalLayout_7.addWidget(self.label)

        self.fixJointButton = QPushButton(Dialog)
        self.fixJointButton.setObjectName(u"fixJointButton")

        self.horizontalLayout_7.addWidget(self.fixJointButton)

        self.translateJointButton = QPushButton(Dialog)
        self.translateJointButton.setObjectName(u"translateJointButton")

        self.horizontalLayout_7.addWidget(self.translateJointButton)

        self.translateXLineEdit = QLineEdit(Dialog)
        self.translateXLineEdit.setObjectName(u"translateXLineEdit")
        self.translateXLineEdit.setMaximumSize(QSize(40, 16777215))

        self.horizontalLayout_7.addWidget(self.translateXLineEdit)

        self.translateYLineEdit = QLineEdit(Dialog)
        self.translateYLineEdit.setObjectName(u"translateYLineEdit")
        self.translateYLineEdit.setMaximumSize(QSize(40, 16777215))

        self.horizontalLayout_7.addWidget(self.translateYLineEdit)

        self.translateZLineEdit = QLineEdit(Dialog)
        self.translateZLineEdit.setObjectName(u"translateZLineEdit")
        self.translateZLineEdit.setMaximumSize(QSize(40, 16777215))

        self.horizontalLayout_7.addWidget(self.translateZLineEdit)

        self.applyConstraintsButton = QPushButton(Dialog)
        self.applyConstraintsButton.setObjectName(u"applyConstraintsButton")

        self.horizontalLayout_7.addWidget(self.applyConstraintsButton)

        self.clearConstraintsButton = QPushButton(Dialog)
        self.clearConstraintsButton.setObjectName(u"clearConstraintsButton")

        self.horizontalLayout_7.addWidget(self.clearConstraintsButton)

        self.ccdCheckBox = QCheckBox(Dialog)
        self.ccdCheckBox.setObjectName(u"ccdCheckBox")
        self.ccdCheckBox.setChecked(True)

        self.horizontalLayout_7.addWidget(self.ccdCheckBox)

        self.collectConstraintsCheckBox = QCheckBox(Dialog)
        self.collectConstraintsCheckBox.setObjectName(u"collectConstraintsCheckBox")
        self.collectConstraintsCheckBox.setChecked(False)

        self.horizontalLayout_7.addWidget(self.collectConstraintsCheckBox)

        self.horizontalSpacer_7 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_7.addItem(self.horizontalSpacer_7)


        self.verticalLayout.addLayout(self.horizontalLayout_7)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.label_4 = QLabel(Dialog)
        self.label_4.setObjectName(u"label_4")

        self.horizontalLayout_5.addWidget(self.label_4)

        self.rotateJointButton = QPushButton(Dialog)
        self.rotateJointButton.setObjectName(u"rotateJointButton")

        self.horizontalLayout_5.addWidget(self.rotateJointButton)

        self.rotateXLineEdit = QLineEdit(Dialog)
        self.rotateXLineEdit.setObjectName(u"rotateXLineEdit")
        self.rotateXLineEdit.setMaximumSize(QSize(40, 16777215))

        self.horizontalLayout_5.addWidget(self.rotateXLineEdit)

        self.rotateYLineEdit = QLineEdit(Dialog)
        self.rotateYLineEdit.setObjectName(u"rotateYLineEdit")
        self.rotateYLineEdit.setMaximumSize(QSize(40, 16777215))

        self.horizontalLayout_5.addWidget(self.rotateYLineEdit)

        self.rotateZLineEdit = QLineEdit(Dialog)
        self.rotateZLineEdit.setObjectName(u"rotateZLineEdit")
        self.rotateZLineEdit.setMaximumSize(QSize(40, 16777215))

        self.horizontalLayout_5.addWidget(self.rotateZLineEdit)

        self.label_5 = QLabel(Dialog)
        self.label_5.setObjectName(u"label_5")

        self.horizontalLayout_5.addWidget(self.label_5)

        self.blendRangeLineEdit = QLineEdit(Dialog)
        self.blendRangeLineEdit.setObjectName(u"blendRangeLineEdit")
        self.blendRangeLineEdit.setMaximumSize(QSize(40, 16777215))

        self.horizontalLayout_5.addWidget(self.blendRangeLineEdit)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_5.addItem(self.horizontalSpacer_2)


        self.verticalLayout.addLayout(self.horizontalLayout_5)

        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.deleteAfterButton = QPushButton(Dialog)
        self.deleteAfterButton.setObjectName(u"deleteAfterButton")

        self.horizontalLayout_6.addWidget(self.deleteAfterButton)

        self.deleteBeforeButton = QPushButton(Dialog)
        self.deleteBeforeButton.setObjectName(u"deleteBeforeButton")

        self.horizontalLayout_6.addWidget(self.deleteBeforeButton)

        self.mirrorAnimationButton = QPushButton(Dialog)
        self.mirrorAnimationButton.setObjectName(u"mirrorAnimationButton")

        self.horizontalLayout_6.addWidget(self.mirrorAnimationButton)

        self.concatenateButton = QPushButton(Dialog)
        self.concatenateButton.setObjectName(u"concatenateButton")

        self.horizontalLayout_6.addWidget(self.concatenateButton)

        self.smoothFramesButton = QPushButton(Dialog)
        self.smoothFramesButton.setObjectName(u"smoothFramesButton")

        self.horizontalLayout_6.addWidget(self.smoothFramesButton)

        self.smoothWindowSizeLineEdit = QLineEdit(Dialog)
        self.smoothWindowSizeLineEdit.setObjectName(u"smoothWindowSizeLineEdit")
        self.smoothWindowSizeLineEdit.setMaximumSize(QSize(40, 16777215))

        self.horizontalLayout_6.addWidget(self.smoothWindowSizeLineEdit)

        self.resampleButton = QPushButton(Dialog)
        self.resampleButton.setObjectName(u"resampleButton")

        self.horizontalLayout_6.addWidget(self.resampleButton)

        self.resampleFactorLineEdit = QLineEdit(Dialog)
        self.resampleFactorLineEdit.setObjectName(u"resampleFactorLineEdit")
        self.resampleFactorLineEdit.setMaximumSize(QSize(40, 16777215))

        self.horizontalLayout_6.addWidget(self.resampleFactorLineEdit)

        self.setFPSButton = QPushButton(Dialog)
        self.setFPSButton.setObjectName(u"setFPSButton")

        self.horizontalLayout_6.addWidget(self.setFPSButton)

        self.fpsLineEdit = QLineEdit(Dialog)
        self.fpsLineEdit.setObjectName(u"fpsLineEdit")
        self.fpsLineEdit.setMaximumSize(QSize(40, 16777215))

        self.horizontalLayout_6.addWidget(self.fpsLineEdit)

        self.horizontalSpacer_6 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_6.addItem(self.horizontalSpacer_6)


        self.verticalLayout_4.addLayout(self.horizontalLayout_6)


        self.verticalLayout.addLayout(self.verticalLayout_4)

        self.horizontalLayout_8 = QHBoxLayout()
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.guessGroundHeightButton = QPushButton(Dialog)
        self.guessGroundHeightButton.setObjectName(u"guessGroundHeightButton")

        self.horizontalLayout_8.addWidget(self.guessGroundHeightButton)

        self.moveToGroundButton = QPushButton(Dialog)
        self.moveToGroundButton.setObjectName(u"moveToGroundButton")

        self.horizontalLayout_8.addWidget(self.moveToGroundButton)

        self.label_7 = QLabel(Dialog)
        self.label_7.setObjectName(u"label_7")

        self.horizontalLayout_8.addWidget(self.label_7)

        self.sourceGroundHeightLineEdit = QLineEdit(Dialog)
        self.sourceGroundHeightLineEdit.setObjectName(u"sourceGroundHeightLineEdit")
        self.sourceGroundHeightLineEdit.setMaximumSize(QSize(40, 16777215))

        self.horizontalLayout_8.addWidget(self.sourceGroundHeightLineEdit)

        self.label_6 = QLabel(Dialog)
        self.label_6.setObjectName(u"label_6")

        self.horizontalLayout_8.addWidget(self.label_6)

        self.targetGroundHeightLineEdit = QLineEdit(Dialog)
        self.targetGroundHeightLineEdit.setObjectName(u"targetGroundHeightLineEdit")
        self.targetGroundHeightLineEdit.setMaximumSize(QSize(40, 16777215))

        self.horizontalLayout_8.addWidget(self.targetGroundHeightLineEdit)

        self.detectFootContactsButton = QPushButton(Dialog)
        self.detectFootContactsButton.setObjectName(u"detectFootContactsButton")

        self.horizontalLayout_8.addWidget(self.detectFootContactsButton)

        self.horizontalSpacer_9 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_8.addItem(self.horizontalSpacer_9)


        self.verticalLayout.addLayout(self.horizontalLayout_8)

        self.horizontalLayout_11 = QHBoxLayout()
        self.horizontalLayout_11.setObjectName(u"horizontalLayout_11")
        self.scaleButton = QPushButton(Dialog)
        self.scaleButton.setObjectName(u"scaleButton")

        self.horizontalLayout_11.addWidget(self.scaleButton)

        self.scaleLinEdit = QLineEdit(Dialog)
        self.scaleLinEdit.setObjectName(u"scaleLinEdit")
        self.scaleLinEdit.setMaximumSize(QSize(40, 16777215))

        self.horizontalLayout_11.addWidget(self.scaleLinEdit)

        self.horizontalSpacer_11 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_11.addItem(self.horizontalSpacer_11)


        self.verticalLayout.addLayout(self.horizontalLayout_11)

        self.horizontalLayout_9 = QHBoxLayout()
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.label_9 = QLabel(Dialog)
        self.label_9.setObjectName(u"label_9")

        self.horizontalLayout_9.addWidget(self.label_9)

        self.labelComboBox = QComboBox(Dialog)
        self.labelComboBox.setObjectName(u"labelComboBox")

        self.horizontalLayout_9.addWidget(self.labelComboBox)

        self.setAnnotationStartButton = QPushButton(Dialog)
        self.setAnnotationStartButton.setObjectName(u"setAnnotationStartButton")

        self.horizontalLayout_9.addWidget(self.setAnnotationStartButton)

        self.createAnnotationButton = QPushButton(Dialog)
        self.createAnnotationButton.setObjectName(u"createAnnotationButton")

        self.horizontalLayout_9.addWidget(self.createAnnotationButton)

        self.removeAnnotationButton = QPushButton(Dialog)
        self.removeAnnotationButton.setObjectName(u"removeAnnotationButton")

        self.horizontalLayout_9.addWidget(self.removeAnnotationButton)

        self.groundFeetButton = QPushButton(Dialog)
        self.groundFeetButton.setObjectName(u"groundFeetButton")

        self.horizontalLayout_9.addWidget(self.groundFeetButton)

        self.horizontalSpacer_10 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_9.addItem(self.horizontalSpacer_10)


        self.verticalLayout.addLayout(self.horizontalLayout_9)

        self.contactLabelView = TimeLineLabelView(Dialog)
        self.contactLabelView.setObjectName(u"contactLabelView")
        self.contactLabelView.setMaximumSize(QSize(16777215, 100))

        self.verticalLayout.addWidget(self.contactLabelView)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer)

        self.flipBlenderCoordinateSystemButton = QPushButton(Dialog)
        self.flipBlenderCoordinateSystemButton.setObjectName(u"flipBlenderCoordinateSystemButton")

        self.horizontalLayout_2.addWidget(self.flipBlenderCoordinateSystemButton)

        self.exportCommandsButton = QPushButton(Dialog)
        self.exportCommandsButton.setObjectName(u"exportCommandsButton")

        self.horizontalLayout_2.addWidget(self.exportCommandsButton)

        self.undoButton = QPushButton(Dialog)
        self.undoButton.setObjectName(u"undoButton")

        self.horizontalLayout_2.addWidget(self.undoButton)

        self.selectButton = QPushButton(Dialog)
        self.selectButton.setObjectName(u"selectButton")

        self.horizontalLayout_2.addWidget(self.selectButton)

        self.cancelButton = QPushButton(Dialog)
        self.cancelButton.setObjectName(u"cancelButton")

        self.horizontalLayout_2.addWidget(self.cancelButton)


        self.verticalLayout.addLayout(self.horizontalLayout_2)


        self.gridLayout.addLayout(self.verticalLayout, 1, 0, 1, 1)


        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Animation Editor", None))
        self.label_8.setText(QCoreApplication.translate("Dialog", u"Displayed Frame", None))
        self.label_2.setText(QCoreApplication.translate("Dialog", u"Edit Start", None))
        self.label_3.setText(QCoreApplication.translate("Dialog", u"Edit End", None))
        self.jointLabel.setText(QCoreApplication.translate("Dialog", u"Selected Joint: None", None))
        self.label.setText(QCoreApplication.translate("Dialog", u"IK", None))
        self.fixJointButton.setText(QCoreApplication.translate("Dialog", u"Fix Joint", None))
        self.translateJointButton.setText(QCoreApplication.translate("Dialog", u"Translate Joint", None))
        self.translateXLineEdit.setText(QCoreApplication.translate("Dialog", u"0", None))
        self.translateYLineEdit.setText(QCoreApplication.translate("Dialog", u"0", None))
        self.translateZLineEdit.setText(QCoreApplication.translate("Dialog", u"0", None))
        self.applyConstraintsButton.setText(QCoreApplication.translate("Dialog", u"Apply", None))
        self.clearConstraintsButton.setText(QCoreApplication.translate("Dialog", u"Clear", None))
        self.ccdCheckBox.setText(QCoreApplication.translate("Dialog", u"ccd", None))
        self.collectConstraintsCheckBox.setText(QCoreApplication.translate("Dialog", u"collect", None))
        self.label_4.setText(QCoreApplication.translate("Dialog", u"FK", None))
        self.rotateJointButton.setText(QCoreApplication.translate("Dialog", u"Rotate Joint", None))
        self.rotateXLineEdit.setText(QCoreApplication.translate("Dialog", u"0", None))
        self.rotateYLineEdit.setText(QCoreApplication.translate("Dialog", u"0", None))
        self.rotateZLineEdit.setText(QCoreApplication.translate("Dialog", u"0", None))
        self.label_5.setText(QCoreApplication.translate("Dialog", u"Blend Range", None))
        self.blendRangeLineEdit.setText(QCoreApplication.translate("Dialog", u"20", None))
        self.deleteAfterButton.setText(QCoreApplication.translate("Dialog", u"Delete After Slider", None))
        self.deleteBeforeButton.setText(QCoreApplication.translate("Dialog", u"Delete Before Slider", None))
        self.mirrorAnimationButton.setText(QCoreApplication.translate("Dialog", u"Mirror", None))
        self.concatenateButton.setText(QCoreApplication.translate("Dialog", u"Concatenate", None))
        self.smoothFramesButton.setText(QCoreApplication.translate("Dialog", u"Smooth", None))
        self.smoothWindowSizeLineEdit.setText(QCoreApplication.translate("Dialog", u"15", None))
        self.resampleButton.setText(QCoreApplication.translate("Dialog", u"Resample", None))
        self.resampleFactorLineEdit.setText(QCoreApplication.translate("Dialog", u"1", None))
        self.setFPSButton.setText(QCoreApplication.translate("Dialog", u"SetFPS", None))
        self.fpsLineEdit.setText(QCoreApplication.translate("Dialog", u"0", None))
        self.guessGroundHeightButton.setText(QCoreApplication.translate("Dialog", u"GuessGround", None))
        self.moveToGroundButton.setText(QCoreApplication.translate("Dialog", u"Move To Ground", None))
        self.label_7.setText(QCoreApplication.translate("Dialog", u"Source:", None))
        self.sourceGroundHeightLineEdit.setText(QCoreApplication.translate("Dialog", u"0", None))
        self.label_6.setText(QCoreApplication.translate("Dialog", u"Target:", None))
        self.targetGroundHeightLineEdit.setText(QCoreApplication.translate("Dialog", u"0", None))
        self.detectFootContactsButton.setText(QCoreApplication.translate("Dialog", u"Detect Foot Contacts", None))
        self.scaleButton.setText(QCoreApplication.translate("Dialog", u"Scale", None))
        self.scaleLinEdit.setText(QCoreApplication.translate("Dialog", u"1", None))
        self.label_9.setText(QCoreApplication.translate("Dialog", u"Foot Contacts", None))
        self.setAnnotationStartButton.setText(QCoreApplication.translate("Dialog", u"Set Start Frame", None))
        self.createAnnotationButton.setText(QCoreApplication.translate("Dialog", u"Create Annotation", None))
        self.removeAnnotationButton.setText(QCoreApplication.translate("Dialog", u"Remove Annotation", None))
        self.groundFeetButton.setText(QCoreApplication.translate("Dialog", u"Apply Foot Grounding", None))
        self.flipBlenderCoordinateSystemButton.setText(QCoreApplication.translate("Dialog", u"Flip Blender Coordinate Systems", None))
        self.exportCommandsButton.setText(QCoreApplication.translate("Dialog", u"Export Commands", None))
        self.undoButton.setText(QCoreApplication.translate("Dialog", u"Undo", None))
        self.selectButton.setText(QCoreApplication.translate("Dialog", u"Accept", None))
        self.cancelButton.setText(QCoreApplication.translate("Dialog", u"Cancel", None))
    # retranslateUi

