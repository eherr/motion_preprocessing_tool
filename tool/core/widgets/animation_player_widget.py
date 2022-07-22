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

import os
import collections
import numpy as np
from functools import partial
from PySide2.QtCore import Qt
from PySide2.QtWidgets import  QWidget, QAction, QFileDialog
from PySide2.QtGui import QColor
from tool.core.layout.animation_player_widget_ui import Ui_Form
from tool.core.widget_manager import WidgetManager
from tool.core.dialogs.copy_motion_dialog import CopyMotionDialog
from tool.core.dialogs.select_joints_dialog import SelectJointsDialog
from tool.core.dialogs.retarget_dialog import RetargetDialog
from tool.core.dialogs.copy_from_source_dialog import CopyFromSourceDialog
from tool.core.dialogs.animation_editor_dialog import AnimationEditorDialog
try:
    from tool.core.dialogs.skeleton_editor_dialog import SkeletonEditorDialog
except:
    pass
from tool.core.dialogs.set_annotation_dialog import SetAnnotationDialog
from tool.core.dialogs.utils import load_local_skeleton, load_local_skeleton_model, save_local_skeleton
from tool import constants
from tool.core.application_manager import ApplicationManager
from vis_utils.animation.skeleton_animation_controller import SkeletonAnimationController


def convert_annotation_to_phase(annotations):
    """ annotations: dict that map a string to a list of annotated sections. Each section is defined by a list of ordered frame indices 
    """
    result_str = ""
    return result_str

def convert_annotation_to_actions(annotations):
    """ annotations: dict that map a string to a list of annotated sections. Each section is defined by a list of ordered frame indices 
    """
    result_str = ""
    return result_str

