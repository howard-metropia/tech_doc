# PySimpleSOAP Transport Module

## Overview
This module provides multiple HTTP transport implementations for SOAP clients, supporting various Python HTTP libraries with feature detection and automatic fallback capabilities.

## Key Features

### Transport Architecture

#### Multi-Library Support
The module supports multiple HTTP transport backends:
- **httplib2**: Full-featured HTTP library with proxy and SSL support
- **urllib2**: Standard library HTTP implementation
- **pycurl**: libcurl Python bindings for advanced features
- **DummyTransport**: Testing transport for mock responses

#### Feature Detection System
```python
_http_connectors = {}  # Library name to class mapping
_http_facilities = {}  # Feature to supported libraries mapping

class TransportBase:
    @classmethod
    def supports_feature(cls, feature_name):
        """Check if transport supports specific feature"""
        return cls._wrapper_name in _http_facilities[feature_name]
```

### Transport Implementations

#### HttpLib2 Transport
```python
class Httplib2Transport(httplib2.Http, TransportBase):
    """
    Advanced HTTP transport using httplib2 library
    
    Features:
    - Connection pooling and keep-alive
    - Proxy support (HTTP, SOCKS)
    - SSL certificate validation
    - Timeout configuration
    - Session persistence
    """
    
    def __init__(self, timeout, proxy=None, cacert=None, sessions=False):
        # Proxy configuration
        if proxy:
            import socks
            kwargs['proxy_info'] = httplib2.ProxyInfo(
                proxy_type=socks.PROXY_TYPE_HTTP, **proxy
            )
        
        # SSL configuration
        kwargs['disable_ssl_certificate_validation'] = cacert is None
        kwargs['ca_certs'] = cacert
        
        # Timeout support
        kwargs['timeout'] = timeout
```

**HttpLib2 Features:**
- **Proxy Support**: HTTP and SOCKS proxy configuration
- **SSL Validation**: Certificate authority validation
- **Connection Reuse**: HTTP keep-alive and connection pooling
- **Version Compatibility**: Automatic feature detection based on version

#### urllib2 Transport
```python
class urllib2Transport(TransportBase):
    """
    Standard library HTTP transport
    
    Features:
    - SSL context configuration
    - Cookie jar session support
    - Timeout handling (Python 2.6+)
    - HTTP error handling
    """
    
    def __init__(self, timeout=None, proxy=None, cacert=None, sessions=False):
        handlers = []
        
        # SSL context for newer Python versions
        if sys.version_info >= (2,7,9) or sys.version_info >= (3,2,0):
            context = ssl.create_default_context()
            context.check_hostname = False
            context.verify_mode = ssl.CERT_NONE
            handlers.append(urllib2.HTTPSHandler(context=context))
        
        # Session support with cookies
        if sessions:
            handlers.append(urllib2.HTTPCookieProcessor(CookieJar()))
```

**urllib2 Features:**
- **Standard Library**: No external dependencies
- **SSL Security**: Modern SSL context support
- **Session Management**: Cookie-based session persistence
- **Error Handling**: HTTP 500 error tolerance for SOAP faults

#### pycurl Transport
```python
class pycurlTransport(TransportBase):
    """
    High-performance HTTP transport using libcurl
    
    Features:
    - Advanced proxy support (including NTLM)
    - Comprehensive SSL options
    - High performance for bulk operations
    - Detailed connection control
    """
    
    def request(self, url, method, body, headers):
        c = pycurl.Curl()
        c.setopt(pycurl.URL, url)
        
        # Proxy configuration
        if 'proxy_host' in self.proxy:
            c.setopt(pycurl.PROXY, self.proxy['proxy_host'])
            c.setopt(pycurl.PROXYPORT, self.proxy['proxy_port'])
        
        # SSL configuration
        c.setopt(pycurl.SSL_VERIFYPEER, self.cacert and 1 or 0)
        c.setopt(pycurl.SSL_VERIFYHOST, self.cacert and 2 or 0)
        
        # Timeout configuration
        c.setopt(pycurl.CONNECTTIMEOUT, self.timeout)
        c.setopt(pycurl.TIMEOUT, self.timeout)
```

**pycurl Features:**
- **Performance**: Optimized for high-throughput scenarios
- **Proxy Support**: Advanced proxy authentication (NTLM, digest)
- **SSL Control**: Fine-grained SSL/TLS configuration
- **Connection Management**: Detailed timeout and connection control

### Testing and Development

