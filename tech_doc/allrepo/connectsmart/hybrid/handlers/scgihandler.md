# SCGI Handler Documentation

## Overview

The `scgihandler.py` module provides a Simple Common Gateway Interface (SCGI) handler for deploying web2py applications with high-performance web servers like Lighttpd. SCGI is a protocol for interfacing external applications with web servers, offering better performance than traditional CGI.

## Purpose

This handler enables web2py applications to run efficiently behind SCGI-compatible web servers by:
- Implementing SCGI protocol for web server communication
- Providing asynchronous request processing capabilities
- Supporting connection pooling and process reuse
- Offering GZIP compression middleware integration
- Enabling high-performance deployment scenarios

## Protocol Architecture

### SCGI Protocol Benefits

SCGI offers several advantages over traditional CGI:
- **Persistent Processes**: Eliminates process creation overhead
- **Connection Pooling**: Reuses connections for multiple requests
- **Reduced Latency**: Faster request processing and response times
- **Better Resource Utilization**: More efficient memory and CPU usage
- **Scalability**: Handles higher concurrent request loads

### Communication Flow

```
Web Server → SCGI Protocol → Python Handler → WSGI App → web2py
```

## Configuration

### Lighttpd Configuration

Add the following to your `lighttpd.conf`:

```lighttpd
server.document-root = "/var/www/web2py/"
# For Linux 2.6+
server.event-handler = "linux-sysepoll"

url.rewrite-once = (
    "^(/.+?/static/.+)$" => "/applications$1",
    "(^|/.*)$" => "/handler_web2py.scgi$1",
)

scgi.server = ( "/handler_web2py.scgi" =>
    ("handler_web2py" =>
        ( "host" => "127.0.0.1",
          "port" => "4000",
          "check-local" => "disable",
        )
    )
)
```

**Configuration Elements:**
- **document-root**: Web2py installation directory
- **event-handler**: High-performance event handling (Linux)
- **url.rewrite-once**: URL rewriting rules for static content and dynamic requests
- **scgi.server**: SCGI server configuration with host and port

### Advanced Lighttpd Configuration

```lighttpd
# Performance optimizations
server.max-connections = 1024
server.max-fds = 2048
server.max-worker = 8

# SCGI pool configuration
scgi.server = ( "/handler_web2py.scgi" =>
    (
        "web2py-scgi-1" => (
            "host" => "127.0.0.1",
            "port" => "4000",
            "check-local" => "disable",
            "max-procs" => 4,
            "idle-timeout" => 20,
        ),
        "web2py-scgi-2" => (
            "host" => "127.0.0.1", 
            "port" => "4001",
            "check-local" => "disable",
            "max-procs" => 4,
            "idle-timeout" => 20,
        )
    )
)
```

## Handler Implementation

### Server Selection

The handler supports multiple SCGI server implementations:

```python
# Option 1: Paste SCGI server (commented out)
#import paste.util.scgiserver as scgi
#scgi.serve_application(application, '', 4000).run()

# Option 2: WSGITools SCGI server (active)
from wsgitools.scgi.forkpool import SCGIServer
SCGIServer(application, port=4000).enable_sighandler().run()
```

### WSGI Middleware Integration

The handler incorporates WSGI middleware for enhanced functionality:

```python
from wsgitools.filters import WSGIFilterMiddleware, GzipWSGIFilter

wsgiapp = WSGIFilterMiddleware(gluon.main.wsgibase, GzipWSGIFilter)
```

**Middleware Features:**
- **GzipWSGIFilter**: Automatic response compression
- **WSGIFilterMiddleware**: Extensible middleware framework
- **Performance Enhancement**: Reduced bandwidth usage
- **Transparent Operation**: No application code changes required

### Logging Configuration

Optional logging support for monitoring and debugging:

```python
LOGGING = False  # Set to True for production monitoring

if LOGGING:
    application = gluon.main.appfactory(
        wsgiapp=wsgiapp,
        logfilename='httpserver.log',
        profiler_dir=None
    )
else:
    application = wsgiapp
```

### Soft Cron Integration

Optional soft cron support for background tasks:

```python
SOFTCRON = False  # Set to True to enable soft cron

if SOFTCRON:
    global_settings.web2py_crontype = 'soft'
```

## Deployment Scenarios

### Production Deployment

1. **Install Dependencies**:
   ```bash
   pip install wsgitools
   # or
   pip install paste
   ```

2. **Configure Handler**:
   ```python
   # Edit configuration constants
   LOGGING = True
   SOFTCRON = True
   ```

3. **Start SCGI Server**:
   ```bash
   python scgihandler.py
   ```

