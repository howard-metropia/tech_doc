# gluon/contrib/login_methods/rpx_account.py

## Overview

The rpx_account.py module provides Janrain Engage (formerly RPX) authentication integration for Web2py applications. RPX was Janrain's social login service that aggregated multiple identity providers into a single authentication solution.

## Key Features

- **Social login aggregation**: Multiple providers through single integration
- **Identity management**: Centralized user profile management
- **Provider abstraction**: Unified API across different social networks
- **Legacy support**: Support for older Janrain implementations

## Configuration

```python
from gluon.contrib.login_methods.rpx_account import rpx_auth

auth.settings.login_methods.append(
    rpx_auth(
        domain='yourapp.rpxnow.com',
        api_key='your_rpx_api_key'
    )
)
```

## Service Evolution

RPX has been evolved into Janrain's Identity Cloud platform. New implementations should consider using the newer Janrain services or direct OAuth 2.0 integrations.

## Migration Path

- Transition to direct OAuth 2.0 implementations
- Upgrade to Janrain Identity Cloud
- Consider alternative social login aggregators