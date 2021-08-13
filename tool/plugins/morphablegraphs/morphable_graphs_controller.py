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
from copy import deepcopy
from vis_utils.animation.animation_controller import AnimationController, CONTROLLER_TYPE_MG
from vis_utils.animation.skeleton_animation_controller import LegacySkeletonAnimationController, SkeletonAnimationController
from vis_utils.animation.skeleton_visualization import SkeletonVisualization
from anim_utils.animation_data import BVHWriter, MotionVector
from anim_utils.utilities.io_helper_functions import write_to_json_file
from anim_utils.animation_data.quaternion_frame import convert_quaternion_frames_to_euler_frames
from anim_utils.utilities.log import set_log_mode, LOG_MODE_DEBUG
from anim_utils.animation_data.skeleton_models import *
from anim_utils.animation_data.motion_state import MotionState
from tool.plugins.morphablegraphs.core.motion_model import MotionStateGraphLoader
from tool.plugins.morphablegraphs.core.motion_generator.graph_walk import GraphWalk
from tool.plugins.morphablegraphs.core import MotionGenerator, GraphWalkOptimizer, DEFAULT_ALGORITHM_CONFIG, AnnotatedMotionVector
from tool.plugins.morphablegraphs.core import constraints as mg_constraints
from tool.plugins.morphablegraphs.core import motion_generator

SERVICE_CONFIG = {
    "model_data": "E:\\projects\\INTERACT\\repository\\data\\3 - Motion primitives\\motion_primitives_quaternion_PCA95 m32-integration-1.5.1",
    "transition_data": "E:\\projects\\INTERACT\\repository\\data\\4 - Transition model\\input",
    "output_dir": "E:\\projects\\INTERACT\\repository\\BestFitPipeline\\_Results",
    "input_dir": "E:\\projects\\INTERACT\\repository\\BestFitPipeline\\CNL-GUI",
    "output_filename": "MGResult",
    "port": 8888,
    "export_motion_to_file": True,
    "activate_joint_map": False,
    "activate_coordinate_transform": True,
    "data_folder": "C:\\repo\\data\\1 - MoCap",
    "write_log": True,
    "algorithm_settings": "accuracy",
    "add_time_stamp": True,
    "activate_collision_avoidance": True,
    "collision_avoidance_actions": ["pickRight", "pickLeft", "pickBoth", "placeRight", "placeLeft", "placeBoth"],
    "collision_avoidance_service_url": None,
    "collision_avoidance_service_port": 10030,
    "create_ca_vis_data": False
}


