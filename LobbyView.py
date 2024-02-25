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
    hard_code_token = "eyJhbGciOiJSUzI1NiIsImtpZCI6ImExODE4ZjQ0ODk0MjI1ZjQ2MWQyMmI1NjA4NDcyMDM3MTc2MGY1OWIiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJodHRwczovL3NlY3VyZXRva2VuLmdvb2dsZS5jb20vZ2l0aHViLTczNTA0IiwiYXVkIjoiZ2l0aHViLTczNTA0IiwiYXV0aF90aW1lIjoxNzA4NTQ3NDkyLCJ1c2VyX2lkIjoiZ0I3SzV2eU5MbFJLUXlzTTdjVHNObDZuRmc3MiIsInN1YiI6ImdCN0s1dnlOTGxSS1F5c003Y1RzTmw2bkZnNzIiLCJpYXQiOjE3MDg4OTk1MTIsImV4cCI6MTcwODkwMzExMiwiZW1haWwiOiJueGxpdUBtaXQuZWR1IiwiZW1haWxfdmVyaWZpZWQiOmZhbHNlLCJmaXJlYmFzZSI6eyJpZGVudGl0aWVzIjp7ImVtYWlsIjpbIm54bGl1QG1pdC5lZHUiXX0sInNpZ25faW5fcHJvdmlkZXIiOiJwYXNzd29yZCJ9fQ.LmYk_mMYJMHaTB6RvyFTtyR5moKtbru9dYuzqfVA1pgs8YcrACF0L3ML1VT6Gezozrj3ETPEaUF05eNIhgo1J7rCQtiGRGeK77N2wohzj0tC4rXIY5YP9r-sZVdYOoGyyml0_OrjtGztb3U2IoCD18tAO5zPqg02QG00066NPpJbPpbdAUZoxR-7jAS5s3V23ZqepGfHafcXu2JVZaMgodGwvHVqkMvmXI8JNW8m9BuydxoC-UX8WS4JkD5b0LDB4dIfWMsvpEH-6dCRSS8S596UcIypAwgENhPC5gv9CEcbjdJrn6SlT5ub_DH8E7OxlCyyxBYWk8_GvoJbZRrt8g:gB7K5vyNLlRKQysM7cTsNl6nFg72"
    LOBBYVIEW_TOKEN = os.environ.get('LOBBYVIEW_TOKEN', hard_code_token)

    import doctest
    results = doctest.testmod(extraglobs={'LobbyView': LobbyView(LOBBYVIEW_TOKEN)})
    results_string = f"{results.attempted-results.failed}/{results.attempted} TESTS PASSED"
    if results.failed == 0:
        print(results_string)
    else:
        raise Exception(results_string)