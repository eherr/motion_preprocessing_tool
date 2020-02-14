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
from functools import partial
from motion_analysis.gui.layout.action_sequence_dialog_ui import Ui_Dialog
from PySide2.QtCore import Qt
from PySide2.QtWidgets import QDialog, QTableWidgetItem, QPushButton
from .add_constraint_dialog import AddConstraintDialog, SelectSceneObjectsDialog, get_constraints


class ActionSequenceDialog(QDialog, Ui_Dialog):
    def __init__(self, scene, controller, parent=None):
        self._parent = parent
        QDialog.__init__(self, parent)
        Ui_Dialog.setupUi(self, self)
        self.acceptButton.clicked.connect(self.slot_accept)
        self.rejectButton.clicked.connect(self.slot_reject)
        self.addButton.clicked.connect(self.add_action_from_combobox)
        self.clearButton.clicked.connect(self.clear_actions)
        self.setStartNodeButton.clicked.connect(self.set_start_node)

        self.success = False
        self._scene = scene
        self._controller = controller
        self._current_constraints = None
        self.start_node_object = None
        self.fill_action_combobox()
        self.initialize_action_sequence_list()

    def initialize_action_sequence_list(self):
        #self.actionTableWidget = QtGui.QTableWidget(0,2)
        self.actionTableWidget.setHorizontalHeaderLabels(["Name", "Constraints"])
        action_sequence = self._parent.get_action_sequence()
        if action_sequence is None:
            return

        for row, action in enumerate(action_sequence):
            action_name = action[0]
            item = self.add_action(action_name)
            item.setData(Qt.UserRole, action[1])

    def fill_action_combobox(self):
        self.actionComboBox.clear()
        for idx, action in enumerate(self._controller.getElementaryActions()):
            self.actionComboBox.addItem(action, idx)

    def add_action_from_combobox(self):
        action_name = str(self.actionComboBox.currentText())
        self.add_action(action_name)

    def add_action(self, action_name):
        row = self.actionTableWidget.rowCount()
        self.actionTableWidget.insertRow(row)
        item = QTableWidgetItem()
        item.setText(str(action_name))
        item.setData(Qt.UserRole, None)
        self.actionTableWidget.setItem(row, 0, item)
        #add button
        self.actionTableWidget.setItem(row, 1, QTableWidgetItem())
        button = QPushButton()
        button.setText("Add Constraint")
        self.actionTableWidget.setCellWidget(row, 1, button)
        func = partial(self.set_constraint_in_row, row)
        button.clicked.connect(func)
        return item

    def clear_actions(self):
        self.actionTableWidget.clearContents()
        self.actionTableWidget.setRowCount(0)
        self.actionTableWidget.setHorizontalHeaderLabels(["Name", "Constraints"])

    def add_constraint(self):
        action_name = str(self.actionComboBox.currentText())
        constraint_definition = self.get_constraint(action_name)
        if constraint_definition is not None:
            self._current_constraints = [constraint_definition]#[self._scene.getObject(.selected_node_id)]


    def set_start_node(self):
        set_constraints_dialog = SelectSceneObjectsDialog(self._scene, get_constraints, self)
        set_constraints_dialog.exec_()
        if set_constraints_dialog.success:
            self.start_node_object = self._scene.getObject(set_constraints_dialog.selected_node_id)

    def set_constraint_in_row(self, row_idx):
        item = self.actionTableWidget.item(row_idx, 0)
        if item is not None:
            action_name = str(item.text())
            constraints = item.data(Qt.UserRole)
            if isinstance(constraints, list):
                prev_constraint = constraints[-1]
            else:
                constraints = []
                prev_constraint = None
            new_constraint = self.get_constraint(action_name, prev_constraint)
            constraints.append(new_constraint)
            print("store",len(constraints), "constraints")
            item.setData(Qt.UserRole, constraints)
            print("set constraint", row_idx, constraints, item.data(Qt.UserRole))

    def get_constraint(self, action_name, constraint):
        set_constraints_dialog = AddConstraintDialog(action_name, self._scene, self._controller, constraint, self)
        set_constraints_dialog.exec_()
        if set_constraints_dialog.success:
            return set_constraints_dialog.constraint_definition

    def get_constrained_actions(self):
        actions = []
        for idx in range(self.actionTableWidget.rowCount()):
            item = self.actionTableWidget.item(idx, 0)
            if item is not None:
                action_name = str(item.text())
                constraints = item.data(Qt.UserRole)
                entry = (action_name, constraints)
                actions.append(entry)
        return actions

    def slot_accept(self):
        actions = self.get_constrained_actions()
        if len(actions) > 0:
            self.success = True
        self.close()

    def slot_reject(self):
        self.close()
