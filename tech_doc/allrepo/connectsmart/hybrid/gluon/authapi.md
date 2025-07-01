# Gluon Authentication API Module (`authapi.py`)

## Overview
AuthAPI is a lightweight, barebones authentication implementation for web2py that operates without HTML forms, redirects, email functionality, or URL handling. It follows a "Dict In → Dict Out" pattern, making it ideal for API-based authentication systems and headless applications.

## Architecture

### Core Dependencies
```python
import datetime
from pydal.objects import Field, Row, Table
from gluon import current
from gluon._compat import long
from gluon.settings import global_settings
from gluon.storage import Messages, Settings, Storage
from gluon.utils import web2py_uuid
from gluon.validators import (CRYPT, IS_EMAIL, IS_EQUAL_TO, IS_INT_IN_RANGE,
                              IS_LOWER, IS_MATCH, IS_NOT_EMPTY, IS_NOT_IN_DB)
```

### Class Structure
```python
class AuthAPI(object):
    """
    Barebones Auth implementation with Dict In -> Dict Out logic
    No HTML forms, redirects, emailing, or URL handling
    """
```

## Configuration

### Default Settings
```python
default_settings = {
    "create_user_groups": "user_%(id)s",
    "email_case_sensitive": False,
    "everybody_group_id": None,
    "expiration": 3600,  # 1 hour
    "keep_session_onlogin": True,
    "keep_session_onlogout": False,
    "logging_enabled": True,
    "login_after_registration": False,
    "login_email_validate": True,
    "login_userfield": None,
    "logout_onlogout": None,
    "long_expiration": 3600 * 24 * 30,  # 30 days
    "ondelete": "CASCADE",
    "password_field": "password",
    "password_min_length": 4,
    "registration_requires_approval": False,
    "registration_requires_verification": False,
    "renew_session_onlogin": True,
    "renew_session_onlogout": True,
    # Table naming
    "table_event_name": "auth_event",
    "table_group_name": "auth_group",
    "table_membership_name": "auth_membership",
    "table_permission_name": "auth_permission",
    "table_user_name": "auth_user",
    "use_username": False,
    "username_case_sensitive": True,
}
```

### Default Messages
```python
default_messages = {
    "add_group_log": "Group %(group_id)s created",
    "change_password_log": "User %(id)s Password changed",
    "del_group_log": "Group %(group_id)s deleted",
    "email_taken": "This email already has an account",
    "group_description": "Group uniquely assigned to user %(id)s",
    "invalid_email": "Invalid email",
    "invalid_login": "Invalid login",
    "invalid_password": "Invalid password",
    "invalid_user": "Invalid user",
    "invalid_key": "Invalid key",
    "invalid_username": "Invalid username",
    "key_verified": "Key verified",
    "logged_in": "Logged in",
    "logged_out": "Logged out",
    "login_log": "User %(id)s Logged-in",
    "logout_log": "User %(id)s Logged-out",
    "mismatched_password": "Password fields don't match",
    "password_changed": "Password changed",
    "profile_log": "User %(id)s Profile updated",
    "profile_updated": "Profile updated",
    "register_log": "User %(id)s Registered",
    "registration_pending": "Registration is pending approval",
    "registration_successful": "Registration successful",
    "registration_verifying": "Registration needs verification",
    "username_taken": "Username already taken",
    "verify_log": "User %(id)s verified registration key",
}
```

## Initialization

### Constructor
```python
def __init__(self, db=None, hmac_key=None, signature=True):
    self.db = db
    session = current.session
    auth = session.auth
    self.user_groups = auth and auth.user_groups or {}
    
    # Session expiration handling
    if auth:
        delta = datetime.timedelta(days=0, seconds=auth.expiration)
        if auth.last_visit and auth.last_visit + delta > now:
            self.user = auth.user
            # Update last_visit for session management
            if (now - auth.last_visit).seconds > (auth.expiration // 10):
                auth.last_visit = now
        else:
            # Session expired - clear auth
            self.user = None
            if session.auth:
                del session.auth
            session.renew(clear_session=True)
    else:
        self.user = None
```

