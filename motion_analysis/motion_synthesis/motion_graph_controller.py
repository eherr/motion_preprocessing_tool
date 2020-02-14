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
from PySignal import Signal
from transformations import quaternion_multiply, quaternion_from_euler, quaternion_conjugate
from vis_utils.animation.animation_controller import AnimationController
from vis_utils.animation.skeleton_visualization import SkeletonVisualization
from vis_utils.scene.components import ComponentBase
import math


def quat_rotate_vector(quat, vec):
    quat = quat / np.linalg.norm(quat)
    vec = np.array([0, vec[0], vec[1], vec[2]])
    ret = quaternion_multiply(quaternion_multiply(quat, vec), quaternion_conjugate(quat))
    return np.array([ret[1], ret[2], ret[3]])


class MotionGraphController(ComponentBase, AnimationController):
    """ The MotionGraphController class displays a motion genenrated by motion similarity graph
        The class emits a Qt signals when the animation state changes.
        The scene containing a controller connects to those signals and relays them to the GUI.
    """

    updated_animation_frame = Signal()
    reached_end_of_animation = Signal()

    def __init__(self, scene_object, color=(0, 0, 1), mg=None):
        ComponentBase.__init__(self, scene_object)
        AnimationController.__init__(self)
        self._motion_graph = mg
        self._visualization = SkeletonVisualization(self.scene_object, color)
        self.name = ""
        strong_components = self._motion_graph.strong_components
        self.current_node_id = min(strong_components)
        self.current_direction = []
        self.current_root_pos = []
        self.current_root_quat = []
        self.angleX = 0
        self.frameTime = 0
        self.animationSpeed = 1

    def init_visualization(self):
        msg_node = self._motion_graph.get_pose_by_node_id(self.current_node_id)
        pose = np.copy(msg_node.pose)
        self.current_direction = quat_rotate_vector(pose[3:7], np.array([0, 0, 1]))
        self.current_direction[1] = 0 #prevent error accumulation in y axis
        self.current_root_pos = pose[:3]
        self.current_root_quat = pose[3:7]
        self._visualization.updateTransformation(msg_node.pose, self.scene_object.scale_matrix)

    def set_skeleton(self, skeleton):
        self._visualization.set_skeleton(skeleton)

    def update(self, dt):
        """ update current frame and global joint transformation matrices
        """
        if self.playAnimation:
            self.updateTransformation()
            self.currentFrameNumber += 1
            self.updated_animation_frame.emit(self.currentFrameNumber)

    def updateTransformation(self):
        # update global transformation matrices of joints
        if self.angleX > np.pi:
            self.angleX -= 2 * np.pi
        if self.angleX < -np.pi:
            self.angleX += 2 * np.pi

        if self.animationSpeed < 1:
            self.animationSpeed = 1
        #for i in range(self.animationSpeed):

        self.current_node_id = self._motion_graph.sample_next_node_id(self.current_node_id)

        self.scene_object.scene.global_vars["node_id"] = self.current_node_id

        current_node = self._motion_graph.get_pose_by_node_id(self.current_node_id)


        pose = np.copy(current_node.pose)
        root_velocity = np.linalg.norm(current_node.velocity[:3])
        if (math.isclose(self.angleX, 0.0)): #walking direction remains unchanged
            self.current_root_pos = self.current_root_pos + root_velocity * self.current_direction
            pose[:3] = self.current_root_pos
        else:
            pose[3:7] = quaternion_multiply(pose[3:7], current_node.velocity[3:7])
            pose[3:7] = quaternion_multiply(pose[3:7], quaternion_from_euler(self.angleX, 0, 0))
            self.current_root_quat = pose[3:7]
            self.current_direction = quat_rotate_vector(pose[3:7], np.array([0, 0, 1]))
            self.current_direction[1] = 0  # prevent error accumulation in y axis
            self.current_root_pos = self.current_root_pos + root_velocity * self.current_direction
            pose[:3] = self.current_root_pos

        self._visualization.updateTransformation(pose, self.scene_object.scale_matrix)

    def draw(self, modelMatrix, viewMatrix, projectionMatrix, lightSources):
        self._visualization.draw(modelMatrix, viewMatrix, projectionMatrix, lightSources)

    def drawFrame(self, viewMatrix, projectionMatrix, lightSources, color=(1.0, 1.0, 1.0)):
        for joint in self.jointControllers.values():
            # print "draw",joint.name
            joint.draw(viewMatrix, projectionMatrix, lightSources, color=color)

    def getNumberOfFrames(self):
        return math.inf

    def getPosition(self):
        return self.current_root_pos * self.scene_object.get_scale()

    def set_frame_time(self, frame_time):
        self.skeleton.frame_time = frame_time

    def get_frame_time(self):
        return self.skeleton.frame_time
