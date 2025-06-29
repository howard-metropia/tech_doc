# test_web.py

## Overview
This file contains integration tests for running web2py as a complete web server. It tests the full web2py stack including HTTP server functionality, web client interactions, cookie handling, and end-to-end application workflows.

## Purpose
- Tests complete web2py web server functionality
- Validates HTTP client-server interactions
- Tests cookie parsing and handling
- Verifies user registration and authentication workflows
- Tests WebClient functionality for HTTP requests
- Validates complete application lifecycle testing

## Key Functions and Classes

### Global Functions

#### `startwebserver()`
Starts a web2py web server process for testing.

**Server Startup Process:**
```python
web2py_exec = os.path.join(path, "web2py.py")
webserverprocess = subprocess.Popen([sys.executable, web2py_exec, "-a", "testpass"])
```

**Startup Verification:**
- Waits for server to become available
- Tests server responsiveness with WebClient
- Provides startup status feedback
- Handles startup timing and retries

#### `stopwebserver()`
Stops the running web2py server process.

```python
webserverprocess.terminate()
```

### Cookie Class
Tests cookie parsing and handling functionality.

#### Test Methods

##### `testParseMultipleEquals(self)`
Tests cookie parsing with multiple equals signs (Issue #1500).

**Cookie Parsing Testing:**
```python
client = WebClient()
client.headers["set-cookie"] = "key = value with one =;"
client._parse_headers_in_cookies()

# Should correctly parse: key = "value with one ="
self.assertEqual(client.cookies["key"], "value with one =")
```

**Multiple Equals Handling:**
```python
client.headers["set-cookie"] = "key = value with one = and another one =;"
# Should parse: key = "value with one = and another one ="
```

### LiveTest Class
Base class for live web server testing.

#### Class Methods

##### `setUpClass(cls)`
Class-level setup for live testing.

**Test Application Setup:**
- Creates test application directory
- Initializes application structure
- Starts web2py web server
- Waits for server availability

##### `tearDownClass(cls)`
Class-level cleanup after testing.

- Stops web server process
- Removes test application
- Cleans up temporary files

### TestWeb Class
Comprehensive web server and application testing.

#### Test Methods

##### `testRegisterAndLogin(self)`
Tests complete user registration and login workflow.

**WebClient Setup:**
```python
client = WebClient("http://127.0.0.1:8000/%s/default/" % test_app_name)
client.get("index")
```

**User Registration Testing:**
- Tests user registration form submission
- Validates form data handling
- Verifies user creation in database
- Tests registration confirmation process

**Login Testing:**
- Tests user authentication
- Validates session management
- Verifies authenticated user access
- Tests logout functionality

## Dependencies
- `unittest` - Python testing framework
- `subprocess` - Process management for web server
- `time` - Timing and delays for server startup
- `os` - Operating system interface
- `shutil` - High-level file operations
- `sys` - System-specific parameters
- `gluon._compat` - Cross-version compatibility
- `gluon.contrib.webclient` - WebClient for HTTP requests
- `gluon.fileutils` - File utilities

## Web Server Testing Features

### Server Lifecycle
- **Server Startup**: Automatic web2py server process creation
- **Availability Testing**: Server readiness verification
- **Process Management**: Proper server process handling
- **Graceful Shutdown**: Clean server termination

### HTTP Client Testing
- **WebClient**: Full-featured HTTP client for testing
- **Request Methods**: GET, POST, and other HTTP methods
- **Cookie Handling**: Automatic cookie management
- **Session Management**: Session persistence across requests

### Application Testing
- **End-to-End Workflows**: Complete user workflows
- **Form Submission**: Form data handling and validation
- **Authentication**: User registration and login testing
- **Database Integration**: Database operations through web interface

### Cookie Management
- **Cookie Parsing**: Robust cookie header parsing
- **Multiple Values**: Handling complex cookie values
- **Edge Cases**: Special characters and formatting
- **Session Cookies**: Session management through cookies

## Usage Example
```python
from gluon.contrib.webclient import WebClient
import subprocess
import time

# Manual server testing
def test_web_application():
    # Start web server
    server = subprocess.Popen(['python', 'web2py.py', '-a', 'password'])
    time.sleep(5)  # Wait for startup
    
    try:
        # Test application
        client = WebClient('http://localhost:8000/myapp/default/')
        
        # Test index page
        response = client.get('index')
        assert response.status == 200
        
        # Test form submission
        data = {'name': 'John', 'email': 'john@example.com'}
        response = client.post('register', data=data)
        assert 'registration successful' in response.text
        
        # Test login
        login_data = {'email': 'john@example.com', 'password': 'secret'}
        response = client.post('login', data=login_data)
        assert 'welcome' in response.text.lower()
        
    finally:
        # Stop server
        server.terminate()

# Cookie testing
client = WebClient()
client.headers['set-cookie'] = 'session_id=abc123; path=/'
client._parse_headers_in_cookies()
print(client.cookies['session_id'])  # 'abc123'
```

## Integration with web2py Framework

### Server Integration
- **Built-in Server**: Tests web2py's built-in Rocket server
- **Application Serving**: Multi-application server testing
- **Static Files**: Static file serving verification
- **Error Handling**: Server error response testing

### Authentication System
- **User Registration**: Complete registration workflow testing
- **Login/Logout**: Authentication system verification
- **Session Management**: Session persistence and security
- **Password Handling**: Secure password processing

### Database Integration
- **ORM Testing**: Database operations through web interface
- **Transaction Handling**: Database transaction integrity
- **Data Validation**: Form data validation and processing
- **Error Recovery**: Database error handling

### Development Workflow
- **Live Testing**: Testing against running server
- **Integration Testing**: End-to-end workflow validation
- **Performance Testing**: Server performance under load
- **Debugging**: Live debugging and error investigation

## Test Coverage
- **Server Startup**: Web server initialization and readiness
- **HTTP Handling**: Complete HTTP request-response cycle
- **Cookie Management**: Cookie parsing and handling edge cases
- **User Workflows**: Registration, login, and application usage
- **Error Handling**: Server and application error responses
- **Cross-platform**: Server functionality across platforms

## Expected Results
- **Server Reliability**: Web server should start and run reliably
- **HTTP Compliance**: Proper HTTP protocol implementation
- **Cookie Handling**: Robust cookie parsing and management
- **User Experience**: Smooth user registration and login workflows
- **Performance**: Acceptable response times and resource usage
- **Stability**: Server stability under test conditions

## Test Environment

### Server Configuration
- **Host**: 127.0.0.1 (localhost)
- **Port**: 8000 (default web2py port)
- **Admin Password**: 'testpass' for testing
- **Test Application**: '_test_web' temporary application

### Client Configuration
- **WebClient**: Custom HTTP client for testing
- **Cookie Support**: Automatic cookie handling
- **Session Management**: Persistent session across requests
- **Error Handling**: Proper error response handling

## File Structure
```
gluon/tests/
├── test_web.py           # This file
└── ... (other test files)

applications/_test_web/   # Test application
├── controllers/
├── models/
├── views/
└── ... (application structure)
```

This test suite ensures web2py provides reliable web server functionality with robust HTTP handling, cookie management, and complete application workflow support for production web applications.