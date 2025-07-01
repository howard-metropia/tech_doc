# gluon/contrib/gateways/fcgi.py

## Overview

The fcgi.py module provides a FastCGI/WSGI gateway implementation for Web2py applications. Originally developed by Allan Saddi and modified for Web2py, this module enables deployment of Web2py applications behind FastCGI-compatible web servers like Apache with mod_fastcgi or Nginx.

## Key Components

### Main Classes
- **WSGIServer**: High-level WSGI application server
- **Server**: Low-level FastCGI protocol handler
- **Request**: Individual FastCGI request processor
- **Connection**: FastCGI connection management

### Protocol Implementation
- FastCGI binary protocol support
- WSGI interface compliance
- Multi-threaded request handling
- Connection pooling and reuse

## FastCGI Protocol Support

### Protocol Constants
```python
# FastCGI Version
FCGI_VERSION_1 = 1

# Record Types
FCGI_BEGIN_REQUEST = 1
FCGI_ABORT_REQUEST = 2
FCGI_END_REQUEST = 3
FCGI_PARAMS = 4
FCGI_STDIN = 5
FCGI_STDOUT = 6
FCGI_STDERR = 7
FCGI_DATA = 8
FCGI_GET_VALUES = 9
FCGI_GET_VALUES_RESULT = 10

# Application Roles
FCGI_RESPONDER = 1
FCGI_AUTHORIZER = 2
FCGI_FILTER = 3
```

### Record Structure
```python
class Record:
    def __init__(self, type, requestId, content=''):
        self.version = FCGI_VERSION_1
        self.type = type
        self.requestId = requestId
        self.content = content
        self.contentLength = len(content)
```

## Core Architecture

### WSGIServer Class
```python
class WSGIServer(Server):
    def __init__(self, application, bind_addr=None, 
                 umask=None, multiplexed=False, 
                 bindAddress=None, allowedServers=None,
                 loggingLevel=logging.INFO, **kw):
        # Initialize WSGI application wrapper
        self._application = application
        self._environ = {}
        self._multithreaded = True
        
        # Call parent constructor
        Server.__init__(self, **kw)
```

### Request Processing Flow
1. **Accept Connection**: Server accepts FastCGI connections
2. **Parse Request**: Decode FastCGI protocol messages
3. **Build Environment**: Create WSGI environ dictionary
4. **Call Application**: Invoke WSGI app with environ
5. **Stream Response**: Send response through FastCGI protocol
6. **End Request**: Send end record and cleanup

## WSGI Environment Construction

### Environment Building
```python
def _buildEnviron(self, req):
    """Build WSGI environ dictionary from FastCGI params"""
    environ = self._environ.copy()
    
    # Add FastCGI parameters
    for name, value in req.params.items():
        environ[name] = value
    
    # Set required WSGI variables
    environ['wsgi.version'] = (1, 0)
    environ['wsgi.url_scheme'] = environ.get('HTTPS') and 'https' or 'http'
    environ['wsgi.input'] = req.stdin
    environ['wsgi.errors'] = req.stderr
    environ['wsgi.multithread'] = self._multithreaded
    environ['wsgi.multiprocess'] = True
    environ['wsgi.run_once'] = False
    
    return environ
```

### Parameter Processing
```python
def _decodeParams(self, stream):
    """Decode name-value pairs from FastCGI params stream"""
    params = {}
    while True:
        nameLen, valueLen = self._readLengths(stream)
        if nameLen == 0 and valueLen == 0:
            break
            
        name = stream.read(nameLen)
        value = stream.read(valueLen)
        params[name] = value
    
    return params
```

## Connection Management

### Connection Handling
```python
class Connection:
    def __init__(self, sock, addr):
        self._sock = sock
        self._addr = addr
        self._writeBuffer = []
        self._writeBufferSize = 0
        
    def write(self, data):
        """Buffer data for writing"""
        self._writeBuffer.append(data)
        self._writeBufferSize += len(data)
        
    def flush(self):
        """Flush write buffer to socket"""
        if self._writeBuffer:
            data = ''.join(self._writeBuffer)
            self._sock.sendall(data)
            self._writeBuffer = []
            self._writeBufferSize = 0
```

### Socket Management
```python
def _setupSocket(self):
    """Create and configure listening socket"""
    if self._bindAddress is None:
        # Use stdin for single process mode
        sock = socket.fromfd(sys.stdin.fileno(), 
                           socket.AF_INET, 
                           socket.SOCK_STREAM)
    else:
        # Create network socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind(self._bindAddress)
        sock.listen(5)
    
    return sock
```

## Request Processing

### Request Class
```python
class Request:
    def __init__(self, conn, reqId):
        self._conn = conn
        self.requestId = reqId
        self.role = None
        self.flags = 0
        self.aborted = False
        
        # I/O streams
        self.stdin = StringIO()
        self.stdout = StringIO()
        self.stderr = StringIO()
        self.data = StringIO()
```

