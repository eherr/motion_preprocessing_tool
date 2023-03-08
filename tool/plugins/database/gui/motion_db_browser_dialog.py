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
"""https://stackoverflow.com/questions/4008649/qlistwidget-and-multiple-selection
"""
import os
import ssl
import math
import json
import bson
import numpy as np
import threading
import asyncio
from concurrent.futures import ProcessPoolExecutor
from multiprocessing import cpu_count
import matplotlib.pyplot as plt
from PySide2 import QtWidgets
from PySide2.QtWidgets import QDialog, QListWidgetItem, QFileDialog, QTreeWidgetItem
from PySide2.QtCore import Qt
from tool.core.dialogs.confirmation_dialog import ConfirmationDialog
from tool.core.dialogs.new_skeleton_dialog import NewSkeletonDialog
from .retarget_db_dialog import RetargetDBDialog
from .copy_db_dialog import CopyDBDialog
from .project_dialog import ProjectDialog
from .new_collection_dialog import NewCollectionDialog
from .edit_collection_dialog import EditCollectionDialog
from .motion_modelling_dialog import MotionModellingDialog
from .graph_table_view_dialog import GraphTableViewDialog
from .data_transform_dialog import DataTransformDialog
from tool.core.dialogs.skeleton_editor_dialog import SkeletonEditorDialog
from motion_db_interface import retarget_motion_in_db, start_cluster_job, MGModelDBSession
from vis_utils.io import load_json_file, save_json_file
from anim_utils.animation_data import MotionVector, SkeletonBuilder
from anim_utils.retargeting.analytical import Retargeting, generate_joint_map
from vis_utils.animation.animation_editor import AnimationEditorBase
from tool.core.application_manager import ApplicationManager
from .layout.motion_db_browser_dialog_ui import Ui_Dialog
from tool.plugins.database.session_manager import SessionManager
from tool.plugins.database import constants as db_constants
from morphablegraphs.utilities.db_interface import create_motion_model_in_db, align_motions_in_db, get_standard_config, create_cluster_tree_from_model, load_cluster_tree_from_json
from morphablegraphs.utilities import convert_to_mgrd_skeleton
from morphablegraphs.motion_model.motion_primitive_wrapper import MotionPrimitiveModelWrapper
from anim_utils.animation_data import SkeletonBuilder
if (not os.environ.get('PYTHONHTTPSVERIFY', '') and
getattr(ssl, '_create_unverified_context', None)):
    ssl._create_default_https_context = ssl._create_unverified_context

from motion_db_interface.data_transform_interface import run_data_transform



def normalize(v):
    return v/np.linalg.norm(v)


def quaternion_to_axis_angle(q):
    """http://www.euclideanspace.com/maths/geometry/rotations/conversions/quaternionToAngle/

    """
    a = 2* math.acos(q[0])
    s = math.sqrt(1- q[0]*q[0])
    if s < 0.001:
        x = q[1]
        y = q[2]
        z = q[3]
    else:
        x = q[1] / s
        y = q[2] / s
        z = q[3] / s
    v = np.array([x,y,z])
    if np.sum(v)> 0:
        return normalize(v),a
    else:
        return v, a

def quaternion_to_axis_angle2(q):
    """http://www.euclideanspace.com/maths/geometry/rotations/conversions/quaternionToAngle/

    """
    a = 2* math.acos(q[0])
    x = q[1] / math.sqrt(1-q[0]*q[0])
    y = q[2] / math.sqrt(1-q[0]*q[0])
    z = q[3] / math.sqrt(1-q[0]*q[0])
    return normalize([x,y,z]),a

    

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
    
def get_step_length_for_sample(model, s, method="arc_length"):
    # get quaternion frames from s_vector
    quat_frames = model.back_project(s, use_time_parameters=False).get_motion_vector()
    if method == "arc_length":
        root_pos = quat_frames[:,:3]
        step_length = get_arc_length_from_points(root_pos)
    else:
        step_length = np.linalg.norm(quat_frames[-1][:3] - quat_frames[0][:3])
    return step_length

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



def chunks(l, n):
    """Yield successive n-sized chunks from l.
    https://stackoverflow.com/questions/312443/how-do-you-split-a-list-into-evenly-sized-chunks"""
    for i in range(0, len(l), n):
        yield l[i:i + n]


def retarget_batch(params):
    db_url, batch, retargeting, collection, target_skeleton_name, is_aligned, session = params
    for item in batch:
        print(item)
        retarget_motion_in_db(db_url, retargeting, item[0], item[1], collection, target_skeleton_name, is_aligned, session)


@asyncio.coroutine
def run_retargeting_process(pool, db_url, batch, retargeting, collection, target_skeleton_name, is_aligned, session):
    print("start retarging", len(batch), "motions")
    params = db_url, batch, retargeting, collection, target_skeleton_name, is_aligned, session
    fut = pool.submit(retarget_batch, params)
    while not fut.done() and not fut.cancelled():
        yield from asyncio.sleep(0.1)
    print("done")

def add_plot(ax, timesteps, rewards, lengths, label):
    ax[0].plot(timesteps, rewards, label = label)
    ax[0].set_xlabel('timesteps')
    ax[0].set_ylabel('rewards')
    ax[1].plot(timesteps, lengths, label = label)
    ax[1].set_xlabel('timesteps')
    ax[1].set_ylabel('lengths')

def plot_experiment(runs):
    fig, ax = plt.subplots(1,2)
    for label in runs:
        add_plot(ax, runs[label]["t"], runs[label]["r"], runs[label]["l"], label)
    plt.tight_layout()
    plt.legend()
    plt.show()

