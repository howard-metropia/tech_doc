# gluon/contrib/login_methods/loginza.py

## Overview

The loginza.py module provides Loginza authentication service integration for Web2py applications. Loginza is a Russian social authentication service that aggregates multiple social networks popular in Russia and Eastern Europe.

## Key Features

- **Russian social networks**: VKontakte, Odnoklassniki, Mail.ru
- **International providers**: Facebook, Google, Twitter, LinkedIn
- **Localized interface**: Russian language support
- **Regional optimization**: Optimized for Eastern European users

## Configuration

```python
from gluon.contrib.login_methods.loginza import loginza_auth

auth.settings.login_methods.append(
    loginza_auth(
        site_id='your_loginza_site_id'
    )
)
```

## Regional Focus

- CIS countries social networks
- Localized authentication flows
- Regional compliance requirements
- Culturally appropriate user experience