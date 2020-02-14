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
# last update: 24.1.2014
#===============================================================================

from PySide2.QtCore import Signal, QPointF, Qt
from PySide2 import QtOpenGL
from PySide2.QtWidgets import QApplication
from OpenGL.GL import *
import numpy as np
from vis_utils import constants
from vis_utils.graphics import camera3d
from vis_utils.graphics.graphics_context import GraphicsContext


def getIfromRGB(rgb):
    red = int(rgb[0]*255)
    green = int(rgb[1]*255)
    blue = int(rgb[2]*255)
    #print red, green, blue
    RGBint = (red<<16) + (green<<8) + blue
    return RGBint


class SceneViewerWidget(QtOpenGL.QGLWidget):
    """ Widget containing OpenGL context. 
        To the method paintGL can be implemented to update the canvas.
        Alternatively makeCurrent() and swapBuffers() can be called from outside.
        sources: http://doc.qt.digia.com/qq/qq06-glimpsing.html#writingmultithreadedglapplications
                http://nullege.com/codes/show/src@p@y@PyQt4-HEAD@examples@opengl@overpainting.py/185/PyQt4.QtOpenGL.QGLWidget.makeCurrent
    """
    init_opengl = Signal(name='initializeGL')
    mouse_move = Signal(object, object, object, object, name='mouseMove')
    mouse_click = Signal(object, object, object, object, int, name='mouseClick')
    mouse_release = Signal(object, name='mouseClick')
    dropped_files = Signal(object, name='droppeFiles')

    def __init__(self, parent=None, shareWidget=None, size=None, use_frame_buffer=constants.use_frame_buffer):
        super(SceneViewerWidget, self).__init__( shareWidget=shareWidget)
        self.glWidth = self.width()
        self.glHeight = self.height()
        self.setAcceptDrops(True)
        self.setMouseTracking(True)
        self.setAutoBufferSwap(False)
        self.parent = parent
        self.movement_scale = 0.1
        self.rotation_scale = 0.1
        self.zoom_factor = 0.1
        self._full_screen = False
        
        self.lastMousePosition = QPointF()
        self.statusBar = None
        
        self.clickRayCollision = None
        self.clickRayStart = np.array([0,0,0])
        self.clickRayEnd = np.array([0,0,0])
        self.enable_mouse_interaction = True
        self.use_frame_buffer = use_frame_buffer
        self.graphics_context = None
        self.size = size
        self.initialized = False

    def initializeGL(self):
        self.initialized = True
        w = 800
        h = 600
        if self.size is not None:
            w = self.size[0]
            h = self.size[1]
        #self.qglClearColor(QtGui.QColor(255, 255,  255))
        
        self.makeCurrent()
        self.graphics_context = GraphicsContext(w, h, use_frame_buffer=self.use_frame_buffer)
        self.init_opengl.emit()

    def keyReleaseEvent(self, event):
        if event.key() == Qt.Key_F:
            self._toggleFullScreen()

    def mousePressEvent(self,event):
        x, y = event.x(), event.y()
        self.lastMousePosition = QPointF(x, y)
        if not self.enable_mouse_interaction:
            return
        rayStart, rayDir = self.getRayFromClick(x, y)
        p = self.graphics_context.get_position_from_click(x, y)
        object_id = -1
        if self.use_frame_buffer:
            object_id = self.graphics_context.get_id_from_color_buffer(x,y)
        if object_id <= 0:
            object_id = -1
        self.mouse_click.emit(event, rayStart, rayDir, p, object_id)

    def mouseReleaseEvent(self,event):
        self.mouse_release.emit(event)

    def get_ray_from_pixel(self, pos_2d):
        """" https://github.com/ddiakopoulos/tinygizmo/blob/master/tiny-gizmo-example/util.hpp"""
        width = self.glWidth
        height = self.glHeight 
        ndc_X = ((2.0*pos_2d[0])/width)-1.0
        ndc_Y = 1.0 - ((2.0*pos_2d[1])/height)
        #x = 2 * (pos_2d[0] - viewport.x0) / self.width - 1
        #y = 1 - 2 * (pos_2d[1] - viewport.y0) / self.height

        pm = self.graphics_context.camera.get_projection_matrix()
        vm = self.graphics_context.camera.get_view_matrix()
        pv = np.dot(pm, vm)
        pv = np.linalg.inv(pv)
        return

    def mouseMoveEvent(self, event):
       """pass event along to scenes before changing the own state"""
       #cam_pos = self.graphics_context.camera.get_world_position()
       #pos_2d = [event.x(),event.y()]
       #ray_direction = self.get_ray_from_pixel(pos_2d)
       cam_pos, cam_ray = self.getRayFromClick(event.x(), event.y())
       cam_pos = cam_pos[:3]
       cam_ray = cam_ray[:3]
       self.mouse_move.emit(event, self.lastMousePosition, cam_pos, cam_ray)
       modifiers = QApplication.keyboardModifiers()
       newPosition = QPointF(event.x(),event.y())
       diff = newPosition - self.lastMousePosition
       self.lastMousePosition = newPosition
       if event.buttons() & Qt.MiddleButton and modifiers != Qt.ShiftModifier:
            # set rotation
           self.graphics_context.camera.updateRotationMatrix(self.graphics_context.camera.pitch + diff.y() * self.rotation_scale, self.graphics_context.camera.yaw + diff.x() * self.rotation_scale)
           self.showMessageOnStatusBar("rotation x: "+str(self.graphics_context.camera.yaw)+", rotation y: "+str(self.graphics_context.camera.pitch))
       elif event.buttons() & Qt.MiddleButton and modifiers == Qt.ShiftModifier:
            # set position
            self.graphics_context.camera.moveHorizontally(-diff.x() * self.movement_scale * 2)
            self.graphics_context.camera.position[1] -= diff.y()*self.movement_scale * 2#/(10*self.zoom_factor)
            #self.showMessageOnStatusBar("position x: "+str(self.camera.position[0])+", position y: "+str(self.camera.position[1]) )
        
    def wheelEvent(self, event):
        delta = event.angleDelta().y()*self.zoom_factor
        self.graphics_context.camera.zoom += delta
        
    def resizeGL(self, width, height):
        if height == 0:
            height = 1
        self.glWidth = width
        self.glHeight = height
        #self.camera.set_orthographic_matrix(0, float(width), 0, float(height), -0.1, 10000.0)
        print("resize", width, height)
        if self.graphics_context is not None:
            self.graphics_context.resize(width, height)
        
    def showMessageOnStatusBar(self, message):
        if self.statusBar != None:
            self.statusBar.showMessage(message)

    def getRayFromClick(self, x, y):
        """ copied from http://antongerdelan.net/opengl/raycasting.html and translated into Python
        returns origin and direction of the ray
        """
        # use camera position as origin of the ray
        ray_start = self.graphics_context.camera.get_world_position()

        # transform window X and Y into normalized device coordinates range [-1:1]
        width = self.glWidth
        height = self.glHeight
        ndc_X = ((2.0*x)/width)-1.0
        ndc_Y = 1.0 - ((2.0*y)/height)

        # convert to clipping coordinates range [-1:1, -1:1, -1:1, -1:1]
        cc = [0,0,0,0]
        cc[0] = ndc_X
        cc[1] = ndc_Y
        cc[2] = -1.0  # let ray point forward in negative -z direction
        cc[3] = 1.0

        # unproject x y part of clipping coordinates
        ray_eye = np.dot(self.graphics_context.camera.get_inv_projection_matrix().T, cc)
        ray_eye[2] = -1.0
        ray_eye[3] = 0.0

        # get world coordinates
        ray_world = np.dot(self.graphics_context.camera.get_inv_view_matrix().T, ray_eye)
        ray_world /= np.linalg.norm(ray_world)
        #print("ray world", ray_start, ray_world)
        return np.array([ray_start[0], ray_start[1], ray_start[2], 0]), ray_world

    def printOpenGLContext(self, ctxt):
        """#http://nullege.com/codes/show/src@p@y@pyformex-0.8.6@pyformex@gui@viewport.py/161/PyQt4.QtOpenGL.QGLContext.currentContext"""
        if ctxt:
            print("context is valid: %d" % ctxt.isValid())
            print("context is sharing: %d" % ctxt.isSharing())
        else:
            print("No OpenGL context yet!")

    ############################################################################################################
    #handle drag and drop events
    #http://stackoverflow.com/questions/22543644/how-to-drag-and-drop-from-one-qlistwidget-to-another
    
    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls:
            event.accept()
        else:
            event.ignore()
 
    def dragMoveEvent(self, event):
        if event.mimeData().hasUrls:
            event.setDropAction(Qt.CopyAction)
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        if event.mimeData().hasUrls:
            event.setDropAction(Qt.CopyAction)
            event.accept()
            links = []
            for url in event.mimeData().urls():
                links.append(str(url.toLocalFile()))
            url = event.mimeData().urls()[0]   # get first url
            print("drop", url)
            self.dropped_files.emit(links)
        else:
            event.ignore()

