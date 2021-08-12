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
import threading
from PySide2.QtWidgets import  QDialog, QTreeWidgetItem, QFileDialog
from PySide2.QtCore import Qt
from .layout.upload_motion_dialog_ui import Ui_Dialog
from tool.core.dialogs.enter_name_dialog import EnterNameDialog
from tool.core.dialogs.new_skeleton_dialog import NewSkeletonDialog
from tool.core.dialogs.utils import get_animation_controllers, create_section_dict_from_annotation
from anim_utils.utilities.db_interface import upload_motion_to_db, get_skeletons_from_remote_db, \
                        create_new_skeleton_in_db, get_collections_by_parent_id_from_remote_db
from vis_utils.io import load_json_file
from anim_utils.animation_data.skeleton_models import SKELETON_MODELS
from anim_utils.animation_data import BVHReader
from tool.plugins.database.session_manager import SessionManager
from tool.plugins.database import constants as db_constants


class UploadMotionDialog(QDialog, Ui_Dialog):
    def __init__(self, controller_list, parent=None):
        QDialog.__init__(self, parent)
        self.controller_list = controller_list
        Ui_Dialog.setupUi(self, self)
        self.selectButton.clicked.connect(self.slot_accept)
        self.cancelButton.clicked.connect(self.slot_reject)
        self.db_url = db_constants.DB_URL
        self.session = SessionManager.session
        self.urlLineEdit.setText(self.db_url)
        self.motion_table = "motion_clips"
        self.action_table = "motion_primitives"
        self.action_table = "actions"
        self.action = "grasp"
        self.success = False
        self.fill_combo_box_with_skeletons()
        t = threading.Thread(target=self.fill_tree_widget)
        t.start()
        self.urlLineEdit.textChanged.connect(self.set_url)

    def set_url(self, text):
        print("set url", text)
        self.db_url = str(text)

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
        for col in collection_list:
            colItem = QTreeWidgetItem(parent_item, [col[1], col[2]])
            colItem.setData(0, Qt.UserRole, col[0])
            self.fill_tree_widget((colItem, col[0]))

    def get_collection(self):
        colItem = self.collectionTreeWidget.currentItem()
        if colItem is None:
            return
        return int(colItem.data(0, Qt.UserRole)),  str(colItem.text(0)), str(colItem.text(1))

    def fill_combo_box_with_skeletons(self):
        self.skeletonModelComboBox.clear()
        skeleton_list = get_skeletons_from_remote_db(self.db_url)
        for idx, s in enumerate(skeleton_list):
            self.skeletonModelComboBox.addItem(s[1], idx)

    def slot_accept(self):
        skeleton_name = str(self.skeletonModelComboBox.currentText())
        col = self.get_collection()
        if col is not None:
            c_id, c_name, c_type = col
            self.success = True
            
            is_processed = bool(self.isProcessedCheckBox.isChecked())
            for c in self.controller_list:
                name = c.scene_object.name
                motion_data = c.get_json_data()
                print("upload motion clip ", name, "to ", c_id, c_name, c_type, skeleton_name)
                semantic_annotation = c._motion._semantic_annotation
                meta_info = dict()
                if len(semantic_annotation) >0:
                    meta_info["sections"] = create_section_dict_from_annotation(semantic_annotation)
                time_function = c._motion._time_function
                if time_function is not None and is_processed:
                    meta_info["time_function"] = time_function
                else:
                    is_processed = False

                if len(meta_info) > 0:
                    meta_info_str = json.dumps(meta_info)
                else:
                    meta_info_str = ""
                upload_motion_to_db(self.db_url, name, motion_data, c_id, skeleton_name, meta_info_str, is_processed, session=self.session)
            self.close()

    def slot_reject(self):
        self.close()

    def slot_new_skeleton(self):
        dialog = NewSkeletonDialog()
        dialog.exec_()
        if dialog.success:
            name = dialog.name
            bvh_str = dialog.bvh_str
            model = dialog.skeleton_model_str
            if model == "" and name in SKELETON_MODELS:
                model = json.dumps(SKELETON_MODELS[name])
            create_new_skeleton_in_db(self.db_url, name, bvh_str, model)
            self.fill_combo_box_with_skeletons()
            self._fill_motion_list_from_db()
