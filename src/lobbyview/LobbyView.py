'''
This module provides a Python interface to the LobbyView REST API. It uses the same endpoints
and
parameter names as outlined in the LobbyView REST API Documentation
(https://rest-api.lobbyview.org/).

The LobbyView API provides comprehensive data on lobbying activities in the United States.
This includes information on:

- Legislators: Details about the individuals involved in the legislative process.
- Bills: Information about proposed laws and their progress.
- Clients: Data on the entities that lobbyists represent.
- Reports: Detailed reports on lobbying activities.
- Issues: Government issues/areas that get lobbied on.
- Networks: Connections and relationships in lobbying.
- Texts: Written documents related to lobbying.
- Quarter-level networks: Lobbying networks on a quarterly basis.
- Bill-client networks: Connections between bills and the clients they affect.

This module also defines several custom exceptions to handle errors that may occur when
interacting with the LobbyView API.
'''
import http.client
import json
import os
import ssl
import doctest
from dotenv import load_dotenv

class LobbyViewError(Exception):
    """
    Base class for LobbyView API errors.
    """
    def __str__(self):
        """
        :return str: Name of the class
        """
        return self.__class__.__name__

class UnauthorizedError(LobbyViewError):
    """
    Raised when the API token is invalid or unauthorized.
    """
    def __init__(self):
        super().__init__()

class TooManyRequestsError(LobbyViewError):
    """
    Raised when the API rate limit is exceeded.
    """
    def __init__(self):
        super().__init__()

class PartialContentError(LobbyViewError):
    """
    Raised when the API returns a partial response.
    """
    def __init__(self):
        super().__init__()

class UnexpectedStatusCodeError(LobbyViewError):
    """
    Raised when the API returns an unexpected status code.
    """
    def __init__(self):
        super().__init__()

class InvalidPageNumberError(LobbyViewError):
    """
    Raised when the current page number is greater than the total number of pages.
    """
    def __init__(self):
        super().__init__()

class RequestError(LobbyViewError):
    """
    Raised when an error occurs during the request to the LobbyView API.
    """
    def __init__(self):
        super().__init__()

class LobbyViewResponse:
    """
    Base class for LobbyView API responses.
    """
    def __init__(self, data):
        """
        Initializes the LobbyViewResponse object with the provided JSON data.

        :param dict data: JSON data from the LobbyView API response
        :raises InvalidPageNumberError: If the current page number is greater than the total number
            of pages

        >>> data = {
        ...     'data': [],
        ...     'currentPage': 2,
        ...     'totalPage': 1,
        ...     'totalNumber': 0
        ... }
        >>> response = LobbyViewResponse(data)
        Traceback (most recent call last):
        ...
        InvalidPageNumberError: InvalidPageNumberError
        """
        self.data = data['data']                     # the actual data
        self.current_page = int(data['currentPage']) # current page number
        self.total_pages = int(data['totalPage'])    # total pages available
        self.total_rows = int(data['totalNumber'])   # total rows available (not the number
                                                     # of rows in the response)

        if self.current_page > self.total_pages:
            raise InvalidPageNumberError()

    def __str__(self):
        """
        :return str: JSON data formatted with indentation

        >>> data = {
        ...     'data': [{'name': 'Alice'}, {'name': 'Bob'}],
        ...     'currentPage': 1,
        ...     'totalPage': 1,
        ...     'totalNumber': 2
        ... }
        >>> response = LobbyViewResponse(data)
        >>> print(response)
        [
          {
            "name": "Alice"
          },
          {
            "name": "Bob"
          }
        ]
        """
        return json.dumps(self.data, indent=2)

    def __iter__(self):
        """
        :return: Iterator for the data

        >>> data = {
        ...     'data': [{'name': 'Alice'}, {'name': 'Bob'}],
        ...     'currentPage': 1,
        ...     'totalPage': 1,
        ...     'totalNumber': 2
        ... }
        >>> response = LobbyViewResponse(data)
        >>> for item in response:
        ...     print(item)
        {'name': 'Alice'}
        {'name': 'Bob'}
        """
        return iter(self.data)

    def page_info(self):
        """
        :return str: Current page number, total pages, and total rows

        >>> data = {
        ...     'data': [],
        ...     'currentPage': 1,
        ...     'totalPage': 2,
        ...     'totalNumber': 0
        ... }
        >>> response = LobbyViewResponse(data)
        >>> print(response.page_info())
        Current Page: 1
        Total Pages: 2
        Total Rows: 0
        """
        return f"Current Page: {self.current_page}\nTotal Pages: {self.total_pages}\nTotal Rows: {self.total_rows}"

class LegislatorResponse(LobbyViewResponse):
    """
    Response class for legislator data.
    """
    def __str__(self):
        """
        :return str: representation of the legislator data
            which includes the legislator's full name and ID
        """
        output = "Legislators:\n"
        # uses self because LobbyViewResponse is a parent class with an iter method
        for legislator in self:
            output += f"  {legislator['legislator_full_name']} (ID: {legislator['legislator_id']})\n"
        # remove the trailing newline character
        return output.rstrip()

class BillResponse(LobbyViewResponse):
    """
    Response class for bill data.
    """
    def __str__(self):
        """
        :return str: representation of the bill data
            which includes the bill number, Congress number, and sponsor ID
        """
        output = "Bills:\n"
        for bill in self:
            output += f"  {bill['bill_number']} (Congress: {bill['congress_number']}, Sponsor: {bill['legislator_id']})\n"
        return output.rstrip()

