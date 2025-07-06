# gluon/contrib/login_methods/linkedin_account.py

## Overview

The linkedin_account.py module provides LinkedIn OAuth authentication integration for Web2py applications. This enables users to authenticate using their LinkedIn professional profiles, ideal for business and professional applications.

## Key Features

- **LinkedIn OAuth 2.0**: Professional network authentication
- **Profile access**: Basic profile information retrieval
- **Professional data**: Job titles, company information, connections
- **Business integration**: Ideal for B2B applications

## Configuration

```python
from gluon.contrib.login_methods.linkedin_account import linkedin_auth

auth.settings.login_methods.append(
    linkedin_auth(
        client_id='your_linkedin_client_id',
        client_secret='your_linkedin_client_secret'
    )
)
```

## Profile Data

- Professional headline
- Current position and company
- Education information
- Professional connections (with permissions)