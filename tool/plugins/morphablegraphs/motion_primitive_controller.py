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
import numpy as np
from copy import deepcopy
import collections
from vis_utils.animation.animation_controller import CONTROLLER_TYPE_MP
from vis_utils.animation.skeleton_animation_controller import LegacySkeletonAnimationController
from vis_utils.animation.skeleton_visualization import SkeletonVisualization, SKELETON_DRAW_MODE_LINES
from anim_utils.animation_data import BVHWriter, MotionVector, SkeletonBuilder
from anim_utils.utilities.io_helper_functions import load_json_file, write_to_json_file
from anim_utils.utilities.log import set_log_mode, LOG_MODE_DEBUG
from vis_utils.scene.utils import get_random_color
from morphablegraphs.motion_model.motion_state_graph_node import MotionStateGraphNode
from morphablegraphs.motion_generator.motion_primitive_generator import MotionPrimitiveGenerator
from morphablegraphs.constraints.motion_primitive_constraints import MotionPrimitiveConstraints
from morphablegraphs.constraints.action_constraints import ActionConstraints
from morphablegraphs import MotionGenerator, GraphWalkOptimizer, AnnotatedMotionVector, DEFAULT_ALGORITHM_CONFIG
from morphablegraphs.constraints.spatial_constraints import GlobalTransformConstraint
from morphablegraphs.motion_generator.optimization.optimizer_builder import OptimizerBuilder
from morphablegraphs.space_partitioning import FeatureClusterTree
from morphablegraphs.utilities import convert_to_mgrd_skeleton

class MockGraph(object):
    def __init__(self, skeleton):
        self.skeleton = skeleton


