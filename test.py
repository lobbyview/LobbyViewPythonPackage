import http.client
import json
from dotenv import load_dotenv
import os

load_dotenv()
LOBBYVIEW_TOKEN = os.environ.get('LOBBYVIEW_TOKEN')

def get_legislator(first_name, last_name):
    '''
    Gets legislator information from the LobbyView API based on first and last name

    >>> output = get_legislator("John", "McCain")
    >>> output['data'][0]['legislator_id']
    'M000303'
    >>> get_legislator("", "")
    'Invalid input'
    
    '''
    if not first_name or not last_name:
        output = "Invalid input"

    else:
        connection = http.client.HTTPSConnection('rest-api.lobbyview.org')
        headers = {
            'token': LOBBYVIEW_TOKEN,
        }
        connection.request('GET', f'/api/legislators?legislator_first_name=eq.{first_name}&legislator_last_name=eq.{last_name}', None, headers)

        response = connection.getresponse()
        data_string = response.read().decode('utf-8')
        data = json.loads(data_string)

        output = data

    return output

if __name__ == "__main__":
    # get_legislator("John", "McCain")

    import doctest
    doctest.testmod()