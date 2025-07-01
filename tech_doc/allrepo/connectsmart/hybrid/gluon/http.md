# Gluon HTTP Utilities Documentation

## Overview

The `http.py` module provides comprehensive HTTP response handling and status code management for the Gluon web framework. It implements HTTP exception handling, redirect functionality, and standardized response generation with proper header management and status code handling.

## File Location
`/home/datavan/METROPIA/metro_combine/allrepo/connectsmart/hybrid/gluon/http.py`

## Dependencies

### Core Dependencies
- **re**: Regular expression operations for status validation
- **gluon._compat**: Python version compatibility utilities
  - `iteritems`: Dictionary iteration compatibility
  - `to_bytes`: String to bytes conversion
  - `unicodeT`: Unicode type handling

## HTTP Status Codes

### Defined Status Codes
The module maintains a comprehensive dictionary of HTTP status codes with their corresponding reason phrases.

```python
defined_status = {
    # Success codes
    200: "OK",
    201: "CREATED", 
    202: "ACCEPTED",
    203: "NON-AUTHORITATIVE INFORMATION",
    204: "NO CONTENT",
    205: "RESET CONTENT",
    206: "PARTIAL CONTENT",
    
    # Redirection codes
    301: "MOVED PERMANENTLY",
    302: "FOUND",
    303: "SEE OTHER", 
    304: "NOT MODIFIED",
    305: "USE PROXY",
    307: "TEMPORARY REDIRECT",
    
    # Client error codes
    400: "BAD REQUEST",
    401: "UNAUTHORIZED",
    402: "PAYMENT REQUIRED",
    403: "FORBIDDEN",
    404: "NOT FOUND",
    405: "METHOD NOT ALLOWED",
    406: "NOT ACCEPTABLE",
    407: "PROXY AUTHENTICATION REQUIRED",
    408: "REQUEST TIMEOUT",
    409: "CONFLICT",
    410: "GONE",
    411: "LENGTH REQUIRED",
    412: "PRECONDITION FAILED",
    413: "REQUEST ENTITY TOO LARGE",
    414: "REQUEST-URI TOO LONG",
    415: "UNSUPPORTED MEDIA TYPE",
    416: "REQUESTED RANGE NOT SATISFIABLE",
    417: "EXPECTATION FAILED",
    422: "UNPROCESSABLE ENTITY",
    429: "TOO MANY REQUESTS",
    451: "UNAVAILABLE FOR LEGAL REASONS",
    
    # Server error codes
    500: "INTERNAL SERVER ERROR",
    501: "NOT IMPLEMENTED",
    502: "BAD GATEWAY",
    503: "SERVICE UNAVAILABLE",
    504: "GATEWAY TIMEOUT",
    505: "HTTP VERSION NOT SUPPORTED",
    509: "BANDWIDTH LIMIT EXCEEDED",
}
```

### Status Code Validation
```python
regex_status = re.compile("^\d{3} [0-9A-Z ]+$")  # Validates status format
regex_header_newlines = re.compile(r"[\r\n]")    # Removes newlines from headers
```

## HTTP Exception Class

### Core HTTP Class
The `HTTP` class serves as both an exception and a response object, providing comprehensive HTTP response handling.

```python
class HTTP(Exception):
    """
    Raises an HTTP response with proper status codes, headers, and body content
    
    Args:
        status: HTTP status code (integer) or status string
        body: Response body content (string, bytes, or iterable)
        cookies: HTTP cookies to include in response
        **headers: Additional HTTP headers as keyword arguments
    """
```

### Constructor Implementation
```python
def __init__(self, status, body="", cookies=None, **headers):
    self.status = status
    self.body = body
    self.headers = {}
    
    # Process headers with security filtering
    for k, v in iteritems(headers):
        if isinstance(v, list):
            # Handle multiple header values
            self.headers[k] = [
                regex_header_newlines.sub("", str(item)) for item in v
            ]
        elif v is not None:
            # Single header value with newline removal
            self.headers[k] = regex_header_newlines.sub("", str(v))
    
    # Convert cookies to headers
    self.cookies2headers(cookies)
```

### Cookie Handling
```python
def cookies2headers(self, cookies):
    """Convert cookie objects to Set-Cookie headers"""
    if cookies and len(cookies) > 0:
        self.headers["Set-Cookie"] = [
            str(cookie)[11:] for cookie in cookies.values()
        ]
```

