# LobbyView Package Documentation

![Tests](https://github.com/lobbyview/LobbyViewPythonPackage/actions/workflows/python-package.yml/badge.svg)
![Coverage](./coverage-badge.svg)
![PyPI Downloads](https://github.com/lobbyview/LobbyViewPythonPackage/blob/main/download-badge.svg)

This module provides a Python interface to the LobbyView REST API. It uses the same endpoints
and parameter names as outlined in the LobbyView REST API Documentation
(https://rest-api.lobbyview.org/).

The full documentation for the package is linked here: http://lobbyview.readthedocs.io/

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

Note: This repo is pre-release and our expected time table is November 2024 for a release that's ready for widespread public use.

# Instructions

Import a lobbyview token using os and dotenv

```
import os
from dotenv import load_dotenv
load_dotenv(".env")
LOBBYVIEW_TOKEN = os.environ.get('LOBBYVIEW_TOKEN')
```

Initialize a LobbyView object instance

```
from LobbyView import LobbyView
lobbyview = LobbyView(LOBBYVIEW_TOKEN)
```

Note that ```quarter_level_networks``` and ```bill_client_networks``` API endpoints are not available to all users.

# Classes and Methods

## Class: LobbyView

Main class for interacting with the LobbyView API.


### Method: __init__

Initialize the LobbyView class with the provided API token.


#### Parameters:
- str lobbyview_token: API token for the LobbyView API
- bool test_connection: Whether to test the connection to the API


### Method: get_data

Sends a GET request to the LobbyView API with the provided query string.
Returns the JSON response data.


#### Parameters:
- str query_string: Query string for the API endpoint
:return dict: JSON data from the API response
:raises UnauthorizedError: If the API returns a 401 Unauthorized status code
:raises TooManyRequestsError: If the API returns a 429 Too Many Requests status
    code
:raises PartialContentError: If the API returns a 206 Partial Content status code
:raises UnexpectedStatusCodeError: If the API returns an unexpected status code
:raises RequestError: If an error occurs during the request


#### Example:
```python
>>> lobbyview.get_data('/api/invalid_endpoint')
Traceback (most recent call last):
...
exceptions.UnexpectedStatusCodeError: Unexpected status code: 404

>>> lobbyview.get_data('/api/legislators?invalid_param=value')
Traceback (most recent call last):
...
exceptions.RequestError: RequestError

>>> lobbyview_invalid = LobbyView("invalid_token", test_connection=False)
>>> lobbyview_invalid.get_data('/api/legislators')
Traceback (most recent call last):
...
exceptions.UnauthorizedError: Unauthorized, status code: 401. Please check your API token and permissions.
```

### Method: paginate

Paginates the data retrieval from the LobbyView API using lazy evaluation
via a generator that yields results one at a time.


#### Parameters:
- function func: The API endpoint function to be paginated.
- dict kwargs: Additional keyword arguments to be passed to the API endpoint
    function.

#### Returns:
- A generator object that yields paginated results one item at a time.
:raises PartialContentError: If the API returns a 206 Partial Content status code
:raises LobbyViewError: If a different error occurs during pagination


#### Example:
```python
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
Error occurred: Invalid page number: 1, total pages: 0

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
```

### Method: legislators

Gets legislator information from the LobbyView API based on the provided
parameters.


#### Parameters:
- str legislator_id: Unique identifier of the legislator from LobbyView (Bioguide ID)
- str legislator_govtrack_id: Unique identifier of the legislator from
    GovTrack
- str legislator_first_name: First name of the legislator - using partial match with ilike operator (PostgreSQL)
- str legislator_last_name: Last name of the legislator - using partial match with ilike operator (PostgreSQL)
- str legislator_full_name: Full name of the legislator (First Middle Last) - using partial match with ilike operator (PostgreSQL)
- str legislator_gender: Gender of the legislator
- str exact_birthday: Exact birthday of the legislator (YYYY-MM-DD)
- str min_birthday: Minimum birthday of the legislator (YYYY-MM-DD)
- str max_birthday: Maximum birthday of the legislator (YYYY-MM-DD)
- int page: Page number of the results, default is 1

#### Returns:
- LegislatorResponse object containing the legislator data


#### Example:
```python
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
```

### Method: bills

Gets bill information from the LobbyView API based on the provided parameters.


#### Parameters:
- int congress_number: Session of Congress
- str bill_chamber: Chamber of the legislative branch
    (Component of the bill_id composite key)
- str bill_resolution_type: Bill type (Component of the bill_id composite
    key)
- int bill_number: Bill number (Component of the bill_id composite key)
- str bill_state: Bill status - using partial match with ilike operator (PostgreSQL).
    Examples: `REFERRED`, `PASSED:SIMPLERES`, `REPORTED`, `ENACTED:SIGNED`, `PASS_OVER:HOUSE`
- str legislator_id: Sponsor of the bill
- str min_introduced_date: Minimum date of introduction to Congress
    (YYYY-MM-DD)
- str max_introduced_date: Maximum date of introduction to Congress
    (YYYY-MM-DD)
- str min_updated_date: Minimum date of most recent status change
    (YYYY-MM-DD)
- str max_updated_date: Maximum date of most recent status change
    (YYYY-MM-DD)
- int page: Page number of the results, default is 1

#### Returns:
- BillResponse object containing the bill data


#### Example:
```python
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
```

### Method: clients

Gets client information from the LobbyView API based on the provided parameters.

NAICS (North American Industry Classification System) codes are hierarchical, with the
first few digits representing the industry and subindustry. For example, NAICS codes
starting with the same first 3 digits belong to the same industry, and codes starting
with the same first 4 digits belong to the same subindustry.

When specifying the `min_naics` and `max_naics` parameters, keep in mind the hierarchical
nature of NAICS codes. For instance, setting `min_naics` to '41' and `max_naics` to '42'
will include all NAICS codes starting with '41' and '42', such as '412', '413', etc.
**NOT FULLY IMPLEMENTED YET**


#### Parameters:
- str client_uuid: Unique identifier of the client
- str client_name: Name of the client - using partial match with ilike operator (PostgreSQL)
- str min_naics: Minimum NAICS code to which the client belongs (e.g., '41' for industry-level filtering)
- str max_naics: Maximum NAICS code to which the client belongs (e.g., '42' for industry-level filtering)
- str naics_description: Descriptions of the NAICS code - using partial match with ilike operator (PostgreSQL)
- int page: Page number of the results, default is 1

#### Returns:
- ClientResponse object containing the client data


#### Example:
```python
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
```

### Method: reports

Gets report information from the LobbyView API based on the provided parameters.


#### Parameters:
- str report_uuid: Unique identifier of the report
- str client_uuid: Unique identifier of the client
- str registrant_uuid: Unique identifier of the registrant
- str registrant_name: Name of the registrant - using partial match with ilike operator (PostgreSQL)
- int report_year: Year of the report
- int min_report_year: Minimum year of the report
- int max_report_year: Maximum year of the report
- int report_quarter_code: Quarter period of the report (returns quarter as string)
- int min_report_quarter_code: Minimum quarter period of the report (returns quarter as string)
- int max_report_quarter_code: Maximum quarter period of the report (returns quarter as string)
- str min_amount: Minimum lobbying firm income or lobbying expense
    (in-house)
- str max_amount: Maximum lobbying firm income or lobbying expense
    (in-house)
- bool is_no_activity: Quarterly activity indicator
- bool is_client_self_filer: An organization employing its own in-house
    lobbyist(s)
- bool is_amendment: Amendment of previous report
- int page: Page number of the results, default is 1

#### Returns:
- ReportResponse object containing the report data


#### Example:
```python
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
```

### Method: issues

Gets issue information from the LobbyView API based on the provided parameters.


#### Parameters:
- str report_uuid: Unique identifier of the report
- int issue_ordi: The ordinal number (position) of the issue within the report.
    This is an integer value that represents the order in which the issue appears in
    the report. For example, if an issue has issue_ordi=2, it means it is the second
    issue mentioned in the report.
- str issue_code: General Issue Area Code (Section 15)
- str gov_entity: House(s) of Congress and Federal agencies (Section 17) - using partial match with ilike operator (PostgreSQL)
- int page: Page number of the results, default is 1

#### Returns:
- IssueResponse object containing the issue data


#### Example:
```python
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
```

### Method: networks

Gets network information from the LobbyView API based on the provided parameters.


#### Parameters:
- str client_uuid: Unique identifier of the client
- str legislator_id: Unique identifier of the legislator
- int min_report_year: Minimum year of the report
- int max_report_year: Maximum year of the report
- int min_bills_sponsored: Minimum number of bills sponsored by the legislator
    in a specific year lobbied by the client
- int max_bills_sponsored: Maximum number of bills sponsored by the legislator
    in a specific year lobbied by the client
- int page: Page number of the results, default is 1

#### Returns:
- NetworkResponse object containing the network data


#### Example:
```python
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
```

### Method: texts

Gets issue text data from the LobbyView API based on the provided parameters.


#### Parameters:
- str report_uuid: Unique identifier of the report
- int issue_ordi: The ordinal number (position) of the issue within the report.
    This is an integer value that represents the order in which the issue appears in
    the report. For example, if an issue has issue_ordi=2, it means it is the second
    issue mentioned in the report.
- str issue_code: General Issue Area Code (Section 15)
- str issue_text: Specific lobbying issues (Section 16) - using partial match with ilike operator (PostgreSQL).
    Examples: `Appropriations`, `House and Senate Defense Appropriations Bills`,
    `House and Senate Defense Authorization Bills`, `No lobbying activity.`, `Health care funding and appropriations`
- int page: Page number of the results, default is 1

#### Returns:
- TextResponse object containing the text data


#### Example:
```python
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
  Issue Code: HCR, Issue Text: HR 748 CARES Act - Issues related to COVID-19 relief
...

>>> output = lobbyview.texts(report_uuid='000bef17-9f0a-5d7c-8660-edca16e1dfce', issue_ordi=1)
>>> print(output)
Texts:
  Issue Code: HCR, Issue Text: HR 748 CARES Act - Issues related to COVID-19 relief
```

### Method: quarter_level_networks

Gets quarter-level network information from the LobbyView API based on the provided
parameters. This API is private and requires special permission to access, users do
not have access by default. Thus, trying to use this method without proper permissions
will cause an `UnauthorizedError` to occur. If you are interested in this API, please
contact the LobbyView team at lobbydata@gmail.com.


#### Parameters:
- str client_uuid: Unique identifier of the client
- str legislator_id: Unique identifier of the legislator
- int report_year: Year of the report
- int min_report_year: Minimum year of the report
- int max_report_year: Maximum year of the report
- int report_quarter_code: Quarter period of the report (returns quarter as string)
- int min_report_quarter_code: Minimum quarter period of the report (returns quarter as string)
- int max_report_quarter_code: Maximum quarter period of the report (returns quarter as string)
- int min_bills_sponsored: Minimum number of bills sponsored by the legislator
    in a specific quarter lobbied by the client
- int max_bills_sponsored: Maximum number of bills sponsored by the legislator
    in a specific quarter lobbied by the client
- int page: Page number of the results, default is 1

#### Returns:
- QuarterLevelNetworkResponse object containing the quarter-level network data


#### Example:
```python
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
```

### Method: bill_client_networks

Gets bill-client network information from the LobbyView API based on the provided
parameters. This API is private and requires special permission to access, users do
not have access by default. Thus, trying to use this method without proper permissions
will cause an `UnauthorizedError` to occur. If you are interested in this API, please
contact the LobbyView team at lobbydata@gmail.com.


#### Parameters:
- int congress_number: Session of Congress
- str bill_id: The unique identifier of the bill in the format [bill_chamber][bill_resolution_type][bill_number] - [congress_number]
    - examples: H.R.1174 - 114
- str bill_chamber: Chamber of the legislative branch (Component of the
    bill_id composite key)
- str bill_resolution_type: Bill type (Component of the bill_id composite key)
- int bill_number: Bill number (Component of the bill_id composite key)
- str report_uuid: Unique identifier of the report
- int issue_ordi: The ordinal number (position) of the issue within the report.
    This is an integer value that represents the order in which the issue appears in
    the report. For example, if an issue has issue_ordi=2, it means it is the second
    issue mentioned in the report.
- str client_uuid: Unique identifier of the client
- int page: Page number of the results, default is 1

#### Returns:
- BillClientNetworkResponse object containing the bill-client network data


#### Example:
```python
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
```

