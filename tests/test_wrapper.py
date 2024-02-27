import os
from dotenv import load_dotenv

import sys
sys.path.append('./src/lobbyview/')
from LobbyView import LobbyView

load_dotenv()
LOBBYVIEW_TOKEN = os.environ.get('LOBBYVIEW_TOKEN')

lobbyview = LobbyView(LOBBYVIEW_TOKEN)

def test_legislators():
    print(lobbyview.legislators(legislator_first_name="John", legislator_last_name="McCain"))
    print(lobbyview.legislators(legislator_id="M000303"))

if __name__ == "__main__":
    test_legislators()