### Response Generation
```python
def to(self, responder, env=None):
    """
    Generate WSGI-compatible response
    
    Args:
        responder: WSGI start_response callable
        env: WSGI environment dictionary
    
    Returns:
        Iterable response body
    """
    env = env or {}
    status = self.status
    headers = self.headers
    
    # Format status line
    if status in defined_status:
        status = "%d %s" % (status, defined_status[status])
    elif isinstance(status, int):
        status = "%d UNKNOWN ERROR" % status
    else:
        status = str(status)
        if not regex_status.match(status):
            status = "500 %s" % (defined_status[500])
    
    # Set default content type
    headers.setdefault("Content-Type", "text/html; charset=UTF-8")
    
    # Handle response body
    body = self.body
    if status[:1] == "4":  # Client error responses
        if not body:
            body = status
        if isinstance(body, (str, bytes, bytearray)):
            if isinstance(body, unicodeT):
                body = to_bytes(body)
            headers["Content-Length"] = len(body)
    
    # Format headers for WSGI
    rheaders = []
    for k, v in iteritems(headers):
        if isinstance(v, list):
            rheaders += [(k, str(item)) for item in v]
        else:
            rheaders.append((k, str(v)))
    
    # Call WSGI responder
    responder(status, rheaders)
    
    # Handle HEAD requests
    if env.get("request_method", "") == "HEAD":
        return [to_bytes("")]
    
    # Return response body
    elif isinstance(body, (str, bytes, bytearray)):
        if isinstance(body, unicodeT):
            body = to_bytes(body)
        return [body]
    elif hasattr(body, "__iter__"):
        return body
    else:
        body = str(body)
        if isinstance(body, unicodeT):
            body = to_bytes(body)
        return [body]
```

### Error Message Composition
```python
@property
def message(self):
    """
    Compose descriptive error message
    Format: "status defined_status [web2py_error]"
    """
    msg = "%(status)s"
    if self.status in defined_status:
        msg = "%(status)s %(defined_status)s"
    if "web2py_error" in self.headers:
        msg += " [%(web2py_error)s]"
    
    return msg % dict(
        status=self.status,
        defined_status=defined_status.get(self.status),
        web2py_error=self.headers.get("web2py_error"),
    )

def __str__(self):
    """String representation of HTTP exception"""
    return self.message
```

## Redirect Functionality

### Redirect Function
Comprehensive redirect handling with support for different redirect types and client-side redirects.

```python
def redirect(location="", how=303, client_side=False, headers=None):
    """
    Raises a redirect response
    
    Args:
        location: Target URL for redirection
        how: HTTP status code for redirect (default: 303 See Other)
        client_side: Enable client-side redirect for AJAX requests
        headers: Additional headers to include in response
    """
    headers = headers or {}
    
    if location:
        from gluon.globals import current
        
        # URL encode newlines for security
        loc = location.replace("\r", "%0D").replace("\n", "%0A")
        
        if client_side and current.request.ajax:
            # AJAX client-side redirect
            headers["web2py-redirect-location"] = loc
            raise HTTP(200, **headers)
        else:
            # Standard HTTP redirect
            headers["Location"] = loc
            raise HTTP(
                how, 
                'You are being redirected <a href="%s">here</a>' % loc, 
                **headers
            )
    else:
        from gluon.globals import current
        
        if client_side and current.request.ajax:
            # AJAX page reload
            headers["web2py-component-command"] = "window.location.reload(true)"
            raise HTTP(200, **headers)
```

## Security Features

### Header Security
1. **Newline Filtering**: Removes newlines from headers to prevent header injection
2. **URL Encoding**: Encodes control characters in redirect URLs
3. **AJAX Detection**: Handles AJAX requests with appropriate headers

### Header Injection Prevention
```python
# Remove newlines from all header values
regex_header_newlines.sub("", str(v))

# URL encoding for redirect security
loc = location.replace("\r", "%0D").replace("\n", "%0A")
```

## Usage Patterns

### Basic HTTP Exceptions
```python
# Simple error responses
raise HTTP(404, "Page not found")
raise HTTP(403, "Access denied")
raise HTTP(500, "Internal server error")

# Custom error with headers
raise HTTP(400, "Bad request", **{"X-Error-Code": "INVALID_INPUT"})
```

### Redirect Examples
```python
# Simple redirect
redirect("http://example.com")

# Permanent redirect
redirect("http://example.com", how=301)

# Client-side redirect for AJAX
redirect("http://example.com", client_side=True)

# Conditional redirect
if not user.is_authenticated:
    redirect(URL('auth', 'login'))
```

### Custom Status Codes
```python
# Custom status with message
raise HTTP("299 Custom Status", "Custom response body")

# Status code with custom headers
raise HTTP(422, "Validation failed", **{
    "X-Validation-Error": "email_invalid",
    "Content-Type": "application/json"
})
```

## Advanced Features

### AJAX Integration
The module provides special handling for AJAX requests:

