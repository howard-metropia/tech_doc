# gluon/contrib/login_methods/basic_auth.py

## Overview

The basic_auth.py module provides HTTP Basic Authentication integration for Web2py applications. This module enables authentication against external servers using the HTTP Basic Authentication protocol, allowing Web2py applications to authenticate users against existing HTTP-based authentication services.

## Key Components

### Main Function: basic_auth()
```python
def basic_auth(server="http://127.0.0.1"):
    """
    Factory function for basic authentication method
    
    Args:
        server: Authentication server URL
        
    Returns:
        Authentication function for Web2py Auth system
    """
```

### Authentication Process
1. **Credential Encoding**: Username and password are Base64 encoded
2. **HTTP Request**: Basic auth header sent to authentication server
3. **Response Validation**: Server response determines authentication success
4. **Result**: Returns True/False based on server response

## Dependencies

### Standard Library
```python
import base64           # For credential encoding
```

### Web2py Components
```python
from gluon._compat import urlopen    # Cross-version URL handling
from gluon._compat import urllib2    # HTTP request handling
```

## Implementation Details

### Authentication Function Factory
```python
def basic_auth(server="http://127.0.0.1"):
    def basic_login_aux(username, password, server=server):
        """
        Inner authentication function
        
        Args:
            username: User identifier
            password: User credential
            server: Authentication server (from closure)
            
        Returns:
            bool: Authentication success status
        """
        # Encode credentials
        key = base64.b64encode(username + ':' + password)
        
        # Prepare request headers
        headers = {'Authorization': 'Basic ' + key}
        request = urllib2.Request(server, None, headers)
        
        # Attempt authentication
        try:
            urlopen(request)
            return True
        except (urllib2.URLError, urllib2.HTTPError):
            return False
    
    return basic_login_aux
```

### Credential Encoding
```python
# Base64 encoding of username:password
credentials = f"{username}:{password}"
encoded = base64.b64encode(credentials.encode('utf-8'))
auth_header = f"Basic {encoded.decode('ascii')}"
```

## Usage Patterns

### Basic Implementation
```python
from gluon.contrib.login_methods.basic_auth import basic_auth

# Add basic auth to Web2py Auth
auth.settings.login_methods.append(
    basic_auth('http://auth.company.com/authenticate')
)
```

### Multiple Servers
```python
# Support multiple authentication servers
auth_servers = [
    'http://primary.auth.server',
    'http://backup.auth.server',
    'http://legacy.auth.server'
]

for server in auth_servers:
    auth.settings.login_methods.append(basic_auth(server))
```

### Secure Configuration
```python
# Use HTTPS for secure authentication
secure_server = 'https://secure.auth.company.com/api/auth'
auth.settings.login_methods.append(basic_auth(secure_server))
```

## Server Requirements

### Authentication Endpoint
The target server must:
1. Accept HTTP Basic Authentication
2. Return HTTP 200 for valid credentials
3. Return HTTP 401/403 for invalid credentials
4. Handle UTF-8 encoded usernames/passwords

### Response Handling
```python
# Server response expectations:
# Success: HTTP 200 OK
# Failure: HTTP 401 Unauthorized or HTTP 403 Forbidden
# Error: Any other HTTP error code
```

## Security Considerations

### Credential Transmission
- **HTTPS Required**: Basic auth sends credentials in easily decoded format
- **Network Security**: Ensure secure network channels
- **Credential Exposure**: Base64 is encoding, not encryption

### Implementation Security
```python
# Security best practices
def secure_basic_auth(server):
    # Validate HTTPS usage
    if not server.startswith('https://'):
        raise ValueError("HTTPS required for secure basic auth")
    
    # Additional security headers
    def auth_function(username, password):
        headers = {
            'Authorization': f'Basic {base64.b64encode(f"{username}:{password}".encode()).decode()}',
            'User-Agent': 'Web2py-BasicAuth/1.0',
            'Accept': 'application/json'
        }
        # ... rest of implementation
```

### Error Handling Enhancement
```python
def robust_basic_auth(server, timeout=30, retries=3):
    def auth_function(username, password):
        for attempt in range(retries):
            try:
                # Authentication logic with timeout
                request = urllib2.Request(server, None, headers)
                response = urlopen(request, timeout=timeout)
                return True
            except urllib2.HTTPError as e:
                if e.code in [401, 403]:
                    return False  # Invalid credentials
                elif attempt == retries - 1:
                    raise  # Final attempt failed
                time.sleep(1)  # Brief retry delay
            except (urllib2.URLError, socket.timeout):
                if attempt == retries - 1:
                    return False  # Network/timeout failure
                time.sleep(2)  # Longer delay for network issues
```