class ClientResponse(LobbyViewResponse):
    """
    Response class for client data.
    """
    def __str__(self):
        """
        :return str: representation of the client data
            which includes the client name and ID
        """
        output = "Clients:\n"
        for client in self:
            output += f"  {client['client_name']} (ID: {client['client_uuid']})\n"
        return output.rstrip()

class ReportResponse(LobbyViewResponse):
    """
    Response class for report data.
    """
    def __str__(self):
        """
        :return str: representation of the report data
            which includes the report UUID, year, and quarter
        """
        output = "Reports:\n"
        for report in self:
            output += f"  {report['report_uuid']} (Year: {report['report_year']}, Quarter: {report['report_quarter_code']})\n"
        return output.rstrip()

class IssueResponse(LobbyViewResponse):
    """
    Response class for issue data.
    """
    def __str__(self):
        """
        :return str: representation of the issue data
            which includes the issue code, report UUID, and issue ordi
        """
        output = "Issues:\n"
        for issue in self:
            output += f"  {issue['issue_code']} (Report UUID: {issue['report_uuid']}, Issue Ordi: {issue['issue_ordi']})\n"
        return output.rstrip()

class NetworkResponse(LobbyViewResponse):
    """
    Response class for network data.
    """
    def __str__(self):
        """
        :returnstr : representation of the network data
            which includes the client UUID, legislator ID, year, and number of bills sponsored
        """
        output = "Networks:\n"
        for network in self:
            output += f"  Client UUID: {network['client_uuid']}, Legislator ID: {network['legislator_id']}, Year: {network['report_year']}, Bills Sponsored: {network['n_bills_sponsored']}\n"
        return output.rstrip()

class TextResponse(LobbyViewResponse):
    """
    Response class for text data.
    """
    def __str__(self):
        """
        :return str: representation of the text data
            which includes the issue code and text
        """
        output = "Texts:\n"
        for text in self:
            output += f"  Issue Code: {text['issue_code']}, Issue Text: {text['issue_text']}\n"
        return output.rstrip()

class QuarterLevelNetworkResponse(LobbyViewResponse):
    """
    Response class for quarter-level network data.
    """
    def __str__(self):
        """
        :return str: representation of the quarter-level network data
            which includes the client UUID, legislator ID, year, quarter, and 
            number of bills sponsored
        """
        output = "Quarter-Level Networks:\n"
        for network in self:
            output += f"  Client UUID: {network['client_uuid']}, Legislator ID: {network['legislator_id']}, Year: {network['report_year']}, Quarter: {network['report_quarter_code']}, Bills Sponsored: {network['n_bills_sponsored']}\n"
        return output.rstrip()

class BillClientNetworkResponse(LobbyViewResponse):
    """
    Response class for bill-client network data.
    """
    def __str__(self):
        """
        :return str: representation of the bill-client network data
            which includes the bill number, client UUID, and issue ordi
        """
        output = "Bill-Client Networks:\n"
        for network in self:
            output += f"  Bill Number: {network['bill_number']}, Client UUID: {network['client_uuid']}, Issue Ordi: {network['issue_ordi']}\n"
        return output.rstrip()

