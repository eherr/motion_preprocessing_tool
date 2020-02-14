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
import json
from copy import deepcopy
from PySide2.QtWidgets import QWidget, QFileDialog, QAction
from motion_analysis.gui.layout.mp_player_widget_ui import Ui_Form
from motion_analysis.gui.dialogs import CopyMotionDialog, SetConfigDialog
from .animation_player_widget import AnimationPlayerBaseWidget


class MotionPrimitiveControllerWidget(AnimationPlayerBaseWidget, Ui_Form):
    def __init__(self, parent=None):
        self._parent = parent
        QWidget.__init__(self, parent)
        Ui_Form.setupUi(self, self)
        self.animationSpeedDoubleSpinBox.setRange(-4.0, 4.0)
        self.deactivate_player_controls()
        self.init_animation_player_actions()
        self.init_combo_box()
        self.animationToggleButton.setDefaultAction(self.toggle_animation_action)
        #self.createRagdollButton.setDefaultAction(self.create_ragdoll_action)
        self.initSlots()
        self.isPlaying = False
        self._controller = None
        self.labelView.setTimeLineParameters(100000, 10)
        self.labelView.initScene()
        self.fpsLineEdit.textChanged.connect(self.slot_fps_text_changed)

        self.labelView.show()

        self.generateRandomSamplesAction = QAction("Generate Random Samples", self)
        self.generateRandomSamplesAction.triggered.connect(self.generate_random_samples)
        self.generateRandomSamplesButton.setDefaultAction(self.generateRandomSamplesAction)

        self.generatTreeSamplesAction = QAction("Generate Tree Samples", self)
        self.generatTreeSamplesAction.triggered.connect(self.generate_tree_samples)
        self.generateTreeSamplesButton.setDefaultAction(self.generatTreeSamplesAction)


        self.generateRandomConstraintsAction = QAction("Generate Random Constraints", self)
        self.generateRandomConstraintsAction.triggered.connect(self.generate_random_constraints)
        self.generateRandomConstraintsButton.setDefaultAction(self.generateRandomConstraintsAction)

        self.loadConstraintsAction = QAction("Load Constraints", self)
        self.loadConstraintsAction.triggered.connect(self.load_constraints_from_file)
        self.loadConstraintsButton.setDefaultAction(self.loadConstraintsAction)

        self.reachConstraintsAction = QAction("Reach Constraints", self)
        self.reachConstraintsAction.triggered.connect(self.reach_constraints)
        self.reachConstraintsButton.setDefaultAction(self.reachConstraintsAction)

        self.exportAction = QAction("Export to BVH", self)
        self.exportAction.triggered.connect(self.export_to_file)
        self.exportButton.setDefaultAction(self.exportAction)

        self.copyAction = QAction("Create Copy", self)
        self.copyAction.triggered.connect(self.create_motion_copy)
        self.createCopyButton.setDefaultAction(self.copyAction)

        self.generateBlendControllerAction = QAction("Generate Blend Controller", self)
        self.generateBlendControllerAction.triggered.connect(self.create_blend_controller)
        #self.generateBlendControllerButton.setDefaultAction(self.generateBlendControllerAction)

        self.setConfigAction = QAction("Set Config", self)
        self.setConfigAction.triggered.connect(self.set_config)
        self.setConfigButton.setDefaultAction(self.setConfigAction)
        self.prev_annotation_edit_frame_idx = 0

        self._constraints = []

    def set_object(self, controller):
        AnimationPlayerBaseWidget.set_object(self, controller)
        if controller is not None:
            self.fill_joints_combobox()
            n_frames = controller.getNumberOfFrames()
            self.frameNumberSpinBox.setRange(0, n_frames-1)

    def set_config(self):
        set_config_dialog = SetConfigDialog(deepcopy(self._controller.algorithm_config), self)
        set_config_dialog.exec_()
        if set_config_dialog.success:
            self._controller.set_config(set_config_dialog.config)

    def generate_random_samples(self):
        if self._controller is not None:
            n_samples = int(self.numSamplesLineEdit.text())
            sample_offset = int(self.sampleOffsetLineEdit.text())
            self._controller.generate_random_samples(n_samples, sample_offset)
            n_frames = self._controller.getNumberOfFrames()
            self.setFrameRange(0, n_frames - 1)

    def generate_tree_samples(self):
        if self._controller is not None:
            n_samples = int(self.numSamplesLineEdit.text())
            sample_offset = int(self.sampleOffsetLineEdit.text())
            self._controller.generate_random_samples_from_tree(n_samples, sample_offset)
            n_frames = self._controller.getNumberOfFrames()
            self.setFrameRange(0, n_frames - 1)

    def generate_random_constraints(self):
        joint_name = str(self.jointComboBox.currentText())
        frame_idx = int(self.frameNumberSpinBox.value())
        n_samples = int(self.numConstraintsLineEdit.text())
        positions = self._controller.generate_random_constraints(joint_name, frame_idx, n_samples)
        self.set_constraints(positions)

    def set_constraints(self, positions):
        self._constraints = []
        for idx, p in enumerate(positions):
            name = "constraint" + str(idx)
            self._controller.scene_object.scene.addSphere(name, p, radius=1.0)
            self._constraints.append(p)

    def reach_constraints(self):
        joint_name = str(self.jointComboBox.currentText())
        frame_idx = int(self.frameNumberSpinBox.value())
        self._controller.clear()
        for p in self._constraints:
            self._controller.generate_constrained_sample(joint_name, frame_idx, p)

    def export_to_file(self):
        filename = QFileDialog.getSaveFileName(self, 'Save To File', '.')[0]
        print("export to file", filename)
        self._controller.export_to_file(filename)

    def save_constraints_to_file(self, transform_coordinates=True):

        filename = QFileDialog.getSaveFileName(self, 'Save To File', '.')[0]
        with open(filename, "wb") as out_file:
            json.dump(self._constraints, out_file, indent=4)

    def load_constraints_from_file(self):
        filename = QFileDialog.getOpenFileName(self, 'Load From File', '.')[0]
        with open(filename, "r") as in_file:
            data = json.load(in_file)
            self.set_constraints(data["RightHand"])

    def fill_joints_combobox(self):
        self.jointComboBox.clear()
        joints = self._controller.skeleton.get_joint_names()
        for idx, joint in enumerate(joints):
            self.jointComboBox.addItem(joint, idx)

    def create_blend_controller(self):
        self._controller.create_blend_controller()

    def create_motion_copy(self):
        scene_object = self._controller.scene_object
        if len(self._controller.samples) < 1:
            return
        sample = self._controller.samples[0]
        copy_dialog = CopyMotionDialog(sample.n_frames, scene_object.name, self)
        copy_dialog.exec_()
        if copy_dialog.success:
            scene = scene_object.scene
            skeleton_copy = self._controller.get_skeleton_copy()
            start_frame = copy_dialog.start_frame
            end_frame = copy_dialog.end_frame
            mv_copy = self._controller.get_motion_vector_copy(start_frame, end_frame)
            scene.object_builder.create_object("animation_controller", copy_dialog.name, skeleton_copy, mv_copy, mv_copy.frame_time)
