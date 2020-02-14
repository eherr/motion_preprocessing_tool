#!/usr/bin/env python
#
# Copyright 2019 DFKI GmbH.
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to permit
# persons to whom the Software is furnished to do so, subject to the
# following conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
# OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN
# NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
# DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
# OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE
# USE OR OTHER DEALINGS IN THE SOFTWARE.

from PySide2.QtCore import  Qt
from PySide2.QtGui import QColor
from PySide2.QtWidgets import  QTableWidgetItem, QTableWidget

class AnimationTableEntry(object):
    def __init__(self):
        self.index = -1
        self.name = ""


class SceneObjectTableWidget(QTableWidget):
    def __init__(self, parent=None):
        QTableWidget.__init__(self, parent)

    def addObjectToList(self, sceneId, name, color):
        insertRow = self.rowCount()
        self.insertRow(insertRow)

        indexItem = QTableWidgetItem(str(sceneId))
        indexItem.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
        indexItem.setCheckState(Qt.Checked)

        self.setItem(insertRow, 0, indexItem)
        self.setItem(insertRow, 1, QTableWidgetItem(str(name)))
        self.setItem(insertRow, 2, QTableWidgetItem(""))
        self.item(insertRow, 2).setBackground(QColor(255 * color[0], 255 * color[1], 255 * color[2]))

    def getSelectedAnimations(self):
        animationEntries = []
        for rowIndex in range(self.rowCount()):
            indexCell = self.item(rowIndex,0)
            nameCell = self.item(rowIndex,1)
            if indexCell.isSelected() or nameCell.isSelected():
                entry = AnimationTableEntry()
                entry.index = int(indexCell.text())
                entry.name = str(nameCell.text())
                animationEntries.append(entry)
        return animationEntries

    def getAllAnimations(self):
        animationEntries = []
        for rowIndex in range(self.rowCount()):
            indexCell = self.item(rowIndex,0)
            nameCell = self.item(rowIndex,1)
            entry = AnimationTableEntry()
            entry.index = int(indexCell.text())
            entry.name = str(nameCell.text())
            animationEntries.append(entry)
        return animationEntries

    def updateTable(self):
        for rowIndex in range(self.sceneObjectTableWidget.rowCount()):
            indexItem = QTableWidgetItem(str(rowIndex))
            indexItem.setFlags(Qt.ItemIsUserCheckable |
                               Qt.ItemIsEnabled)
            indexItem.setCheckState(Qt.Unchecked)
            self.sceneObjectTableWidget.setItem(rowIndex, 0, indexItem)

    def getSceneIdFromRow(self, row):
        item = self.item(row, 0)
        #print "row",row,self.item(row, 0).text()
        if item is not None:
            return int(item.text())
        else:
            return -1
