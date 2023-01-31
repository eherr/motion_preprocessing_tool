# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'motion_db_browser_dialog.ui'
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
        Dialog.resize(859, 404)
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
        self.clip_tab = QWidget()
        self.clip_tab.setObjectName(u"clip_tab")
        self.gridLayout = QGridLayout(self.clip_tab)
        self.gridLayout.setObjectName(u"gridLayout")
        self.processedMotionListWidget = QListWidget(self.clip_tab)
        self.processedMotionListWidget.setObjectName(u"processedMotionListWidget")

        self.gridLayout.addWidget(self.processedMotionListWidget, 0, 0, 1, 1)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer)

        self.selectButton = QPushButton(self.clip_tab)
        self.selectButton.setObjectName(u"selectButton")

        self.horizontalLayout_2.addWidget(self.selectButton)

        self.deleteMotionButton = QPushButton(self.clip_tab)
        self.deleteMotionButton.setObjectName(u"deleteMotionButton")

        self.horizontalLayout_2.addWidget(self.deleteMotionButton)


        self.gridLayout.addLayout(self.horizontalLayout_2, 1, 0, 1, 1)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalSpacer2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer2)

        self.importCollectionButton = QPushButton(self.clip_tab)
        self.importCollectionButton.setObjectName(u"importCollectionButton")

        self.horizontalLayout_3.addWidget(self.importCollectionButton)

        self.exportCollectionButton = QPushButton(self.clip_tab)
        self.exportCollectionButton.setObjectName(u"exportCollectionButton")

        self.horizontalLayout_3.addWidget(self.exportCollectionButton)


        self.gridLayout.addLayout(self.horizontalLayout_3, 2, 0, 1, 1)

        self.horizontalLayout_32 = QHBoxLayout()
        self.horizontalLayout_32.setObjectName(u"horizontalLayout_32")
        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_32.addItem(self.horizontalSpacer_3)

        self.alignMotionsButton = QPushButton(self.clip_tab)
        self.alignMotionsButton.setObjectName(u"alignMotionsButton")

        self.horizontalLayout_32.addWidget(self.alignMotionsButton)


        self.gridLayout.addLayout(self.horizontalLayout_32, 3, 0, 1, 1)

        self.horizontalLayout_34 = QHBoxLayout()
        self.horizontalLayout_34.setObjectName(u"horizontalLayout_34")
        self.horizontalSpacer_8 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_34.addItem(self.horizontalSpacer_8)

        self.setTimeFunctionButton = QPushButton(self.clip_tab)
        self.setTimeFunctionButton.setObjectName(u"setTimeFunctionButton")

        self.horizontalLayout_34.addWidget(self.setTimeFunctionButton)

        self.editMotionsButton = QPushButton(self.clip_tab)
        self.editMotionsButton.setObjectName(u"editMotionsButton")

        self.horizontalLayout_34.addWidget(self.editMotionsButton)

        self.retargetMotionsButton = QPushButton(self.clip_tab)
        self.retargetMotionsButton.setObjectName(u"retargetMotionsButton")

        self.horizontalLayout_34.addWidget(self.retargetMotionsButton)

        self.copyMotionsButton = QPushButton(self.clip_tab)
        self.copyMotionsButton.setObjectName(u"copyMotionsButton")

        self.horizontalLayout_34.addWidget(self.copyMotionsButton)


        self.gridLayout.addLayout(self.horizontalLayout_34, 4, 0, 1, 1)

        self.tabWidget.addTab(self.clip_tab, "")
        self.processedMotionListWidget.raise_()
        self.aligned_tab = QWidget()
        self.aligned_tab.setObjectName(u"aligned_tab")
        self.verticalLayout_3 = QVBoxLayout(self.aligned_tab)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.alignedMotionListWidget = QListWidget(self.aligned_tab)
        self.alignedMotionListWidget.setObjectName(u"alignedMotionListWidget")

        self.verticalLayout_3.addWidget(self.alignedMotionListWidget)

        self.horizontalLayout_8 = QHBoxLayout()
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.horizontalSpacer_10 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_8.addItem(self.horizontalSpacer_10)

        self.selectAlignedMotionButton = QPushButton(self.aligned_tab)
        self.selectAlignedMotionButton.setObjectName(u"selectAlignedMotionButton")

        self.horizontalLayout_8.addWidget(self.selectAlignedMotionButton)

        self.deleteAlignedMotionButton = QPushButton(self.aligned_tab)
        self.deleteAlignedMotionButton.setObjectName(u"deleteAlignedMotionButton")

        self.horizontalLayout_8.addWidget(self.deleteAlignedMotionButton)


        self.verticalLayout_3.addLayout(self.horizontalLayout_8)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalSpacer_9 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_5.addItem(self.horizontalSpacer_9)

        self.createMotionModelButton = QPushButton(self.aligned_tab)
        self.createMotionModelButton.setObjectName(u"createMotionModelButton")

        self.horizontalLayout_5.addWidget(self.createMotionModelButton)


        self.verticalLayout_3.addLayout(self.horizontalLayout_5)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalSpacer_5 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer_5)

        self.exportAlignedCollectionButton = QPushButton(self.aligned_tab)
        self.exportAlignedCollectionButton.setObjectName(u"exportAlignedCollectionButton")

        self.horizontalLayout_4.addWidget(self.exportAlignedCollectionButton)

        self.retargetAlignedMotionsButton = QPushButton(self.aligned_tab)
        self.retargetAlignedMotionsButton.setObjectName(u"retargetAlignedMotionsButton")

        self.horizontalLayout_4.addWidget(self.retargetAlignedMotionsButton)


        self.verticalLayout_3.addLayout(self.horizontalLayout_4)

        self.tabWidget.addTab(self.aligned_tab, "")
        self.model_tab = QWidget()
        self.model_tab.setObjectName(u"model_tab")
        self.gridLayout_2 = QGridLayout(self.model_tab)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.modelListWidget = QListWidget(self.model_tab)
        self.modelListWidget.setObjectName(u"modelListWidget")

        self.gridLayout_2.addWidget(self.modelListWidget, 0, 0, 1, 1)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_2)

        self.downloadMotionModelButton = QPushButton(self.model_tab)
        self.downloadMotionModelButton.setObjectName(u"downloadMotionModelButton")

        self.horizontalLayout.addWidget(self.downloadMotionModelButton)

        self.deleteMotionModelButton = QPushButton(self.model_tab)
        self.deleteMotionModelButton.setObjectName(u"deleteMotionModelButton")

        self.horizontalLayout.addWidget(self.deleteMotionModelButton)


        self.gridLayout_2.addLayout(self.horizontalLayout, 1, 0, 1, 1)

        self.horizontalLayout_33 = QHBoxLayout()
        self.horizontalLayout_33.setObjectName(u"horizontalLayout_33")
        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_33.addItem(self.horizontalSpacer_4)

        self.importMotionModelButton = QPushButton(self.model_tab)
        self.importMotionModelButton.setObjectName(u"importMotionModelButton")

        self.horizontalLayout_33.addWidget(self.importMotionModelButton)

        self.exportMotionModelButton = QPushButton(self.model_tab)
        self.exportMotionModelButton.setObjectName(u"exportMotionModelButton")

        self.horizontalLayout_33.addWidget(self.exportMotionModelButton)


        self.gridLayout_2.addLayout(self.horizontalLayout_33, 2, 0, 1, 1)

        self.horizontalLayout_323 = QHBoxLayout()
        self.horizontalLayout_323.setObjectName(u"horizontalLayout_323")
        self.horizontalSpacer_31 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_323.addItem(self.horizontalSpacer_31)

        self.createClusterTreeButton = QPushButton(self.model_tab)
        self.createClusterTreeButton.setObjectName(u"createClusterTreeButton")

        self.horizontalLayout_323.addWidget(self.createClusterTreeButton)

        self.exportClusterTreeJSONButton = QPushButton(self.model_tab)
        self.exportClusterTreeJSONButton.setObjectName(u"exportClusterTreeJSONButton")

        self.horizontalLayout_323.addWidget(self.exportClusterTreeJSONButton)

        self.exportClusterTreePCKButton = QPushButton(self.model_tab)
        self.exportClusterTreePCKButton.setObjectName(u"exportClusterTreePCKButton")

        self.horizontalLayout_323.addWidget(self.exportClusterTreePCKButton)


        self.gridLayout_2.addLayout(self.horizontalLayout_323, 3, 0, 1, 1)

        self.tabWidget.addTab(self.model_tab, "")
        self.splitter.addWidget(self.tabWidget)

        self.gridLayout_3.addWidget(self.splitter, 3, 0, 1, 1)

        self.horizontalLayout_31 = QHBoxLayout()
        self.horizontalLayout_31.setObjectName(u"horizontalLayout_31")
        self.horizontalSpacer21 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_31.addItem(self.horizontalSpacer21)

        self.useComputeClusterCheckBox = QCheckBox(Dialog)
        self.useComputeClusterCheckBox.setObjectName(u"useComputeClusterCheckBox")

        self.horizontalLayout_31.addWidget(self.useComputeClusterCheckBox)

        self.debugInfoButton = QPushButton(Dialog)
        self.debugInfoButton.setObjectName(u"debugInfoButton")

        self.horizontalLayout_31.addWidget(self.debugInfoButton)

        self.exportDatabaseButton = QPushButton(Dialog)
        self.exportDatabaseButton.setObjectName(u"exportDatabaseButton")

        self.horizontalLayout_31.addWidget(self.exportDatabaseButton)

        self.generateMGFromFIleButton = QPushButton(Dialog)
        self.generateMGFromFIleButton.setObjectName(u"generateMGFromFIleButton")

        self.horizontalLayout_31.addWidget(self.generateMGFromFIleButton)


        self.gridLayout_3.addLayout(self.horizontalLayout_31, 4, 0, 1, 1)


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
        ___qtreewidgetitem = self.collectionTreeWidget.headerItem()
        ___qtreewidgetitem.setText(1, QCoreApplication.translate("Dialog", u"Type", None));
        ___qtreewidgetitem.setText(0, QCoreApplication.translate("Dialog", u"Name", None));
        self.addCollectionButton.setText(QCoreApplication.translate("Dialog", u"Add Collection", None))
        self.editCollectionButton.setText(QCoreApplication.translate("Dialog", u"Edit Collection", None))
        self.deleteCollectionButton.setText(QCoreApplication.translate("Dialog", u"Delete Collection", None))
        self.selectButton.setText(QCoreApplication.translate("Dialog", u"Load Selected Motions into Scene", None))
        self.deleteMotionButton.setText(QCoreApplication.translate("Dialog", u"Delete Selected Motions", None))
        self.importCollectionButton.setText(QCoreApplication.translate("Dialog", u"Import Collection from Folder", None))
        self.exportCollectionButton.setText(QCoreApplication.translate("Dialog", u"Export Collection To Folder", None))
        self.alignMotionsButton.setText(QCoreApplication.translate("Dialog", u"Align Motion Clips", None))
        self.setTimeFunctionButton.setText(QCoreApplication.translate("Dialog", u"Set Time Function", None))
        self.editMotionsButton.setText(QCoreApplication.translate("Dialog", u"Edit Selected Motions", None))
        self.retargetMotionsButton.setText(QCoreApplication.translate("Dialog", u"Retarget Selected Motions", None))
        self.copyMotionsButton.setText(QCoreApplication.translate("Dialog", u"Copy Selected Motions", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.clip_tab), QCoreApplication.translate("Dialog", u"Motion Clips", None))
        self.selectAlignedMotionButton.setText(QCoreApplication.translate("Dialog", u"Load Selected Motions into Scene", None))
        self.deleteAlignedMotionButton.setText(QCoreApplication.translate("Dialog", u"Delete Selected Motions", None))
        self.createMotionModelButton.setText(QCoreApplication.translate("Dialog", u"Create Motion Model", None))
        self.exportAlignedCollectionButton.setText(QCoreApplication.translate("Dialog", u"Export Collection", None))
        self.retargetAlignedMotionsButton.setText(QCoreApplication.translate("Dialog", u"Retarget Selected Motions", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.aligned_tab), QCoreApplication.translate("Dialog", u"Aligned Motion Clips", None))
        self.downloadMotionModelButton.setText(QCoreApplication.translate("Dialog", u"Load Motion Model into scene", None))
        self.deleteMotionModelButton.setText(QCoreApplication.translate("Dialog", u"Delete Selected Model", None))
        self.importMotionModelButton.setText(QCoreApplication.translate("Dialog", u"Import Motion Model", None))
        self.exportMotionModelButton.setText(QCoreApplication.translate("Dialog", u"Export Motion Model", None))
        self.createClusterTreeButton.setText(QCoreApplication.translate("Dialog", u"Create Cluster Tree", None))
        self.exportClusterTreeJSONButton.setText(QCoreApplication.translate("Dialog", u"Export Cluster Tree To JSON ", None))
        self.exportClusterTreePCKButton.setText(QCoreApplication.translate("Dialog", u"Export Cluster Tree To Pickle ", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.model_tab), QCoreApplication.translate("Dialog", u"Motion Models", None))
        self.useComputeClusterCheckBox.setText(QCoreApplication.translate("Dialog", u"Use Kubernetes", None))
        self.debugInfoButton.setText(QCoreApplication.translate("Dialog", u"Print Debug Info", None))
        self.exportDatabaseButton.setText(QCoreApplication.translate("Dialog", u"Export Database To Folder", None))
        self.generateMGFromFIleButton.setText(QCoreApplication.translate("Dialog", u"Generate Morphable Graph ", None))
    # retranslateUi

