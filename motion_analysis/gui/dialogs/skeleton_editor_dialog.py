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
import math
import numpy as np
from copy import copy
from PySide2.QtWidgets import  QDialog, QListWidgetItem, QTableWidgetItem, QTableWidget, QFileDialog
from PySide2.QtCore import QTimer, Qt
from PySide2.QtGui import QColor
from OpenGL.GL import *
from motion_analysis.gui.layout.skeleton_editor_dialog_ui import Ui_Dialog
from .utils import get_animation_controllers
from transformations import quaternion_matrix, quaternion_multiply, quaternion_about_axis
from motion_analysis.gui.widgets.scene_viewer import SceneViewerWidget
from vis_utils.animation import load_motion_from_bvh
from vis_utils.scene.editor_scene import EditorScene
from vis_utils.animation.animation_editor import AnimationEditor
from vis_utils.io import save_json_file
from anim_utils.animation_data import BVHReader, BVHWriter, MotionVector, SkeletonBuilder
from anim_utils.retargeting.analytical import create_local_cos_map_from_skeleton_axes_with_map, find_rotation_between_vectors, OPENGL_UP_AXIS
from anim_utils.animation_data.skeleton_models import STANDARD_MIRROR_MAP, STANDARD_MIRROR_MAP_LEFT, STANDARD_MIRROR_MAP_RIGHT, JOINT_CONSTRAINTS

DEFAULT_TARGET_CS_UP = [1,0,0]

def normalize(v):
    return v / np.linalg.norm(v)

def quaternion_from_vector_to_vector(a, b):
    """src: http://stackoverflow.com/questions/1171849/finding-quaternion-representing-the-rotation-from-one-vector-to-another
    http://wiki.ogre3d.org/Quaternion+and+Rotation+Primer"""

    v = np.cross(a, b)
    w = np.sqrt((np.linalg.norm(a) ** 2) * (np.linalg.norm(b) ** 2)) + np.dot(a, b)
    q = np.array([w, v[0], v[1], v[2]])
    if np.dot(q,q) != 0:
        return q/ np.linalg.norm(q)
    else:
        idx = np.nonzero(a)[0]
        q = np.array([0, 0, 0, 0])
        q[1 + ((idx + 1) % 2)] = 1 # [0, 0, 1, 0] for a rotation of 180 around y axis
        return q
    
def rotate_vector(q, v):
    m = quaternion_matrix(q)[:3, :3]
    v = np.dot(m, v)
    return v

X = np.array([1,0,0])
Y = np.array([0,1,0])

STANDARD_JOINTS = ["","root","pelvis", "spine", "spine_1", "spine_2", "neck", "left_clavicle", "head", "left_shoulder", "left_elbow", "left_wrist", "right_clavicle", "right_shoulder",
                    "left_hip", "left_knee", "left_ankle", "left_toe", "right_elbow", "right_wrist", "right_hip", "right_knee", "right_ankle", "right_toe"]

STANDARD_JOINTS += ["left_thumb_base","left_thumb_mid", "left_thumb_tip","left_thumb_end",
                    "left_index_finger_root","left_index_finger_base","left_index_finger_mid", "left_index_finger_tip","left_index_finger_end",
                    "left_middle_finger_root","left_middle_finger_base","left_middle_finger_mid","left_middle_finger_tip","left_middle_finger_end",
                    "left_ring_finger_root","left_ring_finger_base","left_ring_finger_mid","left_ring_finger_tip", "left_ring_finger_end",
                    "left_pinky_finger_root","left_pinky_finger_base","left_pinky_finger_mid","left_pinky_finger_tip", "left_pinky_finger_end",
                   
                    "right_thumb_base","right_thumb_mid","right_thumb_tip","right_thumb_end",
                    "right_index_finger_root","right_index_finger_base","right_index_finger_mid","right_index_finger_tip","right_index_finger_end",
                    "right_middle_finger_root","right_middle_finger_base","right_middle_finger_mid","right_middle_finger_tip","right_middle_finger_end",
                    "right_ring_finger_root","right_ring_finger_base","right_ring_finger_mid","right_ring_finger_tip","right_ring_finger_end",
                    "right_pinky_finger_root","right_pinky_finger_base","right_pinky_finger_mid","right_pinky_finger_tip","right_pinky_finger_end"
                    ]
def find_key(joint_map,value):
    for key,v in joint_map.items():
        if value == v:
            return key
    return None

