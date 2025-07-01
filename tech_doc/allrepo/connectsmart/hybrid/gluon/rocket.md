# Rocket Web Server

## Overview
The Rocket module is a monolithic Python-based HTTP/WSGI web server built into the Gluon framework. Originally developed by Timothy Farrell and modified by Massimo Di Pierro, it provides a lightweight, pure-Python web server implementation suitable for development and small-scale production deployments.

## Key Components

### Constants and Configuration
- **VERSION**: "1.2.6" - Current version of Rocket server
- **SERVER_NAME**: Automatically set to hostname
- **BUF_SIZE**: 16384 bytes for buffer operations
- **SOCKET_TIMEOUT**: 10 seconds default timeout
- **Thread configuration**: Default 10 min threads, 0 max threads (unlimited)

### Core Classes

#### Connection
Manages individual client connections with socket operations.

**Key Features:**
- Socket wrapper with timeout management
- SSL/TLS support detection
- Platform-specific optimizations (Darwin/macOS)
- IPv6 and IPv4 support

**Methods:**
- `__init__(sock_tuple, port, secure)`: Initialize connection
- `_sendall_darwin()`: macOS-specific sendall implementation
- `close()`: Clean connection closure

#### Listener
Thread responsible for accepting connections and queuing them for workers.

**Key Features:**
- Multi-interface support (IPv4/IPv6)
- SSL certificate handling
- Queue management for incoming connections
- Automatic socket reuse configuration

**Methods:**
- `wrap_socket()`: SSL/TLS socket wrapping
- `listen()`: Main accept loop
- `start()`, `stop()`: Thread lifecycle

#### Worker
Base class for processing connections, handling HTTP requests.

**Key Features:**
- Request line parsing with regex
- Header processing
- Error handling and recovery
- Logging integration

**Methods:**
- `run()`: Main worker loop
- `read_request_line()`: HTTP request parsing
- `read_headers()`: Header extraction
- `send_response()`: Error response handling

#### WSGIWorker
WSGI-specific worker implementation extending Worker.

**Key Features:**
- WSGI environment building
- Chunked transfer encoding support
- HTTP/1.1 compliance
- File wrapper support

**Methods:**
- `build_environ()`: WSGI environment construction
- `send_headers()`: Response header management
- `write()`: Response body streaming
- `start_response()`: WSGI start_response callable

#### Rocket (Main Server)
Central server class managing threads and connections.

**Key Features:**
- Multi-interface binding
- Thread pool management
- Signal handling (SIGTERM, SIGHUP)
- Graceful shutdown support

**Methods:**
- `start()`: Server initialization and startup
- `stop()`: Graceful shutdown
- `restart()`: Hot reload support

### Thread Management

#### ThreadPool
Manages worker thread lifecycle and distribution.

**Key Features:**
- Dynamic thread scaling
- Dead thread cleanup
- Load-based thread allocation
- Configurable min/max threads

**Methods:**
- `grow()`: Add worker threads
- `shrink()`: Remove idle threads
- `dynamic_resize()`: Auto-scaling logic

#### Monitor
Dedicated thread for connection monitoring and timeout handling.

**Key Features:**
- Connection timeout detection
- Stale connection cleanup
- Load balancing support
- Platform-specific select() handling

### Advanced Features

#### ChunkedReader
Handles HTTP chunked transfer encoding for request bodies.

**Methods:**
- `read()`: Chunk-aware reading
- `readline()`: Line-based chunk reading

#### Futures Support
Optional concurrent.futures integration for async operations.

**Classes:**
- `WSGIFuture`: Future with timeout support
- `WSGIExecutor`: ThreadPoolExecutor wrapper
- `FuturesMiddleware`: WSGI middleware for futures

## Usage Examples

### Basic Server Creation
```python
from gluon.rocket import Rocket

# Simple HTTP server
server = Rocket(
    ('127.0.0.1', 8000),
    'wsgi',
    {'wsgi_app': my_wsgi_app}
)
server.start()
```

### SSL/HTTPS Server
```python
# HTTPS with client certificates
server = Rocket(
    [('0.0.0.0', 443, 'server.key', 'server.crt', 'ca.crt')],
    'wsgi',
    {'wsgi_app': my_wsgi_app}
)
```

### Multi-Interface Server
```python
# Bind to multiple interfaces
interfaces = [
    ('127.0.0.1', 8080),
    ('::1', 8080),  # IPv6 localhost
    ('0.0.0.0', 80)
]
server = Rocket(interfaces, 'wsgi', {'wsgi_app': app})
```

### CherryPy Compatibility
```python
# Drop-in replacement for CherryPy
server = CherryPyWSGIServer(
    ('localhost', 8080),
    wsgi_app,
    numthreads=10,
    request_queue_size=500
)
```

## Configuration Options

### Server Parameters
- `min_threads`: Minimum worker threads (default: 10)
- `max_threads`: Maximum worker threads (0 = unlimited)
- `queue_size`: Connection queue size (default: SOMAXCONN)
- `timeout`: Worker timeout in seconds (default: 600)

### SSL/TLS Options
- Certificate file paths
- Private key paths
- CA certificate for client verification
- Optional client certificate requirements

## Error Handling

### Exception Types
- `SocketTimeout`: Connection timeout errors
- `BadRequest`: Malformed HTTP requests  
- `SocketClosed`: Client disconnection
- `SSLError`: SSL/TLS handshake failures

### Recovery Mechanisms
- Automatic connection cleanup
- Thread pool recovery
- Graceful degradation on errors

## Performance Optimizations

### Platform-Specific
- Darwin/macOS sendall optimization
- Jython compatibility modes
- Windows socket handling

### Resource Management
- Connection pooling
- Thread recycling
- Memory-efficient streaming
- Lazy imports for optional features

## Security Features

### Built-in Protections
- Request size limits
- Header validation
- Path traversal prevention
- SSL/TLS enforcement options

### Client Authentication
- Optional client certificates
- Certificate validation chains
- Configurable SSL versions

## Logging and Monitoring

### Log Channels
- `Rocket`: Main server events
- `Rocket.Errors`: Error conditions
- `Rocket.Monitor`: Connection monitoring
- `Rocket.Requests`: Access logs

### Metrics Available
- Active connections
- Thread pool status
- Request processing times
- Error rates

## Integration Points

### WSGI Compliance
- Full WSGI 1.0 support
- wsgi.file_wrapper optimization
- Streaming response support
- Proper error handling

### Web2py Integration
- Automatic setup in web2py
- Request/Response object support
- Session management hooks
- Static file serving

## Limitations and Considerations

### Known Limitations
- Single-process architecture
- No HTTP/2 support
- Limited WebSocket support
- Basic load balancing

### Best Practices
- Use reverse proxy for production
- Enable SSL for secure deployments
- Monitor thread pool sizing
- Regular log rotation

## Troubleshooting

### Common Issues
1. **Port binding failures**: Check permissions and conflicts
2. **SSL errors**: Verify certificate paths and formats
3. **Thread exhaustion**: Increase max_threads setting
4. **Memory growth**: Check for request body streaming

### Debug Options
- Increase log verbosity
- Enable request dumping
- Monitor thread states
- Profile worker performance

## See Also
- [WSGI Specification](https://www.python.org/dev/peps/pep-3333/)
- [HTTP/1.1 RFC](https://tools.ietf.org/html/rfc2616)
- Gluon main module for integration
- Web2py deployment guide