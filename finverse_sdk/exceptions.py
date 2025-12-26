class FinverseSDKError(Exception):
    """Base exception for Finverse SDK errors."""
    pass

class FinverseAuthError(FinverseSDKError):
    """Exception for authentication errors."""
    pass

class FinverseAPIError(FinverseSDKError):
    """Exception for Finverse API errors with status code and message."""
    def __init__(self, message, status_code=None, response_data=None):
        super().__init__(message)
        self.status_code = status_code
        self.response_data = response_data

class FinverseRateLimitExceeded(FinverseAPIError):
    """Exception for rate limit exceeded errors."""
    pass

class FinverseInvalidRequest(FinverseAPIError):
    """Exception for invalid request errors."""
    pass