# PySimpleSOAP Package

**File**: `gluon/contrib/pysimplesoap/__init__.py`  
**Type**: SOAP Web Services Library  
**Framework**: Web2py Gluon Framework  
**License**: LGPL 3.0  
**Author**: Mariano Reingart

## Overview

PySimpleSOAP is a Python library for consuming and serving SOAP (Simple Object Access Protocol) web services. It provides a simplified interface for SOAP operations while maintaining compatibility with standard SOAP specifications and WSDL (Web Services Description Language) documents.

## Package Information

### Version and Licensing
- **Version**: 1.16.2
- **License**: LGPL 3.0 (GNU Lesser General Public License)
- **Author**: Mariano Reingart
- **Email**: reingart@gmail.com
- **Copyright**: Copyright (C) 2013 Mariano Reingart

### Core Components
```python
from . import client       # SOAP client functionality
from . import server       # SOAP server implementation
from . import simplexml    # XML manipulation utilities
from . import transport    # HTTP transport layer
```

### Configuration
```python
TIMEOUT = 60  # Default timeout for HTTP requests in seconds
```

## Key Features

### SOAP Client Capabilities
- **WSDL Parsing**: Automatic service discovery from WSDL documents
- **Method Introspection**: Dynamic method generation from service definitions
- **Type Mapping**: Automatic Python-to-SOAP type conversion
- **Error Handling**: Comprehensive SOAP fault handling
- **Authentication**: Support for various authentication mechanisms

### SOAP Server Capabilities
- **Service Publishing**: Expose Python functions as SOAP web services
- **WSDL Generation**: Automatic WSDL document generation
- **Type Validation**: Input/output type validation
- **Fault Management**: Proper SOAP fault response generation

### XML Processing
- **SimpleXML**: Lightweight XML manipulation similar to PHP's SimpleXML
- **Namespace Support**: Full XML namespace handling
- **Type Marshalling**: Automatic conversion between Python and XML types

## Quick Start Examples

### SOAP Client Usage
```python
from gluon.contrib import pysimplesoap

# Create client from WSDL
client = pysimplesoap.SoapClient(
    wsdl="http://example.com/service?wsdl",
    timeout=30
)

# Call service method
response = client.GetUserInfo(user_id=123)
print(response.Name)
print(response.Email)
```

### SOAP Server Creation
```python
from gluon.contrib import pysimplesoap

# Create server
server = pysimplesoap.SoapDispatcher(
    name="MyService",
    location="http://localhost:8080/soap",
    action="http://localhost:8080/soap",
    namespace="http://example.com/myservice",
    documentation="My SOAP Service"
)

# Register service method
def get_user_info(user_id):
    """Get user information"""
    return {
        'name': 'John Doe',
        'email': 'john@example.com',
        'user_id': user_id
    }

server.register_function('GetUserInfo', get_user_info,
                        returns={'name': str, 'email': str, 'user_id': int},
                        args={'user_id': int})
```

## Integration with Web2py

### SOAP Client in Controllers
```python
def call_external_service():
    """Call external SOAP service from Web2py controller"""
    from gluon.contrib import pysimplesoap
    
    try:
        # Create client
        client = pysimplesoap.SoapClient(
            wsdl="http://external-service.com/api?wsdl",
            timeout=pysimplesoap.TIMEOUT
        )
        
        # Call service
        result = client.GetData(request_id=request.vars.id)
        
        # Process response
        return dict(
            success=True,
            data=result,
            message="Service call successful"
        )
        
    except pysimplesoap.SoapFault as e:
        # Handle SOAP faults
        logger.error(f"SOAP Fault: {e.faultcode} - {e.faultstring}")
        return dict(
            success=False,
            error=str(e),
            message="Service call failed"
        )
        
    except Exception as e:
        # Handle other errors
        logger.error(f"Service call error: {str(e)}")
        return dict(
            success=False,
            error=str(e),
            message="Unexpected error"
        )
```

