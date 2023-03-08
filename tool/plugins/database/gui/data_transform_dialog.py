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
from PySide2.QtWidgets import QDialog
from PySide2.QtCore import Qt
from tool.plugins.database.gui.layout.data_transform_dialog_ui import Ui_Dialog
from motion_db_interface import get_skeletons_from_remote_db
from motion_db_interface.data_transform_interface import get_data_transforms, get_data_transform_info, get_data_transform_inputs

class DataTransformDialog(QDialog, Ui_Dialog):
    def __init__(self, db_url, session, collection_id, c_name, input_skeleton, parent=None):
        QDialog.__init__(self, parent)
        Ui_Dialog.setupUi(self, self)
        self.collection_id = collection_id
        self.collection_name = c_name
        self.input_skeleton = input_skeleton
        self.db_url = db_url
        self.session = session
        self.selectButton.clicked.connect(self.slot_accept)
        self.cancelButton.clicked.connect(self.slot_reject)
        self.dataTransformComboBox.currentTextChanged.connect(self.slot_on_change)
        self.success = False
        self.fill_combo_box_with_data_transforms()
        self.fill_combo_box_with_skeletons()
        self.data_transform_id = None
        self.name = None
        self.user = None
        self.password = None
        self.store_log = False
        self.parameters= dict()
        self.use_cluster = False
        self.input_data = None
        self.output_skeleton = None

    def fill_combo_box_with_data_transforms(self):
        data_transforms = get_data_transforms(self.db_url)
        for dtid, name, outputType, isCollection in data_transforms:
            self.dataTransformComboBox.addItem(name, userData=dtid)

    def fill_combo_box_with_skeletons(self):
        input_idx = 0
        skeleton_list = get_skeletons_from_remote_db(self.db_url)
        for idx, (skel_id, skel, owner) in enumerate(skeleton_list):
            self.outputSkeletonComboBox.addItem(skel, skel_id)
            if skel == self.input_skeleton:
                input_idx = idx
        self.outputSkeletonComboBox.setCurrentIndex(input_idx)

    def slot_on_change(self):
        self.data_transform_id = self.dataTransformComboBox.currentData(Qt.UserRole)
        self.info = get_data_transform_info(self.db_url, self.data_transform_id, self.session)
        self.parametersTextEdit.setText(self.info["parameters"])
        return

    def slot_accept(self):
        self.data_transform_id = self.dataTransformComboBox.currentData(Qt.UserRole)
        self.name = str(self.nameLineEdit.text())
        parameters_str = str(self.parametersTextEdit.toPlainText())
        try:
            self.parameters = json.loads(parameters_str)
        except:
            print("Error: parsing parameteres")
        self.output_skeleton = self.dataTransformComboBox.currentText()
        self.store_log = self.storeLogCheckBox.isChecked()
        self.use_cluster = self.useClusterCheckBox.isChecked()
        self.input_data = []
        dt_inputs = get_data_transform_inputs(self.db_url, self.data_transform_id, self.session)
        if dt_inputs is not None:
            for dti in dt_inputs:
                self.input_data.append([self.collection_id, dti[1], dti[2]])

        self.user = str(self.userLineEdit.text())
        self.password = str(self.passwordLineEdit.text())

        self.success = True
        self.close()

    def slot_reject(self):
        self.close()
