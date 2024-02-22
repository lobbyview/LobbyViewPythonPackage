import http.client
import json
from dotenv import load_dotenv
import os

load_dotenv()
LOBBYVIEW_TOKEN = os.environ.get('LOBBYVIEW_TOKEN')

if not LOBBYVIEW_TOKEN:
    LOBBYVIEW_TOKEN = "eyJhbGciOiJSUzI1NiIsImtpZCI6ImExODE4ZjQ0ODk0MjI1ZjQ2MWQyMmI1NjA4NDcyMDM3MTc2MGY1OWIiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJodHRwczovL3NlY3VyZXRva2VuLmdvb2dsZS5jb20vZ2l0aHViLTczNTA0IiwiYXVkIjoiZ2l0aHViLTczNTA0IiwiYXV0aF90aW1lIjoxNzA4NTQ3NDkyLCJ1c2VyX2lkIjoiZ0I3SzV2eU5MbFJLUXlzTTdjVHNObDZuRmc3MiIsInN1YiI6ImdCN0s1dnlOTGxSS1F5c003Y1RzTmw2bkZnNzIiLCJpYXQiOjE3MDg2MTc5ODUsImV4cCI6MTcwODYyMTU4NSwiZW1haWwiOiJueGxpdUBtaXQuZWR1IiwiZW1haWxfdmVyaWZpZWQiOmZhbHNlLCJmaXJlYmFzZSI6eyJpZGVudGl0aWVzIjp7ImVtYWlsIjpbIm54bGl1QG1pdC5lZHUiXX0sInNpZ25faW5fcHJvdmlkZXIiOiJwYXNzd29yZCJ9fQ.ihxpWqlS-XpEEe7_zwPTSetkCfZmw2qEsacXu5kX536T3hvJiB0c1UkBVGuPQhz6SSiQfu5kfnaPyuUujfZv_pj7jWnLsTugge7yI-D8o-m-erEUHTCUMfVxo0tZO_4jb1Bv-LGORJ-sc6ZEnwSkhK1j5KHquELPyd7HZs0u_fWod4kRCSkXYEfceuDLfKn0kBPeWvKCvECUyoWh1Qi1Ay_tROxbItF7ohbTU-EDSeXrokKE3nvqVPlzBexiOQfzGoHVgGl9_UqnrpkY8GigylxLU66TXHz32Fd0DA9l9pacUOw1I4y3NkH3ht-iZLIDXIccfp_mPi7h0P06qBeXjg:gB7K5vyNLlRKQysM7cTsNl6nFg72"

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
    results = doctest.testmod()
    if results.failed == 0:
        print("ALL TESTS PASSED")
    else:
        raise Exception("SOME TESTS FAILED")