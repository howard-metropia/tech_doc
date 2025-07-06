# OAuth 2.0 Account Authentication

## Overview
This module provides OAuth 2.0 authentication support for web2py applications, allowing users to authenticate using third-party OAuth 2.0 providers like Facebook, Google, GitHub, and others.

## Key Features
- **OAuth 2.0 Compliance**: Full RFC 6749 specification support
- **Token Management**: Automatic access token and refresh token handling
- **Extensible Design**: Base class for implementing provider-specific authentication
- **Session Integration**: Seamless integration with web2py session management
- **Error Handling**: Robust error handling for OAuth flows

## Core Class: OAuthAccount

### Constructor Parameters
- `client_id`: OAuth application client identifier
- `client_secret`: OAuth application secret key
- `auth_url`: Authorization endpoint URL
- `token_url`: Token endpoint URL
- `socket_timeout`: HTTP request timeout in seconds (default: 60)
- `**args`: Additional parameters passed to OAuth requests (e.g., scope)

### Key Methods

#### `accessToken()`
Manages OAuth access tokens with automatic refresh capability:
- Returns current valid access token
- Automatically refreshes expired tokens using refresh_token
- Handles token expiration and renewal

#### `get_user()`
**Abstract method** - Must be overridden in subclasses to return user information:
```python
def get_user(self):
    # Return user dict with required fields
    return dict(
        first_name='John',
        last_name='Doe', 
        username='johndoe'
    )
```

#### `login_url(next="/")`
Initiates OAuth authentication flow by redirecting to provider's authorization URL.

#### `logout_url(next="/")`
Clears OAuth session token and returns logout redirect URL.

## Implementation Example

### Facebook OAuth Implementation
```python
from gluon.contrib.login_methods.oauth20_account import OAuthAccount
from facebook import GraphAPI, GraphAPIError

class FacebookAccount(OAuthAccount):
    AUTH_URL = "https://graph.facebook.com/oauth/authorize"
    TOKEN_URL = "https://graph.facebook.com/oauth/access_token"
    
    def __init__(self):
        OAuthAccount.__init__(self,
            client_id=CLIENT_ID,
            client_secret=CLIENT_SECRET,
            auth_url=self.AUTH_URL,
            token_url=self.TOKEN_URL,
            scope='user_photos,friends_photos'
        )
        self.graph = None
    
    def get_user(self):
        if not self.accessToken():
            return None
            
        if not self.graph:
            self.graph = GraphAPI(self.accessToken())
        
        try:
            user = self.graph.get_object("me")
            return dict(
                first_name=user['first_name'],
                last_name=user['last_name'],
                username=user['id']
            )
        except GraphAPIError:
            self.session.token = None
            self.graph = None
            return None
```

### Integration with web2py Auth
```python
# In model (e.g., db.py)
# Define custom auth table
auth_table = db.define_table(
    auth.settings.table_user_name,
    Field('first_name', length=128, default=""),
    Field('last_name', length=128, default=""),
    Field('username', length=128, default="", unique=True),
    Field('password', 'password', length=256, readable=False),
    Field('registration_key', length=128, default="", 
          writable=False, readable=False)
)

auth_table.username.requires = IS_NOT_IN_DB(db, auth_table.username)
auth.define_tables()

# Configure OAuth authentication
auth.settings.actions_disabled = [
    'register', 'change_password', 
    'request_reset_password', 'profile'
]
auth.settings.login_form = FacebookAccount()
```

## OAuth 2.0 Flow

### 1. Authorization Request
When user attempts to login:
- Redirects to OAuth provider's authorization URL
- Includes client_id, redirect_uri, scope, and response_type parameters

### 2. Authorization Response
Provider redirects back with:
- Authorization code (success)
- Error information (failure)

### 3. Token Exchange
- Exchanges authorization code for access token
- Receives access_token, refresh_token, and expires_in
- Stores tokens in web2py session

### 4. Token Refresh
- Automatically refreshes expired tokens
- Uses refresh_token for seamless renewal
- Updates session with new token information

## Token Management

### Session Storage
Tokens are stored in `current.session.token` with structure:
```python
{
    'access_token': 'oauth_access_token',
    'refresh_token': 'oauth_refresh_token', 
    'expires': absolute_expiration_time,
    'expires_in': seconds_until_expiration
}
```

### Automatic Refresh
- Checks token expiration before each use
- Automatically refreshes using refresh_token when needed
- Handles both 'expires' and 'expires_in' response formats

## Security Features

### HTTP Basic Authentication
For token endpoint requests:
- Uses client_id and client_secret for HTTP Basic Auth
- Secure credential transmission to token endpoint

### SSL/HTTPS Support
- Automatic HTTPS detection from environment
- Secure redirect URI generation
- Encrypted token transmission

## Error Handling

### OAuth Errors
- Handles HTTP errors from OAuth endpoints
- Parses error responses from providers
- Graceful fallback for authentication failures

### Token Parsing
- Supports both JSON and URL-encoded responses
- Handles different provider response formats
- Robust parsing with error recovery

## Response Format Support

### JSON Responses
Primary format for modern OAuth providers:
```json
{
    "access_token": "token_value",
    "token_type": "Bearer",
    "expires_in": 3600,
    "refresh_token": "refresh_value"
}
```

### URL-Encoded Responses
Legacy format support:
```
access_token=token_value&expires_in=3600&token_type=Bearer
```

## Best Practices

### Security
- Store client_secret securely
- Use HTTPS for all OAuth endpoints
- Implement proper scope restrictions
- Validate redirect URIs

### Performance
- Cache user information appropriately
- Minimize API calls to OAuth provider
- Handle rate limiting gracefully

### Error Handling
- Provide user-friendly error messages
- Log OAuth errors for debugging
- Implement retry logic for transient failures

This OAuth 2.0 implementation provides a solid foundation for integrating third-party authentication into web2py applications while maintaining security and performance best practices.