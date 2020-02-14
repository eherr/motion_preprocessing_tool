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

PCSKELETON = {
    "Spine": {
        "parent": "LowerBack",
      #  "x_axis_index": 3,
        "index": 7
    },
    "RightHand": {
        "parent": "RightForeArm",
       # "x_axis_index": 23,
        "index": 16
    },
    "RightUpLeg": {
        "parent": "RHipJoint",
       # "x_axis_index": 31,
        "index": 1
    },
    "RightLeg": {
        "parent": "RightUpLeg",
       # "x_axis_index": 33,
        "index": 2
    },
    "RightForeArm": {
        "parent": "RightArm",
       # "x_axis_index": 29,
        "index": 15
    },
    "LeftForeArm": {
        "parent": "LeftArm",
       # "x_axis_index": 13,
        "index": 19
    },
    "RightArm": {
        "parent": "RightShoulder",
       # "x_axis_index": 19,
        "index": 14
    },
    "Hips": {
        "parent": None,
       # "x_axis_index": 1,
        "index": 0
    },
    "LeftFoot": {
        "parent": "LeftLeg",
        #"x_axis_index": 35,
        "index": 6
    },
    "RightShoulder": {
        "parent": "Spine1",
        #"x_axis_index": 17,
        "index": 13
    },
    "LeftShoulder": {
        "parent": "Spine1",
        #"x_axis_index": 9,
        "index": 17
    },
    "Neck1": {
        "parent": "Neck",
       # "x_axis_index": 7,
        "index": 11
    },
    "LeftArm": {
        "parent": "LeftShoulder",
       # "x_axis_index": 11,
        "index": 18
    },
    "LeftLeg": {
        "parent": "LeftUpLeg",
       # "x_axis_index": 27,
        "index": 5
    },
    "LeftUpLeg": {
        "parent": "LHipJoint",
        #"x_axis_index": 25,
        "index": 4
    },
    "LeftHand": {
        "parent": "LeftForeArm",
       # "x_axis_index": 15,
        "index": 20
    },
    "RightFoot": {
        "parent": "RightLeg",
        #"x_axis_index": 37,
        "index": 3
    },
    "Spine1": {
        "parent": "Spine",
        #"x_axis_index": 5,
        "index": 8
    }
}
MODEL_OFFSET = [0,0,0]