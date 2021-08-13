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
from vis_utils.animation.animation_controller import AnimationController
from vis_utils.animation.skeleton_visualization import SkeletonVisualization
from vis_utils.scene.components import ComponentBase
from vis_utils.animation.skeleton_animation_controller import LegacySkeletonAnimationController
import operator
from anim_utils.animation_data import MotionVector
from anim_utils.animation_data.motion_blending import generate_frame_using_iterative_slerp
import heapq


def generate_frame_linear(skeleton, motions, frame_idx, weights):
    frame = None
    for name, weight in weights.items():
        if frame is None:
            frame = weight * motions[name].frames[frame_idx]
        else:
            frame += weight * motions[name].frames[frame_idx]
    if frame is not None:
        for idx, j in enumerate(skeleton.animated_joints):
            q_idx = (idx*4) + 3
            frame[q_idx:q_idx+4] /= np.linalg.norm(frame[q_idx:q_idx+4])
    return frame


def generate_blend_weights(positions, new_p, n_neighbors):
    """ Use inverse distance and K-Nearest-Neighbors Interpolation to estimate weights
        according to [Johansen 2009] Section 6.2.4
    """

    distances = []
    for n, p in positions.items():
        distance = np.linalg.norm(new_p - p)
        heapq.heappush(distances, (distance, n))
    distances = distances[:n_neighbors]
    weights = dict()
    if distances[0][0] <= 0:
        weights[distances[0][1]] = 1.0
    else:
        inv_k_distance = 1.0 / distances[-1][0]
        inv_distances = [(1.0 / d) - inv_k_distance for d, n in distances]
        new_weights = inv_distances / np.sum(inv_distances)
        for idx, v in enumerate(distances):
            weights[v[1]] = new_weights[idx]
    return weights


class AnimationBlendNode(object):
    def __init__(self):
        self._motions = collections.OrderedDict()
        self._weights = collections.OrderedDict()
        self._positions = collections.OrderedDict()
        self._min_pos = 0.0
        self._max_pos = 1.0
        self.n_frames = 0
        self.n_params = None
        self.skeleton = None
        self.n_blend_space_params = 0
        self.frame_time = 1.0/30.0
        self.parameter_labels = [""]

    def set_parameter_labels(self, labels):
        self.parameter_labels = labels
        self.n_blend_space_params = len(labels)

    def add_motion(self, name, frames, position):
        n_frames = len(frames)
        self._motions[name] = frames
        self._positions[name] = position
        self.update_parameter_range()
        if n_frames > self.n_frames:
            self.n_frames = n_frames
        self.n_params = len(frames[0])

    def get_blend_positions(self):
        return self._positions

    def get_motions(self):
        return self._motions

    def update_parameter_range(self):
        positions = np.array(list(self._positions.values())).T
        self._min_pos = np.min(positions, axis=1)
        self._max_pos = np.max(positions, axis=1)
        print(self._positions.values(), positions,self._min_pos, self._max_pos)

    def update_weights(self):
        p = (self._min_pos + self._max_pos) / 2.0
        self.set_blend_parameter(p, len(self._positions))

    def set_blend_parameter_new(self, new_p, n_neighbors):
        self._weights = generate_blend_weights(self._positions, new_p, n_neighbors)

    def set_blend_parameter(self, new_p, n_neighbors):
        distances = {(n, np.linalg.norm(new_p - p)) for n, p in self._positions.items()}
        sorted_distances = sorted(distances, key=operator.itemgetter(1))
        sorted_names = [name for name, v in sorted_distances[:n_neighbors]]
        sorted_values = np.array([v for name, v in sorted_distances[:n_neighbors]])
        if sorted_values[0] <= 0:
            self._weights[sorted_names[0]] = 1.0
        else:
            inv_k_distance = 1.0 / sorted_values[-1]
            inv_distances = 1.0 / sorted_values - inv_k_distance
            new_weights = inv_distances / np.sum(inv_distances)
            for idx, n in enumerate(sorted_names):
                self._weights[n] = new_weights[idx]

    def set_blend_parameter_prev2(self, new_p, k):
        """ Use inverse distance to estimate weights according to [Johansen 2009]"""
        new_p = float(new_p)
        distances = np.array([np.linalg.norm(new_p - p) for p in self._positions.values()])
        if np.any(distances <= 0):
            for idx, n in enumerate(self._positions.keys()):
                if distances[idx] <= 0:
                    self._weights[n] = 1.0
                else:
                    self._weights[n] = 0.0
        else:
            inv_distances = 1.0 / distances
            h_sum = np.sum(inv_distances)
            weights = inv_distances / h_sum
            for idx, n in enumerate(self._positions.keys()):
                self._weights[n] = weights[idx]
        print("update weights", self._weights)

    def get_valid_weights(self, frame_idx):
        weights = collections.OrderedDict()
        w_sum = 0
        for name, weight in self._weights.items():
            if 0 <= frame_idx < len(self._motions[name]):
                weights[name] = weight
                w_sum += weight
        for name, weight in weights.items():
            weights[name] /= w_sum
        return weights

    def get_frame(self, frame_idx):
        weights = self.get_valid_weights(frame_idx)
        if len(weights) == 0:
            return
        return generate_frame_using_iterative_slerp(self.skeleton, self._motions, frame_idx, weights)

    def to_motion_vector(self):
        frames = []
        for idx in range(self.n_frames):
            frames.append(self.get_frame(idx))
        mv = MotionVector()
        mv.frames = self.skeleton.add_fixed_joint_parameters_to_motion(frames)
        mv.n_frames = self.n_frames
        return mv


