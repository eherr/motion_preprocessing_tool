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
import math
import json
import bson
import numpy as np
import threading
from functools import partial
import asyncio
from concurrent.futures import ProcessPoolExecutor
from multiprocessing import cpu_count
from PySide2 import QtWidgets, QtCore, QtUiTools
from PySide2.QtWidgets import QDialog, QListWidgetItem, QFileDialog, QAbstractItemView, QTreeWidgetItem
from PySide2.QtCore import Qt
from .enter_name_dialog import EnterNameDialog
from .confirmation_dialog import ConfirmationDialog
from .new_skeleton_dialog import NewSkeletonDialog
from .retarget_db_dialog import RetargetDBDialog
from .copy_db_dialog import CopyDBDialog
from .new_collection_dialog import NewCollectionDialog
from .edit_collection_dialog import EditCollectionDialog
from .motion_modelling_dialog import MotionModellingDialog
from .graph_definition_dialog import GraphDefinitionDialog
from .graph_table_view_dialog import GraphTableViewDialog
from .skeleton_editor_dialog import SkeletonEditorDialog
from .utils import get_animation_controllers, load_motion_data_from_dir
from anim_utils.utilities.db_interface import create_new_collection_in_remote_db, get_bvh_string, get_motion_list_from_remote_db, get_motion_by_id_from_remote_db, \
                                        delete_motion_by_id_from_remote_db,  upload_motion_to_db, replace_motion_in_db, get_time_function_by_id_from_remote_db, \
                                        create_new_skeleton_in_db, load_skeleton_from_db,delete_skeleton_from_remote_db, retarget_motion_in_db, get_annotation_by_id_from_remote_db, \
                                        get_skeleton_from_remote_db, get_skeletons_from_remote_db,get_collections_from_remote_db, delete_collection_from_remote_db, \
                                        get_collections_by_parent_id_from_remote_db,replace_collection_in_remote_db, get_collection_by_id, \
                                        start_cluster_job, replace_skeleton_in_remote_db, get_skeleton_model_from_remote_db
from motion_analysis import constants
from vis_utils.io import load_json_file, save_json_file
from anim_utils.animation_data.skeleton_models import SKELETON_MODELS
from anim_utils.animation_data import BVHReader, BVHWriter, MotionVector, SkeletonBuilder
from anim_utils.retargeting.analytical import Retargeting, generate_joint_map
from vis_utils.animation.animation_editor import AnimationEditorBase
from motion_analysis.gui.application_manager import ApplicationManager
from motion_analysis.gui.layout.motion_db_browser_dialog_ui import Ui_Dialog
from motion_analysis.session_manager import SessionManager
try:
    from morphablegraphs.utilities import convert_to_mgrd_skeleton
    from morphablegraphs.motion_model.motion_primitive_wrapper import MotionPrimitiveModelWrapper
    from morphablegraphs.utilities.db_interface import get_model_list_from_remote_db,upload_motion_model_to_remote_db, download_motion_model_from_remote_db, \
                                            delete_model_by_id_from_remote_db, upload_cluster_tree_to_remote_db, \
                                            download_cluster_tree_from_remote_db, create_cluster_tree_from_model, \
                                            load_cluster_tree_from_json, get_standard_config, convert_motion_to_static_motion_primitive, \
                                            create_motion_primitive_model, align_motion_data, align_motions_in_db, create_motion_model_in_db
except:
    pass


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