class MotionDBBrowserDialog(QDialog, Ui_Dialog):
    def __init__(self, scene, parent=None):
        QDialog.__init__(self, parent)
        self.setModal(0)
        Ui_Dialog.setupUi(self, self)
        self.scene = scene
        self.newProjectButton.clicked.connect(self.slot_new_project)
        self.editProjectButton.clicked.connect(self.slot_edit_project)
        self.deleteProjectButton.clicked.connect(self.slot_delete_project)
        self.loadFilesButton.clicked.connect(self.slot_load_files)
        self.exportFilesButton.clicked.connect(self.slot_export_file)
        self.deleteFilesButton.clicked.connect(self.slot_delete_file)
        self.addCollectionButton.clicked.connect(self.slot_new_collection)
        self.editCollectionButton.clicked.connect(self.slot_edit_collection)
        self.deleteCollectionButton.clicked.connect(self.slot_delete_collection)
        self.newSkeletonButton.clicked.connect(self.slot_new_skeleton)
        self.deleteSkeletonButton.clicked.connect(self.slot_delete_skeleton)
        self.loadSkeletonButton.clicked.connect(self.slot_load_skeleton)
        self.replaceSkeletonButton.clicked.connect(self.slot_replace_skeleton)
        self.exportSkeletonButton.clicked.connect(self.slot_export_skeleton)
        self.newTagButton.clicked.connect(self.slot_new_tag)
        self.renameTagButton.clicked.connect(self.slot_rename_tag)
        self.deleteTagButton.clicked.connect(self.slot_delete_tag)
        self.importCollectionButton.clicked.connect(self.slot_import_collection_from_folder)
        self.exportCollectionButton.clicked.connect(self.slot_export_collection_to_folder)
        self.importFileButton.clicked.connect(self.slot_import_file)
        self.exportDatabaseButton.clicked.connect(self.slot_export_database_to_folder)
        self.retargetMotionsButton.clicked.connect(self.slot_retarget_motions_parallel)
        self.copyMotionsButton.clicked.connect(self.slot_copy_motions)
        self.generateModelGraphButton.clicked.connect(self.slot_generate_graph_definition)
        self.editSkeletonButton.clicked.connect(self.slot_edit_skeleton)
        self.debugInfoButton.clicked.connect(self.slot_print_debug_info)
        self.plotExperimentButton.clicked.connect(self.slot_plot_experiment)
        self.exportExperimentButton.clicked.connect(self.slot_export_experiment)
        self.deleteExperimentButton.clicked.connect(self.slot_delete_experiment)
        self.runDataTransformButton.clicked.connect(self.slot_run_data_transforms)
        #self.alignMotionsButton.clicked.connect(self.slot_align_motions)
        #self.createMotionModelButton.clicked.connect(self.slot_create_motion_model)
        #self.setTimeFunctionButton.clicked.connect(self.slot_set_timefunction)
        #self.editMotionsButton.clicked.connect(self.slot_edit_motions)
        #self.createClusterTreeButton.clicked.connect(self.slot_create_cluster_tree)
        self.rootItem = None
        self.db_url = db_constants.DB_URL
        self.session = SessionManager.session
        self.mdb_session = MGModelDBSession(self.db_url, self.session)
        print("set session", self.session)
        if self.session is not None and "user" in self.session:
            self.statusLabel.setText("Status: Authenticated as "+self.session["user"])
        else:
            self.disable_editing()
            self.statusLabel.setText("Status: Not authenticated")

            
        self.urlLineEdit.setText(self.db_url)
        self.project_info = None
        self.fill_combo_box_with_tags()
        self.fill_combo_box_with_projects()
        self.fill_combo_box_with_skeletons()
        self.update_collection_tree()
        self.fileListWidget.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.skeletonListComboBox.currentIndexChanged.connect(self.update_lists)
        self.projectListComboBox.currentIndexChanged.connect(self.update_collection_tree)
        self.tagComboBox.currentIndexChanged.connect(self.update_lists)
        self.collectionTreeWidget.itemClicked.connect(self.update_lists)
        self.urlLineEdit.textChanged.connect(self.set_url)
        self.tabWidget.currentChanged.connect(self.on_tab_change)
        self.n_samples = 10000
        self.n_subdivisions_per_level = 4
        self.k8s_resources = db_constants.K8S_RESOURCES
        self.k8s_imagename = db_constants.K8S_IMAGE_NAME
        self.mg_repo_url =  db_constants.MG_REPO_URL
        self.mg_exec_dir =  db_constants.MG_EXEC_DIR
        self.model_filter = None
        self.show()

    def closeEvent(self, event):
        parent = self.parent()
        if parent is not None:
            parent.motion_db_browser_dialog = None

    def exit(self):
        self.close()
    	
    
    def set_url(self, text):
        print("set url", text)
        self.db_url = str(text)

    def on_tab_change(self):
        tab_name = self.tabWidget.currentWidget().objectName()
        print("tab_name", tab_name)

    def update_collection_tree(self):
        project_id = self.projectListComboBox.currentData()
        self.project_info = self.mdb_session.get_project_info(project_id)
        if self.project_info is None:
            print("Error: project could not be found", project_id)
            return
        t = threading.Thread(target=self._update_collection_tree)
        t.start()
        
    def _update_collection_tree(self):
        self.fill_tree_widget()
        self._update_lists()

    def update_lists(self):
        t = threading.Thread(target=self._update_lists)
        t.start()

    def _update_lists(self):
        self._fill_file_list_from_db()
        self._fill_experiment_list_from_db()

    def fill_combo_box_with_tags(self):
        self.tagComboBox.clear()
        tag_list = self.mdb_session.get_tag_list()
        print("get_tag_list", tag_list)
        if tag_list is None:
            return
        for p in tag_list:
            p_name = p[0]
            self.tagComboBox.addItem(p_name, p[0])

    def fill_combo_box_with_projects(self):
        self.projectListComboBox.clear()
        project_list = self.mdb_session.get_project_list()
        print("project_list", project_list)
        if project_list is None:
            return
        for p in project_list:
            p_name = p[1]
            self.projectListComboBox.addItem(p_name, p[0])

    def fill_tree_widget(self):
        self.collectionTreeWidget.clear()
        collection = self.project_info["collection"]
        self.rootItem = QTreeWidgetItem(self.collectionTreeWidget, ["root", "root"])
        self.rootItem.setData(0, Qt.UserRole, collection)
        collection_tree = self.mdb_session.get_collections_tree(collection)
        self._fill_tree_widget(collection_tree, self.rootItem)
        self.rootItem.setExpanded(True)

    def _fill_tree_widget(self, collection_tree, parent_item):
        for key in collection_tree:
            col = collection_tree[key]
            col_item = QTreeWidgetItem(parent_item, [col["name"],col["type"]])
            col_item.setData(0, Qt.UserRole, key)
            self._fill_tree_widget(col["sub_tree"], col_item)

    def fill_combo_box_with_skeletons(self):
        self.skeletonListComboBox.clear()
        skeleton_list = self.mdb_session.get_skeleton_list()
        if skeleton_list is None:
            return
        print(skeleton_list)
        for idx, s in enumerate(skeleton_list):
            s_name = s[1]
            self.skeletonListComboBox.addItem(s_name, idx)

    def get_collection(self):
        colItem = self.collectionTreeWidget.currentItem()
        if colItem is None:
            return
        return int(colItem.data(0, Qt.UserRole)),  str(colItem.text(0)), str(colItem.text(1))

    def get_collection_parent(self):
        colItem = self.collectionTreeWidget.currentItem()
        if colItem is None:
            return
        parent = colItem.parent()
        if parent is None:
            return
        return int(parent.data(0, Qt.UserRole)),  str(parent.text(0)), str(parent.text(1))

    def _fill_file_list_from_db(self, idx=None):
        self.fileListWidget.clear()
        col = self.get_collection()
        if col is None:
            return
        c_id, c_name, c_type = col
        print("update lists", c_id)
        skeleton = str(self.skeletonListComboBox.currentText())
        tags = [str(self.tagComboBox.currentText())]
        motion_list = self.mdb_session.get_file_list(c_id, skeleton, tags=tags)
        if motion_list is None:
            return
        print("loaded", len(motion_list), "clips")
        for m in motion_list:
            node_id = m[0]
            name = m[1]
            data_type = m[2]
            print(m)
            item = QListWidgetItem()
            item.setText(name+"."+data_type)
            item.setData(Qt.UserRole, node_id)
            self.fileListWidget.addItem(item)
        
    def _fill_experiment_list_from_db(self, idx=None):
        self.experimentListWidget.clear()
        col = self.get_collection()
        if col is None:
            return
        c_id, c_name, c_type = col
        skeleton = str(self.skeletonListComboBox.currentText())
        exp_list = self.mdb_session.get_experiment_list(c_id, skeleton)
        print("experiment list", exp_list)
        if exp_list is None:
            return
        for node_id, name in exp_list:
            item = QListWidgetItem()
            item.setText(name)
            item.setData(Qt.UserRole, node_id)
            self.experimentListWidget.addItem(item)


    def slot_load_motions(self):
        items = self.fileListWidget.selectedItems()
        col = self.get_collection()
        if col is None:
            return
        c_id, c_name, c_type = col
        n_motions = len(items)
        count = 1
        for item in items:
            motion_id = int(item.data(Qt.UserRole))
            motion_name = str(item.text())
            print("download motion", str(count)+"/"+str(n_motions), motion_name)
            self.load_motion_from_db(motion_id, motion_name, c_id)

            count+=1

    def slot_load_files(self):
        skeleton_name = str(self.skeletonListComboBox.currentText())
        skeleton_data = self.mdb_session.get_skeleton_data(skeleton_name) 
        if skeleton_data is None:
            print("Error: skeleton data is empty")
            return
        items = self.fileListWidget.selectedItems()
        for item in items:
            file_id = int(item.data(Qt.UserRole))
            name = str(item.text())
            data_type = name.split(".")[-1]
            data_type_info = self.mdb_session.get_data_loader_info(data_type, "vis_utils")
            print(data_type_info)
            if data_type_info is not None and "script" in data_type_info:
                loader_script = data_type_info["script"]
                loader_script = loader_script.replace("\r\n", "\n")
                self.scene.object_builder.load_dynamic_module(data_type, loader_script)
                data = self.mdb_session.download_file(file_id)
                if data is None:
                    return
                self.scene.object_builder.create_object(data_type, name, skeleton_data, data)
            else:
                col = self.get_collection()
                if col is None:
                    return
                c_id, c_name, c_type = col
                self.load_motion_from_db(file_id, skeleton_data, name, c_id)

    def load_motion_from_db(self, motion_id, skeleton_data, motion_name, collection):
        motion_data = self.mdb_session.get_motion_data(motion_id, False)
        meta_info_str = self.mdb_session.get_motion_meta_data(motion_id, False)
        if motion_data is None:
            print("Error: loaded motion data is empty")
            return
        visible = True
        skeleton_model = None
        self.scene.object_builder.create_object("motion_from_json", skeleton_data, motion_data, motion_name, collection, motion_id, meta_info_str, skeleton_model, False, visible=visible)

    def slot_delete_file(self):
        dialog = ConfirmationDialog()
        dialog.exec_()
        if dialog.success:
            items = self.fileListWidget.selectedItems()
            for item in items:
                selected_id = int(item.data(Qt.UserRole))
                print("delete", selected_id)
                self.mdb_session.delete_file(selected_id)
            self._fill_file_list_from_db()

    def slot_new_project(self):
        dialog = ProjectDialog(dict())
        dialog.exec_()
        if dialog.success:
            self.mdb_session.add_new_project(dialog.name, dialog.is_public)
            self.fill_combo_box_with_projects()
            self.update_collection_tree()
    
    def slot_edit_project(self):
        if self.project_info is None:
            return
        dialog = ProjectDialog(self.project_info)
        dialog.exec_()
        if dialog.success:
            project_id = self.projectListComboBox.currentData()
            self.mdb_session.edit_project(project_id, dialog.name, dialog.is_public)
            self.fill_combo_box_with_projects()
            self.update_collection_tree()

    def slot_delete_project(self):
        dialog = ConfirmationDialog()
        dialog.exec_()
        if dialog.success:
            project_id = self.projectListComboBox.currentData()
            self.mdb_session.remove_project(project_id)
            self.fill_combo_box_with_projects()
            self.update_collection_tree()


    def slot_new_collection(self):
        col = self.get_collection()
        if col is None:
            return
        c_id, c_name, c_type = col
        dialog = NewCollectionDialog(c_name, c_id)
        dialog.exec_()
        if dialog.success:
            name = dialog.name
            col_type = dialog.col_type
            owner = dialog.owner
            print("create", name, col_type)
            self.mdb_session.create_new_collection(name, col_type, c_id, owner)
            self.fill_tree_widget()
            self._fill_file_list_from_db()
    
    def slot_edit_collection(self):
        col = self.get_collection()
        if col is None:
            return
        c_id, c_name, c_type = col
        parent = self.get_collection_parent()
        if parent is None:
            return 
        p_id, p_name, p_type = parent
        print("edit", c_name, c_type)
        dialog = EditCollectionDialog(c_id, p_name, p_id, c_name, c_type, 0)
        dialog.exec_()
        if dialog.success:
            name = dialog.name
            col_type = dialog.col_type
            p_id = dialog.parent_id
            owner = dialog.owner
            print("set to", name, col_type)
            self.mdb_session.replace_collection(c_id, name, col_type, p_id, owner)
            self.fill_tree_widget()
            self._fill_file_list_from_db()


    def slot_delete_collection(self):
        dialog = ConfirmationDialog()
        dialog.exec_()
        if dialog.success:
            collection = self.get_collection()
            if collection is not None:
                self.mdb_session.delete_collection(collection[0])
                self.fill_tree_widget()
                self._fill_file_list_from_db()

    def slot_new_skeleton(self):
        dialog = NewSkeletonDialog()
        dialog.exec_()
        if dialog.success:
            name = dialog.name
            data = dialog.data
            meta_data = dialog.skeleton_model
            if data is not None:
                data = json.dumps(data)
                if meta_data is not None:
                    meta_data = json.dumps(meta_data)
                #elif name in SKELETON_MODELS:
                #    meta_data = json.dumps(SKELETON_MODELS[name])
                self.mdb_session.create_new_skeleton(name, data, meta_data)
                self.fill_combo_box_with_skeletons()
                self._fill_file_list_from_db()
            else:
                print("data is None")
        
    def slot_delete_skeleton(self):
        dialog = ConfirmationDialog()
        dialog.exec_()
        if dialog.success:
            skeleton_name = str(self.skeletonListComboBox.currentText())
            self.mdb_session.delete_skeleton(skeleton_name)
            self.fill_combo_box_with_skeletons()
            self._fill_file_list_from_db()

    def slot_export_collection_to_folder(self):
        directory = QFileDialog.getExistingDirectory(self, "Select Directory")
        print("directory", directory)
        if os.path.isdir(directory):
            col = self.get_collection()
            if col is None:
                return
            c_id, c_name, c_type = col
            skeleton_name = str(self.skeletonListComboBox.currentText())
            self.mdb_session.export_collection_clips_to_folder(c_id, skeleton_name, directory)

    def slot_import_collection_from_folder(self):
        directory = QFileDialog.getExistingDirectory(self, "Select Directory")
        print("directory", directory)
        if os.path.isdir(directory):
            col = self.get_collection()
            if col is None:
                return
            c_id, c_name, c_type = col
            self.mdb_session.import_collection_from_directory(c_id, directory)
            self._fill_file_list_from_db()

    def delete_motion(self, motion_id_list):
        for motion_id in motion_id_list:
            self.mdb_session.delete_motion(motion_id)
        self._fill_file_list_from_db()

    def slot_align_motions(self):
        """ run alignment
            upload aligned data to db
        """
        col = self.get_collection()
        if col is None:
            return
        c_id, c_name, c_type = col
        skeleton_name = str(self.skeletonListComboBox.currentText())
        align_motions_in_db(self.db_url, skeleton_name, c_id, session=self.session)
        #job_name = "alignment" +str(col[0])
        parameter_str = self.db_url+ " " + skeleton_name + " "+ str(c_id)
        #if self.session is not None:
        #    parameter_str += " --user "+ self.session["user"] + " --token " + self.session["token"]
        #job_desc = dict()
        #job_desc["command"] = "pip install -r requirements.txt; python run_alignment_in_db.py " + parameter_str
        #job_desc["exec_dir"] = self.mg_exec_dir
        #job_desc["repo_url"] = self.mg_repo_url
        #job_desc["aws"]  = None
        #start_cluster_job(self.db_url, self.k8s_imagename, job_name, job_desc, self.k8s_resources, self.session)
        #print("run on alignment on cluster")

    def slot_create_motion_model(self):
        """ run modeling of aligned data
            upload model to db
        """
        col = self.get_collection()
        if col is None:
            return
        c_id, c_name, c_type = col
        skeleton_name = str(self.skeletonListComboBox.currentText())
        
        config = get_standard_config()
        spline_basis_factor = config["n_spatial_basis_factor"]
        skeleton = self.mdb_session.load_skeleton(skeleton_name)
        dialog = MotionModellingDialog(skeleton, c_name, spline_basis_factor)
        dialog.exec_()
        if not dialog.success:
            return

        name = dialog.name
        spline_basis_factor = dialog.spline_basis_factor
        animated_joints = dialog.animated_joints
        create_motion_model_in_db(self.db_url, skeleton_name, c_id, name, spline_basis_factor, animated_joints, self.session)
        
        #parameter_str = self.db_url+ " " + skeleton_name + " "+ str(c_id) +" " +name + " " + str(spline_basis_factor)
        #if animated_joints:
        #    parameter_str += " --joint_filter "
        #    for joint_name in animated_joints:
        #        parameter_str += " " + joint_name
        #parameter_str = self.db_url+ " " + skeleton_name + " "+ str(c_id)
        #if self.session is not None:
        #    parameter_str += " --user "+ self.session["user"] + " --token " + self.session["token"]
        #job_name = "statistical" +str(col[0])
        #job_desc = dict()
        #job_desc["command"] = "pip install -r requirements.txt; python run_construction_in_db.py " + parameter_str
        #job_desc["exec_dir"] = self.mg_exec_dir
        #job_desc["repo_url"] = self.mg_repo_url
        #job_desc["aws"]  = None
        #start_cluster_job(self.db_url, self.k8s_imagename, job_name, job_desc, self.k8s_resources, self.session)
        #print("run on modelling on cluster")

    def slot_import_file(self):
        filename = QFileDialog.getOpenFileName(self, 'Open File', '.')[0]
        filename = str(filename)
        if os.path.isfile(filename):
            model_data = load_json_file(filename)
            col = self.get_collection()
            if col is None:
                return
            c_id, c_name, c_type = col
            skeleton = str(self.skeletonListComboBox.currentText())
            name = filename.split(os.sep)[-1]
            config = get_standard_config()
            self.mdb_session.upload_model(name, c_id, skeleton, model_data, model_format="mpm", config=config)


        
    def slot_export_file(self):
        item = self.fileListWidget.currentItem()
        model_id = int(item.data(Qt.UserRole))
        model_name = str(item.text())
        model_data = self.mdb_session.download_model(model_id)
        if model_data is not None:
            filename = QFileDialog.getSaveFileName(self, 'Save To File', '.')[0]
            with open(filename, "wb") as out_file:
                out_file.write(model_data)

    def slot_create_cluster_tree(self):
        item = self.fileListWidget.currentItem()
        model_id = int(item.data(Qt.UserRole))
        model_data = self.mdb_session.download_motion_model(model_id)
        tree = create_cluster_tree_from_model(model_data, self.n_samples, self.n_subdivisions_per_level)
        tree_data = dict()
        tree_data["data"] = tree.data.tolist()
        tree_data["features"] = tree._features.tolist()
        tree_data["options"] = tree._options
        tree_data["root"] = tree.node_to_json()
        tree_data = json.dumps(tree_data)
        self.mdb_session.upload_cluster_tree(model_id, tree_data)

    def slot_export_cluster_tree_json(self):
        item = self.fileListWidget.currentItem()
        model_id = int(item.data(Qt.UserRole))
        cluster_tree_data_str = self.mdb_session.download_cluster_tree(model_id)
        if cluster_tree_data_str is not None:
            filename = QFileDialog.getSaveFileName(self, 'Save To File', '.')[0]
            with open(filename, "w") as out_file:
                out_file.write(cluster_tree_data_str)
    
    def slot_export_cluster_tree_pickle(self):
        item = self.fileListWidget.currentItem()
        model_id = int(item.data(Qt.UserRole))
        cluster_tree_data = self.mdb_session.download_cluster_tree(model_id)
        if cluster_tree_data is not None:
            cluster_tree = load_cluster_tree_from_json(cluster_tree_data)
            filename = QFileDialog.getSaveFileName(self, 'Save To File', '.')[0]
            cluster_tree.save_to_file_pickle(filename)
 
    def slot_export_database_to_folder(self):
        directory = QFileDialog.getExistingDirectory(self, "Select Directory")
        if os.path.isdir(directory):
            for i in range(self.skeletonListComboBox.count()):
                skeleton_name = str(self.skeletonListComboBox.itemText(i))
                self.mdb_session.export_database_of_skeleton_to_directory(directory, skeleton_name)
        
    def slot_retarget_motions(self, is_aligned=0):
        dialog = RetargetDBDialog(self.db_url)
        dialog.exec_()
        if dialog.success and dialog.collection is not None:
            collection = dialog.collection
            src_skeleton_name = dialog.src_model
            target_skeleton_name = dialog.target_model
            src_scale = dialog.scale_factor
            place_on_ground = dialog.place_on_ground
            if is_aligned==0:
                items = self.fileListWidget.selectedItems()
            else:
                items = self.fileListWidget.selectedItems()
            n_motions = len(items)
            motions = []
            for item in items:
                motion_id = int(item.data(Qt.UserRole))
                motion_name = str(item.text())
                motions.append((motion_id, motion_name))

            src_skeleton = self.mdb_session.load_skeleton(src_skeleton_name)
            target_skeleton = self.mdb_session.load_skeleton(target_skeleton_name)
            
            joint_map = generate_joint_map(src_skeleton.skeleton_model, target_skeleton.skeleton_model)
            retargeting = Retargeting(src_skeleton, target_skeleton, joint_map, src_scale, additional_rotation_map=None, place_on_ground=place_on_ground)
       
            count = 1
            for motion_id, motion_name in motions:
                print("retarget motion", str(count)+"/"+str(n_motions), motion_name)
                retarget_motion_in_db(self.db_url, retargeting, motion_id, motion_name, collection, target_skeleton_name, is_aligned, session=self.session)
                count+=1

    def slot_retarget_motions_parallel(self):
        col = self.get_collection()
        if col is None:
            return
        dialog = RetargetDBDialog(self.db_url)
        dialog.exec_()
        if dialog.success and dialog.collection is not None:
            collection = dialog.collection
            src_skeleton_name = dialog.src_model
            target_skeleton_name = dialog.target_model
            src_scale = dialog.scale_factor
            place_on_ground = int(dialog.place_on_ground)
            #    job_name = "retargeting" +str(col[0])
            #    imagename = "python:3.5.3"
            #    job_desc = dict()
            #    parameter_str = self.db_url+ " " + src_skeleton_name + " "+ target_skeleton_name + " "+ str(col[0])+ " "+str(is_aligned) +" "+ str(src_scale) +" "+ str(place_on_ground) 
            #    
            #    if self.session is not None:
            #        parameter_str += " --user "+ self.session["user"] + " --token " + self.session["token"]
            #    job_desc["command"] = "pip install -r requirements.txt; python run_retargeting_in_db.py " + parameter_str
            #    job_desc["exec_dir"] = self.mg_exec_dir
            #    job_desc["repo_url"] = self.mg_repo_url
            #    job_desc["aws"]  = None
            #    start_cluster_job(self.db_url, self.k8s_imagename, job_name, job_desc, self.k8s_resources, self.session)
            #    print("run on retargeting on cluster")
            items = self.fileListWidget.selectedItems()
            n_motions = len(items)
            
            motions = []
            for item in items:
                motion_id = int(item.data(Qt.UserRole))
                motion_name = str(item.text())
                motions.append((motion_id, motion_name))
            src_skeleton = self.mdb_session.load_skeleton(src_skeleton_name)
            target_skeleton = self.mdb_session.load_skeleton(target_skeleton_name)
            joint_map = generate_joint_map(src_skeleton.skeleton_model, target_skeleton.skeleton_model)
            retargeting = Retargeting(src_skeleton, target_skeleton, joint_map, src_scale, additional_rotation_map=None, place_on_ground=place_on_ground)

            n_workers = cpu_count()
            if n_workers > n_motions:
                n_workers = n_motions
            n_batches = int(len(motions) / n_workers)
            pool = ProcessPoolExecutor(max_workers=n_workers)
            tasks = []
            for motion_batch in chunks(motions, n_batches):
                t = run_retargeting_process(pool, self.db_url, motion_batch, retargeting, collection, target_skeleton_name, is_aligned, self.session)
                tasks.append(t)
            asyncio.get_event_loop().run_until_complete(asyncio.gather(*tasks))

    def slot_copy_motions(self):
        dialog = CopyDBDialog(self.db_url)
        dialog.exec_()
        if dialog.success and dialog.collection is not None:
            collection = dialog.collection
            skeleton_name = str(self.skeletonListComboBox.currentText())
            skeleton = self.mdb_session.load_skeleton(skeleton_name)
            items = self.fileListWidget.selectedItems()
            n_motions = len(items)
            count = 1
            for item in items:
                motion_id = int(item.data(Qt.UserRole))
                motion_name = str(item.text())
                motion_name+="_copy"
                print("copy motion", str(count)+"/"+str(n_motions), motion_name)
                self.mdb_session.copy_motion_in_db(motion_id, motion_name, collection, skeleton_name)
                count+=1

    def slot_edit_motions(self):
        filename = QFileDialog.getOpenFileName(self, 'Open File', '.')[0]
        filename = str(filename)
        if os.path.isfile(filename):
            instructions = load_json_file(filename)
            col = self.get_collection()
            if col is None:
                return
            c_id, c_name, c_type = col
            skeleton_name = str(self.skeletonListComboBox.currentText())
            items = self.fileListWidget.selectedItems()
            n_motions = len(items)
            skeleton = self.mdb_session.load_skeleton(skeleton_name)
            count = 1
            for item in items:
                motion_id = int(item.data(Qt.UserRole))
                motion_name = str(item.text())
                print("edit motion", str(count)+"/"+str(n_motions), motion_name)
                self.edit_motion_in_db(skeleton, motion_id, motion_name, c_id, skeleton_name, instructions)
                count += 1

    def edit_motion_in_db(self, skeleton, motion_id, motion_name, collection, skeleton_name, instructions): 
        motion_data = self.mdb_session.get_motion_data(motion_id, is_processed=False)
        if motion_data is None:
            print("Error: motion data is empty")
            return
        motion_vector = MotionVector()
        motion_vector.from_custom_db_format(motion_data)
        motion_vector.skeleton = skeleton
        
        anim_editor = AnimationEditorBase(skeleton, motion_vector)
        for func_name, params in instructions:
            anim_editor.apply_edit(func_name, params)

        #bvh_str = get_bvh_string(skeleton, motion_vector.frames)
        motion_data = motion_vector.to_db_format()
        meta_data = None
        self.mdb_session.replace_motion(motion_id, motion_name, motion_data, collection, skeleton_name, meta_data, is_processed=False)

    def slot_set_timefunction(self):
        filename = QFileDialog.getOpenFileName(self, 'Open File', '.')[0]
        filename = str(filename)
        if os.path.isfile(filename):
            temporal_data = load_json_file(filename)
            items = self.fileListWidget.selectedItems()
            n_motions = len(items)
            count = 1
            for item in items:
                motion_id = int(item.data(Qt.UserRole))
                motion_name = str(item.text())
                if motion_name in temporal_data:
                    print("set time warping ", str(count)+"/"+str(n_motions), motion_name)
                    time_function = temporal_data[motion_name]
                    data = ""
                    collection = ""
                    skeleton_name = ""
                    meta_data = self.mdb_session.get_motion_meta_data(motion_id, is_processed=False)
                    if meta_data is None:
                        meta_data = dict()
                    meta_data["time_function"] = time_function
                    meta_data =  bson.dumps(meta_data)
                    self.mdb_session.replace_motion(motion_id, motion_name, data, collection, 
                                        skeleton_name, meta_data, is_processed=True)
                count += 1

    def slot_generate_graph_definition(self):
        dialog = GraphTableViewDialog(self.scene, self.db_url)
        dialog.exec_()
        if dialog.success:
            return
    
    def slot_load_skeleton(self):
        skeleton_name = str(self.skeletonListComboBox.currentText())
        skeleton = self.mdb_session.load_skeleton(skeleton_name)
        if skeleton is not None:
            motion_vector = MotionVector()
            motion_vector.frames = [skeleton.reference_frame]
            motion_vector.n_frames = 1
            self.scene.object_builder.create_object("animation_controller", skeleton_name, skeleton, motion_vector, skeleton.frame_time)
        else:
            print("Error: Could not load skeleton")

    def slot_export_skeleton(self):
        skeleton_name = str(self.skeletonListComboBox.currentText())
        filename = str(QFileDialog.getSaveFileName(self, 'Save To File', '.')[0])
        if filename != "":
            skeleton = self.mdb_session.load_skeleton(skeleton_name)
            skeleton_data = skeleton.to_json()
            save_json_file(skeleton_data, filename)

    def slot_replace_skeleton(self):
        skeleton_name = str(self.skeletonListComboBox.currentText())
        dialog = NewSkeletonDialog(skeleton_name)
        dialog.exec_()
        if dialog.success:
            name = dialog.name
            data = dialog.data
            meta_data = dialog.skeleton_model
            if data is not None:
                data = json.dumps(data)
            if meta_data is not None:
                meta_data = json.dumps(meta_data)
            if data is not None or meta_data is not None:
                self.mdb_session.replace_skeleton(name, data, meta_data)
            print("replaced skeleton", skeleton_name)

    def slot_edit_skeleton(self):
        graphics_widget = ApplicationManager.instance.graphics_widget
        skeleton_name = str(self.skeletonListComboBox.currentText())
        skeleton = self.mdb_session.load_skeleton(skeleton_name)
        skeleton_editor = SkeletonEditorDialog(skeleton_name, skeleton, graphics_widget, graphics_widget.parent)
        skeleton_editor.exec_()
        if skeleton_editor.success and skeleton_editor.skeleton_model is not None:
            skeleton_data = None
            if skeleton_editor.skeleton_data is not None:
                skeleton_data = json.dumps(skeleton_editor.skeleton_data)
            print("edit skeleton")
            meta_data = json.dumps(skeleton_editor.skeleton_model)  
            self.mdb_session.replace_skeleton(skeleton_name, skeleton_data, meta_data)
        else:
            print("ignore changes")
        
    def slot_print_debug_info(self):
        skeleton_name = str(self.skeletonListComboBox.currentText())
        collection = self.get_collection()
        if collection is None:
            return
        c_id, c_name, c_type = collection
        motion_list = self.mdb_session.get_motion_list(c_id, skeleton_name)
        if motion_list is None:
            return
        print("loaded", len(motion_list), "clips")
        frame_sum = 0
        for motion_id, name in motion_list:
            motion_data = self.mdb_session.get_motion_data(motion_id)
            if motion_data is None:
                print("Error: motion data is empty")
                return
            if "frames" in motion_data:
                n_frames = len(motion_data["frames"])
                frame_sum += n_frames
                print("motion", name, "has", n_frames)
        print("loaded", frame_sum,"frames")

    def disable_editing(self):
        self.newProjectButton.setEnabled(False)
        self.editProjectButton.setEnabled(False)
        self.deleteProjectButton.setEnabled(False)
        self.addCollectionButton.setEnabled(False)
        self.editCollectionButton.setEnabled(False)
        self.deleteCollectionButton.setEnabled(False)
        self.importMotionModelButton.setEnabled(False)
        self.newSkeletonButton.setEnabled(False)
        self.replaceSkeletonButton.setEnabled(False)
        self.deleteSkeletonButton.setEnabled(False)
        self.replaceSkeletonButton.setEnabled(False)
        self.editSkeletonButton.setEnabled(False)
        self.deleteFilesButton.setEnabled(False)
        self.copyMotionsButton.setEnabled(False)
        self.deleteAlignedMotionButton.setEnabled(False)
        self.setTimeFunctionButton.setEnabled(False)
        self.retargetMotionsButton.setEnabled(False)
        self.retargetAlignedMotionsButton.setEnabled(False)
        self.importCollectionButton.setEnabled(False)
        self.runDataTransformButton.setEnabled(False)
        self.newTagButton.setEnabled(False)
        self.renameTagButton.setEnabled(False)
        self.deleteTagButton.clicked.setEnabled(False)
        
        #self.createMotionModelButton.setEnabled(False)
        #self.createClusterTreeButton.setEnabled(False)
        #self.alignMotionsButton.setEnabled(False)
        #self.editMotionsButton.setEnabled(False)

    def slot_generate_morphablegraph_directory(self):
        filename = QFileDialog.getOpenFileName(self, 'Open File', '.')[0]
        filename = str(filename)
        if os.path.isfile(filename):
            graph_def = load_json_file(filename)
            if graph_def is None:
                return
            directory = QFileDialog.getExistingDirectory(self, "Select Directory")
            skeleton_name = str(self.skeletonListComboBox.currentText())
            print("directory", directory)
            if os.path.isdir(directory):
                self.generate_morphable_graph_directory(skeleton_name, graph_def, directory)

    def generate_morphable_graph_directory(self, skeleton_name, grapf_def, out_dir):
        skeleton_data = self.mdb_session.get_skeleton_data(skeleton_name)
        skeleton = SkeletonBuilder().load_from_custom_unity_format(skeleton_data)
        mgrd_skeleton = convert_to_mgrd_skeleton(skeleton)
        skeleton.skeleton_model = self.mdb_session.get_skeleton_meta_data(skeleton_name)
        save_json_file(skeleton.to_json(), out_dir + os.sep + "skeleton.json")
        out_dir = out_dir + os.sep + "elementary_action_models"
        if not os.path.isdir(out_dir):
            os.makedirs(out_dir)
        for a in grapf_def["actionDefinitions"].keys():
            action_def =  grapf_def["actionDefinitions"][a]
            action_dir = out_dir + os.sep + "elementary_action_"+a
            if not os.path.isdir(action_dir):
                os.makedirs(action_dir)
            meta_info = dict()
            meta_info["stats"] = dict()
            meta_info["start_states"] =action_def["start_states"]
            meta_info["end_states"] = action_def["end_states"]
            if "idle_states" in action_def:
                meta_info["idle_states"] = action_def["idle_states"]
            for mp_name in action_def["nodes"]:
                meta_info["stats"][mp_name] = dict()
                print("export motion primitive", mp_name)
                model_list = self.mdb_session.get_model_list(mp_name, skeleton_name, model_format="mpm")
                model_list += self.mdb_session.get_model_list(a+"_"+mp_name, skeleton_name, model_format="mpm")
                if len(model_list) <1:
                    continue
                model_id, name = model_list[-1]
                model_data = self.mdb_session.download_motion_model(model_id)
                with open(action_dir+ os.sep +  a+"_"+mp_name + "_quaternion_mm.json", "w+") as out_file:
                    out_file.write(json.dumps(model_data))
                cluster_tree_data = self.mdb_session.download_cluster_tree(model_id)
                if cluster_tree_data is not None:
                    with open(action_dir+ os.sep +  a+"_"+mp_name + "_quaternion_cluster_tree.json", "w+") as out_file:
                        out_file.write(json.dumps(cluster_tree_data))

                model = MotionPrimitiveModelWrapper()
                model._initialize_from_json(mgrd_skeleton, model_data)
                n_standard_transitions = 1
                n_samples = 5
                meta_info["stats"][mp_name]["average_step_length"] = get_avg_step_length(model, n_samples)
                meta_info["stats"][mp_name]["n_standard_transitions"] = n_standard_transitions

            save_json_file(meta_info, action_dir + os.sep + "meta_information.json")

    def slot_plot_experiment(self):
        runs = self.get_plot_data()
        if len(runs) > 0:
            plot_experiment(runs)

    def get_plot_data(self):
        from scipy.signal import savgol_filter
        def process_plot_data(log_data):
            timesteps, rewards, lengths = [], [], []
            for i in range(len(log_data)):
                rewards.append(log_data[i][0])
                lengths.append(log_data[i][1])
                timesteps.append(log_data[i][2])
            return timesteps, rewards, lengths
        apply_smoothing = self.smoothPlotCheckBox.checkState() == Qt.Checked
        items = self.experimentListWidget.selectedItems()
        runs = dict()
        for item in items:
            label = str(item.text())
            selected_id = int(item.data(Qt.UserRole))
            data = self.mdb_session.get_experiment_log(selected_id)
            print("plot", selected_id, label)
            t, r, l = process_plot_data(data["log_data"])
            entry= dict()
            entry["t"] = t
            entry["r"] = savgol_filter(r, 51, 3) if apply_smoothing else r
            entry["l"] = savgol_filter(l, 51, 3) if apply_smoothing else l
            runs[label] = entry
        return runs

    def slot_delete_experiment(self):
        dialog = ConfirmationDialog()
        dialog.exec_()
        if dialog.success:
            items = self.experimentListWidget.selectedItems()
            for item in items:
                selected_id = int(item.data(Qt.UserRole))
                self.mdb_session.remove_experiment(selected_id)
            self.update_lists()

    def slot_export_experiment(self):
        filename = QFileDialog.getSaveFileName(self, 'Save File', '.')[0]
        filename = str(filename)
        run_data = self.get_plot_data()
        save_json_file(run_data, filename)


    def slot_new_tag(self):
        return
    
    def slot_rename_tag(self):
        return
    
    def slot_delete_tag(self):
        return

    def slot_run_data_transforms(self):
        col = self.get_collection()
        if col is None:
            return
        c_id, c_name, c_type = col
        input_skeleton = str(self.skeletonListComboBox.currentText())
        dialog = DataTransformDialog(self.db_url, self.session, c_id, c_name, input_skeleton)
        dialog.exec_()
        if dialog.success and dialog.data_transform_id is not None:
            data_transform_id = dialog.data_transform_id
            exp_name = dialog.name
            parameters = dialog.parameters
            input_data = dialog.input_data
            output_skeleton = dialog.output_skeleton
            store_log = dialog.store_log
            run_data_transform(self.db_url, data_transform_id, exp_name, input_skeleton, c_id, input_data, output_skeleton, parameters, store_log, self.session)
        