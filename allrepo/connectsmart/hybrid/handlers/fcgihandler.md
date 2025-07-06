# FastCGI Handler Documentation

## Overview

The FastCGI Handler (`fcgihandler.py`) is a Web2py framework component that provides FastCGI (Fast Common Gateway Interface) support for high-performance web server deployments. This handler enables Web2py applications to run as persistent FastCGI processes, offering superior performance compared to traditional CGI by eliminating the overhead of process creation for each request.

## Technical Specifications

### Core Components

#### Framework Integration
- **Framework**: Web2py Web Framework
- **License**: LGPLv3
- **Handler Type**: FastCGI (Fast Common Gateway Interface)
- **Primary Server**: Optimized for lighttpd
- **Protocol**: FastCGI over Unix domain sockets

#### Dependencies
```python
import sys
import os
from gluon.settings import global_settings
import gluon.main
import gluon.contrib.gateways.fcgi as fcgi
```

### Architecture

#### FastCGI Implementation
The handler uses Web2py's built-in FastCGI gateway (`gluon.contrib.gateways.fcgi`) to create a persistent WSGI server that communicates with the web server via FastCGI protocol.

#### Configuration Parameters
```python
LOGGING = False    # Enable/disable request logging
SOFTCRON = False   # Enable/disable soft cron functionality
```

#### Process Management
```python
# Basic WSGI application
application = gluon.main.wsgibase

# Enhanced application with logging
application = gluon.main.appfactory(
    wsgiapp=gluon.main.wsgibase,
    logfilename='httpserver.log',
    profiler_dir=None
)
```

### Lighttpd Configuration

#### Required Modules
```lighttpd
server.modules = ('mod_rewrite', 'mod_fastcgi')
```

#### Complete lighttpd.conf Example
```lighttpd
server.port = 8000
server.bind = '127.0.0.1'
server.event-handler = 'freebsd-kqueue'
server.modules = ('mod_rewrite', 'mod_fastcgi')
server.error-handler-404 = '/test.fcgi'
server.document-root = '/somewhere/web2py'
server.errorlog = '/tmp/error.log'

fastcgi.server = (
    '.fcgi' => (
        'localhost' => (
            'min-procs' => 1,
            'socket' => '/tmp/fcgi.sock'
        )
    )
)
```

### Socket Communication

#### Unix Domain Socket
- **Socket Path**: `/tmp/fcgi.sock`
- **Communication**: Binary FastCGI protocol
- **Persistence**: Socket persists across requests
- **Performance**: Faster than TCP/IP for local communication

#### Connection Management
```python
fcgi.WSGIServer(application, bindAddress='/tmp/fcgi.sock').run()
```

### Configuration Options

#### Logging Configuration
```python
if LOGGING:
    application = gluon.main.appfactory(
        wsgiapp=gluon.main.wsgibase,
        logfilename='httpserver.log',
        profiler_dir=None
    )
```

#### Cron Configuration
```python
if SOFTCRON:
    global_settings.web2py_crontype = 'soft'
```

### Performance Characteristics

#### Process Model
- **Persistent Processes**: Processes remain alive between requests
- **Memory Efficiency**: Shared memory across requests
- **Startup Time**: Fast response due to pre-loaded Python interpreter
- **Scalability**: Excellent for medium to high traffic applications

#### Advantages over CGI
- **No Process Creation**: Eliminates fork/exec overhead
- **Memory Sharing**: Reduced memory footprint per request
- **Module Caching**: Python modules loaded once and cached
- **Connection Pooling**: Database connections can be maintained

### Deployment Architecture

#### Single Process Configuration
```lighttpd
'min-procs' => 1,
'max-procs' => 1,
'socket' => '/tmp/fcgi.sock'
```

#### Multi-Process Configuration
```lighttpd
'min-procs' => 2,
'max-procs' => 8,
'socket' => '/tmp/fcgi.sock'
```

### Runtime Configuration

#### Global Settings
```python
global_settings.web2py_runtime_handler = True
```

#### Path Management
```python
path = os.path.dirname(os.path.abspath(__file__))
os.chdir(path)
sys.path = [path] + [p for p in sys.path if not p == path]
```

