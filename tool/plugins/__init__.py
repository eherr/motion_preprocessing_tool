import os
import pickle
import json
from .morphablegraphs.morphable_graph_state_machine import MorphableGraphStateMachine, DEFAULT_CONFIG
from .morphablegraphs.core.motion_model.motion_state_graph_loader import MotionStateGraphLoader
from .morphablegraphs.morphable_graphs_controller import MorphableGraphsController, DEFAULT_ALGORITHM_CONFIG
from .morphablegraphs.motion_graph_controller import MotionGraphController
from .morphablegraphs.motion_primitive_controller import MotionPrimitiveController
from .morphablegraphs.blend_animation_controller import BlendAnimationController, AnimationBlendNode
from .morphablegraphs.simple_navigation_agent import SimpleNavigationAgent
from vis_utils.scene.scene_object_builder import SceneObjectBuilder, SceneObject
from vis_utils.scene.utils import get_random_color

def create_blend_controller(self, name, skeleton, motions, joint_name=None, constrained_frame=-1):
    joint_name = "hand_l"
    constrained_frame = 50
    count = float(len(motions))
    if count > 0:
        scene_object = SceneObject()
        scene_object.name = name
        blend_animation_controller = BlendAnimationController(scene_object)
        node = AnimationBlendNode()
        for idx, motion in enumerate(motions):
            print("add motion ", idx, count - 1)
            # pos = float(idx)/(count-1)
            if joint_name is None:
                x = motion.frames[constrained_frame][0]
                z = motion.frames[constrained_frame][2]
                node.add_motion("motion_" + str(idx), motion.frames, [x, z])
            else:
                frame = motion.frames[constrained_frame]
                p = skeleton.nodes[joint_name].get_global_position(frame)
                x = p[0]
                y = p[2]
                z = p[2]
                node.add_motion("motion_"+str(idx), motion.frames, [x,y, z])
        node.update_weights()
        if joint_name is None:
            node.set_parameter_labels(["x", "z"])
        else:
            node.set_parameter_labels(["x", "y", "z"])

        node.frame_time = motions[0].frame_time
        blend_animation_controller.set_track(node)
        blend_animation_controller.set_skeleton(skeleton)
        blend_animation_controller.updateTransformation(0)
        scene_object.add_component("blend_controller", blend_animation_controller)
        self._scene.addAnimationController(scene_object, "blend_controller")


def load_blend_controller(self, filename):
    with open(filename, "rb") as in_file:
        node = pickle.load(in_file)
        scene_object = SceneObject()
        name = filename.split("/")[-1]
        scene_object.name = name
        blend_animation_controller = BlendAnimationController(scene_object)
        blend_animation_controller.set_track(node)
        blend_animation_controller.set_skeleton(node.skeleton)
        blend_animation_controller.updateTransformation(0)
        scene_object.add_component("blend_controller", blend_animation_controller)
        self._scene.addAnimationController(scene_object, "blend_controller")


def load_morphable_graphs_file(builder, filename):
    scene_object = SceneObject()
    loader = MotionStateGraphLoader()
    loader.set_data_source(filename[:-4])
    loader.use_all_joints = False  # = set animated joints to all
    name = filename.split("/")[-1]
    graph = loader.build()
    animation_controller = MorphableGraphsController(scene_object, name, graph, color=get_random_color())
    scene_object.add_component("morphablegraphs_controller", animation_controller)
    scene_object.add_component("skeleton_vis", animation_controller._visualization)
    scene_object.name = animation_controller.name
    animation_controller.init_visualization()
    builder._scene.addAnimationController(scene_object, "morphablegraphs_controller")
    return scene_object


def load_motion_graph_controller(self, name, skeleton, motion_graph, frame_time):
    scene_object = SceneObject()
    motion_graph_controller = MotionGraphController(scene_object, color=get_random_color(), mg=motion_graph)
    motion_graph_controller.name = name
    motion_graph_controller.frameTime = frame_time
    motion_graph_controller.set_skeleton(skeleton)
    motion_graph_controller.init_visualization()
    scene_object.name = motion_graph_controller.name
    scene_object.add_component("motion_graph_controller", motion_graph_controller)
    self.addAnimationController(scene_object, "motion_graph_controller")
    return scene_object


    
def load_knn_controller(builder, graph_path):
    scene_object = SceneObject()
    scene_object.scene = builder._scene
    builder.create_component("knn_graph_controller", scene_object, graph_path)
    builder._scene.addObject(scene_object)
    return scene_object


SceneObjectBuilder.register_object("file_blend_controller", load_blend_controller)
SceneObjectBuilder.register_object("blend_controller", create_blend_controller)

SceneObjectBuilder.register_file_handler("motion_graph", load_motion_graph_controller)

def load_morphable_graph_state_machine(builder, path, use_all_joints=True):
    scene_object = SceneObject()
    scene_object.scene = builder._scene
    builder.create_component("morphablegraph_state_machine", scene_object, path, use_all_joints)
    builder._scene.addObject(scene_object)
    return scene_object

def load_morphable_graph_state_machine_from_db(builder, db_path, skeleton_name, graph_id, use_all_joints=False, config=DEFAULT_CONFIG):
    scene_object = SceneObject()
    scene_object.scene = builder._scene
    builder.create_component("morphablegraph_state_machine_from_db", scene_object,  db_path, skeleton_name, graph_id, use_all_joints, config)
    builder._scene.addObject(scene_object)
    return scene_object

def load_morphable_graphs_generator_from_db(builder, db_path, skeleton_name, graph_id, use_all_joints=False, config=DEFAULT_ALGORITHM_CONFIG):
    scene_object = SceneObject()
    scene_object.scene = builder._scene
    builder.create_component("morphablegraph_generator_from_db", scene_object,  db_path, skeleton_name, graph_id, use_all_joints, config)
    builder._scene.addObject(scene_object)
    return scene_object

