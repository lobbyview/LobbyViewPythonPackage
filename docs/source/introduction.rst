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

To use the package, you need to obtain an API token from the LobbyView service. Set the ``LOBBYVIEW_TOKEN`` environment variable with your API token:

.. code-block:: text

    export LOBBYVIEW_TOKEN=your-api-token  # For Unix/Linux

    set LOBBYVIEW_TOKEN=your-api-token  # For Windows

Replace ``your-api-token`` with your actual API token.

Example Usage
-------------

Here's a simple example of how to use the LobbyView package to retrieve legislator data:

.. code-block:: python

   from lobbyview import LobbyView

   lv = LobbyView(api_token='your-api-token')

   # Get a specific legislator by ID
   legislator = lv.legislators(legislator_id='L000123')
   print(legislator[0])

   # Search for legislators by name
   legislators = lv.search_legislators(legislator_first_name='John')
   for legislator in legislators:
       print(legislator)

This example demonstrates how to create an instance of the ``LobbyView`` class, retrieve a specific legislator by ID, and search for legislators by name.

The package provides similar methods for accessing bill data, client data, report data, issue data, network data, and text data. Refer to the API documentation for more details on available methods and parameters.