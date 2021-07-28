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
import threading
import glob
import json
from PySide2.QtWidgets import  QDialog, QTableWidgetItem, QFileDialog
from PySide2.QtCore import Qt
from .layout.synchronize_skeletons_with_db_dialog_ui import Ui_Dialog
from tool.core.dialogs.enter_name_dialog import EnterNameDialog
from tool.core.dialogs.new_skeleton_dialog import NewSkeletonDialog
from tool.core.dialogs.utils import get_animation_controllers
from tool import constants
from tool.core.dialogs.utils import create_sections_from_annotation
from anim_utils.utilities.db_interface import get_skeletons_from_remote_db, get_skeleton_from_remote_db, get_skeleton_model_from_remote_db, replace_skeleton_in_remote_db, create_new_skeleton_in_db
from anim_utils.animation_data.skeleton_models import SKELETON_MODELS
from anim_utils.animation_data import BVHReader
from tool.plugins.database.session_manager import SessionManager
from vis_utils.io import load_json_file, save_json_file


class SynchronizeSkeletonsWithDBDialog(QDialog, Ui_Dialog):
    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        Ui_Dialog.setupUi(self, self)
        self.downloadButton.clicked.connect(self.slot_download)
        self.uploadButton.clicked.connect(self.slot_upload)

        self.selectAllDBButton.clicked.connect(self.slot_select_all_db_skeletons)
        self.clearDBSelectionButton.clicked.connect(self.slot_clear_db_skeleton_selection)

        self.selectAllLocalButton.clicked.connect(self.slot_select_all_local_skeletons)
        self.clearLocalSelectionButton.clicked.connect(self.slot_clear_local_skeleton_selection)

        self.db_url = constants.DB_URL
        self.local_skeleton_dir = constants.DATA_DIR + os.sep + "skeletons"
        self.session = SessionManager.session
        self.urlLineEdit.setText(self.db_url)
        self.success = False
        self.db_skeletons = []
        self.local_skeletons = []
        self.fill_db_table_with_skeletons()
        self.fill_local_table_with_skeletons()
        self.urlLineEdit.textChanged.connect(self.set_url)

    def set_url(self, text):
        print("set url", text)
        self.db_url = str(text)


    def fill_local_table_with_skeletons(self):
        self.skeletonLocalTableWidget.clear()
        self.local_skeletons = []
        
        if not os.path.isdir(self.local_skeleton_dir):
            return
        for filename in glob.glob(self.local_skeleton_dir + os.sep + "*.json"):
            name = filename.split(os.sep)[-1][:-5]
            insertRow = self.skeletonLocalTableWidget.rowCount()
            self.skeletonLocalTableWidget.insertRow(insertRow)
            indexItem = QTableWidgetItem("")
            indexItem.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
            indexItem.setCheckState(Qt.Unchecked)
            self.skeletonLocalTableWidget.setItem(insertRow, 0, indexItem)
            self.skeletonLocalTableWidget.setItem(insertRow, 1, QTableWidgetItem(str(name)))
            self.local_skeletons.append(name)

    def fill_db_table_with_skeletons(self):
        self.db_skeletons = []
        self.skeletonDBTableWidget.clear()
        skeleton_list = get_skeletons_from_remote_db(self.db_url)
        for idx, s, owner in skeleton_list:
            insertRow = self.skeletonDBTableWidget.rowCount()
            self.skeletonDBTableWidget.insertRow(insertRow)
            indexItem = QTableWidgetItem("")
            indexItem.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
            indexItem.setCheckState(Qt.Checked)
            self.skeletonDBTableWidget.setItem(insertRow, 0, indexItem)
            self.skeletonDBTableWidget.setItem(insertRow, 1, QTableWidgetItem(str(s)))
            self.db_skeletons.append(s)

    def get_selected_db_skeletons(self):
        skeleton_list = []
        for row_idx in range(self.skeletonDBTableWidget.rowCount()):
            index_cell = self.skeletonDBTableWidget.item(row_idx,0)
            if index_cell.checkState() == Qt.Checked:
                name_cell = self.skeletonDBTableWidget.item(row_idx,1)
                skeleton_name = str(name_cell.text())
                skeleton_list.append(skeleton_name)
        return skeleton_list

    def get_selected_local_skeletons(self):
        skeleton_list = []
        for row_idx in range(self.skeletonLocalTableWidget.rowCount()):
            index_cell = self.skeletonLocalTableWidget.item(row_idx,0)
            if index_cell.checkState() == Qt.Checked:
                name_cell = self.skeletonLocalTableWidget.item(row_idx,1)
                skeleton_name = str(name_cell.text())
                skeleton_list.append(skeleton_name)
        return skeleton_list


    def slot_download(self):
        skeleton_list = self.get_selected_db_skeletons()
        for skeleton_name in skeleton_list:
            skeleton = get_skeleton_from_remote_db(self.db_url, skeleton_name, self.session)
            skeleton_model = get_skeleton_model_from_remote_db(self.db_url, skeleton_name, self.session)
            if not os.path.isdir(self.local_skeleton_dir):
                os.makedirs(self.local_skeleton_dir)
            filename = self.local_skeleton_dir +os.sep + skeleton_name + ".json"
            data =dict()
            data["name"] = skeleton_name
            data["skeleton"] = skeleton
            data["model"] = skeleton_model
            save_json_file(data, filename)
        self.close()

    def slot_upload(self):
        skeleton_list = self.get_selected_local_skeletons()
        for skeleton_name in skeleton_list:
            filename = self.local_skeleton_dir +os.sep + skeleton_name + ".json"
            data = load_json_file(filename)
            skeleton_name = data["name"]
            skeleton = json.dumps(data["skeleton"])
            skeleton_model = json.dumps(data["model"])
            if skeleton_name in self.db_skeletons:
                replace_skeleton_in_remote_db(self.db_url, skeleton_name, skeleton, skeleton_model, self.session)
            else:
                create_new_skeleton_in_db(self.db_url, skeleton_name, skeleton, skeleton_model, self.session)
        self.close()    
        
    def slot_select_all_local_skeletons(self):
        for row_idx in range(self.skeletonLocalTableWidget.rowCount()):
            index_cell = self.skeletonLocalTableWidget.item(row_idx,0)
            index_cell.setCheckState(Qt.Checked)

    def slot_clear_local_skeleton_selection(self):
        for row_idx in range(self.skeletonLocalTableWidget.rowCount()):
            index_cell = self.skeletonLocalTableWidget.item(row_idx,0)
            index_cell.setCheckState(Qt.Unchecked)

    def slot_select_all_db_skeletons(self):
        for row_idx in range(self.skeletonDBTableWidget.rowCount()):
            index_cell = self.skeletonDBTableWidget.item(row_idx,0)
            index_cell.setCheckState(Qt.Checked)

    def slot_clear_db_skeleton_selection(self):
        for row_idx in range(self.skeletonDBTableWidget.rowCount()):
            index_cell = self.skeletonDBTableWidget.item(row_idx,0)
            index_cell.setCheckState(Qt.Unchecked)