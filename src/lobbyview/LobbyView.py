import http.client
import json
from dotenv import load_dotenv
import os

class LobbyView():
    def __init__(self, lobbyview_token):
        self.lobbyview_token = lobbyview_token
        self.connection = http.client.HTTPSConnection('rest-api.lobbyview.org')
        self.headers = {
            'token': self.lobbyview_token,
        }

        self.get_data('/api/legislators') # test connection
 
    def get_data(self, query_string):
        try:
            self.connection.request('GET', query_string, None, self.headers)
            response = self.connection.getresponse()
            data_string = response.read().decode('utf-8')
            data = json.loads(data_string)

            return data
        except:
            raise Exception("Unsuccessful Connection to LobbyView Endpoints. Please check your token and try again.")
    
    def legislators(self, legislator_id=None, legislator_govtrack_id=None, 
                        legislator_other_ids=None, legislator_first_name=None, 
                        legislator_last_name=None, legislator_full_name=None, 
                        legislator_other_names=None, legislator_birthday=None, 
                        legislator_gender=None):

        '''
        Gets legislator information from the LobbyView API based on params

        >>> output = lobbyview.legislators(legislator_first_name="John", legislator_last_name="McCain")
        >>> output['data'][0]['legislator_id']
        'M000303'
        >>> output = lobbyview.legislators(legislator_id="M000303")
        >>> output['data'][0]['legislator_full_name']
        'John McCain'
        '''
        
        query_params = []
        if legislator_id:
            query_params.append(f'legislator_id=eq.{legislator_id}')
        if legislator_govtrack_id:
            query_params.append(f'legislator_govtrack_id=eq.{legislator_govtrack_id}')
        if legislator_other_ids:
            query_params.append(f'legislator_other_ids=eq.{legislator_other_ids}')
        if legislator_first_name:
            query_params.append(f'legislator_first_name=eq.{legislator_first_name}')
        if legislator_last_name:
            query_params.append(f'legislator_last_name=eq.{legislator_last_name}')
        if legislator_full_name:
            query_params.append(f'legislator_full_name=eq.{legislator_full_name}')
        if legislator_other_names:
            query_params.append(f'legislator_other_names=eq.{legislator_other_names}')
        if legislator_birthday:
            query_params.append(f'legislator_birthday=eq.{legislator_birthday}')
        if legislator_gender:
            query_params.append(f'legislator_gender=eq.{legislator_gender}')
        
        query_string = '&'.join(query_params)
        data = self.get_data(f'/api/legislators?{query_string}')

        return data
    
    def bills(self, congress_number=None, bill_chamber=None, 
              bill_resolution_type=None, bill_number=None, bill_introduced_datetime=None, 
              bill_date_updated=None, bill_state=None, legislator_id=None, bill_url=None):

        '''
        Gets bills information from the LobbyView API based on params

        >>> pass
        '''

        query_params = []
        if congress_number:
            query_params.append(f'congress_number=eq.{congress_number}')
        if bill_chamber:
            query_params.append(f'bill_chamber=eq.{bill_chamber}')
        if bill_resolution_type:
            query_params.append(f'bill_resolution_type=eq.{bill_resolution_type}')
        if bill_number:
            query_params.append(f'bill_number=eq.{bill_number}')
        if bill_introduced_datetime:
            query_params.append(f'bill_introduced_datetime=eq.{bill_introduced_datetime}')
        if bill_date_updated:
            query_params.append(f'bill_date_updated=eq.{bill_date_updated}')
        if bill_state:
            query_params.append(f'bill_state=eq.{bill_state}')
        if legislator_id:
            query_params.append(f'legislator_id=eq.{legislator_id}')
        if bill_url:
            query_params.append(f'bill_url=eq.{bill_url}')
        
        query_string = '&'.join(query_params)
        data = self.get_data(f'/api/bills?{query_string}')

        return data

    def clients(self, client_uuid=None, client_name=None, 
                    primary_naics=None, naics_description=None):
       
        '''
        Gets clients information from the LobbyView API based on params

        >>> pass
        '''
    
        query_params = []
        if client_uuid:
            query_params.append(f'client_uuid=eq.{client_uuid}')
        if client_name:
            query_params.append(f'client_name=eq.{client_name}')
        if primary_naics:
            query_params.append(f'primary_naics=eq.{primary_naics}')
        if naics_description:
            query_params.append(f'naics_description=eq.{naics_description}')
        
        query_string = '&'.join(query_params)
        data = self.get_data(f'/api/clients?{query_string}')

        return data

    def reports(self, report_uuid=None, client_uuid=None, registrant_uuid=None, 
            registrant_name=None, report_year=None, report_quarter_code=None, 
            amount=None, is_no_activity=None, is_client_self_filer=None, is_amendment=None):

        '''
        Gets report information from the LobbyView API based on params

        >>> pass
        '''

        query_params = []
        if report_uuid:
            query_params.append(f'report_uuid=eq.{report_uuid}')
        if client_uuid:
            query_params.append(f'client_uuid=eq.{client_uuid}')
        if registrant_uuid:
            query_params.append(f'registrant_uuid=eq.{registrant_uuid}')
        if registrant_name:
            query_params.append(f'registrant_name=eq.{registrant_name}')
        if report_year:
            query_params.append(f'report_year=eq.{report_year}')
        if report_quarter_code:
            query_params.append(f'report_quarter_code=eq.{report_quarter_code}')
        if amount:
            query_params.append(f'amount=eq.{amount}')
        if is_no_activity:
            query_params.append(f'is_no_activity=eq.{is_no_activity}')
        if is_client_self_filer:
            query_params.append(f'is_client_self_filer=eq.{is_client_self_filer}')
        if is_amendment:
            query_params.append(f'is_amendment=eq.{is_amendment}')
        
        query_string = '&'.join(query_params)
        data = self.get_data(f'/api/reports?{query_string}')

        return data

    def issues(self, report_uuid=None, issue_ordi=None, issue_code=None, gov_entity=None):

        '''
        Gets issues information from the LobbyView API based on params

        >>> pass
        '''

        query_params = []
        if report_uuid:
            query_params.append(f'report_uuid=eq.{report_uuid}')
        if issue_ordi:
            query_params.append(f'issue_ordi=eq.{issue_ordi}')
        if issue_code:
            query_params.append(f'issue_code=eq.{issue_code}')
        if gov_entity:
            query_params.append(f'gov_entity=eq.{gov_entity}')
        
        query_string = '&'.join(query_params)
        data = self.get_data(f'/api/issues?{query_string}')

        return data

    def networks(self, client_uuid=None, legislator_id=None, report_year=None, n_bills_sponsored=None):

        '''
        Gets network information from the LobbyView API based on params

        >>> pass
        '''

        query_params = []
        if client_uuid:
            query_params.append(f'client_uuid=eq.{client_uuid}')
        if legislator_id:
            query_params.append(f'legislator_id=eq.{legislator_id}')
        if report_year:
            query_params.append(f'report_year=eq.{report_year}')
        if n_bills_sponsored:
            query_params.append(f'n_bills_sponsored=eq.{n_bills_sponsored}')
        
        query_string = '&'.join(query_params)
        data = self.get_data(f'/api/networks?{query_string}')

        return data

    def texts(self, report_uuid=None, issue_ordi=None, issue_code=None, issue_text=None):

        '''
        Gets issue text data from the LobbyView API based on params

        >>> pass
        '''

        query_params = []
        if report_uuid:
            query_params.append(f'report_uuid=eq.{report_uuid}')
        if issue_ordi:
            query_params.append(f'issue_ordi=eq.{issue_ordi}')
        if issue_code:
            query_params.append(f'issue_code=eq.{issue_code}')
        if issue_text:
            query_params.append(f'issue_text=eq.{issue_text}')
        
        query_string = '&'.join(query_params)
        data = self.get_data(f'/api/texts?{query_string}')

        return data

    def quarter_level_networks(self, client_uuid=None, legislator_id=None, report_year=None, report_quarter_code=None, n_bills_sponsored=None):

        '''
        Gets quarter-level network information from the LobbyView API based on params

        >>> pass
        '''

        query_params = []
        if client_uuid:
            query_params.append(f'client_uuid=eq.{client_uuid}')
        if legislator_id:
            query_params.append(f'legislator_id=eq.{legislator_id}')
        if report_year:
            query_params.append(f'report_year=eq.{report_year}')
        if report_quarter_code:
            query_params.append(f'report_quarter_code=eq.{report_quarter_code}')
        if n_bills_sponsored:
            query_params.append(f'n_bills_sponsored=eq.{n_bills_sponsored}')
        
        query_string = '&'.join(query_params)
        data = self.get_data(f'/api/quarter_level_networks?{query_string}')

        return data

    def bill_client_networks(self, congress_number=None, bill_chamber=None, 
                         bill_resolution_type=None, bill_number=None, 
                         report_uuid=None, issue_ordi=None, client_uuid=None):

        '''
        Gets bill-client network information from the LobbyView API based on params

        >>> pass
        '''

        query_params = []
        if congress_number:
            query_params.append(f'congress_number=eq.{congress_number}')
        if bill_chamber:
            query_params.append(f'bill_chamber=eq.{bill_chamber}')
        if bill_resolution_type:
            query_params.append(f'bill_resolution_type=eq.{bill_resolution_type}')
        if bill_number:
            query_params.append(f'bill_number=eq.{bill_number}')
        if report_uuid:
            query_params.append(f'report_uuid=eq.{report_uuid}')
        if issue_ordi:
            query_params.append(f'issue_ordi=eq.{issue_ordi}')
        if client_uuid:
            query_params.append(f'client_uuid=eq.{client_uuid}')
        
        query_string = '&'.join(query_params)
        data = self.get_data(f'/api/bill_client_networks?{query_string}')

        return data

