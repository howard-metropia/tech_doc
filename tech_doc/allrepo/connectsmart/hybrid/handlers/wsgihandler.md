# WSGI Handler Documentation

## Overview

The `wsgihandler.py` module provides a standard WSGI (Web Server Gateway Interface) application handler for web2py applications. This handler serves as the foundation for deploying web2py applications with any WSGI-compliant server, offering maximum compatibility and flexibility.

## Purpose

This handler enables web2py applications to run on any WSGI-compatible server by:
- Implementing the standard WSGI application interface
- Providing configurable logging and monitoring capabilities
- Supporting soft cron functionality for background tasks
- Offering a lightweight, minimal deployment option
- Ensuring compatibility with diverse WSGI server implementations

## Architecture

### WSGI Compliance

The handler creates a standard WSGI application that can be deployed on various servers:

```python
import gluon.main

# Basic WSGI application
application = gluon.main.wsgibase

# Enhanced application with logging
application = gluon.main.appfactory(
    wsgiapp=gluon.main.wsgibase,
    logfilename='httpserver.log',
    profiler_dir=None
)
```

### Deployment Compatibility

Compatible with numerous WSGI servers:
- **Gunicorn**: High-performance Python WSGI server
- **uWSGI**: Feature-rich application server
- **mod_wsgi**: Apache HTTP Server module
- **Waitress**: Production-ready pure Python server
- **Twisted Web**: Event-driven networking engine
- **CherryPy**: Pure Python HTTP server

## Configuration Options

### Basic Configuration

```python
# change these parameters as required
LOGGING = False   # Enable/disable logging
SOFTCRON = False  # Enable/disable soft cron
```

### Logging Configuration

When `LOGGING = True`, the handler creates an enhanced application with:

```python
application = gluon.main.appfactory(
    wsgiapp=gluon.main.wsgibase,
    logfilename='httpserver.log',
    profiler_dir=None
)
```

**Logging Features:**
- **Request Logging**: HTTP request/response logging
- **Error Logging**: Application error tracking
- **Performance Logging**: Response time measurement
- **Access Logging**: User access patterns
- **Debug Information**: Detailed debugging information

### Soft Cron Configuration

When `SOFTCRON = True`, the handler enables background task processing:

```python
if SOFTCRON:
    global_settings.web2py_crontype = 'soft'
```

**Soft Cron Benefits:**
- **Background Tasks**: Execute scheduled tasks within web requests
- **No External Dependencies**: No need for system cron daemon
- **Automatic Execution**: Tasks run automatically with web traffic
- **Simple Configuration**: Easy to enable and configure

## Deployment Examples

### Gunicorn Deployment

```bash
# Basic deployment
gunicorn wsgihandler:application

# Production deployment with workers
gunicorn wsgihandler:application \
    --workers 4 \
    --bind 0.0.0.0:8000 \
    --timeout 30 \
    --keep-alive 2 \
    --max-requests 1000 \
    --max-requests-jitter 100
```

**Gunicorn Configuration File** (`gunicorn.conf.py`):
```python
# Server socket
bind = "0.0.0.0:8000"
backlog = 2048

# Worker processes
workers = 4
worker_class = "sync"
worker_connections = 1000
timeout = 30
keepalive = 2

# Restart workers after handling requests
max_requests = 1000
max_requests_jitter = 100

# Logging
accesslog = "access.log"
errorlog = "error.log"
loglevel = "info"

# Process naming
proc_name = "web2py"

# Server mechanics
daemon = False
pidfile = "web2py.pid"
user = "www-data"
group = "www-data"
tmp_upload_dir = None
```

### uWSGI Deployment

```ini
[uwsgi]
module = wsgihandler:application
master = true
processes = 4
socket = 127.0.0.1:8000
chmod-socket = 666
vacuum = true
die-on-term = true
logto = uwsgi.log
```

**Advanced uWSGI Configuration**:
```ini
[uwsgi]
module = wsgihandler:application
master = true
processes = 4
threads = 2
socket = /tmp/web2py.sock
chmod-socket = 666
vacuum = true
die-on-term = true

# Performance tuning
buffer-size = 32768
post-buffering = 8192
harakiri = 60
max-requests = 5000

# Logging
logto = /var/log/uwsgi/web2py.log
log-maxsize = 20971520
log-backupname = /var/log/uwsgi/web2py.log.old

# Security
uid = www-data
gid = www-data
chdir = /var/www/web2py

# Stats
stats = 127.0.0.1:9191
```

### mod_wsgi Deployment

**Apache Configuration**:
```apache
LoadModule wsgi_module modules/mod_wsgi.so

<VirtualHost *:80>
    ServerName web2py.example.com
    DocumentRoot /var/www/web2py
    
    WSGIDaemonProcess web2py python-path=/var/www/web2py
    WSGIProcessGroup web2py
    WSGIScriptAlias / /var/www/web2py/wsgihandler.py
    
    <Directory /var/www/web2py>
        WSGIApplicationGroup %{GLOBAL}
        Require all granted
    </Directory>
    
    # Static files
    Alias /static /var/www/web2py/applications/*/static
    <Directory /var/www/web2py/applications/*/static>
        Require all granted
    </Directory>
</VirtualHost>
```

### Waitress Deployment

