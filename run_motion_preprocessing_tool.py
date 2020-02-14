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
import sys, traceback
import os
#workaround for wrong Qt5 DLL path http://www.programmersought.com/article/8605863159/
import PySide2
dirname = os.path.dirname(PySide2.__file__)
plugin_path = os.path.join(dirname, 'plugins', 'platforms')
os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = plugin_path
from PySide2.QtWidgets import QApplication
import motion_analysis.gui.darkorange_icon_rc


if __name__ == '__main__':
    from motion_analysis.constants import CONFIG_FILE
    if os.path.isfile(CONFIG_FILE):
        from motion_analysis.constants import set_constants_from_file
        set_constants_from_file(CONFIG_FILE)

    from motion_analysis.gui.editor_window import EditorWindow

    app = QApplication(sys.argv)
    # set style according to http://discourse.techart.online/t/release-qt-dark-orange-stylesheet/
    style_sheet_file = os.sep.join(["motion_analysis", "gui", "darkorange.stylesheet"])
    app.setStyle('Fusion')
    with open(style_sheet_file, "r") as fh:
        app.setStyleSheet(fh.read())
    
    win = EditorWindow()
    win.show()
    app.setActiveWindow(win)
    app.exec_()
