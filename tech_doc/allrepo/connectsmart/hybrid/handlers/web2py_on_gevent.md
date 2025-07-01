# Web2py on Gevent Documentation

## Overview

The `web2py_on_gevent.py` module provides a high-performance asynchronous web server implementation for web2py applications using Gevent. Gevent is a coroutine-based Python networking library that uses greenlet to provide a synchronous API on top of the libevent event loop.

## Purpose

This handler enables web2py applications to achieve high concurrency and performance by:
- Implementing asynchronous I/O using Gevent's event loop
- Supporting thousands of concurrent connections
- Providing non-blocking network operations
- Offering built-in SSL/TLS support
- Enabling efficient resource utilization through cooperative multitasking

## Architecture

### Gevent Integration

The handler leverages Gevent's key components:

```python
from gevent import pywsgi
from gevent.pool import Pool
from gevent import monkey
monkey.patch_all()  # Patch standard library for async operation
```

**Key Features:**
- **Monkey Patching**: Makes standard library functions asynchronous
- **WSGI Server**: High-performance WSGI server implementation
- **Connection Pooling**: Manages concurrent connections efficiently
- **Event Loop**: Single-threaded event loop for handling I/O operations

### Asynchronous Processing Model

```
Request → Gevent Event Loop → Greenlet → WSGI App → web2py → Response
```

**Benefits:**
- **High Concurrency**: Handle thousands of simultaneous connections
- **Low Memory Footprint**: Lightweight greenlets instead of threads
- **Non-blocking I/O**: Efficient handling of I/O operations
- **Scalability**: Excellent scaling characteristics for I/O-bound applications

## Configuration Options

### Command Line Interface

The handler provides a comprehensive CLI for server configuration:

```bash
python web2py_on_gevent.py -i 127.0.0.1 -p 8000 -a "<recycle>"
```

### Available Options

#### Basic Configuration

- **`-i, --ip`**: IP address to bind to (default: 127.0.0.1)
- **`-p, --port`**: Port number to listen on (default: 8000)
- **`-a, --password`**: Admin password (use "<recycle>" to reuse last password)

#### SSL Configuration

- **`-c, --ssl_certificate`**: Path to SSL certificate file
- **`-k, --ssl_private_key`**: Path to SSL private key file

#### Performance Configuration

- **`-w, --workers`**: Number of worker greenlets (default: None for unlimited)
- **`-l, --logging`**: Enable logging to httpserver.log
- **`-F, --profiler`**: Enable profiling with specified directory

### Example Configurations

#### Development Server

```bash
python web2py_on_gevent.py -i 0.0.0.0 -p 8000 -a "admin123" -l
```

#### Production Server

```bash
python web2py_on_gevent.py -i 0.0.0.0 -p 443 -a "<recycle>" \
  -c /path/to/cert.pem -k /path/to/key.pem -w 1000 -l
```

#### SSL Development

```bash
python web2py_on_gevent.py -i 127.0.0.1 -p 8443 -a "dev123" \
  -c server.crt -k server.key -l
```

## Server Implementation

### Core Server Function

```python
def run(options):
    from gluon.settings import global_settings
    global_settings.web2py_runtime_handler = True
    import gluon.main
    
    # Password management
    if options.password != '<recycle>':
        gluon.main.save_password(options.password, int(options.port))
    
    # Application setup
    if options.logging:
        application = gluon.main.appfactory(
            wsgiapp=gluon.main.wsgibase,
            logfilename='httpserver.log',
            profiler_dir=profiler
        )
    else:
        application = gluon.main.wsgibase
    
    # Server configuration
    address = (options.ip, int(options.port))
    workers = options.workers
    spawn = workers and Pool(int(options.workers)) or 'default'
    
    # SSL setup
    ssl_args = dict()
    if options.ssl_private_key:
        ssl_args['keyfile'] = options.ssl_private_key
    if options.ssl_certificate:
        ssl_args['certfile'] = options.ssl_certificate
    
    # Create and start server
    server = pywsgi.WSGIServer(
        address, application,
        spawn=spawn, log=None,
        **ssl_args
    )
    server.serve_forever()
```

### Worker Pool Management

The handler supports configurable worker pools:

```python
# Unlimited workers (default)
spawn = 'default'

# Limited worker pool
spawn = Pool(int(options.workers))
```

**Worker Pool Benefits:**
- **Resource Control**: Limit concurrent connections
- **Memory Management**: Prevent memory exhaustion
- **Performance Tuning**: Optimize for specific workloads
- **Graceful Degradation**: Handle overload scenarios

## SSL/TLS Support

### Certificate Configuration

```python
ssl_args = dict()
if options.ssl_private_key:
    ssl_args['keyfile'] = options.ssl_private_key
if options.ssl_certificate:
    ssl_args['certfile'] = options.ssl_certificate
```

