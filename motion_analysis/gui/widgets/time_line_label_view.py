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
from PySide2.QtCore import QRectF, QPointF, Qt, QSizeF
from PySide2.QtWidgets import  QGraphicsItem, QGraphicsView, QGraphicsScene
from PySide2.QtGui import  QColor, QBrush, QFont, QTransform
drag_mode = QGraphicsView.DragMode.RubberBandDrag # 1
transform_anchor = QGraphicsView.ViewportAnchor.NoAnchor # 0
blue = QColor()
blue.setBlue(255)
blue.setAlpha(255)
red = QColor()
red.setRed(255)
red.setAlpha(255)
green = QColor()
green.setGreen(255)
green.setAlpha(255)
black = QColor()
black.setAlpha(255)
grey = QColor()
grey.setRed(100)
grey.setBlue(100)
grey.setGreen(100)
grey.setAlpha(255)


class FrameIndicator(QGraphicsItem):
    def __init__(self, size, frame_width, offset,y, color=red, parent=None):
        super(FrameIndicator, self).__init__(parent)
        self._size = size
        self._frame_width = frame_width
        self.y = y
        self.offset = offset
        self.view_rect = QRectF()
        self.setFrame(0)
        self.color = color

    def paint(self, painter, styleoptions, parent=None):
        brush = QBrush()
        brush.setColor(self.color)
        painter.setBrush(self.color)
        painter.drawRect(self._bounding_rect)

    def boundingRect(self):
        return self._bounding_rect

    def setFrame(self, idx):
        self.prepareGeometryChange()
        x = idx*self._frame_width + self.offset
        self._bounding_rect = QRectF()
        self._bounding_rect.setX(x)
        self._bounding_rect.setY(self.y)
        self._bounding_rect.setSize(self._size)


class TimeLine(QGraphicsItem):
    def __init__(self, label, indices, pos, length, height, label_width, frame_width, color, parent=None):
        super(TimeLine, self).__init__(parent)
        self._pos = pos
        self._length = length
        self._height = height
        self.label = label
        self._label_width = label_width
        self._indices = indices
        self.frame_width = frame_width

        size = QSizeF()
        size.setHeight(self._height)
        size.setWidth(self._length)
        self._bounding_rect = QRectF()
        self._bounding_rect.setX(self._pos.x())
        self._bounding_rect.setY(self._pos.y())
        self._bounding_rect.setSize(size)
        self._tpos = QPointF(pos)
        self._tpos.setY(pos.y()+self._height)
        self.color = QColor()
        self.color.setRed(color[0] * 255)
        self.color.setGreen(color[1]* 255)
        self.color.setBlue(color[2] * 255)
        self.color.setAlpha(255)


    def paint(self, painter, styleoptions, parent=None):
        #brush = QtGui.QBrush()
        #brush.setColor(blue)
        painter.setBrush(self.color)
        for idx in self._indices:
            x = self._pos.x() + self._label_width + self.frame_width * idx
            painter.drawRect(x, self._pos.y(), self.frame_width, self._height)

        #brush = QtGui.QBrush()
        #brush.setColor(red)
        painter.setBrush(black)
        painter.drawLine(self._pos.x(), self._pos.y(), self._pos.x()+self._length, self._pos.y())
        painter.setPen(black)
        painter.setFont(QFont("Arial", 10))
        painter.drawText(self._tpos,self.label)# QtCore.Qt.AlignCenter,

    def boundingRect(self):
        return self._bounding_rect


class TimeLineLabelView(QGraphicsView):
    def __init__(self, parent=None):
        super(TimeLineLabelView, self).__init__(parent)
        self.x = 0
        self.y = 0
        self.m_originX = 0
        self.m_originY = 0
        self.label_height = 10
        self.frame_width = 10
        self.time_line_length = 10
        self.label_width = 80
        self.zoom_factor = 0.0001
        self._min_scale_factor = 0.01
        self.scale_factor = 1.0
        self.time_lines = dict()
        self.setInteractive(True)
        self.setDragMode(drag_mode)
        self.setSceneRect(0, 0, self.time_line_length, self.label_height)
        self.labels = []
        self.setTransformationAnchor(transform_anchor)  # needs to be set to 0 to allow view transform changes https://bugreports.qt.io/browse/QTBUG-
        self.frame_indicator = None
        self.edit_start_frame_indicator = None
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

    def create_frame_indicator(self):
        size = QSizeF()
        height = 100
        size.setHeight(height)
        size.setWidth(self.label_height)
        self.frame_indicator = FrameIndicator(size, self.frame_width, self.label_width, 0)
        self._label_scene.addItem(self.frame_indicator)

        self.edit_start_frame_indicator = FrameIndicator(size, self.frame_width, self.label_width, 0, blue)
        self._label_scene.addItem(self.edit_start_frame_indicator)

    def initScene(self):
        brush = QBrush()
        color = QColor()
        color.setGreen(255)
        color.setAlpha(255)
        brush.setColor(color)
        self._label_scene = QGraphicsScene()
        self._label_scene.setBackgroundBrush(grey)
        #self._label_scene.setForegroundBrush(color)
        self.setScene(self._label_scene)

    def clearScene(self):
        self.labels = []
        self.time_lines = dict()
        self._label_scene.clear()

    def setTimeLineParameters(self, time_line_length, label_height):
        self.label_height = label_height
        self.time_line_length = self.frame_width*time_line_length

    def addLabel(self, l, indices, color):
        y = len(self.labels)*self.label_height
        pos = QPointF(0, y)
        label = l
        timeline = TimeLine(label, indices, pos, self.time_line_length,
                                                self.label_height,
                                                self.label_width,
                                                self.frame_width,
                                                color)
        self._label_scene.addItem(timeline)
        self.time_lines[label] = timeline
        self.labels.append(l)

        self.setSceneRect(0, 0, self.time_line_length, self.label_height*len(self.labels))

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.m_originX = event.x()
            self.m_originY = event.y()

    def mouseMoveEvent(self, event):
        if event.buttons() and Qt.LeftButton:
            deltaX = event.x()-self.m_originX
            deltaY = event.y() - self.m_originY
            #self.translate(deltaX, deltaY)
            self.x += deltaX
            self.y += deltaY
            self.updateTransform()
            self.m_originX = event.x()
            self.m_originY = event.y()

    def wheelEvent(self, event):
        self.scale_factor += event.angleDelta().y() * self.zoom_factor
        self.scale_factor = max(self._min_scale_factor, self.scale_factor)
        self.updateTransform()

    def setFrame(self, idx):
        self.x = self.scale_factor*-idx*self.frame_width + self.label_width

        #transform = Qt.QTransform()
        #transform.translate(-deltaX, 0)
        #self.setTransform(transform)
        self.updateTransform()
        if self.frame_indicator is not None:
            self.frame_indicator.setFrame(idx)
    
    def set_edit_start_frame(self, idx):
        if self.edit_start_frame_indicator is not None:
            self.edit_start_frame_indicator.setFrame(idx)

    def updateTransform(self):
        if self.x > 0:
            self.x = 0

        self.resetTransform()
        m = QTransform()
        m.translate(self.x, self.y)
        m.scale(self.scale_factor, 1.0)
        self.setTransform(m)