if __name__ == "__main__":
    load_dotenv("tests/.env")
    load_dotenv("../../tests/.env")
    hard_code_token = "eyJhbGciOiJSUzI1NiIsImtpZCI6IjNiYjg3ZGNhM2JjYjY5ZDcyYjZjYmExYjU5YjMzY2M1MjI5N2NhOGQiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJodHRwczovL3NlY3VyZXRva2VuLmdvb2dsZS5jb20vZ2l0aHViLTczNTA0IiwiYXVkIjoiZ2l0aHViLTczNTA0IiwiYXV0aF90aW1lIjoxNzA5MDU4MjgwLCJ1c2VyX2lkIjoiZ0I3SzV2eU5MbFJLUXlzTTdjVHNObDZuRmc3MiIsInN1YiI6ImdCN0s1dnlOTGxSS1F5c003Y1RzTmw2bkZnNzIiLCJpYXQiOjE3MDkwODg0NTEsImV4cCI6MTcwOTA5MjA1MSwiZW1haWwiOiJueGxpdUBtaXQuZWR1IiwiZW1haWxfdmVyaWZpZWQiOmZhbHNlLCJmaXJlYmFzZSI6eyJpZGVudGl0aWVzIjp7ImVtYWlsIjpbIm54bGl1QG1pdC5lZHUiXX0sInNpZ25faW5fcHJvdmlkZXIiOiJwYXNzd29yZCJ9fQ.hAJbd95baBgmxqDEu9dKrfGCS9lyUir9-BJmpLUDuzGK2zFfntg6omgEhb5xVVyGVeA_HHr7dS-VPo0QjqKjcJFDIx5GU9HGpZx-a5-Ky4nHhEqZtHda1QHA0MRSlNww-lkf5Rl2yIhk4S8RAr9p7rp3Ru_5YNasgawtHJYQTXcLWh84r21pnKe7j1HnazvteM0C2KmMOE6wffSX-3VgZzTUr6ks6pjz7iJHEjaGUC0mPKawFSGsghDmVn7M7RPRcM5ge_we8TBQmq34NT8jA4j50yn7SKi3AWcI7dGLax_atI9xKCH1ubMZMr9QkUR-VqpXoxuvHcXIve-l9XNLyw:gB7K5vyNLlRKQysM7cTsNl6nFg72"
    LOBBYVIEW_TOKEN = os.environ.get('LOBBYVIEW_TOKEN', hard_code_token)

    import doctest
    results = doctest.testmod(extraglobs={'lobbyview': LobbyView(LOBBYVIEW_TOKEN)})
    results_string = f"{results.attempted-results.failed}/{results.attempted} TESTS PASSED"
    if results.failed == 0:
        print(results_string)
    else:
        raise Exception(results_string)