### SSL Best Practices

```bash
# Generate self-signed certificate for development
openssl req -x509 -newkey rsa:4096 -keyout server.key -out server.crt -days 365 -nodes

# Production certificate setup
python web2py_on_gevent.py -i 0.0.0.0 -p 443 \
  -c /etc/ssl/certs/domain.crt \
  -k /etc/ssl/private/domain.key \
  -a "<recycle>" -w 500
```

## Performance Optimization

### Greenlet Pool Sizing

```python
# CPU-bound applications
workers = multiprocessing.cpu_count()

# I/O-bound applications  
workers = 1000  # or higher

# Memory-constrained environments
workers = 100
```

### Monkey Patching Optimization

```python
# Selective patching for better performance
from gevent import monkey
monkey.patch_socket()
monkey.patch_ssl()
monkey.patch_select()
monkey.patch_threading(Event=True)
```

### Event Loop Tuning

```python
# Optimize event loop
import gevent
from gevent import config

# Increase loop efficiency
config.loop = 'libev'  # Use libev instead of libevent
config.resolver = 'ares'  # Use c-ares for DNS resolution
```

## Monitoring and Logging

### Application Logging

```python
if options.logging:
    application = gluon.main.appfactory(
        wsgiapp=gluon.main.wsgibase,
        logfilename='httpserver.log',
        profiler_dir=profiler
    )
```

### Custom Logging Configuration

```python
import logging
import sys

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('gevent_server.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

# Log server events
def log_server_events(server):
    logging.info(f"Server started on {server.address}")
    logging.info(f"Worker pool: {server.pool}")
    logging.info(f"SSL enabled: {bool(server.ssl_args)}")
```

### Performance Monitoring

```python
import time
import resource

def monitor_server_performance():
    while True:
        # Memory usage
        memory_usage = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
        
        # Connection stats
        active_connections = len(server.pool)
        
        logging.info(f"Memory: {memory_usage}KB, Connections: {active_connections}")
        time.sleep(60)  # Log every minute
```

## Deployment Strategies

### Development Deployment

```python
# Development server with auto-reload
import os
from gevent import spawn

def watch_files():
    """Watch for file changes and restart server"""
    import watchdog
    # Implementation for file watching
    
if __name__ == '__main__':
    if os.getenv('DEVELOPMENT'):
        spawn(watch_files)
    main()
```

### Production Deployment

```python
# Production server with process management
import signal
import sys

def signal_handler(signum, frame):
    """Graceful shutdown on SIGTERM"""
    logging.info(f"Received signal {signum}, shutting down...")
    server.stop()
    sys.exit(0)

signal.signal(signal.SIGTERM, signal_handler)
signal.signal(signal.SIGINT, signal_handler)
```

### Container Deployment

```dockerfile
FROM python:3.9-slim

# Install dependencies
RUN pip install gevent web2py

# Copy application
COPY . /app
WORKDIR /app

# Expose port
EXPOSE 8000

# Run server
CMD ["python", "web2py_on_gevent.py", "-i", "0.0.0.0", "-p", "8000", "-a", "<recycle>"]
```

## Error Handling

### Exception Management

```python
def error_wrapper(application):
    def wrapper(environ, start_response):
        try:
            return application(environ, start_response)
        except Exception as e:
            logging.error(f"Application error: {e}", exc_info=True)
            start_response('500 Internal Server Error', 
                         [('Content-Type', 'text/plain')])
            return [b'Internal Server Error']
    return wrapper

# Apply error handling
application = error_wrapper(application)
```

### Graceful Degradation

```python
def health_check_middleware(application):
    def wrapper(environ, start_response):
        if environ['PATH_INFO'] == '/health':
            start_response('200 OK', [('Content-Type', 'text/plain')])
            return [b'OK']
        return application(environ, start_response)
    return wrapper
```

## Advanced Features

### Custom Gevent Server

```python
from gevent.pywsgi import WSGIServer

class CustomWSGIServer(WSGIServer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request_count = 0
    
    def handle(self, socket, address):
        self.request_count += 1
        super().handle(socket, address)
```

### Middleware Integration

```python
def gevent_middleware(application):
    def wrapper(environ, start_response):
        # Add gevent-specific context
        environ['gevent.version'] = gevent.__version__
        environ['gevent.hub'] = str(gevent.get_hub())
        return application(environ, start_response)
    return wrapper
```

### WebSocket Support

```python
from geventwebsocket import WebSocketServer

# WebSocket-enabled server
server = WebSocketServer(
    (options.ip, int(options.port)),
    application,
    spawn=spawn
)
```

This Gevent handler provides a high-performance, asynchronous deployment solution for web2py applications, offering excellent scalability for I/O-bound workloads while maintaining simplicity and ease of deployment.