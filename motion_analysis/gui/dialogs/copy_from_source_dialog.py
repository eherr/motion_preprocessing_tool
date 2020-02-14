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
from PySide2.QtWidgets import QDialog, QListWidgetItem, QTableWidgetItem, QTableWidget
from PySide2.QtCore import QTimer, Qt
from PySide2.QtGui import QColor
from motion_analysis.gui.layout.copy_from_source_dialog_ui import Ui_Dialog
from motion_analysis.gui.dialogs.utils import get_animation_controllers
from motion_analysis.gui.widgets.scene_viewer import SceneViewerWidget
from vis_utils.scene.editor_scene import EditorScene
from anim_utils.animation_data.motion_blending import create_transition_for_joints_using_slerp, BLEND_DIRECTION_FORWARD, BLEND_DIRECTION_BACKWARD, smooth_translation_in_quat_frames
from anim_utils.motion_editing.cubic_motion_spline import CubicMotionSpline
from OpenGL.GL import *


def stretch_motion(skeleton, frames, n_dest_frames):
    n_frames = len(frames)
    times = list(range(0, n_frames))
    spline = CubicMotionSpline.fit_frames(skeleton, times, frames)
    step_size = (n_frames-1)/n_dest_frames
    streched_times = np.arange(0,n_frames-1,step_size)
    #print(streched_times)
    new_frames = []
    for t in streched_times:
        f = spline.evaluate(t)
        new_frames.append(f)
    print("new frames", len(new_frames))
    return new_frames