#### DummyTransport
```python
class DummyTransport:
    """
    Testing transport for unit tests and development
    
    Features:
    - Mock response injection
    - Request logging and inspection
    - No network connectivity required
    - Deterministic response behavior
    """
    
    def __init__(self, xml_response):
        self.xml_response = xml_response
    
    def request(self, location, method, body, headers):
        log.debug("%s %s", method, location)
        log.debug("Headers: %s", headers)
        log.debug("Body: %s", body)
        return {}, self.xml_response
```

### Transport Selection System

#### Automatic Transport Selection
```python
def get_http_wrapper(library=None, features=[]):
    """
    Select appropriate HTTP transport based on requirements
    
    Parameters:
    - library: Specific library name ('httplib2', 'urllib2', 'pycurl')
    - features: Required features list (['proxy', 'cacert', 'timeout'])
    
    Returns:
    - Transport class that supports requested features
    """
    
    # Specific library requested
    if library is not None:
        if library not in _http_connectors:
            raise RuntimeError('%s transport is not available' % library)
        return _http_connectors[library]
    
    # No specific requirements - return best available
    if not features:
        return _http_connectors.get('httplib2', _http_connectors['urllib2'])
    
    # Find transport supporting all required features
    candidates = set(_http_connectors.keys())
    for feature in features:
        if feature in _http_facilities:
            candidates &= set(_http_facilities[feature])
    
    # Return best candidate
    for preferred in ['httplib2', 'pycurl', 'urllib2']:
        if preferred in candidates:
            return _http_connectors[preferred]
    
    raise RuntimeError('No transport supports features: %s' % features)
```

### Feature Support Matrix

#### Supported Features
```python
# Feature availability mapping
_http_facilities = {
    'proxy': ['httplib2', 'pycurl'],           # HTTP/SOCKS proxy support
    'cacert': ['httplib2', 'pycurl'],          # SSL certificate validation
    'timeout': ['httplib2', 'urllib2', 'pycurl'],  # Request timeout
    'sessions': ['urllib2']                     # Cookie-based sessions
}
```

#### Transport Capabilities
| Transport | Proxy | SSL Certs | Timeout | Sessions | Performance |
|-----------|-------|-----------|---------|----------|-------------|
| httplib2  | ✓     | ✓         | ✓       | ✓        | High        |
| urllib2   | ✗     | ✗         | ✓       | ✓        | Medium      |
| pycurl    | ✓     | ✓         | ✓       | ✗        | Very High   |

### Performance Optimizations

#### Socket-Level Optimizations
```python
# Optional TCP_NODELAY optimization (disabled by default)
if False:  # Enable for Linux performance boost
    import socket
    realsocket = socket.socket
    def socketwrap(family=socket.AF_INET, type=socket.SOCK_STREAM, proto=0):
        sockobj = realsocket(family, type, proto)
        if type == socket.SOCK_STREAM:
            sockobj.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        return sockobj
    socket.socket = socketwrap
```

#### Connection Reuse
- **httplib2**: Automatic connection pooling and keep-alive
- **pycurl**: Manual connection reuse for bulk operations
- **urllib2**: Basic connection management

### SSL and Security

#### SSL Configuration
```python
# Modern SSL context (Python 2.7.9+ and 3.2+)
context = ssl.create_default_context()
context.check_hostname = False
context.verify_mode = ssl.CERT_NONE

# Certificate validation
if cacert:
    context.verify_mode = ssl.CERT_REQUIRED
    context.load_verify_locations(cacert)
```

#### Security Features
- **Certificate Validation**: CA certificate verification
- **Protocol Support**: TLS 1.0+ support
- **Cipher Selection**: Modern cipher suite support
- **Hostname Verification**: Optional hostname checking

### Error Handling and Logging

#### HTTP Error Management
```python
try:
    response = transport.request(url, method, body, headers)
    return response
except urllib2.HTTPError as e:
    if e.code == 500:
        # SOAP faults return HTTP 500 but contain valid response
        return e.info(), e.read()
    raise
```

#### Debugging and Logging
- **Request Logging**: Full request/response logging
- **Debug Output**: Detailed transport-level debugging
- **Error Context**: Rich error information for troubleshooting

### Integration with SOAP Client

#### Transport Usage in SoapClient
```python
from pysimplesoap.transport import get_http_wrapper

# Automatic transport selection
transport_class = get_http_wrapper(features=['proxy', 'timeout'])
transport = transport_class(timeout=30, proxy={'proxy_host': 'proxy.example.com'})

# Use with SOAP client
client = SoapClient(
    wsdl='http://example.com/service?wsdl',
    transport=transport
)
```

This transport system provides robust, feature-rich HTTP connectivity for SOAP operations with automatic fallback and comprehensive error handling across multiple Python HTTP libraries.