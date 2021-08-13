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
from PySide2.QtWidgets import QWidget, QListWidgetItem, QAction
from tool.core.layout.group_animation_player_widget_ui import Ui_Form
from tool.core.widget_manager import WidgetManager
from tool.core.dialogs.select_scene_objects_dialog import SelectSceneObjectsDialog
from tool.core.dialogs.utils import get_animation_controllers

class GroupAnimationPlayerBaseWidget(QWidget):
    COMPONENT_NAME = "group_player"
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)


    def set_object(self, scene_object):
        if scene_object is None or self.COMPONENT_NAME not in scene_object._components:
            return
        self._controller = scene_object._components[self.COMPONENT_NAME]
        
        if self._controller is not None:
            self.activatePlayerControls()
            n_frames = controller.getNumberOfFrames()
            self.setFrameRange(0, n_frames - 1)
            self.update_animation_controller_list()

    def update_animation_controller_list(self):
        self.animationControllerListWidget.clear()
        if self._controller is None:
            return
        for anim_controller in self._controller.get_animation_controllers():
            item = QListWidgetItem()
            item.setText(anim_controller.scene_object.name)
            self.animationControllerListWidget.addItem(item)

    def init_animation_player_actions(self):
        self.toggle_animation_action = QAction("Play", self)
        self.toggle_animation_action.setShortcut('Space')
        self.toggle_animation_action.triggered.connect(self.toggle_animation)

    def init_combo_box(self):
        self.drawModeComboBox.clear()
        self.drawModeComboBox.addItem("None", 0)
        self.drawModeComboBox.addItem("Lines", 1)
        self.drawModeComboBox.addItem("Boxes", 2)
        self.drawModeComboBox.addItem("CoordinateSystem", 3)
        self.drawModeComboBox.setCurrentIndex(1)
        self.drawModeComboBox.currentIndexChanged.connect(self.draw_mode_selection_changed)


    def initSignals(self):
        self.animationButton.setDefaultAction(self.toggle_animation_action)

    def initSlots(self):
        self.loopAnimationCheckBox.clicked.connect(self.toggle_animation_loop)
        self.animationFrameSpinBox.valueChanged.connect(self.update_animation_time_from_spinbox)
        self.animationSpeedDoubleSpinBox.valueChanged.connect(self.set_speed)
        self.animationFrameSlider.valueChanged.connect(self.frame_changed)

    def toggle_animation(self):
        if self._controller is not None:
            if not self._controller.isPlaying():
                self.start_animation()
            else:
                self.stop_animation()

    def update_animation_time_from_spinbox(self, value):
        self.frame_changed(value)

    def frame_changed(self, value):
        if self._controller is not None:
            self._controller.setCurrentFrameNumber(value)
            self.animationFrameSpinBox.setValue(value)

    def toggle_animation_loop(self):
        self._controller.toggle_animation_loop()

    def set_speed(self, value):
        self._controller.setAnimationSpeed(value)

    def start_animation(self):
        self.animationButton.setText("Stop")
        self._controller.startAnimation()

    def stop_animation(self):
        self.animationButton.setText("Play")
        self._controller.stopAnimation()

    def setFrameRange(self, min, max):
        self.animationFrameSlider.setRange(min, max)
        self.animationFrameSpinBox.setRange(min, max)

    def activatePlayerControls(self):
        self.animationFrameSlider.setEnabled(True)
        self.animationFrameSpinBox.setEnabled(True)
        self.animationButton.setEnabled(True)

    def deactivate_player_controls(self):
        self.animationFrameSlider.setEnabled(False)
        self.animationFrameSpinBox.setEnabled(False)
        self.animationButton.setEnabled(False)

    def updateAnimationTimeInGUI(self, value):
        self.setAnimationSliderValue(value)
        self.setAnimationFrameSpinBoxValue(value)

    def setAnimationSliderValue(self, value):
        self.animationFrameSlider.setValue(value)

    def setAnimationFrameSpinBoxValue(self, value):
        self.animationFrameSpinBox.setValue(value)

    def draw_mode_selection_changed(self, idx):
        for anim_controller in self._controller.get_animation_controllers():
            anim_controller._visualization.draw_mode = int(idx)


class GroupAnimationPlayerWidget(GroupAnimationPlayerBaseWidget, Ui_Form):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        Ui_Form.setupUi(self, self)
        self.animationSpeedDoubleSpinBox.setRange(-4.0, 4.0)
        self.deactivate_player_controls()
        self.init_animation_player_actions()
        self.initSignals()
        self.initSlots()
        self.isPlaying = False
        self._controller = None
        self.init_combo_box()



WidgetManager.register("group_player", GroupAnimationPlayerWidget, True)