Usage
=====

The LobbyView Python package provides a simple and intuitive interface for interacting with the LobbyView API. This section will guide you through the usage of the package and demonstrate how to retrieve various types of data.

Initialization
--------------

To start using the LobbyView package, you need to create an instance of the ``LobbyView`` class. Make sure you have obtained an API token from the LobbyView website at lobbyview.org and set it as an environment variable or pass it directly to the constructor.

.. code-block:: python

   from lobbyview import LobbyView

   lv = LobbyView(lobbyview_token="your-api-token")

Replace ``'your-api-token'`` with your actual API token.

When making a query and retreiving data, the LobbyView package will return a response object that contains the data retrieved from the API. The response object has the following attributes (assuming the response object is ``self``):
self.data: This is the actual data that was retrieved from the API.
self.current_page: This is the current page number in the data pagination.
self.total_pages: This is the total number of pages available in the data.
self.total_rows: This is the total number of rows available in the data, not necessarily the number of rows in the current response.

You'll mainly be interested in the ``data`` attribute, which contains the actual data retrieved from the API. Below are examples of how to use the LobbyView package to retrieve data about legislators, bills, clients, reports, issues, networks, texts, quarter-level networks, and bill-client networks.

Retrieving Legislator Data
--------------------------

You can retrieve data about legislators using the ``legislators`` method:

.. code-block:: python

    # Get a specific legislator by ID
    legislators_output = lv.legislators(legislator_id="M000303")
    legislators_output.data
    # legislators.data will output:
    # [{'legislator_id': 'M000303', 'legislator_govtrack_id': '300071', 'legislator_other_ids': {'fec': ['S6AZ00019', 'P80002801'], 'lis': 'S197', 'cspan': 7476, 'icpsr': 15039, 'thomas': '00754', 'bioguide': 'M000303', 'govtrack': 300071, 'maplight': 592, 'wikidata': 'Q10390', 'votesmart': 53270, 'wikipedia': 'John McCain', 'ballotpedia': 'John McCain', 'opensecrets': 'N00006424', 'house_history': 17696, 'google_entity_id': 'kg:/m/0bymv'}, 'legislator_first_name': 'John', 'legislator_last_name': 'McCain', 'legislator_full_name': 'John McCain', 'legislator_other_names': {'last': 'McCain', 'first': 'John', 'middle': 'S.', 'official_full': 'John McCain'}, 'legislator_birthday': '1936-08-29', 'legislator_gender': 'M'}]
    # getting a specific lagislator's data, for example the first one in the matching output:
    legislator = legislators_output.data[0]
    print(legislator['legislator_full_name'])  # Output: 'John McCain'

    # Search for legislators by name
    legislators_output = lv.legislators(legislator_first_name="John", legislator_last_name="McCain")
    legislator_id = legislators_output.data[0]['legislator_id']
    print(legislator_id)  # Output: M000303

Retrieving Bill Data
--------------------

You can retrieve data about bills using the ``bills`` method:

.. code-block:: python
    
    bills_output = lv.bills(congress_number=111, bill_chamber="H", bill_number=4173)
    bills_output.data
    # bills_output.data will output: [{'congress_number': 111, 'bill_chamber': 'H', 'bill_resolution_type': None, 'bill_number': 4173, 'bill_introduced_datetime': '2009-12-02', 'bill_date_updated': '2016-06-29', 'bill_state': 'ENACTED:SIGNED', 'legislator_id': 'F000339', 'bill_url': 'https://congress.gov/bill/111th-congress/house-bill/4173'}]
    bill_state = bills_output.data[0]['bill_state']
    print(bill_state)  # Output: ENACTED:SIGNED

Retrieving Client Data
----------------------

You can retrieve data about lobbying clients using the ``clients`` method:

