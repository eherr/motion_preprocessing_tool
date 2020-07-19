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


import collections
import os
from PySide2.QtUiTools import QUiLoader
from PySide2.QtCore import Qt, QFile
from PySide2.QtWidgets import QMainWindow, QMessageBox, QAction, QFileDialog, QColorDialog
from motion_analysis import constants
from motion_analysis.gui.layout.mainwindow_ui import Ui_MainWindow
from motion_analysis import motion_synthesis
from motion_analysis.gui.widgets import ObjectPropertiesWidget, AnimationEditorWidget, AnimationPlayerWidget, \
                                        CharacterWidget, FigureControllerWidget, GroupAnimationPlayerWidget, MGStateMachineWidget, \
                                         MorphableGraphControllerWidget, MotionPrimitiveControllerWidget, NavAgentWidget, \
                                         BlendAnimationControllerWidget,AnimatedMeshWidget
from motion_analysis.gui.dialogs.motion_db_browser_dialog import MotionDBBrowserDialog
from motion_analysis.gui.dialogs.graph_table_view_dialog import GraphTableViewDialog
from motion_analysis.gui.dialogs.upload_motion_dialog import UploadMotionDialog
from motion_analysis.gui.dialogs.login_dialog import LoginDialog
from motion_analysis.gui.dialogs.synchronize_skeletons_with_db_dialog import SynchronizeSkeletonsWithDBDialog
from motion_analysis.gui.application_manager import ApplicationManager
from motion_analysis.session_manager import SessionManager

