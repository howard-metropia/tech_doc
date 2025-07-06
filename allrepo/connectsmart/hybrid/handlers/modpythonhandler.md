# Mod_Python Handler Documentation

## Overview

The `modpythonhandler.py` module provides a comprehensive WSGI-compliant handler for deploying web2py applications on Apache HTTP Server using mod_python. This handler bridges the gap between Apache's mod_python interface and Python WSGI applications.

## Purpose

This handler enables web2py applications to run efficiently on Apache servers by:
- Implementing WSGI protocol for mod_python integration
- Providing thread-safe request processing
- Supporting both threaded and forked Apache configurations
- Handling CGI environment variable mapping
- Managing request/response lifecycle

## Architecture

### Core Components

The handler consists of several key classes and functions:

1. **InputWrapper**: Manages request input stream
2. **ErrorWrapper**: Handles error logging and output
3. **Handler**: Main WSGI handler implementation
4. **handler()**: Entry point function for mod_python

### Request Processing Flow

```
Apache Request → mod_python → Handler → WSGI App → web2py → Response
```

## Class Definitions

### InputWrapper Class

Wraps mod_python request input for WSGI compatibility:

```python
class InputWrapper(object):
    def __init__(self, req):
        self.req = req
    
    def read(self, size=-1):
        return self.req.read(size)
    
    def readline(self, size=-1):
        return self.req.readline(size)
    
    def __iter__(self):
        # Generator for line-by-line reading
```

**Key Features:**
- **Stream Interface**: Implements standard Python file-like interface
- **Buffered Reading**: Supports both sized and unlimited reads
- **Iterator Protocol**: Enables line-by-line processing
- **Memory Efficient**: Lazy loading of request data

### ErrorWrapper Class

Manages error output and logging integration:

```python
class ErrorWrapper(object):
    def __init__(self, req):
        self.req = req
    
    def write(self, msg):
        self.req.log_error(msg)
    
    def writelines(self, seq):
        self.write(''.join(seq))
```

**Functionality:**
- **Apache Integration**: Direct integration with Apache error logging
- **Standard Interface**: Compatible with Python file-like objects
- **Batch Writing**: Support for multiple line writes
- **Error Propagation**: Ensures errors reach Apache logs

### Handler Class

The main WSGI handler implementation:

```python
class Handler:
    def __init__(self, req):
        # Initialize environment and configuration
        
    def run(self, application):
        # Execute WSGI application
        
    def start_response(self, status, headers, exc_info=None):
        # WSGI start_response callable
        
    def write(self, data):
        # Write response data
```

## Configuration

### Apache Configuration

Add the following to your Apache configuration:

```apache
<Location /myapp>
    SetHandler python-program
    PythonHandler modpythonhandler
    PythonPath "['/path/to/web2py/'] + sys.path"
    PythonOption SCRIPT_NAME /myapp
</Location>
```

**Configuration Options:**
- **PythonHandler**: Specifies the handler module
- **PythonPath**: Adds web2py directory to Python path
- **PythonOption SCRIPT_NAME**: Sets application root URL
- **SetHandler**: Configures Apache to use mod_python

### Advanced Configuration

```apache
<Location /web2py>
    SetHandler python-program
    PythonHandler modpythonhandler
    PythonPath "['/var/www/web2py/'] + sys.path"
    PythonOption SCRIPT_NAME /web2py
    PythonOption multithread off
    PythonOption multiprocess on
    PythonDebug On
</Location>
```

**Advanced Options:**
- **multithread**: Enable/disable threading support
- **multiprocess**: Enable/disable process forking
- **PythonDebug**: Enable debugging mode
- **PythonAutoReload**: Auto-reload modules on changes

## Environment Setup

### WSGI Environment Construction

The handler creates a complete WSGI environment:

```python
env = dict(apache.build_cgi_env(req))
env['wsgi.input'] = InputWrapper(req)
env['wsgi.errors'] = ErrorWrapper(req)
env['wsgi.version'] = (1, 0)
env['wsgi.run_once'] = False
env['wsgi.url_scheme'] = 'https' if env.get('HTTPS') else 'http'
env['wsgi.multithread'] = threaded
env['wsgi.multiprocess'] = forked
```

**Environment Variables:**
- **Standard CGI**: All standard CGI environment variables
- **WSGI Specific**: Required WSGI environment variables
- **Apache Specific**: mod_python specific variables
- **Security Context**: HTTPS detection and URL scheme setting

