import os
from dotenv import load_dotenv

import sys
sys.path.append('./src/lobbyview/')
sys.path.append('../src/lobbyview/')
from LobbyView import LobbyView

load_dotenv("./")
load_dotenv("tests/.env")
hard_code_token = ""
LOBBYVIEW_TOKEN = os.environ.get('LOBBYVIEW_TOKEN', hard_code_token)

lobbyview = LobbyView(LOBBYVIEW_TOKEN)

def test_legislators():
    assert lobbyview.legislators(legislator_first_name="John", legislator_last_name="McCain")['data'][0]['legislator_id'] == 'M000303'
    assert lobbyview.legislators(legislator_id="M000303")['data'][0]['legislator_full_name'] == 'John McCain'

if __name__ == "__main__":
    test_legislators()