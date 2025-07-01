# gluon/contrib/login_methods/oauth20_account.py

## Overview

The oauth20_account.py module provides OAuth 2.0 authentication integration for Web2py applications. It implements the OAuth 2.0 authorization framework (RFC 6749) allowing users to authenticate using third-party providers like Facebook, Google, Twitter, and other OAuth 2.0-compliant services.

## Key Components

### Main Class: OAuthAccount
```python
class OAuthAccount(object):
    """
    OAuth 2.0 authentication handler for Web2py
    
    Provides framework for implementing OAuth 2.0 authentication
    flows with various providers while maintaining security best
    practices and proper token management.
    """
```

### Core Dependencies
```python
import time
import cgi
import json
from gluon._compat import urllib2, urlencode
from gluon import current, redirect, HTTP
```

## OAuth 2.0 Flow Implementation

### Authorization Code Flow
The module implements the standard OAuth 2.0 authorization code flow:

1. **Authorization Request**: Redirect user to provider's authorization server
2. **Authorization Grant**: Provider redirects back with authorization code
3. **Access Token Request**: Exchange authorization code for access token
4. **Resource Access**: Use access token to access protected resources
5. **User Registration**: Create/update user account in Web2py

### Flow Diagram
```
User -> Web2py -> OAuth Provider -> Web2py -> User Account Creation
  |        |           |             |              |
  |        |           |             |              |
  1        2           3             4              5
```

## Base OAuthAccount Class

### Initialization
```python
def __init__(self, g, client_id, client_secret, auth_url, token_url,
             callback_url=None, scope='email', state=None, 
             csrf_prevention=True, detection_cookie_name=None):
    """
    Initialize OAuth account handler
    
    Args:
        g: Gluon global object
        client_id: OAuth application client ID
        client_secret: OAuth application client secret
        auth_url: Provider authorization endpoint
        token_url: Provider token endpoint
        callback_url: Application callback URL
        scope: Requested OAuth scopes
        state: CSRF protection state parameter
        csrf_prevention: Enable CSRF protection
    """
```

### Configuration Properties
```python
self.client_id = client_id
self.client_secret = client_secret  
self.auth_url = auth_url
self.token_url = token_url
self.callback_url = callback_url or self.get_callback_url()
self.scope = scope
self.state = state or self.generate_state()
```

## Authentication Flow Methods

### Authorization URL Generation
```python
def get_authorization_url(self):
    """
    Generate OAuth authorization URL
    
    Returns:
        str: Authorization URL with proper parameters
    """
    params = {
        'client_id': self.client_id,
        'redirect_uri': self.callback_url,
        'scope': self.scope,
        'response_type': 'code',
        'state': self.state
    }
    
    return f"{self.auth_url}?{urlencode(params)}"
```

### Token Exchange
```python
def get_access_token(self, authorization_code):
    """
    Exchange authorization code for access token
    
    Args:
        authorization_code: Authorization code from provider
        
    Returns:
        dict: Token response with access_token, token_type, etc.
    """
    data = {
        'client_id': self.client_id,
        'client_secret': self.client_secret,
        'code': authorization_code,
        'grant_type': 'authorization_code',
        'redirect_uri': self.callback_url
    }
    
    request = urllib2.Request(self.token_url, urlencode(data).encode())
    request.add_header('Accept', 'application/json')
    request.add_header('Content-Type', 'application/x-www-form-urlencoded')
    
    response = urllib2.urlopen(request)
    return json.loads(response.read().decode())
```

### User Information Retrieval
```python
def get_user_info(self, access_token):
    """
    Retrieve user information from provider
    
    Args:
        access_token: Valid OAuth access token
        
    Returns:
        dict: User profile information
        
    Note: Must be implemented by provider-specific subclasses
    """
    raise NotImplementedError("Subclasses must implement get_user_info")
```

## Provider-Specific Implementations

