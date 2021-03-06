# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'animation_player_widget.ui',
# licensing of 'animation_player_widget.ui' applies.
#
# Created: Thu Jan 30 14:24:55 2020
#      by: pyside2-uic  running on PySide2 5.13.1
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(842, 369)
        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.loadAnnotationButton = QtWidgets.QToolButton(Form)
        self.loadAnnotationButton.setObjectName("loadAnnotationButton")
        self.horizontalLayout.addWidget(self.loadAnnotationButton)
        self.setAnnotationButton = QtWidgets.QToolButton(Form)
        self.setAnnotationButton.setObjectName("setAnnotationButton")
        self.horizontalLayout.addWidget(self.setAnnotationButton)
        self.clearAnnotationButton = QtWidgets.QToolButton(Form)
        self.clearAnnotationButton.setObjectName("clearAnnotationButton")
        self.horizontalLayout.addWidget(self.clearAnnotationButton)
        self.splitMotionButton = QtWidgets.QToolButton(Form)
        self.splitMotionButton.setObjectName("splitMotionButton")
        self.horizontalLayout.addWidget(self.splitMotionButton)
        self.saveAnnotationButton = QtWidgets.QToolButton(Form)
        self.saveAnnotationButton.setObjectName("saveAnnotationButton")
        self.horizontalLayout.addWidget(self.saveAnnotationButton)
        self.exportAnnotationsToPhaseButton = QtWidgets.QToolButton(Form)
        self.exportAnnotationsToPhaseButton.setObjectName("exportAnnotationsToPhaseButton")
        self.horizontalLayout.addWidget(self.exportAnnotationsToPhaseButton)
        self.exportAnnotationsToActionsButton = QtWidgets.QToolButton(Form)
        self.exportAnnotationsToActionsButton.setObjectName("exportAnnotationsToActionsButton")
        self.horizontalLayout.addWidget(self.exportAnnotationsToActionsButton)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.labelView = TimeLineLabelView(Form)
        self.labelView.setMaximumSize(QtCore.QSize(16777215, 150))
        self.labelView.setObjectName("labelView")
        self.verticalLayout.addWidget(self.labelView)
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
        self.relativeRootCheckBox = QtWidgets.QCheckBox(Form)
        self.relativeRootCheckBox.setObjectName("relativeRootCheckBox")
        self.playerBar.addWidget(self.relativeRootCheckBox)
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
        self.fpsLineEdit = QtWidgets.QLineEdit(Form)
        self.fpsLineEdit.setMaximumSize(QtCore.QSize(40, 16777215))
        self.fpsLineEdit.setObjectName("fpsLineEdit")
        self.playerBar.addWidget(self.fpsLineEdit)
        self.label_5 = QtWidgets.QLabel(Form)
        self.label_5.setObjectName("label_5")
        self.playerBar.addWidget(self.label_5)
        self.verticalLayout.addLayout(self.playerBar)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label = QtWidgets.QLabel(Form)
        self.label.setObjectName("label")
        self.horizontalLayout_2.addWidget(self.label)
        self.drawModeComboBox = QtWidgets.QComboBox(Form)
        self.drawModeComboBox.setObjectName("drawModeComboBox")
        self.horizontalLayout_2.addWidget(self.drawModeComboBox)
        self.label_4 = QtWidgets.QLabel(Form)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_2.addWidget(self.label_4)
        self.skeletonModelComboBox = QtWidgets.QComboBox(Form)
        self.skeletonModelComboBox.setObjectName("skeletonModelComboBox")
        self.horizontalLayout_2.addWidget(self.skeletonModelComboBox)
        self.editSkeletonModelButton = QtWidgets.QToolButton(Form)
        self.editSkeletonModelButton.setObjectName("editSkeletonModelButton")
        self.horizontalLayout_2.addWidget(self.editSkeletonModelButton)
        self.addNewSkeletonModelButton = QtWidgets.QToolButton(Form)
        self.addNewSkeletonModelButton.setObjectName("addNewSkeletonModelButton")
        self.horizontalLayout_2.addWidget(self.addNewSkeletonModelButton)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.createCopyButton = QtWidgets.QToolButton(Form)
        self.createCopyButton.setObjectName("createCopyButton")
        self.horizontalLayout_3.addWidget(self.createCopyButton)
        self.uploadToDBButton = QtWidgets.QToolButton(Form)
        self.uploadToDBButton.setObjectName("uploadToDBButton")
        self.horizontalLayout_3.addWidget(self.uploadToDBButton)
        self.retargetFromSourceButton = QtWidgets.QToolButton(Form)
        self.retargetFromSourceButton.setObjectName("retargetFromSourceButton")
        self.horizontalLayout_3.addWidget(self.retargetFromSourceButton)
        self.copyFromSourceButton = QtWidgets.QToolButton(Form)
        self.copyFromSourceButton.setObjectName("copyFromSourceButton")
        self.horizontalLayout_3.addWidget(self.copyFromSourceButton)
        self.openEditorButton = QtWidgets.QToolButton(Form)
        self.openEditorButton.setObjectName("openEditorButton")
        self.horizontalLayout_3.addWidget(self.openEditorButton)
        self.saveToBVHFileButton = QtWidgets.QToolButton(Form)
        self.saveToBVHFileButton.setObjectName("saveToBVHFileButton")
        self.horizontalLayout_3.addWidget(self.saveToBVHFileButton)
        self.saveToJSONFileButton = QtWidgets.QToolButton(Form)
        self.saveToJSONFileButton.setObjectName("saveToJSONFileButton")
        self.horizontalLayout_3.addWidget(self.saveToJSONFileButton)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem2)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.loadAnimatedMeshButton = QtWidgets.QToolButton(Form)
        self.loadAnimatedMeshButton.setObjectName("loadAnimatedMeshButton")
        self.horizontalLayout_4.addWidget(self.loadAnimatedMeshButton)
        self.createRagdollButton = QtWidgets.QToolButton(Form)
        self.createRagdollButton.setObjectName("createRagdollButton")
        self.horizontalLayout_4.addWidget(self.createRagdollButton)
        self.attachFigureButton = QtWidgets.QToolButton(Form)
        self.attachFigureButton.setObjectName("attachFigureButton")
        self.horizontalLayout_4.addWidget(self.attachFigureButton)
        self.setReferenceFrameButton = QtWidgets.QToolButton(Form)
        self.setReferenceFrameButton.setObjectName("setReferenceFrameButton")
        self.horizontalLayout_4.addWidget(self.setReferenceFrameButton)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem3)
        self.verticalLayout.addLayout(self.horizontalLayout_4)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.replaceAnimationButton = QtWidgets.QToolButton(Form)
        self.replaceAnimationButton.setObjectName("replaceAnimationButton")
        self.horizontalLayout_5.addWidget(self.replaceAnimationButton)
        self.plotJointsButton = QtWidgets.QToolButton(Form)
        self.plotJointsButton.setObjectName("plotJointsButton")
        self.horizontalLayout_5.addWidget(self.plotJointsButton)
        spacerItem4 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem4)
        self.verticalLayout.addLayout(self.horizontalLayout_5)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QtWidgets.QApplication.translate("Form", "Form", None, -1))
        self.loadAnnotationButton.setText(QtWidgets.QApplication.translate("Form", "Load Annotation", None, -1))
        self.setAnnotationButton.setText(QtWidgets.QApplication.translate("Form", "Set Annotation", None, -1))
        self.clearAnnotationButton.setText(QtWidgets.QApplication.translate("Form", "Clear Annotation", None, -1))
        self.splitMotionButton.setText(QtWidgets.QApplication.translate("Form", "Split Motion", None, -1))
        self.saveAnnotationButton.setText(QtWidgets.QApplication.translate("Form", "Export To File", None, -1))
        self.exportAnnotationsToPhaseButton.setText(QtWidgets.QApplication.translate("Form", "Export To Phase File", None, -1))
        self.exportAnnotationsToActionsButton.setText(QtWidgets.QApplication.translate("Form", "Export To Actions File", None, -1))
        self.animationToggleButton.setText(QtWidgets.QApplication.translate("Form", "Play", None, -1))
        self.loopAnimationCheckBox.setText(QtWidgets.QApplication.translate("Form", "Loop", None, -1))
        self.relativeRootCheckBox.setText(QtWidgets.QApplication.translate("Form", "Relative Root", None, -1))
        self.label_2.setText(QtWidgets.QApplication.translate("Form", "Speed", None, -1))
        self.label_3.setText(QtWidgets.QApplication.translate("Form", "x", None, -1))
        self.fpsLineEdit.setText(QtWidgets.QApplication.translate("Form", "0", None, -1))
        self.label_5.setText(QtWidgets.QApplication.translate("Form", "FPS", None, -1))
        self.label.setText(QtWidgets.QApplication.translate("Form", "Draw Mode", None, -1))
        self.label_4.setText(QtWidgets.QApplication.translate("Form", "Skeleton model", None, -1))
        self.editSkeletonModelButton.setText(QtWidgets.QApplication.translate("Form", "Edit model", None, -1))
        self.addNewSkeletonModelButton.setText(QtWidgets.QApplication.translate("Form", "Add New model", None, -1))
        self.createCopyButton.setText(QtWidgets.QApplication.translate("Form", "Create Copy", None, -1))
        self.uploadToDBButton.setText(QtWidgets.QApplication.translate("Form", "Upload To Database", None, -1))
        self.retargetFromSourceButton.setText(QtWidgets.QApplication.translate("Form", "Retarget from source", None, -1))
        self.copyFromSourceButton.setText(QtWidgets.QApplication.translate("Form", "Copy From Source", None, -1))
        self.openEditorButton.setText(QtWidgets.QApplication.translate("Form", "Open Editor", None, -1))
        self.saveToBVHFileButton.setText(QtWidgets.QApplication.translate("Form", "Save To BVH", None, -1))
        self.saveToJSONFileButton.setText(QtWidgets.QApplication.translate("Form", "Save to JSON", None, -1))
        self.loadAnimatedMeshButton.setText(QtWidgets.QApplication.translate("Form", "Load Mesh", None, -1))
        self.createRagdollButton.setText(QtWidgets.QApplication.translate("Form", "Create Ragdoll", None, -1))
        self.attachFigureButton.setText(QtWidgets.QApplication.translate("Form", "Attach Figure", None, -1))
        self.setReferenceFrameButton.setText(QtWidgets.QApplication.translate("Form", "Set Reference Frame", None, -1))
        self.replaceAnimationButton.setText(QtWidgets.QApplication.translate("Form", "Replace Animation From BVH/ACM File", None, -1))
        self.plotJointsButton.setText(QtWidgets.QApplication.translate("Form", "Plot Joint Trajectories", None, -1))

from motion_analysis.gui.widgets.time_line_label_view import TimeLineLabelView
