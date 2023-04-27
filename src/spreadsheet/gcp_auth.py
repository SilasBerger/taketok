import os

from google.auth.exceptions import RefreshError
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

from src.util.path_utils import gcp_token_file, gcp_credentials_file

_SCOPES = 'https://www.googleapis.com/auth/spreadsheets'


class GcpAuthHandler:

    def __init__(self, config_name: str) -> None:
        self._token_file = gcp_token_file(config_name)
        self._credentials_file = gcp_credentials_file(config_name)
        self._cached_token = None

    @staticmethod
    def is_invalid(token):
        return not (token and token.valid)

    def _is_cache_invalid(self):
        return GcpAuthHandler.is_invalid(self._cached_token)

    def _try_from_token_file(self):
        if os.path.exists(self._token_file):
            return Credentials.from_authorized_user_file(self._token_file, _SCOPES)

    def _refresh_or_authenticate(self, token):
        if token and token.expired and token.refresh_token:
            try:
                new_token = token.refresh(Request())
            except RefreshError:
                new_token = self._perform_auth_flow()
        else:
            new_token = self._perform_auth_flow()
        self._export_token_file(new_token)
        return new_token

    def _perform_auth_flow(self):
        flow = InstalledAppFlow.from_client_secrets_file(self._credentials_file, _SCOPES)
        return flow.run_local_server(port=0)

    def _export_token_file(self, token):
        with open(self._token_file, 'w') as fp:
            fp.write(token.to_json())

    def _update_cached_token(self):
        token = self._try_from_token_file()
        if GcpAuthHandler.is_invalid(token):
            token = self._refresh_or_authenticate(token)
        self._cached_token = token

    def load_credentials(self):
        if self._is_cache_invalid():
            self._update_cached_token()
        return self._cached_token
