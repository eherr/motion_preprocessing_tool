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

import sys
import collections
import os
from functools import partial
from PySide2.QtUiTools import QUiLoader
from PySide2.QtCore import Qt, QFile
from PySide2.QtWidgets import QMainWindow, QMessageBox, QAction, QFileDialog, QColorDialog
from tool import core
from tool import constants
from tool.core.layout.mainwindow_ui import Ui_MainWindow
from tool import plugins
from tool.core.widget_manager import WidgetManager
from tool.core.application_manager import ApplicationManager
from tool.plugins.database.gui import MotionDBBrowserDialog, GraphTableViewDialog, UploadMotionDialog, LoginDialog, SynchronizeSkeletonsWithDBDialog
from tool.plugins.database.session_manager import SessionManager


class EditorWindow(QMainWindow, Ui_MainWindow):
    instance = None

    def __init__(self):
        if EditorWindow.instance is None:
            EditorWindow.instance = self
            QMainWindow.__init__(self)
            Ui_MainWindow.setupUi(self, self)
            self.session_manager = SessionManager()
            self.animationViewer.resize(860, 640)
            self.animationViewer.statusBar = self.statusBar
            self._full_screen = False
            self.app_manager = ApplicationManager(True, self.animationViewer)
            self.animationViewer.init_opengl.connect(self.app_manager.init_scenes)
            self.app_manager.add_view(self.animationViewer)
            self.app_manager.statusBar = self.statusBar
            self.actions = collections.OrderedDict()
            self.actions["File"] = [
                    {"text": "Load BVH File",  "function": partial(self.open_file_dialog, "bvh")},
                    {"text": "Load BVH files from Directory", "function": self.load_animation_directory},
                    {"text": "Load ASF File",  "function":  partial(self.open_file_dialog, "asf")},
                    {"text": "Load Morphable Graph", "function": partial(self.open_file_dialog, "zip")},
                    {"text": "Load Morphable Model", "function": partial(self.open_file_dialog, "mm.json")},
                    {"text": "Load MG State Machine", "function": partial(self.open_file_dialog, "mg.zip")},
                    {"text": "Load OBJ file", "function": partial(self.open_file_dialog, "obj")},
                    {"text": "Load DAE file", "function": partial(self.open_file_dialog, "dae")},
                    {"text": "Load FBX file", "function": partial(self.open_file_dialog, "fbx")},
                    {"text": "Load Ragdoll File",  "function": self.loadRagDoll},
                    {"text": "Load Blend Controller File", "function": self.loadBlendController},
                    {"text": "Load Height Map", "function": self.loadHeightMap},
                    {"text": "Load Constraints Format", "function": self.loadConstraintsFormat},
                    {"text": "Load Point Cloud", "function": partial(self.open_file_dialog, "pc")},
                    {"text": "Load C3D File", "function": partial(self.open_file_dialog, "c3d")},
                    {"text": "Run Python Script", "function": self.runPythonScript},
                    {"text": "Load Custom Unity Format", "function": partial(self.open_file_dialog, "_m.json")},
                    {"text": "Quit", "function": self.close, "status_tip": 'Exit application'}
                    ]
            self.actions["Database"] = [ {"text": "Login",  "function": self.loginToServer},
                                       {"text": "Open Motion DB Browser", "function": self.openMotionDBBrowser},
                                        {"text": "Open Graph Browser", "function" : self.loadGraphFromDB},
                                        {"text": "Upload Selected Motions", "function": self.uploadMotionsToDB},
                                        {"text": "Synchronize Skeleton Definitions", "function": self.synchromizeSkeletonsFromDB}
                                        
                                    ]
            self.actions["Create"] = [
                    {"text": "Group Animation Controller", "function": self.createGroupAnimationController},
                    {"text": "Blend Animation Controller", "function": self.createBlendAnimationController},
                    {"text": "spline", "function": self.startSplineDefinition},
                    {"text": "marker", "short_cut": "O","function": self.startMarkerDefinition},
                    {"text": "Stop editing", "short_cut": "E", "function": self.stopSceneInteraction}
                    ]
            if constants.vis_constants.activate_simulation:
               self.actions["Create"] += [{"text": "Articulated Body", "function": self.addArticulatedBody},
                                            {"text": "ode capsule object", "function": self.app_manager.createCapsuleObject},
                                            {"text": "ode box object", "function": self.app_manager.createBoxObject},
                                            {"text": "ode sphere object", "function": self.app_manager.createSphereObject},
                                            {"text": "ode linked capsule object", "function": self.app_manager.createLinkedCapsuleObject},
                                            {"text": "RagDoll", "function": self.app_manager.createRagDoll}]
            self.actions["View"] = [
                    {"text": "Set selected to camera target", "short_cut": "Ctrl+T", "function": self.setCameraTarget},
                    {"text": "Toggle full screen","short_cut": "F11", "function": self.toggleFullScreen},
                    {"text": "Hide/Show Selected", "short_cut": "Ctrl+H", "function": self.toggleVisibility},
                    {"text": "Save Screenshot", "short_cut": "Ctrl+E", "function": self.saveScreenshot}

            ]
            self.actions["Scene"] = [{"text": "Toggle scene widget", "function": self.toggleEditSceneWidget},
                                     {"text": "Delete selected objects", "short_cut": "Del", "function": self.deleteSelectedObjects}]
            if constants.vis_constants.activate_simulation:
                 self.actions["Scene"] += [{"text": "Toggle simulation", "short_cut": "P", "function": self.toggleSimulation},
                                            {"text": "Save simulation state","function": self.saveSimulationState},
                                            {"text": "Restore simulation state", "function": self.restoreSimulationState}]
  
            self.init_menus()
            self.init_slots()
            self.selectedJointName = ""
            self.object_widgets = dict()
            self.init_widgets()
            self.motion_db_browser_dialog = None

    def closeEvent(self, event):
        print("Close window")
        if self.motion_db_browser_dialog is not None:
            self.motion_db_browser_dialog.close()
            print("close db browser")
        else:
            print("db browser is none")
        self.animationViewer.makeCurrent()
        self.app_manager.deinitialize()
        del self.app_manager
        del self.animationViewer
        sys.exit(0)

    def init_widgets(self):
        self.object_widgets = dict()
        for key in WidgetManager.get_list():
            self.object_widgets[key] = WidgetManager.create(key, self)
            self.object_widgets[key].hide()
            self.objectPropertiesLayout.addWidget(self.object_widgets[key])
            if self.object_widgets[key].animated:
                self.app_manager.updated_animation_frame.connect(self.object_widgets[key].updateAnimationTimeInGUI)

    def init_menus(self):
        count = 0
        self.menus = dict()
        for action_type in self.actions:
            self.menus[action_type] = self.menuBar.addMenu("&"+action_type)
            for action_desc in self.actions[action_type]:
                action = self.create_action(**action_desc)
                self.menus[action_type].addAction(action)
                count += 1

    def init_slots(self):
        self.animationViewer.dropped_files.connect(self.handle_dropped_files)
        self.app_manager.added_scene_object.connect(self.slot_add_item_to_object_list)
        self.app_manager.deleted_scene_object.connect(self.delete_scene_table_entry)
        self.app_manager.update_scene_object.connect(self.update_widgets)
        self.sceneObjectTableWidget.itemClicked.connect(self.slot_set_current_object_based_on_item)
        self.sceneObjectTableWidget.verticalHeader().sectionClicked.connect(self.slot_set_current_object_based_on_row)

    def handle_dropped_files(self,links):
        """ handles drags of files or directories onto the animationViewer widget
        """
        for link in links:
            path = str(link)
            if os.path.isfile(path):
                self.app_manager.loadFile(path)
            elif os.path.isdir(path):
                self.app_manager.scene.object_builder.create_object("animation_directory_explorer", path, "bvh")

    def create_action(self, function, text, short_cut=None, status_tip=None):
        action = QAction(text, self)
        if short_cut is not None:
            action.setShortcut(short_cut)
        if status_tip is not None:
            action.setStatusTip(status_tip)
        action.triggered.connect(function)
        return action

    def update_widgets(self, node_id=-1):
        for key in list(self.object_widgets.keys()):
            self.object_widgets[key].hide()
            self.object_widgets[key].set_object(None)
            self.object_widgets[key].setEnabled(False)

        scene_object = self.app_manager.getSelectedObject()
        if scene_object is not None:
            for key in self.object_widgets:
                component_name = self.object_widgets[key].COMPONENT_NAME
                if component_name is None:
                    self.show_widget(key, scene_object)
                elif scene_object.has_component(component_name):
                    self.show_widget(key, scene_object)

    def show_widget(self, name, scene_object):
        self.object_widgets[name].set_object(scene_object)
        self.object_widgets[name].setEnabled(True)
        self.object_widgets[name].show()

    def load_animation_directory(self):
        directory = QFileDialog.getExistingDirectory(self, "Select Directory")
        directory = str(directory)
        if os.path.isdir(directory):
            self.app_manager.scene.object_builder.create_object("animation_directory_explorer", directory, "bvh")
 
    def slot_add_item_to_object_list(self, sceneId, name):
        """Adds a row to the sceneObjectTableWidget"""
        if sceneId is None:
            return
        print("add object to list")
        sceneObject = self.app_manager.getObject(sceneId)
        color = sceneObject.getColor()
        if color is None:
            color = [0, 0, 0]
        self.sceneObjectTableWidget.addObjectToList(sceneId, name, color)
        self.update_widgets()

    def slotRemoveItemFromAnimationList(self,animationIndex):
        for item in self.sceneObjectTableWidget:
            if animationIndex == item.data(1):
                print((item.text()))

    def slot_set_current_object_based_on_item(self, item):
        """ sets wether or not an animation is going to be displayed """
        print("select item", item.row(), item.column())
        if item.column() != 2:
            sceneId = self.sceneObjectTableWidget.getSceneIdFromRow(item.row())
            if item.checkState() == Qt.Checked:
                print(('"%s" Checked' % item.text()))
                self.app_manager.showSceneObject(sceneId)
            else:
                self.app_manager.hideSceneObject(sceneId)
            self.slot_set_current_object_based_on_row(item.row())
            #self.update_widgets()

        elif item.column() == 2:
            self.changeSkeletonColor(item)

    def slot_set_current_object_based_on_row(self, row):
        sceneId = self.sceneObjectTableWidget.getSceneIdFromRow(row)
        print("select object",sceneId)
        self.app_manager.select_object(sceneId)
        self.update_widgets()

    def open_file_dialog(self, filetype):
        filename = QFileDialog.getOpenFileName(self, 'Open File', '.')[0]
        self.app_manager.scene.object_builder.create_object_from_file(filetype, str(filename))

    def loadRagDoll(self):
        filename = QFileDialog.getOpenFileName(self, 'Open File', '.')[0]
        p = [0, 10, 0]
        scene_object = self.app_manager.scene.object_builder.create_object_from_file("ragdoll",p, str(filename))
        if scene_object is not None:
            self.app_manager.scene.addAnimationController(scene_object, "character_animation_recorder")

    def loadBlendController(self):
        filename = QFileDialog.getOpenFileName(self, 'Open File', '.')[0]
        self.app_manager.loadBlendController(str(filename))

    def openMotionDBBrowser(self):
        """ https://stackoverflow.com/questions/38309803/pyqt-non-modal-dialog-always-modal """
        if self.motion_db_browser_dialog is None:
            self.motion_db_browser_dialog = MotionDBBrowserDialog(self.app_manager.scene, parent=self)
        else:
            self.motion_db_browser_dialog.raise_()
            self.motion_db_browser_dialog.activateWindow()

    def synchromizeSkeletonsFromDB(self):
        synchronize_skeletons = SynchronizeSkeletonsWithDBDialog(self)
        synchronize_skeletons.exec_()

    def loadGraphFromDB(self):
        dialog = GraphTableViewDialog(self.app_manager.scene)
        dialog.exec_()
       
    def uploadMotionsToDB(self):
        controller_list = []
        node_ids = self.getSelectedSceneObjects()
        for node_id in node_ids:
            o = self.app_manager.scene.getObject(node_id)
            if "animation_controller" in o._components:
                controller_list.append(o._components["animation_controller"])
        if len(controller_list) > 0:
            dialog = UploadMotionDialog(controller_list)
            dialog.exec_()
            if dialog.success:
                print("success")

    def loadHeightMap(self):
        filename = QFileDialog.getOpenFileName(self, 'Open File', '.')[0]
        self.app_manager.loadHeightMap(str(filename))

    def loadConstraintsFormat(self):
        filename = QFileDialog.getOpenFileName(self, 'Open File', '.')[0]
        self.app_manager.loadConstraintsFormat(str(filename))

    def runPythonScript(self):
        filename = QFileDialog.getOpenFileName(self, 'Open File', '.')[0]
        self.app_manager.runPythonScript(str(filename))

    def changeSkeletonColor(self, item):
        color = QColorDialog.getColor()
        print("set color")
        item.setBackground(color)
        sceneId = self.sceneObjectTableWidget.getSceneIdFromRow(item.row())
        sceneObject = self.app_manager.scene.getObject(sceneId)
        try:
            sceneObject.setColor([color.redF(), color.greenF(), color.blueF()])
        except:
            print("could not set color")

    def slotShowErrorMessage(self,errorMessage):
        QMessageBox.about(self,"Error", errorMessage)

    def startSplineDefinition(self):
        """ change handling of clicks in the scene to create a spline control points
        """
        print("start spline definition")
        self.app_manager.startSplineDefinition()

    def startMarkerDefinition(self):
        """ change handling of clicks in the scene to create a marker and the edit its position
        """
        print("start marker definition")
        self.app_manager.startMarkerDefinition()

    def stopSceneInteraction(self):
        self.app_manager.stopSceneInteraction()

    def toggleFullScreen(self):
        print("toggle full screen", self._full_screen)
        if self._full_screen:
            self.showNormal()
            self._full_screen = False
        else:
            self.showFullScreen()
            self._full_screen = True

    def setCameraTarget(self):
        camera = self.app_manager.views[0].graphics_context.camera
        if camera._target is None and self.app_manager.scene.selected_scene_object is not None:
            camera.setTarget(self.app_manager.scene.selected_scene_object)
        else:
            camera.removeTarget()

    def toggleEditSceneWidget(self):
        self.app_manager.scene.toggle_scene_edit_widget()

    def toggleSimulation(self):
        self.app_manager.scene.toggle_simulation()
    
    def loginToServer(self):
        loginDialog = LoginDialog()
        loginDialog.exec_()
        if loginDialog.success:
            user = loginDialog.user
            password = loginDialog.password
            self.session_manager.login(user, password)

    def getSelectedSceneObjects(self):
        node_ids = []
        for row_idx in range(self.sceneObjectTableWidget.rowCount()):
            idx_cell = self.sceneObjectTableWidget.item(row_idx, 0)
            name_cell = self.sceneObjectTableWidget.item(row_idx, 1)
            if idx_cell.isSelected() or name_cell.isSelected():
                node_id = self.sceneObjectTableWidget.getSceneIdFromRow(row_idx)
                node_ids.append(node_id)
        return node_ids

    def createGroupAnimationController(self):
        node_ids = self.getSelectedSceneObjects()
        self.app_manager.scene.createGroupAnimationController(node_ids)

    def createBlendAnimationController(self):
        node_ids = self.getSelectedSceneObjects()
        self.app_manager.scene.createBlendAnimationController(node_ids)

    def addArticulatedBody(self):
        node_ids = self.getSelectedSceneObjects()
        if len(node_ids) > 0:
            node_id = node_ids[0]
            self.app_manager.scene.addArticulatedBody(node_id)

    def saveSimulationState(self):
        self.app_manager.scene.save_simulation_state()

    def restoreSimulationState(self):
        self.app_manager.scene.restore_simulation_state()

    def toggleVisibility(self):
        node_ids = self.getSelectedSceneObjects()
        self.app_manager.scene.toggle_visibility(node_ids)

    def saveScreenshot(self):
        self.app_manager.views[0].frame_buffer.save_to_file("framebuffer.png")

    def delete_scene_table_entry(self, node_id):
        for row_idx in range(self.sceneObjectTableWidget.rowCount()):
             if self.sceneObjectTableWidget.getSceneIdFromRow(row_idx) == node_id:
                self.sceneObjectTableWidget.removeRow(row_idx)

    def deleteSelectedObjects(self):
        node_ids = self.getSelectedSceneObjects()
        self.app_manager.scene.delete_objects(node_ids)
        self.deleteSceneTableEntries(node_ids)

    def deleteSceneTableEntries(self, node_ids):
        for node_id in node_ids:
            self.delete_scene_table_entry(node_id)

    def keyReleaseEvent(self, event):
        if event.modifiers() & Qt.ControlModifier:
            if event.key() == Qt.Key_Left:
                self.app_manager.views[0].graphics_context.rotate_left()
            elif event.key() == Qt.Key_Right:
                self.app_manager.views[0].graphics_context.rotate_right()
            elif event.key() == Qt.Key_Up:
                self.app_manager.views[0].graphics_context.rotate_up()
            elif event.key() == Qt.Key_Down:
                self.app_manager.views[0].graphics_context.rotate_down()

            speed = 10
            if event.key() == Qt.Key_A:
                self.app_manager.views[0].graphics_context.move_horizontally(-speed)
            elif event.key() == Qt.Key_D:
                self.app_manager.views[0].graphics_context.move_horizontally(speed)
            elif event.key() == Qt.Key_W:
                self.app_manager.views[0].graphics_context.move_forward(-speed)
            elif event.key() == Qt.Key_S:
                self.app_manager.views[0].graphics_context.move_forward(speed)
            elif event.key() == Qt.Key_R:
                self.app_manager.views[0].graphics_context.reset_camera()
        else:
            for object_id in self.getSelectedSceneObjects():
                o = self.app_manager.scene.getObject(object_id)
                o.handle_keyboard_input(str(event.text()))
            self.app_manager.scene.scene_edit_widget.handle_keyboard_input(event.key())

