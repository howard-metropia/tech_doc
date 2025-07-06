# gluon/contrib/login_methods/freeipa_auth.py

## Overview

The freeipa_auth.py module provides FreeIPA authentication integration for Web2py applications. FreeIPA is an integrated security information management solution that provides centralized authentication, authorization, and account information.

## Key Features

- **FreeIPA integration**: Direct authentication against FreeIPA servers
- **Kerberos support**: Integration with Kerberos authentication
- **LDAP backend**: Leverages LDAP for user information
- **Group management**: Automatic group and role synchronization

## Configuration

```python
from gluon.contrib.login_methods.freeipa_auth import freeipa_auth

auth.settings.login_methods.append(
    freeipa_auth(
        server='ipa.company.com',
        domain='company.com'
    )
)
```

## Enterprise Features

- Single sign-on integration
- Certificate-based authentication
- Role-based access control
- Audit logging capabilities