import os
from dotenv import load_dotenv

import sys
sys.path.append('./src/lobbyview/')
sys.path.append('../src/lobbyview/')
from LobbyView import LobbyView

load_dotenv("./")
load_dotenv("tests/.env")
hard_code_token = "eyJhbGciOiJSUzI1NiIsImtpZCI6IjNiYjg3ZGNhM2JjYjY5ZDcyYjZjYmExYjU5YjMzY2M1MjI5N2NhOGQiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJodHRwczovL3NlY3VyZXRva2VuLmdvb2dsZS5jb20vZ2l0aHViLTczNTA0IiwiYXVkIjoiZ2l0aHViLTczNTA0IiwiYXV0aF90aW1lIjoxNzA5MDU4MjgwLCJ1c2VyX2lkIjoiZ0I3SzV2eU5MbFJLUXlzTTdjVHNObDZuRmc3MiIsInN1YiI6ImdCN0s1dnlOTGxSS1F5c003Y1RzTmw2bkZnNzIiLCJpYXQiOjE3MDkwODg0NTEsImV4cCI6MTcwOTA5MjA1MSwiZW1haWwiOiJueGxpdUBtaXQuZWR1IiwiZW1haWxfdmVyaWZpZWQiOmZhbHNlLCJmaXJlYmFzZSI6eyJpZGVudGl0aWVzIjp7ImVtYWlsIjpbIm54bGl1QG1pdC5lZHUiXX0sInNpZ25faW5fcHJvdmlkZXIiOiJwYXNzd29yZCJ9fQ.hAJbd95baBgmxqDEu9dKrfGCS9lyUir9-BJmpLUDuzGK2zFfntg6omgEhb5xVVyGVeA_HHr7dS-VPo0QjqKjcJFDIx5GU9HGpZx-a5-Ky4nHhEqZtHda1QHA0MRSlNww-lkf5Rl2yIhk4S8RAr9p7rp3Ru_5YNasgawtHJYQTXcLWh84r21pnKe7j1HnazvteM0C2KmMOE6wffSX-3VgZzTUr6ks6pjz7iJHEjaGUC0mPKawFSGsghDmVn7M7RPRcM5ge_we8TBQmq34NT8jA4j50yn7SKi3AWcI7dGLax_atI9xKCH1ubMZMr9QkUR-VqpXoxuvHcXIve-l9XNLyw:gB7K5vyNLlRKQysM7cTsNl6nFg72"
LOBBYVIEW_TOKEN = os.environ.get('LOBBYVIEW_TOKEN', hard_code_token)

lobbyview = LobbyView(LOBBYVIEW_TOKEN)

def test_legislators():
    assert lobbyview.legislators(legislator_first_name="John", legislator_last_name="McCain")['data'][0]['legislator_id'] == 'M000303'
    assert lobbyview.legislators(legislator_id="M000303")['data'][0]['legislator_full_name'] == 'John McCain'

if __name__ == "__main__":
    test_legislators()