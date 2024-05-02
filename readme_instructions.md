# Instructions

Import a lobbyview token using os and dotenv

    import os
    from dotenv import load_dotenv
    load_dotenv(".env")
    LOBBYVIEW_TOKEN = os.environ.get('LOBBYVIEW_TOKEN')

Initialize a LobbyView object instance

    from LobbyView import LobbyView
    lobbyview = LobbyView(LOBBYVIEW_TOKEN)

Note that ```quarter_level_networks``` and ```bill_client_networks``` API endpoints are not available to all users.