class MotionPrimitiveController(LegacySkeletonAnimationController):
    def __init__(self, scene_object, name, data, color=(0, 0, 1)):
        LegacySkeletonAnimationController.__init__(self, scene_object)
        self.motion_primitive = MotionStateGraphNode(None)
        self.skeleton = SkeletonBuilder().load_from_json_data(data["skeleton"])
        self.frameTime = self.skeleton.frame_time
        self._visualizations = []
        self.samples = []
        self.algorithm_config = DEFAULT_ALGORITHM_CONFIG
        self.color = color
        self.motion_primitive._initialize_from_json(convert_to_mgrd_skeleton(self.skeleton), data)
        print("loaded motion primitive")
        print("spatial", self.motion_primitive.get_n_spatial_components())
        print("time", self.motion_primitive.get_n_time_components())
        self.motion_primitive.cluster_tree = None

        self.training_data = None
        #print("n gmm", len(self.motion_primitive.get_gaussian_mixture_model().weights))

        self.name = name
        self._regenerate = True
        self.type = CONTROLLER_TYPE_MP
        set_log_mode(LOG_MODE_DEBUG)
        self.start_pose = {"position": [0, 0, 0], "orientation": [0, 0, 0]}
        self.mock_graph = MockGraph(self.skeleton)
        self.label_color_map = dict()

    def init_visualization(self):
        self.generate_random_samples(1)

    def load_cluster_tree_from_json_file(self, filepath):
        tree_data = load_json_file(filepath)
        self.load_cluster_tree_from_json(tree_data)

    def load_cluster_tree_from_json(self, tree_data):
        print("load cluster tree")
        self.motion_primitive.cluster_tree = FeatureClusterTree.load_from_json(tree_data)
        print("finished loading cluster tree")

    def clear(self):
        self.samples = []
        self._visualizations = []

    def generate_random_samples(self, n_samples, sample_offset=0):
        self.clear()
        if n_samples > 1:
            x_offset = -n_samples / 2 * sample_offset
        else:
            x_offset = 0
        for idx in range(n_samples):
            self.generate_random_sample(x_offset)
            x_offset += sample_offset
        self.updated_frame()

    def generate_random_samples_from_tree(self, n_samples, sample_offset=0):
        if self.motion_primitive.cluster_tree is None:
            return
        self.clear()
        if n_samples > 1:
            x_offset = -n_samples / 2 * sample_offset
        else:
            x_offset = 0
        for idx in range(n_samples):
            self.generate_random_sample_from_tree(x_offset)
            x_offset += sample_offset
        self.updated_frame()

    def generate_random_constraints(self, joint_name, frame_idx, n_samples):
        positions = []
        for idx in range(n_samples):
            positions.append(self.generate_random_constraint(joint_name, frame_idx))
        return positions

    def generate_random_sample(self, x_offset=0):
        spline = self.motion_primitive.sample(use_time=False)
        frames = spline.get_motion_vector()
        self.create_sample_visualization(frames, x_offset)

    def generate_random_sample_from_tree(self, x_offset=0):
        if self.motion_primitive.cluster_tree is not None:
            n_points = len(self.motion_primitive.cluster_tree.data)
            sample_idx = np.random.randint(0, n_points)
            print("visualize", sample_idx, "/", n_points)
            sample = self.motion_primitive.cluster_tree.data[sample_idx]
            frames = self.motion_primitive.back_project(sample, False).get_motion_vector()
            self.create_sample_visualization(frames, x_offset)


    def generate_random_sample_from_data(self, x_offset=0):
        self.clear()
        if self.training_data is not None:
            n_samples = len(self.training_data)
            sample_idx = np.random.randint(0, n_samples)
            print("visualize", sample_idx, "/", n_samples)
            sample = self.training_data[sample_idx]
            frames = self.motion_primitive.back_project(sample, False).get_motion_vector()
            self.create_sample_visualization(frames, x_offset)


    def create_sample_visualization(self, frames, x_offset=0):
        motion = AnnotatedMotionVector(skeleton=self.skeleton)
        frames[:, 0] += x_offset
        print(frames.shape)
        motion.append_frames(frames)
        v = SkeletonVisualization(self.scene_object, self.color)
        v.set_skeleton(self.skeleton)
        v.draw_mode = SKELETON_DRAW_MODE_LINES
        self._visualizations.append(v)
        self.samples.append(motion)

    def generate_constrained_sample(self, joint_name, frame_idx, position):
        action_constraints = ElementaryActionConstraints()
        action_constraints.motion_state_graph = self.mock_graph
        self.algorithm_config["local_optimization_settings"]["max_iterations"] = 50000
        self.algorithm_config["local_optimization_settings"]["method"] = "L-BFGS-B"
        mp_generator = MotionPrimitiveGenerator(action_constraints, self.algorithm_config)
        #mp_generator.numerical_minimizer = OptimizerBuilder(self.algorithm_config).build_path_following_minimizer()
        mp_generator.numerical_minimizer = OptimizerBuilder(self.algorithm_config).build_path_following_with_likelihood_minimizer()

        mp_constraints = MotionPrimitiveConstraints()
        n_frames = self.getNumberOfFrames()
        if frame_idx == -1:
            frame_idx = n_frames-1
        mp_constraints.skeleton = self.skeleton

        c_desc = {"joint": joint_name, "canonical_keyframe": frame_idx, "position": position, "n_canonical_frames": n_frames, "semanticAnnotation": {"keyframeLabel":"none"}}
        print("set constraint", c_desc)
        c = GlobalTransformConstraint(self.skeleton, c_desc, 1.0, 1.0)
        mp_constraints.constraints.append(c)
        mp_constraints.use_local_optimization = self.algorithm_config["local_optimization_mode"] in ["all", "keyframes"]
        vector = mp_generator.generate_constrained_sample(self.motion_primitive, mp_constraints)
        spline = self.motion_primitive.back_project(vector, use_time_parameters=False)

        frames = spline.get_motion_vector()
        self.create_sample_visualization(frames)

    def generate_random_constraint(self, joint_name, frame_idx):
        spline = self.motion_primitive.sample(use_time=False)
        frames = spline.get_motion_vector()
        position = self.skeleton.nodes[joint_name].get_global_position(frames[frame_idx])
        return position

    def updated_frame(self):
        prevPlayAnimation = self.playAnimation
        self.playAnimation = True
        self.update(0)
        self.playAnimation = prevPlayAnimation

    def getNumberOfFrames(self):
        if self.isLoadedCorrectly():
            return len(self.samples[0].frames)
        else:
            return 0

    def isLoadedCorrectly(self):
        return len(self.samples) > 0

    def export_to_file(self, filename, sample_idx=0):
        if sample_idx < len(self.samples):
            frame_time = self.frameTime
            frames = self.skeleton.add_fixed_joint_parameters_to_motion(self.samples[0].frames)
            bvh_writer = BVHWriter(None, self.skeleton, frames, frame_time, True)
            bvh_writer.write(filename)

    def get_skeleton_copy(self):
        skeleton = deepcopy(self.skeleton)
        count = 0
        for node_key in skeleton.get_joint_names():
            if node_key != skeleton.root:
                skeleton.nodes[node_key].quaternion_frame_index = count
            count += 1
        return skeleton

    def get_motion_vector_copy(self, start_frame, end_frame, sample_idx=0):
        if sample_idx < len(self.samples):
            mv_copy = MotionVector()
            mv_copy.frames = deepcopy(self.samples[0].frames[start_frame:end_frame])
            mv_copy.frames = self.skeleton.add_fixed_joint_parameters_to_motion(mv_copy.frames)
            mv_copy.n_frames = len(mv_copy.frames)
            mv_copy.frame_time = self.frameTime
            return mv_copy

    def draw(self, modelMatrix, viewMatrix, projectionMatrix, lightSources):
        if self.isLoadedCorrectly() and 0 <= self.currentFrameNumber < self.getNumberOfFrames():
                for v in self._visualizations:
                    v.draw(modelMatrix, viewMatrix, projectionMatrix, lightSources)

    def updateTransformation(self):
        if self.isLoadedCorrectly() and 0 <= self.currentFrameNumber < self.getNumberOfFrames():
            # update global transformation matrices of joints
            for idx, motion in enumerate(self.samples):
                current_frame = motion.frames[self.currentFrameNumber]
                self._visualizations[idx].updateTransformation(current_frame, self.scene_object.scale_matrix)

    def setColor(self, color):
        print("set color", color)
        self.color = color
        for v in self._visualizations:
            v.set_color(color)

    def create_blend_controller(self):
        skeleton = self.skeleton
        motions = self.samples
        name = "Blend Controller" + self.name
        self.scene_object.scene.object_builder.create_blend_controller(name, skeleton, motions)

    def update_markers(self):
        return

    def set_config(self, algorithm_config):
        self.algorithm_config = algorithm_config

    def getFrameTime(self):
        return self.frameTime

    def get_semantic_annotation(self):
        n_keys = len(self.motion_primitive.keyframes)
        if n_keys <= 0:
            return None
        else:
            sorted_keyframes = collections.OrderedDict(sorted(self.motion_primitive.keyframes.items(), key=lambda t: t[1]))
            start = 0
            end = int(self.motion_primitive.get_n_canonical_frames())
            semantic_annotation = collections.OrderedDict()
            for k, v in sorted_keyframes.items():
                semantic_annotation[k] = list(range(start,  v))
                self.label_color_map[k] = get_random_color()
                start = v
            k = "contact"+str(n_keys)
            semantic_annotation[k] = list(range(start, end))
            self.label_color_map[k] = get_random_color()
            return list(semantic_annotation.items())

    def get_label_color_map(self):
        return self.label_color_map

    def set_frame_time(self, frame_time):
        self.frameTime = frame_time

    def get_frame_time(self):
        return self.frameTime