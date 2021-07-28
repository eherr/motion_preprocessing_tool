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

from PySide2.QtWidgets import QDialog, QAbstractItemView, QListWidgetItem
from tool.core.layout.select_joints_dialog_ui import Ui_Dialog


class SelectJointsDialog(QDialog, Ui_Dialog):
    def __init__(self, skeleton, parent=None):
        QDialog.__init__(self, parent)
        Ui_Dialog.setupUi(self, self)
        self.skeleton = skeleton
        self.jointList.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.fill_joints_list()
        self.selectButton.clicked.connect(self.slot_accept)
        self.cancelButton.clicked.connect(self.slot_reject)

        self.success = False
        self.selected_joints = []

    def fill_joints_list(self):
        self.jointList.clear()
        joints = list(self.skeleton.nodes.keys())
        for idx, joint_name in enumerate(joints):
            item = QListWidgetItem()
            item.setText(joint_name)
            self.jointList.addItem(item)

    def get_selected_joints(self):
        joints = []
        for row_idx in range(self.jointList.count()):
            name_cell = self.jointList.item(row_idx)
            if name_cell.isSelected():
                label = str(name_cell.text())
                joints.append(label)
        return joints

    def slot_accept(self):
        selected_joints = self.get_selected_joints()
        if len(selected_joints) > 0:
            self.selected_joints = selected_joints
            self.success = True
        self.close()

    def slot_reject(self):
        self.close()
