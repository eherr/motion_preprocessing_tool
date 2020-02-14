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
import copy
import threading
import numpy as np
import collections
import time
from datetime import datetime
import os
import glob
from PySignal import Signal
from anim_utils.animation_data.motion_state import MotionState, MotionStateInterface
from vis_utils.animation.state_machine_controller import StateMachineController
from vis_utils.animation.skeleton_visualization import SkeletonVisualization
from vis_utils.graphics.renderer.lines import DebugLineRenderer
from anim_utils.animation_data.motion_concatenation import align_joint
from anim_utils.motion_editing import MotionGrounding
from anim_utils.animation_data.bvh import BVHReader
from anim_utils.animation_data.motion_vector import MotionVector
from anim_utils.retargeting.analytical import Retargeting, generate_joint_map
from transformations import euler_matrix
import vis_utils.constants as constants
from vis_utils.scene.components import ComponentBase
from morphablegraphs.motion_generator.algorithm_configuration import DEFAULT_ALGORITHM_CONFIG
from morphablegraphs.motion_model import MotionStateGraphLoader, NODE_TYPE_STANDARD, NODE_TYPE_END, NODE_TYPE_START, NODE_TYPE_IDLE
from morphablegraphs.motion_model.static_motion_primitive import StaticMotionPrimitive
from morphablegraphs.utilities import set_log_mode, LOG_MODE_DEBUG
from morphablegraphs.motion_generator.mg_state_planner import MGStatePlanner, get_node_aligning_2d_transform, ANIMATED_JOINTS_CUSTOM
from morphablegraphs.constraints.constraint_builder import UnityFrameConstraint
from morphablegraphs.motion_generator.mg_state_queue import StateQueueEntry


def rotate_vector_deg(vec, a):
    a = np.radians(a)
    m = euler_matrix(0, a, 0)[:3,:3]
    vec = np.dot(m, vec)
    return vec

DEFAULT_CONFIG = dict()
DEFAULT_CONFIG["algorithm"]  = DEFAULT_ALGORITHM_CONFIG
DEFAULT_CONFIG["algorithm"]["n_random_samples"] = 300
DEFAULT_CONFIG["algorithm"]["n_cluster_search_candidates"] = 4
DEFAULT_CONFIG["algorithm"]["local_optimization_settings"]["max_iterations"] = 1000
DEFAULT_CONFIG["algorithm"]["local_optimization_settings"]["method"] = "L-BFGS-B"
DEFAULT_CONFIG["algorithm"]["local_optimization_mode"] = "none"
DEFAULT_CONFIG["algorithm"]["inverse_kinematics_settings"]["interpolation_window"]= 120
DEFAULT_CONFIG["algorithm"]["inverse_kinematics_settings"]["transition_window"]= 60

def load_clips(data_path):
    print("load clips", data_path)
    loaded_clips = dict()
    for filepath in glob.glob(data_path+os.sep+"*.bvh"):
        print("load", filepath)
        name = filepath.split(os.sep)[-1][:-4]
        bvh = BVHReader(filepath)
        mv = MotionVector()
        mv.from_bvh_reader(bvh, True)
        state = MotionState(mv)
        state.play = True
        print("load", name, mv.n_frames)
        loaded_clips[name] = state
    return loaded_clips


def update_collision_objects(scene, collision_objects):
    for o_desc in collision_objects:
        o_id = o_desc["id"]
        p = [o_desc["position"]["x"], o_desc["position"]["y"], o_desc["position"]["z"]]
        q = [o_desc["rotation"]["w"], o_desc["rotation"]["x"], o_desc["rotation"]["y"], o_desc["rotation"]["z"]]
        print("set position", o_id, p)
        o = scene.get_scene_node_by_name(str(o_id))
        if o is not None:
            print("found object", o_id, p)
            o.setPosition(p)
            o.setQuaternion(q)
        else:
            print("could not find object")


