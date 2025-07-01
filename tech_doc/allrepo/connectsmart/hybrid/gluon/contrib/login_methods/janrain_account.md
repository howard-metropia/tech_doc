# gluon/contrib/login_methods/janrain_account.py

## Overview

The janrain_account.py module provides Janrain (Akamai Identity Cloud) authentication integration for Web2py applications. Janrain offers comprehensive identity and access management solutions with support for multiple social and enterprise authentication providers.

## Key Features

- **Multi-provider support**: Facebook, Google, Twitter, LinkedIn, and more
- **Enterprise integration**: SAML, LDAP, and custom providers
- **User profile management**: Comprehensive user data handling
- **Analytics and insights**: User behavior tracking

## Configuration

```python
from gluon.contrib.login_methods.janrain_account import janrain_auth

auth.settings.login_methods.append(
    janrain_auth(
        domain='yourapp.rpxnow.com',
        api_key='your_janrain_api_key'
    )
)
```

## Service Integration

- Centralized identity management
- Social login aggregation
- Enterprise directory integration
- Custom authentication workflows