4. **Configure Web Server**: Update lighttpd.conf with SCGI settings

### Development Environment

```python
# Development configuration
LOGGING = True   # Enable detailed logging
SOFTCRON = False # Disable cron for development

# Use development server
from wsgitools.scgi.forkpool import SCGIServer
server = SCGIServer(application, port=4000, debug=True)
server.enable_sighandler().run()
```

## Performance Optimization

### Fork Pool Configuration

The SCGIServer uses a fork pool for handling concurrent requests:

```python
# Advanced fork pool configuration
server = SCGIServer(
    application,
    port=4000,
    max_children=10,    # Maximum child processes
    min_children=2,     # Minimum child processes
    max_requests=1000,  # Requests per child before recycling
    timeout=30          # Request timeout in seconds
)
```

### Memory Management

- **Process Recycling**: Child processes recycled after handling specified requests
- **Memory Monitoring**: Automatic cleanup of memory-intensive processes
- **Resource Limits**: Configurable resource limits per process
- **Garbage Collection**: Explicit garbage collection in long-running processes

### Connection Pooling

SCGI protocol inherently supports connection reuse:

```python
# Connection pool benefits
# - Reduced TCP connection overhead
# - Faster request processing
# - Better resource utilization
# - Improved scalability
```

## Security Considerations

### Network Security

```lighttpd
# Restrict SCGI access
scgi.server = ( "/handler_web2py.scgi" =>
    ("handler_web2py" =>
        ( "host" => "127.0.0.1",  # Local access only
          "port" => "4000",
          "check-local" => "disable",
          "allow-x-send-file" => "disable",  # Security
        )
    )
)
```

### Process Security

- **User Isolation**: Run SCGI processes under restricted user account
- **File Permissions**: Limit file system access to necessary directories
- **Process Limits**: Configure appropriate process and resource limits
- **Signal Handling**: Proper signal handling for graceful shutdown

### Request Validation

- **Input Sanitization**: Validate all incoming request data
- **Header Validation**: Check request headers for malicious content
- **Size Limits**: Configure maximum request size limits
- **Rate Limiting**: Implement request rate limiting

## Monitoring and Debugging

### Logging Configuration

```python
import logging

# Configure detailed logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('scgi.log'),
        logging.StreamHandler()
    ]
)
```

### Performance Monitoring

```python
import time
import psutil

# Monitor process performance
def monitor_performance():
    process = psutil.Process()
    cpu_percent = process.cpu_percent()
    memory_info = process.memory_info()
    
    logging.info(f"CPU: {cpu_percent}%, Memory: {memory_info.rss / 1024 / 1024:.1f}MB")
```

### Health Checks

```python
# Health check endpoint
def health_check(environ, start_response):
    if environ['PATH_INFO'] == '/health':
        start_response('200 OK', [('Content-Type', 'text/plain')])
        return [b'OK']
    return application(environ, start_response)
```

## Error Handling

### Exception Management

```python
import traceback

def error_handler(application):
    def wrapper(environ, start_response):
        try:
            return application(environ, start_response)
        except Exception as e:
            logging.error(f"Application error: {e}")
            logging.error(traceback.format_exc())
            start_response('500 Internal Server Error', 
                         [('Content-Type', 'text/plain')])
            return [b'Internal Server Error']
    return wrapper

# Wrap application with error handler
application = error_handler(application)
```

### Common Issues

1. **Port Conflicts**: Ensure SCGI port is available
2. **Permission Errors**: Check file and directory permissions
3. **Dependency Issues**: Verify wsgitools or paste installation
4. **Configuration Errors**: Validate lighttpd configuration syntax

## Advanced Features

### Custom Middleware

```python
class CustomMiddleware:
    def __init__(self, application):
        self.application = application
    
    def __call__(self, environ, start_response):
        # Pre-processing
        start_time = time.time()
        
        # Execute application
        result = self.application(environ, start_response)
        
        # Post-processing
        duration = time.time() - start_time
        logging.info(f"Request processed in {duration:.3f}s")
        
        return result

# Apply custom middleware
application = CustomMiddleware(application)
```

### Load Balancing

```lighttpd
# Multiple SCGI backends for load balancing
scgi.server = ( "/handler_web2py.scgi" =>
    (
        "backend1" => ( "host" => "127.0.0.1", "port" => "4000" ),
        "backend2" => ( "host" => "127.0.0.1", "port" => "4001" ),
        "backend3" => ( "host" => "127.0.0.1", "port" => "4002" ),
    )
)
```

This SCGI handler provides a high-performance deployment solution for web2py applications, offering excellent scalability and resource efficiency through the SCGI protocol while maintaining compatibility with modern web server architectures.