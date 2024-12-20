# sdk/exceptions.py

class APIError(Exception):
    """Base class for API exceptions."""
    pass

class BadRequestError(APIError):
    """Exception for 400 Bad Request errors."""
    pass

class UnauthorizedError(APIError):
    """Exception for 401 Unauthorized errors."""
    pass

class ForbiddenError(APIError):
    """Exception for 403 Forbidden errors."""
    pass

class NotFoundError(APIError):
    """Exception for 404 Not Found errors."""
    pass

class UnprocessableContentError(APIError):
    """Exception for 422 Unprocessable Content errors."""
    pass

class TooManyRequestsError(APIError):
    """Exception for 429 Too Many Requests errors."""
    pass

class ServerError(APIError):
    """Exception for 5xx Server errors."""
    pass

