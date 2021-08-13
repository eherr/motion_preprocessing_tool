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
import numpy as np
from PySide2.QtWidgets import  QWidget, QAction
from tool.core.layout.object_properties_widget_ui import Ui_Form
from tool.core.widget_manager import WidgetManager


class ObjectPropertiesWidget(QWidget, Ui_Form):
    COMPONENT_NAME = None
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        Ui_Form.setupUi(self, self)

        self._init_actions()
        self._init_signals()
        self._init_slots()
        self._scene_object = None

    def set_object(self, scene_object):
        self._scene_object = scene_object
        if self._scene_object is not None:
            position = self._scene_object.getPosition()
            position = list(map(partial(round, ndigits=3), position))
            position_str = list(map(str, position))
            self.posXLineEdit.setText(position_str[0])
            self.posYLineEdit.setText(position_str[1])
            self.posZLineEdit.setText(position_str[2])
            self.nameLineEdit.setText(self._scene_object.name)
            self.scaleLineEdit.setText(str(self._scene_object.get_scale()))

    def _init_actions(self):
        self.updateAction = QAction("Update", self)
        self.updateAction.triggered.connect(self._set_object_values)
        self.posXLineEdit.returnPressed.connect(self._set_object_values)
        self.posYLineEdit.returnPressed.connect(self._set_object_values)
        self.posZLineEdit.returnPressed.connect(self._set_object_values)
        self.scaleLineEdit.returnPressed.connect(self._set_object_values)

    def _init_signals(self):
        self.updateButton.setDefaultAction(self.updateAction)

    def _init_slots(self):
        return
        #self.connect(self.animationFrameSlider, QtCore.SIGNAL("valueChanged(Qstri) "), self.valueChanged)

    def _set_object_values(self):
        if self._scene_object is not None:
            position = list(map(float, [self.posXLineEdit.text(), self.posYLineEdit.text(), self.posZLineEdit.text()]))
            self._scene_object.setPosition(np.array(position))
            self._scene_object.name = str(self.nameLineEdit.text())
            scale = float(self.scaleLineEdit.text())
            self._scene_object.set_scale(scale)


WidgetManager.register("object", ObjectPropertiesWidget)