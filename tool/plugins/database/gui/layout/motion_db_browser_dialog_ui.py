# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'motion_db_browser_dialog.ui'
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
        Dialog.resize(859, 459)
        self.gridLayout_3 = QGridLayout(Dialog)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.label = QLabel(Dialog)
        self.label.setObjectName(u"label")

        self.horizontalLayout_7.addWidget(self.label)

        self.urlLineEdit = QLineEdit(Dialog)
        self.urlLineEdit.setObjectName(u"urlLineEdit")

        self.horizontalLayout_7.addWidget(self.urlLineEdit)

        self.statusLabel = QLabel(Dialog)
        self.statusLabel.setObjectName(u"statusLabel")

        self.horizontalLayout_7.addWidget(self.statusLabel)

        self.horizontalSpacer_11 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_7.addItem(self.horizontalSpacer_11)


        self.gridLayout_3.addLayout(self.horizontalLayout_7, 0, 0, 1, 1)

        self.horizontalLayout_9 = QHBoxLayout()
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.label_2 = QLabel(Dialog)
        self.label_2.setObjectName(u"label_2")

        self.horizontalLayout_9.addWidget(self.label_2)

        self.projectListComboBox = QComboBox(Dialog)
        self.projectListComboBox.setObjectName(u"projectListComboBox")
        self.projectListComboBox.setMinimumSize(QSize(100, 0))

        self.horizontalLayout_9.addWidget(self.projectListComboBox)

        self.newProjectButton = QPushButton(Dialog)
        self.newProjectButton.setObjectName(u"newProjectButton")

        self.horizontalLayout_9.addWidget(self.newProjectButton)

        self.editProjectButton = QPushButton(Dialog)
        self.editProjectButton.setObjectName(u"editProjectButton")

        self.horizontalLayout_9.addWidget(self.editProjectButton)

        self.deleteProjectButton = QPushButton(Dialog)
        self.deleteProjectButton.setObjectName(u"deleteProjectButton")

        self.horizontalLayout_9.addWidget(self.deleteProjectButton)

        self.horizontalSpacer_7 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_9.addItem(self.horizontalSpacer_7)


        self.gridLayout_3.addLayout(self.horizontalLayout_9, 1, 0, 1, 1)

        self.skeletonHorizontalLayout = QHBoxLayout()
        self.skeletonHorizontalLayout.setObjectName(u"skeletonHorizontalLayout")
        self.skeletonLabel = QLabel(Dialog)
        self.skeletonLabel.setObjectName(u"skeletonLabel")

        self.skeletonHorizontalLayout.addWidget(self.skeletonLabel)

        self.skeletonListComboBox = QComboBox(Dialog)
        self.skeletonListComboBox.setObjectName(u"skeletonListComboBox")
        self.skeletonListComboBox.setMinimumSize(QSize(100, 0))

        self.skeletonHorizontalLayout.addWidget(self.skeletonListComboBox)

        self.newSkeletonButton = QPushButton(Dialog)
        self.newSkeletonButton.setObjectName(u"newSkeletonButton")

        self.skeletonHorizontalLayout.addWidget(self.newSkeletonButton)

        self.deleteSkeletonButton = QPushButton(Dialog)
        self.deleteSkeletonButton.setObjectName(u"deleteSkeletonButton")

        self.skeletonHorizontalLayout.addWidget(self.deleteSkeletonButton)

        self.replaceSkeletonButton = QPushButton(Dialog)
        self.replaceSkeletonButton.setObjectName(u"replaceSkeletonButton")

        self.skeletonHorizontalLayout.addWidget(self.replaceSkeletonButton)

        self.loadSkeletonButton = QPushButton(Dialog)
        self.loadSkeletonButton.setObjectName(u"loadSkeletonButton")

        self.skeletonHorizontalLayout.addWidget(self.loadSkeletonButton)

        self.exportSkeletonButton = QPushButton(Dialog)
        self.exportSkeletonButton.setObjectName(u"exportSkeletonButton")

        self.skeletonHorizontalLayout.addWidget(self.exportSkeletonButton)

        self.editSkeletonButton = QPushButton(Dialog)
        self.editSkeletonButton.setObjectName(u"editSkeletonButton")

        self.skeletonHorizontalLayout.addWidget(self.editSkeletonButton)

        self.horizontalSpacer_6 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.skeletonHorizontalLayout.addItem(self.horizontalSpacer_6)


        self.gridLayout_3.addLayout(self.skeletonHorizontalLayout, 2, 0, 1, 1)

        self.horizontalLayout_11 = QHBoxLayout()
        self.horizontalLayout_11.setObjectName(u"horizontalLayout_11")
        self.label_3 = QLabel(Dialog)
        self.label_3.setObjectName(u"label_3")

        self.horizontalLayout_11.addWidget(self.label_3)

        self.tagComboBox = QComboBox(Dialog)
        self.tagComboBox.setObjectName(u"tagComboBox")

        self.horizontalLayout_11.addWidget(self.tagComboBox)

        self.newTagButton = QPushButton(Dialog)
        self.newTagButton.setObjectName(u"newTagButton")

        self.horizontalLayout_11.addWidget(self.newTagButton)

        self.renameTagButton = QPushButton(Dialog)
        self.renameTagButton.setObjectName(u"renameTagButton")

        self.horizontalLayout_11.addWidget(self.renameTagButton)

        self.deleteTagButton = QPushButton(Dialog)
        self.deleteTagButton.setObjectName(u"deleteTagButton")

        self.horizontalLayout_11.addWidget(self.deleteTagButton)

        self.horizontalSpacer_14 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_11.addItem(self.horizontalSpacer_14)


        self.gridLayout_3.addLayout(self.horizontalLayout_11, 3, 0, 1, 1)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalSpacer2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer2)

        self.debugInfoButton = QPushButton(Dialog)
        self.debugInfoButton.setObjectName(u"debugInfoButton")

        self.horizontalLayout_3.addWidget(self.debugInfoButton)

        self.exportDatabaseButton = QPushButton(Dialog)
        self.exportDatabaseButton.setObjectName(u"exportDatabaseButton")

        self.horizontalLayout_3.addWidget(self.exportDatabaseButton)

        self.generateModelGraphButton = QPushButton(Dialog)
        self.generateModelGraphButton.setObjectName(u"generateModelGraphButton")

        self.horizontalLayout_3.addWidget(self.generateModelGraphButton)


        self.gridLayout_3.addLayout(self.horizontalLayout_3, 5, 0, 1, 1)

        self.splitter = QSplitter(Dialog)
        self.splitter.setObjectName(u"splitter")
        self.splitter.setOrientation(Qt.Horizontal)
        self.layoutWidget = QWidget(self.splitter)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.verticalLayout = QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.collectionTreeWidget = QTreeWidget(self.layoutWidget)
        self.collectionTreeWidget.setObjectName(u"collectionTreeWidget")

        self.verticalLayout.addWidget(self.collectionTreeWidget)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.horizontalSpacer_12 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_6.addItem(self.horizontalSpacer_12)

        self.addCollectionButton = QPushButton(self.layoutWidget)
        self.addCollectionButton.setObjectName(u"addCollectionButton")

        self.horizontalLayout_6.addWidget(self.addCollectionButton)

        self.editCollectionButton = QPushButton(self.layoutWidget)
        self.editCollectionButton.setObjectName(u"editCollectionButton")

        self.horizontalLayout_6.addWidget(self.editCollectionButton)

        self.deleteCollectionButton = QPushButton(self.layoutWidget)
        self.deleteCollectionButton.setObjectName(u"deleteCollectionButton")

        self.horizontalLayout_6.addWidget(self.deleteCollectionButton)


        self.verticalLayout.addLayout(self.horizontalLayout_6)

        self.splitter.addWidget(self.layoutWidget)
        self.tabWidget = QTabWidget(self.splitter)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tabWidget.setMaximumSize(QSize(16777215, 16777211))
        self.tabWidget.setTabBarAutoHide(False)
        self.clip_tab = QWidget()
        self.clip_tab.setObjectName(u"clip_tab")
        self.gridLayout = QGridLayout(self.clip_tab)
        self.gridLayout.setObjectName(u"gridLayout")
        self.fileListWidget = QListWidget(self.clip_tab)
        self.fileListWidget.setObjectName(u"fileListWidget")

        self.gridLayout.addWidget(self.fileListWidget, 0, 0, 1, 1)

        self.horizontalLayout_34 = QHBoxLayout()
        self.horizontalLayout_34.setObjectName(u"horizontalLayout_34")
        self.horizontalSpacer_8 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_34.addItem(self.horizontalSpacer_8)

        self.runDataTransformButton = QPushButton(self.clip_tab)
        self.runDataTransformButton.setObjectName(u"runDataTransformButton")

        self.horizontalLayout_34.addWidget(self.runDataTransformButton)


        self.gridLayout.addLayout(self.horizontalLayout_34, 3, 0, 1, 1)

        self.horizontalLayout_31 = QHBoxLayout()
        self.horizontalLayout_31.setObjectName(u"horizontalLayout_31")
        self.horizontalSpacer21 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_31.addItem(self.horizontalSpacer21)

        self.importFileButton = QPushButton(self.clip_tab)
        self.importFileButton.setObjectName(u"importFileButton")

        self.horizontalLayout_31.addWidget(self.importFileButton)

        self.importCollectionButton = QPushButton(self.clip_tab)
        self.importCollectionButton.setObjectName(u"importCollectionButton")

        self.horizontalLayout_31.addWidget(self.importCollectionButton)

        self.exportCollectionButton = QPushButton(self.clip_tab)
        self.exportCollectionButton.setObjectName(u"exportCollectionButton")

        self.horizontalLayout_31.addWidget(self.exportCollectionButton)


        self.gridLayout.addLayout(self.horizontalLayout_31, 2, 0, 1, 1)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer)

        self.loadFilesButton = QPushButton(self.clip_tab)
        self.loadFilesButton.setObjectName(u"loadFilesButton")

        self.horizontalLayout_2.addWidget(self.loadFilesButton)

        self.deleteFilesButton = QPushButton(self.clip_tab)
        self.deleteFilesButton.setObjectName(u"deleteFilesButton")

        self.horizontalLayout_2.addWidget(self.deleteFilesButton)

        self.exportFilesButton = QPushButton(self.clip_tab)
        self.exportFilesButton.setObjectName(u"exportFilesButton")

        self.horizontalLayout_2.addWidget(self.exportFilesButton)

        self.copyMotionsButton = QPushButton(self.clip_tab)
        self.copyMotionsButton.setObjectName(u"copyMotionsButton")

        self.horizontalLayout_2.addWidget(self.copyMotionsButton)


        self.gridLayout.addLayout(self.horizontalLayout_2, 1, 0, 1, 1)

        self.tabWidget.addTab(self.clip_tab, "")
        self.fileListWidget.raise_()
        self.experiment_tab = QWidget()
        self.experiment_tab.setObjectName(u"experiment_tab")
        self.verticalLayout_2 = QVBoxLayout(self.experiment_tab)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.experimentListWidget = QListWidget(self.experiment_tab)
        self.experimentListWidget.setObjectName(u"experimentListWidget")
        self.experimentListWidget.setSelectionMode(QAbstractItemView.MultiSelection)

        self.verticalLayout_2.addWidget(self.experimentListWidget)

        self.horizontalLayout_10 = QHBoxLayout()
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.horizontalSpacer_13 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_10.addItem(self.horizontalSpacer_13)

        self.smoothPlotCheckBox = QCheckBox(self.experiment_tab)
        self.smoothPlotCheckBox.setObjectName(u"smoothPlotCheckBox")
        self.smoothPlotCheckBox.setEnabled(True)
        self.smoothPlotCheckBox.setChecked(True)

        self.horizontalLayout_10.addWidget(self.smoothPlotCheckBox)

        self.plotExperimentButton = QPushButton(self.experiment_tab)
        self.plotExperimentButton.setObjectName(u"plotExperimentButton")

        self.horizontalLayout_10.addWidget(self.plotExperimentButton)

        self.exportExperimentButton = QPushButton(self.experiment_tab)
        self.exportExperimentButton.setObjectName(u"exportExperimentButton")

        self.horizontalLayout_10.addWidget(self.exportExperimentButton)

        self.deleteExperimentButton = QPushButton(self.experiment_tab)
        self.deleteExperimentButton.setObjectName(u"deleteExperimentButton")

        self.horizontalLayout_10.addWidget(self.deleteExperimentButton)


        self.verticalLayout_2.addLayout(self.horizontalLayout_10)

        self.tabWidget.addTab(self.experiment_tab, "")
        self.splitter.addWidget(self.tabWidget)

        self.gridLayout_3.addWidget(self.splitter, 4, 0, 1, 1)


        self.retranslateUi(Dialog)

        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Motion Database Browser", None))
        self.label.setText(QCoreApplication.translate("Dialog", u"URL", None))
        self.statusLabel.setText(QCoreApplication.translate("Dialog", u"Status", None))
        self.label_2.setText(QCoreApplication.translate("Dialog", u"Project", None))
        self.newProjectButton.setText(QCoreApplication.translate("Dialog", u"New", None))
        self.editProjectButton.setText(QCoreApplication.translate("Dialog", u"Edit", None))
        self.deleteProjectButton.setText(QCoreApplication.translate("Dialog", u"Delete", None))
        self.skeletonLabel.setText(QCoreApplication.translate("Dialog", u"Skeleton", None))
        self.newSkeletonButton.setText(QCoreApplication.translate("Dialog", u"New Skeleton", None))
        self.deleteSkeletonButton.setText(QCoreApplication.translate("Dialog", u"Delete Skeleton", None))
        self.replaceSkeletonButton.setText(QCoreApplication.translate("Dialog", u"Replace Skeleton", None))
        self.loadSkeletonButton.setText(QCoreApplication.translate("Dialog", u"Load Skeleton into Scene", None))
        self.exportSkeletonButton.setText(QCoreApplication.translate("Dialog", u"Export Skeleton", None))
        self.editSkeletonButton.setText(QCoreApplication.translate("Dialog", u"Edit Skeleton", None))
        self.label_3.setText(QCoreApplication.translate("Dialog", u"Tag", None))
        self.newTagButton.setText(QCoreApplication.translate("Dialog", u"New", None))
        self.renameTagButton.setText(QCoreApplication.translate("Dialog", u"Rename", None))
        self.deleteTagButton.setText(QCoreApplication.translate("Dialog", u"Delete", None))
        self.debugInfoButton.setText(QCoreApplication.translate("Dialog", u"Print Debug Info", None))
        self.exportDatabaseButton.setText(QCoreApplication.translate("Dialog", u"Export Database To Folder", None))
        self.generateModelGraphButton.setText(QCoreApplication.translate("Dialog", u"Generate Model Graph ", None))
        ___qtreewidgetitem = self.collectionTreeWidget.headerItem()
        ___qtreewidgetitem.setText(1, QCoreApplication.translate("Dialog", u"Type", None));
        ___qtreewidgetitem.setText(0, QCoreApplication.translate("Dialog", u"Name", None));
        self.addCollectionButton.setText(QCoreApplication.translate("Dialog", u"Add Collection", None))
        self.editCollectionButton.setText(QCoreApplication.translate("Dialog", u"Edit Collection", None))
        self.deleteCollectionButton.setText(QCoreApplication.translate("Dialog", u"Delete Collection", None))
        self.runDataTransformButton.setText(QCoreApplication.translate("Dialog", u"Run Data Transform", None))
        self.importFileButton.setText(QCoreApplication.translate("Dialog", u"Import File", None))
        self.importCollectionButton.setText(QCoreApplication.translate("Dialog", u"Import Collection from Folder", None))
        self.exportCollectionButton.setText(QCoreApplication.translate("Dialog", u"Export Collection To Folder", None))
        self.loadFilesButton.setText(QCoreApplication.translate("Dialog", u"Load Selected into Scene", None))
        self.deleteFilesButton.setText(QCoreApplication.translate("Dialog", u"Delete Selected", None))
        self.exportFilesButton.setText(QCoreApplication.translate("Dialog", u"Export Selected", None))
        self.copyMotionsButton.setText(QCoreApplication.translate("Dialog", u"Copy Selected Motions", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.clip_tab), QCoreApplication.translate("Dialog", u"Files", None))
        self.smoothPlotCheckBox.setText(QCoreApplication.translate("Dialog", u"Smooth", None))
        self.plotExperimentButton.setText(QCoreApplication.translate("Dialog", u"Plot Log", None))
        self.exportExperimentButton.setText(QCoreApplication.translate("Dialog", u"Export Log Data", None))
        self.deleteExperimentButton.setText(QCoreApplication.translate("Dialog", u"Delete Experiment", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.experiment_tab), QCoreApplication.translate("Dialog", u"Experiments", None))
    # retranslateUi

