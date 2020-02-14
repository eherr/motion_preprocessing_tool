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
import json
import glob
import collections
from vis_utils.io import load_json_file, save_json_file
from vis_utils.scene.legacy import ConstraintObject

def get_all_objects(scene):
    return scene.objectList()


def get_splines(scene):
    return scene.getSplineObjects()


def get_animation_controllers(scene):
    for sceneObject in scene.objectList():
        if sceneObject.has_component("animation_controller") or sceneObject.has_component("morphablegraphs_controller"):
            yield sceneObject


def get_constraints(scene):
    for sceneObject in scene.objectList():
        if isinstance(sceneObject, ConstraintObject):
            yield sceneObject

def create_sections_from_annotation(annotations):
    motion_sections = dict()
    for label in annotations:
        annotations[label].sort()
        section = dict()
        section["start_idx"] = annotations[label][0]
        section["end_idx"] = annotations[label][-1]
        motion_sections[section["start_idx"]] = section
    return list(collections.OrderedDict(sorted(motion_sections.items())).values())

def read_annotation_file(annotation_filepath):
    meta_info_str = ""
    with open(annotation_filepath, "rt") as annotation_file:
        print("read meta info from", annotation_filepath)
        annotation_str = annotation_file.read()
        annotation_data = json.loads(annotation_str)
        meta_info_data = dict()
        meta_info_data["sections"] = create_sections_from_annotation(annotation_data["semantic_annotation"])
        meta_info_str = json.dumps(meta_info_data)
    return meta_info_str


def load_bvh_with_annotations(directory, skeleton_model="custom"):
    data = collections.OrderedDict()
    for filename in glob.glob(directory+os.sep+"*.bvh"):
        name = filename.split(os.sep)[-1]
        bvh_str = None
        with open(filename, "rt") as in_file:
            print("read", filename)
            bvh_str = in_file.read()
        if bvh_str is not None:
            meta_info_str = ""
            #check for annoation
            annotation_file_option1 = filename[:-4]+"_section.json"
            annotation_file_option2 = filename[:-4]+"_sections.json"
            meta_info_file = filename+"_meta_info.json"
            if os.path.isfile(annotation_file_option1):
                meta_info_str = read_annotation_file(annotation_file_option1)
            elif os.path.isfile(annotation_file_option2):
                meta_info_str = read_annotation_file(annotation_file_option2)
            elif os.path.isfile(meta_info_file):
                with open(meta_info_file, "rt") as meta_info_file:
                    meta_info_str = meta_info_file.read()
            else:
                print("Did not find meta info for", filename)
                meta_info_str = ""
            data[name] = dict()
            data[name]["meta_info"] = meta_info_str
            data[name]["bvh_str"] = bvh_str
            data[name]["skeleton_model"] = skeleton_model
            
    return data


def load_bvh_with_keyframes(directory, skeleton_model="custom"):
    data = collections.OrderedDict()
    keyframe_file_name = directory+os.sep+"keyframes.json"
    with open(keyframe_file_name, "rt") as keyframe_file:
        keyframe_str = keyframe_file.read()
        keyframe_data = json.loads(keyframe_str)
    print("found keyframes", keyframe_data.keys())
    for filename in glob.glob(directory+os.sep+"*.bvh"):
        name = filename.split(os.sep)[-1]
        with open(filename, "rt") as in_file:
            print("read", filename)

            bvh_str = in_file.read()
            
            key = name[:-4]
            if key in keyframe_data:
                meta_info_data = dict()
                meta_info_data["sections"] = []
                section = dict()
                section["start_idx"] = 0
                section["end_idx"] = keyframe_data[key]
                meta_info_data["sections"].append(section)
                section = dict()
                section["start_idx"] = keyframe_data[key]
                section["end_idx"] = -1
                meta_info_data["sections"].append(section)
                meta_info_str = json.dumps(meta_info_data)
            else:
                meta_info_str = ""


            data[name] = dict()
            data[name]["meta_info"] = meta_info_str
            data[name]["bvh_str"] = bvh_str
            data[name]["skeleton_model"] = skeleton_model
    return data


def load_motion_data_from_dir(directory, skeleton_model="custom"):
    if os.path.isfile(directory+os.sep+"keyframes.json"):
        data = load_bvh_with_keyframes(directory, skeleton_model)
    else:
        data = load_bvh_with_annotations(directory, skeleton_model)
    return data



def get_local_skeletons(local_skeleton_dir):
    skeleton_list = []
    for filename in glob.glob(local_skeleton_dir + os.sep + "*.json"):
        name = filename.split(os.sep)[-1][:-5]
        skeleton_list.append(name)
    return skeleton_list

def load_local_skeleton(local_skeleton_dir, name):
     filename = local_skeleton_dir + os.sep + name+".json"
     data = load_json_file(filename)
     return data

def save_local_skeleton(local_skeleton_dir, name, data):
     filename = local_skeleton_dir + os.sep + name+".json"
     data = save_json_file(data, filename)

def load_local_skeleton_model(local_skeleton_dir, name):
     filename = local_skeleton_dir + os.sep + name+".json"
     data = load_json_file(filename)
     return data["model"]