```python
from waitress import serve
from wsgihandler import application

# Development server
serve(application, host='127.0.0.1', port=8000)

# Production server
serve(application, 
      host='0.0.0.0', 
      port=8000,
      threads=6,
      connection_limit=1000,
      cleanup_interval=30)
```

## Performance Optimization

### Production Configuration

```python
# Production optimized settings
LOGGING = True    # Enable production logging
SOFTCRON = True   # Enable background tasks

# Import optimizations
import sys
if hasattr(sys, 'setrecursionlimit'):
    sys.setrecursionlimit(10000)

# Memory optimization
import gc
gc.set_threshold(700, 10, 10)
```

### Caching Integration

```python
# Add caching middleware
from werkzeug.contrib.cache import SimpleCache
cache = SimpleCache()

def cache_middleware(application):
    def wrapper(environ, start_response):
        # Implement caching logic
        return application(environ, start_response)
    return wrapper

application = cache_middleware(application)
```

### Compression Middleware

```python
# Add GZIP compression
from werkzeug.wsgi import gzip

def compressed_app(environ, start_response):
    return gzip(application)(environ, start_response)

application = compressed_app
```

## Monitoring and Observability

### Custom Logging

```python
import logging
import time

class RequestLoggingMiddleware:
    def __init__(self, application):
        self.application = application
        self.logger = logging.getLogger('web2py.requests')
    
    def __call__(self, environ, start_response):
        start_time = time.time()
        
        def log_start_response(status, headers, exc_info=None):
            duration = time.time() - start_time
            self.logger.info(f"{environ['REQUEST_METHOD']} {environ['PATH_INFO']} - {status} - {duration:.3f}s")
            return start_response(status, headers, exc_info)
        
        return self.application(environ, log_start_response)

# Apply logging middleware
application = RequestLoggingMiddleware(application)
```

### Health Checks

```python
def health_check_middleware(application):
    def wrapper(environ, start_response):
        if environ['PATH_INFO'] == '/health':
            start_response('200 OK', [('Content-Type', 'text/plain')])
            return [b'OK']
        elif environ['PATH_INFO'] == '/ready':
            # Check application readiness
            start_response('200 OK', [('Content-Type', 'text/plain')])
            return [b'READY']
        return application(environ, start_response)
    return wrapper

application = health_check_middleware(application)
```

### Metrics Collection

```python
import time
from collections import defaultdict

class MetricsMiddleware:
    def __init__(self, application):
        self.application = application
        self.request_count = 0
        self.response_times = []
        self.status_codes = defaultdict(int)
    
    def __call__(self, environ, start_response):
        start_time = time.time()
        self.request_count += 1
        
        def capture_response(status, headers, exc_info=None):
            duration = time.time() - start_time
            self.response_times.append(duration)
            self.status_codes[status.split()[0]] += 1
            return start_response(status, headers, exc_info)
        
        return self.application(environ, capture_response)
    
    def get_metrics(self):
        return {
            'request_count': self.request_count,
            'avg_response_time': sum(self.response_times) / len(self.response_times) if self.response_times else 0,
            'status_codes': dict(self.status_codes)
        }
```

## Error Handling

### Exception Handling Middleware

```python
import traceback
import logging

def error_handling_middleware(application):
    logger = logging.getLogger('web2py.errors')
    
    def wrapper(environ, start_response):
        try:
            return application(environ, start_response)
        except Exception as e:
            logger.error(f"Application error: {e}")
            logger.error(traceback.format_exc())
            
            start_response('500 Internal Server Error', 
                         [('Content-Type', 'text/html')])
            return [b'<h1>Internal Server Error</h1>']
    
    return wrapper

application = error_handling_middleware(application)
```

## Security Enhancements

### Security Headers Middleware

```python
def security_headers_middleware(application):
    def wrapper(environ, start_response):
        def secure_start_response(status, headers, exc_info=None):
            # Add security headers
            security_headers = [
                ('X-Content-Type-Options', 'nosniff'),
                ('X-Frame-Options', 'DENY'),
                ('X-XSS-Protection', '1; mode=block'),
                ('Strict-Transport-Security', 'max-age=31536000; includeSubDomains'),
                ('Content-Security-Policy', "default-src 'self'")
            ]
            headers.extend(security_headers)
            return start_response(status, headers, exc_info)
        
        return application(environ, secure_start_response)
    return wrapper

application = security_headers_middleware(application)
```

## Testing

### Unit Testing

```python
import unittest
from wsgihandler import application

class WSGIHandlerTest(unittest.TestCase):
    def setUp(self):
        from werkzeug.test import Client
        from werkzeug.wrappers import Response
        self.client = Client(application, Response)
    
    def test_application_response(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
    
    def test_health_check(self):
        response = self.client.get('/health')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, b'OK')
```

### Load Testing

```python
# locustfile.py for load testing
from locust import HttpUser, task, between

class WebUser(HttpUser):
    wait_time = between(1, 3)
    
    @task
    def index_page(self):
        self.client.get("/")
    
    @task(3)
    def view_page(self):
        self.client.get("/default/index")
```

This WSGI handler provides a versatile, standards-compliant foundation for deploying web2py applications across a wide range of WSGI-compatible servers, offering flexibility, performance, and extensive customization options for diverse deployment scenarios.