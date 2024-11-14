# LobbyView Package Documentation

![Tests](https://github.com/lobbyview/LobbyViewPythonPackage/actions/workflows/python-package.yml/badge.svg)
![Coverage](https://raw.githubusercontent.com/lobbyview/LobbyViewPythonPackage/main/coverage-badge.svg)
![PyPI Downloads](https://raw.githubusercontent.com/lobbyview/LobbyViewPythonPackage/main/download-badge.svg)


The LobbyView Python package is a powerful and easy-to-use library for interacting with the LobbyView API. It provides a convenient way to access and retrieve data related to lobbying activities, legislators, bills, and more. With this package, you can easily integrate lobbying data into your Python projects and perform various analyses.

## Features
--------

- **Legislator Data**: Retrieve detailed information about legislators, including their names, IDs, birthdates, and gender.
- **Bill Data**: Access comprehensive data about bills, including bill numbers, titles, sponsors, and status.
- **Client Data**: Get information about lobbying clients, such as client names, IDs, and NAICS codes.
- **Report Data**: Fetch lobbying report data, including report IDs, years, quarters, and amounts.
- **Issue Data**: Retrieve data related to lobbying issues, including issue codes, descriptions, and associated reports.
- **Network Data**: Explore the relationships between legislators and lobbying clients through network data.
- **Text Data**: Access the text data associated with lobbying issues.

The LobbyView package provides a high-level interface to interact with the LobbyView API endpoints. It handles the complexities of making API requests, pagination, and error handling, allowing you to focus on working with the data itself.

## Getting Started
---------------

To get started with the LobbyView package, you need to have Python installed on your system. The package supports Python versions 3.9 and above.

You can install the LobbyView package using pip:


``pip install lobbyview``

Once installed, you can import the package in your Python code:

``import lobbyview``

To use the LobbyView package, you need to obtain an API token from the LobbyView service. There are two ways to provide your API token to the package:

1. Set the LOBBYVIEW_TOKEN environment variable:

For Unix/Linux (includes MacOS):
Open a terminal and run the following command, replacing your-api-token with your actual API token:


    export LOBBYVIEW_TOKEN=your-api-token

For Windows:
Open the Command Prompt and run the following command, replacing your-api-token with your actual API token:


    set LOBBYVIEW_TOKEN=your-api-token

Setting the environment variable allows you to keep your API token separate from your code, which is generally considered a good practice for security and maintainability.

2. Pass the API token directly in your code - You can also provide the API token directly when initializing the LobbyView object in your Python code. Here's an example:
    

    from lobbyview import LobbyView

    lv = LobbyView(lobbyview_token="your-api-token")

Replace your-api-token with your actual API token.

While passing the API token directly in your code is convenient, it's usually best practice to use an environment variable to store sensitive information like API tokens. This way, you can avoid accidentally exposing your token if you share your code or publish it to a public repository.

# Registration

To register to use the package using a LobbyView API Token, follow these steps:

1. Visit https://www.lobbyview.org
2. Press the user icon on the top right and press "sign in".
3. Next, login if you have an account, or sign up for one by specifying an email address and corresponding organization.
4. Once logged in, navigate to "Data Download".
5. Press "Get Started" under "LobbyView's API".
6. Finally, scroll down and copy your API token.

To contact us for access to other APIs or to increase your quota, please email: lobbydata@gmail.com.

# Classes and Methods

## Class: LobbyView

Main class for interacting with the LobbyView API.

### Method: legislators

Gets legislator information from the LobbyView API based on the provided parameters.

#### Parameters:
- `param str legislator_id`: Unique identifier of the legislator from LobbyView (Bioguide ID)
- `param str legislator_govtrack_id`: Unique identifier of the legislator from
- `param str legislator_first_name`: First name of the legislator - using partial match with ilike operator (PostgreSQL)
- `param str legislator_last_name`: Last name of the legislator - using partial match with ilike operator (PostgreSQL)
- `param str legislator_full_name`: Full name of the legislator (First Middle Last) - using partial match with ilike operator (PostgreSQL)
- `param str legislator_gender`: Gender of the legislator
- `param str birthday`: Exact birthday of the legislator (YYYY-MM-DD)
- `param str min_birthday`: Minimum birthday of the legislator (YYYY-MM-DD)
- `param str max_birthday`: Maximum birthday of the legislator (YYYY-MM-DD)
- `param int page`: Page number of the results, default is 1

#### Example:
```python
>>> output = lobbyview.legislators(legislator_id="M000303")
```python
>>> output.data
[{'legislator_id': 'M000303', 'legislator_govtrack_id': '300071', 'legislator_other_ids': {'fec': ['S6AZ00019', 'P80002801'], 'lis': 'S197', 'cspan': 7476, 'icpsr': 15039, 'thomas': '00754', 'bioguide': 'M000303', 'govtrack': 300071, 'maplight': 592, 'wikidata': 'Q10390', 'votesmart': 53270, 'wikipedia': 'John McCain', 'ballotpedia': 'John McCain', 'opensecrets': 'N00006424', 'house_history': 17696, 'google_entity_id': 'kg:/m/0bymv'}, 'legislator_first_name': 'John', 'legislator_last_name': 'McCain', 'legislator_full_name': 'John McCain', 'legislator_other_names': {'last': 'McCain', 'first': 'John', 'middle': 'S.', 'official_full': 'John McCain'}, 'legislator_birthday': '1936-08-29', 'legislator_gender': 'M'}]
```
```python
>>> output = lobbyview.legislators(legislator_first_name="John", legislator_last_name="McCain")
```python
>>> output.data[0]['legislator_id']
'M000303'
```
```python
>>> output = lobbyview.legislators(legislator_id="M000303", birthday="1936-08-29", min_birthday="1950-08-28")
```python
>>> output.data[0]['legislator_full_name']
'John McCain'
```
```python
>>> output = lobbyview.legislators(legislator_first_name="John", legislator_last_name="McCain")
```python
>>> print(output)
Legislators:
John McCain (ID: M000303)
```
```python
>>> output = lobbyview.legislators(legislator_govtrack_id=412755, legislator_full_name="TJ Cox", legislator_gender="M", min_birthday="1963-03-14", max_birthday="1963-08-14")
```python
>>> print(output)
Legislators:
TJ Cox (ID: C001124)
```
```python
>>> output = lobbyview.legislators(legislator_first_name="John", page=2)
```python
>>> print(output.page_info()['current_page'])
2
```

### Method: bills

Gets bill information from the LobbyView API based on the provided parameters.

#### Parameters:
- `param int congress_number`: Session of Congress
- `param str bill_chamber`: Chamber of the legislative branch
- `param str bill_resolution_type`: Bill type (Component of the bill_id composite
- `param int bill_number`: Bill number (Component of the bill_id composite key)
- `param str bill_state`: Bill status - using partial match with ilike operator (PostgreSQL).
- `param str legislator_id`: Sponsor of the bill
- `param str min_introduced_date`: Minimum date of introduction to Congress
- `param str max_introduced_date`: Maximum date of introduction to Congress
- `param str min_updated_date`: Minimum date of most recent status change
- `param str max_updated_date`: Maximum date of most recent status change
- `param int page`: Page number of the results, default is 1

#### Example:
```python
>>> output = lobbyview.bills(congress_number=111, bill_chamber="H", bill_number=4173)
```python
>>> output.data
[{'congress_number': 111, 'bill_chamber': 'H', 'bill_resolution_type': None, 'bill_number': 4173, 'bill_introduced_datetime': '2009-12-02', 'bill_date_updated': '2016-06-29', 'bill_state': 'ENACTED:SIGNED', 'legislator_id': 'F000339', 'bill_url': 'https://congress.gov/bill/111th-congress/house-bill/4173'}]
```
```python
>>> output = lobbyview.bills(congress_number=111, bill_chamber="H", bill_number=4173)
```python
>>> output.data[0]['bill_state']
'ENACTED:SIGNED'
```
```python
>>> output = lobbyview.bills(congress_number=111, bill_chamber="H", bill_number=4173, bill_resolution_type=None, bill_state="ENACTED:SIGNED", legislator_id="F000339", min_introduced_date="2009-12-01", max_introduced_date="2009-12-03", min_updated_date="2016-06-28", max_updated_date="2016-06-30")
```python
>>> output.data[0]['bill_url']
'https://congress.gov/bill/111th-congress/house-bill/4173'
```
```python
>>> output = lobbyview.bills(congress_number=111, bill_chamber="H", bill_number=4173)
```python
>>> print(output)
Bills:
4173 (Congress: 111, Sponsor: F000339)
```
```python
>>> output = lobbyview.bills(congress_number=116, bill_resolution_type="R", bill_number=400, legislator_id="R000595")
```python
>>> print(output)
Bills:
400 (Congress: 116, Sponsor: R000595)
```
```python
>>> output = lobbyview.bills(min_introduced_date="2020-01-01", page=10)
```python
>>> print(output.page_info()['current_page'])
10
```

### Method: clients

Gets client information from the LobbyView API based on the provided parameters. NAICS (North American Industry Classification System) codes are hierarchical, with the first few digits representing the industry and subindustry. For example, NAICS codes starting with the same first 3 digits belong to the same industry, and codes starting with the same first 4 digits belong to the same subindustry. When specifying the `min_naics` and `max_naics` parameters, keep in mind the hierarchical nature of NAICS codes. For instance, setting `min_naics` to '41' and `max_naics` to '42' will include all NAICS codes starting with '41' and '42', such as '412', '413', etc. **NOT FULLY IMPLEMENTED YET**

#### Parameters:
- `param str client_uuid`: Unique identifier of the client
- `param str client_name`: Name of the client - using partial match with ilike operator (PostgreSQL)
- `param str min_naics`: Minimum NAICS code to which the client belongs (e.g., '41' for industry-level filtering)
- `param str max_naics`: Maximum NAICS code to which the client belongs (e.g., '42' for industry-level filtering)
- `param str naics_description`: Descriptions of the NAICS code - using exact match with cs operator (PostgreSQL)
- `param int page`: Page number of the results, default is 1

#### Example:
```python
>>> output = lobbyview.clients(client_name="Microsoft Corporation", min_naics='51')
```python
>>> output.data
[{'client_uuid': '44563806-56d2-5e99-84a1-95d22a7a69b3', 'client_name': 'Microsoft Corporation', 'primary_naics': '511210', 'naics_description': ['Applications development and publishing, except on a custom basis', 'Applications software, computer, packaged', 'Computer software publishers, packaged', 'Computer software publishing and reproduction', 'Games, computer software, publishing', 'Operating systems software, computer, packaged', 'Packaged computer software publishers', 'Programming language and compiler software publishers, packaged', 'Publishers, packaged computer software', 'Software computer, packaged, publishers', 'Software publishers', 'Software publishers, packaged', 'Utility software, computer, packaged']}]
```
```python
>>> output = lobbyview.clients(client_name="Microsoft Corporation")
```python
>>> output.data[0]['client_uuid']
'44563806-56d2-5e99-84a1-95d22a7a69b3'
```
```python
>>> output = lobbyview.clients(client_uuid="44563806-56d2-5e99-84a1-95d22a7a69b3", min_naics='5112', max_naics='5113')
```python
>>> output.data[0]['client_name']
'Microsoft Corporation'
```
```python
>>> output = lobbyview.clients(client_name="Microsoft Corporation")
```python
>>> print(output)
Clients:
Microsoft Corporation (ID: 44563806-56d2-5e99-84a1-95d22a7a69b3)
PCT Government Relations on behalf of Microsoft Corporation (ID: 62eb98f6-ea3a-542d-abdb-7d2fce94b4f8)
Cornerstone Government Affairs obo Microsoft Corporation (ID: d6634602-1d0b-560d-b4ac-e04194782ad3)
```
```python
>>> output = lobbyview.clients(client_uuid='44563806-56d2-5e99-84a1-95d22a7a69b3', min_naics='5112', max_naics='5113')
```python
>>> print(output)
Clients:
Microsoft Corporation (ID: 44563806-56d2-5e99-84a1-95d22a7a69b3)
```
```python
>>> output = lobbyview.clients(max_naics="5112", page=2)
```python
>>> print(output.page_info()['current_page'])
2
```
```python
>>> output = lobbyview.clients(client_uuid='44563806-56d2-5e99-84a1-95d22a7a69b3', naics_description='Applications software, computer, packaged')
```python
>>> print(output.page_info()['current_page'])
1
```

### Method: reports

Gets report information from the LobbyView API based on the provided parameters.

#### Parameters:
- `param str report_uuid`: Unique identifier of the report
- `param str client_uuid`: Unique identifier of the client
- `param str registrant_uuid`: Unique identifier of the registrant
- `param str registrant_name`: Name of the registrant - using partial match with ilike operator (PostgreSQL)
- `param int report_year`: Year of the report
- `param int min_report_year`: Minimum year of the report
- `param int max_report_year`: Maximum year of the report
- `param int report_quarter_code`: Quarter period of the report (returns quarter as string)
- `param int min_report_quarter_code`: Minimum quarter period of the report (returns quarter as string)
- `param int max_report_quarter_code`: Maximum quarter period of the report (returns quarter as string)
- `param str min_amount`: Minimum lobbying firm income or lobbying expense
- `param str max_amount`: Maximum lobbying firm income or lobbying expense
- `param bool is_no_activity`: Quarterly activity indicator
- `param bool is_client_self_filer`: An organization employing its own in-house
- `param bool is_amendment`: Amendment of previous report
- `param int page`: Page number of the results, default is 1

#### Example:
```python
>>> output = lobbyview.reports(report_year=2020, report_quarter_code=2, is_client_self_filer=True, report_uuid="4b799814-3e94-5ee1-8dd4-b32aead9aca6")
```python
>>> output.data
[{'report_uuid': '4b799814-3e94-5ee1-8dd4-b32aead9aca6', 'client_uuid': 'cdf5a171-6aab-50ea-912c-68c054decdce', 'registrant_uuid': '323adb44-3062-5a5f-98ea-6d4ca51e6f43', 'registrant_name': 'NATIONAL ASSOCIATION OF REALTORS', 'report_year': 2020, 'report_quarter_code': '2', 'amount': '$11,680,000.00', 'is_no_activity': False, 'is_client_self_filer': True, 'is_amendment': False}]
```
```python
>>> output = lobbyview.reports(report_year=2020, report_quarter_code=2, is_client_self_filer=True, report_uuid="4b799814-3e94-5ee1-8dd4-b32aead9aca6")
```python
>>> output.data[0]['amount']
'$11,680,000.00'
```
```python
>>> output = lobbyview.reports(report_year=2020, report_quarter_code=2, is_client_self_filer=True, report_uuid="4b799814-3e94-5ee1-8dd4-b32aead9aca6", min_report_quarter_code=5, max_report_quarter_code=0)
```python
>>> output.data[0]['amount']
'$11,680,000.00'
```
```python
>>> output = lobbyview.reports(client_uuid="cdf5a171-6aab-50ea-912c-68c054decdce", registrant_uuid="323adb44-3062-5a5f-98ea-6d4ca51e6f43", registrant_name="NATIONAL ASSOCIATION OF REALTORS", min_amount="$11,679,999.99", max_amount="$11,680,000.01", is_no_activity=False, is_amendment=False, min_report_year=2017, max_report_year=2023)
```python
>>> output.data[0]['report_year']
2020
```
```python
>>> output = lobbyview.reports(client_uuid="cdf5a171-6aab-50ea-912c-68c054decdce", registrant_uuid="323adb44-3062-5a5f-98ea-6d4ca51e6f43", registrant_name="NATIONAL ASSOCIATION OF REALTORS", min_amount="$11,679,999.99", max_amount="$11,680,000.01", is_no_activity=False, is_amendment=False, report_year=2020, min_report_year=2040, max_report_year=1800)
```python
>>> output.data[0]['report_year']
2020
```
```python
>>> output = lobbyview.reports(report_year=2020, report_quarter_code=2, is_client_self_filer=True, report_uuid="4b799814-3e94-5ee1-8dd4-b32aead9aca6")
```python
>>> print(output)
Reports:
4b799814-3e94-5ee1-8dd4-b32aead9aca6 (Year: 2020, Quarter: 2)
```
```python
>>> output = lobbyview.reports(client_uuid="78043d66-6dc9-5d6c-b0ee-c3afaa33d8d7", report_year=2020, min_report_quarter_code=2, max_report_quarter_code=4, min_amount=150000)
```python
>>> print(output)
Reports:
e2fb926a-2ac5-5c5c-9140-54b4c79d7e56 (Year: 2020, Quarter: 2)
```
```python
>>> output = lobbyview.reports(report_year=2020, page=2)
```python
>>> print(output.page_info()['current_page'])
2
```

### Method: issues

Gets issue information from the LobbyView API based on the provided parameters.

#### Parameters:
- `param str report_uuid`: Unique identifier of the report
- `param int issue_ordi`: The ordinal number (position) of the issue within the report.
- `param str issue_code`: General Issue Area Code (Section 15)
- `param str gov_entity`: House(s) of Congress and Federal agencies (Section 17) - using
- `param int page`: Page number of the results, default is 1

#### Example:
```python
>>> output = lobbyview.issues(issue_code="TRD", report_uuid="00016ab3-2246-5af8-a68d-05af40dfde68", issue_ordi=2)
```python
>>> output.data
[{'report_uuid': '00016ab3-2246-5af8-a68d-05af40dfde68', 'issue_ordi': 2, 'issue_code': 'TRD', 'gov_entity': ['HOUSE OF REPRESENTATIVES', 'SENATE']}]
```
```python
>>> output = lobbyview.issues(issue_code="TRD")
```python
>>> output.data[0]['report_uuid']
'00016ab3-2246-5af8-a68d-05af40dfde68'
```
```python
>>> output = lobbyview.issues(issue_code="TRD")
```python
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
```python
>>> output = lobbyview.issues(issue_code="TRD", page=2)
```python
>>> print(output.page_info()['current_page'])
2
```
```python
>>> output = lobbyview.issues(report_uuid='00016ab3-2246-5af8-a68d-05af40dfde68', gov_entity='SENATE')
```python
>>> output.data
[{'report_uuid': '00016ab3-2246-5af8-a68d-05af40dfde68', 'issue_ordi': 1, 'issue_code': 'SMB', 'gov_entity': ['SENATE', 'SMALL BUSINESS ADMINISTRATION', 'HOUSE OF REPRESENTATIVES']}, {'report_uuid': '00016ab3-2246-5af8-a68d-05af40dfde68', 'issue_ordi': 2, 'issue_code': 'TRD', 'gov_entity': ['HOUSE OF REPRESENTATIVES', 'SENATE']}]
```

### Method: networks

Gets network information from the LobbyView API based on the provided parameters.

#### Parameters:
- `param str client_uuid`: Unique identifier of the client
- `param str legislator_id`: Unique identifier of the legislator
- `param int report_year`: Year of the report
- `param int min_report_year`: Minimum year of the report
- `param int max_report_year`: Maximum year of the report
- `param int min_bills_sponsored`: Minimum number of bills sponsored by the legislator
- `param int max_bills_sponsored`: Maximum number of bills sponsored by the legislator
- `param int page`: Page number of the results, default is 1

#### Example:
```python
>>> output = lobbyview.networks(client_uuid="44563806-56d2-5e99-84a1-95d22a7a69b3", legislator_id="M000303")
```python
>>> output.data
[{'client_uuid': '44563806-56d2-5e99-84a1-95d22a7a69b3', 'legislator_id': 'M000303', 'report_year': 2006, 'n_bills_sponsored': 1}, {'client_uuid': '44563806-56d2-5e99-84a1-95d22a7a69b3', 'legislator_id': 'M000303', 'report_year': 2017, 'n_bills_sponsored': 1}]
```
```python
>>> output = lobbyview.networks(client_uuid="44563806-56d2-5e99-84a1-95d22a7a69b3", legislator_id="M000303")
```python
>>> output.data[0]['report_year']
2006
```
```python
>>> output = lobbyview.networks(client_uuid="44563806-56d2-5e99-84a1-95d22a7a69b3", legislator_id="M000303", min_report_year=2016, max_report_year=2018, min_bills_sponsored=0, max_bills_sponsored=2)
```python
>>> output.data[0]['n_bills_sponsored']
1
```
```python
>>> output = lobbyview.networks(client_uuid="44563806-56d2-5e99-84a1-95d22a7a69b3", legislator_id="M000303", report_year=2006)
```python
>>> output.data[0]['n_bills_sponsored']
1
```
```python
>>> output = lobbyview.networks(client_uuid="44563806-56d2-5e99-84a1-95d22a7a69b3", legislator_id="M000303")
```python
>>> print(output)
Networks:
Client UUID: 44563806-56d2-5e99-84a1-95d22a7a69b3, Legislator ID: M000303, Year: 2006, Bills Sponsored: 1
Client UUID: 44563806-56d2-5e99-84a1-95d22a7a69b3, Legislator ID: M000303, Year: 2017, Bills Sponsored: 1
```
```python
>>> output = lobbyview.networks(min_report_year=2016, max_report_year=2018, min_bills_sponsored=0, max_bills_sponsored=2, client_uuid="44563806-56d2-5e99-84a1-95d22a7a69b3", legislator_id="M000303")
```python
>>> print(output)
Networks:
Client UUID: 44563806-56d2-5e99-84a1-95d22a7a69b3, Legislator ID: M000303, Year: 2017, Bills Sponsored: 1
```
```python
>>> output = lobbyview.networks(min_bills_sponsored=50, page=2)
```python
>>> print(output.page_info()['current_page'])
2
```

### Method: texts

Gets issue text data from the LobbyView API based on the provided parameters.

#### Parameters:
- `param str report_uuid`: Unique identifier of the report
- `param int issue_ordi`: The ordinal number (position) of the issue within the report.
- `param str issue_code`: General Issue Area Code (Section 15)
- `param str issue_text`: Specific lobbying issues (Section 16) - using partial match with ilike operator (PostgreSQL).
- `param int page`: Page number of the results, default is 1

#### Example:
```python
>>> output = lobbyview.texts(issue_code="HCR", issue_text="covid", report_uuid="000bef17-9f0a-5d7c-8660-edca16e1dfce")
```python
>>> output.data
[{'report_uuid': '000bef17-9f0a-5d7c-8660-edca16e1dfce', 'issue_ordi': 1, 'issue_code': 'HCR', 'issue_text': 'HR 748 CARES Act - Issues related to COVID-19 relief'}]
```
```python
>>> output = lobbyview.texts(issue_code="HCR", issue_text="covid")
```python
>>> output.data[0]['issue_ordi']
1
```
```python
>>> output = lobbyview.texts(issue_code="HCR", report_uuid="000bef17-9f0a-5d7c-8660-edca16e1dfce", issue_ordi=1)
```python
>>> output.data[0]['issue_text']
'HR 748 CARES Act - Issues related to COVID-19 relief'
```
```python
>>> output = lobbyview.texts(issue_code="HCR", issue_text="covid")
```python
>>> print(output)
Texts:
Issue Code: HCR
Issue Text: HR 748 CARES Act - Issues related to COVID-19 relief
...
```
```python
>>> output = lobbyview.texts(report_uuid='000bef17-9f0a-5d7c-8660-edca16e1dfce', issue_ordi=1)
```python
>>> print(output)
Texts:
Issue Code: HCR
Issue Text: HR 748 CARES Act - Issues related to COVID-19 relief
```

### Method: quarter_level_networks

Gets quarter-level network information from the LobbyView API based on the provided parameters. This API is private and requires special permission to access, users do not have access by default. Thus, trying to use this method without proper permissions will cause an `UnauthorizedError` to occur. If you are interested in this API, please contact the LobbyView team at lobbydata@gmail.com.

#### Parameters:
- `param str client_uuid`: Unique identifier of the client
- `param str legislator_id`: Unique identifier of the legislator
- `param int report_year`: Year of the report
- `param int min_report_year`: Minimum year of the report
- `param int max_report_year`: Maximum year of the report
- `param int report_quarter_code`: Quarter period of the report (returns quarter as string)
- `param int min_report_quarter_code`: Minimum quarter period of the report (returns quarter as string)
- `param int max_report_quarter_code`: Maximum quarter period of the report (returns quarter as string)
- `param int min_bills_sponsored`: Minimum number of bills sponsored by the legislator
- `param int max_bills_sponsored`: Maximum number of bills sponsored by the legislator
- `param int page`: Page number of the results, default is 1

#### Example:
```python
>>> output = lobbyview.quarter_level_networks(client_uuid="44563806-56d2-5e99-84a1-95d22a7a69b3", legislator_id="M000303", report_year=2017, report_quarter_code=4)
```python
>>> output.data
[{'client_uuid': '44563806-56d2-5e99-84a1-95d22a7a69b3', 'legislator_id': 'M000303', 'report_year': 2017, 'report_quarter_code': '4', 'n_bills_sponsored': 1}]
```
```python
>>> output = lobbyview.quarter_level_networks(client_uuid="44563806-56d2-5e99-84a1-95d22a7a69b3", legislator_id="M000303", report_year=2017, report_quarter_code=4)
```python
>>> output.data[0]['n_bills_sponsored']
1
```
```python
>>> output = lobbyview.quarter_level_networks(client_uuid="44563806-56d2-5e99-84a1-95d22a7a69b3", legislator_id="M000303", report_year=2017, report_quarter_code=4, min_report_quarter_code=9, max_report_quarter_code=-2)
```python
>>> output.data[0]['n_bills_sponsored']
1
```
```python
>>> output = lobbyview.quarter_level_networks(client_uuid="44563806-56d2-5e99-84a1-95d22a7a69b3", legislator_id="M000303", report_year=2017, min_report_quarter_code=3, max_report_quarter_code=5)
```python
>>> output.data[0]['n_bills_sponsored']
1
```
```python
>>> output = lobbyview.quarter_level_networks(client_uuid="44563806-56d2-5e99-84a1-95d22a7a69b3", legislator_id="M000303", report_year=2017, min_report_year=2030, max_report_year=2000)
```python
>>> output.data[0]['n_bills_sponsored']
1
```
```python
>>> output = lobbyview.quarter_level_networks(client_uuid="44563806-56d2-5e99-84a1-95d22a7a69b3", legislator_id="M000303", min_report_year=2016, max_report_year=2018)
```python
>>> output.data[0]['n_bills_sponsored']
1
```
```python
>>> output = lobbyview.quarter_level_networks(client_uuid="44563806-56d2-5e99-84a1-95d22a7a69b3", legislator_id="M000303", report_year=2017, min_bills_sponsored=0, max_bills_sponsored=2)
```python
>>> output.data[0]['report_quarter_code']
'4'
```
```python
>>> output = lobbyview.quarter_level_networks(client_uuid="44563806-56d2-5e99-84a1-95d22a7a69b3", legislator_id="M000303", report_year=2017, report_quarter_code=4)
```python
>>> print(output)
Quarter-Level Networks:
Client UUID: 44563806-56d2-5e99-84a1-95d22a7a69b3, Legislator ID: M000303, Year: 2017, Quarter: 4, Bills Sponsored: 1
```
```python
>>> output = lobbyview.quarter_level_networks(min_bills_sponsored=0, max_bills_sponsored=2, client_uuid="44563806-56d2-5e99-84a1-95d22a7a69b3", legislator_id="M000303")
```python
>>> print(output)
Quarter-Level Networks:
Client UUID: 44563806-56d2-5e99-84a1-95d22a7a69b3, Legislator ID: M000303, Year: 2006, Quarter: 34, Bills Sponsored: 1
Client UUID: 44563806-56d2-5e99-84a1-95d22a7a69b3, Legislator ID: M000303, Year: 2017, Quarter: 4, Bills Sponsored: 1
```
```python
>>> output = lobbyview.quarter_level_networks(min_bills_sponsored=20, page=2)
```python
>>> print(output.page_info()['current_page'])
2
```

### Method: bill_client_networks

Gets bill-client network information from the LobbyView API based on the provided parameters. This API is private and requires special permission to access, users do not have access by default. Thus, trying to use this method without proper permissions will cause an `UnauthorizedError` to occur. If you are interested in this API, please contact the LobbyView team at lobbydata@gmail.com.

#### Parameters:
- `param int congress_number`: Session of Congress
- `param str bill_id`: The unique identifier of the bill in the format [bill_chamber].[bill_number]-[congress_number]
- `param str bill_chamber`: Chamber of the legislative branch (Component of the
- `param str bill_resolution_type`: Bill type (Component of the bill_id composite key)
- `param int bill_number`: Bill number (Component of the bill_id composite key)
- `param str report_uuid`: Unique identifier of the report
- `param int issue_ordi`: The ordinal number (position) of the issue within the report.
- `param str client_uuid`: Unique identifier of the client
- `param int page`: Page number of the results, default is 1

#### Example:
```python
>>> output = lobbyview.bill_client_networks(congress_number=114, bill_chamber="H", bill_number=1174, client_uuid="44563806-56d2-5e99-84a1-95d22a7a69b3", report_uuid="006bd48b-59cf-5cbc-99b8-fc213e509a86")
```python
>>> output.data
[{'congress_number': 114, 'bill_chamber': 'H', 'bill_resolution_type': None, 'bill_number': 1174, 'report_uuid': '006bd48b-59cf-5cbc-99b8-fc213e509a86', 'issue_ordi': 2, 'client_uuid': '44563806-56d2-5e99-84a1-95d22a7a69b3'}]
```
```python
>>> output = lobbyview.bill_client_networks(congress_number=114, bill_chamber="H", bill_resolution_type='C', report_uuid="00043607-ec6d-53a8-85b4-d418a64b423e")
```python
>>> output.data[0]['bill_number']
125
```
```python
>>> output = lobbyview.bill_client_networks(congress_number=114, bill_chamber="H", bill_number=1174, client_uuid="44563806-56d2-5e99-84a1-95d22a7a69b3", report_uuid="006bd48b-59cf-5cbc-99b8-fc213e509a86")
```python
>>> output.data[0]['issue_ordi']
2
```
```python
>>> output = lobbyview.bill_client_networks(report_uuid="006bd48b-59cf-5cbc-99b8-fc213e509a86", issue_ordi=2)
```python
>>> output.data[0]['bill_number']
1174
```
```python
>>> output = lobbyview.bill_client_networks(congress_number=114, bill_chamber="H", bill_number=1174, client_uuid="44563806-56d2-5e99-84a1-95d22a7a69b3")
```python
>>> print(output)
Bill-Client Networks:
Bill Number: 1174, Client UUID: 44563806-56d2-5e99-84a1-95d22a7a69b3, Issue Ordinal number (position) of the issue within the report: 2
Bill Number: 1174, Client UUID: 44563806-56d2-5e99-84a1-95d22a7a69b3, Issue Ordinal number (position) of the issue within the report: 5
Bill Number: 1174, Client UUID: 44563806-56d2-5e99-84a1-95d22a7a69b3, Issue Ordinal number (position) of the issue within the report: 4
...
```
```python
>>> output = lobbyview.bill_client_networks(report_uuid='006bd48b-59cf-5cbc-99b8-fc213e509a86', issue_ordi=2)
```python
>>> print(output)
Bill-Client Networks:
Bill Number: 1174, Client UUID: 44563806-56d2-5e99-84a1-95d22a7a69b3, Issue Ordinal number (position) of the issue within the report: 2
Bill Number: 512, Client UUID: 44563806-56d2-5e99-84a1-95d22a7a69b3, Issue Ordinal number (position) of the issue within the report: 2
```
```python
>>> output = lobbyview.bill_client_networks(bill_chamber="H", bill_resolution_type='C', congress_number=116, page=2)
```python
>>> print(output.page_info()['current_page'])
2
```python
>>> output = lobbyview.bill_client_networks(bill_id="H.R.1174-114")
```python
>>> print(output.page_info()['total_pages'])
3
```