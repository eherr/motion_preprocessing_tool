import importlib
from pathlib import Path
for plugin_dir in Path(__file__).parent.iterdir():
    if plugin_dir.joinpath("__init__.py").is_file():
        try:
            print("Importing "+ plugin_dir.stem + " plugin...")
            importlib.import_module("tool.plugins."+str(plugin_dir.stem))
        except Exception as e:
            print("Error: Could not import plugin "+plugin_dir.stem + ": "+str(e))
            pass
