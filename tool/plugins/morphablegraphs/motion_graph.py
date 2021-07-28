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
"""
This program implements interactive avatar control paper: http://graphics.cs.cmu.edu/projects/Avatar/avatar.pdf
This file implements the similarity motion graphs
Author: Xi Li
"""

import random
import numpy as np
from transformations import quaternion_multiply, quaternion_inverse, quaternion_from_euler, quaternion_matrix
from anim_utils.animation_data.motion_vector import MotionVector
from anim_utils.animation_data.motion_distance import convert_quat_frame_to_point_cloud
from anim_utils.utils import calculate_point_cloud_distance
from tarjan import tarjan

DEBUG = 1


def get_quat_from_two_vectors(u, v):
    w = np.cross(u, v)
    q = np.array([np.dot(u, v), w[0], w[1], w[2]]) #w, x, y, z convention
    q[0] += np.linalg.norm(q)
    q = q / np.linalg.norm(q)

    return q


class MGNode(object):
    """node class for motion similarity graph"""
    def __init__(self, pose, velocity, bvh_id, contact, weights = None):
        self.pose = pose
        self.velocity = velocity
        self.frame_id = bvh_id
        self.contact = contact


class MotionGraphBuilder(object):
    def __init__(self):
        self.measure_method = "motion_field"  # measure method for edges, option: motion_field, TODO
        self.distance_threshold = 0.05
        self.default_pos = [0.0, 100.0, 0.0]

    def build(self, skeleton, motion_vectors):
        """create MG by motion vectors"""
        nodes = self.create_nodes_by_motion_vectors(skeleton, motion_vectors)
        edges = self.create_edges_by_nodes(skeleton, nodes)
        if DEBUG:
            print('original edges: ', edges)
        # implment strongest components by tarjan's algorithm
        strong_components = self.find_strongly_connected_components(edges)
        del strong_components[0]  # TODO: check if there is a bug in tc
        if DEBUG:
            print('find scc: ', strong_components)
        # prune edge so that only strong components preserved
        edges = self.prune_edges(edges, strong_components)
        if DEBUG:
            print('pruned edges: ', edges)

        return MotionGraph(skeleton, nodes, edges, strong_components)

    def transform_motion_to_point_cloud(self, skeleton, node, joints=None):
        return convert_quat_frame_to_point_cloud(skeleton, node)  # adapted from morphaple graph module

    def compute_velocity(self, skeleton, pose, prev_pose):
        """compute velocity via finite difference"""
        joints = skeleton.animated_joints
        v = np.zeros(len(joints) * 4 + 3)  # only preserve the key joints
        v[:3] = pose[:3]- prev_pose[:3]
        index = 3
        root_pos_offset = 3
        for joint in joints:
            offset = skeleton.nodes[joint].index * 4 + root_pos_offset
            qa = pose[offset:offset + 4]
            qb = prev_pose[offset:offset + 4]

            v[index:index + 4] = quaternion_multiply(quaternion_inverse(qa), qb)
            index += 4
        return v

    def compute_LR_foot_velocity(self, skeleton, pose, prev_node):
        """compute the left and right foot velocity, used for contact estimate"""
        LeftIdx = 'Bip01_L_Toe0'
        RightIdx = 'Bip01_R_Toe0'

        leftFoot = skeleton.nodes[LeftIdx].get_global_position(pose)
        leftFootPrev = skeleton.nodes[LeftIdx].get_global_position(prev_node)

        rightFoot = skeleton.nodes[RightIdx].get_global_position(pose)
        rightFootPrev = skeleton.nodes[RightIdx].get_global_position(prev_node)

        axis = 1  # TODO: is this y axis?
        leftVel = (leftFoot[axis] - leftFootPrev[axis] ) / skeleton.frame_time
        rightVel = (rightFoot[axis] - rightFootPrev[axis] ) / skeleton.frame_time

        return leftVel, rightVel, leftFoot[axis], rightFoot[axis]

    def create_nodes_by_motion_vectors(self, skeleton, motion_vectors):
        nodes = dict()
        # set default root pos and orientation
        default_pos = self.default_pos
        default_quat = motion_vectors[0].frames[0][3:7]
        bvh_id = 0
        frame_id = 0
        for mv in motion_vectors:
            for idx, frame in enumerate(mv.frames[1:]):
                node = frame
                prev_node = mv.frames[idx -1]  # used for velocity
                node_velocity = self.compute_velocity(skeleton, node, prev_node)
                [leftVel, rightVel, leftFoot, rightFoot] = self.compute_LR_foot_velocity(skeleton, node, prev_node)
                root_pos = node[:3] - prev_node[:3]
                root_quat = quaternion_multiply(quaternion_inverse(prev_node[3:7]), node[3:7])
                root_transform = quaternion_matrix(root_quat)
                root_transform[:3,3] = root_pos

                # align the pos and quat of all frames to default
                node[:3] = default_pos
                node[3:7] = default_quat
                nodes[frame_id] = MGNode(node, node_velocity, bvh_id, [leftVel, rightVel, leftFoot, rightFoot])
                frame_id += 1
            bvh_id += 1
        return nodes

    def get_contact_state(self, contact_info):
        # intermediate phase
        if contact_info[0] * contact_info[1] < 0:
            return 0

        # left up or right up
        if contact_info[0] > 0:
            return 1

        # left down or right down
        if contact_info[0] < 0:
            return 2

    def estimate_contact_state(self, node1, node2):
        """contact information, we only find pose for forward walking"""

        contact1 = self.get_contact_state(node1.contact)
        contact2 = self.get_contact_state(node2.contact)

        # if left up, next node's left foot should higher than current node
        if contact1 == contact2 == 1 and node2.contact[2] > node1.contact[2]:
            return True

        # if left down, next node's left foot should lower than current node
        if contact1 == contact2 == 2 and node2.contact[2] < node1.contact[2]:
            return True

        if contact1 == contact2 == 0:
            return True

        return False

    def quaternion_distance_between_frames(self, skeleton, frame1, frame2):
        joints = skeleton.animated_joints
        v = np.zeros(len(joints))  # only preserve the key joints
        root_pos_offset = 3
        index = 0
        for joint in joints:
            offset = skeleton.nodes[joint].index * 4 + root_pos_offset
            qa = frame1.pose[offset:offset + 4]
            qb = frame2.pose[offset:offset + 4]

            quat_difference = quaternion_multiply(qb, quaternion_inverse(qa))
            quat_difference = quat_difference / np.linalg.norm(quat_difference)
            v[index] = np.arccos(quat_difference[0])
            index += 1

        distance = np.linalg.norm(v)

        return distance * distance

    def point_cloud_distance(self, skeleton,frames1,frames2, window):
        a = []
        b = []
        for idx in range(len(frames1)):
            for n in skeleton.animated_joints:
                a.append(skeleton.nodes[n].get_global_position(frames1[idx]))
                b.append(skeleton.nodes[n].get_global_position(frames2[idx]))

        distance = calculate_point_cloud_distance(a, b, window)
        return distance

    def get_pose_similarity(self, skeleton, node1, node2):
        distance = 0.0
        if self.measure_method == "motion_field":
            pose_distance = self.quaternion_distance_between_frames(skeleton, node1, node2)
            velocity_distance = np.linalg.norm(node1.velocity - node2.velocity)
            distance = pose_distance + velocity_distance * 0.5
        return distance

    def create_edges_by_nodes(self, skeleton, nodes):
        """create edges for each node, edge value is the similarity between nodes"""
        edges = dict()
        num_nodes = len(nodes) - 1
        for i in range(num_nodes):
            print('find edge for ', i, ' of ', num_nodes, ' nodes')
            if nodes[i].frame_id == nodes[i + 1].frame_id:
                edges[i] = [i + 1]
            else:
                edges[i] = []
            for j in range(num_nodes):
                if i == j or i + 1 == j:  # skip itself and its next
                    continue
                node1 = nodes[i]
                node2 = nodes[j]
                # we first estimate if the contact state of two nodes are same
                contact_state = self.estimate_contact_state(node1, node2)
                if contact_state:  # same contact state
                    # then measure the similarity distance, smaller -> similar
                    similarity = self.get_pose_similarity(skeleton, node1, node2)
                    # if DEBUG:
                    #    print "frame ", i, " frame ", j, " distance: ", similarity_distance
                    if similarity < self.distance_threshold:
                        edges[i].append(j)
        return edges

    def find_strongly_connected_components(self, edges):
        # This function implements Tarjan's find strongly connected components
        scc = tarjan(edges)
        largest_strong_components = []

        for entry in scc:
            try:
                l = len(entry)
                if l > len(largest_strong_components):
                    largest_strong_components.extend(entry)
            except:
                print("Element", entry, "has no defined length")

        return largest_strong_components

    def prune_edges(self, edges, node_filter):
        """prune the edge to preserve the strong components' node"""
        for i in list(edges):
            if i not in node_filter:
                # remove edges from this node
                edges.pop(i, None)
                continue
            preseved_list = []
            #print(i)
            for j in edges[i]:
                if j in node_filter:
                    # remove the item
                    preseved_list.append(j)
            edges[i] = preseved_list
        return edges


