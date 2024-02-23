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

    def legislators(self, first_name="", last_name="", legislator_id="", legislator_govtrack_id=""):
        '''
        Gets legislator information from the LobbyView API based on first and last name

        >>> output = LobbyView.legislators(first_name="John", last_name="McCain")
        >>> output['data'][0]['legislator_id']
        'M000303'
        >>> LobbyView.legislators("", "")
        'Invalid input'
        >>> output = LobbyView.legislators(legislator_id="M000303")
        >>> output['data'][0]['legislator_full_name']
        'John McCain'
        
        '''
        if not first_name and not last_name and not legislator_id and not legislator_govtrack_id:
            output = "Invalid input"

        else:
            url_args = []
            if first_name:
                url_args.append(f'legislator_first_name=eq.{first_name}') 
            if last_name:
                url_args.append(f'legislator_last_name=eq.{last_name}')
            if legislator_id:
                url_args.append(f'legislator_id=eq.{legislator_id}')
            if legislator_govtrack_id:
                url_args.append(f'legislator_govtrack_id=eq.{legislator_govtrack_id}')

            url_args = "&".join(url_args)
                
            self.connection.request('GET', f'/api/legislators?{url_args}', None, self.headers)
            response = self.connection.getresponse()
            data_string = response.read().decode('utf-8')
            data = json.loads(data_string)

            output = data

        return output

if __name__ == "__main__":
    load_dotenv()
    hard_code_token = "eyJhbGciOiJSUzI1NiIsImtpZCI6ImExODE4ZjQ0ODk0MjI1ZjQ2MWQyMmI1NjA4NDcyMDM3MTc2MGY1OWIiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJodHRwczovL3NlY3VyZXRva2VuLmdvb2dsZS5jb20vZ2l0aHViLTczNTA0IiwiYXVkIjoiZ2l0aHViLTczNTA0IiwiYXV0aF90aW1lIjoxNzA4NTQ3NDkyLCJ1c2VyX2lkIjoiZ0I3SzV2eU5MbFJLUXlzTTdjVHNObDZuRmc3MiIsInN1YiI6ImdCN0s1dnlOTGxSS1F5c003Y1RzTmw2bkZnNzIiLCJpYXQiOjE3MDg2NjE4NDksImV4cCI6MTcwODY2NTQ0OSwiZW1haWwiOiJueGxpdUBtaXQuZWR1IiwiZW1haWxfdmVyaWZpZWQiOmZhbHNlLCJmaXJlYmFzZSI6eyJpZGVudGl0aWVzIjp7ImVtYWlsIjpbIm54bGl1QG1pdC5lZHUiXX0sInNpZ25faW5fcHJvdmlkZXIiOiJwYXNzd29yZCJ9fQ.TEtRKE7iU9_XPm1V_1ZZM2B4HNRKYtd1hvujI6N56i-U0dT0z7rjrP2nJQbWvkgwEYZGOfSkW9t16Fae3qLXN8CVDygz9HIKDhAIXxEi0L6cktjmgrO7VxKQkV9BHtPpzIXOSIs1Ukgb0WQ2zY8CWXJeNClhiR7olXjKTB2sSUmXYN4VbedxIVfgbXe93-oekxzbSuo7DZbzqIrf5Wnb9erj-KiIu1IQnXdRJHNYIUOikSMs_d3qZjFukqTWczRQJjqOydNewkx4Ls5ppcNLKlgF-z0bgiJs2O28q_qAz4YCbEJ-UMjHlICqNq8QfSVvLrYDhTAsPMF8r8kcv1gvgw:gB7K5vyNLlRKQysM7cTsNl6nFg72"
    LOBBYVIEW_TOKEN = os.environ.get('LOBBYVIEW_TOKEN', hard_code_token)

    import doctest
    results = doctest.testmod(extraglobs={'LobbyView': LobbyView(LOBBYVIEW_TOKEN)})
    results_string = f"{results.attempted-results.failed}/{results.attempted} TESTS PASSED"
    if results.failed == 0:
        print(results_string)
    else:
        raise Exception(results_string)