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
from PySide2.QtWidgets import QWidget
from tool.core.layout.character_widget_ui import Ui_Form
from tool.core.widget_manager import WidgetManager


class CharacterWidget(QWidget, Ui_Form):
    COMPONENT_NAME = "character"
    def __init__(self, parent=None):
        self._parent = parent
        QWidget.__init__(self, parent)
        Ui_Form.setupUi(self, self)
        self._character = None
        self.applyForceButton.clicked.connect(self.apply_force)
        self.applyTorqueButton.clicked.connect(self.apply_torque)
        self.setAngularVelocityButton.clicked.connect(self.set_angular_velocity)
        self.joint_key_map = dict()

    def set_object(self, scene_object):
        if scene_object is None or self.COMPONENT_NAME not in scene_object._components:
            return
        character = scene_object._components[self.COMPONENT_NAME]
        if character is not None:
            self._character = character.articulated_figure
            self.joint_key_map = dict()
            self.bodyComboBox.clear()
            for idx, key in enumerate(self._character.bodies.keys()):
                self.bodyComboBox.addItem(str(key))

            self.jointComboBox.clear()
            for idx, key in enumerate(self._character.joints.keys()):
                self.jointComboBox.addItem(str(key))
                self.joint_key_map[str(key)] = key

    def apply_force(self):
        body_name = str(self.bodyComboBox.currentText())
        force = list(map(float, [self.forceXLineEdit.text(), self.forceYLineEdit.text(), self.forceZLineEdit.text()]))
        self._character.apply_force(body_name, force)

    def apply_torque(self):
        body_name = str(self.bodyComboBox.currentText())
        torque = list(map(float, [self.torqueXLineEdit.text(), self.torqueYLineEdit.text(), self.torqueZLineEdit.text()]))
        self._character.apply_torque(body_name, torque)

    def set_angular_velocity(self):
        joint_name = str(self.jointComboBox.currentText())
        print(joint_name)
        velocity = list(map(float, [self.angularVelocityXLineEdit.text(), self.angularVelocityYLineEdit.text(), self.angularVelocityZLineEdit.text()]))
        self._character.set_angular_velocity(self.joint_key_map[joint_name], velocity)


WidgetManager.register("character", CharacterWidget)