class MorphableGraphsController(SkeletonAnimationController):#LegacySkeletonAnimationController
    """ The MorphableGraphsController class displays a motion genenrated by a graph of statistical motion models
        The class emits a Qt signals when the animation state changes.
        The scene containing a controller connects to those signals and relays them to the GUI.
    """
    def __init__(self, scene_object, name, graph, start_node=None, config=DEFAULT_ALGORITHM_CONFIG, color=(0, 0, 1)):
        SkeletonAnimationController.__init__(self, scene_object)
        self.name = name# file_path.split("/")[-1]
        self._graph = graph #loader.build()
        self.algorithm_config = config
        self._service_config = SERVICE_CONFIG
        self._graph_walk = None
        self._motion = None
        self._regenerate = True
        self.frameTime = self._graph.skeleton.frame_time
        print(self._graph.skeleton.animated_joints)
        print("set frame time to", self.frameTime)
        #self._visualization = SkeletonVisualization(scene_object, color)
        #self._visualization.set_skeleton(self._graph.skeleton)
        self.type = CONTROLLER_TYPE_MG
        set_log_mode(LOG_MODE_DEBUG)
        if start_node is None:
            print("generate random start")
            start_node = self._graph.get_random_start_node()
        self.start_node = start_node
        print("start node", self.start_node)
        self.start_pose = {"position": [0, 0, 0], "orientation": [0, 0, 0]}

    def set_visualization(self, visualization):
        self._visualization = visualization
        self.synthesize_random_sample(self.start_node)
        self.updateTransformation()

    #def init_visualization(self):
    #    self.synthesize_random_sample(self.start_node)

    def get_skeleton(self):
        return self._graph.skeleton

    def clear_graph_walk(self):
        self._graph_walk = None
        print("cleared graph walk")

    def synthesize_from_constraints(self, constraints, random_seed=None):
        if random_seed is not None:
            np.random.seed(random_seed)
        generator = motion_generator.MotionGenerator(self._graph, self._service_config, self.algorithm_config)
        generator.scene_interface.set_scene(self.scene_object.scene)

        motion = None
        print("start synthesis")
        if not self._regenerate:
            motion = generator.generate_motion(constraints, activate_joint_map=False,
                                                                  activate_coordinate_transform=False,
                                                                  complete_motion_vector=False,
                                                                  prev_graph_walk=self._graph_walk)
            self._graph_walk = generator.graph_walk
        else:
            motion = generator.generate_motion(constraints, activate_joint_map=False,
                                                                  activate_coordinate_transform=False,
                                                                  complete_motion_vector=False)

            self._graph_walk = generator.graph_walk

        if motion.ground_contacts is not None:
            from anim_utils.motion_editing.utils import convert_ground_contacts_to_annotation

            annotation_data = convert_ground_contacts_to_annotation(motion.ground_contacts,
                                                         self._graph.skeleton.skeleton_model[
                                                             "foot_joints"],
                                                         motion.n_frames)

            self._semantic_annotation = annotation_data["semantic_annotation"]
            self.label_color_map = annotation_data["color_map"]
        self._regenerate = False
        if motion is not None:
            self._motion = MotionState(motion)
        self.updateTransformation()
        #self._create_constraint_visualization()
        #self.dump_motion_data()

    def _create_constraint_visualization(self):
        if self._motion.mv.grounding_constraints is None:
            return
        positions = dict()
        for frame_idx, constraints in list(self._motion.mv.grounding_constraints.items()):
            for c in constraints:
                pos = tuple(c.position)
                if pos not in positions:
                    positions[pos] = None
                    name = str(frame_idx) + "_" + c.joint_name
                    self.scene_object.scene.addSphere(name, c.position, simulate=False)

    def dump_motion_data(self, filename="temp_result.json"):
        dump_data = dict()
        dump_data["animation"] = [pose.tolist() for pose in convert_quaternion_frames_to_euler_frames(self._motion.mv.frames)]
        dump_data["jointOrder"] = self._graph.skeleton.animated_joints
        write_to_json_file(filename, dump_data)

    def synthesize_random_walk(self, start_node, n_mp_steps, use_time=False):
        motion = AnnotatedMotionVector(self._graph.skeleton, self.algorithm_config)
        graph_walk = self._graph.node_groups[start_node[0]].generate_random_walk(start_node, n_mp_steps)
        for step in graph_walk:
            frames = self._graph.nodes[step["node_key"]].back_project(step["parameters"], use_time).get_motion_vector()
            motion.append_frames(frames)
        self._motion = MotionState(motion)
        self.updateTransformation()

    def synthesize_random_sample(self, start_node):
        motion = AnnotatedMotionVector(skeleton=self._graph.skeleton)
        spline = self._graph.nodes[start_node].sample()
        frames = spline.get_motion_vector()
        motion.append_frames(frames)
        self._motion = MotionState(motion)
        self.updateTransformation()

    def updated_frame(self):
        prevPlayAnimation = self.playAnimation
        self.playAnimation = True
        self.update(0)
        self.playAnimation = prevPlayAnimation

    def getNumberOfFrames(self):
        if self._motion is not None:
            return self._motion.mv.n_frames
        else:
            return 0

    def isLoadedCorrectly(self):
        return self._motion is not None

    def getElementaryActions(self):
        return list(self._graph.node_groups.keys())

    def getMotionPrimitives(self, action):
        if action not in list(self._graph.node_groups.keys()):
            return []
        keys = list(self._graph.node_groups[action].nodes.keys())
        mps = list(zip(*keys))[1]
        return mps

    def export_to_file(self, filename):
        if self._motion is not None:
            frame_time = self.frameTime
            skeleton = self._graph.skeleton
            frames = skeleton.add_fixed_joint_parameters_to_motion(self._motion.mv.frames)
            bvh_writer = BVHWriter(None, skeleton, frames, frame_time, True)
            bvh_writer.write(filename)

    def export_graph_walk_to_file(self, filename):
        if self._graph_walk is not None:
            self._graph_walk.save_to_file(filename)

    def load_graph_walk_from_file(self, filename):
        with open(filename) as in_file:
            data = json.load(in_file)
            self._graph_walk = GraphWalk.from_json(self._graph, data)
            motion = self._graph_walk.convert_to_annotated_motion()
            self._motion = MotionState(motion)
            self.updateTransformation()

    def getJoints(self):
        return list(self._graph.skeleton.nodes.keys())

    def getAnnotations(self, action_name):
        if action_name in list(self._graph.node_groups.keys()):
            return list(self._graph.node_groups[action_name].label_to_motion_primitive_map.keys())
        else:
            return []

    def getFrameTime(self):
        return self.frameTime

    def set_config(self, config):
        self._regenerate = True
        self.algorithm_config = config

    def set_start_position(self, position):
        self.start_pose["position"] = position

    def get_skeleton_copy(self):
        skeleton = deepcopy(self._visualization.skeleton)
        count = 0
        for node_key in skeleton.get_joint_names():
            if node_key != skeleton.root:
                skeleton.nodes[node_key].quaternion_frame_index = count
            count += 1
        return skeleton

    def get_motion_vector_copy(self, start_frame, end_frame):
        mv_copy = MotionVector()
        mv_copy.frames = deepcopy(self._motion.mv.frames[start_frame:end_frame])
        skeleton = self._graph.skeleton
        mv_copy.frames = skeleton.add_fixed_joint_parameters_to_motion(mv_copy.frames)
        mv_copy.n_frames = len(mv_copy.frames)
        mv_copy.frame_time = self.frameTime
        return mv_copy
    
    def get_label_color_map(self):
        return None

    def set_frame_time(self, frame_time):
        self.frameTime = frame_time

    def get_frame_time(self):
        return self.frameTime
