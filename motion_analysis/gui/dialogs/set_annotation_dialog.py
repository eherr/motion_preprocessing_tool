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
from PySide2.QtCore import QTimer, Qt
from PySide2.QtWidgets import  QDialog, QAction, QColorDialog
from .select_joints_dialog import SelectJointsDialog
from motion_analysis.gui.widgets.scene_viewer import SceneViewerWidget
from vis_utils.scene.editor_scene import EditorScene
from motion_analysis.gui.layout.set_annotation_dialog_ui import Ui_Dialog
from OpenGL.GL import *

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
        self.set_frame_range()
        self.fill_label_combobox()
        self.initialized = False
        
        self.init_actions()

        self.prev_annotation_edit_frame_idx = 0
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
        annotations = self.edit_controller._motion._semantic_annotation
        if annotations is not None:
            for idx, ea in enumerate(annotations.keys()):
                self.labelComboBox.addItem(ea, idx)


    def add_label(self):
        annotations = self.edit_controller._motion._semantic_annotation
        color_map = self.edit_controller._motion.label_color_map
        label = str(self.labelLineEdit.text())
        if label not in list(annotations.keys()):
            annotations[label] = []
            color_map[label] = get_random_color() 
            joint_indices = []
            self.labelView.addLabel(label, joint_indices, color_map[label])
        self.edit_controller._motion._semantic_annotation = annotations
        self.edit_controller._motion.label_color_map = color_map
        self.fill_label_combobox()
        self.init_label_time_line()

    def remove_label(self):
        annotations = self.edit_controller._motion._semantic_annotation
        if annotations is not None:
            label = str(self.labelComboBox.currentText())
            if label in list(annotations.keys()):
                del annotations[label]
        self.edit_controller._motion._semantic_annotation = annotations
        self.fill_label_combobox()
        self.init_label_time_line()

    def slot_accept(self):
        self.success = True
        self.annotations = self.edit_controller._motion._semantic_annotation
        self.color_map = self.edit_controller._motion.label_color_map
        self.close()

    def slot_reject(self):
        self.annotations = self.edit_controller._motion._semantic_annotation
        self.color_map = self.edit_controller._motion.label_color_map
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
        self.labelView.set_edit_start_frame(self.prev_annotation_edit_frame_idx)
        semantic_annotation = self.edit_controller.get_semantic_annotation()
        color_map = self.edit_controller.get_label_color_map()
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
        
    def get_annotation_of_frame(self, frame_idx, ignore_label=None):
        labels = list(self.edit_controller._motion._semantic_annotation.keys())
        current_label = labels[0]
        delta = np.inf
        current_entry_idx = None
        for label in labels:
            if label == ignore_label:
                continue
            entry_idx = 0
            for entry in self.edit_controller._motion._semantic_annotation[label]:
                if type(entry) == list:
                    for idx in entry:
                        if abs(idx - frame_idx) < delta:
                            delta = abs(idx - frame_idx)
                            current_label = label
                            current_entry_idx = entry_idx
                            if delta == 0:
                                break
                else:
                    if abs(entry - frame_idx) < delta:
                        delta = abs(entry - frame_idx)
                        current_label = label
                        current_entry_idx = None
                        if delta == 0:
                            break
                entry_idx+=1
        return current_label, current_entry_idx
    
    def get_section_of_current_frame(self, label, frame_idx):
        delta = np.inf
        current_entry_idx = None
        entry_idx = 0
        for entry in self.edit_controller._motion._semantic_annotation[label]:
            if type(entry) == list:
                for idx in entry:
                    if abs(idx - frame_idx) < delta:
                        delta = abs(idx - frame_idx)
                        current_entry_idx = entry_idx
                        if delta == 0:
                            break
            else:
                if abs(entry - frame_idx) < delta:
                    delta = abs(entry - frame_idx)
                    current_entry_idx = None
                    if delta == 0:
                        break
            entry_idx+=1
        return current_entry_idx

    def split_annotation_section(self, current_label, frame_idx):
        idx_list = self.edit_controller._motion._semantic_annotation[current_label]
        idx_list.sort()
        start_idx = idx_list[0]
        end_idx = idx_list[-1]

        new_annotations = list()
        new_color_map = list()
        for label in self.edit_controller._motion._semantic_annotation.keys():
            if label != current_label: # copy
                new_annotations.append(self.edit_controller._motion._semantic_annotation[label])
                new_color_map.append(self.edit_controller._motion.label_color_map[label])
            else: #split at frame_idx
                new_annotations.append(list(range(start_idx, frame_idx)))
                new_color_map.append([0, 0, 0])
                new_annotations.append(list(range(frame_idx, end_idx)))
                new_color_map.append([0, 0, 0])


        self.edit_controller._motion._semantic_annotation = collections.OrderedDict()
        self.edit_controller._motion.label_color_map = collections.OrderedDict()
        for idx, value in enumerate(new_annotations):
            new_label = "c" + str(idx)
            self.edit_controller._motion._semantic_annotation[new_label] = new_annotations[idx]
            self.edit_controller._motion.label_color_map[new_label] = new_color_map[idx]
        
    def split_annotation(self):
        frame_idx = self.edit_controller._motion.frame_idx
        labels = list(self.edit_controller._motion._semantic_annotation.keys())
        n_labels = len(labels)
        if n_labels > 0:
            current_label, current_entry_idx = self.get_annotation_of_frame(frame_idx)
            self.split_annotation_section(current_label, frame_idx)
        else:
            n_frames = self.edit_controller._motion.get_n_frames()
            section1_label ="c" + str(n_labels)
            section2_label = "c" + str(n_labels + 1)
            self.edit_controller._motion._semantic_annotation[section1_label] = list(range(0, frame_idx))
            self.edit_controller._motion.label_color_map[section1_label] = [0,0,0]
            self.edit_controller._motion._semantic_annotation[section2_label] = list(range(frame_idx, n_frames))
            self.edit_controller._motion.label_color_map[section2_label] = [0,0,0]
        self.fill_label_combobox()
        self.init_label_time_line()
    
    def create_annotation_section(self):
        frame_idx = self.edit_controller._motion.frame_idx
        #labels = list(self.edit_controller._motion._semantic_annotation.keys())
        label = str(self.labelComboBox.currentText())
        n_labels = len(self.edit_controller._motion._semantic_annotation)
        if label in self.edit_controller._motion._semantic_annotation:
            if self.prev_annotation_edit_frame_idx < frame_idx:
                section = list(range(self.prev_annotation_edit_frame_idx, frame_idx))
            else:
                section = list(range(frame_idx, self.prev_annotation_edit_frame_idx))
            self.edit_controller._motion._semantic_annotation[label] += [section]
            self.prev_annotation_edit_frame_idx = frame_idx
            print("set annotation", self.prev_annotation_edit_frame_idx, frame_idx)
            self.clean_annotation_sections()
            self.init_label_time_line()
            index = self.labelComboBox.currentIndex() +1
            index %= n_labels
            self.labelComboBox.setCurrentIndex(index)
        else:
            print("no label found")

    def remove_annotation_section(self):
        frame_idx = self.edit_controller._motion.frame_idx
        labels = list(self.edit_controller._motion._semantic_annotation.keys())
        print("try to remove annoation at", frame_idx, len(labels))
        if len(labels) > 0:
            current_label = str(self.labelComboBox.currentText())
            #current_label, current_entry_idx = self.get_annotation_of_frame(frame_idx)
            current_entry_idx = self.get_section_of_current_frame(current_label, frame_idx)
            if current_entry_idx is None:
                print("did not find section at", frame_idx)
                return
            old_list = self.edit_controller._motion._semantic_annotation[current_label][current_entry_idx]
            if self.prev_annotation_edit_frame_idx < frame_idx:
                min_v = self.prev_annotation_edit_frame_idx
                max_v = frame_idx
            else:
                min_v = frame_idx
                max_v = self.prev_annotation_edit_frame_idx
            new_list = []
            for v in old_list:
                if v < min_v or v >= max_v:
                    new_list.append(v)
            print("remove annotation", len(old_list),len(new_list), min_v, max_v)
            self.edit_controller._motion._semantic_annotation[current_label][current_entry_idx] = new_list
            self.clean_annotation_sections()
            self.init_label_time_line()
       

    def overwrite_current_section_by_neighbor(self):
        frame_idx = self.edit_controller._motion.frame_idx
        labels = list(self.edit_controller._motion._semantic_annotation.keys())
        if len(labels) > 1:
            current_label, current_entry_idx = self.get_annotation_of_frame(frame_idx)
            next_closest_label, next_closest_entry_idx = self.get_next_closest_label_entry(current_label, current_entry_idx)
            self.overwrite_section(next_closest_label, next_closest_entry_idx, current_label, current_entry_idx, frame_idx)
            self.clean_annotation_sections()
            self.init_label_time_line()

    
    def set_annotation_edit_start(self):
        print("set annoatation", self.edit_controller._motion.frame_idx)
        self.prev_annotation_edit_frame_idx = self.edit_controller._motion.frame_idx
        self.labelView.set_edit_start_frame(self.prev_annotation_edit_frame_idx)

    def overwrite_section(self, next_label, next_entry, cur_label, cur_entry, frame_idx):
        """ overwrite current section with closest section """
        print("change", next_label,next_entry, "to", cur_label,cur_entry )
        next_idx_list = self.edit_controller._motion._semantic_annotation[next_label][next_entry]
        cur_idx_list = self.edit_controller._motion._semantic_annotation[cur_label][cur_entry]
        new_cur_idx_list = cur_idx_list
        new_next_idx_list = next_idx_list
        
        if next_idx_list[0] >= frame_idx and frame_idx <= cur_idx_list[-1]: # next is right to cur_label
            next_start_idx = next_idx_list[0]
            next_end_idx = next_idx_list[-1]
            cur_start_idx = cur_idx_list[0]
            cur_end_idx = cur_idx_list[-1]
            new_next_idx_list += list(range(frame_idx, cur_end_idx+1))
            new_cur_idx_list = list(range(cur_start_idx, frame_idx))
            self.edit_controller._motion._semantic_annotation[next_label][next_entry] = new_next_idx_list
            self.edit_controller._motion._semantic_annotation[cur_label][cur_entry] = new_cur_idx_list
            print("next is right")
        elif  next_idx_list[0] <= frame_idx and  frame_idx  <= cur_idx_list[-1] : # next is left to cur_label
            next_end_idx = next_idx_list[-1]
            cur_end_idx = cur_idx_list[-1]
            new_next_idx_list += list(range(next_end_idx, frame_idx))
            new_cur_idx_list = list(range(frame_idx, cur_end_idx+1))
            print("next is left")
            self.edit_controller._motion._semantic_annotation[next_label][next_entry] = new_next_idx_list
            self.edit_controller._motion._semantic_annotation[cur_label][cur_entry] = new_cur_idx_list

    def clean_annotation_sections(self):
        """ order sections remove empty sections and merge neighboring sections"""
        annotations= self.edit_controller._motion._semantic_annotation
        for label in  annotations:
            n_sections_before = len(annotations[label])
            new_sections = []
            for i, indices in enumerate(annotations[label]):
                if len(indices) > 0:
                    new_sections.append(indices)
                else:
                    print("delete section", i)

            new_sections.sort(key=lambda x : x[0]) # order sections

            n_new_sections = len(new_sections)
            merged_new_sections = []
            merged_idx = -1
            for i in range(0, n_new_sections):
                if i == merged_idx:
                    continue
                if i+1 < n_new_sections and (new_sections[i+1][0] -1 in new_sections[i] or new_sections[i+1][0] in new_sections): # merge right
                    merged_idx = i+1
                    merged_new_sections.append(new_sections[i]+new_sections[i+1])
                    print("merged sections", i, i+1)
                else:
                    merged_new_sections.append(new_sections[i])
            annotations[label] = merged_new_sections
            print("before merge:",n_sections_before,"after merge:", len(merged_new_sections))

        self.edit_controller._motion._semantic_annotation = annotations


    def merge_annotation(self):
        frame_idx = self.edit_controller._motion.frame_idx
        labels = list(self.edit_controller._motion._semantic_annotation.keys())
        if len(labels) > 1:
            current_label = self.get_annotation_of_frame(frame_idx)
            next_closest_label = self.get_next_closest_label(current_label)
            self.merge_annotation_sections(current_label, next_closest_label)
            self.init_label_time_line()
            self.fill_label_combobox()

    def merge_annotation_sections(self, label_a, label_b):
        print("merge", label_a, "and", label_b)
        idx_list_a = self.edit_controller._motion._semantic_annotation[label_a]
        idx_list_b = self.edit_controller._motion._semantic_annotation[label_b]
        if idx_list_a[0] <= idx_list_b[0]:
            start_idx = idx_list_a[0]
            end_idx = idx_list_b[-1]
            merged_annotation = list(range(start_idx, end_idx))
        else:
            start_idx = idx_list_b[0]
            end_idx = idx_list_a[-1]
            merged_annotation = list(range(start_idx, end_idx))

        new_annotations = list()
        new_color_map = list()
        added_merged_section = False
        for idx, label in enumerate(self.edit_controller._motion._semantic_annotation.keys()):
            if label != label_a and label != label_b: # copy
                new_annotations.append(self.edit_controller._motion._semantic_annotation[label])
                new_color_map.append(self.edit_controller._motion.label_color_map[label])
            elif not added_merged_section: #split at frame_idx
                new_annotations.append(merged_annotation)
                new_color_map.append([0, 0, 0])
                added_merged_section = True

        self.edit_controller._motion._semantic_annotation = collections.OrderedDict()
        self.edit_controller._motion.label_color_map = collections.OrderedDict()
        for idx, value in enumerate(new_annotations):
            new_label = "c" + str(idx)
            self.edit_controller._motion._semantic_annotation[new_label] = new_annotations[idx]
            self.edit_controller._motion.label_color_map[new_label] = new_color_map[idx]

    def get_next_closest_label_entry(self, label, entry):
        frame_idx = self.edit_controller._motion.frame_idx
        indices = self.edit_controller._motion._semantic_annotation[label][entry]
        indices.sort()
        if abs(frame_idx -indices[0]) < abs(frame_idx - indices[-1]):
            return self.get_prev_label_entry(label, entry)
        else:
            return self.get_next_label_entry(label, entry)

    def get_next_label_entry(self, label, entry):
        indices = self.edit_controller._motion._semantic_annotation[label][entry]
        indices.sort()
        return self.get_annotation_of_frame(indices[-1], ignore_label=label)

    def get_prev_label_entry(self, label, entry):
        indices = self.edit_controller._motion._semantic_annotation[label][entry]
        indices.sort()
        return self.get_annotation_of_frame(indices[0], ignore_label=label)   

    def get_next_closest_label(self, label):
        frame_idx = self.edit_controller._motion.frame_idx
        indices = self.edit_controller._motion._semantic_annotation[label]
        indices.sort()
    
        if abs(frame_idx -indices[0]) < abs(frame_idx - indices[-1]):
            return self.get_prev_label(label)
        else:
            return self.get_next_label(label)


    def get_next_label(self, label):
        indices = self.edit_controller._motion._semantic_annotation[label]
        indices.sort()
        return self.get_annotation_of_frame(indices[-1], ignore_label=label)

    def get_prev_label(self, label):
        indices = self.edit_controller._motion._semantic_annotation[label]
        indices.sort()
        return self.get_annotation_of_frame(indices[0], ignore_label=label)   

    def clear_timeline(self):
        #self._controller._motion._semantic_annotation = collections.OrderedDict()
        #self._controller._motion.label_color_map = dict()
        #self.init_label_time_line()
        annotations = self.edit_controller._motion._semantic_annotation
        if annotations is not None:
            label = str(self.labelComboBox.currentText())
            if label in list(annotations.keys()):
                annotations[label] = []
        self.edit_controller._motion._semantic_annotation = annotations
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
