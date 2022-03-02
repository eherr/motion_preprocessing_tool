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
from PySide2.QtCore import Qt, QFile
from PySide2.QtWidgets import QMainWindow, QMessageBox, QAction, QFileDialog, QColorDialog, QToolButton
from tool import constants
from tool.core.layout.mainwindow_ui import Ui_MainWindow
from tool.core.widget_manager import WidgetManager
from tool.core.application_manager import ApplicationManager


class EditorWindow(QMainWindow, Ui_MainWindow):
    instance = None
    menu_actions = collections.OrderedDict()
    plugin_object_constructors = collections.OrderedDict()
    widget_buttons = collections.OrderedDict()
    def __init__(self):
        if EditorWindow.instance is None:
            EditorWindow.instance = self
            QMainWindow.__init__(self)
            Ui_MainWindow.setupUi(self, self)
            self.animationViewer.resize(860, 640)
            self.animationViewer.statusBar = self.statusBar
            self._full_screen = False
            self.app_manager = ApplicationManager(True, self.animationViewer)
            self.animationViewer.init_opengl.connect(self.app_manager.init_scenes)
            self.app_manager.add_view(self.animationViewer)
            self.app_manager.statusBar = self.statusBar
            self.add_actions_to_menu("File",  [{"text": "Quit", "function": self.close, "status_tip": 'Exit application'}])
            self.init_menus()
            self.init_slots()
            self.selectedJointName = ""
            self.object_widgets = dict()
            self.init_widgets()
            for name, constructor in self.plugin_object_constructors.items():
                if constructor is not None:
                    setattr(self, name, constructor())
                else:
                    setattr(self, name, None)

    def closeEvent(self, event):
        print("Close window")
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
            if key in self.widget_buttons:
                for (name, func, layout_name) in self.widget_buttons[key]:
                    new_button = QToolButton(self.object_widgets[key])
                    new_button.setObjectName(name)
                    action = QAction(name, self.object_widgets[key])
                    action.triggered.connect(partial(func,self.object_widgets[key]))
                    new_button.setDefaultAction(action)
                    setattr(self.object_widgets[key], name, new_button)
                    if layout_name is not None:
                        layout = getattr(self.object_widgets[key], layout_name)
                        layout.addWidget(new_button)

    def init_menus(self):
        count = 0
        self.menus = dict()
        for action_type in self.menu_actions:
            self.menus[action_type] = self.menuBar.addMenu("&"+action_type)
            for action_desc in self.menu_actions[action_type]:
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

    def getSelectedSceneObjects(self):
        node_ids = []
        for row_idx in range(self.sceneObjectTableWidget.rowCount()):
            idx_cell = self.sceneObjectTableWidget.item(row_idx, 0)
            name_cell = self.sceneObjectTableWidget.item(row_idx, 1)
            if idx_cell.isSelected() or name_cell.isSelected():
                node_id = self.sceneObjectTableWidget.getSceneIdFromRow(row_idx)
                node_ids.append(node_id)
        return node_ids

    def delete_scene_table_entry(self, node_id):
        for row_idx in range(self.sceneObjectTableWidget.rowCount()):
             if self.sceneObjectTableWidget.getSceneIdFromRow(row_idx) == node_id:
                self.sceneObjectTableWidget.removeRow(row_idx)

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

    @classmethod
    def add_menu(cls, name, actions):
        cls.menu_actions[name] = actions

    @classmethod
    def add_actions_to_menu(cls, name, actions):
        cls.menu_actions[name] += actions

    @classmethod
    def add_plugin_object(cls, name, constructor):
        cls.plugin_object_constructors[name] = constructor

    @classmethod
    def add_widget_button(cls, widget_name, name, function, layout_name=None):
        if widget_name not in cls.widget_buttons:
            cls.widget_buttons[widget_name] = []
        cls.widget_buttons[widget_name] += [(name, function, layout_name)]

    def toggle_full_screen(self):
        print("toggle full screen", self._full_screen)
        if self._full_screen:
            self.showNormal()
            self._full_screen = False
        else:
            self.showFullScreen()
            self._full_screen = True


def open_file_dialog(filetype):
    filename = QFileDialog.getOpenFileName(EditorWindow.instance, 'Open File', '.')[0]
    ApplicationManager.instance.scene.object_builder.create_object_from_file(filetype, str(filename))


def load_animation_directory():
    directory = QFileDialog.getExistingDirectory(EditorWindow.instance, "Select Directory")
    directory = str(directory)
    if os.path.isdir(directory):
        ApplicationManager.instance.scene.object_builder.create_object("animation_directory_explorer", directory, "bvh")


def load_heightmap(self):
    filename = QFileDialog.getOpenFileName(EditorWindow.instance, 'Open File', '.')[0]
    ApplicationManager.instance.loadHeightMap(str(filename))

def load_ragdoll():
    filename = QFileDialog.getOpenFileName(EditorWindow.instance, 'Open File', '.')[0]
    p = [0, 10, 0]
    scene_object = ApplicationManager.instance.scene.object_builder.create_object_from_file("ragdoll",p, str(filename))
    if scene_object is not None:
        ApplicationManager.instance.scene.addAnimationController(scene_object, "character_animation_recorder")


def load_constraints_format(self):
    filename = QFileDialog.getOpenFileName(self, 'Open File', '.')[0]
    ApplicationManager.instance.loadConstraintsFormat(str(filename))

def load_blender_controller():
    filename = QFileDialog.getOpenFileName(EditorWindow.instance, 'Open File', '.')[0]
    ApplicationManager.instance.loadBlendController(str(filename))

def create_group_animation_controller():
    node_ids = EditorWindow.instance.getSelectedSceneObjects()
    ApplicationManager.instance.scene.createGroupAnimationController(node_ids)


