import os
from dotenv import load_dotenv
import time

import sys
sys.path.append('./src/lobbyview/')
sys.path.append('../src/lobbyview/')
from LobbyView import LobbyView

load_dotenv("./.env")
load_dotenv("./tests/.env")
LOBBYVIEW_TOKEN = os.environ.get('LOBBYVIEW_TOKEN', "NO TOKEN FOUND")

lobbyview = LobbyView(LOBBYVIEW_TOKEN)

def test_legislators():
    output = lobbyview.legislators(legislator_first_name="John", legislator_last_name="McCain")
    assert output.data[0]['legislator_id'] == 'M000303'

    output = lobbyview.legislators(legislator_id="M000303")
    assert output.data[0]['legislator_full_name'] == 'John McCain'

def test_legislators_ranges():
    output = lobbyview.legislators(min_birthday="1900-01-01", max_birthday="1950-12-31")
    assert len(output.data) > 0

def test_bills():
    output = lobbyview.bills(congress_number=111, bill_chamber="H", bill_number=4173)
    assert output.data[0]['bill_state'] == 'ENACTED:SIGNED'

def test_bills_ranges():
    output = lobbyview.bills(min_introduced_date="2009-01-01", max_introduced_date="2009-12-31")
    assert len(output.data) > 0

def test_clients():
    output = lobbyview.clients(client_name="Microsoft Corporation")
    assert output.data[0]['client_uuid'] == '44563806-56d2-5e99-84a1-95d22a7a69b3'

def test_clients_naics_ranges():
    output = lobbyview.clients(min_naics='511209', max_naics='511211')
    assert len(output.data) > 0

def test_reports():
    output = lobbyview.reports(report_year=2020, report_quarter_code="2", is_client_self_filer=True, report_uuid="4b799814-3e94-5ee1-8dd4-b32aead9aca6")
    assert output.data[0]['amount'] == '$11,680,000.00'

def test_reports_amount_ranges():
    output = lobbyview.reports(min_amount='1000000', max_amount='100000000')
    assert len(output.data) > 0

def test_issues():
    output = lobbyview.issues(issue_code="TRD")
    assert len(output.data) > 0

def test_networks():
    output = lobbyview.networks(client_uuid="44563806-56d2-5e99-84a1-95d22a7a69b3", legislator_id="M000303")
    assert output.data[0]['report_year'] == 2017

def test_networks_ranges():
    output = lobbyview.networks(min_report_year=2015, max_report_year=2020, min_bills_sponsored=1)
    assert len(output.data) > 0

def test_texts():
    output = lobbyview.texts(issue_code="HCR", issue_text="covid")
    assert len(output.data) > 0

def test_quarter_level_networks():
    output = lobbyview.quarter_level_networks(client_uuid="44563806-56d2-5e99-84a1-95d22a7a69b3", legislator_id="M000303", report_year=2017, report_quarter_code=4)
    assert output.data[0]['n_bills_sponsored'] == 1

def test_quarter_level_networks_ranges():
    output = lobbyview.quarter_level_networks(min_bills_sponsored=1, max_bills_sponsored=5)
    assert len(output.data) > 0

def test_bill_client_networks():
    output = lobbyview.bill_client_networks(congress_number=114, bill_chamber="H", bill_number=1174, client_uuid="44563806-56d2-5e99-84a1-95d22a7a69b3")
    assert output.data[0]['issue_ordi'] == 2

if __name__ == "__main__":
    test_legislators()
    test_legislators_ranges()
    test_bills()
    test_bills_ranges()
    test_clients()
    test_clients_naics_ranges()
    test_reports()
    test_reports_amount_ranges()
    test_issues()
    test_networks()
    test_networks_ranges()
    test_texts()
    test_quarter_level_networks()
    test_quarter_level_networks_ranges()
    test_bill_client_networks()