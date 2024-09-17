Troubleshooting
===============

This page provides information on how to troubleshoot common issues and errors when using the LobbyView Python Package.

Exception Classes
-----------------

The LobbyView package defines several custom exception classes in the `exceptions.py` file to handle specific error scenarios. Understanding these exceptions can help you identify and resolve issues more effectively.

- `LobbyViewError`: Base class for all LobbyView API errors.
- `UnauthorizedError`: Raised when the API token is invalid or unauthorized.
- `TooManyRequestsError`: Raised when the API rate limit is exceeded.
- `PartialContentError`: Raised when the API returns a partial response.
- `UnexpectedStatusCodeError`: Raised when the API returns an unexpected status code.
- `InvalidPageNumberError`: Raised when the current page number is greater than the total number of pages.
- `RequestError`: Raised when an error occurs during the request to the LobbyView API.

Common Issues and Solutions
---------------------------

1. **UnauthorizedError**:

- Ensure that you have a valid API token and that it is correctly set in your code or environment variables.
- Double-check that you have the necessary permissions to access the requested endpoints.
- Verify that your API token has not expired or been revoked.

2. **TooManyRequestsError**:

- Default users are limited to 100 requests per day. If you exceed this limit, you will receive a `TooManyRequestsError`.
- To resolve this issue, wait for the specified time period (usually 24 hours) before making more requests.
- If you require a higher request limit, reach out to us at lobbydata@gmail.com for more information.

3. **PartialContentError**:

- This error occurs when the API returns a partial response due to server-side issues or timeouts.
- Retry the request after a short delay to see if the issue resolves itself.
- If the problem persists, refer to the "Getting Help" section at the bottom of this page.

4. **UnexpectedStatusCodeError**:

- This error is raised when the API returns an unexpected status code that is not handled by the package.
- Check the API documentation to ensure that you are using the correct endpoints and parameters.
- If the issue persists, it may indicate a problem with the LobbyView API itself, refer to the "Getting Help" section at the bottom of this page.

5. **InvalidPageNumberError**:

- This error occurs when the requested page number is greater than the total number of available pages.
- Ensure that you are providing valid page numbers within the range of available pages.
- You can check the `total_pages` attribute of the response object to determine the maximum page number.

6. **RequestError**:

- This error is raised when an unspecified error occurs during the request to the LobbyView API.
- Check your network connection and ensure that you can reach the LobbyView API endpoints.
- Retry the request after a short delay to see if the issue resolves itself.
- If the problem persists, refer to the "Getting Help" section at the bottom of this page.

Getting Help
------------

If you encounter any issues or have questions that are not covered in this troubleshooting guide, please open an issue on the LobbyView Python Package GitHub repository: https://github.com/lobbyview/LobbyViewPythonPackage. When opening an issue, provide as much detail as possible, including:

- The version of the LobbyView package you are using.
- The specific error message or exception you encountered.
- A minimal code example that reproduces the issue.
- Any relevant configuration or environment details.

Our team will be happy to assist you and provide further guidance on resolving the issue.