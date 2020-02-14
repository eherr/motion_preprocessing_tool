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
from PySide2.QtWidgets import  QDialog, QListWidgetItem, QFileDialog, QAbstractItemView, QTreeWidgetItem
from PySide2.QtCore import Qt
from motion_analysis.gui.layout.new_collection_dialog_ui import Ui_Dialog
from motion_analysis.constants import DB_URL
from anim_utils.utilities.db_interface import get_collections_from_remote_db, get_collections_by_parent_id_from_remote_db



class NewCollectionDialog(QDialog, Ui_Dialog):
    def __init__(self, parent_name, parent_id, default_name="", col_type="", parent=None):
        QDialog.__init__(self, parent)
        Ui_Dialog.setupUi(self, self)
        self.acceptButton.clicked.connect(self.slot_accept)
        self.rejectButton.clicked.connect(self.slot_reject)
        self.parent_name = parent_name
        self.parentLabel.setText("Parent: "+parent_name)
        self.parent_id = parent_id
        self.db_url = DB_URL
        self.success = False
        self.name = default_name
        self.nameLineEdit.setText(default_name)
        self.col_type = col_type
        self.typeLineEdit.setText(col_type)
        self.owner = 0
        
    def slot_accept(self):
        self.success = True
        self.name = str(self.nameLineEdit.text())
        self.col_type = str(self.typeLineEdit.text())
        self.owner = int(self.ownerLineEdit.text())
        self.success = True
        self.close()

    def slot_reject(self):
        self.close()
    
