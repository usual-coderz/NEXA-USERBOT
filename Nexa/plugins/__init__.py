import os
import importlib

def load(client):
    path = os.path.dirname(__file__)

    for file in os.listdir(path):
        if file.endswith(".py") and not file.startswith("__"):
            module_name = f"Nexa.plugins.{file[:-3]}"

            module = importlib.import_module(module_name)

            if hasattr(module, "setup"):
                module.setup(client)