#### Directory Validation
```python
if not os.path.isdir('applications'):
    raise RuntimeError('Running from the wrong folder')
```

### Monitoring and Logging

#### Application Logging
- **Log File**: `httpserver.log` (when LOGGING=True)
- **Profiling**: Optional profiler directory
- **Request Tracking**: Detailed request/response logging

#### Server Logging
- **lighttpd Error Log**: `/tmp/error.log`
- **FastCGI Communication**: Logged via lighttpd
- **Socket Status**: Connection state monitoring

### Error Handling

#### Common Error Scenarios
- **Socket Permission Issues**: Unix socket file permissions
- **Process Crashes**: FastCGI process failure recovery
- **Memory Leaks**: Long-running process memory management
- **Database Connections**: Connection pool exhaustion

#### Recovery Mechanisms
- **Process Restart**: lighttpd automatically restarts failed processes
- **Socket Recreation**: Automatic socket file management
- **Graceful Degradation**: Error responses maintain service availability

### Security Considerations

#### Socket Security
- **File Permissions**: Proper Unix socket permissions (600 or 660)
- **Process Owner**: Run as non-privileged user
- **Socket Location**: Secure temporary directory

#### Process Isolation
- **User Context**: Execute under web server user
- **Resource Limits**: Set appropriate memory/CPU limits
- **File System Access**: Restrict file system permissions

### Advanced Configuration

#### Load Balancing
```lighttpd
fastcgi.server = (
    '.fcgi' => (
        'server1' => (
            'socket' => '/tmp/fcgi1.sock',
            'min-procs' => 2,
            'max-procs' => 4
        ),
        'server2' => (
            'socket' => '/tmp/fcgi2.sock',
            'min-procs' => 2,
            'max-procs' => 4
        )
    )
)
```

#### Health Monitoring
```lighttpd
fastcgi.server = (
    '.fcgi' => (
        'localhost' => (
            'socket' => '/tmp/fcgi.sock',
            'check-local' => 'enable',
            'broken-scriptfilename' => 'enable'
        )
    )
)
```

### Integration Points

#### Web2py Framework
- **WSGI Application**: Full Web2py WSGI app support
- **Session Management**: Persistent session handling
- **Database Connections**: Connection pooling compatibility
- **Cron Jobs**: Soft cron integration

#### Web Server Integration
- **lighttpd**: Primary target server
- **nginx**: Compatible with nginx FastCGI
- **Apache**: mod_fastcgi support

### Best Practices

#### Performance Optimization
- **Process Count**: Match CPU core count
- **Memory Monitoring**: Regular memory usage checks
- **Connection Pooling**: Database connection management
- **Static File Serving**: Use web server for static files

#### Reliability
- **Process Limits**: Set appropriate min/max processes
- **Health Checks**: Implement process health monitoring
- **Graceful Restart**: Plan for zero-downtime deployments
- **Error Logging**: Comprehensive error tracking

#### Security
- **Process User**: Run as dedicated user account
- **File Permissions**: Secure socket and log files
- **Resource Limits**: Prevent resource exhaustion
- **Input Validation**: Validate all external inputs

### Troubleshooting

#### Common Issues
- **Socket Not Found**: Check socket path and permissions
- **Process Won't Start**: Verify Python path and dependencies
- **High Memory Usage**: Monitor for memory leaks
- **Slow Responses**: Check database connection status

#### Debugging Commands
```bash
# Check socket status
ls -la /tmp/fcgi.sock

# Monitor processes
ps aux | grep fcgihandler

# Test socket connection
socat - UNIX-CONNECT:/tmp/fcgi.sock

# Monitor lighttpd status
lighttpd -f /etc/lighttpd/lighttpd.conf -D
```

### Migration and Deployment

#### From CGI Migration
1. Update web server configuration
2. Install FastCGI modules
3. Configure socket communication
4. Test process persistence
5. Monitor performance improvements

#### Production Deployment
1. Set production configuration flags
2. Configure log rotation
3. Implement monitoring
4. Set up process supervision
5. Plan maintenance procedures

This FastCGI handler provides excellent performance characteristics for Web2py applications, making it ideal for production deployments requiring high throughput and low latency response times.