.. code-block:: python

    # Search for clients by name
    clients_output = lv.clients(client_name="Microsoft Corporation")
    clients_output.data
    # clients_output.data will output: [{'client_uuid': '44563806-56d2-5e99-84a1-95d22a7a69b3', 'client_name': 'Microsoft Corporation', 'primary_naics': '511210', 'naics_description': ['Applications development and publishing, except on a custom basis', 'Applications software, computer, packaged', 'Computer software publishers, packaged', 'Computer software publishing and reproduction', 'Games, computer software, publishing', 'Operating systems software, computer, packaged', 'Packaged computer software publishers', 'Programming language and compiler software publishers, packaged', 'Publishers, packaged computer software', 'Software computer, packaged, publishers', 'Software publishers', 'Software publishers, packaged', 'Utility software, computer, packaged']}]
    client_uuid = clients_output.data[0]['client_uuid']
    print(client_uuid)  # Output: 44563806-56d2-5e99-84a1-95d22a7a69b3

Retrieving Report Data
----------------------

You can retrieve lobbying report data using the ``reports`` method:

.. code-block:: python

    # Get a specific report by year, quarter, client self-filer status, and report UUID
    reports_output = lv.reports(report_year=2020, report_quarter_code="2", is_client_self_filer=True, report_uuid="4b799814-3e94-5ee1-8dd4-b32aead9aca6")
    reports_output.data
    # reports_output.data will output: [{'report_uuid': '4b799814-3e94-5ee1-8dd4-b32aead9aca6', 'client_uuid': 'cdf5a171-6aab-50ea-912c-68c054decdce', 'registrant_uuid': '323adb44-3062-5a5f-98ea-6d4ca51e6f43', 'registrant name': 'NATIONAL ASSOCIATION OF REALTORS', 'report_year': 2020, 'report_quarter_code': '2', 'amount': '$11,680,000.00', 'is_no_activity': False, 'is_client_self_filer': True, 'is_amendment': False}]
    amount = reports_output.data[0]['amount']
    print(amount)  # Output: $11,680,000.00

Retrieving Issue Data
---------------------

You can retrieve data about lobbying issues using the ``issues`` method:

.. code-block:: python

    # Search for issues by issue code and report uuid
    issues_output = lv.issues(issue_code="TRD", report_uuid="00016ab3-2246-5af8-a68d-05af40dfde68", issue_ordi=2)
    issues_output.data
    # issues_output.data will output: [{'report_uuid': '00016ab3-2246-5af8-a68d-05af40dfde68', 'issue_ordi': 2, 'issue_code': 'TRD', 'gov_entity': ['HOUSE OF REPRESENTATIVES', 'SENATE']}]
    gov_entity = issues_output.data[0]['gov_entity']
    print(gov_entity)  # Output: ['HOUSE OF REPRESENTATIVES', 'SENATE']

Retrieving Network Data
-----------------------

You can retrieve network data that represents relationships between legislators and lobbying clients using the ``networks`` method:

.. code-block:: python

    # Get network data for a specific client and legislator
    network_output = lv.networks(client_uuid="44563806-56d2-5e99-84a1-95d22a7a69b3", legislator_id="M000303")
    network_output.data
    # network_output.data will output: [{'client_uuid': '44563806-56d2-5e99-84a1-95d22a7a69b3', 'legislator_id': 'M000303', 'report_year': 2006, 'n_bills_sponsored': 1}, {'client_uuid': '44563806-56d2-5e99-84a1-95d22a7a69b3', 'legislator_id': 'M000303', 'report_year': 2017, 'n_bills_sponsored': 1}]
    report_year = network_output.data[0]['report_year']
    print(report_year)  # Output: 2006

Retrieving Text Data
--------------------

You can retrieve text data associated with lobbying issues using the ``texts`` method:

