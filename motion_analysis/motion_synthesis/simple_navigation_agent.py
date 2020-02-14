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
from vis_utils.scene.components import ComponentBase

class SimpleNavigationAgent(ComponentBase):
    def __init__(self, scene_object):
        ComponentBase.__init__(self, scene_object)
        self.controller = scene_object._components["morphablegraph_state_machine"]
        self.walk_targets = []
        self.tolerance = 20

    def get_actions(self):
        return self.controller.get_actions()

    def get_keyframe_labels(self, action_name):
        return self.controller.get_keyframe_labels(action_name)

    def perform_action(self, action_name, keyframe_label, position):
        constraint = None
        if keyframe_label is not None and position is not None:
            constraint = self.controller.create_action_constraint(action_name, keyframe_label, position)
        self.controller.transition_to_action(action_name, constraint)

    def set_walk_target(self, target):
        self.walk_targets.append(target)
        self.update(0)
        if self.controller.node_type == "idle":
            self.controller.transition_to_next_state_controlled()

    def remove_walk_target(self):
        if len(self.walk_targets) > 1:
            self.walk_targets = self.walk_targets[1:]
        else:
            self.walk_targets = []
        self.controller.target_projection_len = 0

    def get_current_walk_target(self):
        if len(self.walk_targets) > 0:
            return self.walk_targets[0]
        else:
            return None

    def update(self, dt):
        target = self.get_current_walk_target()
        if target is None:
            return
        controller_pos = np.array(self.controller.getPosition())
        controller_pos[1] = 0
        target_pos = target.getPosition()
        target_pos[1] = 0
        target_dir = target_pos - controller_pos
        distance = np.linalg.norm(target_dir)
        target_dir = target_dir / distance
        self.controller.direction_vector = target_dir
        if distance > self.tolerance:
            self.controller.target_projection_len = min(self.controller.max_step_length, distance)
        else:
            self.remove_walk_target()




