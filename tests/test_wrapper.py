import os
from dotenv import load_dotenv

import sys
sys.path.append('./src/lobbyview/')
sys.path.append('../src/lobbyview/')
from LobbyView import LobbyView

load_dotenv("./")
load_dotenv("./tests/.env")
hard_code_token = "eyJhbGciOiJSUzI1NiIsImtpZCI6IjNiYjg3ZGNhM2JjYjY5ZDcyYjZjYmExYjU5YjMzY2M1MjI5N2NhOGQiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJodHRwczovL3NlY3VyZXRva2VuLmdvb2dsZS5jb20vZ2l0aHViLTczNTA0IiwiYXVkIjoiZ2l0aHViLTczNTA0IiwiYXV0aF90aW1lIjoxNzA5MDkzMDMyLCJ1c2VyX2lkIjoiVVdldVNQQ2ZuM1JZUGV3SFg1Mk9mZ0xuZGRFMiIsInN1YiI6IlVXZXVTUENmbjNSWVBld0hYNTJPZmdMbmRkRTIiLCJpYXQiOjE3MDkwOTMwNDAsImV4cCI6MTcwOTA5NjY0MCwiZW1haWwiOiJhYmNAbWl0LmVkdSIsImVtYWlsX3ZlcmlmaWVkIjpmYWxzZSwiZmlyZWJhc2UiOnsiaWRlbnRpdGllcyI6eyJlbWFpbCI6WyJhYmNAbWl0LmVkdSJdfSwic2lnbl9pbl9wcm92aWRlciI6InBhc3N3b3JkIn19.cSSnqzLm_g5LoUS0TB6VMIjK2j7nS1zkt2GF-kkpDf4b0tkeaPfixfmaQPKkqEV4X5Zq9pVQKoaDqTiNvz_asrcyBhUaJWR7fD2a-3uzofc57pqTPvvw9hQGcrWtnzpnXgEMLEmBmQb8qQhNUVEksn0E9xymG85jGhgYffNTp9fQaQNKLzb249A9DLy9-tj8DYgmQeLp-WIOEM8X1jB1POK9W5XdRVwYUBfsgJVVsIuSRxZHWA3AKnwMe41ohMsTns28kj_9fCWA_26zwO9awxGj6PTdl1wWWFAoRvanuH-dI2OBp65X-IeLjB5xu6Usx-c4inOP3WoXktpSfoPP8g:UWeuSPCfn3RYPewHX52OfgLnddE2"
LOBBYVIEW_TOKEN = os.environ.get('LOBBYVIEW_TOKEN', hard_code_token)
print(LOBBYVIEW_TOKEN)

lobbyview = LobbyView(LOBBYVIEW_TOKEN)

def test_legislators():
    assert lobbyview.legislators(legislator_first_name="John", legislator_last_name="McCain")['data'][0]['legislator_id'] == 'M000303'
    assert lobbyview.legislators(legislator_id="M000303")['data'][0]['legislator_full_name'] == 'John McCain'

if __name__ == "__main__":
    test_legislators()