```python
# Check for AJAX requests
if current.request.ajax:
    # Return AJAX-specific response
    headers["web2py-redirect-location"] = url
    raise HTTP(200, **headers)
```

### Custom Response Bodies
```python
# String response
raise HTTP(200, "Hello, World!")

# JSON response
import json
data = {"message": "Success", "code": 200}
raise HTTP(200, json.dumps(data), **{"Content-Type": "application/json"})

# Binary response
with open("image.png", "rb") as f:
    raise HTTP(200, f.read(), **{"Content-Type": "image/png"})

# Streaming response
def generate_data():
    for i in range(1000):
        yield f"Line {i}\n"

raise HTTP(200, generate_data(), **{"Content-Type": "text/plain"})
```

### Error Handling Patterns
```python
# Controller error handling
def my_controller():
    try:
        # Application logic
        result = process_request()
        return dict(result=result)
    except ValidationError as e:
        raise HTTP(400, str(e))
    except PermissionError as e:
        raise HTTP(403, "Access denied")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise HTTP(500, "Internal server error")
```

## Content Type Handling

### Automatic Content-Type Setting
```python
# Default content type
headers.setdefault("Content-Type", "text/html; charset=UTF-8")

# JSON responses
raise HTTP(200, json_data, **{"Content-Type": "application/json"})

# XML responses  
raise HTTP(200, xml_data, **{"Content-Type": "application/xml"})

# Plain text responses
raise HTTP(200, text_data, **{"Content-Type": "text/plain"})
```

### Content-Length Calculation
```python
# Automatic content length for error responses
if status[:1] == "4":  # Client errors
    if isinstance(body, (str, bytes, bytearray)):
        if isinstance(body, unicodeT):
            body = to_bytes(body)
        headers["Content-Length"] = len(body)
```

## Integration Examples

### Web2py/Gluon Integration
```python
# In controllers
def index():
    if not auth.is_logged_in():
        redirect(URL('default', 'user', args='login'))
    
    try:
        data = get_user_data()
        return dict(data=data)
    except DataNotFound:
        raise HTTP(404, "Data not found")

# API endpoints
def api():
    try:
        result = process_api_request()
        response.headers['Content-Type'] = 'application/json'
        return json.dumps(result)
    except APIError as e:
        raise HTTP(400, json.dumps({"error": str(e)}))
```

### Middleware Integration
```python
# Custom middleware using HTTP exceptions
class AuthMiddleware:
    def __init__(self, app):
        self.app = app
    
    def __call__(self, environ, start_response):
        if not self.check_auth(environ):
            http_exc = HTTP(401, "Unauthorized")
            return http_exc.to(start_response, environ)
        return self.app(environ, start_response)
```

## Performance Considerations

### Response Optimization
1. **Content-Length**: Automatically set for measurable content
2. **Header Efficiency**: Minimize header processing overhead
3. **Body Handling**: Support for streaming responses
4. **Memory Management**: Efficient handling of large responses

### Caching Integration
```python
# Cache-aware redirects
def cached_redirect(url, cache_time=3600):
    headers = {
        "Cache-Control": f"max-age={cache_time}",
        "Expires": (datetime.now() + timedelta(seconds=cache_time)).strftime("%a, %d %b %Y %H:%M:%S GMT")
    }
    redirect(url, headers=headers)
```

## Best Practices

### Error Handling
1. **Consistent Status Codes**: Use appropriate HTTP status codes
2. **Meaningful Messages**: Provide helpful error messages
3. **Security Awareness**: Avoid leaking sensitive information
4. **Logging**: Log errors appropriately for debugging

### Redirect Handling
1. **Secure Redirects**: Validate redirect URLs
2. **AJAX Awareness**: Handle AJAX requests appropriately
3. **Status Code Selection**: Use correct redirect status codes
4. **User Experience**: Provide fallback for JavaScript-disabled clients

### Header Management
1. **Security Headers**: Include appropriate security headers
2. **Content Types**: Set correct content types
3. **Caching**: Use appropriate cache headers
4. **Encoding**: Handle character encoding properly

## Debugging and Troubleshooting

### Common Issues
1. **Status Code Errors**: Verify status codes are properly formatted
2. **Header Injection**: Check for newlines in header values
3. **Redirect Loops**: Validate redirect logic
4. **Content Type Mismatches**: Ensure proper content type headers

### Debugging Techniques
```python
# Debug HTTP responses
try:
    raise HTTP(404, "Debug message")
except HTTP as e:
    print(f"Status: {e.status}")
    print(f"Headers: {e.headers}")
    print(f"Body: {e.body}")
    print(f"Message: {e.message}")
```

This HTTP utilities module provides a robust foundation for HTTP response handling, error management, and redirect functionality essential for web application development in the Gluon framework.