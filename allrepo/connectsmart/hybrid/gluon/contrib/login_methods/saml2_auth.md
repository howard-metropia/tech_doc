# gluon/contrib/login_methods/saml2_auth.py

## Overview

The saml2_auth.py module provides SAML 2.0 authentication integration for Web2py applications. SAML (Security Assertion Markup Language) is an XML-based standard for exchanging authentication and authorization data between parties, commonly used in enterprise single sign-on (SSO) scenarios.

## Key Features

- **Enterprise SSO**: Integration with enterprise identity providers
- **SAML 2.0 protocol**: Industry-standard authentication
- **XML assertions**: Secure, signed authentication assertions
- **Federation support**: Cross-domain authentication capabilities

## Configuration

```python
from gluon.contrib.login_methods.saml2_auth import saml2_auth

auth.settings.login_methods.append(
    saml2_auth(
        idp_url='https://idp.company.com/saml2/sso',
        sp_entity_id='https://yourapp.com/saml2/metadata',
        x509_cert='/path/to/certificate.pem'
    )
)
```

## SAML Components

- **Identity Provider (IdP)**: Authentication authority
- **Service Provider (SP)**: Your Web2py application
- **Assertions**: Signed authentication statements
- **Metadata**: Configuration exchange format

## Enterprise Integration

- Active Directory Federation Services (ADFS)
- Okta, OneLogin, Auth0 enterprise plans
- University identity systems
- Government authentication frameworks