import os
from dotenv import load_dotenv

import sys
sys.path.append('./src/lobbyview/')
sys.path.append('../src/lobbyview/')
from LobbyView import LobbyView

env_paths = ["tests/.env", "../../tests/.env"]
for env_path in env_paths:
    load_dotenv(env_path)

LOBBYVIEW_TOKEN = os.environ.get('LOBBYVIEW_TOKEN', "NO TOKEN FOUND")

# LOBBYVIEW_TOKEN = "fail"
# lobbyview = LobbyView(LOBBYVIEW_TOKEN)

# def test_legislators():
#     output = lobbyview.legislators(legislator_first_name="John", legislator_last_name="McCain", page=3)
#     print(output.page_info())

# def test_clients():
#     output = lobbyview.clients(client_name="Microsoft Corporation")
#     assert output.data[0]['client_uuid'] == '44563806-56d2-5e99-84a1-95d22a7a69b3'

if __name__ == "__main__":
    # test_legislators()
    # test_clients()
    # lobbyview_invalid = LobbyView("invalid_token_kvhjeblhvbleihvbehibvfihleqbvihebivlebhl", test_connection=False)
    # lobbyview_invalid.get_data('/api/legislators')

    lobbyview = LobbyView(LOBBYVIEW_TOKEN)
    # lobbyview.get_data('/api/legislators?invalid_param=value')
    for client in lobbyview.paginate(lobbyview.clients, client_name='InvalidClientName'):
        print(f"Client: {client['client_name']} - NAICS: {client['primary_naics']}")