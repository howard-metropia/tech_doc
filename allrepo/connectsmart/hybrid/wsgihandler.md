# wsgihandler.py

## Overview
This file serves as the main WSGI handler for web2py applications, providing the entry point for WSGI-compliant web servers to interface with the web2py framework.

## Purpose
- Main WSGI application entry point
- Initializes web2py environment
- Routes requests to web2py applications
- Handles production deployment scenarios

## Key Functionality

### WSGI Interface
```python
# Standard WSGI application signature
def application(environ, start_response):
    """Process HTTP requests through web2py"""
    request = parse_environ(environ)
    response = web2py_handler(request)
    start_response(response.status, response.headers)
    return response.body
```

### Web2py Integration
- **Framework Loading**: Imports and initializes gluon
- **Application Routing**: Directs requests to apps
- **Error Management**: Handles exceptions gracefully
- **Logging Setup**: Configures production logging

## Deployment Configuration

### Server Examples
- **Apache + mod_wsgi**: Traditional deployment
- **Nginx + Gunicorn**: Modern Python stack
- **Nginx + uWSGI**: High-performance option
- **Docker + WSGI**: Container deployment

### Performance Optimization
- Process pooling configuration
- Thread management
- Static file serving
- Response caching

## Production Features

### Reliability
- Graceful error handling
- Request timeout management
- Memory leak prevention
- Automatic recovery

This WSGI handler is the bridge between web servers and web2py, enabling scalable production deployments.