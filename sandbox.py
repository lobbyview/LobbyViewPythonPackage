from LobbyView import LobbyView
import os
from dotenv import load_dotenv

load_dotenv()
LOBBYVIEW_TOKEN = os.environ.get('LOBBYVIEW_TOKEN')

lobbyview = LobbyView(LOBBYVIEW_TOKEN)
print(lobbyview.get_legislator(first_name="John", last_name="McCain"))