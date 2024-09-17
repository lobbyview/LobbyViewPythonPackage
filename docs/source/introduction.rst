Introduction
============

The LobbyView Python package is a powerful and easy-to-use library for interacting with the LobbyView API. It provides a convenient way to access and retrieve data related to lobbying activities, legislators, bills, and more. With this package, you can easily integrate lobbying data into your Python projects and perform various analyses.

Features
--------

- **Legislator Data**: Retrieve detailed information about legislators, including their names, IDs, birthdates, and gender.
- **Bill Data**: Access comprehensive data about bills, including bill numbers, titles, sponsors, and status.
- **Client Data**: Get information about lobbying clients, such as client names, IDs, and NAICS codes.
- **Report Data**: Fetch lobbying report data, including report IDs, years, quarters, and amounts.
- **Issue Data**: Retrieve data related to lobbying issues, including issue codes, descriptions, and associated reports.
- **Network Data**: Explore the relationships between legislators and lobbying clients through network data.
- **Text Data**: Access the text data associated with lobbying issues.

The LobbyView package provides a high-level interface to interact with the LobbyView API endpoints. It handles the complexities of making API requests, pagination, and error handling, allowing you to focus on working with the data itself.

Getting Started
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

.. code-block:: text

    export LOBBYVIEW_TOKEN=your-api-token

For Windows:
Open the Command Prompt and run the following command, replacing your-api-token with your actual API token:

.. code-block:: text

    set LOBBYVIEW_TOKEN=your-api-token

Setting the environment variable allows you to keep your API token separate from your code, which is generally considered a good practice for security and maintainability.

2. Pass the API token directly in your code - You can also provide the API token directly when initializing the LobbyView object in your Python code. Here's an example:
    
.. code-block:: python

    from lobbyview import LobbyView

    lv = LobbyView(lobbyview_token="your-api-token")

Replace your-api-token with your actual API token.

While passing the API token directly in your code is convenient, it's usually best practice to use an environment variable to store sensitive information like API tokens. This way, you can avoid accidentally exposing your token if you share your code or publish it to a public repository.

Example Usage
-------------

Here's a simple example of how to use the LobbyView package to retrieve legislator data:

.. code-block:: python

   from lobbyview import LobbyView

    # If you have set the LOBBYVIEW_TOKEN environment variable:
    lv = LobbyView(os.environ.get("LOBBYVIEW_TOKEN"))

    # Alternatively, you can pass the API token directly:
    # lv = LobbyView(lobbyview_token="your-api-token")

   # Search for legislators by ID (bioguide ID)
   legislators = lv.legislators(legislator_id="M000303")
   legislators.data
   # legislators.data will output:
   # [{'legislator_id': 'M000303', 'legislator_govtrack_id': '300071', 'legislator_other_ids': {'fec': ['S6AZ00019', 'P80002801'], 'lis': 'S197', 'cspan': 7476, 'icpsr': 15039, 'thomas': '00754', 'bioguide': 'M000303', 'govtrack': 300071, 'maplight': 592, 'wikidata': 'Q10390', 'votesmart': 53270, 'wikipedia': 'John McCain', 'ballotpedia': 'John McCain', 'opensecrets': 'N00006424', 'house_history': 17696, 'google_entity_id': 'kg:/m/0bymv'}, 'legislator_first_name': 'John', 'legislator_last_name': 'McCain', 'legislator_full_name': 'John McCain', 'legislator_other_names': {'last': 'McCain', 'first': 'John', 'middle': 'S.', 'official_full': 'John McCain'}, 'legislator_birthday': '1936-08-29', 'legislator_gender': 'M'}]

   # Get a specific legislator by name
   legislator = lv.legislators(legislator_first_name="John", legislator_last_name="McCain")
   print(legislator)
   # will output the string formatted data:       
   # Legislators:
     # John McCain (ID: M000303)

This example demonstrates how to create an instance of the ``LobbyView`` class, retrieve a specific legislator by ID, and search for legislators by name.

The package provides similar methods for accessing bill data, client data, report data, issue data, network data, and text data. Refer to the API documentation for more details on available methods and parameters.