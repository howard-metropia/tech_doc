# gluon/contrib/login_methods/oauth10a_account.py

## Overview

The oauth10a_account.py module provides OAuth 1.0a authentication integration for Web2py applications. OAuth 1.0a is the revised version of the original OAuth specification, providing secure authentication for legacy providers that haven't migrated to OAuth 2.0.

## Key Features

- **OAuth 1.0a protocol**: Support for legacy OAuth providers
- **Signature-based security**: Cryptographic request signing
- **Twitter integration**: Primary use case for Twitter API
- **Request token flow**: Three-legged authentication process

## Configuration

```python
from gluon.contrib.login_methods.oauth10a_account import oauth10a_auth

auth.settings.login_methods.append(
    oauth10a_auth(
        consumer_key='your_consumer_key',
        consumer_secret='your_consumer_secret',
        request_token_url='https://api.provider.com/oauth/request_token',
        access_token_url='https://api.provider.com/oauth/access_token',
        authorize_url='https://api.provider.com/oauth/authorize'
    )
)
```

## OAuth 1.0a Flow

1. Request token acquisition
2. User authorization redirect
3. Access token exchange
4. API access with signed requests