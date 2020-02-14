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
from vis_utils.scene.components import ComponentBase
from vis_utils.graphics.renderer.lines import CoordinateSystemRenderer


class JointControlKnob(ComponentBase):
    def __init__(self, scene_object, anim_controller, joint_name):
        ComponentBase.__init__(self, scene_object)
        self.anim_controller = anim_controller
        self.joint_name = joint_name
        self.skeleton = self.anim_controller.get_skeleton()
        self.edit_mode = False
        if self.joint_name in  self.skeleton.animated_joints and np.linalg.norm(self.skeleton.nodes[self.joint_name].offset)> 0:
            self.cs = CoordinateSystemRenderer(3.0)
        else:
            self.cs = None
        self.global_matrix = np.eye(4)

    def update(self, dt):
        if not self.edit_mode:
            p = self.get_joint_position()
            self.scene_object.setPosition(p)
        
    def get_joint_position(self):
        frame = self.anim_controller.get_current_frame()
        self.global_matrix = self.anim_controller.get_skeleton().nodes[self.joint_name].get_global_matrix(frame)
        return self.global_matrix[:3,3]

    def draw(self, modelMatrix, viewMatrix, projectionMatrix, lightSources):
        if self.cs is not None:
            self.cs.draw(self.global_matrix.T, viewMatrix, projectionMatrix)