class AnimationPlayerBaseWidget(QWidget):
    COMPONENT_NAME = None
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)

    def set_object(self, scene_object):
        if scene_object is None or self.COMPONENT_NAME not in scene_object._components:
            return
        controller = scene_object._components[self.COMPONENT_NAME]
        self._controller = controller
        if self._controller is not None:
            self.activatePlayerControls()
            n_frames = controller.getNumberOfFrames()
            self.setFrameRange(0, n_frames - 1)
            frame_time = self._controller.get_frame_time()
            if frame_time > 0:
                fps = str(np.ceil(1.0/frame_time))
                self.fpsLineEdit.setText(fps)
            if self.labelView is not None:
                self.init_label_time_line()
            self.loopAnimationCheckBox.setChecked(self._controller.loopAnimation)
            if hasattr(self, "relativeRootCheckBox") and hasattr(self._controller, "relative_root"):
                self.relativeRootCheckBox.setChecked(self._controller.relative_root)
            self.fill_combo_box_with_models()
            self.fill_annotation_combobox()

    def fill_combo_box_with_models(self):
        if not isinstance(self._controller, SkeletonAnimationController):
            return
        if hasattr(self, "skeletonModelComboBox"):
            self.skeletonModelComboBox.clear()
            model_list = [""] + list(constants.LOCAL_SKELETON_MODELS.keys())
            for idx, m in enumerate(model_list):
                self.skeletonModelComboBox.addItem(m, idx)
            skeleton =  self._controller.get_skeleton()
            if skeleton is not None and skeleton.skeleton_model is not None:
                if "name" in skeleton.skeleton_model:
                    name = skeleton.skeleton_model["name"]
                    #https://stackoverflow.com/questions/22797794/pyqt-how-to-set-combobox-to-item-knowing-items-text-a-title
                    index = self.skeletonModelComboBox.findText(name, Qt.MatchFixedString)
                    if index >= 0:
                            self.skeletonModelComboBox.setCurrentIndex(index)

    def fill_annotation_combobox(self):
        if hasattr(self, "labelComboBox"):
            self.labelComboBox.clear()
            semantic_annotation = self._controller.get_semantic_annotation()
            idx = 0
            for label, indices in semantic_annotation:
                self.labelComboBox.addItem(label, idx)
                idx+=1
       

    def init_label_time_line(self):
        n_frames = self._controller.getNumberOfFrames()
        self.labelView.clearScene()
        self.labelView.create_frame_indicator()
        self.labelView.setTimeLineParameters(n_frames, 10)
        self.labelView.set_edit_start_frame(self.prev_annotation_edit_frame_idx)
        semantic_annotation = self._controller.get_semantic_annotation()
        color_map = self._controller.get_label_color_map()
        if semantic_annotation is not None and color_map is not None:
            for label, indices in semantic_annotation:
                color = [0,0,1]
                if label in color_map:
                    color = color_map[label]
                joint_indices = []
                n_entries = len(indices) 
                if n_entries > 0 and type(indices[0]) == list:
                    for i in range(n_entries):
                        joint_indices += indices[i]
                else:
                    joint_indices = indices
       
                self.labelView.addLabel(label, joint_indices, color)
        else:
            self.labelView.addLabel("empty", [], [0,0,0])

    def init_animation_player_actions(self):
        self.toggle_animation_action = QAction("Play", self)
        self.toggle_animation_action.setShortcut('Space')
        self.toggle_animation_action.triggered.connect(self.toggle_animation)

        self.create_ragdoll_action = QAction("Create Ragdoll", self)
        self.create_ragdoll_action.triggered.connect(self.create_ragdoll)

        self.retarget_from_src_action = QAction("Retarget from source", self)
        self.retarget_from_src_action.triggered.connect(self.retarget_from_src)


        self.save_to_bvh_file_action = QAction("Save to BVH file", self)
        self.save_to_bvh_file_action.triggered.connect(partial(self.save_to_file, export_format='bvh'))

        self.save_to_fbx_file_action = QAction("Save to FBX file", self)
        self.save_to_fbx_file_action.triggered.connect(partial(self.save_to_file, export_format='fbx'))

        self.copy_from_src_action = QAction("Copy From Source", self)
        self.copy_from_src_action.triggered.connect(self.copy_from_src)

        self.open_animation_editor_action = QAction("Open Editor", self)
        self.open_animation_editor_action.triggered.connect(self.open_animation_editor)

        self.save_to_json_file_action = QAction("Save to JSON file", self)
        self.save_to_json_file_action.triggered.connect(self.save_to_json_file)

        self.load_annotation_action = QAction("Load Annotation", self)
        self.load_annotation_action.triggered.connect(self.load_annotation)

        self.save_annotation_action = QAction("Export To File", self)
        self.save_annotation_action.triggered.connect(self.save_annotation)

        self.export_annotation_to_phase_action = QAction("Export To Phase File", self)
        self.export_annotation_to_phase_action.triggered.connect(self.export_annotation_to_phase)

        self.export_annotation_to_action_action = QAction("Export To Actions File", self)
        self.export_annotation_to_action_action.triggered.connect(self.export_annotation_to_action)

        self.split_motion_action = QAction("Split Motion", self)
        self.split_motion_action.triggered.connect(self.split_motion)

        self.set_annotation_action = QAction("Set Annotation", self)
        self.set_annotation_action.triggered.connect(self.set_annotation)

        self.copy_action = QAction("Create Copy", self)
        self.copy_action.triggered.connect(self.create_motion_copy)

        self.replace_action = QAction("Replace Animation From BVH/ACM File", self)
        self.replace_action.triggered.connect(self.replace_motion_from_file)

        self.plot_joints_action = QAction("Plot Joint Trajectories", self)
        self.plot_joints_action.triggered.connect(self.plot_joint_trajectories)

        self.load_animated_mesh_action = QAction("Load Mesh", self)
        self.load_animated_mesh_action.triggered.connect(partial(self.load_animated_mesh, animation_controller="animation_controller"))

        self.attach_figure_action = QAction("Attach Figure", self)
        self.attach_figure_action.triggered.connect(self.attach_figure)

        self.set_reference_frame_action = QAction("Set Reference Frame", self)
        self.set_reference_frame_action.triggered.connect(self.set_reference_frame)

        self.edit_skeleton_model_action = QAction("Edit Model", self)
        self.edit_skeleton_model_action.triggered.connect(self.edit_skeleton_model)
        self.add_new_skeleton_model_action = QAction("Add New Model", self)
        self.add_new_skeleton_model_action.triggered.connect(self.add_new_skeleton_model)
        
        self.clear_annotation_action = QAction("Clear Annotation", self)
        self.clear_annotation_action.triggered.connect(self.clear_annotation)

    def initSignals(self):
        self.animationToggleButton.setDefaultAction(self.toggle_animation_action)
        self.retargetFromSourceButton.setDefaultAction(self.retarget_from_src_action)
        self.saveToBVHFileButton.setDefaultAction(self.save_to_bvh_file_action)
        self.saveToFBXFileButton.setDefaultAction(self.save_to_fbx_file_action)
        self.copyFromSourceButton.setDefaultAction(self.copy_from_src_action)
        self.openEditorButton.setDefaultAction(self.open_animation_editor_action)
        self.saveToJSONFileButton.setDefaultAction(self.save_to_json_file_action)
        self.setAnnotationButton.setDefaultAction(self.set_annotation_action)
        self.loadAnnotationButton.setDefaultAction(self.load_annotation_action)
        self.saveAnnotationButton.setDefaultAction(self.save_annotation_action)
        self.exportAnnotationsToPhaseButton.setDefaultAction(self.export_annotation_to_phase_action)
        self.exportAnnotationsToActionsButton.setDefaultAction(self.export_annotation_to_action_action)
        self.createCopyButton.setDefaultAction(self.copy_action)
        self.replaceAnimationButton.setDefaultAction(self.replace_action)
        self.plotJointsButton.setDefaultAction(self.plot_joints_action)
        self.loadAnimatedMeshButton.setDefaultAction(self.load_animated_mesh_action)
        self.skeletonModelComboBox.currentIndexChanged.connect(self.set_skeleton_model)
        self.setReferenceFrameButton.setDefaultAction(self.set_reference_frame_action)
        self.splitMotionButton.setDefaultAction(self.split_motion_action)

        self.addNewSkeletonModelButton.setDefaultAction(self.edit_skeleton_model_action)
        self.editSkeletonModelButton.setDefaultAction(self.add_new_skeleton_model_action)

        self.clearAnnotationButton.setDefaultAction(self.clear_annotation_action)

    def initSlots(self):
        self.loopAnimationCheckBox.clicked.connect(self.toggle_animation_loop)
        if hasattr(self, "relativeRootCheckBox"):
            self.relativeRootCheckBox.clicked.connect(self.toggle_relative_root)
        self.animationFrameSpinBox.valueChanged.connect(self.update_animation_time_from_spinbox)
        self.animationSpeedDoubleSpinBox.valueChanged.connect(self.set_speed)
        self.animationFrameSlider.valueChanged.connect(self.frame_changed)

    def init_combo_box(self):
        self.drawModeComboBox.clear()
        self.drawModeComboBox.addItem("None", 0)
        self.drawModeComboBox.addItem("Lines", 1)
        self.drawModeComboBox.addItem("Boxes", 2)
        self.drawModeComboBox.addItem("CoordinateSystem", 3)
        self.drawModeComboBox.setCurrentIndex(1)
        self.drawModeComboBox.currentIndexChanged.connect(self.draw_mode_selection_changed)

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
            if self.labelView is not None:
                self.labelView.setFrame(value)

    def toggle_animation_loop(self):
        self._controller.toggle_animation_loop()

    def toggle_relative_root(self):
        self._controller.relative_root = not self._controller.relative_root

    def set_speed(self, value):
        self._controller.setAnimationSpeed(value)

    def start_animation(self):
        if self._controller.startAnimation():
            self.animationToggleButton.setText("Stop")

    def stop_animation(self):
        if self._controller.stopAnimation():
            self.animationToggleButton.setText("Play")

    def setFrameRange(self, min_v, max_v):
        self.animationFrameSlider.setRange(min_v, max_v)
        self.animationFrameSpinBox.setRange(min_v, max_v)

    def activatePlayerControls(self):
        self.animationFrameSlider.setEnabled(True)
        self.animationFrameSpinBox.setEnabled(True)
        self.animationToggleButton.setEnabled(True)

    def deactivate_player_controls(self):
        self.animationFrameSlider.setEnabled(False)
        self.animationFrameSpinBox.setEnabled(False)
        self.animationToggleButton.setEnabled(False)

    def updateAnimationTimeInGUI(self, value):
        self.setAnimationSliderValue(value)
        self.setAnimationFrameSpinBoxValue(value)
        if self.labelView is not None:
            self.labelView.setFrame(value)

    def setAnimationSliderValue(self, value):
        self.animationFrameSlider.setValue(value)
        if self.labelView is not None:
            self.labelView.setFrame(value)

    def setAnimationFrameSpinBoxValue(self, value):
        self.animationFrameSpinBox.setValue(value)
        if self.labelView is not None:
            self.labelView.setFrame(value)

    def create_ragdoll(self):
        self._controller.create_ragdoll()

    def draw_mode_selection_changed(self, idx):
        self._controller._visualization.draw_mode = int(idx)

    def save_to_file(self, export_format="bvh"):
        filename = QFileDialog.getSaveFileName(self, 'Save To File', '.')[0]
        self._controller.export_to_file(filename, export_format=export_format)

    def copy_from_src(self):
        graphics_widget = ApplicationManager.instance.graphics_widget
        copy_from_src_dialog = CopyFromSourceDialog(self._controller, self._controller.scene_object.scene, graphics_widget, graphics_widget.parent)
        copy_from_src_dialog.exec_()
        if copy_from_src_dialog.success:
            new_frames = copy_from_src_dialog.right_controller.get_frames()
            print("overwrite frames", len(new_frames))
            self._controller.replace_frames(new_frames)

    def open_animation_editor(self):
        graphics_widget = ApplicationManager.instance.graphics_widget
        animation_editor = AnimationEditorDialog(self._controller, self._controller.scene_object.scene, graphics_widget, graphics_widget.parent)
        animation_editor.exec_()
        if animation_editor.success:
            new_frames = animation_editor.controller.get_frames()
            n_frames = len(new_frames)
            print("overwrite frames", n_frames)
            self._controller._motion.mv.frame_time = animation_editor.controller._motion.mv.frame_time
            fps = str(np.ceil(1.0/self._controller._motion.mv.frame_time))
            self.fpsLineEdit.setText(fps)
            skeleton = animation_editor.controller.get_skeleton()
            skeleton_vis = self._controller.scene_object._components["skeleton_vis"]
            skeleton_vis.set_skeleton(skeleton)
            self._controller.skeleton = skeleton
            self._controller.replace_frames(new_frames)
            self._controller.updateTransformation()
            self.setFrameRange(0, n_frames-1)
        else:
            new_frames = animation_editor.original_frames
            print("reset frames", len(new_frames))
            self._controller.replace_frames(new_frames)
            self._controller.updateTransformation()

    def save_to_json_file(self):
        filename = QFileDialog.getSaveFileName(self, 'Save To File', '.')[0]
        self._controller.export_to_file(filename, export_format="json")

    def retarget_from_src(self):
        set_controller_dialog = RetargetDialog(self._controller, self._controller.scene_object.scene, self)
        set_controller_dialog.exec_()
        if set_controller_dialog.success:
            src_object = self._controller.scene_object.scene.getObject(set_controller_dialog.selected_node_id)
            scale_factor = set_controller_dialog.scale_factor
            src_model = set_controller_dialog.src_model
            target_model = set_controller_dialog.target_model
            frame_range = set_controller_dialog.start_frame, set_controller_dialog.end_frame
            self._controller.get_skeleton().skeleton_model = target_model
            if "animation_controller" in list(src_object._components.keys()):
                src_controller = src_object._components["animation_controller"]
                n_frames = self._controller.retarget_from_src(src_controller, scale_factor, src_model, target_model, frame_range)
                self.setFrameRange(0, n_frames - 1)
            elif "morphablegraphs_controller" in list(src_object._components.keys()):
                src_controller = src_object._components["morphablegraphs_controller"]
                n_frames = self._controller.retarget_from_src(src_controller, scale_factor, src_model, target_model, frame_range)
                self.setFrameRange(0, n_frames - 1)

    def load_annotation(self):
        filename = QFileDialog.getOpenFileName(self, 'Load From File', '.')[0]
        self._controller.load_annotation(str(filename))
        self.init_label_time_line()

    def save_annotation(self):
        filename = QFileDialog.getSaveFileName(self, 'Save To File', '.')[0]
        self._controller.save_annotation(str(filename))
        
    def export_annotation_to_phase(self):
        filename = QFileDialog.getSaveFileName(self, 'Save To File', '.')[0]
        if filename is not None:
            filename = str(filename)
            phase_str = convert_annotation_to_phase(self._controller._motion._semantic_annotation)
            with open(filename, "wt") as out_file:
                out_file.write(phase_str)

    def export_annotation_to_action(self):
        filename = QFileDialog.getSaveFileName(self, 'Save To File', '.')[0]
        if filename is not None:
            filename = str(filename)
            actions_str = convert_annotation_to_actions(self._controller._motion._semantic_annotation)
            with open(filename, "wt") as out_file:
                out_file.write(actions_str)

    def set_annotation(self):
        graphics_widget = ApplicationManager.instance.graphics_widget
        a = SetAnnotationDialog(self._controller, graphics_widget, graphics_widget.parent)
        a.exec_()
        if a.success:
            self._controller._motion._semantic_annotation = a.annotations
            self._controller._motion.label_color_map = a.color_map
            self.fill_annotation_combobox()
            self.init_label_time_line()

    def clear_annotation(self):
        self._controller._motion._semantic_annotation = collections.OrderedDict()
        self._controller._motion.label_color_map = collections.OrderedDict()
        self.fill_annotation_combobox()
        self.init_label_time_line()

    def split_motion(self):
        for idx, (key, segments) in enumerate(self._controller._motion._semantic_annotation.items()):
            if type(segments[0]) ==list:
                for segment in segments:
                    start = segment[0]
                    end = segment[-1]
                    self.create_motion_segment_copy(idx, start, end)
            else:
                start = segments[0]
                end = segments[-1]
                self.create_motion_segment_copy(idx, start, end)

    def create_motion_segment_copy(self, idx, start, end):
        scene_object = self._controller.scene_object
        out_file_name = scene_object.name + str(idx) + "_" + str(start) + "-" + str(end) + ".bvh"
        #print("write section to " + out_file_name)
        #self._controller.export_to_file(out_file_name, frame_range=(start, end))
        scene = scene_object.scene
        skeleton_copy = self._controller.get_skeleton_copy()
        start_frame = start
        end_frame = end
        mv_copy = self._controller.get_motion_vector_copy(start_frame, end_frame)
        #semantic_annotation = self._controller._motion._semantic_annotation
        scene.object_builder.create_object("animation_controller",out_file_name, skeleton_copy, mv_copy, mv_copy.frame_time) 

    def create_motion_copy(self):
        scene_object = self._controller.scene_object
        copy_dialog = CopyMotionDialog(self._controller.getNumberOfFrames(), scene_object.name, self)
        copy_dialog.exec_()
        if copy_dialog.success:
            scene = scene_object.scene
            skeleton_copy = self._controller.get_skeleton_copy()
            start_frame = copy_dialog.start_frame
            end_frame = copy_dialog.end_frame
            mv_copy = self._controller.get_motion_vector_copy(start_frame, end_frame)
            semantic_annotation = self._controller._motion._semantic_annotation
            scene.object_builder.create_object("animation_controller",copy_dialog.name, skeleton_copy, mv_copy, mv_copy.frame_time, semantic_annotation=semantic_annotation) 

    def plot_joint_trajectories(self):
        select_joints_dialog = SelectJointsDialog(self._controller.get_skeleton(), self)
        select_joints_dialog.exec_()
        if select_joints_dialog.success:
            joint_list = select_joints_dialog.selected_joints
            self._controller.plot_joint_trajectories(joint_list)

    def replace_motion_from_file(self):
        filename = QFileDialog.getOpenFileName(self, 'Load From File', '.')[0]
        self._controller.replace_motion_from_file(str(filename))

    def load_skeleton_model(self):
        filename = QFileDialog.getOpenFileName(self, 'Load From File', '.')[0]
        self._controller.replace_skeleton_model(str(filename))

    def load_animated_mesh(self, animation_controller="animation_controller"):
        filename = QFileDialog.getOpenFileName(self, 'Load From File', '.')[0]
        self._controller.attach_animated_mesh_component(str(filename), animation_controller)

    def attach_figure(self):
        figure_def = None
        self._controller.attach_figure_controller(figure_def, width_scale=0.1)

    def set_reference_frame(self):
        self._controller.set_reference_frame(self._controller._motion.frame_idx)

    def set_skeleton_model(self, idx):
        name = str(self.skeletonModelComboBox.currentText())
        if name == "Load from file":
            self.load_skeleton_model()
        elif name in constants.LOCAL_SKELETON_MODELS:
            self._controller.set_skeleton_model(constants.LOCAL_SKELETON_MODELS[name]["model"])

    def slot_fps_text_changed(self, value):
        fps = float(value)
        if fps > 0:
            print("set fps", fps)
            self._controller.set_frame_time(1.0/fps)

    def edit_skeleton_model(self): 
        skeleton = self._controller.get_skeleton()
        graphics_widget = ApplicationManager.instance.graphics_widget
        name = str(self.skeletonModelComboBox.currentText())
        enable_line_edit = False
        data = load_local_skeleton(self.local_skeleton_dir, name)
        if data is None:
            print("Error could not load skeleton model")
            return
        skeleton_model = data["model"]
        skeleton_editor = SkeletonEditorDialog(name, skeleton, graphics_widget, graphics_widget.parent, enable_line_edit, skeleton_model)
        skeleton_editor.exec_()
        if skeleton_editor.success and skeleton_editor.skeleton_model is not None:
            data["model"] = skeleton_editor.skeleton_model
            save_local_skeleton(self.local_skeleton_dir, name, data)

    def add_new_skeleton_model(self):
        skeleton = self._controller.get_skeleton()
        graphics_widget = ApplicationManager.instance.graphics_widget
        enable_line_edit = True
        skeleton_model = dict() # create a new model
        skeleton_editor = SkeletonEditorDialog("", skeleton, graphics_widget, graphics_widget.parent, enable_line_edit, skeleton_model)
        skeleton_editor.exec_()
        if skeleton_editor.success and skeleton_editor.skeleton_model is not None:
            name = skeleton_editor.name
            data = dict()
            data["name"] = name
            data["skeleton"] = skeleton.to_unity_format()
            data["model"] = skeleton_editor.skeleton_model
            save_local_skeleton(self.local_skeleton_dir, name, data)
            constants.LOCAL_SKELETON_MODELS[name] = data
            self.fill_combo_box_with_models()

class AnimationPlayerWidget(AnimationPlayerBaseWidget, Ui_Form):
    COMPONENT_NAME = "animation_controller"
    def __init__(self, parent):
        QWidget.__init__(self, parent)
        Ui_Form.setupUi(self, self)
        self.local_skeleton_dir = constants.DATA_DIR + os.sep + "skeletons"
        self.animationSpeedDoubleSpinBox.setRange(-4.0, 4.0)
        self.deactivate_player_controls()
        self.init_animation_player_actions()
        self.initSignals()
        self.initSlots()
        self.isPlaying = False
        self._controller = None
        self.fpsLineEdit.textChanged.connect(self.slot_fps_text_changed)
        self.init_combo_box()
        self.prev_annotation_edit_frame_idx = 0
        self.labelView.setTimeLineParameters(100000, 10)
        self.labelView.initScene()

        self.labelView.show()


WidgetManager.register("animation_player", AnimationPlayerWidget, True)