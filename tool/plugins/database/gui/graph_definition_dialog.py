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
import threading
from copy import copy
from PySide2.QtWidgets import QDialog, QTreeWidgetItem, QFileDialog, QListWidgetItem
from PySide2.QtCore import Qt
from .layout.graph_definition_dialog_ui import Ui_Dialog
from tool.core.dialogs.enter_name_dialog import EnterNameDialog
from .select_transition_dialog import SelectTransitionDialog
from vis_utils.io import load_json_file
from anim_utils.animation_data.skeleton_models import SKELETON_MODELS
from anim_utils.utilities.db_interface import DB_URL, get_collections_by_parent_id_from_remote_db
try:
    from morphablegraphs.utilities.db_interface import get_model_list_from_remote_db
    from morphablegraphs.motion_model import NODE_TYPE_STANDARD, NODE_TYPE_END, NODE_TYPE_START, NODE_TYPE_IDLE, NODE_TYPE_SINGLE
except:
    pass

class GraphDefinitionDialog(QDialog, Ui_Dialog):
    def __init__(self, db_url, skeleton, graph_data=None, name="",parent=None):
        QDialog.__init__(self, parent)
        Ui_Dialog.setupUi(self, self)
        self.skeleton = skeleton
        self.db_url = db_url
        self.selectButton.clicked.connect(self.slot_accept)
        self.cancelButton.clicked.connect(self.slot_reject)
        self.success = False
        t = threading.Thread(target=self.fill_tree_widget)
        t.start()

        self.graphRootItem = QTreeWidgetItem(self.graphTreeWidget, ["root", "root"])
        self.graphRootItem.setExpanded(True)
        self.data = graph_data
        if self.data is not None:
            if "start_node" not in self.data:
                self.data["start_node"] = ""
            self.init_graph_view()
        else:
            self.data = dict()
            self.data["nodes"] = dict()
            self.data["start_node"] = ""
        self.name = name
        self.nameLineEdit.setText(name)

        self.collectionTreeWidget.itemClicked.connect(self._fill_model_list_from_db)
        self.modelListWidget.itemClicked.connect(self.update_selected_model)
        self.graphTreeWidget.itemClicked.connect(self.update_model_info)


        self.addModelButton.clicked.connect(self.slot_add_primitive)
        self.replaceModelButton.clicked.connect(self.slot_replace_primitive)
        self.addActionButton.clicked.connect(self.slot_add_action)
        self.removeGraphItemButton.clicked.connect(self.slot_remove_graph_item)
        self.setToStartNodeButton.clicked.connect(self.slot_set_to_start_node)
    
        self.addTransitionButton.clicked.connect(self.slot_add_transition)
        self.removeTransitionButton.clicked.connect(self.slot_remove_transition)
        self.fill_node_type_combobox()
        self.nodeTypeComboBox.currentIndexChanged.connect(self.update_node_type)
        self._fill_model_list_from_db()
    
    def init_graph_view(self):
        print("init graph view")
        start_node = str(self.data["start_node"])
        self.startNodeLabel.setText(start_node)
        for action_name in self.data["nodes"]:
            actionItem = QTreeWidgetItem(self.graphRootItem, [action_name, "action"])
            for mp_id in self.data["nodes"][action_name]:
                mp_name = self.data["nodes"][action_name][mp_id]["name"]
                mpItem = QTreeWidgetItem(actionItem, [mp_name, "primitive"])
                mpItem.setData(0, Qt.UserRole, int(mp_id))

    def slot_accept(self):
        self.name = str(self.nameLineEdit.text())
        self.success = self.name != ""
        self.close()

    def slot_reject(self):
        self.close()

    def slot_add_primitive(self):
        selected_action = self.graphTreeWidget.currentItem()
        selected_primitive = self.modelListWidget.currentItem()
        if selected_action is not None and selected_primitive is not None:
            action_name = str(selected_action.text(0))
            type_str = str(selected_action.text(1))
            if type_str == "action":
                mp_id = int(selected_primitive.data(Qt.UserRole))
                mp_name = str(selected_primitive.text())
                mp_key = str(mp_id)
                if mp_key not in self.data["nodes"][action_name]:
                    mpItem = QTreeWidgetItem(selected_action, [mp_name, "primitive"])
                    mpItem.setData(0, Qt.UserRole, mp_id)
                    mp_dict = dict()
                    mp_dict["transitions"] = dict()
                    mp_dict["type"] = "standard"
                    mp_dict["name"] = mp_name
                    self.data["nodes"][action_name][mp_key] = mp_dict
                else:
                    print(mp_name, "already part of action", action_name)
        
    def slot_replace_primitive(self):
        selected_graph_node = self.graphTreeWidget.currentItem()
        selected_primitive = self.modelListWidget.currentItem()
        if selected_graph_node is not None and selected_primitive is not None:
            type_str = str(selected_graph_node.text(1))
            if type_str == "primitive":
                action_node = selected_graph_node.parent()
                action_name = str(action_node.text(0))
                if action_name in self.data["nodes"]:
                    old_mp_id = int(selected_graph_node.data(0, Qt.UserRole))
                    old_mp_name = str(selected_graph_node.text(0))
                    old_key = str(old_mp_id)

                    new_mp_id = int(selected_primitive.data(Qt.UserRole))
                    new_mp_name = str(selected_primitive.text())
                    new_key = str(new_mp_id)
                    if old_key in self.data["nodes"][action_name]:
                        old_transitions = self.data["nodes"][action_name][old_key]["transitions"]
                        old_type = self.data["nodes"][action_name][old_key]["type"]
                        del self.data["nodes"][action_name][old_key]
                        selected_graph_node.setText(0, new_mp_name)
                        selected_graph_node.setData(0, Qt.UserRole, new_mp_id)

                        mp_dict = dict()
                        mp_dict["transitions"] = old_transitions
                        mp_dict["type"] = old_type
                        mp_dict["name"] = new_mp_name
                        self.data["nodes"][action_name][new_key] = mp_dict
                        self.replace_transitions(action_name, old_mp_name, old_mp_id, new_mp_name, new_mp_id)
                        self.update_model_info()
                        print("replaced", old_mp_id, "with", new_mp_id)
                else:
                    print(old_mp_name, "not part of action", action_name)

    def replace_transitions(self, action_name, old_model_name, old_model_id, new_model_name, new_model_id):
        old_key = action_name+":"+old_model_name
        new_key = action_name+":"+new_model_name
        new_entry = dict()
        new_entry["model_name"] = new_model_name
        new_entry["model_id"] = new_model_id
        for a in self.data["nodes"]:
            for mp in self.data["nodes"][a]:
                if old_key in self.data["nodes"][a][mp]["transitions"]:
                    del self.data["nodes"][a][mp]["transitions"][old_key]
                    self.data["nodes"][a][mp]["transitions"][new_key] = copy(new_entry)


    def slot_remove_graph_item(self):
        item = self.graphTreeWidget.currentItem()
        if item is not None: #and item != self.graphRootItem
            parent_item = item.parent()
            item_name = str(item.text(0))
            parent_name = str(parent_item.text(0))
            if parent_name in self.data["nodes"]:
                mp_id = str(item.data(0, Qt.UserRole))
                if mp_id in self.data["nodes"][parent_name]:
                    del self.data["nodes"][parent_name][mp_id]
                
            elif item_name in self.data["nodes"]:
                del self.data["nodes"][item_name]
            parent_item.removeChild(item)

    def slot_set_to_start_node(self):
        item = self.graphTreeWidget.currentItem()
        if item is not None: #and item != self.graphRootItem
            parent_item = item.parent()
            if parent_item is not None:
                item_name = str(item.text(0))
                parent_name = str(parent_item.text(0))
                start_node = [parent_name, item_name]
                start_node_str = str(start_node)
                self.data["start_node"] = [parent_name, item_name]
                self.startNodeLabel.setText(start_node_str)
        


    def slot_add_action(self):
        dialog = EnterNameDialog()
        dialog.exec_()
        if dialog.success:
            action_name = dialog.name
            if action_name not in self.data["nodes"]:
                actionItem = QTreeWidgetItem(self.graphRootItem, [action_name, "action"])
                self.data["nodes"][action_name] = dict()

    def slot_add_transition(self):
        item = self.graphTreeWidget.currentItem()
        if item is not None:
            parent_item = item.parent()
            item_name = str(item.text(0))
            type_name = str(item.text(1))
            parent_name = str(parent_item.text(0))
            if type_name == "primitive":
                mp_id = str(item.data(0, Qt.UserRole))
                if mp_id in self.data["nodes"][parent_name]:
                    dialog = SelectTransitionDialog(self.data)
                    dialog.exec_()
                    if dialog.success and dialog.transition_entry is not None:
                        
                        action_name = str(dialog.transition_entry["action_name"])
                        model_name = str(dialog.transition_entry["model_name"])
                        name = action_name+":"+model_name
                        self.data["nodes"][parent_name][mp_id]["transitions"][name] = dialog.transition_entry
                        self.update_model_info()
        

    def slot_remove_transition(self):
        selected_transition = self.transitionListWidget.currentItem()
        if selected_transition is not None:
            self.transitionListWidget.takeItem(self.transitionListWidget.row(selected_transition))
            transiton_name = str(selected_transition.text())
            selected_item = self.graphTreeWidget.currentItem()
            action_name =  str(selected_item.parent().text(0))
            #mp_name = str(selected_item.text(0))
            mp_id = str(selected_item.data(0, Qt.UserRole))
            del self.data["nodes"][action_name][mp_id]["transitions"][transiton_name]
            self.update_model_info()

    def fill_tree_widget(self, parent=None):
        if parent is None:
            self.collectionTreeWidget.clear()
            self.rootItem = QTreeWidgetItem(self.collectionTreeWidget, ["root", "root"])
            self.rootItem.setExpanded(True)
            # root collection has id 0
            parent_id = 0
            parent_item = self.rootItem
            self.rootItem.setData(0, Qt.UserRole, parent_id)
        else:
            parent_id = parent[1]
            parent_item = parent[0]

        collection_list = get_collections_by_parent_id_from_remote_db(self.db_url, parent_id)
        for col in collection_list:
            colItem = QTreeWidgetItem(parent_item, [col[1], col[2]])
            colItem.setData(0, Qt.UserRole, col[0])
            self.fill_tree_widget((colItem, col[0]))

    def get_collection(self):
        colItem = self.collectionTreeWidget.currentItem()
        if colItem is None:
            return
        return int(colItem.data(0, Qt.UserRole)),  str(colItem.text(0)), str(colItem.text(1))


    def _fill_model_list_from_db(self, idx=None):
        self.modelListWidget.clear()
        col = self.get_collection()
        if col is None:
            return
        c_id, c_name, c_type = col
        model_list = get_model_list_from_remote_db(self.db_url, c_id, self.skeleton)
        print("model list", model_list)
        if model_list is None:
            return
        for node_id, name in model_list:
            item = QListWidgetItem()
            item.setText(name)
            item.setData(Qt.UserRole, node_id)
            self.modelListWidget.addItem(item)

        self.update_selected_model()
        
    def update_selected_model(self):
        selected_action = self.graphTreeWidget.currentItem()
        selected_primitive = self.modelListWidget.currentItem()
        if selected_action is not None and selected_primitive is not None:
            self.selectedModelLabel.setText(selected_primitive.text())
        else:
            self.selectedModelLabel.setText("None")

    def update_model_info(self, idx=None):
        self.transitionListWidget.clear()
        self.nodeTypeComboBox.setCurrentIndex(0)
        selected_item = self.graphTreeWidget.currentItem()
        if selected_item is None:
            return
        item_type = str(selected_item.text(1))
        if item_type != "primitive":
            return
        item_name = str(selected_item.text(0))
        mp_id = str(selected_item.data(0, Qt.UserRole))
        action_name = str(selected_item.parent().text(0))
        if action_name not in self.data["nodes"]:
            return
        if mp_id not in self.data["nodes"][action_name]:
            print("mp id  not in nodes", mp_id)
            return
        for transiton_key in self.data["nodes"][action_name][mp_id]["transitions"]:
            item = QListWidgetItem()
            item.setText(transiton_key)
            self.transitionListWidget.addItem(item)
        
        node_type = self.data["nodes"][action_name][mp_id]["type"]
        index = self.nodeTypeComboBox.findText(node_type, Qt.MatchFixedString)
        if index >= 0:
            self.nodeTypeComboBox.setCurrentIndex(index)
        print("node_type", node_type, index, mp_id)



    def fill_node_type_combobox(self):
        self.nodeTypeComboBox.clear()
        self.nodeTypeComboBox.addItem("", 0)
        self.nodeTypeComboBox.addItem("standard", 1)
        self.nodeTypeComboBox.addItem("start", 2)
        self.nodeTypeComboBox.addItem("end", 3)
        self.nodeTypeComboBox.addItem("single", 4)
        self.nodeTypeComboBox.addItem("idle", 5)

    def update_node_type(self):
        selected_item = self.graphTreeWidget.currentItem()
        if selected_item is None:
            return
        item_type = str(selected_item.text(1))
        if item_type != "primitive":
            return
        item_name = str(selected_item.text(0))
        mp_id = str(selected_item.data(0, Qt.UserRole))
        action_name = str(selected_item.parent().text(0))
        if action_name not in self.data["nodes"]:
            return
        if mp_id not in self.data["nodes"][action_name]:
            return
        node_type = str(self.nodeTypeComboBox.currentText())
        if node_type != "":
            self.data["nodes"][action_name][mp_id]["type"] = node_type
            print("set node type", item_name, node_type)
