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
from functools import partial
import numpy as np
from transformations import euler_from_quaternion, quaternion_multiply
from PySide2.QtWidgets import  QWidget, QFileDialog, QListWidgetItem, QAction
from PySide2.QtCore import Qt
from motion_analysis.gui.layout.mg_player_widget_ui import Ui_Form
from motion_analysis.gui.dialogs.action_sequence_dialog import ActionSequenceDialog
from motion_analysis.gui.dialogs.select_scene_objects_dialog import SelectSceneObjectsDialog
from motion_analysis.gui.dialogs.utils import get_splines
from motion_analysis.gui.dialogs.set_config_dialog import SetConfigDialog
from motion_analysis.gui.dialogs.add_constraint_dialog import ConstraintDefinition
from .animation_player_widget import AnimationPlayerBaseWidget
from vis_utils.scene.legacy import SplineObject, PositionConstraintObject


def coordinate_transform(p):
    point = [None, None, None]
    if p[0] is not None:
        point[0] = float(p[0])
    if p[2] is not None:
        point[1] = -float(p[2])
    if p[1] is not None:
        point[2] = float(p[1])
    return point


def coordinate_transform_inverse(p):
    point = [None, None, None]
    if p[0] is not None:
        point[0] = float(p[0])
    if p[1] is not None:
        point[2] = -float(p[1])
    if p[2] is not None:
        point[1] = float(p[2])
    print("transform",point, p)
    return point