## Database Schema

### Table Definitions

#### User Table
```python
# With username support
db.define_table(
    settings.table_user_name,
    Field("first_name", length=128, default="", requires=is_not_empty),
    Field("last_name", length=128, default="", requires=is_not_empty),
    Field("email", length=512, default="", requires=is_unique_email),
    Field("username", length=128, default="", requires=is_unique_username),
    Field(passfield, "password", length=512, readable=False, requires=[is_crypted]),
    Field("registration_key", length=512, writable=False, readable=False, default=""),
    Field("reset_password_key", length=512, writable=False, readable=False, default=""),
    Field("registration_id", length=512, writable=False, readable=False, default=""),
    *extra_fields,
    format="%(username)s"
)
```

#### Group Table
```python
db.define_table(
    settings.table_group_name,
    Field("role", length=512, default="", requires=IS_NOT_IN_DB(db, "auth_group.role")),
    Field("description", "text"),
    *extra_fields,
    format="%(role)s (%(id)s)"
)
```

#### Membership Table
```python
db.define_table(
    settings.table_membership_name,
    Field("user_id", reference_table_user),
    Field("group_id", reference_table_group),
    *extra_fields
)
```

#### Permission Table
```python
db.define_table(
    settings.table_permission_name,
    Field("group_id", reference_table_group),
    Field("name", default="default", length=512, requires=is_not_empty),
    Field("table_name", length=512),
    Field("record_id", "integer", default=0, requires=IS_INT_IN_RANGE(0, 10**9)),
    *extra_fields
)
```

#### Event Logging Table
```python
db.define_table(
    settings.table_event_name,
    Field("time_stamp", "datetime", default=current.request.now),
    Field("client_ip", default=current.request.client),
    Field("user_id", reference_table_user, default=None),
    Field("origin", default="auth", length=512, requires=is_not_empty),
    Field("description", "text", default="", requires=is_not_empty),
    *extra_fields
)
```

## Core Authentication Methods

### Login
```python
def login(self, log=DEFAULT, **kwargs):
    """
    Login a user with Dict In -> Dict Out pattern
    
    Keyword Args:
        username/email (string): User identifier
        password (string): User's password
        remember_me (boolean): Extend session duration
    
    Returns:
        {
            "errors": dict or None,
            "message": string,
            "user": dict or None
        }
    """
```

**Login Process:**
1. Validate userfield (username/email)
2. Retrieve user record
3. Check account status (pending, disabled, blocked)
4. Verify password
5. Create session and update groups
6. Return standardized response

### Registration
```python
def register(self, log=DEFAULT, **kwargs):
    """
    Register a new user
    
    Returns:
        {
            "errors": dict or None,
            "message": string,
            "user": dict or None
        }
    """
```

**Registration Process:**
1. Validate input fields
2. Check uniqueness constraints
3. Generate registration key
4. Insert user record
5. Create user groups
6. Handle verification/approval requirements
7. Optional automatic login

### Profile Management
```python
def profile(self, log=DEFAULT, **kwargs):
    """
    Update user profile
    
    Returns:
        {
            "errors": dict or None,
            "message": string,
            "user": dict or None
        }
    """
```

### Password Change
```python
def change_password(self, log=DEFAULT, **kwargs):
    """
    Change user password
    
    Keyword Args:
        old_password (string): Current password
        new_password (string): New password
        new_password2 (string): Password confirmation
    
    Returns:
        {
            "errors": dict or None,
            "message": string
        }
    """
```

### Logout
```python
def logout(self, log=DEFAULT, onlogout=DEFAULT, **kwargs):
    """
    Logout current user
    
    Returns:
        {
            "errors": None,
            "message": string,
            "user": None
        }
    """
```

## Group and Permission Management

### Group Operations
```python
def add_group(self, role, description=""):
    """Creates a group with specified role"""
    
def del_group(self, group_id):
    """Deletes group and associated memberships/permissions"""
    
def id_group(self, role):
    """Returns group_id for specified role"""
    
def user_group(self, user_id=None):
    """Returns user's personal group_id"""
```