### Facebook Integration
```python
class FacebookAccount(OAuthAccount):
    """Facebook OAuth 2.0 implementation"""
    
    def __init__(self, client_id, client_secret, callback_url=None):
        super().__init__(
            g=current,
            client_id=client_id,
            client_secret=client_secret,
            auth_url='https://www.facebook.com/dialog/oauth',
            token_url='https://graph.facebook.com/oauth/access_token',
            callback_url=callback_url,
            scope='email,public_profile'
        )
    
    def get_user_info(self, access_token):
        """Retrieve Facebook user profile"""
        url = f"https://graph.facebook.com/me?access_token={access_token}"
        url += "&fields=id,name,email,first_name,last_name"
        
        response = urllib2.urlopen(url)
        return json.loads(response.read().decode())
```

### Google Integration
```python
class GoogleAccount(OAuthAccount):
    """Google OAuth 2.0 implementation"""
    
    def __init__(self, client_id, client_secret, callback_url=None):
        super().__init__(
            g=current,
            client_id=client_id,
            client_secret=client_secret,
            auth_url='https://accounts.google.com/o/oauth2/auth',
            token_url='https://oauth2.googleapis.com/token',
            callback_url=callback_url,
            scope='openid email profile'
        )
    
    def get_user_info(self, access_token):
        """Retrieve Google user profile"""
        url = f"https://www.googleapis.com/oauth2/v2/userinfo"
        request = urllib2.Request(url)
        request.add_header('Authorization', f'Bearer {access_token}')
        
        response = urllib2.urlopen(request)
        return json.loads(response.read().decode())
```

## Security Features

### CSRF Protection
```python
def generate_state(self):
    """Generate cryptographically secure state parameter"""
    import random
    import string
    import hashlib
    
    # Generate random string
    random_str = ''.join(random.choices(string.ascii_letters + string.digits, k=32))
    
    # Add timestamp for expiration
    timestamp = str(int(time.time()))
    
    # Create hash for integrity
    combined = f"{random_str}:{timestamp}"
    state_hash = hashlib.sha256(combined.encode()).hexdigest()[:16]
    
    return f"{random_str}:{timestamp}:{state_hash}"

def validate_state(self, received_state):
    """Validate state parameter for CSRF protection"""
    try:
        parts = received_state.split(':')
        if len(parts) != 3:
            return False
        
        random_str, timestamp, received_hash = parts
        
        # Check timestamp (expire after 10 minutes)
        if int(time.time()) - int(timestamp) > 600:
            return False
        
        # Verify hash
        combined = f"{random_str}:{timestamp}"
        expected_hash = hashlib.sha256(combined.encode()).hexdigest()[:16]
        
        return received_hash == expected_hash
    except:
        return False
```

### Token Security
```python
def secure_token_storage(self, user_id, tokens):
    """Securely store OAuth tokens"""
    # Encrypt sensitive tokens
    encrypted_access = self.encrypt_token(tokens['access_token'])
    encrypted_refresh = tokens.get('refresh_token')
    if encrypted_refresh:
        encrypted_refresh = self.encrypt_token(encrypted_refresh)
    
    # Store with expiration
    expires_at = time.time() + tokens.get('expires_in', 3600)
    
    db.auth_oauth_tokens.insert(
        user_id=user_id,
        provider='oauth2_provider',
        access_token=encrypted_access,
        refresh_token=encrypted_refresh,
        expires_at=expires_at,
        created_at=time.time()
    )
```

## Error Handling

### OAuth Error Responses
```python
def handle_oauth_error(self, error_response):
    """Handle OAuth error responses"""
    error_code = error_response.get('error', 'unknown_error')
    error_description = error_response.get('error_description', 'Unknown error')
    
    error_mapping = {
        'invalid_request': 'Invalid OAuth request parameters',
        'unauthorized_client': 'Client authentication failed',
        'access_denied': 'User denied authorization',
        'unsupported_response_type': 'Authorization code flow not supported',
        'invalid_scope': 'Requested scope is invalid',
        'server_error': 'Authorization server error',
        'temporarily_unavailable': 'Service temporarily unavailable'
    }
    
    user_message = error_mapping.get(error_code, error_description)
    
    # Log detailed error for debugging
    import logging
    logging.error(f"OAuth error: {error_code} - {error_description}")
    
    # Return user-friendly error
    raise HTTP(400, user_message)
```

