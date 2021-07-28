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
from PySide2.QtWidgets import  QWidget, QFileDialog
from .layout.mg_state_machine_widget_ui import Ui_MGStateMachineWidget
import numpy as np


class MGStateMachineWidget(QWidget, Ui_MGStateMachineWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        Ui_MGStateMachineWidget.setupUi(self, self)
        self.mg_controller = None
        self.stateDisplay.text = ""
        self.dirXLineEdit.returnPressed.connect(self.set_direction_vector)
        self.dirZLineEdit.returnPressed.connect(self.set_direction_vector)
        self.animSpeedLineEdit.returnPressed.connect(self.set_animation_speed)
        self.blendWindowLineEdit.returnPressed.connect(self.set_blend_window)
        self.posWeightLineEdit.returnPressed.connect(self.set_position_weight)
        self.dirWeightLineEdit.returnPressed.connect(self.set_direction_weight)

        self.activateIKCheckBox.stateChanged.connect(self.set_ik)
        self.groundingCheckBox.stateChanged.connect(self.set_grounding)
        self.transitionConstraintCheckBox.stateChanged.connect(self.set_transition_constraint)

    def set_object(self, scene_object):
        if scene_object is not None and scene_object.has_component("morphablegraph_state_machine"):
            self.mg_controller = scene_object._components["morphablegraph_state_machine"]
            self.stateDisplay.setText(self.mg_controller.current_node[1])
            self.dirXLineEdit.setText(str(self.mg_controller.direction_vector[0]))
            self.dirZLineEdit.setText(str(self.mg_controller.direction_vector[2]))
            self.animSpeedLineEdit.setText(str(self.mg_controller.speed))
            self.posWeightLineEdit.setText(str(self.mg_controller.planner.settings.position_constraint_weight))
            self.dirWeightLineEdit.setText(str(self.mg_controller.planner.settings.direction_constraint_weight))

            self.activateIKCheckBox.setChecked(self.mg_controller.planner.settings.activate_ik)
            self.groundingCheckBox.setChecked(self.mg_controller.activate_grounding)
            self.transitionConstraintCheckBox.setChecked(self.mg_controller.planner.settings.add_transition_constraint)

    def set_direction_vector(self):
        x = float(self.dirXLineEdit.text())
        z = float(self.dirZLineEdit.text())
        dir_vector = np.array([x,0,z])
        dir_vector /= np.linalg.norm(dir_vector)
        self.mg_controller.direction_vector = dir_vector

    def set_animation_speed(self):
        speed = float(self.animSpeedLineEdit.text())
        self.mg_controller.speed = speed

    def set_blend_window(self):
        blend_window = int(self.blendWindowLineEdit.text())
        self.mg_controller.planner.settings.blend_window = blend_window

    def set_ik(self, state):
        self.mg_controller.planner.settings.activate_ik = bool(state)

    def set_grounding(self, state):
        self.mg_controller.activate_grounding = bool(state)

    def set_transition_constraint(self, state):
        self.mg_controller.planner.settings.add_transition_constraint = bool(state)

    def set_position_weight(self):
        self.mg_controller.planner.settings.position_constraint_weight = float(self.posWeightLineEdit.text())

    def set_direction_weight(self):
        self.mg_controller.planner.settings.direction_constraint_weight = float(self.dirWeightLineEdit.text())





