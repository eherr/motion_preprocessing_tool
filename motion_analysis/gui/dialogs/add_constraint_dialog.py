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

from PySide2.QtWidgets import QDialog
from motion_analysis.gui.layout.add_constraint_dialog_ui import Ui_Dialog
from .select_scene_objects_dialog import SelectSceneObjectsDialog
from .utils import get_constraints


class ConstraintDefinition(object):
    def __init__(self, constraint_object, joint_name, annotation=None):
        self.constraint_object = constraint_object
        self.joint_name = joint_name
        self.annotation = annotation


class AddConstraintDialog(QDialog, Ui_Dialog):
    def __init__(self, elementary_action, scene, controller, constraint=None, parent=None):
        QDialog.__init__(self, parent)
        Ui_Dialog.setupUi(self, self)
        self.acceptButton.clicked.connect(self.slot_accept)
        self.rejectButton.clicked.connect(self.slot_reject)
        self.setConstraintButton.clicked.connect(self.get_constraint)
        self._elementary_action = elementary_action
        self._controller = controller
        self._scene = scene
        self.success = False
        if constraint is not None:
            self.fill_joints_combobox(constraint.joint_name)
        else:
            self.fill_joints_combobox()
        self.fill_annotation_combobox()
        self._constraint_object = None
        self.constraint_definition = None

    def fill_joints_combobox(self, selected_joint=None):
        self.jointComboBox.clear()
        joints = self._controller.getJoints()
        selected_idx = 0
        for idx, joint in enumerate(joints):
            self.jointComboBox.addItem(joint, idx)
            if joint == selected_joint:
                selected_idx = idx
        self.jointComboBox.setCurrentIndex(selected_idx)

    def fill_annotation_combobox(self):
        self.annotationComboBox.clear()
        annotations = self._controller.getAnnotations(self._elementary_action)
        for idx, annotation in enumerate(annotations):
            self.annotationComboBox.addItem(annotation, idx)

    def get_constraint(self):
        set_constraints_dialog = SelectSceneObjectsDialog(self._scene, get_constraints, self)
        set_constraints_dialog.exec_()
        if set_constraints_dialog.success:
            self._constraint_object = self._scene.getObject(set_constraints_dialog.selected_node_id)

    def slot_accept(self):
        joint = str(self.jointComboBox.currentText())
        if self.annotationComboBox.count() > 0:
            annotation = str(self.annotationComboBox.currentText())
        else:
            annotation = None
        if self._constraint_object is not None:
            self.constraint_definition = ConstraintDefinition(self._constraint_object, joint, annotation=annotation)
            self.success = True
        self.close()

    def slot_reject(self):
        self.close()
