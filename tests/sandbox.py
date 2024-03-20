import os
from dotenv import load_dotenv

import sys
sys.path.append('./src/lobbyview/')
sys.path.append('../src/lobbyview/')
from LobbyView import LobbyView

load_dotenv("./.env")
load_dotenv("./tests/.env")
LOBBYVIEW_TOKEN = os.environ.get('LOBBYVIEW_TOKEN', "NO TOKEN FOUND")

lobbyview = LobbyView(LOBBYVIEW_TOKEN)

def test_legislators():
    output = lobbyview.legislators(legislator_first_name="John", legislator_last_name="McCain", page=3)
    print(output.page_info())

    # output = lobbyview.legislators(legislator_first_name="John", page=2)
    # print(output)

if __name__ == "__main__":
    test_legislators()