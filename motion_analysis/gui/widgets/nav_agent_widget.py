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

import numpy as np
from PySide2.QtWidgets import QWidget
from motion_analysis.gui.layout.nav_agent_widget_ui import Ui_NavAgentWidget
from motion_analysis.gui.dialogs.select_scene_objects_dialog import SelectSceneObjectsDialog
from motion_analysis.gui.dialogs.utils import get_constraints


class NavAgentWidget(QWidget, Ui_NavAgentWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        Ui_NavAgentWidget.setupUi(self, self)
        self.nav_agent = None
        self.SelectWalkTargetButton.pressed.connect(self.set_walk_target)
        self.removeWalkTargetButton.pressed.connect(self.remove_walk_target)
        self.performActionButton.pressed.connect(self.perform_action)
        self.actionComboBox.currentTextChanged.connect(self.update_keyframe_combobox)
        self.toleranceLineEdit.returnPressed.connect(self.set_tolerance)

    def set_object(self, scene_object):
        if scene_object is not None and scene_object.has_component("nav_agent"):
            self.nav_agent = scene_object._components["nav_agent"]
            self.fill_action_combobox()
            action_name = str(self.actionComboBox.currentText())
            self.fill_keyframe_combobox(action_name)
            self.toleranceLineEdit.setText(str(self.nav_agent.tolerance))

    def fill_action_combobox(self):
        self.actionComboBox.clear()
        for action in self.nav_agent.get_actions():
            self.actionComboBox.addItem(action)

    def fill_keyframe_combobox(self, action):
        self.keyframeComboBox.clear()
        for keyframe_label in self.nav_agent.get_keyframe_labels(action):
            self.keyframeComboBox.addItem(keyframe_label)

    def set_walk_target(self):
        set_constraint_dialog = SelectSceneObjectsDialog(self.nav_agent.scene_object.scene, get_constraints)
        set_constraint_dialog.exec_()
        if set_constraint_dialog.success:
            constraint_object = self.nav_agent.scene_object.scene.getObject(set_constraint_dialog.selected_node_id)
            self.nav_agent.set_walk_target(constraint_object)

    def remove_walk_target(self):
        self.nav_agent.remove_walk_target()

    def perform_action(self):
        position = None
        keyframe_label = None
        action_name = str(self.actionComboBox.currentText())
        if self.keyframeComboBox.count() > 0:
            set_constraint_dialog = SelectSceneObjectsDialog(self.nav_agent.scene_object.scene, get_constraints)
            set_constraint_dialog.exec_()
            if set_constraint_dialog.success:
                constraint_object = self.nav_agent.scene_object.scene.getObject(set_constraint_dialog.selected_node_id)
                keyframe_label = str(self.keyframeComboBox.currentText())
                position = constraint_object.getPosition()
        self.nav_agent.perform_action(action_name, keyframe_label, position)

    def update_keyframe_combobox(self, label):
        self.fill_keyframe_combobox(str(label))

    def set_tolerance(self):
        self.nav_agent.tolerance = float(self.toleranceLineEdit.text())



