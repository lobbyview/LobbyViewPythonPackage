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
    hard_code_token = "eyJhbGciOiJSUzI1NiIsImtpZCI6ImExODE4ZjQ0ODk0MjI1ZjQ2MWQyMmI1NjA4NDcyMDM3MTc2MGY1OWIiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJodHRwczovL3NlY3VyZXRva2VuLmdvb2dsZS5jb20vZ2l0aHViLTczNTA0IiwiYXVkIjoiZ2l0aHViLTczNTA0IiwiYXV0aF90aW1lIjoxNzA4NTQ3NDkyLCJ1c2VyX2lkIjoiZ0I3SzV2eU5MbFJLUXlzTTdjVHNObDZuRmc3MiIsInN1YiI6ImdCN0s1dnlOTGxSS1F5c003Y1RzTmw2bkZnNzIiLCJpYXQiOjE3MDg2NDA1NTUsImV4cCI6MTcwODY0NDE1NSwiZW1haWwiOiJueGxpdUBtaXQuZWR1IiwiZW1haWxfdmVyaWZpZWQiOmZhbHNlLCJmaXJlYmFzZSI6eyJpZGVudGl0aWVzIjp7ImVtYWlsIjpbIm54bGl1QG1pdC5lZHUiXX0sInNpZ25faW5fcHJvdmlkZXIiOiJwYXNzd29yZCJ9fQ.hBJhikfmIrsmT_pan_QQ0VVv1fKOgjT_HUqYuwhXykp7K4kz7Cn5wvoKpQHLnUssdxiH7zRS-6Ccb48UfqKiZ8o2_mpnYBax5ZkJT2rkRzFc7pckRFongtB-5pRDKPd28GYg5n3yMu08MP5EizqJJ3HQMbqmXq8-yKACPQvWqG63h-Vd17nDDp2glYRGUSVxmsCP1CiyZ9fvwwXy7bwaloG-KGNIVP352J2LDOFNgC10ejIx2snRys_03Evo9JGQycJRvVZ-mIzpGdirJkbWKqiJ3kLz8JkBln4_W47eVBTTvjgd6c4ny3OLgzU1kZA_4nRffS4iI2TQLk5XPX9ZEw:gB7K5vyNLlRKQysM7cTsNl6nFg72"
    LOBBYVIEW_TOKEN = os.environ.get('LOBBYVIEW_TOKEN', hard_code_token)

    import doctest
    results = doctest.testmod(extraglobs={'LobbyView': LobbyView(LOBBYVIEW_TOKEN)})
    if results.failed == 0:
        print(f"{results.attempted-results.failed}/{results.attempted} TESTS PASSED")
    else:
        raise Exception(f"{results.failed}/{results.attempted} TESTS FAILED")