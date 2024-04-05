Usage
=====

The LobbyView Python package provides a simple and intuitive interface for interacting with the LobbyView API. This section will guide you through the usage of the package and demonstrate how to retrieve various types of data.

Initialization
--------------

To start using the LobbyView package, you need to create an instance of the ``LobbyView`` class. Make sure you have obtained an API token from the LobbyView website at lobbyview.org and set it as an environment variable or pass it directly to the constructor.

.. code-block:: python

   from lobbyview import LobbyView

   lv = LobbyView(api_token='your-api-token')

Replace ``'your-api-token'`` with your actual API token.

Retrieving Legislator Data
--------------------------

You can retrieve data about legislators using the ``legislators`` method:

.. code-block:: python

    # Get a specific legislator by ID
    output = lv.legislators(legislator_id="M000303")
    legislator = output.data[0]
    print(legislator['legislator_full_name'])  # Output: John McCain

    # Search for legislators by name
    output = lv.legislators(legislator_first_name="John", legislator_last_name="McCain")
    legislator_id = output.data[0]['legislator_id']
    print(legislator_id)  # Output: M000303

Retrieving Bill Data
--------------------

You can retrieve data about bills using the ``bills`` method:

.. code-block:: python

    # Get a specific bill by congress number, chamber, and bill number
    output = lv.bills(congress_number=111, bill_chamber="H", bill_number=4173)
    bill_state = output.data[0]['bill_state']
    print(bill_state)  # Output: ENACTED:SIGNED

Retrieving Client Data
----------------------

You can retrieve data about lobbying clients using the ``clients`` method:

.. code-block:: python

    # Search for clients by name
    output = lv.clients(client_name="Microsoft Corporation")
    client_uuid = output.data[0]['client_uuid']
    print(client_uuid)  # Output: 44563806-56d2-5e99-84a1-95d22a7a69b3

Retrieving Report Data
----------------------

You can retrieve lobbying report data using the ``reports`` method:

.. code-block:: python

    # Get a specific report by year, quarter, client self-filer status, and report UUID
    output = lv.reports(report_year=2020, report_quarter_code="2", is_client_self_filer=True, report_uuid="4b799814-3e94-5ee1-8dd4-b32aead9aca6")
    amount = output.data[0]['amount']
    print(amount)  # Output: $11,680,000.00

Retrieving Issue Data
---------------------

You can retrieve data about lobbying issues using the ``issues`` method:

.. code-block:: python

    # Search for issues by issue code
    output = lv.issues(issue_code="TRD")

Retrieving Network Data
-----------------------

You can retrieve network data that represents relationships between legislators and lobbying clients using the ``networks`` method:

.. code-block:: python

    # Get network data for a specific client and legislator
    output = lv.networks(client_uuid="44563806-56d2-5e99-84a1-95d22a7a69b3", legislator_id="M000303")
    report_year = output.data[0]['report_year']
    print(report_year)  # Output: 2017

Retrieving Text Data
--------------------

You can retrieve text data associated with lobbying issues using the ``texts`` method:

.. code-block:: python

    # Search for text data by issue code and text content
    output = lv.texts(issue_code="HCR", issue_text="covid")

Retrieving Quarter-Level Network Data
-------------------------------------

You can retrieve quarter-level network data using the ``quarter_level_networks`` method:

.. code-block:: python

    # Get quarter-level network data for a specific client, legislator, year, and quarter
    output = lv.quarter_level_networks(client_uuid="44563806-56d2-5e99-84a1-95d22a7a69b3", legislator_id="M000303", report_year=2017, report_quarter_code=4)
    bills_sponsored = output.data[0]['n_bills_sponsored']
    print(bills_sponsored)  # Output: 1

Retrieving Bill-Client Network Data
-----------------------------------

You can retrieve bill-client network data using the ``bill_client_networks`` method:

.. code-block:: python

    # Get bill-client network data for a specific bill and client
    output = lv.bill_client_networks(congress_number=114, bill_chamber="H", bill_number=1174, client_uuid="44563806-56d2-5e99-84a1-95d22a7a69b3")
    issue_ordi = output.data[0]['issue_ordi']
    print(issue_ordi)  # Output: 2

These examples demonstrate how to use the main methods provided by the LobbyView package to retrieve different types of data from the LobbyView API. Each method returns a response object containing the retrieved data, which can be accessed using the ``data`` attribute.

Remember to handle any exceptions that may occur during API requests, such as authentication errors or rate limiting.

For more detailed information on the available parameters and return values for each method, please refer to the API documentation.