### Network Error Handling
```python
def robust_api_call(self, url, data=None, headers=None, retries=3):
    """Make API calls with retry logic and error handling"""
    for attempt in range(retries):
        try:
            request = urllib2.Request(url, data, headers or {})
            response = urllib2.urlopen(request, timeout=30)
            return response.read().decode()
            
        except urllib2.HTTPError as e:
            if e.code in [400, 401, 403]:
                # Client errors - don't retry
                raise
            elif attempt == retries - 1:
                # Final attempt failed
                raise
        except (urllib2.URLError, socket.timeout) as e:
            if attempt == retries - 1:
                raise
            time.sleep(2 ** attempt)  # Exponential backoff
```

## User Management Integration

### User Creation/Update
```python
def register_or_update_user(self, user_info):
    """Register new user or update existing user"""
    email = user_info.get('email')
    if not email:
        raise ValueError("Email required for user registration")
    
    # Check if user exists
    existing_user = db(db.auth_user.email == email).select().first()
    
    if existing_user:
        # Update existing user
        self.update_user_profile(existing_user, user_info)
        return existing_user
    else:
        # Create new user
        return self.create_new_user(user_info)

def create_new_user(self, user_info):
    """Create new user from OAuth profile"""
    user_data = {
        'first_name': user_info.get('first_name', ''),
        'last_name': user_info.get('last_name', ''),
        'email': user_info['email'],
        'username': user_info.get('username', user_info['email']),
        'password': 'oauth',  # Placeholder - user can't login with password
        'registration_key': '',  # Auto-activate OAuth users
        'registration_id': user_info.get('id', '')
    }
    
    user_id = db.auth_user.insert(**user_data)
    return db.auth_user[user_id]
```

## Complete Integration Example

### Web2py Controller Integration
```python
def oauth_login():
    """OAuth login handler"""
    # Initialize OAuth provider
    oauth = FacebookAccount(
        client_id=settings.facebook_client_id,
        client_secret=settings.facebook_client_secret
    )
    
    # Handle callback
    if request.vars.code:
        # Validate state for CSRF protection
        if not oauth.validate_state(request.vars.state):
            raise HTTP(400, "Invalid state parameter")
        
        try:
            # Exchange code for tokens
            token_response = oauth.get_access_token(request.vars.code)
            
            # Get user information
            user_info = oauth.get_user_info(token_response['access_token'])
            
            # Register or update user
            user = oauth.register_or_update_user(user_info)
            
            # Log user in
            auth.login_user(user)
            
            # Redirect to success page
            redirect(URL('default', 'index'))
            
        except Exception as e:
            # Handle authentication failure
            session.flash = f"Authentication failed: {str(e)}"
            redirect(URL('default', 'user', args=['login']))
    
    elif request.vars.error:
        # Handle authorization denial
        oauth.handle_oauth_error(request.vars)
    
    else:
        # Start OAuth flow
        authorization_url = oauth.get_authorization_url()
        redirect(authorization_url)
```

### Template Integration
```html
<!-- Login form with OAuth options -->
<div class="login-form">
    <h2>Login to Your Account</h2>
    
    <!-- Traditional login form -->
    {{=form}}
    
    <!-- OAuth login buttons -->
    <div class="oauth-buttons">
        <a href="{{=URL('default', 'oauth_login', vars={'provider': 'facebook'})}}" 
           class="btn btn-facebook">
            Login with Facebook
        </a>
        
        <a href="{{=URL('default', 'oauth_login', vars={'provider': 'google'})}}" 
           class="btn btn-google">
            Login with Google
        </a>
    </div>
</div>
```

## Best Practices

### Security Best Practices
1. **Always use HTTPS** for OAuth flows
2. **Validate state parameter** to prevent CSRF attacks
3. **Securely store client secrets** using environment variables
4. **Implement proper token expiration** and refresh logic
5. **Validate redirect URIs** to prevent open redirects

### Implementation Best Practices
1. **Handle all OAuth error scenarios** gracefully
2. **Implement retry logic** for network failures
3. **Cache user profile data** appropriately
4. **Log OAuth events** for monitoring and debugging
5. **Test with actual OAuth providers** regularly

### User Experience Best Practices
1. **Provide clear error messages** to users
2. **Implement loading states** during OAuth flow
3. **Allow account linking** for existing users
4. **Respect user privacy** and data minimization
5. **Provide logout functionality** that clears tokens