class MorphableGraphControllerWidget(AnimationPlayerBaseWidget, Ui_Form):
    def __init__(self, parent=None):
        self._parent = parent
        QWidget.__init__(self, parent)
        Ui_Form.setupUi(self, self)
        self.animationSpeedDoubleSpinBox.setRange(-4.0, 4.0)
        self.deactivate_player_controls()
        self.init_animation_player_actions()
        self.init_combo_box()
        self.animationToggleButton.setDefaultAction(self.toggle_animation_action)
        self.createRagdollButton.setDefaultAction(self.create_ragdoll_action)
        self.initSlots()
        self.isPlaying = False
        self._controller = None
        #self.labelView = None
        self.labelView.setTimeLineParameters(100000, 10)
        self.labelView.initScene()

        self.labelView.show()

        self.generateConstrainedAction = QAction("Generate", self)
        self.generateConstrainedAction.triggered.connect(self.generate_constrained_motion)

        self.generateConstrainedButton.setDefaultAction(self.generateConstrainedAction)
        self._default_style_sheet = self.generateConstrainedButton.styleSheet()
        self.generateConstrainedButton.setStyleSheet("background-color: red")

        self.generateRandomAction = QAction("Generate", self)
        self.generateRandomAction.triggered.connect(self.generate_random_motion)
        self.generateRandomButton.setDefaultAction(self.generateRandomAction)

        self.setConstraintsAction = QAction("Set Action Sequence", self)
        self.setConstraintsAction.triggered.connect(self.set_constraints)
        self.setConstraintsButton.setDefaultAction(self.setConstraintsAction)

        self.clearGraphWalkAction = QAction("Clear Graph Walk", self)
        self.clearGraphWalkAction.triggered.connect(self.clear_graph_walk)
        self.clearGraphWalkButton.setDefaultAction(self.clearGraphWalkAction)

        self.setConfigAction = QAction("Set Config", self)
        self.setConfigAction.triggered.connect(self.set_config)
        self.setConfigButton.setDefaultAction(self.setConfigAction)

        self.exportAction = QAction("Export to BVH", self)
        self.exportAction.triggered.connect(self.export_to_file)
        self.exportButton.setDefaultAction(self.exportAction)

        self.saveConstraintsAction = QAction("Save Constraints", self)
        self.saveConstraintsAction.triggered.connect(self.save_constraints_to_file)
        self.saveConstraintsButton.setDefaultAction(self.saveConstraintsAction)

        self.copyAction = QAction("Create Copy", self)
        self.copyAction.triggered.connect(self.create_motion_copy)
        self.createCopyButton.setDefaultAction(self.copyAction)

        self.loadConstraintsAction = QAction("Load Constraints", self)
        self.loadConstraintsAction.triggered.connect(self.load_constraints_from_file)
        self.loadConstraintsButton.setDefaultAction(self.loadConstraintsAction)

        self.exportGraphWalkAction = QAction("Export Graph Walk", self)
        self.exportGraphWalkAction.triggered.connect(self.save_graph_walk_to_file)
        self.exportGraphWalkButton.setDefaultAction(self.exportGraphWalkAction)

        self.loadGraphWalkAction = QAction("Load Graph Walk", self)
        self.loadGraphWalkAction.triggered.connect(self.load_graph_walk_from_file)
        self.loadGraphWalkButton.setDefaultAction(self.loadGraphWalkAction)

        self.load_animated_mesh_action = QAction("Load Mesh", self)
        self.load_animated_mesh_action.triggered.connect(partial(self.load_animated_mesh, animation_controller="morphablegraphs_controller"))
        self.loadAnimatedMeshButton.setDefaultAction(self.load_animated_mesh_action)

        self._action_sequence = None
        self._constraints_dict = None
        self.prev_annotation_edit_frame_idx = 0

    def set_object(self, controller):
        AnimationPlayerBaseWidget.set_object(self, controller)
        if self._controller is not None:
            self.elementaryActionComboBox.clear()
            self.motionPrimitiveComboBox.clear()
            for idx, ea in enumerate(self._controller.getElementaryActions()):
                self.elementaryActionComboBox.addItem(ea, idx)
            start_ea = self._controller.start_node[0]
            for idx, mp in enumerate(self._controller.getMotionPrimitives(start_ea)):
                self.motionPrimitiveComboBox.addItem(mp, idx)

            self.elementaryActionComboBox.currentIndexChanged.connect(self.action_selection_change)
            self.action_selection_change(0)

    def action_selection_change(self, idx):
        self.motionPrimitiveComboBox.clear()
        ea = str(self.elementaryActionComboBox.currentText())
        for idx, mp in enumerate(self._controller.getMotionPrimitives(ea)):
            self.motionPrimitiveComboBox.addItem(mp, idx)

    def set_constraints_splines(self):
        scene = self._parent.sceneManager.getDisplayedScene()
        set_constraints_dialog = SelectSceneObjectsDialog(scene, get_splines, self)
        set_constraints_dialog.exec_()
        if set_constraints_dialog.success:
            splineObject = scene.getObject(set_constraints_dialog.selected_node_id)
            self._create_mg_constraints_dict_from_single_spline(splineObject)

    def set_constraints(self):
        scene = self._parent.sceneManager.getDisplayedScene()
        ea_constraints_dialog = ActionSequenceDialog(scene, self._controller, self)
        ea_constraints_dialog.exec_()
        self._action_sequence = ea_constraints_dialog.get_constrained_actions()

        if len(self._action_sequence) == 0:
            self._controller.clear_graph_walk()
        self.update_action_sequence_list()
        if ea_constraints_dialog.success:
            if ea_constraints_dialog.start_node_object is not None:
                self._controller.set_start_position(ea_constraints_dialog.start_node_object.getPosition())
            self._convert_actions_to_mg_constraints()

    def set_config(self):
        set_config_dialog = SetConfigDialog(deepcopy(self._controller.algorithm_config), self)
        set_config_dialog.exec_()
        if set_config_dialog.success:
            self._controller.set_config(set_config_dialog.config)

    def get_action_sequence(self):
        return self._action_sequence

    def _convert_actions_to_mg_constraints(self):
        if self._action_sequence is None:
            return
        start_position = self._controller.start_pose["position"]
        star_orientation = self._controller.start_pose["orientation"]
        action_list = []
        for action in self._action_sequence:
            action_dict = dict()
            action_dict["action"] = action[0]
            action_dict["constraints"] = []
            if action[1] is not None:
                merged_keyframe_constraints = dict()
                for constraint in action[1]:
                    if isinstance(constraint.constraint_object, SplineObject):
                        if start_position is None:
                            p = constraint.constraint_object.spline.controlPoints[0]
                            start_position = [p.x, p.y, p.z]
                        constraint_dict = self._create_trajectory_constraint_from_spline(constraint.constraint_object, constraint.joint_name)
                        action_dict["constraints"].append(constraint_dict)
                    if isinstance(constraint.constraint_object, PositionConstraintObject):
                        if constraint.joint_name not in merged_keyframe_constraints:
                            merged_keyframe_constraints[constraint.joint_name] = list()
                        merged_keyframe_constraints[constraint.joint_name].append(constraint)

                for joint_name, constraints in merged_keyframe_constraints.items():
                    print("add constraints for ", joint_name, len(constraints))
                    constraint_dict = self._create_keyframe_constraint_dict(joint_name, constraints)
                    action_dict["constraints"].append(constraint_dict)
            action_list.append(action_dict)
        self.create_task_list(action_list, start_position, star_orientation)

    def _create_actions_from_mg_constraints(self):
        if self._constraints_dict is None:
            return
        self._action_sequence = []
        print("create objects from constraints")
        scene = self._parent.sceneManager.getDisplayedScene()
        action_list = []
        if "tasks" in self._constraints_dict.keys():
            for task in self._constraints_dict["tasks"]:
                for action in task["elementaryActions"]:
                    action_list.append(action)
        elif "elementaryActions" in self._constraints_dict.keys():
            for action in self._constraints_dict["elementaryActions"]:
                action_list.append(action)
        else:
            print("Error: Did not find expected keys in input file")
            return

        for action in action_list:
            a = [None, []]
            a[0] = action["action"]
            a[1] = []
            constraints = action["constraints"]
            for constraint in constraints:
                if "keyframeConstraints" in list(constraint.keys()):
                    # add point to scene
                    for c in constraint["keyframeConstraints"]:
                        position = c["position"]
                        scene_object = PositionConstraintObject(position, 2.5)
                        scene.addObject(scene_object)
                        if "semanticAnnotation" in c.keys():
                            if "keyframeLabel" in c["semanticAnnotation"].keys():
                                annotation = c["semanticAnnotation"]["keyframeLabel"]
                            else:
                                annotation = list(c["semanticAnnotation"].keys())[0]
                        elif "keyframeLabel" in c.keys():
                            annotation = c["keyframeLabel"]
                        else:
                            continue
                        print("add", constraint["joint"], annotation, constraint)
                        a[1].append(ConstraintDefinition(scene_object, constraint["joint"], annotation=annotation))
                if "trajectoryConstraints" in list(constraint.keys()):
                    # add trajectory to scene
                    control_points = []
                    for point in constraint["trajectoryConstraints"]:
                        p = [float(p) if p is not None else 0.0 for p in point["position"]]
                        control_points.append(np.array(p))
                    scene_object = SplineObject(control_points,  0.1, 0.6, 0.3)
                    scene_object.transformation[3, :3] = [0, 1, 0]
                    scene.addObject(scene_object)
                    annotation = None# c["semanticAnnotation"].keys()[0]

                    a[1].append(ConstraintDefinition(scene_object, constraint["joint"], annotation=annotation))

            self._action_sequence.append(a)
        self.update_action_sequence_list()


    def _create_actions_from_unity_format(self):
        if self._constraints_dict is None:
            return

        p = self._constraints_dict["startPosition"]
        q = self._constraints_dict["startOrientation"]
        start_pose = dict()
        start_pose["position"] = np.array([p["x"], p["y"], p["z"]])
        q = np.array([q["w"], q["x"], q["y"], q["z"]])
        q = quaternion_multiply([0, 0, 1, 0], q)
        start_pose["orientation"] = np.degrees(euler_from_quaternion(q))
        print("start rotation", start_pose["orientation"])
        self._controller.start_pose = start_pose
        self._action_sequence = []
        print("create objects from constraints")
        scene = self._parent.sceneManager.getDisplayedScene()
        a = [None, []]
        a[0] = self._constraints_dict["name"]
        a[1] = []
        for c in self._constraints_dict["frameConstraints"]:
            p = c["position"]
            p = np.array([p["x"], p["y"], p["z"]])
            # q = c["orientation"]
            # c["orientation"] = np.array([q["w"], q["x"], q["y"], q["z"]])
            annotation = c["keyframe"]
            joint_name = c["joint"]
            scene_object = PositionConstraintObject(p, 2.5)
            scene.addObject(scene_object)
            a[1].append(ConstraintDefinition(scene_object, joint_name, annotation=annotation))

        self._action_sequence.append(a)
        self.update_action_sequence_list()

    def generate_random_motion(self):
        if self._controller is not None:
            ea = str(self.elementaryActionComboBox.currentText())
            mp = str(self.motionPrimitiveComboBox.currentText())
            start_node = (ea, mp)
            n_mp_steps = int(self.mpStepsLineEdit.text())
            # self._controller.synthesize_random_sample(start_node)#generate
            self._controller.synthesize_random_walk(start_node, n_mp_steps)
            n_frames = self._controller.getNumberOfFrames()
            self.setFrameRange(0, n_frames - 1)

    def generate_constrained_motion(self):
        if self._controller is not None and self._constraints_dict is not None:
            random_seed = None
            random_seed_str = str(self.randomSeedLineEdit.text())
            if random_seed_str != "":
                random_seed = int(random_seed_str)
            self._convert_actions_to_mg_constraints()
            print(self._constraints_dict)
            self._controller.synthesize_from_constraints(self._constraints_dict, random_seed)
            n_frames = self._controller.getNumberOfFrames()
            self.setFrameRange(0, n_frames - 1)
            self.init_label_time_line()

    def _create_mg_constraints_dict_from_single_spline(self, splineObject):
        p = splineObject.spline.controlPoints[0]
        start_position = [p.x, p.y, p.z]
        joint_constraint = self._create_trajectory_constraint_from_spline(splineObject)

        action = dict()
        action["action"] = "walk"
        action["constraints"] = [joint_constraint]
        self.create_task_list(start_position, [action])

    def create_task_list(self, action_list, start_position=None, start_orientation=None):
        if start_position is None:
            start_position = np.zeros(3)
        if start_orientation is None:
            start_orientation = np.zeros(3)
        if len(action_list) == 0:
            self._controller.clear_graph_walk()
            #self._constraints_dict["tasks"]["elementaryActions"].keys() == constraints["tasks"]["elementaryActions"].keys()
        constraints = dict()
        constraints["startPose"] = {"position": start_position,
                                    "orientation": start_orientation}
        constraints["tasks"] = [{"elementaryActions": action_list}]
        self._constraints_dict = constraints
        self.generateConstrainedButton.setStyleSheet(self._default_style_sheet)

    def _create_trajectory_constraint_from_spline(self, spline_object, joint_name="Hips"):
        joint_constraint = dict()
        joint_constraint["joint"] = joint_name
        joint_constraint["trajectoryConstraints"] = []
        # ignore the first and the last two points which are duplicates for the spline evaluation
        for p in spline_object.spline.controlPoints[1:-2]:
            control_point = dict()
            if joint_name == self._controller._graph.skeleton.aligning_root_node:
                control_point["position"] = [p[0], 0, p[2]]
            else:
                control_point["position"] = [p[0], p[1], p[2]]

            control_point["orientation"] = [None, None, None]
            joint_constraint["trajectoryConstraints"].append(control_point)
        joint_constraint["keyframeConstraints"] = []
        return joint_constraint

    def _create_keyframe_constraint_dict(self, joint_name, constraint_definitions):
        joint_constraint = dict()
        joint_constraint["joint"] = joint_name
        joint_constraint["keyframeConstraints"] = []
        for c in constraint_definitions:
            keyframe_constraint = dict()
            keyframe_constraint["position"] = c.constraint_object.getPosition()
            keyframe_constraint["semanticAnnotation"] = {c.annotation: True}
            joint_constraint["keyframeConstraints"].append(keyframe_constraint)
        return joint_constraint

    def export_to_file(self):
        print("export to file")
        filename = QFileDialog.getSaveFileName(self, 'Save To File', '.')[0]
        self._controller.export_to_file(filename)

    def save_constraints_to_file(self, transform_coordinates=True):
        if transform_coordinates:
            constraints = self._apply_coordinate_transform(self._constraints_dict)
        else:
            constraints = self._constraints_dict

        filename = QFileDialog.getSaveFileName(self, 'Save To File', '.')[0]
        with open(filename, "w") as out_file:
            json.dump(constraints, out_file, indent=4)

    def load_constraints_from_file(self):
        filename = QFileDialog.getOpenFileName(self, 'Load From File', '.')[0]
        with open(filename, "r") as in_file:
            self._constraints_dict = json.load(in_file)

        if "startPose" in self._constraints_dict.keys():
            self._controller.start_pose = self._constraints_dict["startPose"]
        if "startPosition" in self._constraints_dict.keys():
            self._create_actions_from_unity_format()
        else:
            self._constraints_dict = self._apply_coordinate_transform(self._constraints_dict,
                                                                      coordinate_transform_inverse)
            self._create_actions_from_mg_constraints()

    def _apply_coordinate_transform(self, constraints_dict, transform_func=coordinate_transform):
        constraints_dict = deepcopy(constraints_dict)
        start_position = constraints_dict["startPose"]["position"]
        start_orientation = constraints_dict["startPose"]["orientation"]
        constraints_dict["startPose"] = {"position": transform_func(start_position),
                                         "orientation": transform_func(start_orientation)}
        if "tasks" in constraints_dict:
            for task in constraints_dict["tasks"]:
                for idx, ea in enumerate(task["elementaryActions"]):
                    for c_idx, c in enumerate(ea["constraints"]):
                        if "keyframeConstraints" in list(c.keys()):
                            for p_idx, p in enumerate(c["keyframeConstraints"]):
                                c["keyframeConstraints"][p_idx]["position"] = transform_func(p["position"])
                        if "trajectoryConstraints" in list(c.keys()):
                            for p_idx, p in enumerate(c["trajectoryConstraints"]):
                                c["trajectoryConstraints"][p_idx]["position"] = transform_func(p["position"])
                        constraint = c
                        task["elementaryActions"][idx]["constraints"][c_idx] = constraint
        else:
            for idx, ea in enumerate(constraints_dict["elementaryActions"]):
                for c_idx, c in enumerate(ea["constraints"]):
                    if "keyframeConstraints" in list(c.keys()):
                        for p_idx, p in enumerate(c["keyframeConstraints"]):
                            c["keyframeConstraints"][p_idx]["position"] = transform_func(p["position"])
                    if "trajectoryConstraints" in list(c.keys()):
                        for p_idx, p in enumerate(c["trajectoryConstraints"]):
                            c["trajectoryConstraints"][p_idx]["position"] = transform_func(p["position"])
                    constraint = c
                    constraints_dict["elementaryActions"][idx]["constraints"][c_idx] = constraint
        return constraints_dict

    def update_action_sequence_list(self):
        self.actionListWidget.clear()
        if self._action_sequence is None:
            return
        for action in self._action_sequence:
            item = QListWidgetItem()
            item.setText(action[0])
            item.setData(Qt.UserRole, action[1])
            self.actionListWidget.addItem(item)

    def save_graph_walk_to_file(self):
        filename = QFileDialog.getSaveFileName(self, 'Save To File', '.')[0]
        self._controller.export_graph_walk_to_file(filename)

    def load_graph_walk_from_file(self):
        filename = str(QFileDialog.getOpenFileName(self, 'Load From File', '.'))[0]
        self._controller.load_graph_walk_from_file(filename)

    def clear_graph_walk(self):
        self._controller.clear_graph_walk()


