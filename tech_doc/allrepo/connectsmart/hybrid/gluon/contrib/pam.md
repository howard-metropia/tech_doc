# Gluon Contrib PAM Module

## Overview
Pluggable Authentication Modules (PAM) integration for Python applications. Provides user authentication against system PAM services using ctypes, enabling password verification without requiring compilation of external libraries.

## Module Information
- **Module**: `gluon.contrib.pam`
- **Author**: Chris AtLee
- **License**: MIT License
- **Dependencies**: PAM system library, ctypes
- **Platform**: Unix/Linux systems with PAM support

## Key Features
- **System Authentication**: Authenticate against system user accounts
- **PAM Integration**: Full PAM conversation protocol support
- **ctypes Implementation**: No compilation required
- **Service Flexibility**: Support for different PAM services
- **Password Security**: Secure password handling through PAM

## Core Function

### authenticate()
Main authentication function that validates username/password against PAM.

**Signature:**
```python
def authenticate(username, password, service='login')
```

**Parameters:**
- `username`: Username to authenticate (string)
- `password`: Password in plain text (string)  
- `service`: PAM service name (default: 'login')

**Returns:**
- `True`: Authentication successful
- `False`: Authentication failed or error occurred

**Example:**
```python
from gluon.contrib.pam import authenticate

# Authenticate user against system
if authenticate('john', 'password123'):
    print("Authentication successful")
else:
    print("Authentication failed")

# Authenticate against specific service
if authenticate('john', 'password123', service='sshd'):
    print("SSH authentication successful")
```

## PAM Services

### Common Services
- **login**: Default login service
- **sshd**: SSH daemon authentication
- **su**: Switch user authentication  
- **passwd**: Password change service
- **ftp**: FTP service authentication
- **httpd**: Web server authentication

### Service Configuration
PAM services are configured in `/etc/pam.d/` directory:
```bash
# Example: /etc/pam.d/myapp
auth    required    pam_unix.so
account required    pam_unix.so
```

## Implementation Details

### ctypes Structures
The module defines ctypes structures for PAM interaction:

#### PamHandle
```python
class PamHandle(Structure):
    _fields_ = [("handle", c_void_p)]
```
Wrapper for PAM handle structure.

#### PamMessage  
```python
class PamMessage(Structure):
    _fields_ = [
        ("msg_style", c_int),
        ("msg", c_char_p),
    ]
```
PAM message structure for prompts and information.

#### PamResponse
```python
class PamResponse(Structure):
    _fields_ = [
        ("resp", c_char_p),
        ("resp_retcode", c_int),
    ]
```
Response structure for PAM conversation.

#### PamConv
```python
class PamConv(Structure):
    _fields_ = [
        ("conv", CONV_FUNC),
        ("appdata_ptr", c_void_p)
    ]
```
Conversation function structure.

### Conversation Protocol
PAM uses a conversation mechanism to interact with the user:

```python
@CONV_FUNC
def my_conv(n_messages, messages, p_response, app_data):
    """Conversation function that responds to prompts"""
    # Allocate response array
    addr = CALLOC(n_messages, sizeof(PamResponse))
    p_response[0] = cast(addr, POINTER(PamResponse))
    
    # Process each message
    for i in range(n_messages):
        if messages[i].contents.msg_style == PAM_PROMPT_ECHO_OFF:
            # Respond to password prompt
            pw_copy = STRDUP(str(password))
            p_response.contents[i].resp = cast(pw_copy, c_char_p)
            p_response.contents[i].resp_retcode = 0
    return 0
```

### Message Types
- `PAM_PROMPT_ECHO_OFF` (1): Password prompt (hidden input)
- `PAM_PROMPT_ECHO_ON` (2): Username prompt (visible input)
- `PAM_ERROR_MSG` (3): Error message
- `PAM_TEXT_INFO` (4): Informational message

## Usage Examples

### Basic Authentication
```python
from gluon.contrib.pam import authenticate

def login_user(username, password):
    """Authenticate user against system accounts"""
    if authenticate(username, password):
        # User authenticated successfully
        session.user = username
        session.authenticated = True
        return True
    else:
        # Authentication failed
        session.flash = "Invalid username or password"
        return False
```

