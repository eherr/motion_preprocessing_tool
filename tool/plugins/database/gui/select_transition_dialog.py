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
from PySide2.QtWidgets import QDialog, QTreeWidgetItem, QFileDialog
from PySide2.QtCore import Qt
from .layout.copy_db_dialog_ui import Ui_Dialog
from vis_utils.io import load_json_file
from anim_utils.animation_data.skeleton_models import SKELETON_MODELS

class SelectTransitionDialog(QDialog, Ui_Dialog):
    def __init__(self, graph_data, parent=None):
        QDialog.__init__(self, parent)
        Ui_Dialog.setupUi(self, self)
        self.graph_data = graph_data
        self.selectButton.clicked.connect(self.slot_accept)
        self.cancelButton.clicked.connect(self.slot_reject)
        self.success = False
        self.transition_name = ""
        self.transition_entry = None
        self.fill_tree_widget()

    def slot_accept(self):
        colItem = self.collectionTreeWidget.currentItem()
        if colItem is None or colItem.parent() is None:
            return
        model_name = str(colItem.text(0))
        action_name = str(colItem.parent().text(0))
        model_id = int(colItem.data(0, Qt.UserRole))
        self.transition_name = action_name+":"+model_name
        self.transition_entry = {"action_name": action_name, "model_name": model_name, "model_id": model_id}
        self.success = True
        self.close()

    def slot_reject(self):
        self.close()

    def fill_tree_widget(self):
        self.collectionTreeWidget.clear()
        self.rootItem = QTreeWidgetItem(self.collectionTreeWidget, ["root", "root"])
        self.rootItem.setExpanded(True)
        # root collection has id 0
        self.rootItem.setData(0, Qt.UserRole, 0)
        for action in self.graph_data["nodes"]:
            actionItem = QTreeWidgetItem(self.rootItem, [action, "action"])
            actionItem.setData(0, Qt.UserRole, action)
            for mp_id in self.graph_data["nodes"][action]:
                model_name = self.graph_data["nodes"][action][mp_id]["name"]
                mpItem = QTreeWidgetItem(actionItem, [model_name, "primitive"])
                mpItem.setData(0, Qt.UserRole, int(mp_id))
