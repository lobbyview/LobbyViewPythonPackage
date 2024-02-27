## Functionality
Python wrapper for Lobbyview Rest API; uses same endpoints and parameter names as outlined in the
[LobbyView Rest API Documentation](https://rest-api.lobbyview.org/)

## Sample Code
    
    import os
    from dotenv import load_dotenv

    from lobbyview import LobbyView

    load_dotenv()
    LOBBYVIEW_TOKEN = os.environ.get('LOBBYVIEW_TOKEN')

    lobbyview = LobbyView.LobbyView(LOBBYVIEW_TOKEN)
    print(lobbyview.legislators(legislator_first_name="John", legislator_last_name="McCain"))
    print(lobbyview.legislators(legislator_id="M000303"))
