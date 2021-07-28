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
import glob
from PySide2.QtWidgets import QDialog, QListWidgetItem, QFileDialog
from PySide2.QtCore import Qt
from tool.core.layout.retarget_dialog_ui import Ui_Dialog
from vis_utils.io import load_json_file, save_json_file
from .utils import get_animation_controllers, load_local_skeleton, load_local_skeleton_model, save_local_skeleton, get_local_skeletons
from tool import constants
try:
    from tool.core.dialogs.skeleton_editor_dialog import SkeletonEditorDialog
except:
    pass
from tool.core.application_manager import ApplicationManager


class RetargetDialog(QDialog, Ui_Dialog):
    def __init__(self, target_controller, scene, parent=None):
        QDialog.__init__(self, parent)
        Ui_Dialog.setupUi(self, self)
        self.selectButton.clicked.connect(self.slot_accept)
        self.cancelButton.clicked.connect(self.slot_reject)
        self.addNewSourceSkeletonModelButton.clicked.connect(self.add_new_src_skeleton_model)
        self.addTartSkeletonModelButton.clicked.connect(self.add_new_target_skeleton_model)

        self.editSourceSkeletonModel.clicked.connect(self.edit_src_skeleton_model)
        self.editTargetSkeletonModel.clicked.connect(self.edit_target_skeleton_model)
        
        self.db_url = constants.DB_URL
        self.target_controller = target_controller
        self.target_skeleton = self.target_controller.get_skeleton()
        self.target_model = self.target_skeleton.skeleton_model
        self.local_skeleton_dir = constants.DATA_DIR + os.sep + "skeletons"
        self.skeleton_list = get_local_skeletons(self.local_skeleton_dir)
        self.success = False
        self.controllers = dict()
        self.selected_node_id = -1
        self.scale_factor = 1.0
        self._fill_list_with_scene_objects(scene)
        self.fill_combo_box_with_models()
        self.src_model = None
        self.target_model = None
        self.start_frame = 0
        self.end_frame = 1
        self.init_sliders(None)
        self.sceneObjectListWidget.itemClicked.connect(self.init_sliders)

    def init_sliders(self, item):
        if item is not None:
            selected_item = str(self.sceneObjectListWidget.currentItem().text())
            c = self.controllers[selected_item]
            self.end_frame = c.getNumberOfFrames()
        self.startFrameSlider.setRange(self.start_frame, self.end_frame)
        self.startFrameSlider.setValue(self.start_frame)
        self.endFrameSlider.setRange(self.start_frame, self.end_frame)
        self.endFrameSlider.setValue(self.end_frame-1)

        self.startFrameSlider.valueChanged.connect(self.slider_frame_changed)
        self.endFrameSlider.valueChanged.connect(self.slider_frame_changed)
        self.startFrameLineEdit.setText(str(self.startFrameSlider.value()))
        self.endFrameLineEdit.setText(str(self.endFrameSlider.value()))

    def _fill_list_with_scene_objects(self, scene):
        for sceneObject in get_animation_controllers(scene):
            item = QListWidgetItem()
            item.setText(sceneObject.name)
            item.setData(Qt.UserRole, sceneObject.node_id)
            self.sceneObjectListWidget.addItem(item)
            self.controllers[sceneObject.name] = sceneObject._components["animation_controller"]

    def fill_combo_box_with_models(self):
        skeleton_model_list = self.skeleton_list
        for idx, m in enumerate(skeleton_model_list):
            self.sourceModelComboBox.addItem(m, idx)
            self.targetModelComboBox.addItem(m, idx)
            if self.target_model is not None and "name" in self.target_model and self.target_model["name"] == m:
                self.targetModelComboBox.setCurrentIndex(idx)

    def slot_accept(self):
        selected_item = self.sceneObjectListWidget.currentItem()
        self.scale_factor = float(self.scaleLineEdit.text())
        node_id = selected_item.data(Qt.UserRole)
        self.selected_node_id = node_id
        if self.src_model is None:
            key = str(self.sourceModelComboBox.currentText())
            self.src_model = load_local_skeleton_model(self.local_skeleton_dir, key)
        if self.target_model is None:
            key = str(self.targetModelComboBox.currentText())
            self.target_model = load_local_skeleton_model(self.local_skeleton_dir, key)

        self.start_frame = int(self.startFrameSlider.value())
        self.end_frame = int(self.endFrameSlider.value())
        if self.start_frame > self.end_frame:
            self.end_frame = self.start_frame + 1
        print("selected item", selected_item.text(),self.selected_node_id)
        self.success = True
        self.close()

    def slot_reject(self):
        self.close()

    def add_new_src_skeleton_model(self):
        selected_item = str(self.sceneObjectListWidget.currentItem().text())
        c = self.controllers[selected_item]
        skeleton = c.get_skeleton()
        graphics_widget = ApplicationManager.instance.graphics_widget
        enable_line_edit = True
        skeleton_model = dict() # create a new model
        skeleton_editor = SkeletonEditorDialog("", skeleton, graphics_widget, graphics_widget.parent, enable_line_edit, skeleton_model)
        skeleton_editor.exec_()
        if skeleton_editor.success and skeleton_editor.skeleton_model is not None:
            name = skeleton_editor.name
            data = dict()
            data["name"] = name
            data["skeleton"] = skeleton.to_unity_format()
            data["model"] = skeleton_editor.skeleton_model
            save_local_skeleton(self.local_skeleton_dir, name, skeleton_model)
            self.skeleton_list.append(name)
            self.fill_combo_box_with_models()

    def add_new_target_skeleton_model(self):
        skeleton = self.target_controller.get_skeleton()
        graphics_widget = ApplicationManager.instance.graphics_widget
        enable_line_edit = True
        skeleton_model = dict() # create a new model
        skeleton_editor = SkeletonEditorDialog("", skeleton, graphics_widget, graphics_widget.parent, enable_line_edit, skeleton_model)
        skeleton_editor.exec_()
        if skeleton_editor.success and skeleton_editor.skeleton_model is not None:
            name = skeleton_editor.name
            data = dict()
            data["name"] = name
            data["skeleton"] = skeleton.to_unity_format()
            data["model"] = skeleton_editor.skeleton_model
            save_local_skeleton(self.local_skeleton_dir, name, data)
            self.skeleton_list.append(name)
            self.fill_combo_box_with_models()

    def edit_src_skeleton_model(self):
        selected_item = str(self.sceneObjectListWidget.currentItem().text())
        c = self.controllers[selected_item]
        skeleton = c.get_skeleton()
        graphics_widget = ApplicationManager.instance.graphics_widget
        name = str(self.sourceModelComboBox.currentText())
        enable_line_edit = False
        data = load_local_skeleton(self.local_skeleton_dir, name)
        skeleton_model = data["model"]
        skeleton_editor = SkeletonEditorDialog(name, skeleton, graphics_widget, graphics_widget.parent, enable_line_edit, skeleton_model)
        skeleton_editor.exec_()
        if skeleton_editor.success and skeleton_editor.skeleton_model is not None:
            data["model"] = skeleton_editor.skeleton_model
            save_local_skeleton(self.local_skeleton_dir, name, data)

    def edit_target_skeleton_model(self):
        skeleton = self.target_controller.get_skeleton()
        graphics_widget = ApplicationManager.instance.graphics_widget
        name = str(self.targetModelComboBox.currentText())
        enable_line_edit = False
        data = load_local_skeleton(self.local_skeleton_dir, name)
        skeleton_model = data["model"]
        skeleton_editor = SkeletonEditorDialog(name, skeleton, graphics_widget, graphics_widget.parent, enable_line_edit, skeleton_model)
        skeleton_editor.exec_()
        if skeleton_editor.success and skeleton_editor.skeleton_model is not None:
            data["model"] = skeleton_editor.skeleton_model
            save_local_skeleton(self.local_skeleton_dir, name, data)

    def slider_frame_changed(self, frame):
        self.startFrameLineEdit.setText(str(self.startFrameSlider.value()))
        self.endFrameLineEdit.setText(str(self.endFrameSlider.value()))