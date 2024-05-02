"""
(Sub)classes of LobbyViewError that represent different types of errors.
"""

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
    def __init__(self, status_code=None):
        super().__init__()
        self.status_code = status_code
    def __str__(self):
        if self.status_code is not None:
            return f"Unauthorized, status code: {self.status_code}. Please check your API token and permissions."
        return "Unauthorized. Please check your API token and permissions."

class TooManyRequestsError(LobbyViewError):
    """
    Raised when the API rate limit is exceeded.
    """
    def __init__(self, status_code):
        super().__init__()
        self.status_code = status_code
    def __str__(self):
        return f"Rate limit exceeded, status code: {self.status_code}"

class PartialContentError(LobbyViewError):
    """
    Raised when the API returns a partial response.
    """
    def __init__(self, status_code):
        super().__init__()
        self.status_code = status_code
    def __str__(self):
        return f"Partial content returned, status code: {self.status_code}"

class UnexpectedStatusCodeError(LobbyViewError):
    """
    Raised when the API returns an unexpected status code.
    """
    def __init__(self, status_code):
        super().__init__()
        self.status_code = status_code
    def __str__(self):
        return f"Unexpected status code: {self.status_code}"

class InvalidPageNumberError(LobbyViewError):
    """
    Raised when the current page number is greater than the total number of pages.
    """
    def __init__(self, current_page, total_pages):
        super().__init__()
        self.current_page = current_page
        self.total_pages = total_pages
    def __str__(self):
        return f"Invalid page number: {self.current_page}, total pages: {self.total_pages}"

class RequestError(LobbyViewError):
    """
    Raised when an error occurs during the request to the LobbyView API.
    """
    def __init__(self):
        super().__init__()