### Threading Detection

Automatic detection of Apache threading configuration:

```python
try:
    q = apache.mpm_query
    threaded = q(apache.AP_MPMQ_IS_THREADED)
    forked = q(apache.AP_MPMQ_IS_FORKED)
except AttributeError:
    # Fallback to manual configuration
    threaded = options.get('multithread', '').lower() == 'on'
    forked = options.get('multiprocess', '').lower() == 'on'
```

## Request Processing

### Application Execution

The `run()` method executes the WSGI application:

```python
def run(self, application):
    try:
        result = application(self.environ, self.start_response)
        for data in result:
            self.write(data)
        if not self.started:
            self.request.set_content_length(0)
        if hasattr(result, 'close'):
            result.close()
    except:
        # Error handling and 500 response
```

**Execution Flow:**
1. **Application Invocation**: Call WSGI application with environment
2. **Response Iteration**: Process response iterator
3. **Data Writing**: Write response data to Apache
4. **Content Length**: Set content length if not started
5. **Cleanup**: Close response iterator if closeable

### Response Handling

The `start_response()` method handles WSGI response initialization:

```python
def start_response(self, status, headers, exc_info=None):
    if exc_info:
        # Handle exception information
    
    self.request.status = int(status[:3])
    
    for (key, val) in headers:
        if key.lower() == 'content-length':
            self.request.set_content_length(int(val))
        elif key.lower() == 'content-type':
            self.request.content_type = val
        else:
            self.request.headers_out.add(key, val)
    
    return self.write
```

## Error Handling

### Exception Management

Comprehensive error handling for production environments:

```python
try:
    result = application(self.environ, self.start_response)
    # ... processing
except:
    traceback.print_exc(None, self.environ['wsgi.errors'])
    if not self.started:
        self.request.status = 500
        self.request.content_type = 'text/plain'
        data = 'A server error occurred. Please contact the administrator.'
        self.request.set_content_length(len(data))
        self.request.write(data)
```

**Error Features:**
- **Exception Logging**: Full traceback logging to Apache error log
- **Graceful Degradation**: 500 error response for unhandled exceptions
- **Error Isolation**: Prevents application errors from crashing Apache
- **Debug Information**: Detailed error information in development mode

### Common Error Scenarios

1. **Import Errors**: Missing dependencies or Python path issues
2. **Permission Errors**: File system access restrictions
3. **Configuration Errors**: Invalid Apache configuration
4. **Application Errors**: Unhandled exceptions in web2py code

## Performance Optimization

### Memory Management

- **Request Isolation**: Each request processed in separate context
- **Resource Cleanup**: Proper cleanup of request resources
- **Memory Efficiency**: Lazy loading and streaming where possible

### Threading Considerations

```python
# Thread-safe configuration
env['wsgi.multithread'] = threaded
env['wsgi.multiprocess'] = forked

# Appropriate for different Apache MPMs
# - prefork: multiprocess=True, multithread=False
# - worker: multiprocess=True, multithread=True  
# - event: multiprocess=True, multithread=True
```

## Security Features

### Input Validation

- **Request Size Limits**: Apache-level request size enforcement
- **Header Validation**: Automatic header validation by Apache
- **Path Security**: Apache path traversal protection

### Environment Security

- **Variable Sanitization**: Clean environment variable handling
- **Script Name Override**: Secure script name configuration
- **Error Information**: Limited error information exposure

## Deployment Best Practices

### Production Configuration

```apache
<Location /web2py>
    SetHandler python-program
    PythonHandler modpythonhandler
    PythonPath "['/var/www/web2py/'] + sys.path"
    PythonOption SCRIPT_NAME /web2py
    PythonAutoReload Off
    PythonDebug Off
    # Security headers
    Header always set X-Content-Type-Options nosniff
    Header always set X-Frame-Options DENY
</Location>
```

### Monitoring and Logging

- **Apache Error Logs**: Monitor Apache error.log for issues
- **Access Logs**: Track request patterns and performance
- **Application Logs**: Enable web2py application logging
- **Performance Metrics**: Monitor response times and resource usage

### Maintenance

- **Module Reloading**: Configure appropriate reload policies
- **Cache Management**: Implement proper caching strategies
- **Resource Monitoring**: Monitor memory and CPU usage
- **Backup Procedures**: Regular backup of configuration and data

This mod_python handler provides a robust, production-ready solution for deploying web2py applications on Apache HTTP Server with full WSGI compliance and comprehensive error handling.