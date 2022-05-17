import os
import json
from tool.core.editor_window import EditorWindow
from tool.core.application_manager import ApplicationManager
from tool.constants import CONFIG_FILE
if os.path.isfile(CONFIG_FILE):
    from tool.plugins.database.constants import set_constants_from_file
    set_constants_from_file(CONFIG_FILE)

from tool.plugins.database.gui import MotionDBBrowserDialog, GraphTableViewDialog, UploadMotionDialog, LoginDialog, SynchronizeSkeletonsWithDBDialog
from tool.plugins.database.session_manager import SessionManager
from motion_db_interface import replace_motion_in_db

EditorWindow.add_plugin_object("session_manager", SessionManager)
EditorWindow.add_plugin_object("motion_db_browser_dialog", None)

def open_motion_db_browser():
    """ https://stackoverflow.com/questions/38309803/pyqt-non-modal-dialog-always-modal """
    if EditorWindow.instance.motion_db_browser_dialog is None:
        EditorWindow.instance.motion_db_browser_dialog = MotionDBBrowserDialog(ApplicationManager.instance.scene, parent=EditorWindow.instance)
    else:
        EditorWindow.instance.motion_db_browser_dialog.raise_()
        EditorWindow.instance.motion_db_browser_dialog.activateWindow()

def synchronize_skeletons_from_db():
    synchronize_skeletons = SynchronizeSkeletonsWithDBDialog()
    synchronize_skeletons.exec_()

def load_graph_from_db():
    dialog = GraphTableViewDialog(ApplicationManager.instance.scene)
    dialog.exec_()
    
def upload_motions_to_db():
    controller_list = []
    node_ids = EditorWindow.instance.getSelectedSceneObjects()
    for node_id in node_ids:
        o = ApplicationManager.instance.scene.getObject(node_id)
        if "animation_controller" in o._components:
            controller_list.append(o)
        if "animation_directory_explorer" in o._components:
            controller_list.append(o)
    if len(controller_list) > 0:
        dialog = UploadMotionDialog(controller_list)
        dialog.exec_()
        if dialog.success:
            print("success")

def login_to_server():
    print(EditorWindow.instance.session_manager)
    login_dialog = LoginDialog()
    login_dialog.exec_()
    if login_dialog.success:
        user = login_dialog.user
        password = login_dialog.password
        EditorWindow.instance.session_manager.login(user, password)


actions = [ {"text": "Login",  "function": login_to_server},
            {"text": "Open Motion DB Browser", "function": open_motion_db_browser},
            {"text": "Open Graph Browser", "function" : load_graph_from_db},
            {"text": "Upload Selected Motions", "function": upload_motions_to_db},
            {"text": "Synchronize Skeleton Definitions", "function": synchronize_skeletons_from_db}
        ]
EditorWindow.add_menu("Database", actions)
 
def create_section_dict_from_annotation(annotations):
    motion_sections = dict()
    for label, sections in annotations.items():
        motion_sections[label] = []
        for sub_section in sections:
            sub_section.sort()
            section_dict = dict()
            section_dict["start_idx"] = sub_section[0]
            section_dict["end_idx"] = sub_section[-1]
            motion_sections[label].append(section_dict)
    return motion_sections

def upload_motion_to_db(widget):
    from tool.plugins.database.constants import DB_URL
    node_id = widget._controller.scene_object.node_id
    if "data_base_ids" in widget._controller.scene_object.scene.internal_vars and node_id in widget._controller.scene_object.scene.internal_vars["data_base_ids"]:
        collection, motion_id, is_processed = widget._controller.scene_object.scene.internal_vars["data_base_ids"][node_id]
        bvh_name = widget._controller.scene_object.name
        motion_data = widget._controller.get_json_data()
        skeleton_model_name = str(widget.skeletonModelComboBox.currentText())
        print("replace motion clip with id",motion_id, "and name", bvh_name, collection,is_processed)
        meta_info = dict()
        if len(widget._controller._motion._semantic_annotation) >0:
            meta_info["sections"] = create_section_dict_from_annotation(widget._controller._motion._semantic_annotation)
        if is_processed and widget._controller._motion._time_function is not None:
            meta_info["time_function"] = widget._controller._motion._time_function
        else:
            is_processed = False
        if len(meta_info) > 0:
            meta_info_str = json.dumps(meta_info)
        else:
            meta_info_str = ""
        session = EditorWindow.instance.session_manager.session
        replace_motion_in_db(DB_URL, motion_id, bvh_name, motion_data, collection, skeleton_model_name, meta_info_str, is_processed, session=session)

    else:
        dialog = UploadMotionDialog([widget._controller.scene_object])
        dialog.exec_()
        if dialog.success:
            print("success")

EditorWindow.add_widget_button("animation_player", "UploadMotionToDB", upload_motion_to_db, "horizontalLayout_3")
