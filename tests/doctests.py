import doctest
import importlib.util
import os
from dotenv import load_dotenv

import sys
sys.path.append('./src/lobbyview/')
sys.path.append('../src/lobbyview/')
from LobbyView import LobbyView

# loads token from .env file/environment variable
load_dotenv("tests/.env")
load_dotenv("../../tests/.env")
LOBBYVIEW_TOKEN = os.environ.get('LOBBYVIEW_TOKEN', "NO TOKEN FOUND")

def import_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    foo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(foo)
    return foo

if __name__ == "__main__":
    # run doctests, pass in the LobbyView object with the token
    try:
        results = doctest.testmod(import_module("src.lobbyview.LobbyView", "../src/lobbyview/LobbyView.py"), 
                                extraglobs={'lobbyview': LobbyView(LOBBYVIEW_TOKEN)},
                                optionflags=doctest.ELLIPSIS)
    except:
        results = doctest.testmod(import_module("src.lobbyview.LobbyView", "./src/lobbyview/LobbyView.py"), 
                                extraglobs={'lobbyview': LobbyView(LOBBYVIEW_TOKEN)},
                                optionflags=doctest.ELLIPSIS)
    
    results_string = f"{results.attempted-results.failed}/{results.attempted} TESTS PASSED"
    if results.failed == 0:
        print(results_string)
    else:
        raise Exception(results_string)