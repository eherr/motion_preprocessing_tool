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

from PySide2.QtWidgets import QDialog, QListWidgetItem, QHBoxLayout, QLabel, QCheckBox, QLineEdit, QPushButton
from PySide2.QtCore import Qt
from motion_analysis.gui.layout.select_scene_object_dialog_ui import Ui_Dialog
from .utils import get_all_objects
from functools import partial
from .set_properties_dialog import SetPropertiesDialog


class SelectSceneObjectsDialog(QDialog, Ui_Dialog):
    def __init__(self, scene, filter_function=get_all_objects, parent=None, name=None, properties=None):
        QDialog.__init__(self, parent)
        Ui_Dialog.setupUi(self, self)
        if name is not None:
            self.setWindowTitle(name)

        self._filter_function = filter_function
        self.selectButton.clicked.connect(self.slot_accept)
        self.cancelButton.clicked.connect(self.slot_reject)
        self.success = False
        self.selected_node_id = -1
        self._fill_list_with_scene_objects(scene)
        self.properties = dict()
        if properties is not None:
            self.properties = properties
            for key in list(self.properties.keys()):
                self.add_line(key)

    def _fill_list_with_scene_objects(self, scene):
        for sceneObject in self._filter_function(scene):
            item = QListWidgetItem()
            item.setText(sceneObject.name)
            item.setData(Qt.UserRole, sceneObject.node_id)
            self.sceneObjectListWidget.addItem(item)

    def slot_accept(self):
        selected_item = self.sceneObjectListWidget.currentItem()
        node_id = selected_item.data(Qt.UserRole)
        self.selected_node_id = node_id
        print("selected item", selected_item.text(),self.selected_node_id)
        self.success = True
        self.close()

    def slot_reject(self):
        self.close()

    def add_line(self, key):
        layout = QHBoxLayout()
        label = QLabel(self)
        name =str(key)
        label.setText(name)
        layout.addWidget(label)
        value = self.properties[key]
        if isinstance(value, (bool)):
            checkbox = QCheckBox(self)
            checkbox.setChecked(bool(value))
            layout.addWidget(checkbox)
            checkbox.stateChanged.connect(partial(self.update_value, key=key, type_func=bool))
            #self.connect(checkbox, QtCore.SIGNAL('stateChanged(int)'), partial(self.update_value, key=key, type_func=bool))
        elif isinstance(value, (int, float, complex)):
            value = str(value)
            line_edit = QLineEdit(self)
            line_edit.setText(value)
            layout.addWidget(line_edit)
            line_edit.textChanged.connect(partial(self.update_value, key=key, type_func=float))
            #self.connect(line_edit, QtCore.SIGNAL('textChanged(QString)'), partial(self.update_value, key=key, type_func=float))
        elif isinstance(value, (int)):
            value = str(value)
            line_edit = QLineEdit(self)
            line_edit.setText(value)
            layout.addWidget(line_edit)
            line_edit.textChanged.connect(partial(self.update_value, key=key, type_func=int))
            #self.connect(line_edit, QtCore.SIGNAL('textChanged(QString)'), partial(self.update_value, key=key, type_func=int))
        elif isinstance(value, (str)):
            value = str(value)
            line_edit = QLineEdit(self)
            line_edit.setText(value)
            layout.addWidget(line_edit)
            line_edit.textChanged.connect(partial(self.update_value, key=key, type_func=str))
            #self.connect(line_edit, QtCore.SIGNAL('textChanged(QString)'), partial(self.update_value, key=key, type_func=str))
        elif isinstance(value, dict):
            button = QPushButton(self)
            button.setText("Set Values")
            button.setObjectName(key)
            button.clicked.connect(self.update_dictionary)
            #self.connect(button, QtCore.SIGNAL("clicked()"), self.update_dictionary)
            layout.addWidget(button)
        self.settingsVerticalLayout.addLayout(layout)

    def update_value(self, value, key, type_func):
        self.properties[key] = type_func(value)
        print("value changed", key, self.properties[key])

    def update_dictionary(self):
        key = str(self.sender().objectName())
        print("sender", key)
        dialog = SetPropertiesDialog(self.properties[key], self)
        dialog.exec_()
        self.properties[key] = dialog.properties