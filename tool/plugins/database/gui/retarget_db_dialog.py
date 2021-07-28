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
import threading
from PySide2.QtWidgets import QDialog, QTreeWidgetItem, QFileDialog
from PySide2.QtCore import Qt
from tool.core.layout.retarget_db_dialog_ui import Ui_Dialog
from vis_utils.io import load_json_file
from anim_utils.animation_data.skeleton_models import SKELETON_MODELS
from tool.constants import DB_URL
from anim_utils.utilities.db_interface import get_collections_by_parent_id_from_remote_db, get_skeletons_from_remote_db

class RetargetDBDialog(QDialog, Ui_Dialog):
    def __init__(self, db_url, parent=None):
        QDialog.__init__(self, parent)
        Ui_Dialog.setupUi(self, self)
        self.db_url = db_url
        self.selectButton.clicked.connect(self.slot_accept)
        self.cancelButton.clicked.connect(self.slot_reject)
        self.success = False
        self.scale_factor = 1.0
        self.place_on_ground = False
        self.fill_combo_box_with_skeletons()
        t = threading.Thread(target=self.fill_tree_widget)
        t.start()
        self.src_model = None
        self.target_model = None
        self.collection = None

    def fill_combo_box_with_skeletons(self):
        skeleton_list = get_skeletons_from_remote_db(self.db_url)
        for idx, skel, owner in skeleton_list:
            self.sourceModelComboBox.addItem(skel, idx)
            self.targetModelComboBox.addItem(skel, idx)

    def slot_accept(self):
        self.scale_factor = float(self.scaleLineEdit.text())
        self.src_model = str(self.sourceModelComboBox.currentText())
        self.target_model = str(self.targetModelComboBox.currentText())
        self.place_on_ground = self.placeOnGroundRadioButton.isChecked()
            
        col = self.get_collection()
        if col is not None:
            self.collection, c_name, c_type = col
            self.success = True
        self.close()

    def slot_reject(self):
        self.close()#

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