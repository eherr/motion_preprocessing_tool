import os
from tool.constants import CONFIG_FILE
if os.path.isfile(CONFIG_FILE):
    from tool.plugins.database.constants import set_constants_from_file
    set_constants_from_file(CONFIG_FILE)