class MotionGraph(object):
    def __init__(self, skeleton, nodes, edges, strong_components):
        self.skeleton = skeleton
        self.nodes = nodes
        self.edges = edges
        self.strong_components = strong_components

    def get_pose_by_trajectory(self, node, last_pose, trj_type, trj_value, direction, orientation):
        pose = np.copy(node.pose)
        last_root_pos = last_pose[:3]
        root_velocity = node.velocity[:3]
        if trj_type == "euler":
            current_pos = last_root_pos + np.linalg.norm(root_velocity) * direction
            pose[:3] = current_pos
            pose[3:7] = quaternion_multiply(pose[3:7], node.velocity[3:7])
            pose[3:7] = quaternion_multiply(pose[3:7], quaternion_from_euler(orientation, 0, 0))
        return pose

    def sample_next_node_id(self, node_id):
        # here, we find the node based on lowest transition value
        if len(self.edges[node_id]) <= 0:
            return -1
        length = len(self.edges[node_id])
        random_index = random.randrange(0, length, 1)
        #random_index = random.randrange(0, 3, 1) #greedy chose from three largest

        # prevent local minimum
        if node_id - self.edges[node_id][random_index] > 0 and node_id - self.edges[node_id][random_index] < 10:
            return self.edges[node_id][random.randrange(0, length, 1)]

        return self.edges[node_id][random_index]  #0 cause sliding

    def get_pose_by_node_id(self, id):
        return self.nodes[id]

    def generate_motion_old(self, trajectory):
        """generate motion vector by pre-defined trajectory"""


        node_id = min(self.strong_components) #start from the minimum frame id
        pose = None
        last_pose = None

        trj_type = trajectory.getType()
        trj_value = trajectory.getValue()
        trj_frame = 0
        direction = []
        orientation = 0
        if trj_type == "euler":
            trj_frame = trajectory.getFrame()
            #compute the translation along the walking direction
            radian = np.deg2rad(trj_value[0])
            direction = np.array([np.sin(radian), 0, -1 * np.cos(radian)]) #walk toward to [0 0 -1]
            orientation = -radian

        out_mv = MotionVector()
        out_mv.frames = []

        for frame_idx in range(trj_frame):
            node = self.nodes[node_id]
            if pose is None:
                pose = np.copy(node.pose)
                pose[3:7] = quaternion_multiply(pose[3:7], node.velocity[3:7])
                pose[3:7] = quaternion_multiply(pose[3:7], quaternion_from_euler(orientation, 0, 0))
                last_pose = np.copy(pose)
            else:
                pose = self.get_pose_by_trajectory(node, last_pose, trj_type, trj_value, direction, orientation)
                last_pose = np.copy(pose)
            out_mv.frames.append(last_pose) #TODO: why mess when using "pose" here?
            node_id = self.sample_next_node_id(node_id)

            if DEBUG:
                if node_id < 0:
                    print('frame ', frame_idx,  'not find any edge, dead end')
                else:
                    print('frame ', frame_idx, 'current node', node_id)
        return out_mv



