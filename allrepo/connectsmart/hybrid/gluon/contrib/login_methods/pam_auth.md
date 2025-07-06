# gluon/contrib/login_methods/pam_auth.py

## Overview

The pam_auth.py module provides PAM (Pluggable Authentication Modules) integration for Web2py applications. PAM allows authentication against system-level authentication mechanisms on Unix-like systems.

## Key Features

- **System integration**: Authenticate against system accounts
- **PAM module support**: Leverage existing PAM configurations
- **Unix/Linux compatibility**: Native system authentication
- **Flexible backends**: Support for various PAM modules

## Configuration

```python
from gluon.contrib.login_methods.pam_auth import pam_auth

auth.settings.login_methods.append(
    pam_auth(service='web2py')
)
```

## PAM Service Configuration

Create `/etc/pam.d/web2py`:
```
auth    required    pam_unix.so
account required    pam_unix.so
```

## Use Cases

- Server applications requiring system account access
- Integration with existing Unix user management
- Corporate environments with centralized user accounts