# gluon/contrib/login_methods/openid_auth.py

## Overview

The openid_auth.py module provides OpenID authentication integration for Web2py applications. OpenID is a decentralized authentication protocol that allows users to log in using their existing accounts from OpenID providers.

## Key Features

- **Decentralized authentication**: No central authority required
- **Provider flexibility**: Users choose their OpenID provider
- **URL-based identity**: User identity represented as URL
- **Legacy support**: Support for older authentication systems

## Configuration

```python
from gluon.contrib.login_methods.openid_auth import openid_auth

auth.settings.login_methods.append(
    openid_auth()
)
```

## OpenID Flow

1. User enters OpenID identifier
2. Discovery of OpenID provider
3. Authentication at provider
4. Assertion verification
5. User login to Web2py application

## Status Note

OpenID 2.0 has been largely superseded by OAuth 2.0 and OpenID Connect. This module is primarily for legacy system support.