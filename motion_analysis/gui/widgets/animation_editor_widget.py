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

from PySide2.QtWidgets import  QWidget, QAction, QTableWidgetItem
from PySide2.QtCore import Qt
from motion_analysis.gui.layout.animation_editing_widget_ui import Ui_Form
from motion_analysis.gui.dialogs.select_scene_objects_dialog import SelectSceneObjectsDialog
from motion_analysis.gui.dialogs.set_properties_dialog import SetPropertiesDialog
from motion_analysis.gui.dialogs.utils import get_constraints, get_animation_controllers


class AnimationEditorWidget(QWidget, Ui_Form):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        Ui_Form.setupUi(self, self)
        self._init_actions()
        self._init_signals()
        self._animation_editor = None

    def set_object(self, scene_object):
        self._scene_object = scene_object
        if self._scene_object is not None:
            if scene_object.has_component("animation_editor"):
                self._animation_editor = scene_object._components["animation_editor"]
                self.initialize_constraints_list()
                self.fill_joints_combobox()
                self._scene = scene_object.scene

    def initialize_constraints_list(self):
        self.clear_constraints_list()
        self.constraintsTableWidget.setHorizontalHeaderLabels(["Frame", "Joint", "Constraint"])
        constraints = self._animation_editor.get_constraints()
        for row, c in enumerate(constraints):
            frame_idx = c[0]
            joint_name = c[1]
            constraint_name = c[2].name
            self.add_constraint_to_table(frame_idx, joint_name, constraint_name)

    def add_constraint_to_table(self, frame_idx, joint_name, constraint_name):
        row = self.constraintsTableWidget.rowCount()
        self.constraintsTableWidget.insertRow(row)
        item0 = QTableWidgetItem()
        item0.setText(str(frame_idx))
        item0.setData(Qt.UserRole, None)
        self.constraintsTableWidget.setItem(row, 0, item0)
        item1 = QTableWidgetItem()
        item1.setText(str(joint_name))
        item1.setData(Qt.UserRole, None)
        self.constraintsTableWidget.setItem(row, 1, item1)
        item2 = QTableWidgetItem()
        item2.setText(str(constraint_name))
        item2.setData(Qt.UserRole, None)
        self.constraintsTableWidget.setItem(row, 2, item2)

    def clear_constraints_list(self):
        self.constraintsTableWidget.clearContents()
        self.constraintsTableWidget.setRowCount(0)
        self.constraintsTableWidget.setHorizontalHeaderLabels(["Frame", "Joint", "Constraint"])

    def _init_actions(self):
        self.add_constraint_action = QAction("Add Constraint", self)
        self.add_constraint_action.triggered.connect(self.add_constraint)
        self.clear_constraints_action = QAction("Clear Constraints", self)
        self.clear_constraints_action.triggered.connect(self.clear_constraints)
        self.apply_constraints_action = QAction("Apply Constraints", self)
        self.apply_constraints_action.triggered.connect(self.apply_constraints)
        self.undo_edit_action = QAction("Undo Edit", self)
        self.undo_edit_action.triggered.connect(self.undo_edit)

        self.delete_frames_before_action = QAction("Delete Before Slider", self)
        self.delete_frames_before_action.triggered.connect(self.delete_frames_before_slider)

        self.delete_frames_after_action = QAction("Delete After Slider", self)
        self.delete_frames_after_action.triggered.connect(self.delete_frames_after_slider)

        self.translate_frames_action = QAction("Translate", self)
        self.translate_frames_action.triggered.connect(self.translate_frames)

        self.rotate_frames_action = QAction("Rotate", self)
        self.rotate_frames_action.triggered.connect(self.rotate_frames)

        self.detect_ground_contacts_actions = QAction("Detect Ground Contacts", self)
        self.detect_ground_contacts_actions.triggered.connect(self.detect_ground_contacts)

        self.apply_foot_constraints_action = QAction("Apply Foot Constraints", self)
        self.apply_foot_constraints_action.triggered.connect(self.apply_foot_constraints)

        self.move_to_ground_action = QAction("Move To Ground", self)
        self.move_to_ground_action.triggered.connect(self.move_to_ground)

        self.guess_ground_height_action = QAction("Guess Ground Height", self)
        self.guess_ground_height_action.triggered.connect(self.guess_ground_height)

        self.concatenate_action = QAction("Concatenate", self)
        self.concatenate_action.triggered.connect(self.concatenate)

        self.rotate_joint_action = QAction("Rotate Joint", self)
        self.rotate_joint_action.triggered.connect(self.apply_joint_rotation_offset)

        self.smooth_frames_action = QAction("Smoot Frames", self)
        self.smooth_frames_action.triggered.connect(self.smooth_frames)

        self.mirror_animation_action = QAction("Mirror Animation", self)
        self.mirror_animation_action.triggered.connect(self.mirror_animation)

    def _init_signals(self):
        self.addConstraintButton.setDefaultAction(self.add_constraint_action)
        self.clearConstraintsButton.setDefaultAction(self.clear_constraints_action)
        self.applyConstraintsButton.setDefaultAction(self.apply_constraints_action)
        self.undoEditButton.setDefaultAction(self.undo_edit_action)
        self.deleteBeforeButton.setDefaultAction(self.delete_frames_before_action)
        self.deleteAfterButton.setDefaultAction(self.delete_frames_after_action)
        self.translateFramesButton.setDefaultAction(self.translate_frames_action)
        self.rotateFramesButton.setDefaultAction(self.rotate_frames_action)
        self.detectGroundContactButton.setDefaultAction(self.detect_ground_contacts_actions)
        self.applyFootConstraintsButton.setDefaultAction(self.apply_foot_constraints_action)
        self.guessGroundHeightButton.setDefaultAction(self.guess_ground_height_action)
        self.moveToGroundButton.setDefaultAction(self.move_to_ground_action)
        self.concatenateButton.setDefaultAction(self.concatenate_action)
        self.rotateJointButton.setDefaultAction(self.rotate_joint_action)
        self.smoothFramesButton.setDefaultAction(self.smooth_frames_action)
        self.mirrorAnimationButton.setDefaultAction(self.mirror_animation_action)

    def add_constraint(self):
        frame_idx = self._animation_editor._animation_controller.get_current_frame_idx()
        joint_name = str(self.jointComboBox.currentText())
        set_constraints_dialog = SelectSceneObjectsDialog(self._scene, get_constraints, self)
        set_constraints_dialog.exec_()
        if set_constraints_dialog.success:
            constraint_object = self._scene.getObject(set_constraints_dialog.selected_node_id)
            if constraint_object is not None:
                self._animation_editor.add_constraint(frame_idx, joint_name, constraint_object)
                self.add_constraint_to_table(frame_idx, joint_name, constraint_object.name)

    def clear_constraints(self):
        self._animation_editor.clear_constraints()
        self.clear_constraints_list()

    def apply_constraints(self):
        plot_curve = self.plotCheckBox.isChecked()
        self._animation_editor.apply_constraints(plot_curve)

    def undo_edit(self):
        self._animation_editor.undo_edit()

    def fill_joints_combobox(self):
        self.jointComboBox.clear()
        self.jointRotationComboBox.clear()
        joints = self._animation_editor.get_skeleton().get_joint_names()
        for idx, joint in enumerate(joints):
            self.jointComboBox.addItem(joint, idx)
            self.jointRotationComboBox.addItem(joint, idx)

    def translate_frames(self):
        x = float(self.translateXLineEdit.text())
        y = float(self.translateYLineEdit.text())
        z = float(self.translateZLineEdit.text())
        self._animation_editor.translate_frames([x, y, z])

    def rotate_frames(self):
        x = float(self.rotateXLineEdit.text())
        y = float(self.rotateYLineEdit.text())
        z = float(self.rotateZLineEdit.text())
        self._animation_editor.rotate_frames([x, y, z])

    def guess_ground_height(self):
        source_ground_height = self._animation_editor.guess_ground_height()
        self.sourceGroundHeightLineEdit.setText(str(source_ground_height))

    def move_to_ground(self):
        source_ground_height = float(self.sourceGroundHeightLineEdit.text())
        target_ground_height = float(self.targetGroundHeightLineEdit.text())
        self._animation_editor.move_to_ground(source_ground_height, target_ground_height)

    def detect_ground_contacts(self):
        print("detect ground contacts")
        source_ground_height = float(self.sourceGroundHeightLineEdit.text())
        self._animation_editor.detect_ground_contacts(source_ground_height)

    def apply_foot_constraints(self):
        print("run grounding")
        target_ground_height = float(self.targetGroundHeightLineEdit.text())
        self._animation_editor.apply_foot_constraints(target_ground_height)

    def delete_frames_before_slider(self):
        frame_idx = self._animation_editor.get_current_frame_number()
        self._animation_editor.delete_frames_before(frame_idx)

    def delete_frames_after_slider(self):
        frame_idx = self._animation_editor.get_current_frame_number()
        self._animation_editor.delete_frames_after(frame_idx)

    def concatenate(self):
        options = dict()
        options["activate_smoothing"] = True
        options["window"] = 20
        select_animation_dialog = SelectSceneObjectsDialog(self._scene, get_animation_controllers, self, name="Concatenate", properties=options)
        select_animation_dialog.exec_()
        if select_animation_dialog.success:
            o = self._scene.getObject(select_animation_dialog.selected_node_id)
            options = select_animation_dialog.properties
            animation_controller = o._components["animation_controller"]
            self._animation_editor.concatenate(animation_controller, options["activate_smoothing"], options["window"])


    def apply_joint_rotation_offset(self):
        joint_name = str(self.jointRotationComboBox.currentText())
        x = float(self.rotateJointXLineEdit.text())
        y = float(self.rotateJointYLineEdit.text())
        z = float(self.rotateJointZLineEdit.text())
        self._animation_editor.apply_joint_rotation_offset(joint_name, [x,y,z])


    def smooth_frames(self):
        window_size = int(self.smoothWindowSizeLineEdit.text())
        if window_size >= 5:
            print("smooth frames using a window size of", window_size)
            self._animation_editor.smooth_using_moving_average(window_size)
        else:
            print("Error: window size must be >= 5")

        
    def mirror_animation(self):
        self._animation_editor.mirror_animation()


