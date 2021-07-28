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
from PySide2.QtWidgets import QWidget,QAction, QTableWidgetItem, QHBoxLayout, QLabel, QDoubleSpinBox, QSlider, QFileDialog
from PySide2.QtCore import Qt
from .layout.blend_animation_player_widget_ui import Ui_Form
from tool.core.widgets.group_animation_controller_widget import GroupAnimationPlayerBaseWidget


class BlendAnimationControllerWidget(GroupAnimationPlayerBaseWidget, Ui_Form):
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
        self._layouts = []
        self._sliders = []
        self._labels = []
        self._spin_boxes = []
        self.init_combo_box()

    def set_object(self, controller):
        for idx, h in enumerate(self._layouts):
            h.removeWidget(self._sliders[idx])
            self._sliders[idx].deleteLater()
            h.removeWidget(self._spin_boxes[idx])
            self._spin_boxes[idx].deleteLater()
            h.removeWidget(self._labels[idx])
            self._labels[idx].deleteLater()
            self.parameterSliderLayout.removeItem(h)
            h.deleteLater()
        self._layouts = []
        self._sliders = []
        self._spin_boxes = []
        self._labels = []
        self._controller = controller
        if self._controller is not None:
            self.activatePlayerControls()
            n_frames = controller.getNumberOfFrames()
            self.setFrameRange(0, n_frames - 1)
            self.neighborLineEdit.setText(str(controller.n_neighbors))
            parameter = controller.current_parameter
            min_pos, max_pos = controller.get_parameter_range()
            for idx, label in enumerate(controller.get_parameter_labels()):
                print ("add parameter", label, min_pos[idx], max_pos[idx])
                h_layout = QHBoxLayout()
                parameter_label = QLabel()
                parameter_label.setText(label)
                h_layout.addWidget(parameter_label)
                parameter_slider = QSlider()
                parameter_slider.setOrientation(Qt.Horizontal)
                parameter_slider.setRange(min_pos[idx] * 100, max_pos[idx] * 100)
                if parameter is not None:
                    parameter_slider.setValue(parameter[idx] * 100)
                h_layout.addWidget(parameter_slider)
                parameter_spin_box = QDoubleSpinBox()
                parameter_spin_box.setRange(min_pos[idx], max_pos[idx])
                if parameter is not None:
                    parameter_spin_box.setValue(parameter[idx])
                h_layout.addWidget(parameter_spin_box)
                self.parameterSliderLayout.addLayout(h_layout)
                parameter_slider.valueChanged.connect(self.parameter_changed)
                parameter_spin_box.valueChanged.connect(self.update_parameter_from_spin_box)
                self._sliders.append(parameter_slider)
                self._spin_boxes.append(parameter_spin_box)
                self._labels.append(parameter_label)
                self._layouts.append(h_layout)
            self.update_animation_controller_list()

    def update_animation_controller_list(self):
        self.animationControllerTableWidget.setRowCount(0)
        if self._controller is None:
            return
        positions = self._controller.get_blend_positions()
        for name, position in positions.items():
            row = self.animationControllerTableWidget.rowCount()
            self.animationControllerTableWidget.insertRow(row)
            name_item = QTableWidgetItem(str(name))
            position_item = QTableWidgetItem(str(position))
            self.animationControllerTableWidget.setItem(row, 0, name_item)
            self.animationControllerTableWidget.setItem(row, 1, position_item)

    def init_animation_player_actions(self):
        self.toggle_animation_action = QAction("Play", self)
        self.toggle_animation_action.setShortcut('Space')
        self.toggle_animation_action.triggered.connect(self.toggle_animation)
        self.save_action = QAction("Save To File", self)
        self.save_action.triggered.connect(self.save_to_file)
        self.export_action = QAction("Export To BVH", self)
        self.export_action.triggered.connect(self.export_to_bvh_file)

    def initSignals(self):
        self.animationButton.setDefaultAction(self.toggle_animation_action)
        self.saveToFileButton.setDefaultAction(self.save_action)
        self.exportToBVHButton.setDefaultAction(self.export_action)

    def initSlots(self):
        self.loopAnimationCheckBox.clicked.connect(self.toggle_animation_loop)
        self.animationFrameSpinBox.valueChanged.connect(self.update_animation_time_from_spinbox)
        self.animationSpeedDoubleSpinBox.valueChanged.connect(self.set_speed)
        self.animationFrameSlider.valueChanged.connect(self.frame_changed)
        self.neighborLineEdit.textChanged.connect(self.update_n_neighbors)

    def parameter_changed(self, value):
        parameter = np.zeros(self._controller.get_n_parameters())
        for idx, slider in enumerate(self._sliders):
            v = float(slider.value()) / 100
            parameter[idx] = v
            self._spin_boxes[idx].setValue(v)
        self._controller.set_blend_parameter(parameter)

    def update_parameter_from_spin_box(self, value):
        value = int(value * 100)
        self.parameter_changed(value)

    def update_n_neighbors(self, value):
        n_neighbors = int(value)
        self._controller.set_n_neighbors(n_neighbors)

    def init_combo_box(self):
        self.drawModeComboBox.clear()
        self.drawModeComboBox.addItem("None", 0)
        self.drawModeComboBox.addItem("Lines", 1)
        self.drawModeComboBox.addItem("Boxes", 2)
        self.drawModeComboBox.addItem("CoordinateSystem", 3)
        self.drawModeComboBox.setCurrentIndex(1)
        self.drawModeComboBox.currentIndexChanged.connect(self.draw_mode_selection_changed)

    def draw_mode_selection_changed(self, idx):
        self._controller._visualization.draw_mode = int(idx)

    def save_to_file(self):
        filename = str(QFileDialog.getSaveFileName(self, 'Save To File', '.'))[0]
        self._controller.save_to_file(filename)

    def export_to_bvh_file(self):
        filename = str(QFileDialog.getSaveFileName(self, 'Save To File', '.'))[0]
        self._controller.export_to_bvh_file(filename)

