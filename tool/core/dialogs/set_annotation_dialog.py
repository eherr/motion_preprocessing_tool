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
import collections
import numpy as np
from OpenGL.GL import *
from PySide2.QtCore import QTimer, Qt
from PySide2.QtWidgets import  QDialog, QAction, QColorDialog
from .select_joints_dialog import SelectJointsDialog
from tool.core.widgets.scene_viewer import SceneViewerWidget
from vis_utils.scene.editor_scene import EditorScene
from tool.core.annotation_editor import AnnotationEditor
from tool.core.layout.set_annotation_dialog_ui import Ui_Dialog

def get_random_color():
    random_color = np.random.rand(3, )
    if np.sum(random_color) < 0.5:
        random_color += np.array([0, 0, 1])
    return random_color.tolist()

class SetAnnotationDialog(QDialog, Ui_Dialog):
    def __init__(self, controller, share_widget, parent=None):
        QDialog.__init__(self, parent)
        Ui_Dialog.setupUi(self, self)
        self.view = SceneViewerWidget(parent, share_widget, size=(400,400))
        self.view.setObjectName("left")
        self.view.setMinimumSize(400,400)
        self.view.initializeGL()
        self.view.enable_mouse_interaction = True
        self.viewerLayout.addWidget(self.view)
        self.success = False
        self.okButton.clicked.connect(self.slot_accept)
        self.cancelButton.clicked.connect(self.slot_reject)
        self.removeButton.clicked.connect(self.remove_label)
        self.addButton.clicked.connect(self.add_label)
        self.setColorButton.clicked.connect(self.set_color)
        self.displayFrameSlider.valueChanged.connect(self.slider_frame_changed)
        self.displayFrameSpinBox.valueChanged.connect(self.spinbox_frame_changed)
        self.displayFrameSlider.valueChanged.connect(self.display_changed)
        self.displayFrameSpinBox.valueChanged.connect(self.display_changed)
        self.fps = 60
        self.dt = 1/60
        self.timer = QTimer()
        self.timer.timeout.connect(self.draw)
        self.timer.start(0)
        self.timer.setInterval(1000.0/self.fps)
        self.view.makeCurrent()
        self.edit_scene = EditorScene(True)
        self.edit_scene.enable_scene_edit_widget = False
        self.edit_controller = self.copy_controller(controller, self.edit_scene)
        self.n_frames = controller._motion.get_n_frames()
        self.editor = AnnotationEditor()
        motion = self.edit_controller._motion
        self.editor.set_annotation(motion._semantic_annotation, motion.label_color_map)
        self.set_frame_range()
        
        self.fill_label_combobox()
        self.initialized = False
        
        self.init_actions()
        self.labelView.setTimeLineParameters(100000, 10)
        self.labelView.initScene()
        self.labelView.show()
        self.init_label_time_line()
        self.plot_objects = []

    def init_actions(self):
        self.create_segment_action = QAction("Create Segment", self)
        self.create_segment_action.triggered.connect(self.create_annotation_section)
        self.createSegmentButton.clicked.connect(self.create_segment_action.trigger)

        self.remove_segment_action = QAction("Remove Segment", self)
        self.remove_segment_action.triggered.connect(self.remove_annotation_section)
        self.removeSegmentButton.clicked.connect(self.remove_segment_action.trigger)
        
        self.extend_annotation_action = QAction("Extend Segment", self)
        self.extend_annotation_action.triggered.connect(self.overwrite_current_section_by_neighbor)
        self.extendSegmentButton.clicked.connect(self.extend_annotation_action.trigger)

        self.set_annotation_edit_start_action = QAction("Set Window Start", self)
        self.set_annotation_edit_start_action.triggered.connect(self.set_annotation_edit_start)
        self.setAnnotationStartButton.clicked.connect(self.set_annotation_edit_start_action.trigger)

        self.split_annotation_action = QAction("Split Segment", self)
        self.split_annotation_action.triggered.connect(self.split_annotation)
        self.splitSegmentsButton.clicked.connect(self.split_annotation_action.trigger)
        
        self.merge_annotation_action = QAction("Merge Segments", self)
        self.merge_annotation_action.triggered.connect(self.merge_annotation)
        self.mergeSegmentsButton.clicked.connect(self.merge_annotation_action.trigger)


        self.clearTimelineButton.clicked.connect(self.clear_timeline)
        self.plotJointsButton.clicked.connect(self.plot_joint_trajectories)
        self.removeJointPlotButton.clicked.connect(self.remove_joint_plot)


    def closeEvent(self, e):
        self.timer.stop()
        self.view.makeCurrent()
        try:
           del self.view
        except:
            print("ignore the error and keep going")
    
    def draw(self):
        """ draw current scene on the given view
        (note before calling this function the context of the view has to be set as current using makeCurrent() and afterwards the doubble buffer has to swapped to display the current frame swapBuffers())
        """
        if not self.initialized:
            if self.view.graphics_context is not None:
                self.view.resize(400,400)
                self.initialized = True
        self.edit_scene.update(self.dt)
        self.view.makeCurrent()
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        self.view.graphics_context.render(self.edit_scene)
        self.view.swapBuffers()

    def display_changed(self, frame_idx):
        if self.edit_controller is not None:
            self.edit_controller.setCurrentFrameNumber(frame_idx)
            self.displayFrameSpinBox.setValue(frame_idx)
            self.labelView.setFrame(frame_idx)

    def set_color(self):
        color_map = self.edit_controller._motion.label_color_map
        if color_map is not None:
            label = str(self.labelComboBox.currentText())
            if label in list(color_map.keys()):
                color = QColorDialog.getColor()
                color_map[label] = [color.redF(), color.greenF(), color.blueF()]
        self.edit_controller._motion.label_color_map = color_map
        self.init_label_time_line()

    def set_frame_range(self):
        self.displayFrameSlider.setRange(0, self.n_frames-1)
        self.displayFrameSpinBox.setRange(0, self.n_frames-1)
        self.displayFrameSlider.setValue(0)
        self.displayFrameSpinBox.setValue(0)

    def spinbox_frame_changed(self, frame):
        self.displayFrameSlider.setValue(self.displayFrameSpinBox.value())

    def slider_frame_changed(self, frame):
        self.displayFrameSpinBox.setValue(self.displayFrameSlider.value())

    def fill_label_combobox(self):
        self.labelComboBox.clear()
        for idx, label in enumerate(self.editor._semantic_annotation):
            self.labelComboBox.addItem(label, idx)

    def add_label(self):
        label = str(self.labelLineEdit.text())
        color = get_random_color()
        if self.editor.add_label(label, color):
            joint_indices = []
            self.labelView.addLabel(label, joint_indices, color_map[label])
        self.edit_controller._motion._semantic_annotation = self.editor._semantic_annotation
        self.edit_controller._motion.label_color_map = self.editor._label_color_map
        self.fill_label_combobox()
        self.init_label_time_line()

    def remove_label(self):
        label = str(self.labelComboBox.currentText())
        if self.editor.remove_label(label):
            self.edit_controller._motion._semantic_annotation = self.editor._semantic_annotation
            self.fill_label_combobox()
            self.init_label_time_line()

    def slot_accept(self):
        self.success = True
        self.annotations = self.editor._semantic_annotation
        self.color_map = self.editor._label_color_map
        self.close()

    def slot_reject(self):
        self.annotations = self.editor._semantic_annotation
        self.color_map = self.editor._label_color_map
        self.close()

    def copy_controller(self, controller, target_scene):
        skeleton = controller.get_skeleton_copy()
        mv = controller.get_motion_vector_copy()
        print("copied", mv.n_frames, len(mv.frames), controller.getNumberOfFrames())
        o = target_scene.object_builder.create_object("animation_controller","", 
                                            skeleton, mv, mv.frame_time, 
                                            semantic_annotation=None) 
        c = o._components["animation_controller"]
        c._motion._semantic_annotation = controller._motion._semantic_annotation
        c._motion.label_color_map = controller._motion.label_color_map
        return c
    
    def init_label_time_line(self):
        n_frames = self.edit_controller.getNumberOfFrames()
        self.labelView.clearScene()
        self.labelView.create_frame_indicator()
        self.labelView.setTimeLineParameters(n_frames, 10)
        self.labelView.set_edit_start_frame(self.editor.prev_annotation_edit_frame_idx)
        if len(self.editor._semantic_annotation) > 0:
            for label, indices in self.editor._semantic_annotation.items():
                color = [0,0,1]
                if label in self.editor._label_color_map:
                    color = self.editor._label_color_map[label]
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
  
    def split_annotation(self):
        frame_idx = self.edit_controller._motion.frame_idx
        n_frames = self.edit_controller._motion.get_n_frames()
        self.editor.split_annotation(frame_idx, n_frames)
        self.fill_label_combobox()
        self.init_label_time_line()
    
    def create_annotation_section(self):
        frame_idx = self.edit_controller._motion.frame_idx
        label = str(self.labelComboBox.currentText())
        n_labels = len(self.editor._semantic_annotation)
        if self.editor.create_annotation_section(frame_idx, label):
            self.init_label_time_line()
            index = self.labelComboBox.currentIndex() +1
            index %= n_labels
            self.labelComboBox.setCurrentIndex(index)

    def remove_annotation_section(self):
        frame_idx = self.edit_controller._motion.frame_idx
        current_label = str(self.labelComboBox.currentText())
        #current_label, current_entry_idx = self.get_annotation_of_frame(frame_idx)
        if self.editor.remove_annotation_section(current_label, frame_idx):
            self.init_label_time_line()

    def overwrite_current_section_by_neighbor(self):
        frame_idx = self.edit_controller._motion.frame_idx
        if self.editor.overwrite_current_section_by_neighbor(frame_idx):
            self.init_label_time_line()
    
    def set_annotation_edit_start(self):
        frame_idx = self.edit_controller._motion.frame_idx
        self.editor.set_annotation_edit_start(frame_idx)
        self.labelView.set_edit_start_frame(frame_idx)

    def merge_annotation(self):
        frame_idx = self.edit_controller._motion.frame_idx
        if self.editor.merge_annotation(frame_idx):
            self.init_label_time_line()
            self.fill_label_combobox()

    def clear_timeline(self):
        label = str(self.labelComboBox.currentText())
        if self.editor.clear_timeline(label):
            self.init_label_time_line()

    def keyReleaseEvent(self, event):
        if event.key() == Qt.Key_G:
            self.create_annotation_section()
        elif event.key() == Qt.Key_H:
            self.remove_annotation_section()
        elif event.key() == Qt.Key_J:
            self.overwrite_current_section_by_neighbor()
        elif event.key() == Qt.Key_K:
            self.set_annotation_edit_start()
        elif event.key() == Qt.Key_M:
            self.split_annotation()
        elif event.key() == Qt.Key_N:
            self.merge_annotation()

    def plot_joint_trajectories(self):
        select_joints_dialog = SelectJointsDialog(self.edit_controller._visualization.skeleton, self)
        select_joints_dialog.exec_()
        if select_joints_dialog.success:
            joint_list = select_joints_dialog.selected_joints
            self.plot_objects = self.edit_controller.plot_joint_trajectories(joint_list)
    
    def remove_joint_plot(self):
        for o in self.plot_objects:
            self.edit_scene.removeObject(o.node_id)
        self.plot_objects = []
