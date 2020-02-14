# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\Research\physics\workspace\mosi_app_mgtools\motion_analysis\GUI\layout\.\mainwindow.ui',
# licensing of 'D:\Research\physics\workspace\mosi_app_mgtools\motion_analysis\GUI\layout\.\mainwindow.ui' applies.
#
# Created: Wed Jan 15 17:42:07 2020
#      by: pyside2-uic  running on PySide2 5.13.1
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1248, 737)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.splitter_2 = QtWidgets.QSplitter(self.centralwidget)
        self.splitter_2.setOrientation(QtCore.Qt.Horizontal)
        self.splitter_2.setObjectName("splitter_2")
        self.gridLayoutWidget_2 = QtWidgets.QWidget(self.splitter_2)
        self.gridLayoutWidget_2.setObjectName("gridLayoutWidget_2")
        self.gl_container = QtWidgets.QGridLayout(self.gridLayoutWidget_2)
        self.gl_container.setContentsMargins(0, 0, -1, -1)
        self.gl_container.setObjectName("gl_container")
        self.animationViewer = SceneViewerWidget(self.gridLayoutWidget_2)
        self.animationViewer.setMinimumSize(QtCore.QSize(640, 480))
        self.animationViewer.setObjectName("animationViewer")
        self.gl_container.addWidget(self.animationViewer, 0, 0, 1, 1)
        self.splitter = QtWidgets.QSplitter(self.splitter_2)
        self.splitter.setOrientation(QtCore.Qt.Vertical)
        self.splitter.setObjectName("splitter")
        self.sceneObjectTableWidget = SceneObjectTableWidget(self.splitter)
        self.sceneObjectTableWidget.setColumnCount(3)
        self.sceneObjectTableWidget.setObjectName("sceneObjectTableWidget")
        self.sceneObjectTableWidget.setColumnCount(3)
        self.sceneObjectTableWidget.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.sceneObjectTableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.sceneObjectTableWidget.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.sceneObjectTableWidget.setHorizontalHeaderItem(2, item)
        self.sceneObjectTableWidget.horizontalHeader().setDefaultSectionSize(50)
        self.sceneObjectTableWidget.horizontalHeader().setMinimumSectionSize(200)
        self.sceneObjectTableWidget.horizontalHeader().setStretchLastSection(True)
        self.objectPropertiesGroupBox = QtWidgets.QGroupBox(self.splitter)
        self.objectPropertiesGroupBox.setObjectName("objectPropertiesGroupBox")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.objectPropertiesGroupBox)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.objectPropertiesLayout = QtWidgets.QGridLayout()
        self.objectPropertiesLayout.setObjectName("objectPropertiesLayout")
        self.gridLayout_2.addLayout(self.objectPropertiesLayout, 0, 0, 1, 1)
        self.gridLayout.addWidget(self.splitter_2, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menuBar = QtWidgets.QMenuBar(MainWindow)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 1248, 21))
        self.menuBar.setObjectName("menuBar")
        MainWindow.setMenuBar(self.menuBar)
        self.statusBar = QtWidgets.QStatusBar(MainWindow)
        self.statusBar.setObjectName("statusBar")
        MainWindow.setStatusBar(self.statusBar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtWidgets.QApplication.translate("MainWindow", "Motion Preprocessing Tool", None, -1))
        self.sceneObjectTableWidget.horizontalHeaderItem(0).setText(QtWidgets.QApplication.translate("MainWindow", "Index", None, -1))
        self.sceneObjectTableWidget.horizontalHeaderItem(1).setText(QtWidgets.QApplication.translate("MainWindow", "Name", None, -1))
        self.sceneObjectTableWidget.horizontalHeaderItem(2).setText(QtWidgets.QApplication.translate("MainWindow", "Color", None, -1))
        self.objectPropertiesGroupBox.setTitle(QtWidgets.QApplication.translate("MainWindow", "Properties", None, -1))

from motion_analysis.gui.widgets.scene_object_table_widget import SceneObjectTableWidget
from motion_analysis.gui.widgets.scene_viewer import SceneViewerWidget
