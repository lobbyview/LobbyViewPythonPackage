import os
import doctest
import importlib.util
from dotenv import load_dotenv
from sys import path as sys_path

# Configuring the search paths for modules
sys_path.append('./src/lobbyview/')
sys_path.append('../src/lobbyview/')
from LobbyView import LobbyView

# Load environment variables from .env files
env_paths = ["tests/.env", "../../tests/.env"]
for env_path in env_paths:
    load_dotenv(env_path)

# Retrieve the LobbyView token
LOBBYVIEW_TOKEN = os.getenv('LOBBYVIEW_TOKEN', "NO TOKEN FOUND")

def import_module(module_name, module_path):
    """ Dynamically imports a module from a given file path """
    spec = importlib.util.spec_from_file_location(module_name, module_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

def run_doctests(module_name, module_path):
    """ Runs doctest on a specified module """
    try:
        # Attempt to load the module and run tests
        module = import_module(module_name, module_path)
        results = doctest.testmod(module, extraglobs={'lobbyview': LobbyView(LOBBYVIEW_TOKEN)},
                                  optionflags=doctest.ELLIPSIS)
        results_string = f"{results.attempted - results.failed}/{results.attempted} TESTS PASSED"
        if results.failed == 0:
            print(results_string)
        else:
            raise Exception(results_string)
    except ImportError as e:
        print(f"Failed to import {module_name} from {module_path}: {e}")

if __name__ == "__main__":
    # Define paths to the module
    module_paths = ["../src/lobbyview/LobbyView.py", "./src/lobbyview/LobbyView.py"]
    
    for path in module_paths:
        run_doctests("src.lobbyview.LobbyView", path)