def attach_mg_state_machine(builder, scene_object,file_path, use_all_joints=True, config=DEFAULT_CONFIG):
    color=get_random_color()  
    loader = MotionStateGraphLoader()
    loader.use_all_joints = use_all_joints# = set animated joints to all
    if os.path.isfile(file_path):
        loader.set_data_source(file_path[:-4])
        graph = loader.build()
        name = file_path.split("/")[-1]
        start_node = None
        animation_controller = MorphableGraphStateMachine(scene_object, graph, start_node, use_all_joints=use_all_joints, config=config, pfnn_data=loader.pfnn_data)
        scene_object.add_component("morphablegraph_state_machine", animation_controller)
        scene_object.name = name
        if builder._scene.visualize:
            vis = builder.create_component("skeleton_vis", scene_object, animation_controller.get_skeleton(), color)
            animation_controller.set_visualization(vis)
            #scene_object._components["morphablegraph_state_machine"].update_scene_object.connect(builder._scene.slotUpdateSceneObjectRelay)

        agent = SimpleNavigationAgent(scene_object)
        scene_object.add_component("nav_agent", agent)
        return animation_controller

    
def attach_mg_state_machine_from_db(builder, scene_object, db_url, skeleton_name, graph_id, use_all_joints=False, config=DEFAULT_CONFIG):
    color=get_random_color()
    loader = MotionStateGraphLoader()
    # set animated joints to all necessary for combination of models with different joints
    loader.use_all_joints = use_all_joints
    frame_time = 1.0/72
    graph = loader.build_from_database(db_url, skeleton_name, graph_id, frame_time)
    start_node = None
    name = skeleton_name
    animation_controller = MorphableGraphStateMachine(scene_object, graph, start_node, use_all_joints=use_all_joints, config=config, pfnn_data=loader.pfnn_data)
    scene_object.add_component("morphablegraph_state_machine", animation_controller)
    scene_object.name = name
    if builder._scene.visualize:
        vis = builder.create_component("skeleton_vis", scene_object, animation_controller.get_skeleton(), color)
        animation_controller.set_visualization(vis)
        #scene_object._components["morphablegraph_state_machine"].update_scene_object.connect(builder._scene.slotUpdateSceneObjectRelay)

    agent = SimpleNavigationAgent(scene_object)
    scene_object.add_component("nav_agent", agent)
    return animation_controller

def attach_mg_generator_from_db(builder, scene_object, db_url, skeleton_name, graph_id, use_all_joints=False, config=DEFAULT_CONFIG):
    color=get_random_color()
    loader = MotionStateGraphLoader()
    # set animated joints to all necessary for combination of models with different joints
    loader.use_all_joints = use_all_joints
    frame_time = 1.0/72
    graph = loader.build_from_database(db_url, skeleton_name, graph_id, frame_time)
    start_node = None
    name = skeleton_name
    animation_controller = MorphableGraphsController(scene_object, name, graph, start_node=start_node, config=DEFAULT_ALGORITHM_CONFIG, color=get_random_color()) #start_node, use_all_joints=use_all_joints, config=config, pfnn_data=loader.pfnn_data)
   
    #scene_object.add_component("skeleton_vis", animation_controller._visualization)
    scene_object.add_component("morphablegraphs_controller", animation_controller)
    scene_object.name = name
    if builder._scene.visualize:
        vis = builder.create_component("skeleton_vis", scene_object, animation_controller.get_skeleton(), color)
        animation_controller.set_visualization(vis)
        #scene_object._components["morphablegraph_state_machine"].update_scene_object.connect(builder._scene.slotUpdateSceneObjectRelay)
    return animation_controller

def load_motion_primitive(builder, file_path):
    scene_object = SceneObject()
    with open(file_path, "r") as in_file:
        data = json.load(in_file)
    name = file_path.split("/")[-1]
    animation_controller = MotionPrimitiveController(scene_object, name, data, color=get_random_color())
    scene_object.add_component("motion_primitive_controller", animation_controller)
    scene_object.name = animation_controller.name
    animation_controller.init_visualization()
    builder._scene.addAnimationController(scene_object, "motion_primitive_controller")
    return scene_object
    
def create_motion_primitive(builder, name, data, cluster_tree_data=None):
    scene_object = SceneObject()
    #data = json.loads(data_str)
    animation_controller = MotionPrimitiveController(scene_object, name, data, color=get_random_color())
    if cluster_tree_data is not None:
        animation_controller.load_cluster_tree_from_json(cluster_tree_data)
    scene_object.add_component("motion_primitive_controller", animation_controller)
    scene_object.name = animation_controller.name
    animation_controller.init_visualization()
    builder._scene.addAnimationController(scene_object, "motion_primitive_controller")
    return scene_object


SceneObjectBuilder.register_object("motion_primitive", create_motion_primitive)
SceneObjectBuilder.register_component("morphablegraph_state_machine", attach_mg_state_machine)
SceneObjectBuilder.register_component("morphablegraph_state_machine_from_db", attach_mg_state_machine_from_db)
SceneObjectBuilder.register_component("morphablegraph_generator_from_db", attach_mg_generator_from_db)
SceneObjectBuilder.register_file_handler("mg.zip", load_morphable_graph_state_machine)
SceneObjectBuilder.register_object("mg_state_machine_from_db", load_morphable_graph_state_machine_from_db)
SceneObjectBuilder.register_object("mg_generator_from_db", load_morphable_graphs_generator_from_db)
SceneObjectBuilder.register_file_handler("mm.json", load_motion_primitive)
SceneObjectBuilder.register_file_handler("zip", load_morphable_graphs_file)