class CopyFromSourceDialog(QDialog, Ui_Dialog):
    def __init__(self, controller, scene, share_widget, parent=None):
        QDialog.__init__(self, parent)
        Ui_Dialog.setupUi(self, self)
        
        self.leftView = SceneViewerWidget(parent, share_widget, size=(400,400), use_frame_buffer=False)
        self.leftView.setObjectName("left")
        self.leftView.setMinimumSize(400,400)
        self.leftView.initializeGL()
        self.leftView.enable_mouse_interaction = False
        self.leftViewerLayout.addWidget(self.leftView)

        self.rightView = SceneViewerWidget(parent, self.leftView, size=(400,400), use_frame_buffer=False)
        self.rightView.setObjectName("right")
        self.rightView.setMinimumSize(400,400)
        self.rightView.initializeGL()
        self.rightView.enable_mouse_interaction = False
        self.rightViewerLayout.addWidget(self.rightView)

        self.fps = 60
        self.dt = 1/60
        self.timer = QTimer()
        self.timer.timeout.connect(self.draw)
        self.timer.start(0)
        self.timer.setInterval(1000.0/self.fps)
        self.scene = scene
        self.right_controller = None
        self.skeleton = None
        self.rightView.makeCurrent()
        self.right_scene = EditorScene(True)
        if controller is not None:
            self.right_controller = self.copy_controller(controller, self.right_scene)
            self.skeleton = self.right_controller.get_skeleton()
            n_frames = self.right_controller.getNumberOfFrames()
            self._fill_list_with_joints(controller)
        else:
            n_frames = 0
        
        self.leftView.makeCurrent()
        self.left_scene = EditorScene(True)
        
        self.copyButton.clicked.connect(self.copy_from_left_to_right)
        self.left_controller = None
        self.controllers = dict()
        self._fill_list_with_scene_objects(scene)
        
        self.selectButton.clicked.connect(self.slot_accept)
        self.cancelButton.clicked.connect(self.slot_reject)

        self.selectAllJointsButton.clicked.connect(self.slot_select_all_joints)
        self.selectJointChildrenButton.clicked.connect(self.slot_select_joint_children)
        self.deselectJointChildrenButton.clicked.connect(self.slot_deselect_joint_children)
        self.clearSelectedJointsButton.clicked.connect(self.slot_clear_all_joints)

        self.leftStartFrameSlider.valueChanged.connect(self.left_slider_frame_changed)
        self.leftEndFrameSlider.valueChanged.connect(self.left_slider_frame_changed)
        self.leftStartFrameSpinBox.valueChanged.connect(self.left_spinbox_frame_changed)
        self.leftEndFrameSpinBox.valueChanged.connect(self.left_spinbox_frame_changed)


        self.leftDisplayFrameSlider.valueChanged.connect(self.left_display_changed)
        self.leftDisplayFrameSpinBox.valueChanged.connect(self.left_display_changed)

        self.rightStartFrameSlider.valueChanged.connect(self.right_slider_frame_changed)
        self.rightStartFrameSpinBox.valueChanged.connect(self.right_spinbox_frame_changed)
        self.rightEndFrameSlider.valueChanged.connect(self.right_slider_frame_changed)
        self.rightEndFrameSpinBox.valueChanged.connect(self.right_spinbox_frame_changed)

        self.rightDisplayFrameSpinBox.valueChanged.connect(self.right_display_changed)
        self.rightDisplayFrameSlider.valueChanged.connect(self.right_display_changed)

        self.sceneObjectListWidget.itemClicked.connect(self.load_src_controller)
        self.success = False
        self.n_frames = n_frames
        self.start_frame = 0
        self.end_frame = n_frames-1#
        self.set_right_frame_range()
        self.initialized = False

    def closeEvent(self, e):
        self.timer.stop()
        self.leftView.makeCurrent()
        del self.leftView
        self.rightView.makeCurrent()
        del self.rightView

    def copy_from_left_to_right(self):
        """ copy values from left start to end to right start to end and interpolate with the rest """
        if self.left_controller is not None and self.right_controller is not None and self.skeleton is not None:
            left_frames = self.left_controller.get_frames()
            right_frames = self.right_controller.get_frames()

            n_right_frames = self.right_controller.getNumberOfFrames()
            print("loaded", len(right_frames), n_right_frames)
            dest_start = self.rightStartFrameSlider.value()
            src_start = self.leftStartFrameSlider.value()
            src_end = self.leftEndFrameSlider.value()+1
            dest_end = self.rightEndFrameSlider.value()+1


            n_dest_frames = dest_end - dest_start
            if n_dest_frames <= 0:
                print("wrong dest frames", dest_start, dest_end)
                return

            #extract number of copied frames from source
            n_copied_frames = src_end - src_start
            if n_copied_frames <= 0:
                print("wrong src frames", src_start, src_end)
                return
         
            
            joint_list, joint_index_list = self.get_selected_joints()
            print("copy", joint_list, joint_index_list)
            
            modified_frames = self.copy_joint_values(left_frames, right_frames, joint_list, joint_index_list, src_start, src_end, dest_start, dest_end)
            n_blend_range = int(self.blendRangeLineEdit.text())
            if n_blend_range > 0:
                modified_frames = self.apply_blending(modified_frames, joint_list, joint_index_list, dest_start, dest_end-1, n_blend_range)
            self.right_controller.replace_frames(modified_frames)
            n_new_right_frames = self.right_controller.getNumberOfFrames()
            print("finished overwriting", n_right_frames, n_new_right_frames)
        
    def copy_joint_values(self, left_frames, right_frames, joint_list, joint_index_list, src_start, src_end, dest_start, dest_end):
        n_copied_frames = src_end - src_start
        n_dest_frames = dest_end - dest_start
        modified_frames = np.array(right_frames)
        if n_copied_frames > 1:
            src_frames = stretch_motion(self.skeleton, left_frames[src_start:src_end], n_dest_frames)
        else:
            src_frames = []
            for i in range(n_dest_frames):
                src_frames.append(left_frames[src_start])
            src_frames = np.array(src_frames)
        print("copy ", n_copied_frames, n_dest_frames)
        for frame_idx in range(n_dest_frames):
            modified_frames[dest_start+frame_idx][joint_index_list] = src_frames[frame_idx][joint_index_list]
        return modified_frames

    def apply_blending(self, frames, joint_list, joint_index_list, dest_start, dest_end, n_blend_range):
        n_frames = len(frames)
        blend_start = max(dest_start- n_blend_range, 0)
        start_window = dest_start -blend_start
        blend_end =  min(dest_end +n_blend_range, n_frames-1)
        end_window = blend_end- dest_end
         #remove root indices
        print("blend ", dest_start, dest_end, n_blend_range, start_window, end_window)
        quat_joint_index_list = list(joint_index_list)
        if self.skeleton.root in joint_list:
            # apply root smnoothing and remove from index list
            if start_window > 0:
                frames = smooth_translation_in_quat_frames(frames, dest_start, start_window)
            if end_window > 0:
                frames = smooth_translation_in_quat_frames(frames, dest_end, end_window)
            for i in range(3):
                quat_joint_index_list.remove(i)
        
        if len(quat_joint_index_list) > 0:
            o = 0
            for j in joint_list:
                q_indices = quat_joint_index_list[o:o+4]
                if start_window > 0:
                    frames = create_transition_for_joints_using_slerp(frames, q_indices, blend_start, dest_start, start_window, BLEND_DIRECTION_FORWARD)
                if end_window > 0:
                    print(j, q_indices)
                    frames = create_transition_for_joints_using_slerp(frames, q_indices, dest_end, blend_end, end_window, BLEND_DIRECTION_BACKWARD)
                o += 4
        
        return frames
        
    def get_selected_joints(self):
        joint_list = []
        joint_index_list = []
        for row_idx in range(self.jointTableWidget.rowCount()):
            index_cell = self.jointTableWidget.item(row_idx,0)
            if index_cell.checkState() == Qt.Checked:
                name_cell = self.jointTableWidget.item(row_idx,1)
                joint_name = str(name_cell.text())
                joint_list.append(joint_name)
                if joint_name == self.skeleton.root:
                    offset = 0
                    n_channels = 7
                else:
                    offset = self.skeleton.nodes[joint_name].quaternion_frame_index * 4 + 3
                    n_channels = 4
                joint_index_list += list(range(offset,offset+n_channels))
        return joint_list, joint_index_list


    def _fill_list_with_joints(self, controller):
        #self.jointTableWidget.clear()
        for joint_name in controller.get_animated_joints():
            insertRow = self.jointTableWidget.rowCount()
            self.jointTableWidget.insertRow(insertRow)
            indexItem = QTableWidgetItem("")
            indexItem.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
            indexItem.setCheckState(Qt.Unchecked)
            self.jointTableWidget.setItem(insertRow, 0, indexItem)
            self.jointTableWidget.setItem(insertRow, 1, QTableWidgetItem(str(joint_name)))

    def copy_controller(self, controller, target_scene):
        skeleton = controller.get_skeleton_copy()
        mv = controller.get_motion_vector_copy()
        o = target_scene.object_builder.create_object("animation_controller","", 
                                            skeleton, mv, mv.frame_time, 
                                            semantic_annotation=None) 
        return o._components["animation_controller"]

    def load_src_controller(self, item):
        if item is None:
            return
        selected_item = str(self.sceneObjectListWidget.currentItem().text())
        if self.left_controller is not None:
            node_id = self.left_controller.scene_object.node_id
            self.left_scene.removeObject(node_id)
        src_controller = self.controllers[selected_item]
        self.left_controller = self.copy_controller(src_controller, self.left_scene)

        n_frames = src_controller.getNumberOfFrames()

        self.leftStartFrameSlider.setRange(0,  n_frames-1)
        self.leftStartFrameSlider.setValue(0)
        self.leftEndFrameSlider.setRange(0, n_frames-1)
        self.leftEndFrameSlider.setValue(n_frames-1)
        self.leftDisplayFrameSlider.setRange(0, n_frames-1)
        self.leftDisplayFrameSlider.setRange(0, n_frames-1)


    def draw(self):
        """ draw current scene on the given view
        (note before calling this function the context of the view has to be set as current using makeCurrent() and afterwards the doubble buffer has to swapped to display the current frame swapBuffers())
        """
        if not self.initialized:
            if self.leftView.graphics_context is not None and self.rightView.graphics_context is not None:
                self.leftView.resize(400,400)
                self.rightView.resize(400,400)
                self.initialized = True
        self.left_scene.update(self.dt)
        self.leftView.makeCurrent()
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        self.leftView.graphics_context.render(self.left_scene)
        self.leftView.swapBuffers()


        self.right_scene.update(self.dt)
        self.rightView.makeCurrent()
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        self.rightView.graphics_context.render(self.right_scene)
        self.rightView.swapBuffers()
        #print(len(self.right_scene.lightSources))

    def right_display_changed(self, frame_idx):
        if self.right_controller is not None:
            self.right_controller.setCurrentFrameNumber(frame_idx)
            self.rightDisplayFrameSpinBox.setValue(frame_idx)

    def left_display_changed(self, frame_idx):
        if self.left_controller is not None:
            self.left_controller.setCurrentFrameNumber(frame_idx)
            self.leftDisplayFrameSpinBox.setValue(frame_idx)

    
    def _fill_list_with_scene_objects(self, scene):
        for sceneObject in get_animation_controllers(scene):
            item = QListWidgetItem()
            item.setText(sceneObject.name)
            item.setData(Qt.UserRole, sceneObject.node_id)
            self.sceneObjectListWidget.addItem(item)
            self.controllers[sceneObject.name] = sceneObject._components["animation_controller"]

    def set_right_frame_range(self):
        self.leftStartFrameSlider.setRange(0, self.n_frames-1)
        self.leftEndFrameSlider.setRange(0, self.n_frames-1)
        self.leftStartFrameSpinBox.setRange(0, self.n_frames-1)
        self.leftEndFrameSpinBox.setRange(0, self.n_frames-1)

        self.leftEndFrameSlider.setValue(self.n_frames - 1)
        self.leftEndFrameSpinBox.setValue(self.n_frames - 1)


        self.rightStartFrameSlider.setRange(0, self.n_frames-1)
        self.rightStartFrameSpinBox.setRange(0, self.n_frames-1)

        self.rightEndFrameSlider.setRange(0, self.n_frames-1)
        self.rightEndFrameSpinBox.setRange(0, self.n_frames-1)
        self.rightEndFrameSlider.setValue(self.n_frames - 1)
        self.rightEndFrameSpinBox.setValue(self.n_frames - 1)

        self.rightDisplayFrameSlider.setRange(0, self.n_frames-1)
        self.rightDisplayFrameSpinBox.setRange(0, self.n_frames-1)


    def left_spinbox_frame_changed(self, frame):
        self.leftStartFrameSlider.setValue(self.leftStartFrameSpinBox.value())
        self.leftEndFrameSlider.setValue(self.leftEndFrameSpinBox.value())

    def left_slider_frame_changed(self, frame):
        self.leftStartFrameSpinBox.setValue(self.leftStartFrameSlider.value())
        self.leftEndFrameSpinBox.setValue(self.leftEndFrameSlider.value())

    def right_spinbox_frame_changed(self, frame):
        self.rightStartFrameSlider.setValue(self.rightStartFrameSpinBox.value())
        self.rightEndFrameSlider.setValue(self.rightEndFrameSpinBox.value())

    def right_slider_frame_changed(self, frame):
        self.rightStartFrameSpinBox.setValue(self.rightStartFrameSlider.value())
        self.rightEndFrameSpinBox.setValue(self.rightEndFrameSlider.value())

    def slot_accept(self):
        self.success = True
        self.close()

    def slot_reject(self):
        self.close()

    def slot_select_all_joints(self):
        for row_idx in range(self.jointTableWidget.rowCount()):
            index_cell = self.jointTableWidget.item(row_idx,0)
            index_cell.setCheckState(Qt.Checked)

    def slot_clear_all_joints(self):
        for row_idx in range(self.jointTableWidget.rowCount()):
            index_cell = self.jointTableWidget.item(row_idx,0)
            index_cell.setCheckState(Qt.Unchecked)

    def slot_select_joint_children(self):
        for row_idx in range(self.jointTableWidget.rowCount()):
            index_cell = self.jointTableWidget.item(row_idx, 0)
            name_cell = self.jointTableWidget.item(row_idx, 1)
            if index_cell.isSelected() or name_cell.isSelected():
                joint_name = str(name_cell.text())
                self.change_joint_children_state(joint_name, Qt.Checked)

    def slot_deselect_joint_children(self):
        for row_idx in range(self.jointTableWidget.rowCount()):
            index_cell = self.jointTableWidget.item(row_idx, 0)
            name_cell = self.jointTableWidget.item(row_idx, 1)
            if index_cell.isSelected() or name_cell.isSelected():
                joint_name = str(name_cell.text())
                self.change_joint_children_state(joint_name, Qt.Unchecked)


    def change_joint_children_state(self, joint_name, state):
        self.change_joint_state(joint_name, state)
        if joint_name in self.skeleton.nodes:
            for n in self.skeleton.nodes[joint_name].children:
                self.change_joint_children_state(n.node_name, state)

    def change_joint_state(self, joint_name, state):
        print("select", joint_name)
        for row_idx in range(self.jointTableWidget.rowCount()):
            name_cell = self.jointTableWidget.item(row_idx, 1)
            if joint_name == str(name_cell.text()):
                index_cell = self.jointTableWidget.item(row_idx, 0)
                index_cell.setCheckState(state)
                break

