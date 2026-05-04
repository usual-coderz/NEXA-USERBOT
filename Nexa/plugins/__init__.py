import os
import importlib

def load(client):
    path = os.path.dirname(__file__)

    for file in os.listdir(path):
        if file.endswith(".py") and not file.startswith("__"):
            module_name = f"Nexa.plugins.{file[:-3]}"

            try:
                if module_name in globals():
                    module = importlib.reload(importlib.import_module(module_name))
                else:
                    module = importlib.import_module(module_name)

                if hasattr(module, "setup"):
                    module.setup(client)

            except Exception as e:
                print(f"Failed to load {module_name}: {e}")