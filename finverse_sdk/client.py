import requests
import uuid
import urllib.parse
from .auth import FinverseAuthenticator
from .exceptions import (
    FinverseAPIError,
    FinverseRateLimitExceeded,
    FinverseInvalidRequest,
    FinverseAuthError,
    FinverseSDKError
)

class FinverseClient:
    def __init__(self, client_id, client_secret, customer_app_id, redirect_uri=None, base_url="https://api.sandbox.finverse.net"):
        self.base_url = base_url
        self.redirect_uri = redirect_uri
        self.authenticator = FinverseAuthenticator(client_id, client_secret, customer_app_id, base_url)

    def _request(self, method, endpoint, params=None, json_data=None, form_data=None, authenticated=True, content_type="application/json"):
        """
        Helper method to make API requests with flexible content types and authentication.
        
        Args:
            method: HTTP method (GET, POST, PUT, DELETE)
            endpoint: API endpoint path
            params: URL parameters for GET requests
            json_data: Data to send as JSON
            form_data: Data to send as form-encoded
            authenticated: Whether to include auth headers
            content_type: Content-Type header value
        """
        url = f"{self.base_url}{endpoint}"
        
        headers = {"Content-Type": content_type}
        if authenticated:
            headers.update(self.authenticator.get_auth_headers())
        
        headers["X-Request-Id"] = str(uuid.uuid4().int)[:10]

        try:
            request_kwargs = {"headers": headers}
            
            if method == "GET":
                request_kwargs["params"] = params
            elif form_data is not None:
                request_kwargs["data"] = urllib.parse.urlencode(form_data)
            elif json_data is not None:
                request_kwargs["json"] = json_data

            # Make the request
            response = requests.request(method, url, **request_kwargs)
            response.raise_for_status()
            
            return response.json()

        except requests.exceptions.HTTPError as e:
            self._handle_http_error(e)
        except requests.exceptions.RequestException as e:
            raise FinverseSDKError(f"Network or connection error: {e}")
        except ValueError:
            raise FinverseAPIError("Failed to decode JSON response from API.")
        except Exception as e:
            raise FinverseSDKError(f"An unexpected error occurred: {e}")

    def _handle_http_error(self, e):
        """Centralized HTTP error handling."""
        status_code = e.response.status_code
        response_data = None
        
        try:
            response_data = e.response.json()
        except ValueError:
            pass

        error_message = response_data.get("message", e.response.text) if response_data else e.response.text

        if status_code == 401:
            raise FinverseAuthError(f"Authentication failed: {error_message}")
        elif status_code == 429:
            raise FinverseRateLimitExceeded(f"Rate limit exceeded: {error_message}", status_code, response_data)
        elif status_code == 400:
            raise FinverseInvalidRequest(f"Invalid request: {error_message}", status_code, response_data)
        else:
            raise FinverseAPIError(f"API error ({status_code}): {error_message}", status_code, response_data)

    def generate_link_token(self, user_id, state, country_codes=None):
        """
        Generates a link token and URL for the Finverse Link UI.
        This is the first step to allow a user to link their bank account.
        """
        if not self.redirect_uri:
            raise ValueError("redirect_uri must be provided for Data API linking.")

        if country_codes is None:
            country_codes = []

        endpoint = "/link/token"
        json_data = {
            "client_id": self.authenticator.client_id,
            "user_id": user_id,
            "redirect_uri": self.redirect_uri,
            "state": state,
            "response_mode": "form_post",
            "response_type": "code",
            "grant_type": "client_credentials",
            "countries": country_codes,
            "link_mode": "real test",
            #"user_type": "INDIVIDUAL",
            "ui_mode": "auto_redirect",
            "institution_status": "beta supported"
        }
        response = self._request("POST", endpoint, json_data=json_data)
        return response

    def exchange_authorization_code(self, code):
        """
        Exchanges an authorization code for login_identity_token and login_identity_id.
        Uses form-encoded data as required by the OAuth2 specification.
        """
        if not self.redirect_uri:
            raise ValueError("redirect_uri must be provided for authorization code exchange.")

        endpoint = "/auth/token"
        form_data = {
            "client_id": self.authenticator.client_id,
            "code": code,
            "grant_type": "authorization_code",
            "redirect_uri": self.redirect_uri
        }
        
        response = self._request(
            "POST", 
            endpoint, 
            form_data=form_data, 
            content_type="application/x-www-form-urlencoded"
        )
        
        if 'access_token' in response:
            self.authenticator.set_user_access_token(response['access_token'])
        return response

    def get_accounts(self):
        """
        Retrieves accounts for a linked institution using its specific access_token.
        """
        endpoint = "/accounts"
        response = self._request("GET", endpoint)
        return response

    def get_transactions(self, account_ids=None, start_date=None, end_date=None):
        """
        Retrieves transactions for a linked institution.
        
        Args:
            account_ids: Optional list of account IDs to filter by
            start_date: Optional start date in YYYY-MM-DD format
            end_date: Optional end date in YYYY-MM-DD format
        """
        endpoint = "/transactions"
        

        response = self._request("GET", endpoint)
        return response

    def get_identity(self):
        """
        Retrieves identity information for a linked institution.
        """
        endpoint = "/identity"
        response = self._request("GET", endpoint)
        return response

    def get_statements(self, account_ids=None, start_date=None, end_date=None):
        """
        Retrieves statements for a linked institution.
        """
        endpoint = "/statements"

        response = self._request("GET", endpoint)
        return response
    
    def get_composite_statements(self, account_ids=None, start_date=None, end_date=None):
        """
        Retrieves statements for a linked institution.
        """
        endpoint = "/composite_statement"

        response = self._request("GET", endpoint)
        return response
    
    def get_card_detals(self, account_ids=None, start_date=None, end_date=None):
        """
        Retrieves statements for a linked institution.
        """
        endpoint = "/card_details"

        response = self._request("GET", endpoint)
        return response

    def get_customer_token(self):
        """Get the current customer token (mainly for debugging/testing purposes)."""
        return self.authenticator.get_customer_token()
