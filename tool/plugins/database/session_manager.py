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
from vis_utils.io import save_json_file, load_json_file
from tool.constants import DB_URL, SESSION_FILE
from anim_utils.utilities.db_interface import authenticate

class SessionManager(object):
    session = None
    def __init__(self):
        if SessionManager.session is None:
            if os.path.isfile(SESSION_FILE):
                try:
                    SessionManager.session = load_json_file(SESSION_FILE)
                except:
                    pass

    def login(self, user, password):
        result = authenticate(DB_URL, user, password)
        if "token" in result:
            print("authenticated", user, result["token"])
            SessionManager.session = {"user": user, "token": result["token"]}
            save_json_file(SessionManager.session, SESSION_FILE)

    def logout(self):
        SessionManager.session = None
        save_json_file({}, SESSION_FILE)