### Membership Management
```python
def add_membership(self, group_id=None, user_id=None, role=None):
    """Adds user to group"""
    
def del_membership(self, group_id=None, user_id=None, role=None):
    """Removes user from group"""
    
def has_membership(self, group_id=None, user_id=None, role=None, cached=False):
    """Checks if user belongs to group"""
```

### Permission System
```python
def add_permission(self, group_id, name="any", table_name="", record_id=0):
    """Grants permission to group"""
    
def del_permission(self, group_id, name="any", table_name="", record_id=0):
    """Revokes permission from group"""
    
def has_permission(self, name="any", table_name="", record_id=0, 
                   user_id=None, group_id=None):
    """Checks if user/group has specific permission"""
```

## Session Management

### Session Handling
```python
def _update_session_user(self, user):
    """Updates session with user information"""
    if global_settings.web2py_runtime_gae:
        user = Row(self.table_user()._filter_fields(user, id=True))
        delattr(user, self.settings.password_field)
    else:
        user = Row(user)
        for key in list(user.keys()):
            value = user[key]
            if callable(value) or key == self.settings.password_field:
                delattr(user, key)
    
    current.session.auth = Storage(
        user=user,
        last_visit=current.request.now,
        expiration=self.settings.expiration,
        hmac_key=web2py_uuid(),
    )
    return user
```

### Session Expiration
- **Short Expiration**: 3600 seconds (1 hour) default
- **Long Expiration**: 2,592,000 seconds (30 days) for "remember me"
- **Automatic Renewal**: Updates last_visit timestamp
- **Session Cleanup**: Removes expired sessions

## Verification System

### Email Verification
```python
def verify_key(self, key=None, ignore_approval=False, log=DEFAULT):
    """
    Verify registration key
    
    Keyword Args:
        key (string): Registration verification key
    
    Returns:
        {
            "errors": dict or None,
            "message": string
        }
    """
```

**Verification Process:**
1. Validate key exists in database
2. Update registration status
3. Handle approval requirements
4. Synchronize session state
5. Log verification event

## Event Logging

### Audit Trail
```python
def log_event(self, description, vars=None, origin="auth"):
    """
    Logs authentication events for audit trail
    
    Features:
    - User action tracking
    - IP address logging
    - Timestamp recording
    - Configurable logging levels
    """
```

**Logged Events:**
- User login/logout
- Registration attempts
- Password changes
- Permission modifications
- Group membership changes

## Security Features

### Password Security
- **CRYPT Validator**: Secure password hashing
- **Minimum Length**: Configurable password requirements
- **Password Verification**: Secure comparison
- **Salt Generation**: Automatic salt handling

### Session Security
- **HMAC Keys**: Unique session keys per user
- **Session Renewal**: Automatic session regeneration
- **Expiration Handling**: Configurable timeouts
- **Cross-Session Protection**: Session invalidation

### Input Validation
- **Email Validation**: Format and uniqueness checking
- **Username Validation**: Pattern matching and uniqueness
- **Field Validation**: Comprehensive input sanitization
- **SQL Injection Protection**: Parameterized queries

## API Response Format

### Standardized Responses
All methods return consistent dictionary structures:

```python
{
    "errors": {
        "field_name": "error_message",
        # ... additional field errors
    } or None,
    "message": "Human-readable status message",
    "user": {
        "id": user_id,
        "email": "user@example.com",
        # ... other readable fields
    } or None
}
```

## Integration Patterns

### API Development
- **RESTful Services**: Clean dict-based responses
- **JSON APIs**: Direct serialization support
- **Microservices**: Lightweight authentication
- **Headless Applications**: No UI dependencies

### Framework Integration
- **Current Context**: Uses web2py's current object
- **Database Integration**: PyDAL compatibility
- **Session Management**: web2py session system
- **Validation System**: Leverages web2py validators

This module provides a robust, API-focused authentication system that maintains the security and flexibility of web2py's auth system while removing UI dependencies for modern application architectures.