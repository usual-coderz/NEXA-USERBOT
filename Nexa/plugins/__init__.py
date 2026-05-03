import os
import importlib

def load(client):
    for file in os.listdir(os.path.dirname(__file__)):
        if file.endswith(".py") and not file.startswith("__"):
            module = importlib.import_module(f"Nexa.plugins.{file[:-3]}")
            if hasattr(module, "setup"):
                module.setup(client)