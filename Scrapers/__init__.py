import os
import importlib

# Automatically import all modules in the current package (Scrapers folder)
for filename in os.listdir(os.path.dirname(__file__)):
    if filename.endswith(".py") and filename != "__init__.py":
        module_name = filename[:-3]  # Remove the '.py' extension
        importlib.import_module(f".{module_name}", package=__name__)