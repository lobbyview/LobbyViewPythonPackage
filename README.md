# LobbyView Package Documentation

Python wrapper for Lobbyview Rest API; uses same endpoints and parameter names as outlined in the
[LobbyView Rest API Documentation](https://rest-api.lobbyview.org/)

## Class: LobbyViewResponse

Base class for LobbyView API responses.


## Class: LegislatorResponse

Response class for legislator data.


## Class: BillResponse

Response class for bill data.


## Class: ClientResponse

Response class for client data.


## Class: ReportResponse

Response class for report data.


## Class: IssueResponse

Response class for issue data.


## Class: NetworkResponse

Response class for network data.


## Class: TextResponse

Response class for text data.


## Class: QuarterLevelNetworkResponse

Response class for quarter-level network data.


## Class: BillClientNetworkResponse

Response class for bill-client network data.


## Class: LobbyView

Main class for interacting with the LobbyView API.


### Method: __init__

Initialize the LobbyView class with the provided API token.


### Method: get_data

Sends a GET request to the LobbyView API with the provided query string.
Returns the JSON response data.


### Method: legislators

Gets legislator information from the LobbyView API based on the provided parameters.


#### Parameters:
- legislator_id: Unique identifier of the legislator from LobbyView
- legislator_govtrack_id: Unique identifier of the legislator from GovTrack
- legislator_first_name: First name of the legislator
- legislator_last_name: Last name of the legislator
- legislator_full_name: Full name of the legislator
- legislator_gender: Gender of the legislator
- min_birthday: Minimum birthday of the legislator (YYYY-MM-DD)
- max_birthday: Maximum birthday of the legislator (YYYY-MM-DD)

#### Returns:
- LegislatorResponse object containing the legislator data


#### Example:
```python
>>> lobbyview = LobbyView(LOBBYVIEW_TOKEN)
>>> output = lobbyview.legislators(legislator_first_name="John", legislator_last_name="McCain")
>>> output.data[0]['legislator_id']
'M000303'
>>> output = lobbyview.legislators(legislator_id="M000303")
>>> output.data[0]['legislator_full_name']
'John McCain'
```

### Method: bills

Gets bill information from the LobbyView API based on the provided parameters.


#### Parameters:
- congress_number: Session of Congress
- bill_chamber: Chamber of the legislative branch (Component of the bill_id composite key)
- bill_resolution_type: Bill type (Component of the bill_id composite key)
- bill_number: Bill number (Component of the bill_id composite key)
- bill_state: Bill status
- legislator_id: Sponsor of the bill
- min_introduced_date: Minimum date of introduction to Congress (YYYY-MM-DD)
- max_introduced_date: Maximum date of introduction to Congress (YYYY-MM-DD)
- min_updated_date: Minimum date of most recent status change (YYYY-MM-DD)
- max_updated_date: Maximum date of most recent status change (YYYY-MM-DD)

#### Returns:
- BillResponse object containing the bill data


#### Example:
```python
>>> lobbyview = LobbyView(LOBBYVIEW_TOKEN)
>>> output = lobbyview.bills(congress_number=111, bill_chamber="H", bill_number=4173)
>>> output.data[0]['bill_state']
'ENACTED:SIGNED'
```

### Method: clients

Gets client information from the LobbyView API based on the provided parameters.


#### Parameters:
- client_uuid: Unique identifier of the client
- client_name: Name of the client
- min_naics: Minimum NAICS code to which the client belongs
- max_naics: Maximum NAICS code to which the client belongs
- naics_description: Descriptions of the NAICS code

#### Returns:
- ClientResponse object containing the client data


#### Example:
```python
>>> lobbyview = LobbyView(LOBBYVIEW_TOKEN)
>>> output = lobbyview.clients(client_name="Microsoft Corporation")
>>> output.data[0]['client_uuid']
'44563806-56d2-5e99-84a1-95d22a7a69b3'
```

### Method: reports

Gets report information from the LobbyView API based on the provided parameters.


#### Parameters:
- report_uuid: Unique identifier of the report
- client_uuid: Unique identifier of the client
- registrant_uuid: Unique identifier of the registrant
- registrant_name: Name of the registrant
- report_year: Year of the report
- report_quarter_code: Quarter period of the report
- min_amount: Minimum lobbying firm income or lobbying expense (in-house)
- max_amount: Maximum lobbying firm income or lobbying expense (in-house)
- is_no_activity: Quarterly activity indicator
- is_client_self_filer: An organization employing its own in-house lobbyist(s)
- is_amendment: Amendment of previous report

#### Returns:
- ReportResponse object containing the report data


#### Example:
```python
>>> lobbyview = LobbyView(LOBBYVIEW_TOKEN)
>>> output = lobbyview.reports(report_year=2020, report_quarter_code="2", is_client_self_filer=True, report_uuid="4b799814-3e94-5ee1-8dd4-b32aead9aca6")
>>> output.data[0]['amount']
'$11,680,000.00'
```

### Method: issues

Gets issue information from the LobbyView API based on the provided parameters.


#### Parameters:
- report_uuid: Unique identifier of the report
- issue_ordi: An integer given to the issue
- issue_code: General Issue Area Code (Section 15)
- gov_entity: House(s) of Congress and Federal agencies (Section 17)

#### Returns:
- IssueResponse object containing the issue data


#### Example:
```python
>>> lobbyview = LobbyView(LOBBYVIEW_TOKEN)
>>> output = lobbyview.issues(issue_code="TRD")
```

### Method: networks

Gets network information from the LobbyView API based on the provided parameters.


#### Parameters:
- client_uuid: Unique identifier of the client
- legislator_id: Unique identifier of the legislator
- min_report_year: Minimum year of the report
- max_report_year: Maximum year of the report
- min_bills_sponsored: Minimum number of bills sponsored by the legislator in a specific year lobbied by the client
- max_bills_sponsored: Maximum number of bills sponsored by the legislator in a specific year lobbied by the client

#### Returns:
- NetworkResponse object containing the network data


#### Example:
```python
>>> lobbyview = LobbyView(LOBBYVIEW_TOKEN)
>>> output = lobbyview.networks(client_uuid="44563806-56d2-5e99-84a1-95d22a7a69b3", legislator_id="M000303")
>>> output.data[0]['report_year']
2017
```

### Method: texts

Gets issue text data from the LobbyView API based on the provided parameters.


#### Parameters:
- report_uuid: Unique identifier of the report
- issue_ordi: An integer given to the issue
- issue_code: General Issue Area Code (Section 15)
- issue_text: Specific lobbying issues (Section 16)

#### Returns:
- TextResponse object containing the text data


#### Example:
```python
>>> lobbyview = LobbyView(LOBBYVIEW_TOKEN)
>>> output = lobbyview.texts(issue_code="HCR", issue_text="covid")
```

### Method: quarter_level_networks

Gets quarter-level network information from the LobbyView API based on the provided parameters.


#### Parameters:
- client_uuid: Unique identifier of the client
- legislator_id: Unique identifier of the legislator
- report_year: Year of the report
- report_quarter_code: Quarter period of the report
- min_bills_sponsored: Minimum number of bills sponsored by the legislator in a specific quarter lobbied by the client
- max_bills_sponsored: Maximum number of bills sponsored by the legislator in a specific quarter lobbied by the client

#### Returns:
- QuarterLevelNetworkResponse object containing the quarter-level network data


#### Example:
```python
>>> lobbyview = LobbyView(LOBBYVIEW_TOKEN)
>>> output = lobbyview.quarter_level_networks(client_uuid="44563806-56d2-5e99-84a1-95d22a7a69b3", legislator_id="M000303", report_year=2017, report_quarter_code=4)
>>> output.data[0]['n_bills_sponsored']
1
```

### Method: bill_client_networks

Gets bill-client network information from the LobbyView API based on the provided parameters.


#### Parameters:
- congress_number: Session of Congress
- bill_chamber: Chamber of the legislative branch (Component of the bill_id composite key)
- bill_resolution_type: Bill type (Component of the bill_id composite key)
- bill_number: Bill number (Component of the bill_id composite key)
- report_uuid: Unique identifier of the report
- issue_ordi: An integer given to the issue
- client_uuid: Unique identifier of the client

#### Returns:
- BillClientNetworkResponse object containing the bill-client network data


#### Example:
```python
>>> lobbyview = LobbyView(LOBBYVIEW_TOKEN)
>>> output = lobbyview.bill_client_networks(congress_number=114, bill_chamber="H", bill_number=1174, client_uuid="44563806-56d2-5e99-84a1-95d22a7a69b3")
>>> output.data[0]['issue_ordi']
2
```

