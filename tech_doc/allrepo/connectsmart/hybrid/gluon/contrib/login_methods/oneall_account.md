# gluon/contrib/login_methods/oneall_account.py

## Overview

The oneall_account.py module provides OneAll social login service integration for Web2py applications. OneAll is a social login platform that aggregates 40+ social networks into a single, standardized API.

## Key Features

- **40+ social networks**: Comprehensive provider support
- **Unified API**: Single integration for multiple providers
- **Real-time synchronization**: Automatic profile updates
- **Global coverage**: Worldwide social network support

## Configuration

```python
from gluon.contrib.login_methods.oneall_account import oneall_auth

auth.settings.login_methods.append(
    oneall_auth(
        subdomain='your_oneall_subdomain',
        public_key='your_public_key',
        private_key='your_private_key'
    )
)
```

## Supported Networks

- Facebook, Google, Twitter, LinkedIn
- Regional networks (VKontakte, Weibo, etc.)
- Professional networks
- Gaming and entertainment platforms