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
from PySide2.QtWidgets import  QDialog, QListWidgetItem, QTableWidgetItem, QTableWidget
from PySide2.QtCore import Qt
from PySide2.QtGui import QColor
from .layout.motion_modelling_dialog_ui import Ui_Dialog
import numpy as np
import json
from OpenGL.GL import *




class MotionModellingDialog(QDialog, Ui_Dialog):
    def __init__(self, skeleton, name, spline_basis_factor, parent=None):
        QDialog.__init__(self, parent)
        Ui_Dialog.setupUi(self, self)
        self.skeleton = skeleton
        self.animated_joints = self.skeleton.animated_joints
        self.selectButton.clicked.connect(self.slot_accept)
        self.cancelButton.clicked.connect(self.slot_reject)
        self._fill_list_with_joints()

        self.selectAllJointsButton.clicked.connect(self.slot_select_all_joints)
        self.selectJointChildrenButton.clicked.connect(self.slot_select_joint_children)
        self.deselectJointChildrenButton.clicked.connect(self.slot_deselect_joint_children)
        self.clearSelectedJointsButton.clicked.connect(self.slot_clear_all_joints)
        self.selectJointsFromStringButton.clicked.connect(self.slot_set_joints_from_string)
        self.name = name
        self.spline_basis_factor = spline_basis_factor
        self.nameLineEdit.setText(name)
        self.splineBasisFactorLineEdit.setText(str(spline_basis_factor))
        self.success = False

    def get_selected_joints(self):
        joint_list = []
        for row_idx in range(self.jointTableWidget.rowCount()):
            index_cell = self.jointTableWidget.item(row_idx,0)
            if index_cell.checkState() == Qt.Checked:
                name_cell = self.jointTableWidget.item(row_idx,1)
                joint_name = str(name_cell.text())
                joint_list.append(joint_name)
        return joint_list


    def _fill_list_with_joints(self):
        #self.jointTableWidget.clear()
        for joint_name in self.skeleton.animated_joints:
            insertRow = self.jointTableWidget.rowCount()
            self.jointTableWidget.insertRow(insertRow)
            indexItem = QTableWidgetItem("")
            indexItem.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
            indexItem.setCheckState(Qt.Checked)
            self.jointTableWidget.setItem(insertRow, 0, indexItem)
            self.jointTableWidget.setItem(insertRow, 1, QTableWidgetItem(str(joint_name)))

    def slot_accept(self):
        self.success = True
        self.name =  str(self.nameLineEdit.text())
        self.spline_basis_factor = float(self.splineBasisFactorLineEdit.text())
        self.animated_joints  = self.get_selected_joints()
        self.close()

    def slot_reject(self):
        self.close()

    def slot_select_all_joints(self):
        for row_idx in range(self.jointTableWidget.rowCount()):
            index_cell = self.jointTableWidget.item(row_idx,0)
            index_cell.setCheckState(Qt.Checked)

    def slot_clear_all_joints(self):
        for row_idx in range(self.jointTableWidget.rowCount()):
            index_cell = self.jointTableWidget.item(row_idx,0)
            index_cell.setCheckState(Qt.Unchecked)

    def slot_select_joint_children(self):
        for row_idx in range(self.jointTableWidget.rowCount()):
            index_cell = self.jointTableWidget.item(row_idx, 0)
            name_cell = self.jointTableWidget.item(row_idx, 1)
            if index_cell.isSelected() or name_cell.isSelected():
                joint_name = str(name_cell.text())
                self.change_joint_children_state(joint_name, Qt.Checked)

    def slot_deselect_joint_children(self):
        for row_idx in range(self.jointTableWidget.rowCount()):
            index_cell = self.jointTableWidget.item(row_idx, 0)
            name_cell = self.jointTableWidget.item(row_idx, 1)
            if index_cell.isSelected() or name_cell.isSelected():
                joint_name = str(name_cell.text())
                self.change_joint_children_state(joint_name, Qt.Unchecked)
    
    def slot_set_joints_from_string(self):
        joint_list = []
        try:
            joint_list_str =  str(self.jointListLineEdit.text())
            joint_list = json.loads(joint_list_str)
        except Exception as e:
            print("String could not be processed", e.args)
            pass
        for joint in joint_list:
            self.change_joint_state(joint, Qt.Checked)
        return


    def change_joint_children_state(self, joint_name, state):
        self.change_joint_state(joint_name, state)
        if joint_name in self.skeleton.nodes:
            for n in self.skeleton.nodes[joint_name].children:
                self.change_joint_children_state(n.node_name, state)

    def change_joint_state(self, joint_name, state):
        print("select", joint_name)
        for row_idx in range(self.jointTableWidget.rowCount()):
            name_cell = self.jointTableWidget.item(row_idx, 1)
            if joint_name == str(name_cell.text()):
                index_cell = self.jointTableWidget.item(row_idx, 0)
                index_cell.setCheckState(state)
                break

