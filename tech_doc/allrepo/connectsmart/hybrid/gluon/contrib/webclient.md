# Gluon Contrib WebClient Module

## Overview
HTTP client library for web2py applications providing simplified web scraping, testing, and automation capabilities. Built on top of urllib2 with enhanced features for handling web2py-specific elements like forms, sessions, and CSRF protection.

## Module Information
- **Module**: `gluon.contrib.webclient`
- **Author**: Massimo Di Pierro
- **License**: LGPL (web2py license)
- **Dependencies**: `urllib2`, `cookielib`, `re`
- **Purpose**: HTTP client for testing and automation

## Key Features
- **Web2py Integration**: Automatic handling of formkeys and formnames
- **Session Management**: Cookie-based session handling
- **CSRF Protection**: Automatic web2py CSRF token handling
- **Basic Authentication**: Built-in HTTP basic auth support
- **Form Postback**: Intelligent form submission with postback detection
- **History Tracking**: Request history for debugging and analysis

## Main Class

### WebClient
Primary HTTP client class with web2py-specific enhancements.

**Constructor:**
```python
def __init__(self, app='', postbacks=True, default_headers=DEFAULT_HEADERS, 
             session_regex=SESSION_REGEX)
```

**Parameters:**
- `app`: Base application URL
- `postbacks`: Enable automatic postback handling (default: True)
- `default_headers`: Default HTTP headers
- `session_regex`: Regex pattern for session detection

## Core Methods

### get()
Perform HTTP GET request.

**Signature:**
```python
def get(self, url, cookies=None, headers=None, auth=None)
```

**Parameters:**
- `url`: Request URL (relative to app base)
- `cookies`: Custom cookies dictionary
- `headers`: Custom headers dictionary
- `auth`: Authentication credentials

### post()
Perform HTTP POST request with automatic form handling.

**Signature:**
```python
def post(self, url, data=None, cookies=None, headers=None, auth=None, 
         method='auto', charset='utf-8')
```

**Features:**
- Automatic CSRF token extraction and submission
- Form postback detection and handling
- Session cookie management
- Authentication support

## Usage Examples

### Basic HTTP Testing
```python
from gluon.contrib.webclient import WebClient

# Initialize client
client = WebClient(app='http://localhost:8000/myapp')

# Simple GET request
response = client.get('/default/index')
print("Status:", response['status'])
print("Body:", response['body'])

# POST request
data = {'name': 'John', 'email': 'john@example.com'}
response = client.post('/default/submit', data=data)
```

### Web2py Form Testing
```python
# Test web2py form submission
client = WebClient(app='http://localhost:8000/myapp')

# Get form page (extracts formkey automatically)
response = client.get('/default/contact')

# Submit form (formkey included automatically)
form_data = {
    'name': 'Test User',
    'email': 'test@example.com',
    'message': 'Test message',
    '_formname': 'contact_form'
}

response = client.post('/default/contact', data=form_data)

# Check for success
if 'Thank you' in response['body']:
    print("Form submitted successfully")
```

### Authentication Testing
```python
# Test with basic authentication
auth_data = {
    'realm': 'Protected Area',
    'uri': 'http://localhost:8000',
    'user': 'admin',
    'passwd': 'password'
}

client = WebClient()
response = client.get('/admin/default/index', auth=auth_data)
```

### Session Testing
```python
# Test session-based functionality
client = WebClient(app='http://localhost:8000/myapp')

# Login to create session
login_data = {
    'email': 'user@example.com',
    'password': 'userpass',
    '_formname': 'auth_login'
}

response = client.post('/default/user/login', data=login_data)

# Access protected page using session
response = client.get('/default/protected')

# Check session cookies
print("Session cookies:", client.cookies)
```

## Advanced Features

### Custom Headers
```python
custom_headers = {
    'User-Agent': 'MyBot/1.0',
    'Accept': 'application/json',
    'X-Custom-Header': 'CustomValue'
}

client = WebClient(default_headers=custom_headers)
response = client.get('/api/data')
```

### Cookie Management
```python
# Manual cookie handling
custom_cookies = {
    'session_id': 'abc123',
    'user_pref': 'theme_dark'
}

response = client.get('/default/index', cookies=custom_cookies)

# Access response cookies
print("Response cookies:", client.cookies)
```

### Form Automation
```python
def automate_form_submission(client, form_url, form_data, form_name):
    """Automate web2py form submission with error handling"""
    
    # Get form page to extract tokens
    response = client.get(form_url)
    
    if response['status'] != 200:
        return False, "Failed to load form page"
    
    # Add form identification
    form_data['_formname'] = form_name
    
    # Submit form
    response = client.post(form_url, data=form_data)
    
    # Check for web2py error ticket
    if 'ticket' in response['body']:
        return False, "Web2py error ticket generated"
    
    # Check for form errors
    if 'error' in response['body'].lower():
        return False, "Form validation errors"
    
    return True, "Form submitted successfully"

# Usage
client = WebClient(app='http://localhost:8000/myapp')
success, message = automate_form_submission(
    client, 
    '/default/register',
    {'name': 'John', 'email': 'john@example.com'},
    'register_form'
)
```

