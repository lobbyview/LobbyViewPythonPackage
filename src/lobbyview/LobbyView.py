# pylint: disable=E0401, C0411, W1203, C0301
'''
This module provides a Python interface to the LobbyView REST API. It uses the same endpoints
and parameter names as outlined in the LobbyView REST API Documentation
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
import ssl
import logging
import functools
import inspect
from urllib.parse import quote
from textwrap import fill
from exceptions import LobbyViewError, UnauthorizedError, TooManyRequestsError, PartialContentError
from exceptions import UnexpectedStatusCodeError, InvalidPageNumberError, RequestError

# for doctest at end, will remove in the future
import doctest
import os
from dotenv import load_dotenv

logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')

def validate_token(func):
    """
    Decorator function to validate the LobbyView token.
    """
    @functools.wraps(func)
    def wrapper(self, lobbyview_token, *args, **kwargs):
        if not isinstance(lobbyview_token, str) or len(lobbyview_token) < 20:
            logging.error("Unauthorized. Please check your API token.")
            raise UnauthorizedError()
        return func(self, lobbyview_token, *args, **kwargs)
    return wrapper

def url_quote(func):
    """
    Decorator function to quote string arguments in the function call.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Check if the function is a method
        if inspect.ismethod(func) or inspect.isbuiltin(func):
            # Skip the first argument (self)
            quoted_args = [quote(arg) if isinstance(arg, str) else arg for arg in args[1:]]
            quoted_args.insert(0, args[0])  # Add the self argument back to the start of the list
        else:
            quoted_args = [quote(arg) if isinstance(arg, str) else arg for arg in args]
        quoted_kwargs = {k: quote(v) if isinstance(v, str) else v for k, v in kwargs.items()}
        return func(*quoted_args, **quoted_kwargs)
    return wrapper

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
        exceptions.InvalidPageNumberError: Invalid page number: 2, total pages: 1
        """
        self.data = data['data']                     # the actual data
        self.current_page = int(data['currentPage']) # current page number
        self.total_pages = int(data['totalPage'])    # total pages available
        self.total_rows = int(data['totalNumber'])   # total rows available (not the number
                                                     # of rows in the response)

        if self.current_page > self.total_pages:
            logging.error(f"Invalid page number: {self.current_page}, total pages: {self.total_pages}")
            raise InvalidPageNumberError(current_page=self.current_page,
                                         total_pages=self.total_pages)

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
        {'current_page': 1, 'total_pages': 2, 'total_rows': 0}
        """
        return {"current_page": self.current_page, "total_pages": self.total_pages, "total_rows": self.total_rows}

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
            which includes the issue code, report UUID, and issue ordinal number
        """
        output = "Issues:\n"
        for issue in self:
            output += f"  {issue['issue_code']} (Report UUID: {issue['report_uuid']}, Issue Ordinal number (position) of the issue within the report: {issue['issue_ordi']})\n"
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

        >>> output = lobbyview.texts(issue_code="HCR", issue_text="covid", report_uuid="113f0964-33f7-5263-8037-d33c03408756")
        >>> print(output)
        Texts:
          Issue Code: HCR
          Issue Text: Health Insurance Tax, Pharmacy Benefit Managers (PBMs), COVID-19 Relief Efforts,
          Medicare Advantage, CARES Act Implementation, General Industry Issues, Drug
          Pricing and Transparency
        """
        output = "Texts:\n"
        for text in self:
            issue_code = text['issue_code']
            issue_text = text['issue_text']
            wrapped_text = fill(issue_text, width=80, subsequent_indent='  ')
            output += f"  Issue Code: {issue_code}\n  Issue Text: {wrapped_text}\n\n"
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
            which includes the bill number, client UUID, and issue ordinal number
        """
        output = "Bill-Client Networks:\n"
        for network in self:
            output += f"  Bill Number: {network['bill_number']}, Client UUID: {network['client_uuid']}, Issue Ordinal number (position) of the issue within the report: {network['issue_ordi']}\n"
        return output.rstrip()

class LobbyView:
    """
    Main class for interacting with the LobbyView API.
    """
    @validate_token
    def __init__(self, lobbyview_token, test_connection=True):
        """
        Initialize the LobbyView class with the provided API token.

        :param str lobbyview_token: API token for the LobbyView API
        :param bool test_connection: Whether to test the connection to the API
        """
        self.lobbyview_token = lobbyview_token
        self.headers = {
            'token': self.lobbyview_token,
        }

        if test_connection:
            try:
                self.get_data('/api/legislators')
            except Exception as exc:
                raise RequestError() from exc

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

        >>> lobbyview.get_data('/api/invalid_endpoint')
        Traceback (most recent call last):
        ...
        exceptions.UnexpectedStatusCodeError: Unexpected status code: 404

        >>> lobbyview.get_data('/api/legislators?invalid_param=value')
        Traceback (most recent call last):
        ...
        exceptions.UnexpectedStatusCodeError: Unexpected status code: 504

        >>> lobbyview_invalid = LobbyView("invalid_token", test_connection=False)
        Traceback (most recent call last):
        ...
        exceptions.UnauthorizedError: Unauthorized. Please check your API token and permissions.

        >>> lobbyview_invalid = LobbyView("invalid_token_alsd2kjfa44hsd3feawol", test_connection=False)
        >>> lobbyview_invalid.get_data('/api/legislators')
        Traceback (most recent call last):
        ...
        exceptions.UnauthorizedError: Unauthorized, status code: 401. Please check your API token and permissions.
        """
        # connection = http.client.HTTPSConnection('rest-api.lobbyview.org')

        # temporary connection to test API with unlimited token
        context = ssl._create_unverified_context()
        connection = http.client.HTTPSConnection(
            "lobbyview-rest-api-test.eba-witbq7ed.us-east-1.elasticbeanstalk.com", 
            context=context
            )
        
        try:
            connection.request('GET', query_string, None, self.headers)
            response = connection.getresponse()
            status_code = response.status

            if status_code == 200:
                data_string = response.read().decode('utf-8')
                # use json.loads to convert the string to a dictionary
                return json.loads(data_string)
            if status_code == 401:
                logging.error(f"Unauthorized, status code: {status_code}. Please check your API token and permissions.")
                raise UnauthorizedError(status_code=status_code)
            if status_code == 429:
                logging.error(f"Rate limit exceeded, status code: {status_code}")
                raise TooManyRequestsError(status_code=status_code)
            if status_code == 206:
                logging.error(f"Partial content returned, status code: {status_code}")
                raise PartialContentError(status_code=status_code)
            raise UnexpectedStatusCodeError(status_code=status_code)
        except (UnauthorizedError, TooManyRequestsError,
                PartialContentError, UnexpectedStatusCodeError):
            raise
        except Exception as exc:
            # error occurred during the request
            logging.error(f"Request error during API call: {str(exc)}")
            raise RequestError() from exc

    def paginate(self, func, **kwargs):
        """
        Paginates the data retrieval from the LobbyView API using lazy evaluation
        via a generator that yields results one at a time.

        :param function func: The API endpoint function to be paginated.
        :param dict kwargs: Additional keyword arguments to be passed to the API endpoint
            function.
        :return: A generator object that yields paginated results one item at a time.
        :raises PartialContentError: If the API returns a 206 Partial Content status code
        :raises LobbyViewError: If a different error occurs during pagination

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
        Traceback (most recent call last):
        ...
        exceptions.InvalidPageNumberError: Invalid page number: 1, total pages: 0

        >>> for network in lobbyview.paginate(lobbyview.bill_client_networks, congress_number=114, bill_chamber="H", bill_number=1174, client_uuid="44563806-56d2-5e99-84a1-95d22a7a69b3"):
        ...     print(f"Issue Ordinal number (position) of the issue within the report: {network['issue_ordi']}")
        Retrieving page 1...
        Issue Ordinal number (position) of the issue within the report: 2
        Issue Ordinal number (position) of the issue within the report: 5
        Issue Ordinal number (position) of the issue within the report: 4
        ...

        >>> for text in lobbyview.paginate(lobbyview.texts, issue_code="HCR", issue_text="covid"):
        ...     print(f"Issue Code: {text['issue_code']}")
        Retrieving page 1...
        Issue Code: HCR
        Issue Code: HCR
        ...
        Issue Code: HCR
        Retrieving page 2...
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
                logging.error(f"{str(exc)} - Partial results retrieved. Please wait for more quota.")
                raise
            except LobbyViewError as exc:
                logging.error(str(exc))
                raise

    @url_quote
    def legislators(self, legislator_id=None, legislator_govtrack_id=None,
                        legislator_first_name=None, legislator_last_name=None,
                        legislator_full_name=None, legislator_gender=None,
                        exact_birthday=None, min_birthday=None, max_birthday=None, page=1):
        """
        Gets legislator information from the LobbyView API based on the provided
        parameters.

        :param str legislator_id: Unique identifier of the legislator from LobbyView (Bioguide ID)
        :param str legislator_govtrack_id: Unique identifier of the legislator from
            GovTrack
        :param str legislator_first_name: First name of the legislator - using partial match with ilike operator (PostgreSQL)
        :param str legislator_last_name: Last name of the legislator - using partial match with ilike operator (PostgreSQL)
        :param str legislator_full_name: Full name of the legislator (First Middle Last) - using partial match with ilike operator (PostgreSQL)
        :param str legislator_gender: Gender of the legislator
        :param str exact_birthday: Exact birthday of the legislator (YYYY-MM-DD)
        :param str min_birthday: Minimum birthday of the legislator (YYYY-MM-DD)
        :param str max_birthday: Maximum birthday of the legislator (YYYY-MM-DD)
        :param int page: Page number of the results, default is 1
        :return: LegislatorResponse object containing the legislator data

        >>> output = lobbyview.legislators(legislator_id="M000303")
        >>> output.data
        [{'legislator_id': 'M000303', 'legislator_govtrack_id': '300071', 'legislator_other_ids': {'fec': ['S6AZ00019', 'P80002801'], 'lis': 'S197', 'cspan': 7476, 'icpsr': 15039, 'thomas': '00754', 'bioguide': 'M000303', 'govtrack': 300071, 'maplight': 592, 'wikidata': 'Q10390', 'votesmart': 53270, 'wikipedia': 'John McCain', 'ballotpedia': 'John McCain', 'opensecrets': 'N00006424', 'house_history': 17696, 'google_entity_id': 'kg:/m/0bymv'}, 'legislator_first_name': 'John', 'legislator_last_name': 'McCain', 'legislator_full_name': 'John McCain', 'legislator_other_names': {'last': 'McCain', 'first': 'John', 'middle': 'S.', 'official_full': 'John McCain'}, 'legislator_birthday': '1936-08-29', 'legislator_gender': 'M'}]

        >>> output = lobbyview.legislators(legislator_first_name="John", legislator_last_name="McCain")
        >>> output.data[0]['legislator_id']
        'M000303'
        
        >>> output = lobbyview.legislators(legislator_id="M000303", exact_birthday="1936-08-29", min_birthday="1950-08-28")
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
        if exact_birthday:
            query_params.append(f'legislator_birthday=eq.{exact_birthday}')
        if min_birthday and (exact_birthday is None):
            query_params.append(f'legislator_birthday=gte.{min_birthday}')
        if max_birthday and (exact_birthday is None):
            query_params.append(f'legislator_birthday=lte.{max_birthday}')
        if page != 1:
            query_params.append(f'page={page}')

        query_string = '&'.join(query_params)
        data = self.get_data(f'/api/legislators?{query_string}')

        return LegislatorResponse(data)

    @url_quote
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
        :param str bill_state: Bill status - using partial match with ilike operator (PostgreSQL).
            Examples: `REFERRED`, `PASSED:SIMPLERES`, `REPORTED`, `ENACTED:SIGNED`, `PASS_OVER:HOUSE`
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

        >>> output = lobbyview.bills(congress_number=111, bill_chamber="H", bill_number=4173)
        >>> output.data
        [{'congress_number': 111, 'bill_chamber': 'H', 'bill_resolution_type': None, 'bill_number': 4173, 'bill_introduced_datetime': '2009-12-02', 'bill_date_updated': '2016-06-29', 'bill_state': 'ENACTED:SIGNED', 'legislator_id': 'F000339', 'bill_url': 'https://congress.gov/bill/111th-congress/house-bill/4173'}]

        >>> output = lobbyview.bills(congress_number=111, bill_chamber="H", bill_number=4173)
        >>> output.data[0]['bill_state']
        'ENACTED:SIGNED'

        >>> output = lobbyview.bills(congress_number=111, bill_chamber="H", bill_number=4173, bill_resolution_type=None, bill_state="ENACTED:SIGNED", legislator_id="F000339", min_introduced_date="2009-12-01", max_introduced_date="2009-12-03", min_updated_date="2016-06-28", max_updated_date="2016-06-30")
        >>> output.data[0]['bill_url']
        'https://congress.gov/bill/111th-congress/house-bill/4173'

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
            query_params.append(f'bill_resolution_type=eq.{bill_resolution_type}')
        if bill_number:
            query_params.append(f'bill_number=eq.{bill_number}')
        if bill_state:
            query_params.append(f'bill_state=ilike.*{bill_state}*')
        if legislator_id:
            query_params.append(f'legislator_id=eq.{legislator_id}')
        if min_introduced_date:
            query_params.append(f'bill_introduced_datetime=gte.{min_introduced_date}')
        if max_introduced_date:
            query_params.append(f'bill_introduced_datetime=lte.{max_introduced_date}')
        if min_updated_date:
            query_params.append(f'bill_date_updated=gte.{min_updated_date}')
        if max_updated_date:
            query_params.append(f'bill_date_updated=lte.{max_updated_date}')
        if page != 1:
            query_params.append(f'page={page}')

        query_string = '&'.join(query_params)
        data = self.get_data(f'/api/bills?{query_string}')

        return BillResponse(data)

    @url_quote
    def clients(self, client_uuid=None, client_name=None,
                min_naics=None, max_naics=None, naics_description=None, page=1):
        """
        Gets client information from the LobbyView API based on the provided parameters.

        NAICS (North American Industry Classification System) codes are hierarchical, with the
        first few digits representing the industry and subindustry. For example, NAICS codes
        starting with the same first 3 digits belong to the same industry, and codes starting
        with the same first 4 digits belong to the same subindustry.

        When specifying the `min_naics` and `max_naics` parameters, keep in mind the hierarchical
        nature of NAICS codes. For instance, setting `min_naics` to '41' and `max_naics` to '42'
        will include all NAICS codes starting with '41' and '42', such as '412', '413', etc.
        **NOT FULLY IMPLEMENTED YET**

        :param str client_uuid: Unique identifier of the client
        :param str client_name: Name of the client - using partial match with ilike operator (PostgreSQL)
        :param str min_naics: Minimum NAICS code to which the client belongs (e.g., '41' for industry-level filtering)
        :param str max_naics: Maximum NAICS code to which the client belongs (e.g., '42' for industry-level filtering)
        :param str naics_description: Descriptions of the NAICS code - using partial match with ilike operator (PostgreSQL)
        :param int page: Page number of the results, default is 1
        :return: ClientResponse object containing the client data

        >>> output = lobbyview.clients(client_name="Microsoft Corporation", min_naics='51')
        >>> output.data
        [{'client_uuid': '44563806-56d2-5e99-84a1-95d22a7a69b3', 'client_name': 'Microsoft Corporation', 'primary_naics': '511210', 'naics_description': ['Applications development and publishing, except on a custom basis', 'Applications software, computer, packaged', 'Computer software publishers, packaged', 'Computer software publishing and reproduction', 'Games, computer software, publishing', 'Operating systems software, computer, packaged', 'Packaged computer software publishers', 'Programming language and compiler software publishers, packaged', 'Publishers, packaged computer software', 'Software computer, packaged, publishers', 'Software publishers', 'Software publishers, packaged', 'Utility software, computer, packaged']}]

        >>> output = lobbyview.clients(client_name="Microsoft Corporation")
        >>> output.data[0]['client_uuid']
        '44563806-56d2-5e99-84a1-95d22a7a69b3'

        >>> output = lobbyview.clients(client_uuid="44563806-56d2-5e99-84a1-95d22a7a69b3", min_naics='5112', max_naics='5113')
        >>> output.data[0]['client_name']
        'Microsoft Corporation'

        >>> output = lobbyview.clients(client_name="Microsoft Corporation")
        >>> print(output)
        Clients:
          Microsoft Corporation (ID: 44563806-56d2-5e99-84a1-95d22a7a69b3)
          PCT Government Relations on behalf of Microsoft Corporation (ID: 62eb98f6-ea3a-542d-abdb-7d2fce94b4f8)
          Cornerstone Government Affairs obo Microsoft Corporation (ID: d6634602-1d0b-560d-b4ac-e04194782ad3)

        >>> output = lobbyview.clients(client_uuid='44563806-56d2-5e99-84a1-95d22a7a69b3', min_naics='5112', max_naics='5113')
        >>> print(output)
        Clients:
          Microsoft Corporation (ID: 44563806-56d2-5e99-84a1-95d22a7a69b3)
        """
        query_params = []
        if client_uuid:
            query_params.append(f'client_uuid=eq.{client_uuid}')
        if client_name:
            query_params.append(f'client_name=ilike.*{client_name}*')
        if min_naics:
            query_params.append(f'primary_naics=gte.{min_naics}')
        if max_naics:
            query_params.append(f'primary_naics=lte.{max_naics}')
        if naics_description:
            query_params.append(f'naics_description=ilike.*{naics_description}*') #!? - is too slow to search
        if page != 1:
            query_params.append(f'page={page}')

        # query_string = '&'.join([urllib.parse.quote(query_param) for query_param in query_params])
        query_string = '&'.join(query_params)
        data = self.get_data(f'/api/clients?{query_string}')

        return ClientResponse(data)

    @url_quote
    def reports(self, report_uuid=None, client_uuid=None, registrant_uuid=None,
            registrant_name=None, report_year=None, min_report_year=None,
            max_report_year=None, report_quarter_code=None, min_report_quarter_code=None,
            max_report_quarter_code=None, min_amount=None, max_amount=None,
            is_no_activity=None, is_client_self_filer=None, is_amendment=None, page=1):
        """
        Gets report information from the LobbyView API based on the provided parameters.

        :param str report_uuid: Unique identifier of the report
        :param str client_uuid: Unique identifier of the client
        :param str registrant_uuid: Unique identifier of the registrant
        :param str registrant_name: Name of the registrant - using partial match with ilike operator (PostgreSQL)
        :param int report_year: Year of the report
        :param int min_report_year: Minimum year of the report
        :param int max_report_year: Maximum year of the report
        :param int report_quarter_code: Quarter period of the report (returns quarter as string)
        :param int min_report_quarter_code: Minimum quarter period of the report (returns quarter as string)
        :param int max_report_quarter_code: Maximum quarter period of the report (returns quarter as string)
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

        >>> output = lobbyview.reports(report_year=2020, report_quarter_code=2, is_client_self_filer=True, report_uuid="4b799814-3e94-5ee1-8dd4-b32aead9aca6")
        >>> output.data
        [{'report_uuid': '4b799814-3e94-5ee1-8dd4-b32aead9aca6', 'client_uuid': 'cdf5a171-6aab-50ea-912c-68c054decdce', 'registrant_uuid': '323adb44-3062-5a5f-98ea-6d4ca51e6f43', 'registrant_name': 'NATIONAL ASSOCIATION OF REALTORS', 'report_year': 2020, 'report_quarter_code': '2', 'amount': '$11,680,000.00', 'is_no_activity': False, 'is_client_self_filer': True, 'is_amendment': False}]

        >>> output = lobbyview.reports(report_year=2020, report_quarter_code=2, is_client_self_filer=True, report_uuid="4b799814-3e94-5ee1-8dd4-b32aead9aca6")
        >>> output.data[0]['amount']
        '$11,680,000.00'

        >>> output = lobbyview.reports(report_year=2020, report_quarter_code=2, is_client_self_filer=True, report_uuid="4b799814-3e94-5ee1-8dd4-b32aead9aca6", min_report_quarter_code=5, max_report_quarter_code=0)
        >>> output.data[0]['amount']
        '$11,680,000.00'

        >>> output = lobbyview.reports(client_uuid="cdf5a171-6aab-50ea-912c-68c054decdce", registrant_uuid="323adb44-3062-5a5f-98ea-6d4ca51e6f43", registrant_name="NATIONAL ASSOCIATION OF REALTORS", min_amount="$11,679,999.99", max_amount="$11,680,000.01", is_no_activity=False, is_amendment=False, min_report_year=2017, max_report_year=2023)
        >>> output.data[0]['report_year']
        2020

        >>> output = lobbyview.reports(client_uuid="cdf5a171-6aab-50ea-912c-68c054decdce", registrant_uuid="323adb44-3062-5a5f-98ea-6d4ca51e6f43", registrant_name="NATIONAL ASSOCIATION OF REALTORS", min_amount="$11,679,999.99", max_amount="$11,680,000.01", is_no_activity=False, is_amendment=False, report_year=2020, min_report_year=2040, max_report_year=1800)
        >>> output.data[0]['report_year']
        2020
        
        >>> output = lobbyview.reports(report_year=2020, report_quarter_code=2, is_client_self_filer=True, report_uuid="4b799814-3e94-5ee1-8dd4-b32aead9aca6")
        >>> print(output)
        Reports:
          4b799814-3e94-5ee1-8dd4-b32aead9aca6 (Year: 2020, Quarter: 2)
        """
        query_params = []
        if report_uuid:
            query_params.append(f'report_uuid=eq.{report_uuid}')
        if client_uuid:
            query_params.append(f'client_uuid=eq.{client_uuid}')
        if registrant_uuid:
            query_params.append(f'registrant_uuid=eq.{registrant_uuid}')
        if registrant_name:
            query_params.append(f'registrant_name=ilike.*{registrant_name}*')
        if report_year:
            query_params.append(f'report_year=eq.{report_year}')
        if min_report_year and (report_year is None):
            query_params.append(f'report_year=gte.{min_report_year}')
        if max_report_year and (report_year is None):
            query_params.append(f'report_year=lte.{max_report_year}')
        if report_quarter_code:
            query_params.append(f'report_quarter_code=eq.{report_quarter_code}')
        if min_report_quarter_code and (report_quarter_code is None):
            query_params.append(f'report_quarter_code=gte.{min_report_quarter_code}')
        if max_report_quarter_code and (report_quarter_code is None):
            query_params.append(f'report_quarter_code=lte.{max_report_quarter_code}')
        if min_amount:
            query_params.append(f'amount=gte.{min_amount}')
        if max_amount:
            query_params.append(f'amount=lte.{max_amount}')
        if is_no_activity is not None:
            query_params.append(f'is_no_activity=eq.{is_no_activity}')
        if is_client_self_filer is not None:
            query_params.append(f'is_client_self_filer=eq.{is_client_self_filer}')
        if is_amendment is not None:
            query_params.append(f'is_amendment=eq.{is_amendment}')
        if page != 1:
            query_params.append(f'page={page}')

        query_string = '&'.join(query_params)
        data = self.get_data(f'/api/reports?{query_string}')

        return ReportResponse(data)

    @url_quote
    def issues(self, report_uuid=None, issue_ordi=None, issue_code=None, gov_entity=None,
               page=1):
        """
        Gets issue information from the LobbyView API based on the provided parameters.

        :param str report_uuid: Unique identifier of the report
        :param int issue_ordi: The ordinal number (position) of the issue within the report.
            This is an integer value that represents the order in which the issue appears in
            the report. For example, if an issue has issue_ordi=2, it means it is the second
            issue mentioned in the report.
        :param str issue_code: General Issue Area Code (Section 15)
        :param str gov_entity: House(s) of Congress and Federal agencies (Section 17) - using partial match with ilike operator (PostgreSQL)
        :param int page: Page number of the results, default is 1
        :return: IssueResponse object containing the issue data

        >>> output = lobbyview.issues(issue_code="TRD", report_uuid="00016ab3-2246-5af8-a68d-05af40dfde68", issue_ordi=2)
        >>> output.data
        [{'report_uuid': '00016ab3-2246-5af8-a68d-05af40dfde68', 'issue_ordi': 2, 'issue_code': 'TRD', 'gov_entity': ['HOUSE OF REPRESENTATIVES', 'SENATE']}]

        >>> output = lobbyview.issues(issue_code="TRD")
        >>> output.data[0]['report_uuid']
        '00016ab3-2246-5af8-a68d-05af40dfde68'

        >>> output = lobbyview.issues(issue_code="TRD")
        >>> print(output)
        Issues:
          TRD (Report UUID: 00016ab3-2246-5af8-a68d-05af40dfde68, Issue Ordinal number (position) of the issue within the report: 2)
          TRD (Report UUID: 0001f9b9-84d7-5ceb-af03-8987bb76d593, Issue Ordinal number (position) of the issue within the report: 1)
          TRD (Report UUID: 00020868-67be-5975-955d-7ecab8d42e6e, Issue Ordinal number (position) of the issue within the report: 2)
          TRD (Report UUID: 00040172-6cda-5b31-8d83-9c1bcfd4b289, Issue Ordinal number (position) of the issue within the report: 1)
          TRD (Report UUID: 00047fc7-2207-5f3b-951d-692b9f35825b, Issue Ordinal number (position) of the issue within the report: 1)
          TRD (Report UUID: 000759fa-dc93-5849-b1e5-7aa751e86433, Issue Ordinal number (position) of the issue within the report: 4)
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
            query_params.append(f'gov_entity=ilike.*{gov_entity}*') # !? - too slow to search
        if page != 1:
            query_params.append(f'page={page}')

        query_string = '&'.join(query_params)
        data = self.get_data(f'/api/issues?{query_string}')

        return IssueResponse(data)

    @url_quote
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

        >>> output = lobbyview.networks(client_uuid="44563806-56d2-5e99-84a1-95d22a7a69b3", legislator_id="M000303")
        >>> output.data
        [{'client_uuid': '44563806-56d2-5e99-84a1-95d22a7a69b3', 'legislator_id': 'M000303', 'report_year': 2006, 'n_bills_sponsored': 1}, {'client_uuid': '44563806-56d2-5e99-84a1-95d22a7a69b3', 'legislator_id': 'M000303', 'report_year': 2017, 'n_bills_sponsored': 1}]

        >>> output = lobbyview.networks(client_uuid="44563806-56d2-5e99-84a1-95d22a7a69b3", legislator_id="M000303")
        >>> output.data[0]['report_year']
        2006

        >>> output = lobbyview.networks(client_uuid="44563806-56d2-5e99-84a1-95d22a7a69b3", legislator_id="M000303", min_report_year=2016, max_report_year=2018, min_bills_sponsored=0, max_bills_sponsored=2)
        >>> output.data[0]['n_bills_sponsored']
        1

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
            query_params.append(f'report_year=gte.{min_report_year}')
        if max_report_year:
            query_params.append(f'report_year=lte.{max_report_year}')
        if min_bills_sponsored:
            query_params.append(f'n_bills_sponsored=gte.{min_bills_sponsored}')
        if max_bills_sponsored:
            query_params.append(f'n_bills_sponsored=lte.{max_bills_sponsored}')
        if page != 1:
            query_params.append(f'page={page}')

        query_string = '&'.join(query_params)
        data = self.get_data(f'/api/networks?{query_string}')

        return NetworkResponse(data)

    @url_quote
    def texts(self, report_uuid=None, issue_ordi=None, issue_code=None, issue_text=None,
              page=1):
        """
        Gets issue text data from the LobbyView API based on the provided parameters.

        :param str report_uuid: Unique identifier of the report
        :param int issue_ordi: The ordinal number (position) of the issue within the report.
            This is an integer value that represents the order in which the issue appears in
            the report. For example, if an issue has issue_ordi=2, it means it is the second
            issue mentioned in the report.
        :param str issue_code: General Issue Area Code (Section 15)
        :param str issue_text: Specific lobbying issues (Section 16) - using partial match with ilike operator (PostgreSQL).
            Examples: `Appropriations`, `House and Senate Defense Appropriations Bills`,
            `House and Senate Defense Authorization Bills`, `No lobbying activity.`, `Health care funding and appropriations`
        :param int page: Page number of the results, default is 1
        :return: TextResponse object containing the text data

        >>> output = lobbyview.texts(issue_code="HCR", issue_text="covid", report_uuid="000bef17-9f0a-5d7c-8660-edca16e1dfce")
        >>> output.data
        [{'report_uuid': '000bef17-9f0a-5d7c-8660-edca16e1dfce', 'issue_ordi': 1, 'issue_code': 'HCR', 'issue_text': 'HR 748 CARES Act - Issues related to COVID-19 relief'}]

        >>> output = lobbyview.texts(issue_code="HCR", issue_text="covid")
        >>> output.data[0]['issue_ordi']
        1

        >>> output = lobbyview.texts(issue_code="HCR", report_uuid="000bef17-9f0a-5d7c-8660-edca16e1dfce", issue_ordi=1)
        >>> output.data[0]['issue_text']
        'HR 748 CARES Act - Issues related to COVID-19 relief'
        
         >>> output = lobbyview.texts(issue_code="HCR", issue_text="covid")
        >>> print(output)
        Texts:
          Issue Code: HCR
          Issue Text: HR 748 CARES Act - Issues related to COVID-19 relief
        ...

        >>> output = lobbyview.texts(report_uuid='000bef17-9f0a-5d7c-8660-edca16e1dfce', issue_ordi=1)
        >>> print(output)
        Texts:
          Issue Code: HCR
          Issue Text: HR 748 CARES Act - Issues related to COVID-19 relief
        """
        query_params = []
        if report_uuid:
            query_params.append(f'report_uuid=eq.{report_uuid}')
        if issue_ordi:
            query_params.append(f'issue_ordi=eq.{issue_ordi}')
        if issue_code:
            query_params.append(f'issue_code=eq.{issue_code}')
        if issue_text:
            query_params.append(f'issue_text=ilike.*{issue_text}*')
        if page != 1:
            query_params.append(f'page={page}')

        query_string = '&'.join(query_params)
        data = self.get_data(f'/api/texts?{query_string}')

        return TextResponse(data)

    @url_quote
    def quarter_level_networks(self, client_uuid=None, legislator_id=None, report_year=None,
                               min_report_year=None, max_report_year=None,
                               report_quarter_code=None, min_report_quarter_code=None, max_report_quarter_code=None,
                               min_bills_sponsored=None, max_bills_sponsored=None, page=1):
        """
        Gets quarter-level network information from the LobbyView API based on the provided
        parameters. This API is private and requires special permission to access, users do
        not have access by default. Thus, trying to use this method without proper permissions
        will cause an `UnauthorizedError` to occur. If you are interested in this API, please
        contact the LobbyView team at lobbydata@gmail.com.

        :param str client_uuid: Unique identifier of the client
        :param str legislator_id: Unique identifier of the legislator
        :param int report_year: Year of the report
        :param int min_report_year: Minimum year of the report
        :param int max_report_year: Maximum year of the report
        :param int report_quarter_code: Quarter period of the report (returns quarter as string)
        :param int min_report_quarter_code: Minimum quarter period of the report (returns quarter as string)
        :param int max_report_quarter_code: Maximum quarter period of the report (returns quarter as string)
        :param int min_bills_sponsored: Minimum number of bills sponsored by the legislator
            in a specific quarter lobbied by the client
        :param int max_bills_sponsored: Maximum number of bills sponsored by the legislator
            in a specific quarter lobbied by the client
        :param int page: Page number of the results, default is 1
        :return: QuarterLevelNetworkResponse object containing the quarter-level network data

        >>> output = lobbyview.quarter_level_networks(client_uuid="44563806-56d2-5e99-84a1-95d22a7a69b3", legislator_id="M000303", report_year=2017, report_quarter_code=4)
        >>> output.data
        [{'client_uuid': '44563806-56d2-5e99-84a1-95d22a7a69b3', 'legislator_id': 'M000303', 'report_year': 2017, 'report_quarter_code': '4', 'n_bills_sponsored': 1}]

        >>> output = lobbyview.quarter_level_networks(client_uuid="44563806-56d2-5e99-84a1-95d22a7a69b3", legislator_id="M000303", report_year=2017, report_quarter_code=4)
        >>> output.data[0]['n_bills_sponsored']
        1

        >>> output = lobbyview.quarter_level_networks(client_uuid="44563806-56d2-5e99-84a1-95d22a7a69b3", legislator_id="M000303", report_year=2017, report_quarter_code=4, min_report_quarter_code=9, max_report_quarter_code=-2)
        >>> output.data[0]['n_bills_sponsored']
        1

        >>> output = lobbyview.quarter_level_networks(client_uuid="44563806-56d2-5e99-84a1-95d22a7a69b3", legislator_id="M000303", report_year=2017, min_report_quarter_code=3, max_report_quarter_code=5)
        >>> output.data[0]['n_bills_sponsored']
        1

        >>> output = lobbyview.quarter_level_networks(client_uuid="44563806-56d2-5e99-84a1-95d22a7a69b3", legislator_id="M000303", report_year=2017, min_report_year=2030, max_report_year=2000)
        >>> output.data[0]['n_bills_sponsored']
        1

        >>> output = lobbyview.quarter_level_networks(client_uuid="44563806-56d2-5e99-84a1-95d22a7a69b3", legislator_id="M000303", min_report_year=2016, max_report_year=2018)
        >>> output.data[0]['n_bills_sponsored']
        1

        >>> output = lobbyview.quarter_level_networks(client_uuid="44563806-56d2-5e99-84a1-95d22a7a69b3", legislator_id="M000303", report_year=2017, min_bills_sponsored=0, max_bills_sponsored=2)
        >>> output.data[0]['report_quarter_code']
        '4'
        
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
        if min_report_year and (report_year is None):
            query_params.append(f'report_year=gte.{min_report_year}')
        if max_report_year and (report_year is None):
            query_params.append(f'report_year=lte.{max_report_year}')
        if report_quarter_code:
            query_params.append(f'report_quarter_code=eq.{report_quarter_code}')
        if min_report_quarter_code and (report_quarter_code is None):
            query_params.append(f'report_quarter_code=gte.{min_report_quarter_code}')
        if max_report_quarter_code and (report_quarter_code is None):
            query_params.append(f'report_quarter_code=lte.{max_report_quarter_code}')
        if min_bills_sponsored:
            query_params.append(f'n_bills_sponsored=gte.{min_bills_sponsored}')
        if max_bills_sponsored:
            query_params.append(f'n_bills_sponsored=lte.{max_bills_sponsored}')
        if page != 1:
            query_params.append(f'page={page}')

        query_string = '&'.join(query_params)
        data = self.get_data(f'/api/quarter_level_networks?{query_string}')

        return QuarterLevelNetworkResponse(data)

    @url_quote
    def bill_client_networks(self, congress_number=None, bill_chamber=None,
                        bill_resolution_type=None, bill_number=None, bill_id=None,
                        report_uuid=None, issue_ordi=None, client_uuid=None, page=1):
        """
        Gets bill-client network information from the LobbyView API based on the provided
        parameters. This API is private and requires special permission to access, users do
        not have access by default. Thus, trying to use this method without proper permissions
        will cause an `UnauthorizedError` to occur. If you are interested in this API, please
        contact the LobbyView team at lobbydata@gmail.com.

        :param int congress_number: Session of Congress
        :param str bill_id: The unique identifier of the bill in the format [bill_chamber][bill_resolution_type][bill_number] - [congress_number]
            - examples: H.R.1174 - 114
        :param str bill_chamber: Chamber of the legislative branch (Component of the
            bill_id composite key)
        :param str bill_resolution_type: Bill type (Component of the bill_id composite key)
        :param int bill_number: Bill number (Component of the bill_id composite key)
        :param str report_uuid: Unique identifier of the report
        :param int issue_ordi: The ordinal number (position) of the issue within the report.
            This is an integer value that represents the order in which the issue appears in
            the report. For example, if an issue has issue_ordi=2, it means it is the second
            issue mentioned in the report.
        :param str client_uuid: Unique identifier of the client
        :param int page: Page number of the results, default is 1
        :return: BillClientNetworkResponse object containing the bill-client network data

        >>> output = lobbyview.bill_client_networks(congress_number=114, bill_chamber="H", bill_number=1174, client_uuid="44563806-56d2-5e99-84a1-95d22a7a69b3", report_uuid="006bd48b-59cf-5cbc-99b8-fc213e509a86")
        >>> output.data
        [{'congress_number': 114, 'bill_chamber': 'H', 'bill_resolution_type': None, 'bill_number': 1174, 'report_uuid': '006bd48b-59cf-5cbc-99b8-fc213e509a86', 'issue_ordi': 2, 'client_uuid': '44563806-56d2-5e99-84a1-95d22a7a69b3'}]

        >>> output = lobbyview.bill_client_networks(congress_number=114, bill_chamber="H", bill_resolution_type='C', report_uuid="00043607-ec6d-53a8-85b4-d418a64b423e")
        >>> output.data[0]['bill_number']
        125

        >>> output = lobbyview.bill_client_networks(congress_number=114, bill_chamber="H", bill_number=1174, client_uuid="44563806-56d2-5e99-84a1-95d22a7a69b3", report_uuid="006bd48b-59cf-5cbc-99b8-fc213e509a86")
        >>> output.data[0]['issue_ordi']
        2

        >>> output = lobbyview.bill_client_networks(report_uuid="006bd48b-59cf-5cbc-99b8-fc213e509a86", issue_ordi=2)
        >>> output.data[0]['bill_number']
        1174
        
        >>> output = lobbyview.bill_client_networks(congress_number=114, bill_chamber="H", bill_number=1174, client_uuid="44563806-56d2-5e99-84a1-95d22a7a69b3")
        >>> print(output)
        Bill-Client Networks:
          Bill Number: 1174, Client UUID: 44563806-56d2-5e99-84a1-95d22a7a69b3, Issue Ordinal number (position) of the issue within the report: 2
          Bill Number: 1174, Client UUID: 44563806-56d2-5e99-84a1-95d22a7a69b3, Issue Ordinal number (position) of the issue within the report: 5
          Bill Number: 1174, Client UUID: 44563806-56d2-5e99-84a1-95d22a7a69b3, Issue Ordinal number (position) of the issue within the report: 4
        ...

        >>> output = lobbyview.bill_client_networks(report_uuid='006bd48b-59cf-5cbc-99b8-fc213e509a86', issue_ordi=2)
        >>> print(output)
        Bill-Client Networks:
          Bill Number: 1174, Client UUID: 44563806-56d2-5e99-84a1-95d22a7a69b3, Issue Ordinal number (position) of the issue within the report: 2
          Bill Number: 512, Client UUID: 44563806-56d2-5e99-84a1-95d22a7a69b3, Issue Ordinal number (position) of the issue within the report: 2
        """
        query_params = []
        if congress_number:
            query_params.append(f'congress_number=eq.{congress_number}')
        if bill_id:
            bill_parts = bill_id.split(" - ")
            if len(bill_parts) == 2:
                congress_number = bill_parts[1]
                bill_parts = bill_parts[0]
                bill_chamber = bill_parts[0]
                bill_resolution_type = bill_parts[1:-1] or None
                bill_number = bill_parts[-1]

                query_params.append(f'congress_number=eq.{congress_number}')
                query_params.append(f'bill_chamber=eq.{bill_chamber}')
                if bill_resolution_type:
                    query_params.append(f'bill_resolution_type=eq.{bill_resolution_type}')
                query_params.append(f'bill_number=eq.{bill_number}')
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
        if page != 1:
            query_params.append(f'page={page}')

        # query_string = '&'.join([urllib.parse.quote(query_param) for query_param in query_params])
        query_string = '&'.join(query_params)
        data = self.get_data(f'/api/bill_client_networks?{query_string}')

        return BillClientNetworkResponse(data)

if __name__ == "__main__":
    # loads token from .env file/environment variable
    load_dotenv("tests/.env")
    load_dotenv("../../tests/.env")
    LOBBYVIEW_TOKEN = os.environ.get('LOBBYVIEW_TOKEN', "NO TOKEN FOUND")

    # code commented out below will allow for running individual method doctests

    # runner = doctest.DocTestRunner(optionflags=doctest.ELLIPSIS)
    # finder = doctest.DocTestFinder()
    # for test in finder.find(LobbyViewResponse, globs={'lobbyview': LobbyView(LOBBYVIEW_TOKEN)}):
    #     runner.run(test)
    # result = runner.summarize()
    # results_string = f"{result.attempted - result.failed}/{result.attempted} TESTS PASSED"
    # if result.failed == 0:
    #     print(results_string)
    # else:
    #     raise Exception(results_string)

    # original code below will run all doctests

    # run doctests, pass in the LobbyView object with the token
    results = doctest.testmod(extraglobs={'lobbyview': LobbyView(LOBBYVIEW_TOKEN)},
                              optionflags=doctest.ELLIPSIS)
    results_string = f"{results.attempted-results.failed}/{results.attempted} TESTS PASSED"
    if results.failed == 0:
        print(results_string)
    else:
        raise Exception(results_string)
