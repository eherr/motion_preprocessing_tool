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
import json
from PySide2.QtWidgets import  QDialog, QFileDialog
from motion_analysis.gui.layout.new_skeleton_dialog_ui import Ui_Dialog
from anim_utils.animation_data import BVHReader, BVHWriter, MotionVector, SkeletonBuilder, parse_asf_file


class NewSkeletonDialog(QDialog, Ui_Dialog):
    def __init__(self, default_name="", parent=None):
        QDialog.__init__(self, parent)
        Ui_Dialog.setupUi(self, self)
        self.acceptButton.clicked.connect(self.slot_accept)
        self.rejectButton.clicked.connect(self.slot_reject)
        self.loadBVHButton.clicked.connect(self.slot_load_bvh_str)
        self.loadASFButton.clicked.connect(self.slot_load_asf_str)
        self.loadSkeletonModelButton.clicked.connect(self.slot_load_skeleton_model)
        self.success = False
        self.name = default_name
        self.nameLineEdit.setText(default_name)
        self.data = None
        self.skeleton_model = None


    def slot_accept(self):
        self.name = str(self.nameLineEdit.text())
        self.success = True
        self.close()

    def slot_reject(self):
        self.close()
    
    def slot_load_bvh_str(self):        
        filename = QFileDialog.getOpenFileName(self, 'Open File', '.')[0]
        filename = str(filename)
        if os.path.isfile(filename):
            try:
                bvh = BVHReader(filename)
                skeleton = SkeletonBuilder().load_from_bvh(bvh, list(bvh.get_animated_joints()))
                self.data = skeleton.to_unity_format()
                print("loaded bvh string from", filename)
            except Exception as e:
                self.data = None
                print("Could not read file", e.args, filename)

    def slot_load_asf_str(self):        
        filename = QFileDialog.getOpenFileName(self, 'Open File', '.')[0]
        filename = str(filename)
        if os.path.isfile(filename):
            try:
                asf_data = parse_asf_file(filename)
                skeleton = SkeletonBuilder().load_from_asf_data(asf_data)
                self.data = skeleton.to_unity_format()
                print("loaded asf string from", filename)
            except Exception as e:
                self.data = None
                print("Could not read file", e.args, filename)
    
    def slot_load_skeleton_model(self):
        filename = QFileDialog.getOpenFileName(self, 'Open File', '.')[0]
        filename = str(filename)
        if os.path.isfile(filename):
            try:
                with open(filename, "rt") as in_file:
                    self.skeleton_model = json.load(in_file)
                    print("loaded skeleton model from", filename)
            except  Exception as e:
                self.skeleton_model = None
                print("Could not read file", e.args)
