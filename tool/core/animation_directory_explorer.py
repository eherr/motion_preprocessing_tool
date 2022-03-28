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
import os
from pathlib import Path
from copy import deepcopy
from PySignal import Signal
import numpy as np
from vis_utils.animation.animation_controller import AnimationController
from vis_utils.scene.components import ComponentBase
from vis_utils.animation.skeleton_visualization import SkeletonVisualization
from anim_utils.animation_data import BVHReader, MotionVector, SkeletonBuilder
from anim_utils.animation_data.motion_state import MotionState


class AnimationDirectoryExplorer(ComponentBase, AnimationController):
    updated_animation_frame = Signal()
    reached_end_of_animation = Signal()

    def __init__(self, scene_object, folder_path, filetype, color):
        ComponentBase.__init__(self, scene_object)
        self.mainContext = 0
        self.name = folder_path
        AnimationController.__init__(self)
        self.skeleton_vis = SkeletonVisualization(scene_object, color)
        self.skeleton_vis.draw_mode = 2
        self.skeleton_vis.visible = False
        scene_object.add_component("skeleton_vis", self.skeleton_vis)
        self.folder_path = Path(folder_path)
        self._animation_files = []
        self.current_controller = None
        self.motion_cache = dict()
        self.state = None
        for filename in self.folder_path.iterdir():
            print(filename, filetype, filename.suffix)
            if filename.is_file() and filename.suffix == "."+filetype:
                self._animation_files.append(filename.name)
        self.select_file(self._animation_files[0])

    def select_file(self, filename):
        if filename not in self._animation_files:
            return
        if filename not in self.motion_cache:
            self.load_file(filename)
        self.current_controller = filename
        self.skeleton_vis.set_skeleton(self.motion_cache[filename].skeleton, True)
        self.skeleton_vis.visible = True
        self.state = MotionState(self.motion_cache[filename])
        self.state.play = self.playAnimation
        self.updateTransformation()
        return self.motion_cache[filename].n_frames

    def load_file(self, filename):
        bvh_reader = BVHReader(str(self.folder_path) +os.sep+filename)
        mv = MotionVector()
        mv.from_bvh_reader(bvh_reader, False)
        animated_joints = list(bvh_reader.get_animated_joints())
        mv.skeleton = SkeletonBuilder().load_from_bvh(bvh_reader, animated_joints=animated_joints)
        self.motion_cache[filename] = mv
        return mv

    def get_animation_files(self):
        return self._animation_files

    def update(self, dt):
        """ update current frame and global joint transformation matrices
        """
        dt *= self.animationSpeed
        if self.isLoadedCorrectly():
            if self.playAnimation:
                self.state.update(dt)
                self.updateTransformation()

                # update gui
                if self.state.frame_idx > self.getNumberOfFrames():
                        self.resetAnimationTime()
                        self.reached_end_of_animation.emit(self.loopAnimation)
                else:
                    self.updated_animation_frame.emit(self.state.frame_idx)

    def draw(self, modelMatrix, viewMatrix, projectionMatrix, lightSources):
        return

    def updateTransformation(self, frame_idx=None):
        if self.state is None:
            return
        if frame_idx is not None:
            self.state.set_frame_idx(frame_idx)
        pose = self.state.get_pose()
        self.skeleton_vis.updateTransformation(pose, np.eye(4))

    def resetAnimationTime(self):
        if self.state is None:
            return
        AnimationController.resetAnimationTime(self)
        self.currentFrameNumber = 0
        self.state.reset()
        self.updateTransformation(self.state.frame_idx)

    def setCurrentFrameNumber(self, frame_idx):
        if self.state is None:
            return
        self.state.set_frame_idx(frame_idx)
        self.updateTransformation()

    def getNumberOfFrames(self):
        if self.state is not None:
            return self.state.mv.n_frames
        else:
            return 0

    def isLoadedCorrectly(self):
        return len(self._animation_files) > 0 and self.state is not None

    def getFrameTime(self):
        if self.isLoadedCorrectly():
            return self.state.mv.frame_time
        else:
            return 0

    def toggle_animation_loop(self):
        self.loopAnimation = not self.loopAnimation

    def set_draw_mode(self, draw_mode):
        self.skeleton_vis.draw_mode = draw_mode
        return

    def startAnimation(self):
        if self.state is None:
            return
        self.playAnimation = True
        self.state.play = True

    def stopAnimation(self):
        if self.state is None:
            return
        self.playAnimation = False
        self.state.play = False

    def load_selected(self):
        mv_copy = deepcopy(self.state.mv)
        self.scene_object.scene.object_builder.create_object("animation_controller",
                                                            self.current_controller, 
                                                            mv_copy.skeleton, mv_copy, 
                                                            mv_copy.frame_time) 