## Integration Examples

### Apache HTTP Server
```apache
# Apache .htaccess for basic auth endpoint
AuthType Basic
AuthName "Web2py Authentication"
AuthUserFile /path/to/.htpasswd
Require valid-user
```

### Nginx Configuration
```nginx
# Nginx basic auth configuration
location /auth {
    auth_basic "Web2py Authentication";
    auth_basic_user_file /etc/nginx/.htpasswd;
    
    # Return 200 for successful auth
    return 200 "Authentication successful";
}
```

### Custom Python Server
```python
# Simple Flask authentication server
from flask import Flask, request
import base64

app = Flask(__name__)

@app.route('/authenticate', methods=['GET', 'POST'])
def authenticate():
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Basic '):
        return 'Unauthorized', 401
    
    try:
        encoded = auth_header[6:]  # Remove 'Basic '
        decoded = base64.b64decode(encoded).decode('utf-8')
        username, password = decoded.split(':', 1)
        
        # Validate credentials against your system
        if validate_user(username, password):
            return 'OK', 200
        else:
            return 'Invalid credentials', 401
    except:
        return 'Bad request', 400
```

## Error Handling

### Network Errors
```python
def handle_network_errors(auth_func):
    def wrapper(username, password):
        try:
            return auth_func(username, password)
        except urllib2.URLError as e:
            # Log network error
            import logging
            logging.error(f"Basic auth network error: {e}")
            return False
        except Exception as e:
            # Log unexpected errors
            logging.error(f"Basic auth unexpected error: {e}")
            return False
    return wrapper
```

### Timeout Management
```python
import socket

def basic_auth_with_timeout(server, timeout=10):
    def auth_function(username, password):
        old_timeout = socket.getdefaulttimeout()
        try:
            socket.setdefaulttimeout(timeout)
            # Perform authentication
            return basic_auth_request(username, password, server)
        finally:
            socket.setdefaulttimeout(old_timeout)
```

## Performance Optimization

### Connection Reuse
```python
import urllib2

# Create opener with connection pooling
opener = urllib2.build_opener(urllib2.HTTPSHandler())

def optimized_basic_auth(server):
    def auth_function(username, password):
        request = urllib2.Request(server, None, headers)
        try:
            opener.open(request)
            return True
        except (urllib2.URLError, urllib2.HTTPError):
            return False
    return auth_function
```

### Caching Results
```python
import time
from functools import lru_cache

@lru_cache(maxsize=128)
def cached_auth_check(username, password_hash, timestamp):
    """Cache authentication results for short period"""
    # Implementation would check actual auth
    pass

def cached_basic_auth(server, cache_duration=300):
    def auth_function(username, password):
        # Create cache key
        import hashlib
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        timestamp = int(time.time() / cache_duration)
        
        return cached_auth_check(username, password_hash, timestamp)
```

## Testing and Validation

### Unit Testing
```python
import unittest
from unittest.mock import patch
from gluon.contrib.login_methods.basic_auth import basic_auth

class TestBasicAuth(unittest.TestCase):
    @patch('gluon.contrib.login_methods.basic_auth.urlopen')
    def test_successful_auth(self, mock_urlopen):
        mock_urlopen.return_value = None
        
        auth_func = basic_auth('http://test.server')
        result = auth_func('testuser', 'testpass')
        
        self.assertTrue(result)
    
    @patch('gluon.contrib.login_methods.basic_auth.urlopen')
    def test_failed_auth(self, mock_urlopen):
        mock_urlopen.side_effect = urllib2.HTTPError(
            url='http://test.server', 
            code=401, 
            msg='Unauthorized', 
            hdrs={}, 
            fp=None
        )
        
        auth_func = basic_auth('http://test.server')
        result = auth_func('baduser', 'badpass')
        
        self.assertFalse(result)
```

## Best Practices

### Security Guidelines
1. **Always use HTTPS** for production environments
2. **Validate server certificates** to prevent MITM attacks
3. **Implement timeouts** to prevent hanging requests
4. **Log authentication attempts** for security monitoring
5. **Use strong passwords** and consider password policies

### Implementation Guidelines
1. **Handle network failures gracefully**
2. **Implement retry logic** for transient failures
3. **Cache results appropriately** to reduce server load
4. **Validate configuration** before deployment
5. **Monitor authentication performance**

### Deployment Considerations
1. **Test against actual authentication servers**
2. **Monitor server response times**
3. **Implement fallback authentication methods**
4. **Document server requirements**
5. **Plan for server maintenance windows**