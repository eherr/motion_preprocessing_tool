import os
import pickle
import json
from .joint_control_knob import JointControlKnob
from vis_utils.graphics import materials
from vis_utils.graphics.geometry.mesh import Mesh
from vis_utils.scene.components import GeometryDataComponent
from vis_utils.scene.scene_object_builder import SceneObjectBuilder, SceneObject
from vis_utils.scene.utils import get_random_color
import vis_utils.constants as constants
from .animation_directory_explorer import AnimationDirectoryExplorer

 
def create_joint_control_knob(builder, anim_controller, joint_name, radius, material=materials.red):
    scene_object = SceneObject()
    geometry = Mesh.build_sphere(20, 20, 2 * radius, material)
    scene_object._components["geometry"] = GeometryDataComponent(scene_object, geometry)

    c = JointControlKnob(scene_object, anim_controller, joint_name)
    scene_object.add_component("joint_control_knob", c)
    builder._scene.addObject(scene_object)
    return scene_object


def create_animation_directory_explorer(builder, directory, filetype):
    scene_object = SceneObject()
    animation_controller = AnimationDirectoryExplorer(scene_object, directory, filetype, color=get_random_color())
    scene_object.add_component("animation_directory_explorer", animation_controller)
    scene_object.name = animation_controller.name
    builder._scene.addAnimationController(scene_object, "animation_directory_explorer")
    return scene_object


SceneObjectBuilder.register_object("joint_control_knob", create_joint_control_knob)
SceneObjectBuilder.register_object("animation_directory_explorer", create_animation_directory_explorer)
