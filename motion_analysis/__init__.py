import json
import collections
from vis_utils.scene.scene_object_builder import SceneObjectBuilder, SceneObject
from vis_utils.scene.utils import get_random_color
from anim_utils.animation_data import BVHReader, MotionVector, SkeletonBuilder


def create_annotation_from_sections_list(sections, n_frames):
    annotations = collections.OrderedDict()
    for idx, section in enumerate(sections):
        #print("section", label, section)
        label = "c"+str(idx)# TODO store labels
        indices_sections = []
        if type(section) == list:
            for sub_section in section:
                start = sub_section["start_idx"]
                end = sub_section["end_idx"]
                if end == -1:
                    end = n_frames-1
                else:
                    end += 1
                frame_indices = list(range(start, end))
                indices_sections.append(frame_indices)
        else:
            start = section["start_idx"]
            end = section["end_idx"]
            if end == -1:
                end = n_frames-1
            else:
                end += 1
            frame_indices = list(range(start, end))
            indices_sections.append(frame_indices)
        annotations[label] = indices_sections
    #return annotations
    return collections.OrderedDict(sorted(annotations.items(), key=lambda x: x[1][0][0]))

def create_annotation_from_sections_dict(sections, n_frames):
    annotations = collections.OrderedDict()
    for label, section in sections.items():
        #print("section", label, section)
        indices_sections = []
        if type(section) == list:
            for sub_section in section:
                start = sub_section["start_idx"]
                end = sub_section["end_idx"]
                if end == -1:
                    end = n_frames-1
                else:
                    end += 1
                frame_indices = list(range(start, end))
                indices_sections.append(frame_indices)
        else:
            start = section["start_idx"]
            end = section["end_idx"]
            if end == -1:
                end = n_frames-1
            else:
                end += 1
            frame_indices = list(range(start, end))
            indices_sections.append(frame_indices)
        annotations[label] = indices_sections
    #return annotations
    return collections.OrderedDict(sorted(annotations.items(), key=lambda x: x[1][0][0]))

def get_bvh_from_str(bvh_str):
    bvh_reader = BVHReader("")
    lines = bvh_str.split("\n")
    lines = [l for l in lines if len(l) > 0]
    bvh_reader.process_lines(lines)
    return bvh_reader


def load_motion_from_str(builder, bvh_str, name, node_key, motion_id, meta_info_str="", draw_mode=2, visualize=True, color=None):
    if color is None:
        color = get_random_color()

    bvh_reader = get_bvh_from_str(bvh_str)
    print("loaded motion", bvh_reader.frames.shape)
    animated_joints = [key for key in list(bvh_reader.node_names.keys()) if not key.endswith("EndSite")]
    skeleton = SkeletonBuilder().load_from_bvh(bvh_reader, animated_joints)
    
    motion_vector = MotionVector()
    motion_vector.from_bvh_reader(bvh_reader, False)
    motion_vector.skeleton = skeleton
    motion_vector.scale_root(0.01)
    o = builder.create_object("animation_controller", name, skeleton, motion_vector, bvh_reader.frame_time, draw_mode, visualize, color)
    if "data_base_ids" not in builder._scene.internal_vars:
        builder._scene.internal_vars["data_base_ids"] = dict()
    builder._scene.internal_vars["data_base_ids"][o.node_id] = (node_key, motion_id)
    if meta_info_str != "":
        c = o._components["animation_controller"]
        meta_info = json.loads(meta_info_str)
        if "sections" in meta_info:
            sections = meta_info["sections"]
            if type(sections) == list:
                semantic_annotation = create_annotation_from_sections_list(sections, motion_vector.n_frames)
            else:
                semantic_annotation = create_annotation_from_sections_dict(sections, motion_vector.n_frames)
            color_map = dict()
            for key in semantic_annotation.keys():
                color_map[key] = get_random_color()
            c.set_color_annotation(semantic_annotation, color_map)
    return o



def load_motion_from_json(builder, skeleton_data, motion_data, name, collection_id, motion_id, meta_data_str="", skeleton_model=None, is_processed=False, draw_mode=2, visualize=True, color=None, visible=True):
    if color is None:
        color = get_random_color()

    skeleton = SkeletonBuilder().load_from_custom_unity_format(skeleton_data)
    skeleton.skeleton_model = skeleton_model
    motion_vector = MotionVector()
    motion_vector.from_custom_db_format(motion_data)
    motion_vector.skeleton = skeleton
    skeleton.frame_time = motion_vector.frame_time
    #motion_vector.scale_root(scale)
    o = builder.create_object("animation_controller", name, skeleton, motion_vector, motion_vector.frame_time, draw_mode, visualize, color)
    o.visible = visible
    if "data_base_ids" not in builder._scene.internal_vars:
        builder._scene.internal_vars["data_base_ids"] = dict()
    builder._scene.internal_vars["data_base_ids"][o.node_id] = (collection_id, motion_id, is_processed)
    if meta_data_str != "":
        c = o._components["animation_controller"]
        meta_data = json.loads(meta_data_str)
        if "sections" in meta_data:
            sections = meta_data["sections"]
            print("sections", sections)
            sections = meta_data["sections"]
            if type(sections) == list:
                semantic_annotation = create_annotation_from_sections_list(sections, motion_vector.n_frames)
            else:
                semantic_annotation = create_annotation_from_sections_dict(sections, motion_vector.n_frames)
            color_map = dict()
            for key in semantic_annotation.keys():
                color_map[key] = get_random_color()
            c.set_color_annotation(semantic_annotation, color_map)

        if "time_function" in meta_data:
            print("set time_function")
            time_function = meta_data["time_function"]
            print(meta_data["time_function"])
            c.set_time_function(time_function)
        else:
            print("meta_data", meta_data)

    return o

SceneObjectBuilder.register_object("motion_from_str", load_motion_from_str)
SceneObjectBuilder.register_object("motion_from_json", load_motion_from_json)