## Testing Utilities

### Automated Testing
```python
class WebAppTester:
    def __init__(self, app_url):
        self.client = WebClient(app=app_url)
        self.test_results = []
    
    def test_page(self, url, expected_status=200, expected_content=None):
        """Test single page"""
        response = self.client.get(url)
        
        # Check status code
        status_ok = response['status'] == expected_status
        
        # Check content if specified
        content_ok = True
        if expected_content:
            content_ok = expected_content in response['body']
        
        result = {
            'url': url,
            'status_ok': status_ok,
            'content_ok': content_ok,
            'actual_status': response['status']
        }
        
        self.test_results.append(result)
        return status_ok and content_ok
    
    def test_form_submission(self, form_url, form_data, form_name, 
                           success_indicator):
        """Test form submission"""
        # Get form page
        self.client.get(form_url)
        
        # Submit form
        form_data['_formname'] = form_name
        response = self.client.post(form_url, data=form_data)
        
        # Check for success
        success = success_indicator in response['body']
        
        self.test_results.append({
            'type': 'form_submission',
            'url': form_url,
            'success': success
        })
        
        return success
    
    def run_smoke_tests(self, urls):
        """Run smoke tests on multiple URLs"""
        for url in urls:
            self.test_page(url)
        
        return self.test_results

# Usage
tester = WebAppTester('http://localhost:8000/myapp')
results = tester.run_smoke_tests([
    '/default/index',
    '/default/about',
    '/default/contact'
])
```

### Performance Testing
```python
import time

def performance_test(client, url, iterations=10):
    """Simple performance testing"""
    times = []
    
    for i in range(iterations):
        start_time = time.time()
        response = client.get(url)
        end_time = time.time()
        
        if response['status'] == 200:
            times.append(end_time - start_time)
    
    if times:
        avg_time = sum(times) / len(times)
        min_time = min(times)
        max_time = max(times)
        
        return {
            'avg_response_time': avg_time,
            'min_response_time': min_time,
            'max_response_time': max_time,
            'successful_requests': len(times)
        }
    
    return None

# Usage
client = WebClient(app='http://localhost:8000/myapp')
perf_results = performance_test(client, '/default/index')
print(f"Average response time: {perf_results['avg_response_time']:.3f}s")
```

## Error Handling

### Response Validation
```python
def validate_response(response, expected_patterns=None, forbidden_patterns=None):
    """Validate HTTP response"""
    errors = []
    
    # Check status code
    if response['status'] >= 400:
        errors.append(f"HTTP error: {response['status']}")
    
    # Check for expected content
    if expected_patterns:
        for pattern in expected_patterns:
            if pattern not in response['body']:
                errors.append(f"Missing expected content: {pattern}")
    
    # Check for forbidden content
    if forbidden_patterns:
        for pattern in forbidden_patterns:
            if pattern in response['body']:
                errors.append(f"Found forbidden content: {pattern}")
    
    return len(errors) == 0, errors

# Usage
response = client.get('/default/index')
is_valid, errors = validate_response(
    response,
    expected_patterns=['Welcome', 'Home'],
    forbidden_patterns=['Error', 'Exception']
)
```

### Exception Handling
```python
def safe_request(client, method, url, **kwargs):
    """Make HTTP request with error handling"""
    try:
        if method.upper() == 'GET':
            response = client.get(url, **kwargs)
        else:
            response = client.post(url, **kwargs)
        
        return True, response
    
    except Exception as e:
        return False, str(e)

# Usage
success, result = safe_request(client, 'GET', '/default/index')
if success:
    print("Request successful")
else:
    print(f"Request failed: {result}")
```

## Integration Patterns

### CI/CD Testing
```python
def run_integration_tests():
    """Run integration tests for CI/CD pipeline"""
    client = WebClient(app=os.environ.get('TEST_APP_URL'))
    
    tests = [
        ('homepage', '/default/index', 200),
        ('about_page', '/default/about', 200),
        ('api_health', '/api/health', 200),
        ('nonexistent', '/default/missing', 404)
    ]
    
    results = []
    for test_name, url, expected_status in tests:
        response = client.get(url)
        passed = response['status'] == expected_status
        results.append((test_name, passed))
    
    # Return exit code for CI/CD
    all_passed = all(result[1] for result in results)
    return 0 if all_passed else 1
```

### Load Testing Preparation
```python
def generate_test_data():
    """Generate test data for load testing"""
    client = WebClient(app='http://localhost:8000/myapp')
    
    # Create test users
    for i in range(100):
        user_data = {
            'first_name': f'User{i}',
            'last_name': f'Test{i}',
            'email': f'user{i}@test.com',
            '_formname': 'user_registration'
        }
        
        response = client.post('/default/register', data=user_data)
        print(f"Created user {i}: {response['status']}")
```

This module provides comprehensive HTTP client capabilities specifically tailored for web2py applications, making it invaluable for testing, automation, and integration scenarios.