import importlib
from pathlib import Path

for plugin_dir in Path(__file__).parent.iterdir():
    if plugin_dir.joinpath("__init__.py").is_file():
        print("import plugin", plugin_dir.stem)
        importlib.import_module("tool.plugins."+str(plugin_dir.stem))