### Response Streaming
```python
def _finishRequest(self, req):
    """Send response data and end request"""
    # Send stdout data
    stdout_data = req.stdout.getvalue()
    if stdout_data:
        self._sendRecord(FCGI_STDOUT, req.requestId, stdout_data)
    
    # Send end-of-stream record
    self._sendRecord(FCGI_STDOUT, req.requestId, '')
    
    # Send stderr data if any
    stderr_data = req.stderr.getvalue()
    if stderr_data:
        self._sendRecord(FCGI_STDERR, req.requestId, stderr_data)
        self._sendRecord(FCGI_STDERR, req.requestId, '')
    
    # Send end request record
    endReq = struct.pack('!BBxxxxxx', 0, FCGI_REQUEST_COMPLETE)
    self._sendRecord(FCGI_END_REQUEST, req.requestId, endReq)
```

## Error Handling

### Protocol Errors
```python
def _handleProtocolError(self, error):
    """Handle FastCGI protocol violations"""
    logging.error(f"FastCGI protocol error: {error}")
    # Close connection on protocol errors
    self._conn.close()
```

### Application Errors
```python
def _handleApplicationError(self, req, error):
    """Handle WSGI application errors"""
    req.stderr.write(f"Application error: {str(error)}\n")
    
    # Send 500 error response
    response = "Status: 500 Internal Server Error\r\n\r\n"
    req.stdout.write(response)
```

## CGI Fallback Mode

### CGI Detection
```python
def _isCGI():
    """Detect if running in CGI mode"""
    return os.environ.get('FCGI_FORCE_CGI', '').lower() in ('y', 'yes', '1')

def _handleCGI(application):
    """Run in standard CGI mode"""
    environ = os.environ.copy()
    environ['wsgi.input'] = sys.stdin
    environ['wsgi.errors'] = sys.stderr
    
    def start_response(status, headers, exc_info=None):
        print(f"Status: {status}")
        for header in headers:
            print(f"{header[0]}: {header[1]}")
        print()
    
    result = application(environ, start_response)
    for data in result:
        sys.stdout.write(data)
```

## Threading Support

### Thread Safety
```python
import threading

class ThreadedServer(WSGIServer):
    def __init__(self, application, **kw):
        WSGIServer.__init__(self, application, **kw)
        self._lock = threading.Lock()
        self._threads = []
    
    def _spawnThread(self, conn):
        """Spawn thread to handle connection"""
        thread = threading.Thread(target=self._handleConnection, 
                                 args=(conn,))
        thread.daemon = True
        thread.start()
        
        with self._lock:
            self._threads.append(thread)
```

## Performance Features

### Buffer Management
```python
def _optimizeBuffers(self):
    """Optimize I/O buffer sizes"""
    # Increase socket buffer sizes
    self._sock.setsockopt(socket.SOL_SOCKET, 
                         socket.SO_RCVBUF, 32768)
    self._sock.setsockopt(socket.SOL_SOCKET, 
                         socket.SO_SNDBUF, 32768)
```

### Connection Pooling
```python
class ConnectionPool:
    def __init__(self, maxConnections=10):
        self._pool = []
        self._maxConnections = maxConnections
        self._lock = threading.Lock()
    
    def getConnection(self):
        """Get connection from pool"""
        with self._lock:
            if self._pool:
                return self._pool.pop()
        return None
    
    def putConnection(self, conn):
        """Return connection to pool"""
        with self._lock:
            if len(self._pool) < self._maxConnections:
                self._pool.append(conn)
```

## Integration with Web Servers

### Apache Configuration
```apache
# Apache mod_fastcgi configuration
LoadModule fastcgi_module modules/mod_fastcgi.so
FastCgiExternalServer /var/www/web2py/fcgihandler.fcgi -host 127.0.0.1:9000

<VirtualHost *:80>
    DocumentRoot /var/www/web2py
    ScriptAlias / /var/www/web2py/fcgihandler.fcgi/
</VirtualHost>
```

### Nginx Configuration
```nginx
# Nginx FastCGI configuration
location / {
    fastcgi_pass 127.0.0.1:9000;
    fastcgi_param SCRIPT_FILENAME $document_root$fastcgi_script_name;
    include fastcgi_params;
}
```

## Usage Examples

### Basic FastCGI Server
```python
from gluon.contrib.gateways.fcgi import WSGIServer
from gluon.main import wsgibase

# Create WSGI application
application = wsgibase

# Start FastCGI server
server = WSGIServer(application, 
                   bindAddress=('127.0.0.1', 9000))
server.run()
```

### Production Deployment
```python
#!/usr/bin/env python
import os
import sys
from gluon.contrib.gateways.fcgi import WSGIServer

# Add web2py to path
sys.path.insert(0, '/path/to/web2py')

from gluon.main import wsgibase

if __name__ == '__main__':
    server = WSGIServer(wsgibase)
    server.run()
```

## Security Considerations

### Process Isolation
- Runs as separate process from web server
- Limited file system access
- Configurable user/group permissions

### Input Validation
- Protocol message validation
- Parameter length checking
- Buffer overflow protection

## Best Practices

### Configuration
1. Set appropriate buffer sizes
2. Configure connection limits
3. Use process monitoring
4. Enable logging

### Deployment
1. Use separate user account
2. Restrict file permissions
3. Monitor resource usage
4. Implement graceful shutdown

### Error Handling
1. Log all errors appropriately
2. Implement proper cleanup
3. Handle connection failures
4. Provide meaningful error messages