def axes_to_q(g_twist, g_swing, flip=False):
    q = [1, 0, 0, 0] 
    q_y = quaternion_from_vector_to_vector(Y, g_twist)
    q_y = normalize(q_y)
    q = quaternion_multiply(q_y, q)
    X_prime = rotate_vector(q_y, X)
    X_prime = normalize(X_prime)
    q_x = quaternion_from_vector_to_vector(X_prime, g_swing)
    q_x = normalize(q_x)
    q = quaternion_multiply(q_x, q)
    q = normalize(q)
    Y_prime = rotate_vector(q, Y)
    dot = np.dot(Y_prime, g_twist)
    #dot = min(dot,1)
    dot = max(dot,-1)
    if dot == -1:
        q180 = quaternion_about_axis(np.deg2rad(180), g_swing)
        q180 = normalize(q180)
        q = quaternion_multiply(q180, q)
        q = normalize(q)
    elif abs(dot) != 1.0:
        q_y = quaternion_from_vector_to_vector(Y_prime, g_twist)
        q = quaternion_multiply(q_y, q)
        q = normalize(q)
    return q


OPENGL_UP_AXIS = [0,1,0]
OPENGL_FORWARD_AXIS = [0,0,1]
def get_axis_correction(skeleton, joint_name, up_vector, target_vector=OPENGL_UP_AXIS):
    node = skeleton.nodes[joint_name]
    t_pose_global_m = node.get_global_matrix(skeleton.reference_frame)
    global_original = np.dot(t_pose_global_m[:3, :3], up_vector)
    global_original = normalize(global_original)
    qoffset = find_rotation_between_vectors(global_original, target_vector)
    return qoffset



def get_child_index(skeleton, joint_name):
    for idx, c in enumerate(skeleton.nodes[joint_name].parent.children):
        if c.node_name == joint_name:
            return idx 
    return -1

def get_traversal_map_from_parent(skeleton, joint_name, target_parent):
    traversal_map = []
    while joint_name != target_parent and skeleton.nodes[joint_name].parent is not None:
        #print("get traversal map", joint_name, target_parent, )
        idx = get_child_index(skeleton, joint_name)
        if idx == -1:
            print("Error index is none", joint_name, skeleton.nodes[joint_name].parent.children)
            break
        traversal_map.append(idx)
        joint_name = skeleton.nodes[joint_name].parent.node_name
    return list(reversed(traversal_map))

def get_joint_from_traversal_map(skeleton, traversal_map, joint_name):
    for idx in traversal_map:
        joint_name = skeleton.nodes[joint_name].children[idx].node_name
    return joint_name


def generate_sequence_from_root_to_joint(skeleton, skeleton_model, joint_key_list, joint_val_list, joint_name, known_joints, partial_mirror_map):
    joint_list = []
    while joint_name != "pelvis":
        #print("add", joint_name)
        joint_list.append(joint_name)
        skel_j = skeleton_model["joints"][joint_name]
        parent = skeleton.nodes[skel_j].parent
        while parent is not None and parent.node_name not in joint_val_list:
            parent = parent.parent
        if parent is None:
            print("Error: parent is None")
            break
        idx = joint_val_list.index(parent.node_name)
        joint_name = joint_key_list[idx]
        skel_j = skeleton_model["joints"][joint_name]
        if (len(joint_list)> 1 and joint_name in known_joints) or  joint_name not in partial_mirror_map:
            break
    return list(reversed(joint_list))

def mirror_sequence(skeleton, src_joint_list, skeleton_model):
    """ mirror sequence by corresponding joint hierarchy"""
    standard_mirror_map = STANDARD_MIRROR_MAP 
    joint_map = skeleton_model["joints"]
    parent_src = src_joint_list[0]
    parent_dst = standard_mirror_map[parent_src]
    if parent_dst not in joint_map:
        return skeleton_model
    for src in src_joint_list[1:]:
        src_j = joint_map[src]
        dst = standard_mirror_map[src]
        src_parent_j = joint_map[parent_src]
        parent_dst_j = joint_map[parent_dst]
        traversal_map = get_traversal_map_from_parent(skeleton, src_j, src_parent_j)
        dst_j = get_joint_from_traversal_map(skeleton, traversal_map, parent_dst_j)
        skeleton_model["joints"][dst] = dst_j
        print("set", dst, dst_j)
        #src_cos_map = skeleton_model["cost_map"][src_j]
        #skeleton_model["cost_map"][dst_j] = src_cos_map
        parent_src = src
        parent_dst = dst

    return skeleton_model