def start_spline_definition():
    """ change handling of clicks in the scene to create a spline control points
    """
    print("start spline definition")
    ApplicationManager.instance.startSplineDefinition()

def start_marker_definition():
    """ change handling of clicks in the scene to create a marker and the edit its position
    """
    print("start marker definition")
    ApplicationManager.instance.startMarkerDefinition()

def stop_scene_interaction():
    ApplicationManager.instance.stopSceneInteraction()


def toggle_edit_scene_widget():
    ApplicationManager.instance.scene.toggle_scene_edit_widget()

def toggle_simulation():
    ApplicationManager.instance.scene.toggle_simulation()


def delete_selected_objects():
    node_ids = EditorWindow.instance.getSelectedSceneObjects()
    ApplicationManager.instance.scene.delete_objects(node_ids)
    EditorWindow.instance.deleteSceneTableEntries(node_ids)


def run_python_script():
    filename = QFileDialog.getOpenFileName(EditorWindow.instance, 'Open File', '.')[0]
    ApplicationManager.instance.runPythonScript(str(filename))

def save_simulation_state():
    ApplicationManager.instance.scene.save_simulation_state()

def restore_simulation_state():
    ApplicationManager.instance.scene.restore_simulation_state()

def add_articulated_body():
    node_ids = EditorWindow.instance.getSelectedSceneObjects()
    if len(node_ids) > 0:
        node_id = node_ids[0]
        ApplicationManager.instance.scene.add_articulated_body(node_id)

def toggle_visibility():
    node_ids = EditorWindow.instance.getSelectedSceneObjects()
    ApplicationManager.instance.scene.toggle_visibility(node_ids)

def save_screen_shot():
    ApplicationManager.instance.views[0].frame_buffer.save_to_file("framebuffer.png")

def toggle_full_screen():
    EditorWindow.instance.toggle_full_screen()

def set_camera_target():
    camera = ApplicationManager.instance.views[0].graphics_context.camera
    if camera._target is None and ApplicationManager.instance.scene.selected_scene_object is not None:
        camera.setTarget(ApplicationManager.instance.scene.selected_scene_object)
    else:
        camera.removeTarget()

EditorWindow.add_menu("File", [
        {"text": "Load BVH File",  "function": partial(open_file_dialog, "bvh")},
        {"text": "Load BVH files from Directory", "function": load_animation_directory},
        {"text": "Load ASF File",  "function":  partial(open_file_dialog, "asf")},
        {"text": "Load OBJ file", "function": partial(open_file_dialog, "obj")},
        {"text": "Load DAE file", "function": partial(open_file_dialog, "dae")},
        {"text": "Load FBX file", "function": partial(open_file_dialog, "fbx")},
        {"text": "Load Ragdoll File",  "function": load_ragdoll},
        {"text": "Load Blend Controller File", "function": load_blender_controller},
        {"text": "Load Height Map", "function": load_heightmap},
        {"text": "Load Constraints Format", "function": load_constraints_format},
        {"text": "Load Point Cloud", "function": partial(open_file_dialog, "pc")},
        {"text": "Load C3D File", "function": partial(open_file_dialog, "c3d")},
        {"text": "Run Python Script", "function": run_python_script},
        {"text": "Load Custom Unity Format", "function": partial(open_file_dialog, "_m.json")}
        ])

create_menu_actions = [
        {"text": "spline", "function": start_spline_definition},
        {"text": "marker", "short_cut": "O","function": start_marker_definition},
        {"text": "Stop editing", "short_cut": "E", "function": stop_scene_interaction},
          {"text": "Group Animation Controller", "function": create_group_animation_controller}
        ]
if constants.vis_constants.activate_simulation:
        
    def create_physics_object(object_type):
        if object_type == "capsule":
            ApplicationManager.instance.createCapsuleObject()
        elif object_type == "box":
            ApplicationManager.instance.createBoxObject()
        elif object_type == "sphere":
            ApplicationManager.instance.createSphereObject()
        elif object_type == "linked_capsule":
            ApplicationManager.instance.createLinkedCapsuleObject()
        elif object_type == "ragdoll":
            ApplicationManager.instance.createRagDoll()

    create_menu_actions += [{"text": "Articulated Body", "function": add_articulated_body},
                                    {"text": "ode capsule object", "function": partial(create_physics_object, "capsule")},
                                    {"text": "ode box object", "function": partial(create_physics_object, "box")},
                                    {"text": "ode sphere object", "function": partial(create_physics_object, "sphere")},
                                    {"text": "ode linked capsule object", "function": partial(create_physics_object, "linked_capsule")},
                                    {"text": "RagDoll", "function": partial(create_physics_object, "ragdoll")}]
EditorWindow.add_menu("Create", create_menu_actions)
EditorWindow.add_menu("View", [
        {"text": "Set selected to camera target", "short_cut": "Ctrl+T", "function": set_camera_target},
        {"text": "Toggle full screen","short_cut": "F11", "function": toggle_full_screen},
        {"text": "Hide/Show Selected", "short_cut": "Ctrl+H", "function": toggle_visibility},
        {"text": "Save Screenshot", "short_cut": "Ctrl+E", "function": save_screen_shot}
])

scene_menu_actions =  [{"text": "Toggle scene widget", "function": toggle_edit_scene_widget},
                        {"text": "Delete selected objects", "short_cut": "Del", "function": delete_selected_objects}]
if constants.vis_constants.activate_simulation:
    scene_menu_actions += [{"text": "Toggle simulation", "short_cut": "P", "function": toggle_simulation},
                                {"text": "Save simulation state","function": save_simulation_state},
                                {"text": "Restore simulation state", "function": restore_simulation_state}]

EditorWindow.add_menu("Scene", scene_menu_actions)