class LobbyView:
    """
    Main class for interacting with the LobbyView API.
    """
    def __init__(self, lobbyview_token, test_connection=True):
        """
        Initialize the LobbyView class with the provided API token.

        :param str lobbyview_token: API token for the LobbyView API
        :param bool test_connection: Whether to test the connection to the API
        """
        self.lobbyview_token = lobbyview_token
        # self.connection = http.client.HTTPSConnection('rest-api.lobbyview.org')

        context = ssl._create_unverified_context()
        # temporary connection to test API with unlimited token
        self.connection = http.client.HTTPSConnection(
            "lobbyview-rest-api-test.eba-witbq7ed.us-east-1.elasticbeanstalk.com", 
            context=context
            )

        self.headers = {
            'token': self.lobbyview_token,
        }

        if test_connection:
            try:
                self.get_data('/api/legislators')
            except Exception as exc:
                print(f"Warning: Connection test failed - {str(exc)}")

    def get_data(self, query_string):
        """
        Sends a GET request to the LobbyView API with the provided query string.
        Returns the JSON response data.

        :param str query_string: Query string for the API endpoint
        :return dict: JSON data from the API response
        :raises UnauthorizedError: If the API returns a 401 Unauthorized status code
        :raises TooManyRequestsError: If the API returns a 429 Too Many Requests status
            code
        :raises PartialContentError: If the API returns a 206 Partial Content status code
        :raises UnexpectedStatusCodeError: If the API returns an unexpected status code
        :raises RequestError: If an error occurs during the request

        >>> lobbyview = LobbyView("invalid_token", test_connection=False)
        >>> lobbyview.get_data('/api/legislators')
        Traceback (most recent call last):
        ...
        UnauthorizedError: UnauthorizedError

        >>> lobbyview = LobbyView(LOBBYVIEW_TOKEN)
        >>> lobbyview.get_data('/api/invalid_endpoint')
        Traceback (most recent call last):
        ...
        UnexpectedStatusCodeError: UnexpectedStatusCodeError

        >>> lobbyview = LobbyView(LOBBYVIEW_TOKEN)
        >>> lobbyview.get_data('/api/legislators?invalid_param=value')
        Traceback (most recent call last):
        ...
        UnexpectedStatusCodeError: UnexpectedStatusCodeError
        """
        try:
            query_string = query_string.replace(" ", "%20")
            self.connection.request('GET', query_string, None, self.headers)
            response = self.connection.getresponse()
            status_code = response.status

            if status_code == 200:
                data_string = response.read().decode('utf-8')
                # use json.loads to convert the string to a dictionary
                return json.loads(data_string)
            if status_code == 401:
                raise UnauthorizedError()
            if status_code == 429:
                raise TooManyRequestsError()
            if status_code == 206:
                raise PartialContentError()
            raise UnexpectedStatusCodeError()
        except (UnauthorizedError, TooManyRequestsError,
                PartialContentError, UnexpectedStatusCodeError):
            raise
        except Exception as exc:
            # error occurred during the request
            raise RequestError() from exc

    def paginate(self, func, **kwargs):
        """
        Paginates the data retrieval from the LobbyView API using lazy evaluation
        via a genrator that yields results one at a time.

        :param function func: The API endpoint function to be paginated.
        :param dict kwargs: Additional keyword arguments to be passed to the API endpoint
            function.
        :return: A generator object that yields paginated results one item at a time.
        :raises PartialContentError: If the API returns a 206 Partial Content status code
        :raises LobbyViewError: If a different error occurs during pagination

        example usage:

        for legislator in lobbyview.paginate(lobbyview.legislators, legislator_state='CA'):
            print(f'Legislator: {legislator['legislator_full_name']}')

        for bill in lobbyview.paginate(lobbyview.bills, congress_number=117, bill_resolution_type='hr'):
            print(f'Bill: {bill['bill_number']} - {bill['bill_title']}')

        for client in lobbyview.paginate(lobbyview.clients, client_name='Microsoft', min_naics=500000):
            print(f'Client: {client['client_name']} - NAICS: {client['primary_naics']}')

        >>> lobbyview = LobbyView(LOBBYVIEW_TOKEN)
        >>> for legislator in lobbyview.paginate(lobbyview.legislators, legislator_first_name="John", legislator_last_name="McCain"):
        ...     print(f"Legislator: {legislator['legislator_full_name']}")
        Retrieving page 1...
        Legislator: John McCain

        >>> for bill in lobbyview.paginate(lobbyview.bills, congress_number=111, bill_chamber="H", bill_number=4173):
        ...     print(f"Bill: {bill['bill_number']} - {bill['bill_chamber']}")
        Retrieving page 1...
        Bill: 4173 - H

        >>> for client in lobbyview.paginate(lobbyview.clients, client_name='InvalidClientName'):
        ...     print(f"Client: {client['client_name']} - NAICS: {client['primary_naics']}")
        Retrieving page 1...
        Error occurred: InvalidPageNumberError

        >>> lobbyview = LobbyView(LOBBYVIEW_TOKEN)
        >>> for network in lobbyview.paginate(lobbyview.bill_client_networks, congress_number=114, bill_chamber="H", bill_number=1174, client_uuid="44563806-56d2-5e99-84a1-95d22a7a69b3"):
        ...     print(f"Issue Ordi: {network['issue_ordi']}")
        Retrieving page 1...
        Issue Ordi: 2
        Issue Ordi: 5
        Issue Ordi: 4
        ...

        >>> lobbyview = LobbyView(LOBBYVIEW_TOKEN)
        >>> for text in lobbyview.paginate(lobbyview.texts, issue_code="HCR", issue_text="covid"):
        ...     print(f"Issue Code: {text['issue_code']}")
        Retrieving page 1...
        Issue Code: HCR
        Issue Code: HCR
        Issue Code: HCR
        Issue Code: HCR
        Issue Code: HCR
        Issue Code: HCR
        Issue Code: HCR
        Issue Code: HCR
        Issue Code: HCR
        Issue Code: HCR
        Issue Code: HCR
        Issue Code: HCR
        Issue Code: HCR
        Issue Code: HCR
        Issue Code: HCR
        Issue Code: HCR
        Issue Code: HCR
        Issue Code: HCR
        Issue Code: HCR
        Issue Code: HCR
        Issue Code: HCR
        Issue Code: HCR
        Issue Code: HCR
        Issue Code: HCR
        Issue Code: HCR
        Issue Code: HCR
        Issue Code: HCR
        Issue Code: HCR
        Issue Code: HCR
        Issue Code: HCR
        Issue Code: HCR
        Issue Code: HCR
        Issue Code: HCR
        Issue Code: HCR
        Issue Code: HCR
        Issue Code: HCR
        Issue Code: HCR
        Issue Code: HCR
        Issue Code: HCR
        Issue Code: HCR
        Issue Code: HCR
        Issue Code: HCR
        Issue Code: HCR
        Issue Code: HCR
        Issue Code: HCR
        Issue Code: HCR
        Issue Code: HCR
        Issue Code: HCR
        Issue Code: HCR
        Issue Code: HCR
        Issue Code: HCR
        Issue Code: HCR
        Issue Code: HCR
        Issue Code: HCR
        Issue Code: HCR
        Issue Code: HCR
        Issue Code: HCR
        Issue Code: HCR
        Issue Code: HCR
        Issue Code: HCR
        Issue Code: HCR
        Issue Code: HCR
        Issue Code: HCR
        Issue Code: HCR
        Issue Code: HCR
        Issue Code: HCR
        Issue Code: HCR
        Issue Code: HCR
        Issue Code: HCR
        Issue Code: HCR
        Issue Code: HCR
        Issue Code: HCR
        Issue Code: HCR
        Issue Code: HCR
        Issue Code: HCR
        Issue Code: HCR
        Issue Code: HCR
        Issue Code: HCR
        Issue Code: HCR
        Issue Code: HCR
        Issue Code: HCR
        Issue Code: HCR
        Issue Code: HCR
        Issue Code: HCR
        Issue Code: HCR
        Issue Code: HCR
        Issue Code: HCR
        Issue Code: HCR
        Issue Code: HCR
        Issue Code: HCR
        Issue Code: HCR
        Issue Code: HCR
        Issue Code: HCR
        Issue Code: HCR
        Issue Code: HCR
        Issue Code: HCR
        Issue Code: HCR
        Issue Code: HCR
        Issue Code: HCR
        Issue Code: HCR
        Retrieving page 2...
        Issue Code: HCR
        Issue Code: HCR
        Issue Code: HCR
        Issue Code: HCR
        ...
        """
        page = 1

        while True:
            print(f"Retrieving page {page}...")
            kwargs['page'] = page

            try:
                # unpack the keyword arguments and call the function
                response = func(**kwargs)
                yield from response.data

                if page >= response.total_pages:
                    break

                page += 1

            except PartialContentError as exc:
                print(f"Error occurred: {str(exc)}")
                print("Partial results retrieved. Please wait for more quota.")
                break
            except LobbyViewError as exc:
                print(f"Error occurred: {str(exc)}")
                break

    def legislators(self, legislator_id=None, legislator_govtrack_id=None,
                        legislator_first_name=None, legislator_last_name=None,
                        legislator_full_name=None, legislator_gender=None,
                        min_birthday=None, max_birthday=None, page=1):
        """
        Gets legislator information from the LobbyView API based on the provided
        parameters.

        :param str legislator_id: Unique identifier of the legislator from LobbyView
        :param str legislator_govtrack_id: Unique identifier of the legislator from
            GovTrack
        :param str legislator_first_name: First name of the legislator
        :param str legislator_last_name: Last name of the legislator
        :param str legislator_full_name: Full name of the legislator
        :param str legislator_gender: Gender of the legislator
        :param str min_birthday: Minimum birthday of the legislator (YYYY-MM-DD)
        :param str max_birthday: Maximum birthday of the legislator (YYYY-MM-DD)
        :param int page: Page number of the results, default is 1
        :return: LegislatorResponse object containing the legislator data

        >>> lobbyview = LobbyView(LOBBYVIEW_TOKEN)
        >>> output = lobbyview.legislators(legislator_first_name="John", legislator_last_name="McCain")
        >>> output.data[0]['legislator_id']
        'M000303'
        >>> output = lobbyview.legislators(legislator_id="M000303")
        >>> output.data[0]['legislator_full_name']
        'John McCain'

        >>> output = lobbyview.legislators(legislator_first_name="John", legislator_last_name="McCain")
        >>> print(output)
        Legislators:
          John McCain (ID: M000303)

        >>> output = lobbyview.legislators(legislator_govtrack_id=412755, legislator_full_name="TJ Cox", legislator_gender="M", min_birthday="1963-03-14", max_birthday="1963-08-14")
        >>> print(output)
        Legislators:
          TJ Cox (ID: C001124)
        """
        query_params = []
        if legislator_id:
            query_params.append(f'legislator_id=eq.{legislator_id}')
        if legislator_govtrack_id:
            query_params.append(f'legislator_govtrack_id=eq.{legislator_govtrack_id}')
        if legislator_first_name:
            query_params.append(f'legislator_first_name=ilike.*{legislator_first_name}*')
        if legislator_last_name:
            query_params.append(f'legislator_last_name=ilike.*{legislator_last_name}*')
        if legislator_full_name:
            query_params.append(f'legislator_full_name=ilike.*{legislator_full_name}*')
        if legislator_gender:
            query_params.append(f'legislator_gender=eq.{legislator_gender}')
        if min_birthday:
            query_params.append(f'legislator_birthday=gte.{min_birthday}')
        if max_birthday:
            query_params.append(f'legislator_birthday=lte.{max_birthday}')
        if page != 1:
            query_params.append(f'page={page}')

        query_string = '&'.join(query_params)
        data = self.get_data(f'/api/legislators?{query_string}')

        return LegislatorResponse(data)

    def bills(self, congress_number=None, bill_chamber=None,
              bill_resolution_type=None, bill_number=None, bill_state=None,
              legislator_id=None, min_introduced_date=None, max_introduced_date=None,
              min_updated_date=None, max_updated_date=None, page=1):
        """
        Gets bill information from the LobbyView API based on the provided parameters.

        :param int congress_number: Session of Congress
        :param str bill_chamber: Chamber of the legislative branch
            (Component of the bill_id composite key)
        :param str bill_resolution_type: Bill type (Component of the bill_id composite 
            key)
        :param int bill_number: Bill number (Component of the bill_id composite key)
        :param str bill_state: Bill status
        :param str legislator_id: Sponsor of the bill
        :param str min_introduced_date: Minimum date of introduction to Congress
            (YYYY-MM-DD)
        :param str max_introduced_date: Maximum date of introduction to Congress
            (YYYY-MM-DD)
        :param str min_updated_date: Minimum date of most recent status change
            (YYYY-MM-DD)
        :param str max_updated_date: Maximum date of most recent status change
            (YYYY-MM-DD)
        :param int page: Page number of the results, default is 1
        :return: BillResponse object containing the bill data

        >>> lobbyview = LobbyView(LOBBYVIEW_TOKEN)
        >>> output = lobbyview.bills(congress_number=111, bill_chamber="H", bill_number=4173)
        >>> output.data[0]['bill_state']
        'ENACTED:SIGNED'

        >>> output = lobbyview.bills(congress_number=111, bill_chamber="H", bill_number=4173)
        >>> print(output)
        Bills:
          4173 (Congress: 111, Sponsor: F000339)
        """
        query_params = []
        if congress_number:
            query_params.append(f'congress_number=eq.{congress_number}')
        if bill_chamber:
            query_params.append(f'bill_chamber=eq.{bill_chamber}')
        if bill_resolution_type:
            query_params.append(f'bill_resolution_type=eq.{bill_resolution_type}') #!?
        if bill_number:
            query_params.append(f'bill_number=eq.{bill_number}')
        if bill_state:
            query_params.append(f'bill_state=ilike.*{bill_state}*') #!?
        if legislator_id:
            query_params.append(f'legislator_id=eq.{legislator_id}') #!?
        if min_introduced_date:
            query_params.append(f'bill_introduced_datetime=gte.{min_introduced_date}') #!?
        if max_introduced_date:
            query_params.append(f'bill_introduced_datetime=lte.{max_introduced_date}') #!?
        if min_updated_date:
            query_params.append(f'bill_date_updated=gte.{min_updated_date}') #!?
        if max_updated_date:
            query_params.append(f'bill_date_updated=lte.{max_updated_date}') #!?
        if page != 1:
            query_params.append(f'page={page}')

        query_string = '&'.join(query_params)
        data = self.get_data(f'/api/bills?{query_string}')

        return BillResponse(data)

    def clients(self, client_uuid=None, client_name=None,
                    min_naics=None, max_naics=None, naics_description=None, page=1):
        """
        Gets client information from the LobbyView API based on the provided parameters.

        :param str client_uuid: Unique identifier of the client
        :param str client_name: Name of the client
        :param str min_naics: Minimum NAICS code to which the client belongs
        :param str max_naics: Maximum NAICS code to which the client belongs
        :param str naics_description: Descriptions of the NAICS code
        :param int page: Page number of the results, default is 1
        :return: ClientResponse object containing the client data

        >>> lobbyview = LobbyView(LOBBYVIEW_TOKEN)
        >>> output = lobbyview.clients(client_name="Microsoft Corporation")
        >>> output.data[0]['client_uuid']
        '44563806-56d2-5e99-84a1-95d22a7a69b3'

        >>> output = lobbyview.clients(client_name="Microsoft Corporation")
        >>> print(output)
        Clients:
          Microsoft Corporation (ID: 44563806-56d2-5e99-84a1-95d22a7a69b3)
          PCT Government Relations on behalf of Microsoft Corporation (ID: 62eb98f6-ea3a-542d-abdb-7d2fce94b4f8)
          Cornerstone Government Affairs obo Microsoft Corporation (ID: d6634602-1d0b-560d-b4ac-e04194782ad3)

        >>> output = lobbyview.clients(client_uuid='44563806-56d2-5e99-84a1-95d22a7a69b3', min_naics=511209, max_naics=511211, naics_description='Applications development and publishing')
        >>> print(output)
        Clients:
          Microsoft Corporation (ID: 44563806-56d2-5e99-84a1-95d22a7a69b3)
        """
        query_params = []
        if client_uuid:
            query_params.append(f'client_uuid=eq.{client_uuid}') #!?
        if client_name:
            query_params.append(f'client_name=ilike.*{client_name}*')
        if min_naics:
            query_params.append(f'primary_naics=gte.{min_naics}') #!?
        if max_naics:
            query_params.append(f'primary_naics=lte.{max_naics}') #!?
        if naics_description:
            query_params.append(f'naics_description=ilike.*{naics_description}*') #!?
        if page != 1:
            query_params.append(f'page={page}')

        query_string = '&'.join(query_params)
        data = self.get_data(f'/api/clients?{query_string}')

        return ClientResponse(data)

    def reports(self, report_uuid=None, client_uuid=None, registrant_uuid=None,
            registrant_name=None, report_year=None, report_quarter_code=None,
            min_amount=None, max_amount=None, is_no_activity=None,
            is_client_self_filer=None, is_amendment=None, page=1):
        """
        Gets report information from the LobbyView API based on the provided parameters.

        :param str report_uuid: Unique identifier of the report
        :param str client_uuid: Unique identifier of the client
        :param str registrant_uuid: Unique identifier of the registrant
        :param str registrant_name: Name of the registrant
        :param int report_year: Year of the report
        :param str report_quarter_code: Quarter period of the report
        :param str min_amount: Minimum lobbying firm income or lobbying expense
            (in-house)
        :param str max_amount: Maximum lobbying firm income or lobbying expense
            (in-house)
        :param bool is_no_activity: Quarterly activity indicator
        :param bool is_client_self_filer: An organization employing its own in-house
            lobbyist(s)
        :param bool is_amendment: Amendment of previous report
        :param int page: Page number of the results, default is 1
        :return: ReportResponse object containing the report data

        >>> lobbyview = LobbyView(LOBBYVIEW_TOKEN)
        >>> output = lobbyview.reports(report_year=2020, report_quarter_code="2", is_client_self_filer=True, report_uuid="4b799814-3e94-5ee1-8dd4-b32aead9aca6")
        >>> output.data[0]['amount']
        '$11,680,000.00'

        >>> output = lobbyview.reports(report_year=2020, report_quarter_code="2", is_client_self_filer=True, report_uuid="4b799814-3e94-5ee1-8dd4-b32aead9aca6")
        >>> print(output)
        Reports:
          4b799814-3e94-5ee1-8dd4-b32aead9aca6 (Year: 2020, Quarter: 2)
        """
        query_params = []
        if report_uuid:
            query_params.append(f'report_uuid=eq.{report_uuid}')
        if client_uuid:
            query_params.append(f'client_uuid=eq.{client_uuid}') #!?
        if registrant_uuid:
            query_params.append(f'registrant_uuid=eq.{registrant_uuid}') #!?
        if registrant_name:
            query_params.append(f'registrant_name=ilike.*{registrant_name}*') #!?
        if report_year:
            query_params.append(f'report_year=eq.{report_year}')
        if report_quarter_code:
            query_params.append(f'report_quarter_code=eq.{report_quarter_code}')
        if min_amount:
            query_params.append(f'amount=gte.{min_amount}') #!?
        if max_amount:
            query_params.append(f'amount=lte.{max_amount}') #!?
        if is_no_activity is not None:
            query_params.append(f'is_no_activity=eq.{is_no_activity}') #!?
        if is_client_self_filer is not None:
            query_params.append(f'is_client_self_filer=eq.{is_client_self_filer}')
        if is_amendment is not None:
            query_params.append(f'is_amendment=eq.{is_amendment}') #!?
        if page != 1:
            query_params.append(f'page={page}')

        query_string = '&'.join(query_params)
        data = self.get_data(f'/api/reports?{query_string}')

        return ReportResponse(data)

    def issues(self, report_uuid=None, issue_ordi=None, issue_code=None, gov_entity=None,
               page=1):
        """
        Gets issue information from the LobbyView API based on the provided parameters.

        :param str report_uuid: Unique identifier of the report
        :param int issue_ordi: An integer given to the issue
        :param str issue_code: General Issue Area Code (Section 15)
        :param str gov_entity: House(s) of Congress and Federal agencies (Section 17)
        :param int page: Page number of the results, default is 1
        :return: IssueResponse object containing the issue data

        >>> lobbyview = LobbyView(LOBBYVIEW_TOKEN)
        >>> output = lobbyview.issues(issue_code="TRD")
        >>> output.data[0]['report_uuid']
        '00016ab3-2246-5af8-a68d-05af40dfde68'

        >>> output = lobbyview.issues(issue_code="TRD")
        >>> print(output)
        Issues:
          TRD (Report UUID: 00016ab3-2246-5af8-a68d-05af40dfde68, Issue Ordi: 2)
          TRD (Report UUID: 0001f9b9-84d7-5ceb-af03-8987bb76d593, Issue Ordi: 1)
          TRD (Report UUID: 00020868-67be-5975-955d-7ecab8d42e6e, Issue Ordi: 2)
          TRD (Report UUID: 00040172-6cda-5b31-8d83-9c1bcfd4b289, Issue Ordi: 1)
          TRD (Report UUID: 00047fc7-2207-5f3b-951d-692b9f35825b, Issue Ordi: 1)
          TRD (Report UUID: 000759fa-dc93-5849-b1e5-7aa751e86433, Issue Ordi: 4)
        ...
        """
        query_params = []
        if report_uuid:
            query_params.append(f'report_uuid=eq.{report_uuid}')
        if issue_ordi:
            query_params.append(f'issue_ordi=eq.{issue_ordi}')
        if issue_code:
            query_params.append(f'issue_code=eq.{issue_code}')
        if gov_entity:
            query_params.append(f'gov_entity=ilike.*{gov_entity}*')
        if page != 1:
            query_params.append(f'page={page}')

        query_string = '&'.join(query_params)
        data = self.get_data(f'/api/issues?{query_string}')

        return IssueResponse(data)


    def networks(self, client_uuid=None, legislator_id=None, min_report_year=None,
                 max_report_year=None, min_bills_sponsored=None, max_bills_sponsored=None,
                 page=1):
        """
        Gets network information from the LobbyView API based on the provided parameters.

        :param str client_uuid: Unique identifier of the client
        :param str legislator_id: Unique identifier of the legislator
        :param int min_report_year: Minimum year of the report
        :param int max_report_year: Maximum year of the report
        :param int min_bills_sponsored: Minimum number of bills sponsored by the legislator
            in a specific year lobbied by the client
        :param int max_bills_sponsored: Maximum number of bills sponsored by the legislator
            in a specific year lobbied by the client
        :param int page: Page number of the results, default is 1
        :return: NetworkResponse object containing the network data

        >>> lobbyview = LobbyView(LOBBYVIEW_TOKEN)
        >>> output = lobbyview.networks(client_uuid="44563806-56d2-5e99-84a1-95d22a7a69b3", legislator_id="M000303")
        >>> output.data[0]['report_year']
        2006

        >>> output = lobbyview.networks(client_uuid="44563806-56d2-5e99-84a1-95d22a7a69b3", legislator_id="M000303")
        >>> print(output)
        Networks:
          Client UUID: 44563806-56d2-5e99-84a1-95d22a7a69b3, Legislator ID: M000303, Year: 2006, Bills Sponsored: 1
          Client UUID: 44563806-56d2-5e99-84a1-95d22a7a69b3, Legislator ID: M000303, Year: 2017, Bills Sponsored: 1

        >>> output = lobbyview.networks(min_report_year=2016, max_report_year=2018, min_bills_sponsored=0, max_bills_sponsored=2, client_uuid="44563806-56d2-5e99-84a1-95d22a7a69b3", legislator_id="M000303")
        >>> print(output)
        Networks:
          Client UUID: 44563806-56d2-5e99-84a1-95d22a7a69b3, Legislator ID: M000303, Year: 2017, Bills Sponsored: 1
        """
        query_params = []
        if client_uuid:
            query_params.append(f'client_uuid=eq.{client_uuid}')
        if legislator_id:
            query_params.append(f'legislator_id=eq.{legislator_id}')
        if min_report_year:
            query_params.append(f'report_year=gte.{min_report_year}') #!?
        if max_report_year:
            query_params.append(f'report_year=lte.{max_report_year}') #!?
        if min_bills_sponsored:
            query_params.append(f'n_bills_sponsored=gte.{min_bills_sponsored}') #!?
        if max_bills_sponsored:
            query_params.append(f'n_bills_sponsored=lte.{max_bills_sponsored}') #!?
        if page != 1:
            query_params.append(f'page={page}')

        query_string = '&'.join(query_params)
        data = self.get_data(f'/api/networks?{query_string}')

        return NetworkResponse(data)

    def texts(self, report_uuid=None, issue_ordi=None, issue_code=None, issue_text=None,
              page=1):
        """
        Gets issue text data from the LobbyView API based on the provided parameters.

        :param str report_uuid: Unique identifier of the report
        :param int issue_ordi: An integer given to the issue
        :param str issue_code: General Issue Area Code (Section 15)
        :param str issue_text: Specific lobbying issues (Section 16)
        :param int page: Page number of the results, default is 1
        :return: TextResponse object containing the text data

        >>> lobbyview = LobbyView(LOBBYVIEW_TOKEN)
        >>> output = lobbyview.texts(issue_code="HCR", issue_text="covid")
        >>> output.data[0]['issue_ordi']
        1

        >>> output = lobbyview.texts(issue_code="HCR", issue_text="covid")
        >>> print(output)
        Texts:
          Issue Code: HCR, Issue Text: HR 748 CARES Act - Issues related to COVID-19 relief
        ...

        >>> output = lobbyview.texts(report_uuid='000bef17-9f0a-5d7c-8660-edca16e1dfce', issdue_ordi=1)
        >>> print(output)
        Texts:
          Issue Code: HCR, Issue Text: HR 748 CARES Act - Issues related to COVID-19 relief
        """
        query_params = []
        if report_uuid:
            query_params.append(f'report_uuid=eq.{report_uuid}') #!?
        if issue_ordi:
            query_params.append(f'issue_ordi=eq.{issue_ordi}') #!?
        if issue_code:
            query_params.append(f'issue_code=eq.{issue_code}')
        if issue_text:
            query_params.append(f'issue_text=ilike.*{issue_text}*')
        if page != 1:
            query_params.append(f'page={page}')

        query_string = '&'.join(query_params)
        data = self.get_data(f'/api/texts?{query_string}')

        return TextResponse(data)

    def quarter_level_networks(self, client_uuid=None, legislator_id=None, report_year=None,
                               report_quarter_code=None, min_bills_sponsored=None,
                               max_bills_sponsored=None, page=1):
        """
        Gets quarter-level network information from the LobbyView API based on the provided
        parameters.

        :param str client_uuid: Unique identifier of the client
        :param str legislator_id: Unique identifier of the legislator
        :param int report_year: Year of the report
        :param str report_quarter_code: Quarter period of the report
        :param int min_bills_sponsored: Minimum number of bills sponsored by the legislator
            in a specific quarter lobbied by the client
        :param int max_bills_sponsored: Maximum number of bills sponsored by the legislator
            in a specific quarter lobbied by the client
        :param int page: Page number of the results, default is 1
        :return: QuarterLevelNetworkResponse object containing the quarter-level network data

        >>> lobbyview = LobbyView(LOBBYVIEW_TOKEN)
        >>> output = lobbyview.quarter_level_networks(client_uuid="44563806-56d2-5e99-84a1-95d22a7a69b3", legislator_id="M000303", report_year=2017, report_quarter_code=4)
        >>> output.data[0]['n_bills_sponsored']
        1

        >>> output = lobbyview.quarter_level_networks(client_uuid="44563806-56d2-5e99-84a1-95d22a7a69b3", legislator_id="M000303", report_year=2017, report_quarter_code=4)
        >>> print(output)
        Quarter-Level Networks:
          Client UUID: 44563806-56d2-5e99-84a1-95d22a7a69b3, Legislator ID: M000303, Year: 2017, Quarter: 4, Bills Sponsored: 1

        >>> output = lobbyview.quarter_level_networks(min_bills_sponsored=0, max_bills_sponsored=2, client_uuid="44563806-56d2-5e99-84a1-95d22a7a69b3", legislator_id="M000303")
        >>> print(output)
        Quarter-Level Networks:
          Client UUID: 44563806-56d2-5e99-84a1-95d22a7a69b3, Legislator ID: M000303, Year: 2006, Quarter: 34, Bills Sponsored: 1
          Client UUID: 44563806-56d2-5e99-84a1-95d22a7a69b3, Legislator ID: M000303, Year: 2017, Quarter: 4, Bills Sponsored: 1
        """
        query_params = []
        if client_uuid:
            query_params.append(f'client_uuid=eq.{client_uuid}')
        if legislator_id:
            query_params.append(f'legislator_id=eq.{legislator_id}')
        if report_year:
            query_params.append(f'report_year=eq.{report_year}')
        if report_quarter_code:
            query_params.append(f'report_quarter_code=eq.{report_quarter_code}')
        if min_bills_sponsored:
            query_params.append(f'n_bills_sponsored=gte.{min_bills_sponsored}') #!?
        if max_bills_sponsored:
            query_params.append(f'n_bills_sponsored=lte.{max_bills_sponsored}') #!?
        if page != 1:
            query_params.append(f'page={page}')

        query_string = '&'.join(query_params)
        data = self.get_data(f'/api/quarter_level_networks?{query_string}')

        return QuarterLevelNetworkResponse(data)

    def bill_client_networks(self, congress_number=None, bill_chamber=None,
                        bill_resolution_type=None, bill_number=None,
                        report_uuid=None, issue_ordi=None, client_uuid=None, page=1):
        """
        Gets bill-client network information from the LobbyView API based on the provided
        parameters.

        :param int congress_number: Session of Congress
        :param str bill_chamber: Chamber of the legislative branch (Component of the
            bill_id composite key)
        :param str bill_resolution_type: Bill type (Component of the bill_id composite key)
        :param int bill_number: Bill number (Component of the bill_id composite key)
        :param str report_uuid: Unique identifier of the report
        :param int issue_ordi: An integer given to the issue
        :param str client_uuid: Unique identifier of the client
        :param int page: Page number of the results, default is 1
        :return: BillClientNetworkResponse object containing the bill-client network data

        >>> lobbyview = LobbyView(LOBBYVIEW_TOKEN)
        >>> output = lobbyview.bill_client_networks(congress_number=114, bill_chamber="H", bill_number=1174, client_uuid="44563806-56d2-5e99-84a1-95d22a7a69b3")
        >>> output.data[0]['issue_ordi']
        2

        >>> output = lobbyview.bill_client_networks(congress_number=114, bill_chamber="H", bill_number=1174, client_uuid="44563806-56d2-5e99-84a1-95d22a7a69b3")
        >>> print(output)
        Bill-Client Networks:
          Bill Number: 1174, Client UUID: 44563806-56d2-5e99-84a1-95d22a7a69b3, Issue Ordi: 2
          Bill Number: 1174, Client UUID: 44563806-56d2-5e99-84a1-95d22a7a69b3, Issue Ordi: 5
          Bill Number: 1174, Client UUID: 44563806-56d2-5e99-84a1-95d22a7a69b3, Issue Ordi: 4
        ...

        >>> output = lobbyview.bill_client_networks(bill_resolution_type=None, report_uuid='006bd48b-59cf-5cbc-99b8-fc213e509a86', issue_ordi=2)
        >>> print(output)
        Bill-Client Networks:
          Bill Number: 1174, Client UUID: 44563806-56d2-5e99-84a1-95d22a7a69b3, Issue Ordi: 2
        """
        query_params = []
        if congress_number:
            query_params.append(f'congress_number=eq.{congress_number}')
        if bill_chamber:
            query_params.append(f'bill_chamber=eq.{bill_chamber}')
        if bill_resolution_type:
            query_params.append(f'bill_resolution_type=eq.{bill_resolution_type}') #!?
        if bill_number:
            query_params.append(f'bill_number=eq.{bill_number}')
        if report_uuid:
            query_params.append(f'report_uuid=eq.{report_uuid}') #!?
        if issue_ordi:
            query_params.append(f'issue_ordi=eq.{issue_ordi}') #!?
        if client_uuid:
            query_params.append(f'client_uuid=eq.{client_uuid}')
        if page != 1:
            query_params.append(f'page={page}')

        query_string = '&'.join(query_params)
        data = self.get_data(f'/api/bill_client_networks?{query_string}')

        return BillClientNetworkResponse(data)

if __name__ == "__main__":
    # loads token from .env file/environment variable
    load_dotenv("tests/.env")
    load_dotenv("../../tests/.env")
    LOBBYVIEW_TOKEN = os.environ.get('LOBBYVIEW_TOKEN', "NO TOKEN FOUND")

    # run doctests, pass in the LobbyView object with the token
    results = doctest.testmod(extraglobs={'lobbyview': LobbyView(LOBBYVIEW_TOKEN)},
                              optionflags=doctest.ELLIPSIS)
    results_string = f"{results.attempted-results.failed}/{results.attempted} TESTS PASSED"
    if results.failed == 0:
        print(results_string)
    else:
        raise Exception(results_string)
