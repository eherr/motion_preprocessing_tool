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
from PySide2.QtWidgets import QWidget, QTableWidgetItem
from motion_analysis.gui.layout.figure_controller_widget_ui import Ui_FigureControllerWidget


class FigureControllerWidget(QWidget, Ui_FigureControllerWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        Ui_FigureControllerWidget.setupUi(self, self)
        self._figure_controller = None
        self.controlModeComboBox.currentIndexChanged.connect(self.on_changed_mode)
        self.visibleCheckBox.stateChanged.connect(self.on_click_visible)
        self.kinematicRootCheckBox.stateChanged.connect(self.on_click_kinematic_root)
        self.externalForceCheckBox.stateChanged.connect(self.on_click_external_force)
        self.balanceCheckBox.stateChanged.connect(self.on_click_balance)

        self.balanceCheckBox.stateChanged.connect(self.on_click_balance)
        self.avScaleLineEdit.returnPressed.connect(self.on_av_scale_changed)
        self.visibleCOMCheckBox.stateChanged.connect(self.on_click_visible_com)
        self.pdGainTableWidget.cellChanged.connect(self.cell_data_changed)
        self.activate_table_edit = False

    def set_object(self, scene_object):
        if scene_object is not None:
            if scene_object.has_component("figure_controller") and scene_object.has_component("character"):
                self._figure_controller = scene_object._components["figure_controller"]
                self.fill_combobox()
                self.activate_table_edit = False
                self.fill_pd_gain_table()
                self.activate_table_edit = True
                self.visibleCheckBox.setChecked(scene_object._components["character"].visible)
                self.kinematicRootCheckBox.setChecked(self._figure_controller.activate_kinematic_root)
                self.externalForceCheckBox.setChecked(self._figure_controller.activate_external_force)
                self.balanceCheckBox.setChecked(self._figure_controller.activate_balance)

    def fill_combobox(self):
        self.controlModeComboBox.clear()
        for idx, action in enumerate(["None", "kinematic", "angular", "pd_controller", "sampling", "cma-es"]):
            self.controlModeComboBox.addItem(action, idx)
        if self._figure_controller.mode > 0:
            self.controlModeComboBox.setCurrentIndex(self._figure_controller.mode)

    def fill_pd_gain_table(self):
        self.pdGainTableWidget.clear()
        self.pdGainTableWidget.setRowCount(0)
        for j in self._figure_controller.pd_gains:
            kp = self._figure_controller.pd_gains[j]["kp"]
            kd = self._figure_controller.pd_gains[j]["kd"]
            row = self.pdGainTableWidget.rowCount()
            self.pdGainTableWidget.insertRow(row)
            self.pdGainTableWidget.setItem(row, 0, QTableWidgetItem(j))
            self.pdGainTableWidget.setItem(row, 1, QTableWidgetItem(str(kp)))
            self.pdGainTableWidget.setItem(row, 2, QTableWidgetItem(str(kd)))

    def cell_data_changed(self, row, col):
        print("data changed", row, col)
        if col < 1 and self.activate_table_edit:
            return
        joint = str(self.pdGainTableWidget.item(row, 0).text())
        value = float(str(self.pdGainTableWidget.item(row, col).text()))
        if col == 1:
            self._figure_controller.pd_gains[joint]["kp"] = value
            print("set kp", joint, self._figure_controller.pd_gains[joint]["kp"])
        elif col == 2:
            self._figure_controller.pd_gains[joint]["kd"] = value
            print("set kd",joint, self._figure_controller.pd_gains[joint]["kd"])

    def on_changed_mode(self, idx):
        self._figure_controller.mode = int(idx)
        if self._figure_controller.mode == 1:
            self._figure_controller.set_kinematic()
        else:
            self._figure_controller.set_dynamic()
            self._figure_controller.reset_motor_targets()

    def on_click_visible(self):
        new_visible = self.visibleCheckBox.isChecked()
        self._figure_controller.scene_object._components["character"].visible = new_visible

    def on_av_scale_changed(self):
        self._figure_controller.av_scale = float(self.avScaleLineEdit.text())

    def on_click_visible_com(self):
        new_visible = self.visibleCOMCheckBox.isChecked()
        self._figure_controller.visualize_com = new_visible

    def on_click_kinematic_root(self):
        self._figure_controller.activate_kinematic_root = self.kinematicRootCheckBox.isChecked()
        if not self._figure_controller.activate_kinematic_root:
            root_body = self._figure_controller.target_figure.root_body
            self._figure_controller.target_figure.bodies[root_body].set_dynamic()

    def on_click_external_force(self):
        self._figure_controller.activate_external_force = self.externalForceCheckBox.isChecked()
        if not self._figure_controller.activate_external_force:
            self._figure_controller.reset_motor_targets()

    def on_click_balance(self):
        self._figure_controller.activate_balance = self.balanceCheckBox.isChecked()


