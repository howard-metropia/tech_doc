# gluon/contrib/login_methods/email_auth.py

## Overview

The email_auth.py module provides email-based authentication for Web2py applications. This method sends authentication links via email, allowing users to log in without traditional passwords through email verification.

## Key Features

- **Passwordless authentication**: Users receive login links via email
- **Email verification**: Ensures email ownership
- **Time-limited tokens**: Security through token expiration
- **Simple integration**: Easy setup with existing Web2py Auth

## Usage

```python
from gluon.contrib.login_methods.email_auth import email_auth

auth.settings.login_methods.append(email_auth())
```

## Security Features

- Token-based authentication
- Time-limited login links
- Email address verification
- Protection against replay attacks