class MotionDBBrowserDialog(QDialog, Ui_Dialog):
    def __init__(self, scene, parent=None):
        QDialog.__init__(self, parent)
        self.setModal(0)
        Ui_Dialog.setupUi(self, self)
        self.scene = scene
        self.selectButton.clicked.connect(partial(MotionDBBrowserDialog.slot_load_motions, self, 0))
        self.deleteMotionButton.clicked.connect(partial(MotionDBBrowserDialog.slot_delete_motion, self,0))
        self.selectAlignedMotionButton.clicked.connect(partial(MotionDBBrowserDialog.slot_load_motions, self, 1))
        self.deleteAlignedMotionButton.clicked.connect(partial(MotionDBBrowserDialog.slot_delete_motion, self,1))
        self.addCollectionButton.clicked.connect(self.slot_new_collection)
        self.editCollectionButton.clicked.connect(self.slot_edit_collection)
        self.deleteCollectionButton.clicked.connect(self.slot_delete_collection)
        self.newSkeletonButton.clicked.connect(self.slot_new_skeleton)
        self.deleteSkeletonButton.clicked.connect(self.slot_delete_skeleton)
        self.loadSkeletonButton.clicked.connect(self.slot_load_skeleton)
        self.replaceSkeletonButton.clicked.connect(self.slot_replace_skeleton)
        self.exportSkeletonButton.clicked.connect(self.slot_export_skeleton)
        self.importCollectionButton.clicked.connect(self.slot_import_collection_from_folder)
        self.exportCollectionButton.clicked.connect(partial(MotionDBBrowserDialog.slot_export_collection_to_folder,self,0))
        self.exportAlignedCollectionButton.clicked.connect(partial(MotionDBBrowserDialog.slot_export_collection_to_folder,self,1))
        self.alignMotionsButton.clicked.connect(self.slot_align_motions)
        self.createMotionModelButton.clicked.connect(self.slot_create_motion_model)
        self.downloadMotionModelButton.clicked.connect(self.slot_download_motion_model)
        self.deleteMotionModelButton.clicked.connect(self.slot_delete_motion_model)
        self.exportMotionModelButton.clicked.connect(self.slot_export_motion_model)
        self.importMotionModelButton.clicked.connect(self.slot_import_motion_model)
        self.exportDatabaseButton.clicked.connect(self.slot_export_database_to_folder)
        self.createClusterTreeButton.clicked.connect(self.slot_create_cluster_tree)
        self.exportClusterTreeJSONButton.clicked.connect(self.slot_export_cluster_tree_json)
        self.exportClusterTreePCKButton.clicked.connect(self.slot_export_cluster_tree_pickle)
        self.retargetMotionsButton.clicked.connect(partial(MotionDBBrowserDialog.slot_retarget_motions_parallel,self, False))
        self.copyMotionsButton.clicked.connect(self.slot_copy_motions)
        self.setTimeFunctionButton.clicked.connect(self.slot_set_timefunction)
        self.editMotionsButton.clicked.connect(self.slot_edit_motions)
        self.generateMGFromFIleButton.clicked.connect(self.slot_generate_graph_definition)
        self.retargetAlignedMotionsButton.clicked.connect(partial(MotionDBBrowserDialog.slot_retarget_motions_parallel,self, True))
        self.editSkeletonButton.clicked.connect(self.slot_edit_skeleton)
        self.debugInfoButton.clicked.connect(self.slot_print_debug_info)
        self.rootItem = None
        self.db_url = constants.DB_URL
        self.session = SessionManager.session
        print("set session", self.session)
        if self.session is not None and "user" in self.session:
            self.statusLabel.setText("Status: Authenticated as "+self.session["user"])
        else:
            self.disable_editing()
            self.statusLabel.setText("Status: Not authenticated")

            
        self.urlLineEdit.setText(self.db_url)
        self.fill_combo_box_with_skeletons()
        self.update_lists()
        self.processedMotionListWidget.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.alignedMotionListWidget.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.skeletonListComboBox.currentIndexChanged.connect(self.update_lists)
        self.collectionTreeWidget.itemClicked.connect(self.update_lists)
        self.urlLineEdit.textChanged.connect(self.set_url)
        self.tabWidget.currentChanged.connect(self.toggle_motion_primitive_list)
        t = threading.Thread(target=self.fill_tree_widget)
        t.start()
        self.n_samples = 10000
        self.n_subdivisions_per_level = 4
        self.k8s_resources = constants.K8S_RESOURCES
        self.k8s_imagename = constants.K8S_IMAGE_NAME
        self.mg_repo_url =  constants.MG_REPO_URL
        self.mg_exec_dir =  constants.MG_EXEC_DIR
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

    def toggle_motion_primitive_list(self):
        tab_name = self.tabWidget.currentWidget().objectName()
        print("tab_name", tab_name)

    def update_lists(self):
        self._fill_motion_list_from_db()
        self._fill_model_list_from_db()
        self._fill_aligned_motion_list_from_db()

    def fill_tree_widget(self, parent=None):
        if parent is None:
            self.collectionTreeWidget.clear()
            self.rootItem = QTreeWidgetItem(self.collectionTreeWidget, ["root", "root"])
            self.rootItem.setExpanded(True)
            # root collection has id 0
            parent_id = 0
            parent_item = self.rootItem
            self.rootItem.setData(0, Qt.UserRole, parent_id)
        else:
            parent_id = parent[1]
            parent_item = parent[0]

        collection_list = get_collections_by_parent_id_from_remote_db(self.db_url, parent_id)
        if collection_list is not None:
            for col in collection_list:
                colItem = QTreeWidgetItem(parent_item, [col[1], col[2]])
                colItem.setData(0, Qt.UserRole, col[0])
                self.fill_tree_widget((colItem, col[0]))
            

    def fill_combo_box_with_skeletons(self):
        self.skeletonListComboBox.clear()
        skeleton_list = get_skeletons_from_remote_db(self.db_url)
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

    def _fill_motion_list_from_db(self, idx=None):
        self.processedMotionListWidget.clear()
        col = self.get_collection()
        if col is None:
            return
        c_id, c_name, c_type = col
        print("update lists", c_id)
        skeleton = str(self.skeletonListComboBox.currentText())
        motion_list = get_motion_list_from_remote_db(self.db_url, c_id, skeleton, is_processed=False, session=self.session)
        if motion_list is None:
            return
        print("loaded", len(motion_list), "clips")
        for node_id, name in motion_list:
            item = QListWidgetItem()
            item.setText(name)
            item.setData(Qt.UserRole, node_id)
            self.processedMotionListWidget.addItem(item)

    def  _fill_aligned_motion_list_from_db(self, idx=None):
        self.alignedMotionListWidget.clear()
        col = self.get_collection()
        if col is None:
            return
        c_id, c_name, c_type = col
        skeleton = str(self.skeletonListComboBox.currentText())
        motion_list = get_motion_list_from_remote_db(self.db_url, c_id, skeleton, is_processed=True)
        if motion_list is None:
            return
        print("loaded", len(motion_list), "aligned clips")
        for node_id, name in motion_list:
            item = QListWidgetItem()
            item.setText(name)
            item.setData(Qt.UserRole, node_id)
            print("loaded", name, node_id)
            self.alignedMotionListWidget.addItem(item)
        
    def _fill_model_list_from_db(self, idx=None):
        self.modelListWidget.clear()
        col = self.get_collection()
        if col is None:
            return
        c_id, c_name, c_type = col
        skeleton = str(self.skeletonListComboBox.currentText())
        model_list = get_model_list_from_remote_db(self.db_url, c_id, skeleton)
        print("model list", model_list)
        if model_list is None:
            return
        for node_id, name in model_list:
            item = QListWidgetItem()
            item.setText(name)
            item.setData(Qt.UserRole, node_id)
            self.modelListWidget.addItem(item)

    def slot_load_motions(self, is_aligned=0):
        if is_aligned==0:
            items = self.processedMotionListWidget.selectedItems()
        else:
            items = self.alignedMotionListWidget.selectedItems()
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
            self.load_motion_from_db(motion_id, motion_name, c_id, is_aligned)

            count+=1

    def load_motion_from_db(self, motion_id, motion_name, collection, is_processed=False):
        #print("selected item", item.text(),self.selected_id)
        motion_data = get_motion_by_id_from_remote_db(self.db_url, motion_id, is_processed)
        if motion_data is None:
            print("Error: motion data is empty")
            return
        #skeleton_name = motion_data["skeletonModel"]
        skeleton_name = str(self.skeletonListComboBox.currentText())
        print("load skeleton", skeleton_name)
        skeleton_data = get_skeleton_from_remote_db(self.db_url, skeleton_name)
        if skeleton_data is None:
            print("Error: skeleton data is empty")
            return
        meta_info_str = get_annotation_by_id_from_remote_db(self.db_url, motion_id, is_processed)
        skeleton_model = None
        if skeleton_name in SKELETON_MODELS:
            skeleton_model = SKELETON_MODELS[skeleton_name]
        visible = True
        color = [0,0,1]
        self.scene.object_builder.create_object("motion_from_json", skeleton_data, motion_data, motion_name, collection, motion_id, meta_info_str, skeleton_model, is_processed, visible=visible)

    def slot_delete_motion(self, is_processed=0):
        dialog = ConfirmationDialog()
        dialog.exec_()
        if dialog.success:
            if is_processed:
                items = self.alignedMotionListWidget.selectedItems()
            else:
                items = self.processedMotionListWidget.selectedItems()
            for item in items:
                selected_id = int(item.data(Qt.UserRole))
                print("delete", selected_id, is_processed)
                delete_motion_by_id_from_remote_db(self.db_url, selected_id, is_processed, session=self.session)
            self._fill_motion_list_from_db()

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
            create_new_collection_in_remote_db(self.db_url, name, col_type, c_id, owner, self.session)
            self.fill_tree_widget()
            self._fill_motion_list_from_db()
    
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
            replace_collection_in_remote_db(self.db_url, c_id, name, col_type, p_id, owner, self.session)
            self.fill_tree_widget()
            self._fill_motion_list_from_db()


    def slot_delete_collection(self):
        dialog = ConfirmationDialog()
        dialog.exec_()
        if dialog.success:
            collection = self.get_collection()
            if collection is not None:
                delete_collection_from_remote_db(self.db_url, collection[0], self.session)
                self.fill_tree_widget()
                self._fill_motion_list_from_db()

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
                create_new_skeleton_in_db(self.db_url, name, data, meta_data, self.session)
                self.fill_combo_box_with_skeletons()
                self._fill_motion_list_from_db()
            else:
                print("data is None")
        
    def slot_delete_skeleton(self):
        dialog = ConfirmationDialog()
        dialog.exec_()
        if dialog.success:
            skeleton_name = str(self.skeletonListComboBox.currentText())
            delete_skeleton_from_remote_db(self.db_url, skeleton_name, self.session)
            self.fill_combo_box_with_skeletons()
            self._fill_motion_list_from_db()


    def slot_delete_motion_model(self):
        dialog = ConfirmationDialog()
        dialog.exec_()
        if dialog.success:
            items = self.modelListWidget.selectedItems()
            for item in items:
                selected_id = int(item.data(Qt.UserRole))
                delete_model_by_id_from_remote_db(self.db_url, selected_id, self.session)
            self.update_lists()

    def slot_export_collection_to_folder(self, is_aligned=False):
        directory = QFileDialog.getExistingDirectory(self, "Select Directory")
        print("directory", directory)
        if os.path.isdir(directory):
            col = self.get_collection()
            if col is None:
                return
            c_id, c_name, c_type = col
            skeleton_name = str(self.skeletonListComboBox.currentText())
            self.export_collection_clips_to_folder(c_id, skeleton_name, directory, is_aligned)
            #self.export_processed_motion_data(skeleton_name, directory, c_id)

    def export_collection_clips_to_folder(self, c_id, skeleton_name, directory, is_aligned):
        print("export", is_aligned)
        #is_aligned = 1
        skeleton = load_skeleton_from_db(self.db_url, skeleton_name)
        motion_list = get_motion_list_from_remote_db(self.db_url, c_id, skeleton_name, is_aligned, self.session)
        if motion_list is None:
            print("could not find motions")
            return
        n_motions = len(motion_list)
        if n_motions < 1:
            print("no motions", c_id)
            return
        if not os.path.isdir(directory):
            os.makedirs(directory)
        count = 1
        #print(skeleton_name, len(motion_list), is_aligned, directory)
        for motion_id, name in motion_list:
            print("download motion", str(count)+"/"+str(n_motions), name, is_aligned)
            self.export_motion_clip(skeleton, motion_id, name, directory)
            count+=1

    def export_motion_clip(self, skeleton, motion_id, name, directory, export_bvh=False, export_json=False, export_bson=True):
        print("export clip")
        motion_dict = get_motion_by_id_from_remote_db(self.db_url, motion_id, is_processed=False, session=self.session)
        if motion_dict is None:
            return
        print("write to file")
        if export_bvh:
            motion_vector = MotionVector()
            motion_vector.from_custom_unity_format(motion_dict)
            bvh_str = get_bvh_string(skeleton, motion_vector.frames)
            filename = directory+os.sep+name
            if not name.endswith(".bvh"):
                filename += ".bvh"
            with open(filename, "wt") as out_file:
                out_file.write(bvh_str)
        filename = directory+os.sep+name
        annotation_str = get_annotation_by_id_from_remote_db(self.db_url, motion_id, is_processed=False, session=self.session)
        if annotation_str != "":
            annotation_filename = filename + "_meta_info.json"
            with open(annotation_filename, "wt") as out_file:
                out_file.write(annotation_str)
        else:
            print("no meta info")
        time_function_str = get_time_function_by_id_from_remote_db(self.db_url, motion_id, self.session)
        if time_function_str != "":
            time_function_filename = filename + "_time_function.json"
            with open(time_function_filename, "wt") as out_file:
                out_file.write(time_function_str)
        else:
            print("no time function")

    def slot_import_collection_from_folder(self):
        directory = QFileDialog.getExistingDirectory(self, "Select Directory")
        print("directory", directory)
        if os.path.isdir(directory):
            col = self.get_collection()
            if col is None:
                return
            c_id, c_name, c_type = col
            motion_data_list = load_motion_data_from_dir(directory)
            count = 1
            n_motions = len(motion_data_list)
            for name, data in motion_data_list.items():
                print("upload motion", str(count)+"/"+str(n_motions), name)
                is_processed = False
                motion_data = data["bvh_str"]
                upload_motion_to_db(self.db_url, name, motion_data, c_id, data["skeleton_model"], data["meta_info"], is_processed, self.session)
                count+=1
            self._fill_motion_list_from_db()

    def delete_motion(self, motion_id_list):
        for motion_id in motion_id_list:
            delete_motion_by_id_from_remote_db(self.db_url, motion_id, self.session)
        self._fill_motion_list_from_db()

    def slot_align_motions(self):
        """ run alignment
            upload aligned data to db
        """
        col = self.get_collection()
        if col is None:
            return
        c_id, c_name, c_type = col
        skeleton_name = str(self.skeletonListComboBox.currentText())
        # TODO start process with detached window
        if not self.useComputeClusterCheckBox.isChecked():
            align_motions_in_db(self.db_url, skeleton_name, c_id, session=self.session)
        else:
            job_name = "alignment" +str(col[0])
            parameter_str = self.db_url+ " " + skeleton_name + " "+ str(c_id)
            if self.session is not None:
                parameter_str += " --user "+ self.session["user"] + " --token " + self.session["token"]
            job_desc = dict()
            job_desc["command"] = "pip install -r requirements.txt; python run_alignment_in_db.py " + parameter_str
            job_desc["exec_dir"] = self.mg_exec_dir
            job_desc["repo_url"] = self.mg_repo_url
            job_desc["aws"]  = None
            start_cluster_job(self.db_url, self.k8s_imagename, job_name, job_desc, self.k8s_resources, self.session)
            print("run on alignment on cluster")
    
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
        skeleton = load_skeleton_from_db(self.db_url, skeleton_name)
        dialog = MotionModellingDialog(skeleton, c_name, spline_basis_factor)
        dialog.exec_()
        if not dialog.success:
            return

        name = dialog.name
        spline_basis_factor = dialog.spline_basis_factor
        animated_joints = dialog.animated_joints
        # TODO start process with detached window
        if not self.useComputeClusterCheckBox.isChecked():
            create_motion_model_in_db(self.db_url, skeleton_name, c_id, name, spline_basis_factor, animated_joints, self.session)
        else:
            
            parameter_str = self.db_url+ " " + skeleton_name + " "+ str(c_id) +" " +name + " " + str(spline_basis_factor)
            if animated_joints:
                parameter_str += " --joint_filter "
                for joint_name in animated_joints:
                    parameter_str += " " + joint_name
            parameter_str = self.db_url+ " " + skeleton_name + " "+ str(c_id)
            if self.session is not None:
                parameter_str += " --user "+ self.session["user"] + " --token " + self.session["token"]
            job_name = "statistical" +str(col[0])
            job_desc = dict()
            job_desc["command"] = "pip install -r requirements.txt; python run_construction_in_db.py " + parameter_str
            job_desc["exec_dir"] = self.mg_exec_dir
            job_desc["repo_url"] = self.mg_repo_url
            job_desc["aws"]  = None
            start_cluster_job(self.db_url, self.k8s_imagename, job_name, job_desc, self.k8s_resources, self.session)
            print("run on modelling on cluster")

    def slot_import_motion_model(self):
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
            upload_motion_model_to_remote_db(self.db_url, name, c_id, skeleton, model_data, config, self.session)
    
    def slot_download_motion_model(self):
        item = self.modelListWidget.currentItem()
        model_id = int(item.data(Qt.UserRole))
        model_name = str(item.text())
        model_data_str = download_motion_model_from_remote_db(self.db_url, model_id, self.session)
        cluster_tree_data_str = download_cluster_tree_from_remote_db(self.db_url, model_id, self.session)
        if model_data_str is not None:
            self.scene.object_builder.create_object("motion_primitive", model_name, model_data_str, cluster_tree_data_str)

    def slot_export_motion_model(self):
        item = self.modelListWidget.currentItem()
        model_id = int(item.data(Qt.UserRole))
        model_name = str(item.text())
        model_data_str = download_motion_model_from_remote_db(self.db_url, model_id, self.session)
        if model_data_str is not None:
            filename = QFileDialog.getSaveFileName(self, 'Save To File', '.')[0]
            with open(filename, "w") as out_file:
                out_file.write(model_data_str)

    def slot_create_cluster_tree(self):
        item = self.modelListWidget.currentItem()
        model_id = int(item.data(Qt.UserRole))
        model_data_str = download_motion_model_from_remote_db(self.db_url, model_id, self.session)
        model = json.loads(model_data_str)

        tree = create_cluster_tree_from_model(model, self.n_samples, self.n_subdivisions_per_level)
        tree_data = dict()
        tree_data["data"] = tree.data.tolist()
        tree_data["features"] = tree._features.tolist()
        tree_data["options"] = tree._options
        tree_data["root"] = tree.node_to_json()
        tree_data = json.dumps(tree_data)
        upload_cluster_tree_to_remote_db(self.db_url, model_id, tree_data, self.session)

    def slot_export_cluster_tree_json(self):
        item = self.modelListWidget.currentItem()
        model_id = int(item.data(Qt.UserRole))
        model_name = str(item.text())
        cluster_tree_data_str = download_cluster_tree_from_remote_db(self.db_url, model_id, self.session)
        if cluster_tree_data_str is not None:
            filename = QFileDialog.getSaveFileName(self, 'Save To File', '.')[0]
            with open(filename, "w") as out_file:
                out_file.write(cluster_tree_data_str)
    
    def slot_export_cluster_tree_pickle(self):
        item = self.modelListWidget.currentItem()
        model_id = int(item.data(Qt.UserRole))
        model_name = str(item.text())
        cluster_tree_data_str = download_cluster_tree_from_remote_db(self.db_url, model_id, self.session)
        if cluster_tree_data_str is not None:
            cluster_tree_data = json.loads(cluster_tree_data_str)
            cluster_tree = load_cluster_tree_from_json(cluster_tree_data)
            filename = QFileDialog.getSaveFileName(self, 'Save To File', '.')[0]
            cluster_tree.save_to_file_pickle(filename)
 
    def slot_export_database_to_folder(self):
        directory = QFileDialog.getExistingDirectory(self, "Select Directory")
        if os.path.isdir(directory):
            for i in range(self.skeletonListComboBox.count()):
                skeleton_name = str(self.skeletonListComboBox.itemText(i))
                skeleton_dir = directory+os.sep+skeleton_name
                if not os.path.isdir(skeleton_dir):
                    os.makedirs(skeleton_dir)
                skeleton_data = get_skeleton_from_remote_db(self.db_url, skeleton_name, self.session)
                save_json_file(skeleton_data, skeleton_dir + os.sep + skeleton_name+"_skeleton.json")
                
                #self.export_raw_motion_data(skeleton_name, skeleton_dir + os.sep + "raw")
                self.export_processed_motion_data(skeleton_name, skeleton_dir + os.sep + "processed")
                #self.export_aligned_motion_data(skeleton_name, skeleton_dir + os.sep + "aligned")
                self.export_motion_models(skeleton_name, skeleton_dir + os.sep + "models")
                break
                  
            
    def export_motion_models(self, skeleton_name, out_dir, parent=0):
        for col in get_collections_by_parent_id_from_remote_db(self.db_url, parent, self.session):
            col_id, col_name, col_type, owner = col
            action_dir = out_dir+os.sep+col_name
            self.export_motion_primitive_models(col_id, skeleton_name, action_dir)
            self.export_motion_models(skeleton_name, action_dir, col_id)

    def export_aligned_motion_data(self, skeleton_name, out_dir, parent=0):
        for col in get_collections_by_parent_id_from_remote_db(self.db_url, parent):
            col_id, col_name, col_type, owner = col
            action_dir = out_dir+os.sep+col_name
            if self.model_filter is None or col_name in self.model_filter:
                self.export_collection_clips_to_folder(col_id, skeleton_name, action_dir, is_aligned=1)
            self.export_aligned_motion_data(skeleton_name, action_dir, col_id)

    def export_processed_motion_data(self, skeleton_name, out_dir, parent=0):
        for col in get_collections_by_parent_id_from_remote_db(self.db_url, parent):
            print(col)
            col_id, col_name, col_type, owner = col
            action_dir = out_dir+os.sep+col_name
            if self.model_filter is None or col_name in self.model_filter:
                self.export_collection_clips_to_folder(col_id, skeleton_name, action_dir, is_aligned=0)
            self.export_processed_motion_data(skeleton_name, action_dir, col_id)

    def export_motion_primitive_models(self, mp_name, skeleton_name, out_dir):
        model_list = get_model_list_from_remote_db(self.db_url, mp_name, skeleton_name, self.session)
        if len(model_list) > 0 and not os.path.isdir(out_dir):
            os.makedirs(out_dir)
        for model_id, name in model_list:
            model_data_str = download_motion_model_from_remote_db(self.db_url, model_id, self.session)
            with open(out_dir+ os.sep + name + "_quaternion_mm.json", "w+") as out_file:
                out_file.write(model_data_str)
            cluster_tree_data_str = download_cluster_tree_from_remote_db(self.db_url, model_id, self.session)
            if cluster_tree_data_str is not None and len(cluster_tree_data_str) > 0:
                with open(out_dir+ os.sep + name + "_cluster_tree.json", "w+") as out_file:
                    out_file.write(cluster_tree_data_str)

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
                items = self.processedMotionListWidget.selectedItems()
            else:
                items = self.alignedMotionListWidget.selectedItems()
            n_motions = len(items)
            motions = []
            for item in items:
                motion_id = int(item.data(Qt.UserRole))
                motion_name = str(item.text())
                motions.append((motion_id, motion_name))

            src_skeleton = load_skeleton_from_db(self.db_url, src_skeleton_name, self.session)
            target_skeleton = load_skeleton_from_db(self.db_url, target_skeleton_name, self.session)
            
            joint_map = generate_joint_map(src_skeleton.skeleton_model, target_skeleton.skeleton_model)
            retargeting = Retargeting(src_skeleton, target_skeleton, joint_map, src_scale, additional_rotation_map=None, place_on_ground=place_on_ground)
       
            count = 1
            for motion_id, motion_name in motions:
                print("retarget motion", str(count)+"/"+str(n_motions), motion_name)
                retarget_motion_in_db(self.db_url, retargeting, motion_id, motion_name, collection, target_skeleton_name, is_aligned, session=self.session)
                count+=1

    def slot_retarget_motions_parallel(self, is_aligned=0):
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
            if self.useComputeClusterCheckBox.isChecked():
                job_name = "retargeting" +str(col[0])
                imagename = "python:3.5.3"
                job_desc = dict()
                parameter_str = self.db_url+ " " + src_skeleton_name + " "+ target_skeleton_name + " "+ str(col[0])+ " "+str(is_aligned) +" "+ str(src_scale) +" "+ str(place_on_ground) 
                
                if self.session is not None:
                    parameter_str += " --user "+ self.session["user"] + " --token " + self.session["token"]
                job_desc["command"] = "pip install -r requirements.txt; python run_retargeting_in_db.py " + parameter_str
                job_desc["exec_dir"] = self.mg_exec_dir
                job_desc["repo_url"] = self.mg_repo_url
                job_desc["aws"]  = None
                start_cluster_job(self.db_url, self.k8s_imagename, job_name, job_desc, self.k8s_resources, self.session)
                print("run on retargeting on cluster")
            
            else:
                if is_aligned==0:
                    items = self.processedMotionListWidget.selectedItems()
                else:
                    items = self.alignedMotionListWidget.selectedItems()
                n_motions = len(items)
                
                motions = []
                for item in items:
                    motion_id = int(item.data(Qt.UserRole))
                    motion_name = str(item.text())
                    motions.append((motion_id, motion_name))
                src_skeleton = load_skeleton_from_db(self.db_url, src_skeleton_name, self.session)
                target_skeleton = load_skeleton_from_db(self.db_url, target_skeleton_name, self.session)
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
            skeleton = load_skeleton_from_db(self.db_url, skeleton_name, self.session)
            items = self.processedMotionListWidget.selectedItems()
            n_motions = len(items)
            count = 1
            for item in items:
                motion_id = int(item.data(Qt.UserRole))
                motion_name = str(item.text())
                motion_name+="_copy"
                print("copy motion", str(count)+"/"+str(n_motions), motion_name)
                self.copy_motion_in_db(skeleton, motion_id, motion_name, collection, skeleton_name)
                count+=1
   
    def copy_motion_in_db(self, skeleton, motion_id, motion_name, collection, skeleton_model_name):
        motion_data = get_motion_by_id_from_remote_db(self.db_url, motion_id, is_processed=False, session=self.session)
        if motion_data is None:
            print("Error: motion data is empty")
            return
        #motion_vector = MotionVector()
        #motion_vector.from_custom_unity_format(motion_data)
        #bvh_str = get_bvh_string(skeleton, motion_vector.frames)
        #motion_vector.skeleton = skeleton
        meta_info_str = get_annotation_by_id_from_remote_db(self.db_url, motion_id)
        upload_motion_to_db(self.db_url, motion_name, motion_data, collection, skeleton_model_name, meta_info_str, session=self.session)

    def slot_edit_motions(self):
        filename = QFileDialog.getOpenFileName(self, 'Open File', '.')[0]
        filename = str(filename)
        if os.path.isfile(filename):
            instructions = load_json_file(filename)
            #action = str(self.actionListComboBox.currentText())
            col = self.get_collection()
            if col is None:
                return
            c_id, c_name, c_type = col
            skeleton_name = str(self.skeletonListComboBox.currentText())
            items = self.processedMotionListWidget.selectedItems()
            n_motions = len(items)
            skeleton = load_skeleton_from_db(self.db_url, skeleton_name, self.session)
            count = 1
            for item in items:
                motion_id = int(item.data(Qt.UserRole))
                motion_name = str(item.text())
                print("edit motion", str(count)+"/"+str(n_motions), motion_name)
                self.edit_motion_in_db(skeleton, motion_id, motion_name, c_id, skeleton_name, instructions)
                count += 1

    def edit_motion_in_db(self, skeleton, motion_id, motion_name, collection, skeleton_name, instructions): 
        motion_data = get_motion_by_id_from_remote_db(self.db_url, motion_id, is_processed=False, session=self.session)
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
        replace_motion_in_db(self.db_url, motion_id, motion_name, motion_data, collection, skeleton_name, meta_data, is_processed=False, session=self.session)

    def slot_set_timefunction(self):
        filename = QFileDialog.getOpenFileName(self, 'Open File', '.')[0]
        filename = str(filename)
        if os.path.isfile(filename):
            temporal_data = load_json_file(filename)
            #action = str(self.actionListComboBox.currentText())
            #motion_primitive = str(self.motionPrimitiveListComboBox.currentText())
            items = self.processedMotionListWidget.selectedItems()
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
                    meta_data = get_annotation_by_id_from_remote_db(self.db_url, motion_id, is_processed=False, session=self.session)
                    if meta_data is None:
                        meta_data = dict()
                    meta_data["time_function"] = time_function
                    meta_data =  bson.dumps(meta_data)
                    replace_motion_in_db(self.db_url, motion_id, motion_name, data, collection, 
                                        skeleton_name, meta_data, is_processed=True, session=self.session)
                count += 1

    def slot_generate_graph_definition(self):
        dialog = GraphTableViewDialog(self.scene, self.db_url)
        dialog.exec_()
        if dialog.success:
            return
        return

        filename = QFileDialog.getOpenFileName(self, 'Open File', '.')[0]
        filename = str(filename)
        if os.path.isfile(filename):
            graph_data = load_json_file(filename)
        else:
            graph_data = None
        skeleton = str(self.skeletonListComboBox.currentText())
        print(graph_data)
        dialog = GraphDefinitionDialog(skeleton, self.db_url, graph_data=graph_data)
        dialog.exec_()
        if dialog.success:
            filename = QFileDialog.getSaveFileName(self, 'Save To File', '.')[0]
            filename = str(filename)
            save_json_file(dialog.data, filename)
        
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
        skeleton_data = get_skeleton_from_remote_db(self.db_url, skeleton_name, self.session)
        skeleton = SkeletonBuilder().load_from_custom_unity_format(skeleton_data)
        mgrd_skeleton = convert_to_mgrd_skeleton(skeleton)
        skeleton.skeleton_model = SKELETON_MODELS[skeleton_name] # TODO read from database
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
                model_list = get_model_list_from_remote_db(self.db_url, mp_name, skeleton_name, self.session)
                model_list += get_model_list_from_remote_db(self.db_url, a+"_"+mp_name, skeleton_name, self.session)
                if len(model_list) <1:
                    continue
                model_id, name = model_list[-1]
                model_data_str = download_motion_model_from_remote_db(self.db_url, model_id, self.session)
                with open(action_dir+ os.sep +  a+"_"+mp_name + "_quaternion_mm.json", "w+") as out_file:
                    out_file.write(model_data_str)
                cluster_tree_data_str = download_cluster_tree_from_remote_db(self.db_url, model_id, self.session)
                if cluster_tree_data_str is not None and len(cluster_tree_data_str) > 0:
                    with open(action_dir+ os.sep +  a+"_"+mp_name + "_quaternion_cluster_tree.json", "w+") as out_file:
                        out_file.write(cluster_tree_data_str)

                model_data = json.loads(model_data_str)
                model = MotionPrimitiveModelWrapper()
                model._initialize_from_json(mgrd_skeleton, model_data)
                n_standard_transitions = 1
                n_samples = 5
                meta_info["stats"][mp_name]["average_step_length"] = get_avg_step_length(model, n_samples)
                meta_info["stats"][mp_name]["n_standard_transitions"] = n_standard_transitions

            save_json_file(meta_info, action_dir + os.sep + "meta_information.json")

    def slot_load_skeleton(self):
        skeleton_name = str(self.skeletonListComboBox.currentText())
        skeleton = load_skeleton_from_db(self.db_url, skeleton_name, self.session)
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
            skeleton = load_skeleton_from_db(self.db_url, skeleton_name, self.session)
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
                replace_skeleton_in_remote_db(self.db_url, name, data, meta_data, self.session)
            print("replaced skeleton", skeleton_name)

    def slot_edit_skeleton(self):
        graphics_widget = ApplicationManager.instance.graphics_widget
        skeleton_name = str(self.skeletonListComboBox.currentText())
        skeleton = load_skeleton_from_db(self.db_url, skeleton_name, self.session)
        skeleton_editor = SkeletonEditorDialog(skeleton_name, skeleton, graphics_widget, graphics_widget.parent)
        skeleton_editor.exec_()
        if skeleton_editor.success and skeleton_editor.skeleton_model is not None:
            skeleton_data = None
            if skeleton_editor.skeleton_data is not None:
                skeleton_data = json.dumps(skeleton_editor.skeleton_data)
            print("edit skeleton")
            meta_data = json.dumps(skeleton_editor.skeleton_model)  
            replace_skeleton_in_remote_db(self.db_url, skeleton_name, skeleton_data, meta_data, self.session)
        else:
            print("ignore changes")
        
    def slot_print_debug_info(self):
        skeleton_name = str(self.skeletonListComboBox.currentText())
        collection = self.get_collection()
        if collection is None:
            return
        c_id, c_name, c_type = collection
        motion_list = get_motion_list_from_remote_db(self.db_url, c_id, skeleton_name, is_processed=False, session=self.session)
        if motion_list is None:
            return
        print("loaded", len(motion_list), "clips")
        frame_sum = 0
        for motion_id, name in motion_list:
            motion_data = get_motion_by_id_from_remote_db(self.db_url, motion_id, self.session)
            if motion_data is None:
                print("Error: motion data is empty")
                return
            if "frames" in motion_data:
                n_frames = len(motion_data["frames"])
                frame_sum += n_frames
                print("motion", name, "has", n_frames)
        print("loaded", frame_sum,"frames")

    def disable_editing(self):
        self.addCollectionButton.setEnabled(False)
        self.editCollectionButton.setEnabled(False)
        self.deleteCollectionButton.setEnabled(False)
        self.createMotionModelButton.setEnabled(False)
        self.deleteMotionModelButton.setEnabled(False)
        self.createClusterTreeButton.setEnabled(False)
        self.importMotionModelButton.setEnabled(False)
        self.newSkeletonButton.setEnabled(False)
        self.replaceSkeletonButton.setEnabled(False)
        self.deleteSkeletonButton.setEnabled(False)
        self.replaceSkeletonButton.setEnabled(False)
        self.editSkeletonButton.setEnabled(False)
        self.deleteMotionButton.setEnabled(False)
        self.copyMotionsButton.setEnabled(False)
        self.deleteAlignedMotionButton.setEnabled(False)
        self.setTimeFunctionButton.setEnabled(False)
        self.retargetMotionsButton.setEnabled(False)
        self.alignMotionsButton.setEnabled(False)
        self.retargetAlignedMotionsButton.setEnabled(False)
        self.editMotionsButton.setEnabled(False)
        self.importCollectionButton.setEnabled(False)

def main():
    get_collections_by_parent_id_from_remote_db("motion.dfki.de/8888", 0)

if __name__ == "__main__":
    main()
