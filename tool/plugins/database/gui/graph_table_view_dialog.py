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
import json
import bson
import os
from PySide2.QtWidgets import  QDialog, QListWidgetItem, QFileDialog
from PySide2.QtCore import Qt
from .layout.graph_table_view_dialog_ui import Ui_Dialog
from tool.core.dialogs.utils import get_animation_controllers
from .graph_definition_dialog import GraphDefinitionDialog, EnterNameDialog
from tool.core.dialogs.confirmation_dialog import ConfirmationDialog
from anim_utils.animation_data import SkeletonBuilder
from anim_utils.utilities.db_interface import call_rest_interface, get_skeletons_from_remote_db, get_skeleton_from_remote_db, get_skeleton_model_from_remote_db
from vis_utils.io import load_json_file, save_json_file
from tool.plugins.database.session_manager import SessionManager
try:
    from morphablegraphs.utilities import convert_to_mgrd_skeleton
    from morphablegraphs.motion_model.motion_primitive_wrapper import MotionPrimitiveModelWrapper
    from morphablegraphs.utilities.db_interface import download_motion_model_from_remote_db, download_cluster_tree_from_remote_db
except:
    pass


def get_graph_list_from_db(url, skeleton):
    data = {"skeleton":skeleton}
    result_str = call_rest_interface(url, "get_graph_list", data)
    try:
        result_data = json.loads(result_str)
        print("graphs", result_data)
    except:
        result_data = None
    return result_data


def create_new_graph_in_db(url, name, skeleton, graph_data, session=None):
    data = {"name": name, "skeleton": skeleton, "data": graph_data}
    if session is not None:
        data.update(session)
    result_str = call_rest_interface(url, "upload_graph", data)


def replace_graph_in_remote_db(url, graph_id, name, skeleton, graph_data, session=None):
    data = {"id":graph_id,"name": name, "skeleton": skeleton, "data": graph_data}
    if session is not None:
        data.update(session)
    result_str = call_rest_interface(url, "replace_graph", data)


def delete_graph_from_remote_db(url, graph_id, session=None):
    data = {"id": graph_id}
    if session is not None:
        data.update(session)
    result_str = call_rest_interface(url, "remove_graph", data)


def download_graph_from_remote_db(url, graph_id, session=None):
    data = {"id": graph_id}
    if session is not None:
        data.update(session)
    result_str = call_rest_interface(url, "download_graph", data)
    print("recieved", result_str)
    try:
        result_data = json.loads(result_str)
    except:
        result_data = None
    return result_data



def get_avg_step_length(model, n_samples, method="median") :
    sample_lengths = []
    for i in range(n_samples):
        s = np.ravel(model.sample_low_dimensional_vector())
        sample_lengths.append(get_step_length_for_sample(model, s))
    if method == "average":
        step_length = sum(sample_lengths)/n_samples
    else:
        step_length = np.median(sample_lengths)
    return step_length

def get_step_length_for_sample(model, s, method="arc_length"):
    # get quaternion frames from s_vector
    quat_frames = model.back_project(s, use_time_parameters=False).get_motion_vector()
    if method == "arc_length":
        root_pos = quat_frames[:,:3]
        step_length = get_arc_length_from_points(root_pos)
    else:
        step_length = np.linalg.norm(quat_frames[-1][:3] - quat_frames[0][:3])
    return step_length

        
def get_arc_length_from_points(points):
    """
    Note: accuracy depends on the granulariy of points
    """
    points = np.asarray(points)
    arc_length = 0.0
    last_p = None
    for p in points:
        if last_p is not None:
            delta = p - last_p
            arc_length += np.linalg.norm(delta)
        last_p = p
    return arc_length



