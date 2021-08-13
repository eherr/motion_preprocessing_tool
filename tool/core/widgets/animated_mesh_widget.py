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
import numpy as np
from PySide2.QtWidgets import  QWidget, QAction
from tool.core.layout.animated_mesh_widget_ui import Ui_Form
from tool.core.widget_manager import WidgetManager


class AnimatedMeshWidget(QWidget, Ui_Form):
    COMPONENT_NAME = "animated_mesh"
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        Ui_Form.setupUi(self, self)
        self._init_actions()
        self._init_signals()
        self._init_slots()
        self._animated_mesh = None
        self.visibleCheckBox.stateChanged.connect(self.on_click_visible)

    def set_object(self, scene_object):
        if scene_object is None or self.COMPONENT_NAME not in scene_object._components:
            return
        animated_mesh = scene_object._components[self.COMPONENT_NAME]
        if animated_mesh is not None:
            self.scaleLineEdit.setText("1")
            self._animated_mesh = animated_mesh
            self.init_render_mode_combo_box()
            if self._animated_mesh.visible:
                self.visibleCheckBox.setChecked(True)
            else:
                self.visibleCheckBox.setChecked(False)

    def _init_actions(self):
        self.applyScaleAction = QAction("Apply", self)
        self.applyScaleAction.triggered.connect(self._apply_scale)

    def _init_signals(self):
        self.applyScaleButton.setDefaultAction(self.applyScaleAction)

    def _init_slots(self):
        return

    def _apply_scale(self):
        if self._animated_mesh is not None:
            scale = float(self.scaleLineEdit.text())
            self._animated_mesh.scale_mesh(scale)

    def on_click_visible(self):
        new_visible = self.visibleCheckBox.isChecked()
        self._animated_mesh.visible = new_visible

    def render_mode_selection_changed(self, idx):
        if self._animated_mesh is not None:
            self._animated_mesh.render_mode = idx

    def init_render_mode_combo_box(self):
        self.renderModeComboBox.clear()
        self.renderModeComboBox.addItem("None", 0)
        self.renderModeComboBox.addItem("Standard", 1)
        self.renderModeComboBox.addItem("Normal Map", 2)
        self.renderModeComboBox.setCurrentIndex(1)
        self.renderModeComboBox.currentIndexChanged.connect(self.render_mode_selection_changed)


WidgetManager.register("animated_mesh", AnimatedMeshWidget)