class BlendAnimationController(LegacySkeletonAnimationController):
    def __init__(self, scene_object, color=(0, 0, 1)):
        ComponentBase.__init__(self, scene_object)
        AnimationController.__init__(self)
        self.loadedCorrectly = False
        self.hasVisualization = False
        self.name = ""
        self._visualization = SkeletonVisualization(self.scene_object, color)
        self.track = AnimationBlendNode()
        self.n_neighbors = 5
        self.current_parameter = None
        self.markers = dict()

    def set_skeleton(self, skeleton):
        self._visualization.set_skeleton(skeleton)
        self.track.skeleton = skeleton

    def set_track(self, track):
        self.track = track

    def get_valid_weights(self, frame_idx):
        return self.track.get_valid_weights(frame_idx)

    def update_weights(self):
        self.track.update_weights()

    def getPosition(self):
        return [0, 0, 0]

    def get_blend_positions(self):
        return self.track._positions

    def get_motions(self):
        return self.track._motions

    def updateTransformation(self, frame_idx):
        if 0 <= frame_idx < self.track.n_frames:
            self.current_frame = self.track.get_frame(frame_idx)
            if self.current_frame is not None:
                self._visualization.updateTransformation(self.current_frame,
                                                         self.scene_object.scale_matrix)
                #self.update_markers()
            else:
                print("frame is none")

    def update_markers(self):
        frame = self.current_frame
        scale = self.scene_object.scale_matrix[0][0]
        for joint in list(self.markers.keys()):
            for marker in self.markers[joint]:
                m = self._visualization.skeleton.nodes[joint].get_global_matrix(frame, True)
                position = np.dot(m, marker["relative_trans"])[:3, 3]
                marker["object"].setPosition(position * scale)

    def set_blend_parameter(self, p):
        """ Use inverse distance to estimate weights according to [Johansen 2009]"""
        self.current_parameter = p
        self.track.set_blend_parameter(p, self.n_neighbors)
        self.updateTransformation(self.currentFrameNumber)

    def set_n_neighbors(self, n_neighbors):
        self.n_neighbors = n_neighbors

    def isLoadedCorrectly(self):
        return len(self.track._motions) > 0

    def getNumberOfFrames(self):
        return self.track.n_frames

    def getFrame(self, frame_idx):
        return self.track.get_frame(frame_idx)

    def get_parameter_range(self):
        return self.track._min_pos, self.track._max_pos

    def get_n_parameters(self):
        return self.track.n_blend_space_params

    def get_parameter_labels(self):
        return self.track.parameter_labels

    def save_to_file(self, filename):
        import pickle
        with open(filename, "wb") as out_file:
            pickle.dump(self.track, out_file)

    def getFrameTime(self):
        return self.track.frame_time

    def export_to_bvh_file(self, filename):
        mv = self.track.to_motion_vector()
        mv.export(self.track.skeleton, filename, False)

    def set_frame_time(self, frame_time):
        self.track.frame_time = frame_time

    def get_frame_time(self):
        return self.track.frame_time
    