def mirror_join_map(skeleton, skeleton_model, partial_mirror_map):
    """ for each end effector generate a sequence to the root or the last mirrored joint and then try to mirror the sequence"""
    known_joints = set()
    joint_key_list = list(skeleton_model["joints"].keys()) 
    joint_val_list = list(skeleton_model["joints"].values()) 
    for key in partial_mirror_map:
        print("try to mirror  ", key)
        if key in known_joints:
            print("seen joint already")
            continue
        if key not in skeleton_model["joints"] :
            print(key, "not in joint map")
            continue
        if skeleton_model["joints"][key] is None:
            print("joint map set to None")
            continue
        #skel_j = skeleton_model["joints"][key]
        #if len(skeleton.nodes[skel_j].children) > 0:
        #    print("too many children")
        #    continue
        sequence = generate_sequence_from_root_to_joint(skeleton, skeleton_model, joint_key_list, joint_val_list, key, known_joints, partial_mirror_map)
        print("generate ", sequence)
        for k in sequence:
            known_joints.add(k)
        skeleton_model = mirror_sequence(skeleton, sequence, skeleton_model)
    return skeleton_model
    

class SkeletonEditorDialog(QDialog, Ui_Dialog):
    def __init__(self, name, skeleton, share_widget, parent=None, enable_line_edit=False, skeleton_model=None):
        self.initialized = False
        QDialog.__init__(self, parent)
        Ui_Dialog.setupUi(self, self)
        self.view = SceneViewerWidget(parent, share_widget, size=(400,400))
        self.view.setObjectName("left")
        self.view.setMinimumSize(400,400)
        self.view.initializeGL()
        self.nameLineEdit.setText(name)
        self.nameLineEdit.setEnabled(enable_line_edit)
        self.name = name
        self.view.enable_mouse_interaction = True
        self.view.mouse_click.connect(self.on_mouse_click)
        self.viewerLayout.addWidget(self.view)


        self.radius = 1.5
        self.fps = 60
        self.dt = 1/60
        self.timer = QTimer()
        self.timer.timeout.connect(self.draw)
        self.timer.start(0)
        self.timer.setInterval(1000.0/self.fps)
        self.skeleton = skeleton
        self.view.makeCurrent()
        self.scene = EditorScene(True)
        self.scene.enable_scene_edit_widget = True
        
        if skeleton_model is not None:
            self.skeleton_model = skeleton_model
        elif skeleton.skeleton_model is not None:
            self.skeleton_model = skeleton.skeleton_model
        else:
            self.skeleton_model = dict()
            print("create new skeleton model")
        if "cos_map" not in self.skeleton_model:
            self.skeleton_model["cos_map"] = dict()
        if "joints" not in self.skeleton_model:
            self.skeleton_model["joints"] = dict()
        if "joint_constraints" not in self.skeleton_model:
            self.skeleton_model["joint_constraints"] = dict()

        motion_vector = MotionVector()
        self.reference_frame = skeleton.reference_frame
        print(self.reference_frame[:3])
        motion_vector.frames = [skeleton.reference_frame]
        motion_vector.n_frames = 1
        o = self.scene.object_builder.create_object("animation_controller", "skeleton", skeleton, motion_vector, skeleton.frame_time)
        self.controller = o._components["animation_controller"]
        self.skeleton = self.controller.get_skeleton()
        self.init_joints(self.controller)
        self.fill_joint_map()

        self.selectButton.clicked.connect(self.slot_accept)
        self.cancelButton.clicked.connect(self.slot_reject)
        self.applyTwistRotationButton.clicked.connect(self.slot_set_twist)
        self.applySwingRotationButton.clicked.connect(self.slot_set_swing)

        self.setOrthogonalTwistButton.clicked.connect(self.slot_set_orthogonal_twist)
        self.setOrthogonalSwingButton.clicked.connect(self.slot_set_orthogonal_swing)
        self.rotateTwistButton.clicked.connect(self.slot_rotate_twist)
        self.rotateSwingButton.clicked.connect(self.slot_rotate_swing)

        self.flipTwistButton.clicked.connect(self.slot_flip_twist)
        self.flipSwingButton.clicked.connect(self.slot_flip_swing)

        self.flipZAxisButton.clicked.connect(self.slot_flip_z_axis)
        self.alignToUpAxisButton.clicked.connect(self.slot_align_to_up_axis)
        self.alignToForwardAxisButton.clicked.connect(self.slot_align_to_forward_axis)

        self.guessSelectedButton.clicked.connect(self.slot_guess_selected_cos_map)
        self.resetSelectedCosButton.clicked.connect(self.slot_reset_selected_cos_map)
        self.guessAllCosButton.clicked.connect(self.slot_guess_cos_map)
        self.resetAllCosButton.clicked.connect(self.slot_reset_cos_map)
        self.loadDefaultPoseButton.clicked.connect(self.slot_load_default_pose)
        self.applyScaleButton.clicked.connect(self.slot_apply_scale)
        self.jointMapComboBox.currentIndexChanged.connect(self.slot_update_joint_map)
        self.aligningRootComboBox.currentIndexChanged.connect(self.slot_update_aligning_root_joint)

        self.mirrorLeftButton.clicked.connect(self.slot_mirror_left_to_right)
        self.mirrorRightButton.clicked.connect(self.slot_mirror_right_to_left)

        self.is_updating_joint_info = False
        self.success = False
        self.initialized = False
        self.skeleton_data = None
        self.precision = 3
        self.aligning_root_node = self.skeleton.aligning_root_node
        self.fill_root_combobox()
        self.init_aligning_root_node()


    def init_aligning_root_node(self):
        print("init",self.skeleton.root, self.skeleton.aligning_root_node)
        if self.aligning_root_node is None:
            self.aligning_root_node = self.skeleton.root
        if self.aligning_root_node is not None:
            index = self.aligningRootComboBox.findText(self.aligning_root_node, Qt.MatchFixedString)
            print("found index", index, self.aligning_root_node)
            if index >= 0:
                self.aligningRootComboBox.setCurrentIndex(index)

    def closeEvent(self, e):
         self.timer.stop()
         self.view.makeCurrent()
         del self.view

    def on_mouse_click(self, event, ray_start, ray_dir, pos, node_id):
        if event.button() == Qt.LeftButton:
            self.scene.select_object(node_id)            
            joint_knob = self.get_selected_joint()
            self.update_joint_info(joint_knob)
            

    def update_joint_info(self, joint_knob):
        self.is_updating_joint_info = True
        self.scene.scene_edit_widget.reset_rotation()
        self.jointMapComboBox.setCurrentIndex(0)
        label = "Selected Joint: "
        if joint_knob is None:
            label += "None"
            self.jointLabel.setText(label)
            self.is_updating_joint_info = False
            return

        label += joint_knob.joint_name
        joint_name = joint_knob.joint_name
        if "joints" in self.skeleton_model:
            key = find_key(self.skeleton_model["joints"], joint_name)
            print("key", joint_name, key)
            if key is not None:
                index = self.jointMapComboBox.findText(key, Qt.MatchFixedString)
                if index >= 0:
                    self.jointMapComboBox.setCurrentIndex(index)

        if "cos_map" in self.skeleton_model and joint_name in self.skeleton_model["cos_map"]:
            x_vector = self.skeleton_model["cos_map"][joint_name]["x"]
            if x_vector is None:
                x_vector = [1,0,0]
                self.skeleton_model["cos_map"][joint_name]["x"] = x_vector
            y_vector = self.skeleton_model["cos_map"][joint_name]["y"]
            if y_vector is None:
                y_vector = [0,1,0]
                self.skeleton_model["cos_map"][joint_name]["y"] = y_vector
            swing = np.round(x_vector, self.precision)
            twist = np.round(y_vector, self.precision)
            self.set_swing_text(swing)
            self.set_twist_text(twist)
            m = self.skeleton.nodes[joint_name].get_global_matrix(self.reference_frame)[:3,:3]
            g_swing = np.dot(m, swing)
            g_swing = normalize(g_swing)
            g_twist = np.dot(m, twist)
            g_twist = normalize(g_twist)
            q = axes_to_q(g_twist, g_swing)
            m = quaternion_matrix(q)
            #print("g_twist", g_twist, twist)
            #print("g_swing", g_swing, swing)
            self.scene.scene_edit_widget.rotation = m[:3,:3].T
        else:
            print("no cos map", self.skeleton_model.keys())
   
        self.jointLabel.setText(label)
        self.is_updating_joint_info = False

    def set_swing_text(self, swing):
        self.swingXLineEdit.setText(str(swing[0]))
        self.swingYLineEdit.setText(str(swing[1]))
        self.swingZLineEdit.setText(str(swing[2]))

    def set_twist_text(self, twist):
        self.twistXLineEdit.setText(str(twist[0]))
        self.twistYLineEdit.setText(str(twist[1]))
        self.twistZLineEdit.setText(str(twist[2]))

    def fill_joint_map(self):
        self.jointMapComboBox.clear()
        for idx, joint in enumerate(STANDARD_JOINTS):
            print("add", joint)
            self.jointMapComboBox.addItem(joint, idx)

    def fill_root_combobox(self):
        self.aligningRootComboBox.clear()
        for idx, joint in enumerate(self.controller.get_animated_joints()):
            self.aligningRootComboBox.addItem(joint, idx)

    def init_joints(self, controller):
        for joint_name in controller.get_animated_joints():
            if len(self.skeleton.nodes[joint_name].children) > 0: # filter out end site joints
                child_node = self.skeleton.nodes[joint_name]#.children[0]
                if np.linalg.norm(child_node.offset)> 0:
                    self.scene.object_builder.create_object("joint_control_knob", controller, joint_name, self.radius)

    def draw(self):
        """ draw current scene on the given view
        (note before calling this function the context of the view has to be set as current using makeCurrent() and afterwards the doubble buffer has to swapped to display the current frame swapBuffers())
        """
        if not self.initialized:
            if self.view.graphics_context is not None:
                self.view.resize(400,400)
                self.initialized = True
        self.scene.update(self.dt)
        self.view.makeCurrent()
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        self.view.graphics_context.render(self.scene)
        self.view.swapBuffers()


    def left_display_changed(self, frame_idx):
        if self.controller is not None:
            self.controller.setCurrentFrameNumber(frame_idx)
            self.leftDisplayFrameSpinBox.setValue(frame_idx)


    def left_spinbox_frame_changed(self, frame):
        self.leftStartFrameSlider.setValue(self.leftStartFrameSpinBox.value())
        self.leftEndFrameSlider.setValue(self.leftEndFrameSpinBox.value())

    def left_slider_frame_changed(self, frame):
        self.leftStartFrameSpinBox.setValue(self.leftStartFrameSlider.value())
        self.leftEndFrameSpinBox.setValue(self.leftEndFrameSlider.value())

    def slot_accept(self):
        self.name = str(self.nameLineEdit.text())
        if self.name != "":
            print("accept")
            self.success = True
            self.skeleton = self.controller.get_skeleton()
            self.skeleton.set_reference_frame(self.reference_frame)
            if self.aligning_root_node is not None:
                self.skeleton.aligning_root_node = self.aligning_root_node
            self.skeleton_data = self.skeleton.to_unity_format()
            if "cos_map" in self.skeleton_model:
                for k in self.skeleton_model["cos_map"]:
                    for l in self.skeleton_model["cos_map"][k]:
                        if type(self.skeleton_model["cos_map"][k][l]) == np.ndarray:
                            self.skeleton_model["cos_map"][k][l] = self.skeleton_model["cos_map"][k][l].tolist()
                        else:
                            self.skeleton_model["cos_map"][k][l] = self.skeleton_model["cos_map"][k][l]
            self.close()
        else:
            print("Please provide a name")

    def slot_reject(self):
        self.close()

    def get_selected_joint(self):
        joint_knob = None
        o = self.scene.selected_scene_object
        if o is not None and "joint_control_knob" in o._components:
            joint_knob = o._components["joint_control_knob"]
        return joint_knob


    def set_twist(self, joint_name):
        x = round(float(self.twistXLineEdit.text()),self.precision)
        y = round(float(self.twistYLineEdit.text()),self.precision)
        z = round(float(self.twistZLineEdit.text()),self.precision)
        #set twist axis
        twist = np.array([x,y,z])
        magnitude = np.linalg.norm(twist)
        if magnitude > 0:
            twist /= magnitude
        self.skeleton_model["cos_map"][joint_name]["y"] = twist

    def set_swing(self, joint_name):
        x = round(float(self.swingXLineEdit.text()),self.precision)
        y = round(float(self.swingYLineEdit.text()),self.precision)
        z = round(float(self.swingZLineEdit.text()),self.precision)
        #set swing axis
        swing = np.array([x,y,z])
        magnitude = np.linalg.norm(swing)
        if magnitude > 0:
            swing /= magnitude
        self.skeleton_model["cos_map"][joint_name]["x"] = swing.tolist()

    def slot_set_twist(self):
        plot = False
        joint_knob = self.get_selected_joint()
        if joint_knob is None:
            return
        self.set_swing(joint_knob.joint_name)
        self.set_twist(joint_knob.joint_name)
        self.update_joint_info(joint_knob)

    def slot_set_swing(self):
        joint_knob = self.get_selected_joint()
        if joint_knob is None:
            return
        self.set_swing(joint_knob.joint_name)
        self.set_twist(joint_knob.joint_name)
        self.update_joint_info(joint_knob)


    def slot_set_orthogonal_twist(self):
        """ https://stackoverflow.com/questions/33658620/generating-two-orthogonal-vectors-that-are-orthogonal-to-a-particular-direction """
        joint_knob = self.get_selected_joint()
        if joint_knob is None:
            return
        joint_name = joint_knob.joint_name
        #get swing axis 
        swing = np.array(self.skeleton_model["cos_map"][joint_name]["x"])
        # find orthogonal vector
        y = np.array(self.skeleton_model["cos_map"][joint_name]["y"])
        
        #y = np.random.randn(3)  # take a random vector
        y -= y.dot(swing) * swing      # make it orthogonal to twist
        y /= np.linalg.norm(y)  # normalize it

        #replace twist axis
        self.set_twist_text(y)
        self.skeleton_model["cos_map"][joint_name]["y"] = y
        self.update_joint_info(joint_knob)
        
    def slot_set_orthogonal_swing(self):
        """ https://stackoverflow.com/questions/33658620/generating-two-orthogonal-vectors-that-are-orthogonal-to-a-particular-direction """
        joint_knob = self.get_selected_joint()
        if joint_knob is None:
            return
        joint_name = joint_knob.joint_name
        #get twist axis 
        twist = np.array(self.skeleton_model["cos_map"][joint_name]["y"] )
        x = np.array(self.skeleton_model["cos_map"][joint_name]["x"] )
        x -= x.dot(twist) * twist      # make it orthogonal to twist
        x /= np.linalg.norm(x)  # normalize it
        #replace twist axis
        self.set_swing_text(x)
        self.skeleton_model["cos_map"][joint_name]["x"] = x
        self.update_joint_info(joint_knob)

    def slot_flip_twist(self):
        joint_knob = self.get_selected_joint()
        if joint_knob is None:
            return
        joint_name = joint_knob.joint_name
        #get twist axis 
        twist = np.array(self.skeleton_model["cos_map"][joint_name]["y"])
        twist *= -1
        self.skeleton_model["cos_map"][joint_name]["y"] = twist
        self.set_twist_text(twist)
        self.update_joint_info(joint_knob)

    def slot_flip_swing(self):
        joint_knob = self.get_selected_joint()
        if joint_knob is None:
            return
        joint_name = joint_knob.joint_name
        swing = np.array(self.skeleton_model["cos_map"][joint_name]["x"])
        swing *= -1
        self.skeleton_model["cos_map"][joint_name]["x"] = swing
        self.set_swing_text(swing)
        self.update_joint_info(joint_knob)

    def slot_rotate_twist(self):
        joint_knob = self.get_selected_joint()
        if joint_knob is None:
            return
        joint_name = joint_knob.joint_name
        #get twist axis 
        angle = round(float(self.twistRotationLineEdit.text()),self.precision)
        rotation_axis = np.array(self.skeleton_model["cos_map"][joint_name]["x"])
        q = quaternion_about_axis(np.deg2rad(angle), rotation_axis)
        q = normalize(q)
        twist = np.array(self.skeleton_model["cos_map"][joint_name]["y"])
        twist = rotate_vector(q, twist)
        twist = normalize(twist)
        self.skeleton_model["cos_map"][joint_name]["y"] = twist
        self.set_twist_text(twist)
        self.update_joint_info(joint_knob)

    def slot_rotate_swing(self):
        joint_knob = self.get_selected_joint()
        if joint_knob is None:
            return
        joint_name = joint_knob.joint_name
        
        angle = round(float(self.swingRotationLineEdit.text()),self.precision)
        rotation_axis = np.array(self.skeleton_model["cos_map"][joint_name]["y"])
        q = quaternion_about_axis(np.deg2rad(angle), rotation_axis)
        q = normalize(q)
        swing = np.array(self.skeleton_model["cos_map"][joint_name]["x"])
        swing = rotate_vector(q, swing)
        swing = normalize(swing)

        self.skeleton_model["cos_map"][joint_name]["x"] = swing
        self.set_swing_text(swing)
        self.update_joint_info(joint_knob)


    def slot_flip_z_axis(self):
        joint_knob = self.get_selected_joint()
        if joint_knob is None:
            return
        joint_name = joint_knob.joint_name
        twist = np.array(self.skeleton_model["cos_map"][joint_name]["y"])
        swing = np.array(self.skeleton_model["cos_map"][joint_name]["x"])
        new_swing = twist
        new_twist = swing
        #print("new swing", new_swing, swing)
        self.skeleton_model["cos_map"][joint_name]["y"] = new_twist
        self.skeleton_model["cos_map"][joint_name]["x"] = new_swing
        self.set_swing_text(new_swing)
        self.set_twist_text(new_twist)
        self.update_joint_info(joint_knob)

    def slot_guess_cos_map(self):
        """ creates a guess for the coordinate system for all joints"""
        temp_skeleton = copy(self.skeleton)
        temp_skeleton.skeleton_model = self.skeleton_model
        cos_map = create_local_cos_map_from_skeleton_axes_with_map(temp_skeleton)
        self.skeleton_model["cos_map"] = cos_map
        joint_knob = self.get_selected_joint()
        if joint_knob is not None:
            self.update_joint_info(joint_knob)

    def slot_reset_cos_map(self):
        """ resets the coordinate systems for all joints"""
        for joint_name in self.skeleton_model["cos_map"]:
            up_vector = self.skeleton_model["cos_map"][joint_name]["y"]
            x_vector = self.skeleton_model["cos_map"][joint_name]["x"]
            if up_vector is not None and x_vector is not None:
                new_up_vector, new_x_vector = self.reset_joint_cos(joint_name, up_vector, x_vector)
                self.skeleton_model["cos_map"][joint_name]["y"] = new_up_vector
                self.skeleton_model["cos_map"][joint_name]["x"] = new_x_vector
        joint_knob = self.get_selected_joint()
        if joint_knob is not None:
            self.update_joint_info(joint_knob)

    def slot_guess_selected_cos_map(self):
        """ creates a guess for the for the selected joint"""
        joint_knob = self.get_selected_joint()
        if joint_knob is None:
            return
        joint_name = joint_knob.joint_name
        temp_skeleton = copy(self.skeleton)
        temp_skeleton.skeleton_model = self.skeleton_model
        cos_map = create_local_cos_map_from_skeleton_axes_with_map(temp_skeleton)
        self.skeleton_model["cos_map"][joint_name] = cos_map[joint_name]
        self.update_joint_info(joint_knob)
        
    def slot_reset_selected_cos_map(self):
        """ creates resetrs the coordinate system for the selected joint"""
        joint_knob = self.get_selected_joint()
        if joint_knob is None:
            return
        joint_name = joint_knob.joint_name
        if joint_name in self.skeleton_model["cos_map"]:
            up_vector = self.skeleton_model["cos_map"][joint_name]["y"]
            x_vector = self.skeleton_model["cos_map"][joint_name]["x"]
            new_up_vector, new_x_vector = self.reset_joint_cos(joint_name, up_vector, x_vector)
            self.skeleton_model["cos_map"][joint_name]["y"] = new_up_vector
            self.skeleton_model["cos_map"][joint_name]["x"] = new_x_vector
            self.update_joint_info(joint_knob)

    
    def slot_update_joint_map(self):
        if not self.is_updating_joint_info and "joints" in self.skeleton_model:
            joint_knob = self.get_selected_joint()
            if joint_knob is not None:
                new_joint_key = str(self.jointMapComboBox.currentText())
                old_joint_key = find_key(self.skeleton_model["joints"], joint_knob.joint_name)
                if old_joint_key in self.skeleton_model["joints"]:
                    self.skeleton_model["joints"][old_joint_key] = None
                self.skeleton_model["joints"][new_joint_key] = joint_knob.joint_name
                print("update joint mapping", joint_knob.joint_name, new_joint_key)
            else:
                print("is updating joint info")

    def reset_joint_cos(self, joint_name, up_vector, x_vector, target_up_vector=DEFAULT_TARGET_CS_UP):
        """ rotates the up_vector to look towards target_up_vector and rotates the x_vector with the same rotation """
        m = self.skeleton.nodes[joint_name].get_global_matrix(self.skeleton.reference_frame)[:3,:3]
        m_inv = np.linalg.inv(m)
        target_up_vector = normalize(target_up_vector)
        local_target = np.dot(m_inv, target_up_vector)
        local_target = normalize(local_target)
        q = quaternion_from_vector_to_vector(up_vector, local_target)
        x_vector = rotate_vector(q, x_vector)
        
        x_vector -= x_vector.dot(local_target) * local_target      # make it orthogonal to twist
        x_vector /= np.linalg.norm(x_vector)  # normalize it
        x_vector = normalize(x_vector)
        return local_target, x_vector

    def slot_update_aligning_root_joint(self):
        if not self.is_updating_joint_info and "joints" in self.skeleton_model:
            self.aligning_root_node = str(self.aligningRootComboBox.currentText())


    def slot_load_default_pose(self):
        filename = QFileDialog.getOpenFileName(self, 'Load From File', '.')[0]
        filename = str(filename)
        if os.path.isfile(filename):
            motion = load_motion_from_bvh(filename)
            if len(motion.frames):
                self.reference_frame = motion.frames[0]
                frames = [self.reference_frame]
                self.controller.replace_frames(frames)
                self.controller.set_reference_frame(0)
                self.controller.updateTransformation()
                print("replaced frames")

    
    def slot_apply_scale(self):
        scale = float(self.scaleLineEdit.text())
        if scale > 0:
            self.controller.set_scale(scale)
            frames = [self.reference_frame]
            self.controller.replace_frames(frames)
            self.controller.currentFrameNumber = 0
            self.controller.updateTransformation()

    def slot_align_to_up_axis(self):
        joint_knob = self.get_selected_joint()
        if joint_knob is None:
            return
        joint_name = joint_knob.joint_name
        if joint_name in self.skeleton_model["cos_map"]:
            up_vector = self.skeleton_model["cos_map"][joint_name]["y"]
            x_vector = self.skeleton_model["cos_map"][joint_name]["x"]
            q_offset = get_axis_correction(self.skeleton, joint_name, up_vector, OPENGL_UP_AXIS)
            up_vector = rotate_vector(q_offset, up_vector)
            x_vector = rotate_vector(q_offset, x_vector)
            self.skeleton_model["cos_map"][joint_name]["x"] = normalize(x_vector)
            self.skeleton_model["cos_map"][joint_name]["y"] = normalize(up_vector)
            self.update_joint_info(joint_knob)

    def slot_align_to_forward_axis(self):
        joint_knob = self.get_selected_joint()
        if joint_knob is None:
            return
        joint_name = joint_knob.joint_name
        if joint_name in self.skeleton_model["cos_map"]:
            up_vector = self.skeleton_model["cos_map"][joint_name]["y"]
     
            m = self.skeleton.nodes[joint_name].get_global_matrix(self.skeleton.reference_frame)[:3,:3]
            m_inv = np.linalg.inv(m)
            target_vector = np.dot(m, up_vector)
            target_vector[1] = 0
            target_vector = normalize(target_vector)
            local_up = np.dot(m_inv, target_vector)
            local_up = normalize(local_up)
            self.skeleton_model["cos_map"][joint_name]["y"] = local_up

            x_vector = self.skeleton_model["cos_map"][joint_name]["x"]
            q = quaternion_from_vector_to_vector(up_vector, local_up)
            x_vector = rotate_vector(q, x_vector)
            
            x_vector -= x_vector.dot(local_up) * local_up      # make it orthogonal to twist
            x_vector /= np.linalg.norm(x_vector)  # normalize it
            self.skeleton_model["cos_map"][joint_name]["x"] = normalize(x_vector)
            self.update_joint_info(joint_knob)

    def slot_mirror_left_to_right(self):
        self.skeleton_model = mirror_join_map(self.skeleton, self.skeleton_model, STANDARD_MIRROR_MAP_LEFT)
        print("mirrored left to right") 
        print(self.skeleton_model["joints"])

    def slot_mirror_right_to_left(self):
        self.skeleton_model = mirror_join_map(self.skeleton, self.skeleton_model, STANDARD_MIRROR_MAP_RIGHT)
        print("mirrored right to left") 
