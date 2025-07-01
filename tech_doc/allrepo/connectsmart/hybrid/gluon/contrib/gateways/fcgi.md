# FastCGI Gateway Module

## Overview
This module implements a FastCGI/WSGI gateway for web2py, providing FastCGI protocol support for high-performance web applications. It's based on Allan Saddi's fcgi module and has been modified for web2py compatibility.

## Key Features
- **FastCGI Protocol Implementation**: Complete FastCGI 1.0 protocol support
- **WSGI Gateway**: Web Server Gateway Interface compatibility
- **Multi-threading Support**: Handles multiple concurrent requests
- **CGI Fallback**: Automatic fallback to CGI mode when not in FastCGI context
- **Connection Management**: Efficient socket and connection handling

## Core Classes

### WSGIServer
Main FastCGI server class that supports the Web Server Gateway Interface.

**Parameters:**
- `application`: WSGI application callable
- `environ`: Additional environment variables (optional)
- `multithreaded`: Enable multi-threading support (default: True)
- `maxwrite`: Maximum bytes per record (default: 8192)
- `bindAddress`: Socket binding address (optional)
- `multiplexed`: Handle multiple requests per connection (default: False)

### Connection Classes
- **Connection**: Basic FastCGI connection handler
- **MultiplexedConnection**: Thread-safe connection for multiple simultaneous requests

### Stream Classes
- **InputStream**: FastCGI input stream (FCGI_STDIN/FCGI_DATA)
- **OutputStream**: FastCGI output stream (FCGI_STDOUT/FCGI_STDERR)
- **MultiplexedInputStream**: Thread-safe input stream for multiplexed connections

## Protocol Constants
The module defines all FastCGI protocol constants including:
- **Record Types**: FCGI_BEGIN_REQUEST, FCGI_PARAMS, FCGI_STDIN, etc.
- **Roles**: FCGI_RESPONDER, FCGI_AUTHORIZER, FCGI_FILTER
- **Status Codes**: FCGI_REQUEST_COMPLETE, FCGI_CANT_MPX_CONN, etc.

## Usage Example

### Basic WSGI Application
```python
#!/usr/bin/env python
from myapplication import app  # Your WSGI application
from fcgi import WSGIServer

# Start FastCGI server
WSGIServer(app).run()
```

### Advanced Configuration
```python
from fcgi import WSGIServer

# Configure with custom settings
server = WSGIServer(
    application=my_app,
    environ={'APP_MODE': 'production'},
    multithreaded=True,
    multiplexed=True,
    maxwrite=16384
)

# Run with timeout
server.run(timeout=5.0)
```

## Environment Variables
- **FCGI_FORCE_CGI**: Set to "Y" to force CGI mode
- **FCGI_WEB_SERVER_ADDRS**: Comma-separated list of allowed web server addresses

## Threading Considerations
- **Single-threaded**: Use `multithreaded=False` for non-thread-safe applications
- **Multiplexed**: Enable for handling multiple requests per connection
- **Thread Safety**: MultiplexedConnection provides thread-safe request handling

## Error Handling
- **Exception Handling**: Automatic error page generation using cgitb
- **Socket Errors**: Graceful handling of connection failures
- **Protocol Errors**: Proper FastCGI error responses

## Performance Features
- **Buffer Management**: Efficient memory usage with configurable thresholds
- **Connection Pooling**: Reuses connections when possible
- **Signal Handling**: Proper cleanup on SIGHUP, SIGINT, SIGTERM

## Debugging
Enable debugging by setting:
```python
if __debug__:
    DEBUG = 1  # Set debug level (0-9)
    DEBUGLOG = '/tmp/fcgi.log'  # Debug log file
```

## Compatibility
- **Python 2/3**: Compatible with both Python versions
- **Web Servers**: Works with Apache mod_fastcgi, nginx, lighttpd
- **WSGI**: Full WSGI 1.0 specification compliance

## Integration with web2py
This module is specifically modified for web2py integration and provides the foundation for deploying web2py applications in FastCGI environments for improved performance over standard CGI.