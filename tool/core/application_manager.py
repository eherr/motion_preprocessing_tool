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
# -*- coding: utf-8 -*-
#===============================================================================
# author: Erik Herrmann (DFKI GmbH, FB: Agenten und Simulierte Realit�t)
# last update: 15.1.2014
#===============================================================================
import sys
import time
import math
from PySide2.QtCore import QObject, QTimer, Qt
from PySignal import Signal
from vis_utils.scene.editor_scene import EditorScene
from OpenGL.GL import *
from vis_utils.scene.scene_interaction import SceneInteraction, INTERACTION_DEFINE_SPLINE, INTERACTION_NONE, INTERACTION_DEFINE_MARKER
from vis_utils import constants
if constants.activate_simulation:
    from physics_utils.sim import SimWorld

class ApplicationManager(QObject):
    """ main application logic
    controls the updates to the scene done by the main thread via a Qt.QTimer event
    holds the reference to the server thread
    "singleton class" by calling convention #http://stackoverflow.com/questions/31875/is-there-a-simple-elegant-way-to-define-singletons-in-python/33201#33201
    """
    instance = None

    added_scene_object = Signal()
    updated_animation_frame = Signal()
    reached_end_of_animation = Signal()
    deleted_scene_object = Signal()
    update_scene_object = Signal()

    def __init__(self, visualize=True, graphics_widget=None):
        if ApplicationManager.instance == None:
            ApplicationManager.instance = self
            QObject.__init__(self)
            self.visualize = visualize
            self.frames = 0
            self.fps = 60.0
            self.sim_dt = 1/30
            self.interval = 1.0 / self.fps
            self.last_time = time.perf_counter()
            self.last_fps_update_time = self.last_time
            self.views = list()
            self.drawDebugVisualization = True
            self.statusBar = None
            self.scene = None
            self.graphics_widget = graphics_widget
            self.interaction = SceneInteraction()
            self.timer = QTimer()
            self.timer.timeout.connect(self.update)
            self.timer.start(0)
            self.timer.setInterval(self.interval*1000)

    def toggle_renderer(self):
        self.use_color_renderer = not self.use_color_renderer
        print("use color picking renderer")

    def add_view(self, view):
        """adds view to list of views whose paint function is called by the function self.update()
        """
        self.views.append(view)
       
    def init_scenes(self):
        sim = None
        if constants.activate_simulation:
            sim_settings = dict()
            sim_settings["auto_disable"] = False
            sim_settings["engine"] = "ode"
            #sim_settings["engine"] = "bullet"
            sim_settings["add_ground"] = True
            sim = SimWorld(**sim_settings)
        
        self.scene = EditorScene(self.visualize, sim)
        self.scene.added_scene_object.connect(self.relayAddedSceneObject)
        self.scene.reached_end_of_animation.connect(self.relayEndOfAnimation)
        self.scene.deleted_scene_object.connect(self.relayDeletedSceneObject)
        self.scene.update_scene_object.connect(self.relayUpdateSceneObject)
        #self.connect(self.scene, QtCore.SIGNAL('displayError(QString)'),self.relayShowErrorMessage)
        self.scene.updated_animation_frame.connect(self.relayUpdateAnimationFrame)
        self.interaction.set_scene(self.scene)
        for view in self.views:
            view.mouse_click.connect(self.on_mouse_click)
            view.mouse_move.connect(self.on_mouse_move)
            view.mouse_release.connect(self.on_mouse_release)
        print("init scene")

    def on_mouse_click(self, event, ray_start, ray_dir, pos, node_id):
        self.interaction.handleMouseClick(event, ray_start, ray_dir, pos)
        if event.button() == Qt.LeftButton:
            self.select_object(node_id, (ray_start, ray_dir))
            self.update_scene_object.emit(node_id)
        
    def on_mouse_release(self, event):
        print("mouse release")
        self.scene.deactivate_axis()

    def on_mouse_move(self, event, last_mouse_pos, cam_pos, cam_ray):
        self.scene.handle_mouse_movement(cam_pos, cam_ray)
        
    def update(self):
        """ main loop of the application
        """
        dt = self.update_delta_time()
        if self.scene is not None:
            # from locotest
            n_steps = int(math.ceil(self.interval / self.sim_dt))
            self.scene.before_update(dt)
            for i in range(0, n_steps):
                self.scene.sim_update(self.sim_dt)
            self.scene.update(dt)
            self.scene.after_update(dt)

        for view in self.views:
            view.graphics_context.update(dt)
            self.drawOnView(view)

    def update_scene(self, scene, dt):
        n_steps = int(math.ceil(self.interval / self.sim_dt))
        scene.before_update(dt)
        for i in range(0, n_steps):
            scene.sim_update(self.sim_dt)
        scene.update(dt)
        scene.after_update(dt)

    def draw(self, projection, view):
        return

    def drawOnView(self,view):
        """ draw current scene on the given view
        (note before calling this function the context of the view has to be set as current using makeCurrent() and afterwards the doubble buffer has to swapped to display the current frame swapBuffers())
        """
        view.makeCurrent()
        view.graphics_context.render(self.scene)
        view.swapBuffers()

    def update_delta_time(self):
        t = time.perf_counter()
        dt = t - self.last_time
        self.last_time = t
        if t - self.last_fps_update_time > 1.0:
            self.fps = self.frames
            self.frames = 0
            self.last_fps_update_time = t
        self.update_status_bar("FPS " + str(round(self.fps)))
        self.frames += 1
        return dt

    def update_status_bar(self, message):
        if self.statusBar != None:
            self.statusBar.showMessage(message)
    
    def getDisplayedScene(self):
        return self.scene
    
    def select_object(self, sceneId, ray=None):
        return self.scene.select_object(sceneId, ray)

    def getSelectedObject(self):
        return self.scene.getSelectedObject()

    def getObject(self, sceneId):
        return self.scene.getObject(sceneId)

    def showSceneObject(self, sceneId):
        self.scene.showSceneObject(sceneId)
        
    def hideSceneObject(self, sceneId):
        self.scene.hideSceneObject(sceneId)

    def runPythonScript(self, filename):
        self.scene.runPythonScript(filename)

    def startSplineDefinition(self):
        self.interaction.set_mode(INTERACTION_DEFINE_SPLINE)

    def stopSceneInteraction(self):
        self.interaction.set_mode(INTERACTION_NONE)

    def startMarkerDefinition(self):
        self.interaction.set_mode(INTERACTION_DEFINE_MARKER)

    def createBoxObject(self):
        self.interaction.set_mode("box")

    def createSphereObject(self):
        self.interaction.set_mode("sphere")

    def createCapsuleObject(self):
        self.interaction.set_mode("capsule")

    def createLinkedCapsuleObject(self):
        self.interaction.set_mode("linked_capsule")

    def createRagDoll(self):
        self.interaction.set_mode("ragdoll")


    #======================================================================================================
    # SCENE SIGNAL RELAYS
    #======================================================================================================

    def relayAddedSceneObject(self, sceneId):
        sceneObject = self.scene.getObject(sceneId)
        if sceneObject is not None:
            self.added_scene_object.emit(sceneId, sceneObject.name)
        else:
            self.added_scene_object.emit(None, None)

    def relayUpdateSceneObject(self, sceneId):
        self.update_scene_object.emit(sceneId)
   
    def relayEndOfAnimation(self,animationIndex,loop):
        self.reached_end_of_animation.emit(animationIndex,loop)
        
    def relayUpdateAnimationFrame(self,frameNumber):
        self.updated_animation_frame.emit(frameNumber)

    def relayDeletedSceneObject(self, node_id):
        self.deleted_scene_object.emit(node_id)

    def deinitialize(self):
        self.timer.stop()

    def loadFile(self, path):
        if self.scene.object_builder.load_file(path):
            return
        elif path.endswith(".py"):
            self.scene.runPythonScript(path)
        else:
            print("Could not load", path)





