import http.client
import json
from dotenv import load_dotenv
import os

class LobbyView():
    def __init__(self, token):
        self.lobbyview_token = token
        self.connection = http.client.HTTPSConnection('rest-api.lobbyview.org')
        self.headers = {
            'token': self.lobbyview_token,
        }

    def get_legislator(self, first_name="", last_name=""):
        '''
        Gets legislator information from the LobbyView API based on first and last name

        >>> output = LobbyView.get_legislator("John", "McCain")
        >>> output['data'][0]['legislator_id']
        'M000303'
        >>> LobbyView.get_legislator("", "")
        'Invalid input'
        
        '''
        if not first_name and not last_name:
            output = "Invalid input"

        else: 
            first_name_arg = f'legislator_first_name=eq.{first_name}' if first_name else ""
            last_name_arg = f'legislator_last_name=eq.{last_name}' if last_name else ""
                
            self.connection.request('GET', f'/api/legislators?{first_name_arg}&{last_name_arg}', None, self.headers)
            response = self.connection.getresponse()
            data_string = response.read().decode('utf-8')
            data = json.loads(data_string)

            output = data

        return output

if __name__ == "__main__":
    load_dotenv()
    LOBBYVIEW_TOKEN = os.environ.get('LOBBYVIEW_TOKEN', "")

    import doctest
    results = doctest.testmod(extraglobs={'LobbyView': LobbyView(LOBBYVIEW_TOKEN)})
    if results.failed == 0:
        print(f"{results.attempted-results.failed}/{results.attempted} TESTS PASSED")
    else:
        raise Exception(f"{results.failed}/{results.attempted} TESTS FAILED")