### SOAP Server in Web2py
```python
def soap_service():
    """Expose Web2py functions as SOAP services"""
    from gluon.contrib import pysimplesoap
    
    # Create SOAP dispatcher
    dispatcher = pysimplesoap.SoapDispatcher(
        name="Web2pyService",
        location=URL('default', 'soap_service', scheme=True),
        action=URL('default', 'soap_service', scheme=True),
        namespace="http://web2py.com/services",
        documentation="Web2py SOAP Services"
    )
    
    # Register database operations
    def get_user(user_id):
        """Get user from database"""
        user = db.auth_user(user_id)
        if user:
            return {
                'id': user.id,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name
            }
        else:
            raise pysimplesoap.SoapFault("UserNotFound", "User not found")
    
    def create_user(email, first_name, last_name):
        """Create new user"""
        try:
            user_id = db.auth_user.insert(
                email=email,
                first_name=first_name,
                last_name=last_name
            )
            db.commit()
            return {'user_id': user_id, 'success': True}
        except Exception as e:
            db.rollback()
            raise pysimplesoap.SoapFault("CreateUserFailed", str(e))
    
    # Register methods
    dispatcher.register_function(
        'GetUser', get_user,
        returns={'id': int, 'email': str, 'first_name': str, 'last_name': str},
        args={'user_id': int}
    )
    
    dispatcher.register_function(
        'CreateUser', create_user,
        returns={'user_id': int, 'success': bool},
        args={'email': str, 'first_name': str, 'last_name': str}
    )
    
    # Handle SOAP requests
    if request.env.request_method == 'POST':
        # Process SOAP request
        response.headers['Content-Type'] = 'text/xml; charset=utf-8'
        return dispatcher.dispatch(request.body.read())
    else:
        # Return WSDL
        response.headers['Content-Type'] = 'text/xml; charset=utf-8'
        return dispatcher.wsdl()
```

### Advanced Client Configuration
```python
def configure_soap_client():
    """Advanced SOAP client configuration"""
    from gluon.contrib import pysimplesoap
    
    # Client with authentication
    client = pysimplesoap.SoapClient(
        wsdl="https://secure-service.com/api?wsdl",
        username="api_user",
        password="api_password",
        timeout=60,
        cache=True  # Cache WSDL locally
    )
    
    # Set custom headers
    client.http.headers['User-Agent'] = 'Web2py Application 1.0'
    client.http.headers['X-API-Key'] = 'your-api-key'
    
    # Configure SSL/TLS
    client.http.config['ca_certs'] = '/path/to/ca-bundle.crt'
    client.http.config['cert_reqs'] = 2  # Require valid certificate
    
    return client
```

## Error Handling and Debugging

### SOAP Fault Handling
```python
def handle_soap_errors():
    """Comprehensive SOAP error handling"""
    from gluon.contrib import pysimplesoap
    
    try:
        client = pysimplesoap.SoapClient(wsdl=service_url)
        result = client.ServiceMethod(param1="value1")
        return result
        
    except pysimplesoap.SoapFault as e:
        # SOAP-specific errors
        error_info = {
            'type': 'SOAP Fault',
            'code': e.faultcode,
            'message': e.faultstring,
            'detail': e.detail
        }
        logger.error(f"SOAP Fault: {error_info}")
        return error_info
        
    except pysimplesoap.transport.HTTPError as e:
        # HTTP transport errors
        error_info = {
            'type': 'HTTP Error',
            'status_code': e.code,
            'message': str(e)
        }
        logger.error(f"HTTP Error: {error_info}")
        return error_info
        
    except Exception as e:
        # Other errors
        error_info = {
            'type': 'General Error',
            'message': str(e)
        }
        logger.error(f"Unexpected error: {error_info}")
        return error_info
```

### Debug Configuration
```python
def enable_soap_debugging():
    """Enable detailed SOAP debugging"""
    import logging
    
    # Enable detailed logging
    logging.basicConfig(level=logging.DEBUG)
    
    # Set specific loggers
    logging.getLogger('pysimplesoap.client').setLevel(logging.DEBUG)
    logging.getLogger('pysimplesoap.simplexml').setLevel(logging.DEBUG)
    logging.getLogger('pysimplesoap.transport').setLevel(logging.DEBUG)
    
    # Create client with debugging
    client = pysimplesoap.SoapClient(
        wsdl=service_url,
        trace=True  # Enable request/response tracing
    )
    
    return client
```

