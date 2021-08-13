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
from PySide2.QtWidgets import  QDialog, QListWidgetItem, QFileDialog, QAbstractItemView, QTreeWidgetItem
from PySide2.QtCore import Qt
from .layout.edit_collection_dialog_ui import Ui_Dialog
from tool.plugins.database.constants import DB_URL
from anim_utils.utilities.db_interface import get_collections_from_remote_db, get_collections_by_parent_id_from_remote_db



class EditCollectionDialog(QDialog, Ui_Dialog):
    def __init__(self, collection_id, parent_name, parent_id, default_name="", col_type="", owner=0, parent=None):
        QDialog.__init__(self, parent)
        Ui_Dialog.setupUi(self, self)
        self.acceptButton.clicked.connect(self.slot_accept)
        self.rejectButton.clicked.connect(self.slot_reject)
        self.parent_name = parent_name
        self.collection_id = collection_id
        #self.parentLabel.setText("Parent: "+parent_name)
        self.parent_id = parent_id
        self.db_url = DB_URL
        self.success = False
        self.name = default_name
        self.nameLineEdit.setText(default_name)
        self.col_type = col_type
        self.typeLineEdit.setText(col_type)
        self.ownerLineEdit.setText(str(owner))
        t = threading.Thread(target=self.fill_tree_widget)
        t.start()

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
            if col[0] == self.collection_id:
                self.select_tree_node(parent_item)
                continue
            colItem = QTreeWidgetItem(parent_item, [col[1], col[2]])
            colItem.setData(0, Qt.UserRole, col[0])
            self.fill_tree_widget((colItem, col[0]))

    def select_tree_node(self, node):
        node.setSelected(True)
        while node is not None:
            node.setExpanded(True)
            node = node.parent()

    def get_collection(self):
        colItem = self.collectionTreeWidget.currentItem()
        if colItem is None:
            return
        return int(colItem.data(0, Qt.UserRole)),  str(colItem.text(0)), str(colItem.text(1))

    def slot_accept(self):
        col = self.get_collection()
        if col is not None:
            self.parent_id, self.parent_name, c_type = col
            self.success = True
        self.name = str(self.nameLineEdit.text())
        self.col_type = str(self.typeLineEdit.text())
        self.owner = int(self.ownerLineEdit.text())
        self.success = True
        self.close()

    def slot_reject(self):
        self.close()
    
