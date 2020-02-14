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
from functools import partial
from PySide2.QtWidgets import  QDialog, QHBoxLayout, QLabel, QCheckBox, QLineEdit, QPushButton
from motion_analysis.gui.layout.set_config_dialog_ui import Ui_Dialog


class SetConfigDialog(QDialog, Ui_Dialog):
    def __init__(self, config, parent=None):
        self.success = False
        self.config = config
        QDialog.__init__(self, parent)
        Ui_Dialog.setupUi(self, self)
        self.acceptButton.clicked.connect(self.slot_accept)
        self.rejectButton.clicked.connect(self.slot_reject)
        for key in list(self.config.keys()):
                self.add_line(key)

    def add_line(self, key):
        layout = QHBoxLayout()
        label = QLabel(self)
        name =str(key)
        label.setText(name)
        layout.addWidget(label)
        value = self.config[key]
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

    def update_value(self, value,  key, type_func):
        self.config[key] = type_func(value)
        print("value changed", key, self.config[key])

    def update_dictionary(self):
        key = str(self.sender().objectName())
        print("sender", key)
        dialog = SetConfigDialog(self.config[key], self)
        dialog.exec_()
        self.config[key] = dialog.config

    def slot_accept(self):
        self.success = True
        self.close()

    def slot_reject(self):
        self.close()