MG_COMPONENT = "morphablegraphs_controller"
ANIMATION_COMPONENT = "animation_controller"
MP_COMPONENT = "motion_primitive_controller"
BLEND_COMPONENT = "blend_controller"
ANIMATED_MESH_COMPONENT = "animated_mesh"
FIGURE_CONTROLLER_COMPONENT = "figure_controller"
ANIMATION_EDITOR_COMPONENT = "animation_editor"
MG_STATE_MACHINE_COMPONENT = "morphablegraph_state_machine"
NAV_AGENT_COMPONENT = "nav_agent"
SCENE_OBJECT_WIDGETS = collections.OrderedDict()
SCENE_OBJECT_WIDGETS["object"] =dict(constructor=ObjectPropertiesWidget, animated=False)
SCENE_OBJECT_WIDGETS["animation_player"] = dict(constructor=AnimationPlayerWidget, animated=True)
SCENE_OBJECT_WIDGETS["mg_player"] =dict(constructor=MorphableGraphControllerWidget, animated=False)
SCENE_OBJECT_WIDGETS["mp_player"] = dict(constructor=MotionPrimitiveControllerWidget, animated=True)
SCENE_OBJECT_WIDGETS["character"] = dict(constructor=CharacterWidget, animated=False)
SCENE_OBJECT_WIDGETS["group_player"] = dict(constructor=GroupAnimationPlayerWidget, animated=True)
SCENE_OBJECT_WIDGETS["blend_controller"] = dict(constructor=BlendAnimationControllerWidget, animated=True)
SCENE_OBJECT_WIDGETS["animated_mesh"] = dict(constructor=AnimatedMeshWidget, animated=False)
SCENE_OBJECT_WIDGETS["figure_controller"] = dict(constructor=FigureControllerWidget, animated=False)
SCENE_OBJECT_WIDGETS["morphablegraph_state_machine"] = dict(constructor=MGStateMachineWidget, animated=False)
SCENE_OBJECT_WIDGETS["nav_agent"] = dict(constructor=NavAgentWidget, animated=False)


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
            self.sceneManager = ApplicationManager(True, self.animationViewer)
            self.animationViewer.init_opengl.connect(self.sceneManager.init_scenes)
            self.sceneManager.add_view(self.animationViewer)
            self.sceneManager.statusBar = self.statusBar
            self.actions = collections.OrderedDict()
            self.actions["File"] = [
                    {"text": "Load BVH File",  "function": self.loadBVHFile},
                    {"text": "Load BVH files from Directory", "function": self.loadBVHFilesFromDirectory},
                    {"text": "Load ASF File",  "function": self.loadASFFile},
                    {"text": "Load Morphable Graph", "function": self.loadMorphableGraphFile},
                    {"text": "Load Morphable Model", "function": self.loadMorphableModelFile},
                    {"text": "Load MG State Machine", "function": self.loadMorphableGraphStateMachine},
                    {"text": "Load OBJ file", "function": self.loadOBJFile},
                    {"text": "Load DAE file", "function": self.loadCOLLADAFile},
                    {"text": "Load FBX file", "function": self.loadFBXFile},
                    {"text": "Load Ragdoll File",  "function": self.loadRagDoll},
                    {"text": "Load Blend Controller File", "function": self.loadBlendController},
                    {"text": "Load Height Map", "function": self.loadHeightMap},
                    {"text": "Load Constraints Format", "function": self.loadConstraintsFormat},
                    {"text": "Load Point Cloud", "function": self.loadPointCloud},
                    {"text": "Load C3D File", "function": self.loadC3DFile},
                    {"text": "Run Python Script", "function": self.runPythonScript},
                    {"text": "Load Custom Unity Format", "function": self.loadCustomUnityFormat},
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
                                            {"text": "ode capsule object", "function": self.sceneManager.createCapsuleObject},
                                            {"text": "ode box object", "function": self.sceneManager.createBoxObject},
                                            {"text": "ode sphere object", "function": self.sceneManager.createSphereObject},
                                            {"text": "ode linked capsule object", "function": self.sceneManager.createLinkedCapsuleObject},
                                            {"text": "RagDoll", "function": self.sceneManager.createRagDoll}]
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
            self.initActions()
            self.initMenus()
            self.initSlots()
            self.selectedJointName = ""
            self.object_widgets = dict()
            self.addObjectWidgets()
            self.db_url = constants.DB_URL
            self.motion_db_browser_dialog = None

    def closeEvent(self, event):
        print("Close window")
        if self.motion_db_browser_dialog is not None:
            self.motion_db_browser_dialog.close()
            print("close db browser")
        else:
            print("db browser is none")
        self.animationViewer.makeCurrent()
        self.sceneManager.deinitialize()
        try:
           del self.sceneManager
           del self.animationViewer
        except:
            print("ignore the error and keep going")

    def addObjectWidgets(self):
        widgets = SCENE_OBJECT_WIDGETS
        self.object_widgets = dict()
        for key in widgets:
            self.object_widgets[key] = widgets[key]["constructor"](self)
            self.object_widgets[key].hide()
            self.objectPropertiesLayout.addWidget(self.object_widgets[key])
            if widgets[key]["animated"]:
                self.sceneManager.updated_animation_frame.connect(self.object_widgets[key].updateAnimationTimeInGUI)

    def initActions(self):
        for action_type in list(self.actions.keys()):
            for action_desc in self.actions[action_type]:
                self._add_qt_action(**action_desc)

    def initMenus(self):
        self.menus = dict()
        for action_type in list(self.actions.keys()):
            self.menus[action_type] = self.menuBar.addMenu("&"+action_type)
            for action in self.actions[action_type]:
                action_name = action["function"].__name__ + 'Action'
                self.menus[action_type].addAction(getattr(self, action_name))

    def initSlots(self):
        self.animationViewer.dropped_files.connect(self.handleDroppedFiles)
        self.sceneManager.reached_end_of_animation.connect(self.slotHandleEndOfAnimation)
        self.sceneManager.added_scene_object.connect(self.slotAddItemToObjectList)
        self.sceneManager.deleted_scene_object.connect(self.deleteSceneTableEntry)
        self.sceneManager.update_scene_object.connect(self.updateAnimationGUI)
        self.sceneObjectTableWidget.itemClicked.connect(self.slotSetCurrentObjectBasedOnItem)
        self.sceneObjectTableWidget.verticalHeader().sectionClicked.connect(self.slotSetCurrentObjectBasedOnRow)

    def handleDroppedFiles(self,links):
        """ handles drags of files or directories onto the animationViewer widget
        """
        for link in links:
            path = str(link)
            if os.path.isfile(path):
                self.sceneManager.loadFile(path)
            elif os.path.isdir(path):
                filePaths = []
                for root, dirs, files in os.walk(path):
                    for name in files:
                        if name.endswith(".bvh"):
                            filePath = os.path.join(root,name)
                            self.sceneManager.scene.object_builder.create_object_from_file("bvh", filePath)

    def _add_qt_action(self, function, text, short_cut=None, status_tip=None):
        action_name = function.__name__ + 'Action'
        setattr(self, action_name, QAction(text, self))
        if short_cut is not None:
            getattr(self, action_name).setShortcut(short_cut)
        if status_tip is not None:
            getattr(self, action_name).setStatusTip(status_tip)
        getattr(self, action_name).triggered.connect(function)

    #======================================================================================================
    # ANIMATION VIEWER
    #======================================================================================================

    def updateAnimationGUI(self, node_id=-1):
        for key in list(self.object_widgets.keys()):
            self.object_widgets[key].hide()
            self.object_widgets[key].set_object(None)
            self.object_widgets[key].setEnabled(False)

        scene_object = self.sceneManager.getSelectedObject()
        if scene_object is not None:
            if scene_object.has_component(MG_COMPONENT):
                self.show_widget("mg_player", scene_object._components[MG_COMPONENT])

            if scene_object.has_component(MP_COMPONENT):
                self.show_widget("mp_player", scene_object._components[MP_COMPONENT])

            if scene_object.has_component(ANIMATION_COMPONENT):
                self.show_widget("animation_player", scene_object._components[ANIMATION_COMPONENT])

            if scene_object.has_component("character"):
                self.show_widget("character", scene_object._components["character"])

            if scene_object.has_component("character_animation_recorder"):
                self.show_widget("character_animation_recorder", scene_object._components["character_animation_recorder"])

            if scene_object.has_component("group_player"):
                self.show_widget("group_player", scene_object._components["group_player"])

            if scene_object.has_component("blend_controller"):
                self.show_widget("blend_controller", scene_object._components["blend_controller"])

            if scene_object.has_component("animated_mesh"):
                self.show_widget("animated_mesh", scene_object._components["animated_mesh"])

            if scene_object.has_component("figure_controller"):
                self.show_widget("figure_controller", scene_object)

            if scene_object.has_component("animation_editor"):
                self.show_widget("animation_editor", scene_object)

            if scene_object.has_component("morphablegraph_state_machine"):
                self.show_widget("morphablegraph_state_machine", scene_object)

            if scene_object.has_component("nav_agent"):
                self.show_widget("nav_agent", scene_object)

            self.show_widget("object", scene_object)

    def show_widget(self, name, scene_object):
        self.object_widgets[name].set_object(scene_object)
        self.object_widgets[name].setEnabled(True)
        self.object_widgets[name].show()

    def loadBVHFile(self):
        filename = QFileDialog.getOpenFileName(self, 'Open File', '.')[0]
        if filename is not None:
            self.sceneManager.scene.object_builder.create_object_from_file("bvh",str(filename))

    def loadASFFile(self):
        filename = QFileDialog.getOpenFileName(self, 'Open File', '.')[0]
        if filename is not None:
            self.sceneManager.scene.object_builder.create_object_from_file("asf",str(filename))

    def loadBVHFilesFromDirectory(self):
        directory = QFileDialog.getExistingDirectory(self, "Select Directory")
        for root, dirs, files in os.walk(str(directory)):
            for name in files:
                if name.endswith(".bvh"):
                    filePath = os.path.join(root,name)
                    self.sceneManager.scene.object_builder.create_object_from_file("bvh", filePath)

 
    def slotAddItemToObjectList(self, sceneId, name):
        """Adds a row to the sceneObjectTableWidget"""
        if sceneId is None:
            return
        print("add object to list")
        sceneObject = self.sceneManager.getObject(sceneId)
        color = sceneObject.getColor()
        if color is None:
            color = [0, 0, 0]
        self.sceneObjectTableWidget.addObjectToList(sceneId, name, color)
        self.updateAnimationGUI()

    def slotRemoveItemFromAnimationList(self,animationIndex):
        for item in self.sceneObjectTableWidget:
            if animationIndex == item.data(1):
                print((item.text()))

    def slotHandleEndOfAnimation(self,animationIndex,loop):
        return

    def slotSetCurrentObjectBasedOnItem(self, item):
        """ sets wether or not an animation is going to be displayed """
        print("select item", item.row(), item.column())
        if item.column() != 2:
            sceneId = self.sceneObjectTableWidget.getSceneIdFromRow(item.row())
            if item.checkState() == Qt.Checked:
                print(('"%s" Checked' % item.text()))
                self.sceneManager.showSceneObject(sceneId)
            else:
                self.sceneManager.hideSceneObject(sceneId)
            self.slotSetCurrentObjectBasedOnRow(item.row())
            #self.updateAnimationGUI()

        elif item.column() == 2:
            self.changeSkeletonColor(item)

    def slotSetCurrentObjectBasedOnRow(self, row):
        sceneId = self.sceneObjectTableWidget.getSceneIdFromRow(row)
        print("select object",sceneId)
        self.sceneManager.select_object(sceneId)
        self.updateAnimationGUI()

    def loadOBJFile(self):
        filename = QFileDialog.getOpenFileName(self, 'Open File', '.')[0]
        self.sceneManager.scene.object_builder.create_object_from_file("obj", str(filename))

    def loadCOLLADAFile(self):
        filename = QFileDialog.getOpenFileName(self, 'Open File', '.')[0]
        self.sceneManager.scene.object_builder.create_object_from_file("dae", str(filename))

    def loadFBXFile(self):
        filename = QFileDialog.getOpenFileName(self, 'Open File', '.')[0]
        self.sceneManager.scene.object_builder.create_object_from_file("fbx", str(filename))

    def loadRagDoll(self):
        filename = QFileDialog.getOpenFileName(self, 'Open File', '.')[0]
        p = [0, 10, 0]
        scene_object = self.sceneManager.scene.object_builder.create_object_from_file("ragdoll",p, str(filename))
        if scene_object is not None:
            self.sceneManager.scene.addAnimationController(scene_object, "character_animation_recorder")

    def loadMorphableGraphFile(self):
        filename = QFileDialog.getOpenFileName(self, 'Open File', '.')[0]
        self.sceneManager.scene.object_builder.create_object_from_file("zip",str(filename))

    def loadMorphableModelFile(self):
        filename = QFileDialog.getOpenFileName(self, 'Open File', '.')[0]
        self.sceneManager.scene.object_builder.create_object_from_file("mm.json",str(filename))

    def loadMorphableGraphStateMachine(self):
        filename = QFileDialog.getOpenFileName(self, 'Open File', '.')[0]
        self.sceneManager.scene.object_builder.create_object_from_file("mg.zip", str(filename))

    def loadBlendController(self):
        filename = QFileDialog.getOpenFileName(self, 'Open File', '.')[0]
        self.sceneManager.loadBlendController(str(filename))

    def openMotionDBBrowser(self):
        """ https://stackoverflow.com/questions/38309803/pyqt-non-modal-dialog-always-modal """
        if self.motion_db_browser_dialog is None:
            self.motion_db_browser_dialog = MotionDBBrowserDialog(self.sceneManager.scene, parent=self)
        else:
            self.motion_db_browser_dialog.raise_()
            self.motion_db_browser_dialog.activateWindow()

    def synchromizeSkeletonsFromDB(self):
        synchronize_skeletons = SynchronizeSkeletonsWithDBDialog(self)
        synchronize_skeletons.exec_()

    def loadGraphFromDB(self):
        dialog = GraphTableViewDialog(self.sceneManager.scene, self.db_url)
        dialog.exec_()
       
    def uploadMotionsToDB(self):
        controller_list = []
        node_ids = self.getSelectedSceneObjects()
        for node_id in node_ids:
            o = self.sceneManager.scene.getObject(node_id)
            if "animation_controller" in o._components:
                controller_list.append(o._components["animation_controller"])
        if len(controller_list) > 0:
            dialog = UploadMotionDialog(controller_list)
            dialog.exec_()
            if dialog.success:
                print("success")

    def loadHeightMap(self):
        filename = QFileDialog.getOpenFileName(self, 'Open File', '.')[0]
        self.sceneManager.loadHeightMap(str(filename))

    def loadConstraintsFormat(self):
        filename = QFileDialog.getOpenFileName(self, 'Open File', '.')[0]
        self.sceneManager.loadConstraintsFormat(str(filename))

    def loadPointCloud(self):
        filename = QFileDialog.getOpenFileName(self, 'Open File', '.')[0]
        self.sceneManager.scene.object_builder.create_object_from_file("pc", str(filename))


    def loadC3DFile(self):
        filename = QFileDialog.getOpenFileName(self, 'Open File', '.')[0]
        self.sceneManager.scene.object_builder.create_object_from_file("c3d", str(filename))

    def runPythonScript(self):
        filename = QFileDialog.getOpenFileName(self, 'Open File', '.')[0]
        self.sceneManager.runPythonScript(str(filename))

    def loadCustomUnityFormat(self):
        filename = QFileDialog.getOpenFileName(self, 'Open File', '.')[0]
        self.sceneManager.scene.object_builder.create_object_from_file("_m.json", str(filename))

    def changeSkeletonColor(self, item):
        color = QColorDialog.getColor()
        print("set color")
        item.setBackground(color)
        sceneId = self.sceneObjectTableWidget.getSceneIdFromRow(item.row())
        sceneObject = self.sceneManager.scene.getObject(sceneId)
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
        self.sceneManager.startSplineDefinition()

    def startMarkerDefinition(self):
        """ change handling of clicks in the scene to create a marker and the edit its position
        """
        print("start marker definition")
        self.sceneManager.startMarkerDefinition()

    def stopSceneInteraction(self):
        self.sceneManager.stopSceneInteraction()

    def toggleFullScreen(self):
        print("toggle full screen", self._full_screen)
        if self._full_screen:
            self.showNormal()
            self._full_screen = False
        else:
            self.showFullScreen()
            self._full_screen = True

    def setCameraTarget(self):
        camera = self.sceneManager.views[0].graphics_context.camera
        if camera._target is None and self.sceneManager.scene.selected_scene_object is not None:
            camera.setTarget(self.sceneManager.scene.selected_scene_object)
        else:
            camera.removeTarget()

    def toggleEditSceneWidget(self):
        self.sceneManager.scene.toggle_scene_edit_widget()

    def toggleSimulation(self):
        self.sceneManager.scene.toggle_simulation()
    
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
        self.sceneManager.scene.createGroupAnimationController(node_ids)


    def createBlendAnimationController(self):
        node_ids = self.getSelectedSceneObjects()
        self.sceneManager.scene.createBlendAnimationController(node_ids)

    def addArticulatedBody(self):
        node_ids = self.getSelectedSceneObjects()
        if len(node_ids) > 0:
            node_id = node_ids[0]
            self.sceneManager.scene.addArticulatedBody(node_id)

    def saveSimulationState(self):
        self.sceneManager.scene.save_simulation_state()

    def restoreSimulationState(self):
        self.sceneManager.scene.restore_simulation_state()

    def toggleVisibility(self):
        node_ids = self.getSelectedSceneObjects()
        self.sceneManager.scene.toggle_visibility(node_ids)

    def saveScreenshot(self):
        self.sceneManager.views[0].frame_buffer.save_to_file("framebuffer.png")

    def deleteSceneTableEntry(self, node_id):
        for row_idx in range(self.sceneObjectTableWidget.rowCount()):
             if self.sceneObjectTableWidget.getSceneIdFromRow(row_idx) == node_id:
                self.sceneObjectTableWidget.removeRow(row_idx)

    def deleteSelectedObjects(self):
        node_ids = self.getSelectedSceneObjects()
        self.sceneManager.scene.delete_objects(node_ids)
        self.deleteSceneTableEntries(node_ids)

    def deleteSceneTableEntries(self, node_ids):
        for node_id in node_ids:
            self.deleteSceneTableEntry(node_id)

    def keyReleaseEvent(self, event):
        if event.modifiers() & Qt.ControlModifier:
            if event.key() == Qt.Key_Left:
                self.sceneManager.views[0].graphics_context.rotate_left()
            elif event.key() == Qt.Key_Right:
                self.sceneManager.views[0].graphics_context.rotate_right()
            elif event.key() == Qt.Key_Up:
                self.sceneManager.views[0].graphics_context.rotate_up()
            elif event.key() == Qt.Key_Down:
                self.sceneManager.views[0].graphics_context.rotate_down()
        #elif event.modifiers() & Qt.ControlModifier:
            speed = 10
            if event.key() == Qt.Key_A:
                self.sceneManager.views[0].graphics_context.move_horizontally(-speed)
            elif event.key() == Qt.Key_D:
                self.sceneManager.views[0].graphics_context.move_horizontally(speed)
            elif event.key() == Qt.Key_W:
                self.sceneManager.views[0].graphics_context.move_forward(-speed)
            elif event.key() == Qt.Key_S:
                self.sceneManager.views[0].graphics_context.move_forward(speed)
            elif event.key() == Qt.Key_R:
                self.sceneManager.views[0].graphics_context.reset_camera()
        else:
            for id in self.getSelectedSceneObjects():
                o = self.sceneManager.scene.getObject(id)
                o.handle_keyboard_input(str(event.text()))
            self.sceneManager.scene.scene_edit_widget.handle_keyboard_input(event.key())

