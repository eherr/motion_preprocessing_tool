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
from PySide2.QtWidgets import QDialog
from motion_analysis.gui.layout.copy_motion_dialog_ui import Ui_Dialog


class CopyMotionDialog(QDialog, Ui_Dialog):
    def __init__(self, n_frames, default_name="",parent=None):
        QDialog.__init__(self, parent)
        Ui_Dialog.setupUi(self, self)
      
        self.selectButton.clicked.connect(self.slot_accept)
        self.cancelButton.clicked.connect(self.slot_reject)
        self.startFrameSlider.valueChanged.connect(self.slider_frame_changed)
        self.endFrameSlider.valueChanged.connect(self.slider_frame_changed)
        self.startFrameSpinBox.valueChanged.connect(self.spinbox_frame_changed)
        self.endFrameSpinBox.valueChanged.connect(self.spinbox_frame_changed)
        self.success = False
        self.name = default_name
        self.n_frames = n_frames
        self.start_frame = 0
        self.end_frame = n_frames-1
        self.nameLineEdit.setText(default_name)
        self.set_frame_range()

    def set_frame_range(self):
        self.startFrameSlider.setRange(0, self.n_frames)
        self.endFrameSlider.setRange(0, self.n_frames)
        self.startFrameSpinBox.setRange(0, self.n_frames)
        self.endFrameSpinBox.setRange(0, self.n_frames)

        self.endFrameSlider.setValue(self.n_frames - 1)
        self.endFrameSpinBox.setValue(self.n_frames - 1)

    def spinbox_frame_changed(self, frame):
        self.startFrameSlider.setValue(self.startFrameSpinBox.value())
        self.endFrameSlider.setValue(self.endFrameSpinBox.value())

    def slider_frame_changed(self, frame):
        self.startFrameSpinBox.setValue(self.startFrameSlider.value())
        self.endFrameSpinBox.setValue(self.endFrameSlider.value())

    def slot_accept(self):
        self.name = str(self.nameLineEdit.text())
        self.start_frame = int(self.startFrameSlider.value())
        self.end_frame = int(self.endFrameSlider.value())
        self.success = True
        self.close()

    def slot_reject(self):
        self.close()
