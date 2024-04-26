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

def test_clients():
    output = lobbyview.clients(client_name="Microsoft Corporation")
    assert output.data[0]['client_uuid'] == '44563806-56d2-5e99-84a1-95d22a7a69b3'

if __name__ == "__main__":
    # test_legislators()
    test_clients()