# finverse_sdk/auth.py

import requests
import time
import uuid
from .exceptions import FinverseAuthError

class FinverseAuthenticator:
    def __init__(self, client_id, client_secret, customer_app_id, base_url="https://api.sandbox.finverse.net"):
        self.client_id = client_id
        self.client_secret = client_secret
        self.customer_app_id = customer_app_id
        self.base_url = base_url
        self._customer_token = None
        self._token_expiry_time = 0
        self._user_access_token = None

    def _is_token_expired(self):
        """Checks if the current customer_token is expired or close to expiring."""
        # Refresh if less than 5 minutes remaining
        return time.time() >= (self._token_expiry_time - 300)

    def get_customer_token(self):
        """Get a cached customer token, refreshing if necessary."""
        if not self._customer_token or self._is_token_expired():
            self._refresh_customer_token()
        return self._customer_token

    def set_user_access_token(self, access_token):
        """Set the user access token after authorization code exchange."""
        self._user_access_token = access_token

    def _refresh_customer_token(self):
        """Refresh the customer token by making an API call."""
        url = f"{self.base_url}/auth/customer/token"
        headers = {
            "Content-Type": "application/json",
            "X-Customer-App-ID": self.customer_app_id,
            "X-Request-Id": str(uuid.uuid4().int)[:10]
        }
        data = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "grant_type": "client_credentials"
        }

        try:
            response = requests.post(url, headers=headers, json=data)
            response.raise_for_status()
            token_data = response.json()
            
            self._customer_token = token_data.get("access_token")
            if not self._customer_token:
                raise FinverseAuthError("Failed to obtain access_token from Finverse API.")
            
            # Set token expiry time
            expires_in = token_data.get("expires_in", 3600)
            self._token_expiry_time = time.time() + expires_in

        except requests.exceptions.HTTPError as e:
            status_code = e.response.status_code
            try:
                error_details = e.response.json()
                error_message = error_details.get("message", e.response.text)
            except ValueError:
                error_message = e.response.text
            
            if status_code == 401:
                raise FinverseAuthError(f"Customer authentication failed: {error_message}")
            else:
                raise FinverseAuthError(f"API error ({status_code}): {error_message}")
                
        except requests.exceptions.RequestException as e:
            raise FinverseAuthError(f"Network or connection error: {e}")
        except ValueError:
            raise FinverseAuthError("Failed to decode JSON response during token refresh.")
        except Exception as e:
            raise FinverseAuthError(f"An unexpected error occurred during token refresh: {e}")

    def get_auth_headers(self):
        """Returns the authorization headers for authenticated API calls."""

        if self._user_access_token:
            bearer_token = self._user_access_token
        else:
            bearer_token = self.get_customer_token()
            
        return {
            "Authorization": f"Bearer {bearer_token}",
            "X-Customer-App-ID": self.customer_app_id,
        }
