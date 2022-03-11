# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'animation_player_widget.ui'
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


class Ui_Form(object):
    def setupUi(self, Form):
        if Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(842, 369)
        self.verticalLayout = QVBoxLayout(Form)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.loadAnnotationButton = QToolButton(Form)
        self.loadAnnotationButton.setObjectName(u"loadAnnotationButton")

        self.horizontalLayout.addWidget(self.loadAnnotationButton)

        self.setAnnotationButton = QToolButton(Form)
        self.setAnnotationButton.setObjectName(u"setAnnotationButton")

        self.horizontalLayout.addWidget(self.setAnnotationButton)

        self.clearAnnotationButton = QToolButton(Form)
        self.clearAnnotationButton.setObjectName(u"clearAnnotationButton")

        self.horizontalLayout.addWidget(self.clearAnnotationButton)

        self.splitMotionButton = QToolButton(Form)
        self.splitMotionButton.setObjectName(u"splitMotionButton")

        self.horizontalLayout.addWidget(self.splitMotionButton)

        self.saveAnnotationButton = QToolButton(Form)
        self.saveAnnotationButton.setObjectName(u"saveAnnotationButton")

        self.horizontalLayout.addWidget(self.saveAnnotationButton)

        self.exportAnnotationsToPhaseButton = QToolButton(Form)
        self.exportAnnotationsToPhaseButton.setObjectName(u"exportAnnotationsToPhaseButton")

        self.horizontalLayout.addWidget(self.exportAnnotationsToPhaseButton)

        self.exportAnnotationsToActionsButton = QToolButton(Form)
        self.exportAnnotationsToActionsButton.setObjectName(u"exportAnnotationsToActionsButton")

        self.horizontalLayout.addWidget(self.exportAnnotationsToActionsButton)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.labelView = TimeLineLabelView(Form)
        self.labelView.setObjectName(u"labelView")
        self.labelView.setMaximumSize(QSize(16777215, 150))

        self.verticalLayout.addWidget(self.labelView)

        self.playerBar = QHBoxLayout()
        self.playerBar.setObjectName(u"playerBar")
        self.animationToggleButton = QToolButton(Form)
        self.animationToggleButton.setObjectName(u"animationToggleButton")

        self.playerBar.addWidget(self.animationToggleButton)

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

        self.relativeRootCheckBox = QCheckBox(Form)
        self.relativeRootCheckBox.setObjectName(u"relativeRootCheckBox")

        self.playerBar.addWidget(self.relativeRootCheckBox)

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

        self.fpsLineEdit = QLineEdit(Form)
        self.fpsLineEdit.setObjectName(u"fpsLineEdit")
        self.fpsLineEdit.setMaximumSize(QSize(40, 16777215))

        self.playerBar.addWidget(self.fpsLineEdit)

        self.label_5 = QLabel(Form)
        self.label_5.setObjectName(u"label_5")

        self.playerBar.addWidget(self.label_5)


        self.verticalLayout.addLayout(self.playerBar)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.label = QLabel(Form)
        self.label.setObjectName(u"label")

        self.horizontalLayout_2.addWidget(self.label)

        self.drawModeComboBox = QComboBox(Form)
        self.drawModeComboBox.setObjectName(u"drawModeComboBox")

        self.horizontalLayout_2.addWidget(self.drawModeComboBox)

        self.label_4 = QLabel(Form)
        self.label_4.setObjectName(u"label_4")

        self.horizontalLayout_2.addWidget(self.label_4)

        self.skeletonModelComboBox = QComboBox(Form)
        self.skeletonModelComboBox.setObjectName(u"skeletonModelComboBox")

        self.horizontalLayout_2.addWidget(self.skeletonModelComboBox)

        self.editSkeletonModelButton = QToolButton(Form)
        self.editSkeletonModelButton.setObjectName(u"editSkeletonModelButton")

        self.horizontalLayout_2.addWidget(self.editSkeletonModelButton)

        self.addNewSkeletonModelButton = QToolButton(Form)
        self.addNewSkeletonModelButton.setObjectName(u"addNewSkeletonModelButton")

        self.horizontalLayout_2.addWidget(self.addNewSkeletonModelButton)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_2)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.createCopyButton = QToolButton(Form)
        self.createCopyButton.setObjectName(u"createCopyButton")

        self.horizontalLayout_3.addWidget(self.createCopyButton)

        self.retargetFromSourceButton = QToolButton(Form)
        self.retargetFromSourceButton.setObjectName(u"retargetFromSourceButton")

        self.horizontalLayout_3.addWidget(self.retargetFromSourceButton)

        self.copyFromSourceButton = QToolButton(Form)
        self.copyFromSourceButton.setObjectName(u"copyFromSourceButton")

        self.horizontalLayout_3.addWidget(self.copyFromSourceButton)

        self.openEditorButton = QToolButton(Form)
        self.openEditorButton.setObjectName(u"openEditorButton")

        self.horizontalLayout_3.addWidget(self.openEditorButton)

        self.saveToBVHFileButton = QToolButton(Form)
        self.saveToBVHFileButton.setObjectName(u"saveToBVHFileButton")

        self.horizontalLayout_3.addWidget(self.saveToBVHFileButton)

        self.saveToJSONFileButton = QToolButton(Form)
        self.saveToJSONFileButton.setObjectName(u"saveToJSONFileButton")

        self.horizontalLayout_3.addWidget(self.saveToJSONFileButton)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_3)


        self.verticalLayout.addLayout(self.horizontalLayout_3)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.loadAnimatedMeshButton = QToolButton(Form)
        self.loadAnimatedMeshButton.setObjectName(u"loadAnimatedMeshButton")

        self.horizontalLayout_4.addWidget(self.loadAnimatedMeshButton)

        self.createRagdollButton = QToolButton(Form)
        self.createRagdollButton.setObjectName(u"createRagdollButton")

        self.horizontalLayout_4.addWidget(self.createRagdollButton)

        self.attachFigureButton = QToolButton(Form)
        self.attachFigureButton.setObjectName(u"attachFigureButton")

        self.horizontalLayout_4.addWidget(self.attachFigureButton)

        self.setReferenceFrameButton = QToolButton(Form)
        self.setReferenceFrameButton.setObjectName(u"setReferenceFrameButton")

        self.horizontalLayout_4.addWidget(self.setReferenceFrameButton)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer_4)


        self.verticalLayout.addLayout(self.horizontalLayout_4)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.replaceAnimationButton = QToolButton(Form)
        self.replaceAnimationButton.setObjectName(u"replaceAnimationButton")

        self.horizontalLayout_5.addWidget(self.replaceAnimationButton)

        self.plotJointsButton = QToolButton(Form)
        self.plotJointsButton.setObjectName(u"plotJointsButton")

        self.horizontalLayout_5.addWidget(self.plotJointsButton)

        self.horizontalSpacer_5 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_5.addItem(self.horizontalSpacer_5)


        self.verticalLayout.addLayout(self.horizontalLayout_5)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.loadAnnotationButton.setText(QCoreApplication.translate("Form", u"Load Annotation", None))
        self.setAnnotationButton.setText(QCoreApplication.translate("Form", u"Set Annotation", None))
        self.clearAnnotationButton.setText(QCoreApplication.translate("Form", u"Clear Annotation", None))
        self.splitMotionButton.setText(QCoreApplication.translate("Form", u"Split Motion", None))
        self.saveAnnotationButton.setText(QCoreApplication.translate("Form", u"Export To File", None))
        self.exportAnnotationsToPhaseButton.setText(QCoreApplication.translate("Form", u"Export To Phase File", None))
        self.exportAnnotationsToActionsButton.setText(QCoreApplication.translate("Form", u"Export To Actions File", None))
        self.animationToggleButton.setText(QCoreApplication.translate("Form", u"Play", None))
        self.loopAnimationCheckBox.setText(QCoreApplication.translate("Form", u"Loop", None))
        self.relativeRootCheckBox.setText(QCoreApplication.translate("Form", u"Relative Root", None))
        self.label_2.setText(QCoreApplication.translate("Form", u"Speed", None))
        self.label_3.setText(QCoreApplication.translate("Form", u"x", None))
        self.fpsLineEdit.setText(QCoreApplication.translate("Form", u"0", None))
        self.label_5.setText(QCoreApplication.translate("Form", u"FPS", None))
        self.label.setText(QCoreApplication.translate("Form", u"Draw Mode", None))
        self.label_4.setText(QCoreApplication.translate("Form", u"Skeleton model", None))
        self.editSkeletonModelButton.setText(QCoreApplication.translate("Form", u"Edit model", None))
        self.addNewSkeletonModelButton.setText(QCoreApplication.translate("Form", u"Add New model", None))
        self.createCopyButton.setText(QCoreApplication.translate("Form", u"Create Copy", None))
        self.retargetFromSourceButton.setText(QCoreApplication.translate("Form", u"Retarget from source", None))
        self.copyFromSourceButton.setText(QCoreApplication.translate("Form", u"Copy From Source", None))
        self.openEditorButton.setText(QCoreApplication.translate("Form", u"Open Editor", None))
        self.saveToBVHFileButton.setText(QCoreApplication.translate("Form", u"Save To BVH", None))
        self.saveToJSONFileButton.setText(QCoreApplication.translate("Form", u"Save to JSON", None))
        self.loadAnimatedMeshButton.setText(QCoreApplication.translate("Form", u"Load Mesh", None))
        self.createRagdollButton.setText(QCoreApplication.translate("Form", u"Create Ragdoll", None))
        self.attachFigureButton.setText(QCoreApplication.translate("Form", u"Attach Figure", None))
        self.setReferenceFrameButton.setText(QCoreApplication.translate("Form", u"Set Reference Frame", None))
        self.replaceAnimationButton.setText(QCoreApplication.translate("Form", u"Replace Animation From BVH/ACM File", None))
        self.plotJointsButton.setText(QCoreApplication.translate("Form", u"Plot Joint Trajectories", None))
    # retranslateUi

