import importlib
from os.path import dirname, basename, join, isdir
import glob
modules = glob.glob(join(dirname(__file__), "*"))
plugins = [ basename(f) for f in modules if isdir(f)and not f.endswith('__')]

for plugin in plugins:
    print("import plugin", plugin)
    importlib.import_module("tool.plugins."+plugin)
