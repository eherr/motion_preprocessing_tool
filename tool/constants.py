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
import glob
import collections
import json
from vis_utils import constants as vis_constants

CONFIG_FILE = "config.json"
DATA_DIR = "data"
LOCAL_SKELETON_MODELS = collections.OrderedDict()

def set_constants_from_file(filename):
    global DATA_DIR
    global LOCAL_SKELETON_MODELS
    vis_constants.activate_simulation = True
    vis_constants.use_frame_buffer = True
    vis_constants.activate_shadows = True
    with open(filename, "rt") as in_file:
        config = json.load(in_file)
    if "activate_simulation" in config:
        vis_constants.activate_simulation = config["activate_simulation"]
    if "use_frame_buffer" in config:
        vis_constants.use_frame_buffer = config["use_frame_buffer"]
    if "activate_shadows" in config:
        vis_constants.activate_shadows = config["activate_shadows"]

    if "data_dir" in config:
        DATA_DIR = config["data_dir"]
    
    if not os.path.isdir(DATA_DIR):
        try:
            os.makedirs(DATA_DIR)
            print("Created data dir", DATA_DIR)
        except:
            print("Could not create data dir")
            pass
    else:
        for filename in glob.glob(DATA_DIR+os.sep+"skeletons"+os.sep+"*.json"):
            name = filename.split(os.sep)[-1][:-5]
            with open(filename, "rt") as in_file:
                LOCAL_SKELETON_MODELS[name] = json.load(in_file)
