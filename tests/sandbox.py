import os
from dotenv import load_dotenv

import sys
sys.path.append('./src/lobbyview/')
sys.path.append('../src/lobbyview/')
from LobbyView import LobbyView

env_paths = ["tests/.env", "../../tests/.env"]
for env_path in env_paths:
    load_dotenv(env_path)

LOBBYVIEW_TOKEN = os.environ.get('LOBBYVIEW_TOKEN', "NO TOKEN FOUND")

# LOBBYVIEW_TOKEN = "fail"
# lobbyview = LobbyView(LOBBYVIEW_TOKEN)

# def test_legislators():
#     output = lobbyview.legislators(legislator_first_name="John", page=2)
#     print(output.page_info())
#     print(output.data)

# def test_clients():
#     output = lobbyview.clients(client_name="Microsoft Corporation")
#     assert output.data[0]['client_uuid'] == '44563806-56d2-5e99-84a1-95d22a7a69b3'
#     output = lobbyview.clients(max_naics="5112", page=2)
#     print(output.page_info()['current_page'])
#     output = lobbyview.clients(client_uuid='44563806-56d2-5e99-84a1-95d22a7a69b3')
#     print(output.page_info())
#     output = lobbyview.clients(client_uuid='44563806-56d2-5e99-84a1-95d22a7a69b3', naics_description="Applications software") ### too slow example
#     print(output.page_info())

# def test_bills():
#     output = lobbyview.bills(congress_number=116, bill_resolution_type="R", bill_number=400, legislator_id="R000595")
#     print(output)
#     output = lobbyview.bills(min_introduced_date="2020-01-01", page=10)
#     print(output.page_info()['current_page'])

# def test_reports():
#     output = lobbyview.reports(report_year=2020, page=2)
#     print(output.page_info()['current_page'])
#     print(output.data[0])
#     output = lobbyview.reports(report_uuid="7947c9c2-8595-5bf9-a0af-f516c5a0659f")
#     output = lobbyview.reports(client_uuid="78043d66-6dc9-5d6c-b0ee-c3afaa33d8d7", report_year=2020, min_report_quarter_code=2, max_report_quarter_code=4, min_amount=150000)
#     print(output)

# def test_issues():
#     output = lobbyview.issues(report_uuid='00016ab3-2246-5af8-a68d-05af40dfde68')
#     print(output.page_info())
#     output = lobbyview.issues(report_uuid='00016ab3-2246-5af8-a68d-05af40dfde68', gov_entity='SENATE') ### too slow example
#     print(output.page_info())

#     output = lobbyview.issues(issue_code="TRD", page=2)
#     print(output.page_info()['current_page'])

# def test_networks():
#     output = lobbyview.networks(min_bills_sponsored=50, page=2)
#     print(output.page_info()['current_page'])

# def test_quarter_level_networks():
#     output = lobbyview.quarter_level_networks(min_bills_sponsored=20, page=2)
#     print(output.page_info()['current_page'])

# def test_bill_client_networks():
#     output = lobbyview.bill_client_networks(bill_id="H.R.1174-114")
#     print(output.page_info()['total_pages'])

if __name__ == "__main__":
    lobbyview = LobbyView(LOBBYVIEW_TOKEN)

    # test_bill_client_networks()
    # test_quarter_level_networks()
    # test_networks()
    # test_issues()
    # test_reports()
    # test_bills()
    # test_legislators()
    # test_clients()
    # lobbyview_invalid = LobbyView("invalid_token_kvhjeblhvbleihvbehibvfihleqbvihebivlebhl", test_connection=False)
    # lobbyview_invalid.get_data('/api/legislators')

    # lobbyview.get_data('/api/legislators?invalid_param=value')
    # for client in lobbyview.paginate(lobbyview.clients, client_name='InvalidClientName'):
    #     print(f"Client: {client['client_name']} - NAICS: {client['primary_naics']}")