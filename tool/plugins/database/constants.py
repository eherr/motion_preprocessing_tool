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
import json

SESSION_FILE = "session.json"
CONFIG_FILE = "config.json"
DB_URL = "https://motion.dfki.de/8888"
K8S_RESOURCES = dict()
K8S_RESOURCES["n_gpus"] = 0
K8S_RESOURCES["cpu"] = {"request":1, "limit":2}
K8S_RESOURCES["memory"] = {"request":"2Gi", "limit":"4Gi"}
K8S_IMAGE_NAME = "python:3.5.3"
MG_REPO_URL = "https://iceland.sb.dfki.de/bitbucket/scm/motsy/mosi_dev_mg.git"
MG_EXEC_DIR= "mosi_dev_mg/python_src"

def set_constants_from_file(filename):
    global DB_URL
    global MG_REPO_URL
    global MG_EXEC_DIR
    global K8S_IMAGE_NAME
    with open(filename, "rt") as in_file:
        config = json.load(in_file)
    if "db_url" in config:
        DB_URL = config["db_url"]
    if "mg_repo_url" in config:
        MG_REPO_URL = config["mg_repo_url"]
    if "mg_exec_dir" in config:
        MG_EXEC_DIR = config["mg_exec_dir"]
    if "k8s_image_name" in config:
        K8S_IMAGE_NAME = config["k8s_image_name"]
    
