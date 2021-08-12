import os
from tool.core.editor_window import EditorWindow
from tool.core.application_manager import ApplicationManager
from tool.constants import CONFIG_FILE
if os.path.isfile(CONFIG_FILE):
    from tool.plugins.database.constants import set_constants_from_file
    set_constants_from_file(CONFIG_FILE)


from tool.plugins.database.gui import MotionDBBrowserDialog, GraphTableViewDialog, UploadMotionDialog, LoginDialog, SynchronizeSkeletonsWithDBDialog
from tool.plugins.database.session_manager import SessionManager

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
            controller_list.append(o._components["animation_controller"])
    if len(controller_list) > 0:
        dialog = UploadMotionDialog(controller_list)
        dialog.exec_()
        if dialog.success:
            print("success")

def login_to_server():
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