class GraphTableViewDialog(QDialog, Ui_Dialog):
    def __init__(self, scene, db_url, parent=None):
        QDialog.__init__(self, parent)
        Ui_Dialog.setupUi(self, self)
        self.scene = scene
        self.loadStateMachineButton.clicked.connect(self.slot_load_graph)
        self.addButton.clicked.connect(self.slot_add_graph)
        self.copyButton.clicked.connect(self.slot_copy_graph)
        self.editButton.clicked.connect(self.slot_edit_graph)
        self.removeButton.clicked.connect(self.slot_remove_graph)
        self.exportButton.clicked.connect(self.slot_export_graph)
        self.skeletonListComboBox.currentIndexChanged.connect(self.fill_graph_list)
        self.db_url = db_url
        self.session = SessionManager.session
        print("set session", self.session)
        self.fill_combo_box_with_skeletons()
        self.fill_graph_list()
        self.success = False

    def fill_combo_box_with_skeletons(self):
        self.skeletonListComboBox.clear()
        skeleton_list = get_skeletons_from_remote_db(self.db_url)
        if skeleton_list is None:
            return
        for idx, s in enumerate(skeleton_list):
            print(idx, s)
            self.skeletonListComboBox.addItem(s[1], idx)

    def fill_graph_list(self):
        self.graphListWidget.clear()
        skeleton = str(self.skeletonListComboBox.currentText())
        graph_list = get_graph_list_from_db(self.db_url, skeleton)
        if graph_list is None:
            return
        for graph_id, name in graph_list:
            item = QListWidgetItem()
            item.setText(name)
            item.setData(Qt.UserRole, graph_id)
            self.graphListWidget.addItem(item)

    def slot_add_graph(self):
        skeleton = str(self.skeletonListComboBox.currentText())
        dialog = GraphDefinitionDialog(self.db_url, skeleton)
        dialog.exec_()
        if dialog.success:
            create_new_graph_in_db(self.db_url, dialog.name, skeleton, dialog.data, self.session)
            self.fill_graph_list()

    def slot_load_graph(self):
        skeleton = str(self.skeletonListComboBox.currentText())
        item = self.graphListWidget.currentItem()
        if item is not None:
            name = str(item.text())
            graph_id = str(item.data(Qt.UserRole))
            use_all_joints = True
            self.scene.object_builder.create_object("mg_state_machine_from_db",self.db_url, skeleton, graph_id, use_all_joints=use_all_joints)

    def slot_edit_graph(self):
        skeleton = str(self.skeletonListComboBox.currentText())
        item = self.graphListWidget.currentItem()
        if item is not None:
            name = str(item.text())
            graph_id = str(item.data(Qt.UserRole))
            graph_data = download_graph_from_remote_db(self.db_url, graph_id)
            if graph_data is not None: 
                if type(graph_data) == str:
                    graph_data = json.loads(graph_data)
                dialog = GraphDefinitionDialog(self.db_url, skeleton, graph_data, name)
                dialog.exec_()
                if dialog.success:
                    print("replace")
                    replace_graph_in_remote_db(self.db_url, graph_id, dialog.name, skeleton, dialog.data, self.session)
                    self.fill_graph_list()
                else:
                    print("ignore changes")

    def slot_remove_graph(self):
        item = self.graphListWidget.currentItem()
        if item is not None:
            name = str(item.text())
            graph_id = str(item.data(Qt.UserRole))
            dialog = ConfirmationDialog()
            dialog.exec_()
            if dialog.success:
                delete_graph_from_remote_db(self.db_url, graph_id, self.session)
                self.fill_graph_list()
        
    def slot_copy_graph(self):
        skeleton = str(self.skeletonListComboBox.currentText())
        item = self.graphListWidget.currentItem()
        if item is not None:
            name = str(item.text())
            graph_id = str(item.data(Qt.UserRole))
            dialog = EnterNameDialog(name)
            dialog.exec_()
            if dialog.success:
                name = dialog.name
                graph_data = download_graph_from_remote_db(self.db_url, graph_id)
                create_new_graph_in_db(self.db_url, name, skeleton, graph_data, self.session)
                self.fill_graph_list()

    def slot_export_graph_(self):
        item = self.graphListWidget.currentItem()
        if item is not None:
            name = str(item.text())
            graph_id = str(item.data(Qt.UserRole))
            graph_data = download_graph_from_remote_db(self.db_url, graph_id)
            if graph_data is not None: 
                if type(graph_data) == str:
                    graph_data = json.loads(graph_data)
            filename = QFileDialog.getSaveFileName(self, 'Save To File', '.')[0]
            filename = str(filename)
            if os.path.isfile(filename):
                save_json_file(graph_data, filename)

    def slot_export_graph(self):
        skeleton_name = str(self.skeletonListComboBox.currentText())
        item = self.graphListWidget.currentItem()
        if item is None:
            return

        out_dir = QFileDialog.getExistingDirectory(self, "Select Directory")
        print("directory", out_dir)
        if not os.path.isdir(out_dir):
            return

        name = str(item.text())
        graph_id = str(item.data(Qt.UserRole))
        graph_data = download_graph_from_remote_db(self.db_url, graph_id)
        if graph_data is not None: 
            if type(graph_data) == str:
                graph_data = json.loads(graph_data)
        save_json_file(graph_data, out_dir + os.sep + "graph.json")

        skeleton_data = get_skeleton_from_remote_db(self.db_url, skeleton_name)
        skeleton = SkeletonBuilder().load_from_custom_unity_format(skeleton_data)
        mgrd_skeleton = convert_to_mgrd_skeleton(skeleton)
        skeleton.skeleton_model = get_skeleton_model_from_remote_db(self.db_url, skeleton_name)
        save_json_file(skeleton.to_json(), out_dir + os.sep + "skeleton.json")


        graph_def = dict()
        graph_def["formatVersion"] = "5.0"
        graph_def["usePickle"] = False
        graph_def["transitions"] = dict()
        graph_def["actionDefinitions"] = dict()
        if "start_node" in graph_data:
            graph_def["startNode"] = graph_data["start_node"]
        ea_dir = out_dir + os.sep + "elementary_action_models"
        for a in graph_data["nodes"]:
            action_def = dict()
            action_def["nodes"] = []
            action_def["constraint_slots"] = dict()
            action_data = graph_data["nodes"][a]
            action_dir = ea_dir + os.sep + "elementary_action_"+a
            if not os.path.isdir(action_dir):
                os.makedirs(action_dir)
            meta_info = dict()
            meta_info["stats"] = dict()
            start_states = []
            end_states = []
            idle_states = []
            single_states = []
            for model_id in action_data:
                mp_name = action_data[model_id]["name"]
                if mp_name.startswith("walk"):
                    mp_name =mp_name[5:]

                mp_type = action_data[model_id]["type"]
                action_def["nodes"].append(mp_name)
                transitions = list(action_data[model_id]["transitions"].keys())
                #transitions = [key.replace(":","_") for key in transitions]
                transitions = [key if not key[5:].startswith("walk") else key[:5]+key[10:] for key in transitions]
                graph_def["transitions"][a+":"+mp_name ] = transitions

                if mp_type == "start":
                    start_states.append(mp_name)
                elif mp_type == "end":
                    end_states.append(mp_name)
                elif mp_type == "idle":
                    idle_states.append(mp_name)
                elif mp_type == "single":
                    single_states.append(mp_name)
                meta_info["stats"][mp_name] = dict()
                print("export motion primitive", mp_name)
                model_data_str = download_motion_model_from_remote_db(self.db_url, model_id)
                #if not mp_name.startswith("walk"):
                mp_filename = a+"_"+mp_name
                #else:
                #    mp_filename = mp_name
                with open(action_dir+ os.sep +  mp_filename+ "_quaternion_mm.json", "w+") as out_file:
                    out_file.write(model_data_str)
                cluster_tree_data_str = download_cluster_tree_from_remote_db(self.db_url, model_id)
                if cluster_tree_data_str is not None and len(cluster_tree_data_str) > 0:
                    with open(action_dir+ os.sep + mp_filename + "_quaternion_cluster_tree.json", "w+") as out_file:
                        out_file.write(cluster_tree_data_str)

                model_data = json.loads(model_data_str)
                model = MotionPrimitiveModelWrapper()
                model._initialize_from_json(mgrd_skeleton, model_data)
                n_standard_transitions = 1
                n_samples = 5
                meta_info["stats"][mp_name]["average_step_length"] = get_avg_step_length(model, n_samples)
                meta_info["stats"][mp_name]["n_standard_transitions"] = n_standard_transitions
                if "keyframes" in model_data:
                    for key in model_data["keyframes"]:
                        action_def["constraint_slots"][key] = {"node": mp_name, "joint": "left_wrist"}

            # set node sequence
            action_def["node_sequence"] = []
            if len(action_data) == 1:
                mp_id = list(action_data.keys())[0]
                mp_name = action_data[mp_id]["name"]
                action_def["node_sequence"] = [[mp_name, "single_primitive"]]
 

            meta_info["start_states"] =start_states
            meta_info["end_states"] = end_states
            meta_info["idle_states"] = idle_states
            meta_info["single_states"] = single_states

            action_def["start_states"] = start_states
            action_def["end_states"] = end_states
            action_def["idle_states"] = idle_states
            graph_def["actionDefinitions"][a] = action_def

            save_json_file(meta_info, action_dir + os.sep + "meta_information.json")
        print("export graph definition", out_dir + os.sep + "graph_definition.json")
        save_json_file(graph_def, out_dir + os.sep + "graph_definition.json")