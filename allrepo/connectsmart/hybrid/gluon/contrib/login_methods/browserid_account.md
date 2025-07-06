# gluon/contrib/login_methods/browserid_account.py

## Overview

The browserid_account.py module provides Mozilla BrowserID/Persona authentication integration for Web2py applications. BrowserID was Mozilla's decentralized identity system that allowed users to authenticate using their email addresses without requiring passwords to be shared with individual websites.

## Key Components

### BrowserID Authentication
- **Email-based authentication**: Users authenticate with their email address
- **Decentralized identity**: No central authority required
- **JavaScript integration**: Client-side verification process
- **Privacy-focused**: Minimal data sharing between sites

### Main Function: browserid_auth()
Returns an authentication method that validates BrowserID assertions against Mozilla's verification service.

## Implementation Features

### Assertion Verification
- Validates BrowserID assertions from client
- Communicates with Mozilla's verification API
- Extracts user email from verified assertion
- Handles authentication success/failure states

### Security Features
- **Assertion validation**: Cryptographic verification of identity assertions
- **Audience verification**: Ensures assertions are for correct domain
- **Expiration checking**: Validates assertion timestamps
- **HTTPS enforcement**: Requires secure connections

## Usage Pattern

```python
from gluon.contrib.login_methods.browserid_account import browserid_auth

# Add BrowserID authentication
auth.settings.login_methods.append(browserid_auth())
```

## Integration Requirements

### Client-Side Setup
- Include BrowserID JavaScript library
- Implement login/logout buttons
- Handle assertion generation
- Submit assertions to Web2py

### Server Configuration
- Configure Web2py controller to handle assertions
- Set up proper redirect URLs
- Implement user registration for new BrowserID users

## Status and Deprecation

### Historical Context
Mozilla discontinued Persona/BrowserID service in November 2016, making this module primarily of historical interest.

### Migration Path
Applications using BrowserID should migrate to:
- WebAuthn for passwordless authentication
- OAuth 2.0 with email providers
- Modern authentication standards

## Best Practices

### Legacy Support
- Graceful degradation when BrowserID unavailable
- Clear migration notices for existing users
- Alternative authentication method provision

### Security Considerations
- Verify all assertions server-side
- Implement proper error handling
- Use HTTPS for all authentication flows