.. code-block:: python

    # Search for text data by issue code and text content
    texts_output = lv.texts(issue_code="HCR", issue_text="covid", report_uuid="000bef17-9f0a-5d7c-8660-edca16e1dfce")
    texts_output.data
    # texts_output.data will output: [{'report_uuid': '000bef17-9f0a-5d7c-8660-edca16e1dfce', 'issue_ordi': 1, 'issue_code': 'HCR', 'issue_text': 'HR 748 CARES Act - Issues related to COVID-19 relief'}]
    issue_text = texts_output.data[0]['issue_text']
    print(issue_text)  # Output: 'HR 748 CARES Act - Issues related to COVID-19 relief'

Retrieving Quarter-Level Network Data
-------------------------------------

This API is private and requires special permission to access, users do not have access by default. Thus, trying to use this method without proper permissions will cause an `UnauthorizedError` to occur. If you are interested in this API, please contact the LobbyView team at lobbydata@gmail.com.

You can retrieve quarter-level network data using the ``quarter_level_networks`` method:

.. code-block:: python

    # Get quarter-level network data for a specific client, legislator, year, and quarter
    quarter_level_networks_output = lv.quarter_level_networks(client_uuid="44563806-56d2-5e99-84a1-95d22a7a69b3", legislator_id="M000303", report_year=2017, report_quarter_code=4)
    quarter_level_networks_output.data
    # quarter_level_networks_output.data will output: [{'client_uuid': '44563806-56d2-5e99-84a1-95d22a7a69b3', 'legislator_id': 'M000303', 'report_year': 2017, 'report_quarter_code': 4, 'n_bills_sponsored': 1}]
    bills_sponsored = quarter_level_networks_output.data[0]['n_bills_sponsored']
    print(bills_sponsored)  # Output: 1

Retrieving Bill-Client Network Data
-----------------------------------

This API is private and requires special permission to access, users do not have access by default. Thus, trying to use this method without proper permissions will cause an `UnauthorizedError` to occur. If you are interested in this API, please contact the LobbyView team at lobbydata@gmail.com.

You can retrieve bill-client network data using the ``bill_client_networks`` method:

.. code-block:: python

    # Get bill-client network data for a specific bill and client
    bill_client_networks_output = lv.bill_client_networks(congress_number=114, bill_chamber="H", bill_number=1174, client_uuid="44563806-56d2-5e99-84a1-95d22a7a69b3")
    bill_client_networks_output.data
    # bill_client_networks_output.data will output: [{'congress_number': 114, 'bill_chamber': 'H', 'bill_resolution_type': None, 'bill_number': 1174, 'report_uuid': '006bd48b-59cf-5cbc-99b8-fc213e509a86', 'issue_ordi': 2, 'client_uuid': '44563806-56d2-5e99-84a1-95d22a7a69b3'}]
    report_uuid = bill_client_networks_output.data[0]['report_uuid']
    print(report_uuid)  # Output: '006bd48b-59cf-5cbc-99b8-fc213e509a86'

Using Pagination to Retrieve Data
---------------------------------

The ``paginate`` method allows you to retrieve data in manageable chunks, which is especially useful when dealing with large datasets. Here's an example of how to use it:

.. code-block:: python

    # Get issue text data for all reports that contain the word "covid" under the issue code "HCR"
    for text in lobbyview.paginate(lobbyview.texts, issue_code="HCR", issue_text="covid"):
        print(f"Issue Code: {text['issue_code']}")
    # output looks like:
    # Retrieving page 1...
    # Issue Code: HCR
    # ...
    # Retrieving page 2...
    # Issue Code: HCR
    # ...


These examples demonstrate how to use the main methods provided by the LobbyView package to retrieve different types of data from the LobbyView API. Each method returns a response object containing the retrieved data (as explained at the top of this page), which can be accessed using the ``data`` attribute.

Remember to handle any exceptions that may occur during API requests, such as authentication errors or rate limiting (more information about specific errors can be found in the API documentation and troubleshooting pages of this documentation).

For more detailed information on the available parameters and return values for each method, please also refer to the API documentation.