### Web2py Controller Integration
```python
def user_login():
    """Login controller using PAM authentication"""
    form = FORM(
        INPUT(_name='username', _placeholder='Username', requires=IS_NOT_EMPTY()),
        INPUT(_name='password', _type='password', _placeholder='Password', requires=IS_NOT_EMPTY()),
        INPUT(_type='submit', _value='Login')
    )
    
    if form.process().accepted:
        username = request.vars.username
        password = request.vars.password
        
        if authenticate(username, password):
            session.user = username
            session.flash = "Login successful"
            redirect(URL('default', 'index'))
        else:
            form.errors.username = "Authentication failed"
    
    return dict(form=form)
```

### Service-Specific Authentication
```python
def ssh_auth_check(username, password):
    """Check if user can authenticate via SSH"""
    return authenticate(username, password, service='sshd')

def ftp_auth_check(username, password):
    """Check if user can authenticate via FTP"""
    return authenticate(username, password, service='ftp')

def admin_auth_check(username, password):
    """Check if user can switch to admin"""
    return authenticate(username, password, service='su')
```

### Error Handling
```python
def safe_authenticate(username, password, service='login'):
    """Safe authentication with error handling"""
    try:
        result = authenticate(username, password, service)
        return result, None
    except Exception as e:
        logger.error("PAM authentication error: %s" % str(e))
        return False, str(e)

# Usage
success, error = safe_authenticate('john', 'password')
if success:
    print("Authentication successful")
elif error:
    print("Authentication error: %s" % error)
else:
    print("Authentication failed")
```

## Security Considerations

### Password Security
- Passwords are passed to PAM in plain text
- PAM handles secure password verification
- No password storage in application
- Secure memory handling by PAM libraries

### Best Practices
```python
# Clear password from memory after use
def authenticate_secure(username, password, service='login'):
    try:
        result = authenticate(username, password, service)
        return result
    finally:
        # Clear password variable (limited effectiveness in Python)
        password = None
        del password
```

### Access Control
```python
def check_user_permissions(username):
    """Check if user has required permissions"""
    import pwd
    import grp
    
    try:
        user_info = pwd.getpwnam(username)
        # Check user groups, home directory, shell, etc.
        return user_info.pw_shell != '/bin/false'
    except KeyError:
        return False

def authenticated_login(username, password):
    """Complete authentication with permission check"""
    if authenticate(username, password):
        if check_user_permissions(username):
            return True
        else:
            logger.warning("User %s authenticated but lacks permissions" % username)
            return False
    return False
```

## System Requirements

### PAM Library
- libpam must be installed on the system
- PAM development headers for some distributions
- Proper PAM configuration files

### Installation Check
```python
def check_pam_availability():
    """Check if PAM is available on the system"""
    try:
        from ctypes.util import find_library
        pam_lib = find_library("pam")
        if pam_lib:
            return True
        else:
            return False
    except:
        return False

if not check_pam_availability():
    print("PAM library not available on this system")
```

### Platform Support
- Linux: Full PAM support
- macOS: Limited PAM support
- FreeBSD: PAM support available
- Windows: Not supported (no PAM)

## Configuration Examples

### Custom PAM Service
Create `/etc/pam.d/mywebapp`:
```
#%PAM-1.0
auth    required    pam_unix.so
account required    pam_unix.so
session required    pam_unix.so
```

### LDAP Integration
```
#%PAM-1.0
auth    required    pam_ldap.so
account required    pam_ldap.so
```

### Two-Factor Authentication
```
#%PAM-1.0
auth    required    pam_unix.so
auth    required    pam_google_authenticator.so
account required    pam_unix.so
```

## Troubleshooting

### Common Issues
```python
def debug_pam_auth(username, password, service='login'):
    """Debug PAM authentication issues"""
    import os
    import logging
    
    # Check PAM service file exists
    service_file = '/etc/pam.d/%s' % service
    if not os.path.exists(service_file):
        logging.error("PAM service file not found: %s" % service_file)
        return False
    
    # Check user exists
    try:
        import pwd
        pwd.getpwnam(username)
    except KeyError:
        logging.error("User does not exist: %s" % username)
        return False
    
    # Attempt authentication
    try:
        result = authenticate(username, password, service)
        logging.info("PAM authentication result: %s" % result)
        return result
    except Exception as e:
        logging.error("PAM authentication exception: %s" % str(e))
        return False
```

### Testing
```python
if __name__ == "__main__":
    import getpass
    
    # Interactive testing
    username = input("Username: ")
    password = getpass.getpass("Password: ")
    
    if authenticate(username, password):
        print("Authentication successful!")
    else:
        print("Authentication failed!")
```

This module provides robust system-level authentication capabilities for web2py applications, enabling integration with existing user management infrastructure through PAM.