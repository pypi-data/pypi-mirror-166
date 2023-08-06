from typing import Any, Optional

from gql.transport.appsync_auth import AppSyncAuthentication
from pycognito import Cognito


class AppSyncCognitoAuthentication(AppSyncAuthentication):
    def __init__(self, cognito: Cognito) -> None:
        self.cognito = cognito

    def get_headers(
        self, data: Optional[str] = None, headers: Optional[dict[str, Any]] = None
    ) -> dict[str, Any]:
        # Ensure that the access token is still good
        self.cognito.check_token()
        return dict(Authorization=self.cognito.access_token)
