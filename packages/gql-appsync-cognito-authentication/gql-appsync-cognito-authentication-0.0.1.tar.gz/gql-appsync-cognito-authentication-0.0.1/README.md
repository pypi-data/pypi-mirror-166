# gql-appsync-cognito-authorization

An `AppSyncAuthentication` implementation for `gql.transport.aiohttp.AIOHTTPTransport` using [`pycognito`](https://github.com/pvizeli/pycognito)

## Installation
```bash
pip install gql-appsync-cognito-authentication
```

## Usage
```python
from gql import Client
from gql.transport.aiohttp import AIOHTTPTransport
from gql_appsync_cognito_authentication import AppSyncCognitoAuthentication
from pycognito import Cognito

cognito = Cognito(...)

client = Client(
    transport=AIOHTTPTransport(
        auth=AppSyncCognitoAuthentication(cognito),
        ...
    ),
    ...
)
```