class MorphableGraphStateMachine(StateMachineController):
    def __init__(self, scene_object, graph, start_node=None, use_all_joints=False, config=DEFAULT_CONFIG, pfnn_data=None):
        StateMachineController.__init__(self, scene_object)
        self._graph = graph
        if start_node is None or start_node not in self._graph.nodes:
            start_node = self._graph.start_node
        self.start_node = start_node
        self.frame_time = self._graph.skeleton.frame_time
        self.skeleton = self._graph.skeleton
        self.thread = None
        self._visualization = None
        set_log_mode(LOG_MODE_DEBUG)
        self.current_node = self.start_node
        self.use_all_joints = use_all_joints
        self.node_type = NODE_TYPE_IDLE
        self.state = None
        self.set_initial_idle_state(use_all_joints)
        print("start node", self.current_node)
        self.start_pose = {"position": [0, 0, 0], "orientation": [0, 0, 0]}
        self.speed = 1
        if "speed" in config:
            self.speed = config["speed"]
        print("set speed", self.speed)
        
        self.pose_buffer = []
        self.buffer_size = 10
        self.max_step_length = 80
        self.direction_vector = np.array([-1.0, 0.0, 0.0])
        self.action_constraint = None
        self.target_projection_len = 0
        self.n_joints = len(self.skeleton.animated_joints)
        self.n_max_state_queries = 20

        self.retarget_engine = None
        self.target_skeleton = None
        self.activate_emit = False
        self.show_skeleton = True
        self.node_queue = []
        self.activate_grounding = False
        self.collision_boundary = None
        self.hand_collision_boundary = None

        self.aligning_transform = np.eye(4)
        self.draw_root_trajectory = False
        self.planner = MGStatePlanner(self, self._graph, config)
        self.motion_grounding = MotionGrounding(self.skeleton, config["algorithm"]["inverse_kinematics_settings"], self.skeleton.skeleton_model)
        self.actions = self.planner.action_definitions
        self.planner.settings.use_all_joints = use_all_joints
        self.state.play = True
        self.thread = None
        self.animation_server = None
        self.success = True
        self.is_recording = False
        self.stop_current_state = False
        self.lock = threading.Lock()
        self.recorded_poses = list()
        #if pfnn_data is not None:
        #    self.planner.pfnn_wrapper = PFNNWrapper.load_from_dict(self.skeleton, pfnn_data["weights"], pfnn_data["means"])
        #    self.planner.use_pfnn = True
        self.load_clips = dict()
        if "clip_directory" in config and "clip_directory" in config:
            data_path = config["data_directory"] + os.sep + config["clip_directory"]
            if os.path.isdir(data_path):
                self.loaded_clips = load_clips(data_path)
            else:
                print("Could not find clip directory", data_path)

    def set_graph(self, graph, start_node):
        print("set graph")
        self.lock.acquire()
        self.stop_current_state = True
        if self.thread is not None:
            print("stop thread")
            self.planner.stop_thread = True
            self.thread.join()
            self.stop_current_state = True
            self.thread = None
        self._graph = graph
        self.start_node = start_node
        self.current_node = self.start_node
        self.set_initial_idle_state(self.planner.settings.use_all_joints)
        self.planner.state_queue.reset()
        self.lock.release()
        if self.animation_server is not None:
            #self.animation_server.start()
            print("restarted animation server..............................")

    def create_collision_boundary(self, radius, length, visualize=True, active=True):
        if not constants.activate_simulation:
            return
        print("create collision boundary", radius, length)
        self.collision_boundary = self.scene_object.scene.object_builder.create_component("collision_boundary", self.scene_object, radius, length, "morphablegraph_state_machine", visualize=visualize)
        self.collision_boundary.active = active
        self.planner.collision_boundary = self.collision_boundary

    def create_hand_collision_boundary(self, joint_name, radius, visualize=True, active=True):
        if not constants.activate_simulation:
            return
        print("create collision boundary",joint_name, radius)
        self.hand_collision_boundary = self.scene_object.scene.object_builder.create_component("hand_collision_boundary", joint_name, self.scene_object, radius, "morphablegraph_state_machine", visualize=visualize)
        self.hand_collision_boundary.active = active
        self.planner.hand_collision_boundary = self.hand_collision_boundary

    def load_pfnn_controller(self, path, mean_folder, src_skeleton=None):
        self.planner.pfnn_wrapper = PFNNWrapper.load_from_file(self.skeleton, path, mean_folder, src_skeleton)
        self.planner.use_pfnn = True

    def set_initial_idle_state(self, use_all_joints=False):
        mv = MotionVector(self.skeleton)
        print("node", self.current_node)
        mv.frames = self._graph.nodes[self.current_node].sample().get_motion_vector()
        mv.frame_time = self.frame_time
        mv.n_frames = len(mv.frames)
        print("before", mv.frames.shape, self.skeleton.reference_frame_length)
        other_animated_joints = self._graph.nodes[self.current_node].get_animated_joints()
        if len(other_animated_joints) == 0:
            other_animated_joints = ANIMATED_JOINTS_CUSTOM
        if use_all_joints:
            other_animated_joints = self._graph.nodes[self.current_node].get_animated_joints()
            if len(other_animated_joints) == 0:
                other_animated_joints = ANIMATED_JOINTS_CUSTOM
            full_frames = np.zeros((len(mv.frames), self.skeleton.reference_frame_length))
            for idx, reduced_frame in enumerate(mv.frames):
                full_frames[idx] = self.skeleton.add_fixed_joint_parameters_to_other_frame(reduced_frame,
                                                                                           other_animated_joints)
            mv.frames = full_frames
        self.state = MotionState(mv)
        self.state.play = self.play
    
    def set_config(self, config):
        if "activate_grounding" in config:
            self.activate_grounding =config["activate_grounding"]
        self.planner.set_config(config)

    def set_visualization(self, visualization):
        self._visualization = visualization
        self._visualization.update_dir_vis(self.direction_vector, self.target_projection_len)
        self.update_transformation()

    def update(self, dt):
        """ update current frame and global joint transformation matrices
        """
        if self.play:
            transition = self.state.update(self.speed * dt)
            self.lock.acquire()
            if transition or (len(self.planner.state_queue) > 0 and self.stop_current_state):
                # decide if the state planner should be used based on a given task and the number of states in the queue
                use_state_planner = False
                #self.planner.state_queue.mutex.acquire()
                if self.planner.is_processing or len(self.planner.state_queue) > 0:
                    use_state_planner = True
                #self.planner.state_queue.mutex.release()
                if use_state_planner:
                    # if the state planner should be used wait until a state was generated
                    success = False
                    n_queries = 0
                    while not success and n_queries < self.n_max_state_queries:
                        self.planner.state_queue.mutex.acquire()
                        success = self.pop_motion_state_from_queue()
                        if not success:
                            #print("Warning: state queue is empty")
                            n_queries += 1
                        self.planner.state_queue.mutex.release()
                    if not success:
                        print("Warning: transition to idle state due to empty state queue")
                        state_entry = self.planner.state_queue.generate_idle_state(dt, self.pose_buffer, False)
                        self.set_state_entry(state_entry)
                    self.stop_current_state = False
                else:
                    # otherwise transition to new state without the planner, e.g. to idle state
                    self.transition_to_next_state_controlled()
                    #print("WAIT")
            self.lock.release()
            self.update_transformation()

    def pop_motion_state_from_queue(self):
        if len(self.planner.state_queue) > 0:
            state_entry = self.planner.state_queue.get_first_state()
            self.set_state_entry(state_entry)
            self.planner.state_queue.pop_first_state()
            return True
        else:
            return False

    def set_state_entry(self, state_entry):
        self.state = state_entry.state
        self.current_node = state_entry.node
        self.node_type = state_entry.node_type
        #print("set state", self.current_node, self.state.mv.frames[:,1])
        self.pose_buffer = copy.copy(state_entry.pose_buffer)

    def set_global_position(self, position):
        self.lock.acquire()
        self.state.set_position(position)
        self.set_buffer_position(position)
        self.lock.release()
        assert not np.isnan(self.pose_buffer[-1]).any(), "Error in set pos "+str(position)

    def set_global_orientation(self, orientation):
        self.lock.acquire()
        self.state.set_orientation(orientation)
        self.set_buffer_orientation(orientation)
        self.lock.release()
        assert not np.isnan(self.pose_buffer[-1]).any(), "Error in set orientation "+str(orientation)

    def set_buffer_position(self, pos):
        for idx in range(len(self.pose_buffer)):
            self.pose_buffer[idx][:3] = pos

    def set_buffer_orientation(self, orientation):
        for idx in range(len(self.pose_buffer)):
            self.pose_buffer[idx][3:7] = orientation
        
    def unpause(self):
        self.state.hold_last_frame = False
        self.state.paused = False

    def play_clip(self, clip_name):
        print("play clip")
        if clip_name in self.loaded_clips:
            state = self.loaded_clips[clip_name]
            node_id = ("walk", "idle")
            node_type = NODE_TYPE_IDLE
            self.lock.acquire()
            self.planner.state_queue.mutex.acquire()
            self.stop_current_state = True
            pose_buffer = self.pose_buffer
            state_entry = StateQueueEntry(node_id, node_type, state, pose_buffer)
            self.set_state_entry(state_entry)
            self.planner.state_queue.reset()
            print("set state entry ", clip_name)
            self.planner.state_queue.mutex.release()
            self.lock.release()

    def generate_action_constraints(self, action_desc):
        action_name = action_desc["name"]
        velocity_factor = 1.0
        n_cycles = 1
        upper_body_gesture = None
        constrain_look_at = False
        look_at_constraints = False
        if "locomotionUpperBodyAction" in action_desc:
            upper_body_gesture = dict()
            upper_body_gesture["name"] = action_desc["locomotionUpperBodyAction"]
        elif "upperBodyGesture" in action_desc:
            upper_body_gesture = action_desc["upperBodyGesture"]
        if "velocityFactor" in action_desc:
            velocity_factor = action_desc["velocityFactor"]
        if "nCycles" in action_desc:
            n_cycles = action_desc["nCycles"]
        if "constrainLookAt" in action_desc:
            constrain_look_at = action_desc["constrainLookAt"]
        if "lookAtConstraints" in action_desc:
            look_at_constraints = action_desc["lookAtConstraints"]
        print("enqueue states", action_name)
        frame_constraints, end_direction, body_orientation_targets = self.planner.constraint_builder.extract_constraints_from_dict(action_desc, look_at_constraints)
        out = dict()
        out["action_name"] = action_name
        out["frame_constraints"] = frame_constraints
        out["end_direction"] = end_direction
        out["body_orientation_targets"] = body_orientation_targets
        if "controlPoints" in action_desc:
            out["control_points"] = action_desc["controlPoints"]
        elif "directionAngle" in action_desc and "nSteps" in action_desc and "stepDistance" in action_desc:
            root_dir = get_global_node_orientation_vector(self.skeleton, self.skeleton.aligning_root_node, self.get_current_frame(), self.skeleton.aligning_root_dir)
            root_dir = np.array([root_dir[0], 0, root_dir[1]])
            out["direction"] = rotate_vector_deg(root_dir, action_desc["directionAngle"])
            out["n_steps"] = action_desc["nSteps"]
            out["step_distance"] = action_desc["stepDistance"]
        elif "direction" in action_desc and "nSteps" in action_desc and "stepDistance" in action_desc:
            out["direction"] = action_desc["direction"]
            out["n_steps"] = action_desc["nSteps"]
            out["step_distance"] = action_desc["stepDistance"]
        out["upper_body_gesture"] = upper_body_gesture
        out["velocity_factor"] = velocity_factor
        out["n_cycles"] = n_cycles
        out["constrain_look_at"] = constrain_look_at
        out["look_at_constraints"] = look_at_constraints
        return out

    def enqueue_states(self, action_sequence, dt, refresh=False):
        """ generates states until all control points have been reached
            should to be called by extra thread to asynchronously
        """
        _action_sequence = []
        for action_desc in action_sequence:
            
            if "collisionObjectsUpdates" in action_desc:
                func_name = "a"
                params = self.scene_object.scene,action_desc["collisionObjectsUpdates"]
                self.scene_object.scene.schedule_func_call(func_name, update_collision_objects, params)
            a = self.generate_action_constraints(action_desc)
            _action_sequence.append(a)

        if self.thread is not None:
            print("stop thread")
            self.planner.stop_thread = True
            self.thread.join()
            self.stop_current_state = refresh
            #self.planner.state_queue.reset()
            self.thread = None

        self.planner.state_queue.mutex.acquire()
        start_node = self.current_node
        start_node_type = self.node_type
        pose_buffer = [np.array(frame) for frame in self.state.get_frames()[-self.buffer_size:]]
        self.planner.state_queue.reset()
        self.planner.state_queue.mutex.release()
        self.planner.stop_thread = False
        self.planner.is_processing = True
        if refresh:
            self.lock.acquire()
            self.stop_current_state = True
            pose_buffer = []
            for p in self.pose_buffer:
                pose_buffer.append(p)
            #self.transition_to_next_state_controlled()
            self.lock.release()

        method_args = (_action_sequence, start_node, start_node_type, pose_buffer, dt)
        self.thread = threading.Thread(target=self.planner.generate_motion_states_from_action_sequence, name="c", args=method_args)
        self.thread.start()

    def draw(self, modelMatrix, viewMatrix, projectionMatrix, lightSources):
        return
        if self.show_skeleton:
            self._visualization.draw(modelMatrix, viewMatrix, projectionMatrix, lightSources)
        self._visualization.update_dir_vis(self.direction_vector, self.target_projection_len)
        self.line_renderer.draw(modelMatrix, viewMatrix, projectionMatrix)


    def transition_to_next_state_randomly(self):
        self.current_node = self._graph.nodes[self.current_node].generate_random_transition(NODE_TYPE_STANDARD)
        spline = self._graph.nodes[self.current_node].sample()
        self.set_state_by_spline(spline)

    def emit_update(self):
        if self.activate_emit:
            return
            #self.update_scene_object.emit(-1)

    def set_aligning_transform(self):
        """ uses a random sample of the morphable model to find an aligning transformation to bring constraints into the local coordinate system"""
        sample = self._graph.nodes[self.current_node].sample(False)
        frames = sample.get_motion_vector()
        m = get_node_aligning_2d_transform(self.skeleton, self.skeleton.aligning_root_node,
                                           self.pose_buffer, frames)
        self.aligning_transform = np.linalg.inv(m)

    def transition_to_next_state_controlled(self):
        self.current_node, self.node_type, self.node_queue = self.select_next_node(self.current_node, self.node_type, self.node_queue, self.target_projection_len)
        #print("transition", self.current_node, self.node_type, self.target_projection_len)
        self.set_aligning_transform()
        if isinstance(self._graph.nodes[self.current_node].motion_primitive, StaticMotionPrimitive):
            spline = self._graph.nodes[self.current_node].sample()
            new_frames = spline.get_motion_vector()
        else:
            mp_constraints = self.planner.constraint_builder.generate_walk_constraints(self.current_node, self.aligning_transform, self.direction_vector, self.target_projection_len, self.pose_buffer)
            s = self.planner.mp_generator.generate_constrained_sample(self._graph.nodes[self.current_node], mp_constraints)
            spline = self._graph.nodes[self.current_node].back_project(s, use_time_parameters=False)
            new_frames = spline.get_motion_vector()
            #new_frames = self.planner.generate_constrained_motion_primitive(self.current_node, mp_constraints.constraints, self.pose_buffer)
        
        if self.planner.settings.use_all_joints:
            new_frames = self.planner.complete_frames(self.current_node, new_frames)
        #new_frames = self.state.get_frames()
        ignore_rotation = False
        if self.current_node[1] == "idle" and self.planner.settings.ignore_idle_rotation:
            ignore_rotation = True
        self.state = self.planner.state_queue.build_state(new_frames, self.pose_buffer, ignore_rotation)
        self.state.play = self.play
        self.emit_update()

    def select_next_node(self, current_node, current_node_type, node_queue, step_distance):
        if len(node_queue):
            next_node, node_type = node_queue[0]
            node_queue = node_queue[1:]
            next_node_type = node_type
        else:
            next_node_type = self.planner.get_next_node_type(current_node_type, step_distance)
            next_node = self._graph.nodes[current_node].generate_random_transition(next_node_type)
            if next_node is None:
               next_node = self.start_node
               next_node_type = NODE_TYPE_IDLE
        return next_node, next_node_type, node_queue

    def apply_ik_on_transition(self, spline):
        left_foot = self.skeleton.skeleton_model["joints"]["left_foot"]
        right_foot = self.skeleton.skeleton_model["joints"]["right_foot"]
        right_hand = self.skeleton.skeleton_model["joints"]["right_wrist"]
        left_hand = self.skeleton.skeleton_model["joints"]["left_wrist"]
        n_coeffs = len(spline.coeffs)
        ik_chains = self.skeleton.skeleton_model["ik_chains"]
        ik_window = 5  # n_coeffs - 2
        align_joint(self.skeleton, spline.coeffs, 0, left_foot, ik_chains["foot_l"], ik_window)
        align_joint(self.skeleton, spline.coeffs, 0, right_foot, ik_chains["foot_r"], ik_window)
        align_joint(self.skeleton, spline.coeffs, 0, left_hand, ik_chains[left_hand], ik_window)
        align_joint(self.skeleton, spline.coeffs, 0, right_hand, ik_chains[right_hand], ik_window)

        for i in range(1, n_coeffs):
            spline.coeffs[i] = self.align_frames(spline.coeffs[i], spline.coeffs[0])

    def align_frames(self, frame, ref_frame):
        for i in range(self.n_joints):
            o = i*4+3
            q = frame[o:o+4]
            frame[o:o+4] = -q if np.dot(ref_frame[o:o+4], q) < 0 else q
        return frame

    def update_transformation(self):
        pose = self.state.get_pose()
        if self.activate_grounding:
            pose = self.motion_grounding.apply_on_frame(pose, self.scene_object.scene)
        self.pose_buffer.append(np.array(pose))
        _pose = copy.copy(pose)
        #_pose[:3] = [0,0,0]
        if self.show_skeleton and self._visualization is not None:
            self._visualization.updateTransformation(_pose , self.scene_object.scale_matrix)
            self._visualization.update_dir_vis(self.direction_vector, self.target_projection_len)
        self.pose_buffer = self.pose_buffer[-self.buffer_size:]
        if self.is_recording:
            self.recorded_poses.append(pose)

    def getPosition(self):
        if self.state is not None:
            return self.state.get_pose()[:3]
        else:
            return [0, 0, 0]

    def get_global_transformation(self):
        return self.skeleton.nodes[self.skeleton.root].get_global_matrix(self.pose_buffer[-1])

    def handle_keyboard_input(self, key):
        if key == "p":
            self.transition_to_action("placeLeft")
        else:
            if key == "a":
                self.rotate_dir_vector(-10)
            elif key == "d":
                self.rotate_dir_vector(10)
            elif key == "w":
                self.target_projection_len += 10
                self.target_projection_len = min(self.target_projection_len, self.max_step_length)
            elif key == "s":
                self.target_projection_len -= 10
                self.target_projection_len = max(self.target_projection_len, 0)
            #if self.node_type == NODE_TYPE_IDLE:
            #    self.transition_to_next_state_controlled()
            #if not self.play and self.node_type == NODE_TYPE_END and self.target_projection_len > 0:
            #    self.play = True
        self.emit_update()
    
    def create_action_constraint(self, action_name, keyframe_label, position, joint_name=None):
        node = self.actions[action_name]["constraint_slots"][keyframe_label]["node"]
        if joint_name is None:
            joint_name = self.actions[action_name]["constraint_slots"][keyframe_label]["joint"]
        action_constraint = UnityFrameConstraint((action_name, node), keyframe_label, joint_name, position, None)
        return action_constraint

    def transition_to_action(self, action, constraint=None):
        self.action_constraint  = constraint
        if self.current_node[0] != "walk":
            return
        for node_name, node_type in self.actions[action]["node_sequence"]:
            self.node_queue.append(((action, node_name), node_type))
        if self.node_type == NODE_TYPE_IDLE:
            self.node_queue.append((self.start_node, NODE_TYPE_IDLE))
        self.transition_to_next_state_controlled()

    def rotate_dir_vector(self, angle):
        r = np.radians(angle)
        s = np.sin(r)
        c = np.cos(r)
        self.direction_vector[0] = c * self.direction_vector[0] - s * self.direction_vector[2]
        self.direction_vector[2] = s * self.direction_vector[0] + c * self.direction_vector[2]
        self.direction_vector /= np.linalg.norm(self.direction_vector)
        print("rotate",self.direction_vector)

    def get_n_frames(self):
        return self.state.get_n_frames()

    def get_frame_time(self):
        return self.state.get_frame_time()

    def get_pose(self, frame_idx=None):
        frame = self.state.get_pose(frame_idx)
        if self.retarget_engine is not None:
            return self.retarget_engine.retarget_frame(frame, None)
        else:
            return frame
        

    def get_current_frame_idx(self):
        return self.state.frame_idx

    def get_current_annotation(self):
        return self.state.get_current_annotation()

    def get_n_annotations(self):
        return self.state.get_n_annotations()

    def get_semantic_annotation(self):
        return self.state.get_semantic_annotation()

    def set_target_skeleton(self, target_skeleton):
        self.target_skeleton = target_skeleton
        target_knee = target_skeleton.skeleton_model["joints"]["right_knee"]
        src_knee = self.skeleton.skeleton_model["joints"]["right_knee"]
        scale = 1.0 # np.linalg.norm(target_skeleton.nodes[target_knee].offset) / np.linalg.norm(self.skeleton.nodes[src_knee].offset)
        joint_map = generate_joint_map(self.skeleton.skeleton_model, target_skeleton.skeleton_model)
        skeleton_copy = copy.deepcopy(self.skeleton)
        self.retarget_engine = Retargeting(skeleton_copy, target_skeleton, joint_map, scale, additional_rotation_map=None, place_on_ground=False)
        self.activate_emit = False
        self.show_skeleton = False

    def get_actions(self):
        return list(self.actions.keys())

    def get_keyframe_labels(self, action_name):
        if action_name in self.actions:
            if "constraint_slots" in self.actions[action_name]:
                return list(self.actions[action_name]["constraint_slots"].keys())
            else:
                raise Exception("someting "+ action_name)
        return list()

    def get_skeleton(self):
        if self.target_skeleton is not None:
            return self.target_skeleton
        else:
            return self.skeleton

    def get_animated_joints(self):
        return self._graph.animated_joints

    def get_current_frame(self):
        pose = self.state.get_pose(None)
        if self.target_skeleton is not None:
            pose = self.retarget_engine.retarget_frame(pose, self.target_skeleton.reference_frame)
            if self.activate_grounding:
                x = pose[0]
                z = pose[2]
                target_ground_height = self.scene_object.scene.get_height(x, z)
                #pelvis = self.target_skeleton.skeleton_model["joints"]["pelvis"]
                #offset = self.target_skeleton.nodes[pelvis].offset
                #print("offset", pelvis, offset[2],np.linalg.norm(offset))
                #shift = target_ground_height - (pose[1] + offset[2])
                shift = target_ground_height - pose[1]
                pose[1] += shift
        return pose

    def get_events(self):
        event_keys = list(self.state.events.keys())
        for key in event_keys:
            if self.state.frame_idx >= key:
                # send and remove event
                events = self.state.events[key]
                del self.state.events[key]
                return events
        else:
            return list()

    def get_current_annotation_label(self):
        return ""

    def isPlaying(self):
        return True

    def has_success(self):
        return self.success

    def reset_planner(self):
        print("reset planner")
        self.planner.state_queue.mutex.acquire()
        if self.planner.is_processing:
            self.planner.stop_thread = True
            if self.thread is not None:
                self.thread.stop()
            self.planner.is_processing = False
            #self.current_node = ("walk", "idle")
            self.current_node = self.start_node
            self.node_type = NODE_TYPE_IDLE
            self.planner.state_queue.reset()
            self.pose_buffer = list()
            self.set_initial_idle_state(self.use_all_joints)

        self.planner.state_queue.mutex.release()
        return

    def start_recording(self):
        self.is_recording = True
        self.recorded_poses = list()

    def save_recording_to_file(self):
        time_str = datetime.now().strftime("%d%m%y_%H%M%S")
        filename = "recording_"+time_str+".bvh"
        n_frames = len(self.recorded_poses)
        if n_frames > 0:
            other_animated_joints = self._graph.nodes[self.current_node].get_animated_joints()
            full_frames = np.zeros((n_frames, self.skeleton.reference_frame_length))
            for idx, reduced_frame in enumerate(self.recorded_poses):
                full_frames[idx] = self.skeleton.add_fixed_joint_parameters_to_other_frame(reduced_frame,
                                                                                           other_animated_joints)
            mv = MotionVector()
            mv.frames = full_frames
            mv.n_frames = n_frames
            mv.frame_time = self.frame_time
            mv.export(self.skeleton, filename)
            print("saved recording with", n_frames, "to file", filename)
            self.is_recording = False

    def get_bone_matrices(self):
        return self._visualization.matrices

    def handle_collision(self):
        print("handle collision")
        self.lock.acquire()
        if self.thread is not None:
            print("stop thread")
            self.planner.stop_thread = True
            self.thread.join()
            self.stop_current_state = True
            self.thread = None

        self.planner.state_queue.mutex.acquire()
        self.planner.state_queue.reset()
        self.planner.state_queue.mutex.release()
        self.planner.stop_thread = False
        self.planner.is_processing = True
        
        self.stop_current_state = True
        #self.transition_to_next_state_controlled()
        self.lock.release()