## Performance Optimization

### Caching Strategies
```python
def optimize_soap_performance():
    """Optimize SOAP client performance"""
    from gluon.contrib import pysimplesoap
    import pickle
    import os
    
    wsdl_cache_file = os.path.join(request.folder, 'cache', 'service_wsdl.pkl')
    
    # Load cached WSDL if available
    if os.path.exists(wsdl_cache_file):
        with open(wsdl_cache_file, 'rb') as f:
            cached_wsdl = pickle.load(f)
        
        client = pysimplesoap.SoapClient()
        client.services = cached_wsdl['services']
        client.types = cached_wsdl['types']
    else:
        # Parse WSDL and cache it
        client = pysimplesoap.SoapClient(wsdl=service_url)
        
        wsdl_data = {
            'services': client.services,
            'types': client.types
        }
        
        with open(wsdl_cache_file, 'wb') as f:
            pickle.dump(wsdl_data, f)
    
    return client
```

### Connection Pooling
```python
def soap_connection_pooling():
    """Implement connection pooling for SOAP clients"""
    from gluon.contrib import pysimplesoap
    
    # Global client pool
    if 'soap_clients' not in globals():
        global soap_clients
        soap_clients = {}
    
    def get_soap_client(service_name, wsdl_url):
        """Get or create SOAP client from pool"""
        if service_name not in soap_clients:
            soap_clients[service_name] = pysimplesoap.SoapClient(
                wsdl=wsdl_url,
                timeout=pysimplesoap.TIMEOUT
            )
        return soap_clients[service_name]
    
    # Usage
    client = get_soap_client('UserService', 'http://api.example.com/users?wsdl')
    return client
```

## Security Considerations

### Authentication Methods
```python
def secure_soap_client():
    """Create secure SOAP client with authentication"""
    from gluon.contrib import pysimplesoap
    
    # Basic authentication
    client = pysimplesoap.SoapClient(
        wsdl=service_url,
        username="secure_user",
        password="secure_password"
    )
    
    # WS-Security username token
    client.wsse = pysimplesoap.UsernameToken(
        username="ws_user",
        password="ws_password"
    )
    
    # Custom headers for API keys
    client.http.headers.update({
        'Authorization': 'Bearer your-jwt-token',
        'X-API-Key': 'your-api-key'
    })
    
    return client
```

### Input Validation
```python
def validate_soap_inputs():
    """Validate SOAP service inputs"""
    from gluon.contrib import pysimplesoap
    
    def secure_soap_method(user_input):
        # Validate and sanitize inputs
        if not isinstance(user_input, str):
            raise ValueError("Input must be string")
        
        if len(user_input) > 1000:
            raise ValueError("Input too long")
        
        # Remove potentially dangerous characters
        sanitized_input = re.sub(r'[<>&"]', '', user_input)
        
        # Call SOAP service with sanitized input
        client = pysimplesoap.SoapClient(wsdl=service_url)
        return client.ProcessData(data=sanitized_input)
    
    return secure_soap_method
```

## Best Practices

### Development Guidelines
1. **Error Handling**: Always wrap SOAP calls in try-catch blocks
2. **Timeout Configuration**: Set appropriate timeouts for service calls
3. **Caching**: Cache WSDL documents for better performance
4. **Logging**: Enable appropriate logging for debugging and monitoring
5. **Security**: Use secure authentication methods and validate inputs

### Production Deployment
1. **Connection Pooling**: Reuse SOAP client instances
2. **Monitoring**: Monitor service availability and performance
3. **Fallback Strategies**: Implement fallback mechanisms for service failures
4. **Rate Limiting**: Implement rate limiting for outbound service calls

This package provides comprehensive SOAP web services capabilities for Web2py applications, enabling integration with external services and exposure of application functionality as web services while maintaining security and performance standards.