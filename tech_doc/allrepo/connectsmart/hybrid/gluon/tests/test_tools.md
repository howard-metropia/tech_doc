# test_tools.py

## Overview
Comprehensive unit tests for Web2py's tools module, covering authentication, email functionality, JWT tokens, file exposure, and various utility functions.

## Imports
```python
import datetime
import os
import shutil
import smtplib
import sys
import tempfile
import unittest
from gluon import H3, SPAN, TABLE, TD, TR, URL, A, current, tools
from gluon._compat import PY2, to_bytes
from gluon.dal import DAL, Field
from gluon.globals import Request, Response, Session
from gluon.http import HTTP
from gluon.languages import TranslatorFactory
from gluon.storage import Storage
from gluon.tools import (Auth, Expose, Mail, Recaptcha2, prettydate,
                         prevent_open_redirect)
```

## Test Classes

### TestMail
Tests the Mail class for SMTP email functionality.

#### Helper Classes

##### Message
Wrapper for email messages with parsing capabilities:
- Stores sender, recipient, and payload
- Provides `parsed_payload` property using Python's email module

##### DummySMTP
Mock SMTP server for testing:
- Maintains inbox and user collections
- Simulates authentication, TLS, and email sending
- Thread-safe for concurrent testing

#### Test Methods

##### test_hello_world()
Basic email sending test:
- Configures Mail with SMTP settings
- Sends email with subject, message, and reply-to
- Verifies email appears in mock inbox
- Validates headers and content

##### test_failed_login()
Tests authentication failure:
- Attempts login with invalid credentials
- Verifies send() returns False on auth failure

##### test_login()
Tests successful authentication:
- Adds user to mock server
- Verifies successful login and email sending
- Cleans up test data

##### test_html()
Tests HTML email detection:
- Sends HTML content
- Verifies Content-Type header is set to text/html

##### test_alternative()
Tests multipart alternative emails:
- Sends both text and HTML versions
- Verifies multipart/alternative content type
- Validates both parts are present

##### test_ssl()
Tests SSL connection support:
- Enables SSL setting
- Verifies connection works with SSL

##### test_tls()
Tests TLS/STARTTLS support:
- Enables TLS setting
- Verifies TLS connection functionality

##### test_attachment()
Tests file attachment functionality:
- Attaches test file
- Verifies attachment content matches original
- Tests custom content-id and content-type
- Validates error handling for missing filenames

### TestAuthJWT
Tests JSON Web Token authentication functionality.

#### setUp()
Creates test environment with:
- Mock request/response objects
- Database with auth tables
- Test user credentials
- AuthJWT instance with secret key

#### test_jwt_token_manager()
Tests token generation and validation:
- Generates token with username/password
- Validates token refresh functionality
- Tests token-based authentication

#### test_allows_jwt()
Tests JWT decorator functionality:
- Creates protected function with @allows_jwt()
- Verifies user authentication via JWT
- Validates user context within decorated function

### TestAuth
Comprehensive authentication system tests.

#### setUp()
Creates complete auth environment:
- Request/response/session objects
- Database with auth tables and versioning
- Test user registration
- Various auth settings

#### Test Categories

##### Form Testing
- `test_basic_blank_forms()`: Tests form generation for login, registration, etc.
- `test_change_password()`: Password change form
- `test_profile()`: User profile form
- `test_bulk_register()`: Bulk user registration

##### User Management
- `test_get_or_create_user()`: User creation and retrieval
- `test_register_bare()`: Programmatic user registration
- `test_login_bare()`: Direct authentication without forms
- `test_logout_bare()`: Session termination

##### Group Management
- `test_add_group()`: Group creation
- `test_del_group()`: Group removal
- `test_id_group()`: Group ID lookup
- `test_user_group()`: User's primary group
- `test_user_group_role()`: Group role determination

##### Membership Management
- `test_has_membership()`: Membership checking
- `test_add_membership()`: Adding users to groups
- `test_del_membership()`: Removing memberships

##### Permission Management
- `test_has_permission()`: Permission checking
- `test_add_permission()`: Granting permissions
- `test_del_permission()`: Revoking permissions

##### Advanced Features
- `test_impersonate()`: User impersonation system
- `test_log_event()`: Event logging
- `test_random_password()`: Password generation

### TestToolsFunctions
Tests utility functions from the tools module.

#### test_prettydate()
Comprehensive testing of human-readable date formatting:
- **Time Units**: seconds, minutes, hours, days, weeks, months, years
- **Pluralization**: Handles singular/plural forms correctly
- **Future Dates**: "X from now" format
- **UTC Support**: UTC timezone handling
- **Edge Cases**: None values, invalid dates
- **Date Objects**: Works with both datetime and date objects

### Test_Expose__in_base
Tests path validation for the Expose class.

#### test_in_base()
Tests valid path relationships:
- Subdirectories under parent directories
- Same directory comparisons
- Root directory cases

#### test_not_in_base()
Tests invalid path relationships:
- Paths outside base directory
- Sibling directories
- Reverse relationships

### TestExpose
Tests file/directory exposure functionality for file browsers.

#### Setup
Creates complex directory structure with:
- Regular files and directories
- Symbolic links (on POSIX systems)
- Links pointing inside and outside base directory
- README files for content testing

#### Test Methods

##### State Testing
- `test_expose_inside_state()`: Basic directory listing
- `test_expose_inside_dir1_state()`: Subdirectory contents
- `test_expose_inside_dir2_state()`: Directory with symlinks

##### XML Generation
- `test_xml_inside()`: HTML table generation for directories
- `test_xml_dir1()`: File listing HTML
- `test_xml_dir2()`: Symlink handling in HTML

##### Security Testing
- `test_file_not_found()`: 404 handling
- `test_not_authorized()`: Access control for symlinks

##### Symlink Handling
- Configurable symlink following
- Security restrictions for external links
- Proper link resolution

### Test_OpenRedirectPrevention
Tests security measures against open redirect attacks.

#### test_open_redirect()
Validates URL sanitization:
- **Bad URLs**: Protocol-relative URLs, backslash variations
- **Good URLs**: Legitimate relative and absolute URLs
- **Host Validation**: Ensures redirects stay within allowed domains
- **Protocol Prefixes**: Tests various protocol combinations

## Key Features Tested

### Authentication System
- Complete user lifecycle (register, login, logout)
- Group and permission management
- User impersonation with security checks
- Event logging and auditing

### Email System
- SMTP authentication and encryption
- HTML/text multipart emails
- File attachments with metadata
- Mock testing infrastructure

### JWT Authentication
- Token generation and validation
- Decorator-based protection
- Token refresh mechanisms

### File Exposure
- Directory browsing with security
- Symlink handling and validation
- HTML generation for file lists
- Access control enforcement

### Security Features
- Open redirect prevention
- Path traversal protection
- Authentication bypass prevention
- Input validation and sanitization

### Utility Functions
- Human-readable date formatting
- Password generation
- Event logging
- Form generation

## Testing Patterns

### Mock Objects
- SMTP server simulation
- Request/response mocking
- Database isolation

### Security Testing
- Invalid input handling
- Authorization bypass attempts
- Path traversal prevention

### Integration Testing
- Complete auth workflows
- Email sending pipelines
- File system interactions

## Notes
- Extensive use of mock objects for external dependencies
- Platform-specific testing (symlinks on POSIX)
- Security-focused testing throughout
- Comprehensive coverage of Web2py's core tools