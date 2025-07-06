# PySimpleSOAP Client Module

**File**: `gluon/contrib/pysimplesoap/client.py`  
**Type**: SOAP Client Implementation  
**Framework**: Web2py Gluon Framework  
**License**: LGPL 3.0

## Overview

This module provides the SOAP client implementation for consuming SOAP web services. It includes automatic WSDL parsing, method introspection, type mapping, and comprehensive error handling for robust web service integration.

## Core Classes

### SoapClient Class
The main class for consuming SOAP web services:

```python
class SoapClient:
    def __init__(self, wsdl=None, location=None, action=None,
                 namespace=None, soap_ns='soap', trace=False,
                 exceptions=True, proxy=None, ns=None, 
                 username=None, password=None, cache=None,
                 timeout=TIMEOUT):
        # Initialize SOAP client with service configuration
```

### SoapFault Class
Exception class for SOAP-specific errors:

```python
class SoapFault(RuntimeError):
    def __init__(self, faultcode, faultstring, detail=None):
        self.faultcode = faultcode
        self.faultstring = faultstring
        self.detail = detail
```

## Key Features

### WSDL Processing
- **Automatic Discovery**: Parse WSDL documents to discover services
- **Method Generation**: Dynamically create Python methods from WSDL operations
- **Type Mapping**: Convert between Python types and SOAP/XML types
- **Namespace Handling**: Full support for XML namespaces

### Request/Response Handling
- **XML Generation**: Automatic SOAP envelope creation
- **Parameter Marshalling**: Convert Python objects to SOAP parameters
- **Response Parsing**: Parse SOAP responses into Python objects
- **Error Processing**: Handle SOAP faults and HTTP errors

## Usage Examples

### Basic SOAP Client
```python
from gluon.contrib import pysimplesoap

def create_basic_client():
    """Create basic SOAP client"""
    client = pysimplesoap.SoapClient(
        wsdl="http://example.com/service?wsdl",
        timeout=30,
        trace=True  # Enable request/response logging
    )
    
    # Call service method
    try:
        response = client.GetUserInfo(user_id=123)
        return {
            'name': response.Name,
            'email': response.Email,
            'status': response.Status
        }
    except pysimplesoap.SoapFault as e:
        logger.error(f"SOAP Fault: {e.faultcode} - {e.faultstring}")
        raise
```

### Client with Authentication
```python
def create_authenticated_client():
    """Create SOAP client with authentication"""
    client = pysimplesoap.SoapClient(
        wsdl="https://secure-api.example.com/service?wsdl",
        username="api_user",
        password="api_password",
        timeout=60
    )
    
    # Additional security headers
    client.http.headers.update({
        'X-API-Key': 'your-api-key',
        'User-Agent': 'Web2py SOAP Client 1.0'
    })
    
    return client
```

### Manual Service Configuration
```python
def create_manual_client():
    """Create SOAP client without WSDL"""
    client = pysimplesoap.SoapClient(
        location="http://example.com/soap/endpoint",
        action="http://example.com/soap/action",
        namespace="http://example.com/soap/namespace",
        soap_ns="soap"
    )
    
    # Manually define service method
    client.services = {
        'ServiceName': {
            'ports': {
                'ServicePort': {
                    'location': client.location,
                    'binding': 'ServiceBinding'
                }
            }
        }
    }
    
    return client
```

## Advanced Features

### Complex Type Handling
```python
def handle_complex_types():
    """Handle complex SOAP types"""
    from gluon.contrib import pysimplesoap
    
    client = pysimplesoap.SoapClient(wsdl=service_url)
    
    # Create complex type object
    address = pysimplesoap.Struct()
    address.Street = "123 Main St"
    address.City = "Anytown"
    address.State = "CA"
    address.ZipCode = "12345"
    
    person = pysimplesoap.Struct()
    person.Name = "John Doe"
    person.Email = "john@example.com"
    person.Address = address
    
    # Call service with complex type
    response = client.CreatePerson(person_data=person)
    return response
```

### Array and List Handling
```python
def handle_arrays():
    """Handle SOAP arrays and lists"""
    from gluon.contrib import pysimplesoap
    
    client = pysimplesoap.SoapClient(wsdl=service_url)
    
    # Simple array
    user_ids = [1, 2, 3, 4, 5]
    response = client.GetMultipleUsers(user_ids=user_ids)
    
    # Array of complex objects
    products = []
    for i in range(3):
        product = pysimplesoap.Struct()
        product.Id = i + 1
        product.Name = f"Product {i + 1}"
        product.Price = 10.99 * (i + 1)
        products.append(product)
    
    response = client.CreateProducts(products=products)
    return response
```

### Custom Headers and Namespaces
```python
def custom_headers_namespaces():
    """Handle custom headers and namespaces"""
    from gluon.contrib import pysimplesoap
    
    client = pysimplesoap.SoapClient(wsdl=service_url)
    
    # Add custom SOAP headers
    security_header = pysimplesoap.SimpleXMLElement("""
        <Security xmlns="http://schemas.xmlsoap.org/ws/2005/07/secext">
            <UsernameToken>
                <Username>user</Username>
                <Password>pass</Password>
            </UsernameToken>
        </Security>
    """)
    
    client.headers = [security_header]
    
    # Custom namespace mapping
    client.namespace_prefixes = {
        'custom': 'http://example.com/custom',
        'ext': 'http://external.com/types'
    }
    
    return client
```

## Integration with Web2py

### Controller Integration
```python
def soap_service_call():
    """Integrate SOAP client in Web2py controller"""
    from gluon.contrib import pysimplesoap
    
    # Get service configuration from database or settings
    service_config = db.soap_services(request.vars.service_id)
    
    if not service_config:
        raise HTTP(404, "Service not found")
    
    try:
        # Create client
        client = pysimplesoap.SoapClient(
            wsdl=service_config.wsdl_url,
            username=service_config.username,
            password=service_config.password,
            timeout=30
        )
        
        # Prepare parameters from form/request
        params = {}
        for param_name in request.vars:
            if param_name.startswith('param_'):
                actual_name = param_name[6:]  # Remove 'param_' prefix
                params[actual_name] = request.vars[param_name]
        
        # Call service method
        method_name = request.vars.method or 'GetData'
        method = getattr(client, method_name)
        response = method(**params)
        
        # Return JSON response
        return dict(
            success=True,
            data=response,
            message="Service call successful"
        )
        
    except pysimplesoap.SoapFault as e:
        return dict(
            success=False,
            error={
                'type': 'SOAPFault',
                'code': e.faultcode,
                'message': e.faultstring,
                'detail': e.detail
            }
        )
    except Exception as e:
        logger.error(f"SOAP service call failed: {str(e)}")
        return dict(
            success=False,
            error={
                'type': 'Exception',
                'message': str(e)
            }
        )
```

### Service Wrapper Class
```python
class SOAPServiceWrapper:
    """Wrapper class for SOAP services in Web2py"""
    
    def __init__(self, service_name):
        self.service_name = service_name
        self.config = db.soap_configurations(service_name=service_name)
        self.client = None
        
    def get_client(self):
        """Get or create SOAP client"""
        if not self.client:
            self.client = pysimplesoap.SoapClient(
                wsdl=self.config.wsdl_url,
                username=self.config.username,
                password=self.config.password,
                timeout=self.config.timeout or 30,
                cache=True
            )
        return self.client
    
    def call_method(self, method_name, **kwargs):
        """Call SOAP method with error handling"""
        try:
            client = self.get_client()
            method = getattr(client, method_name)
            
            # Log the call
            logger.info(f"Calling SOAP method {method_name} on {self.service_name}")
            
            # Make the call
            response = method(**kwargs)
            
            # Log success
            logger.info(f"SOAP call successful: {method_name}")
            
            return {
                'success': True,
                'data': response,
                'timestamp': datetime.datetime.now()
            }
            
        except pysimplesoap.SoapFault as e:
            logger.error(f"SOAP Fault in {method_name}: {e}")
            return {
                'success': False,
                'error': 'SOAP_FAULT',
                'message': f"{e.faultcode}: {e.faultstring}",
                'detail': e.detail
            }
        except Exception as e:
            logger.error(f"Error in SOAP call {method_name}: {e}")
            return {
                'success': False,
                'error': 'GENERAL_ERROR',
                'message': str(e)
            }
    
    def introspect_service(self):
        """Get service methods and types"""
        client = self.get_client()
        
        methods = {}
        for service_name, service in client.services.items():
            for port_name, port in service['ports'].items():
                binding = client.bindings.get(port['binding'], {})
                for operation_name, operation in binding.get('operations', {}).items():
                    methods[operation_name] = {
                        'input': operation.get('input', {}),
                        'output': operation.get('output', {}),
                        'documentation': operation.get('documentation', '')
                    }
        
        return {
            'service_name': self.service_name,
            'methods': methods,
            'types': client.types
        }

# Usage in controller
def manage_soap_services():
    service_name = request.vars.service or 'UserService'
    wrapper = SOAPServiceWrapper(service_name)
    
    if request.vars.action == 'introspect':
        return wrapper.introspect_service()
    elif request.vars.action == 'call':
        method_name = request.vars.method
        params = {k: v for k, v in request.vars.items() 
                 if k.startswith('param_')}
        return wrapper.call_method(method_name, **params)
    else:
        return dict(wrapper=wrapper)
```

## Error Handling and Debugging

### Comprehensive Error Handling
```python
def robust_soap_call(wsdl_url, method_name, **params):
    """Robust SOAP call with comprehensive error handling"""
    from gluon.contrib import pysimplesoap
    
    try:
        # Create client
        client = pysimplesoap.SoapClient(
            wsdl=wsdl_url,
            timeout=30,
            trace=True  # Enable for debugging
        )
        
        # Validate method exists
        if not hasattr(client, method_name):
            available_methods = [attr for attr in dir(client) 
                               if not attr.startswith('_')]
            raise ValueError(f"Method {method_name} not found. "
                           f"Available methods: {available_methods}")
        
        # Call method
        method = getattr(client, method_name)
        response = method(**params)
        
        return {
            'success': True,
            'data': response,
            'request_xml': client.xml_request,
            'response_xml': client.xml_response
        }
        
    except pysimplesoap.SoapFault as e:
        return {
            'success': False,
            'error_type': 'SOAP_FAULT',
            'fault_code': e.faultcode,
            'fault_string': e.faultstring,
            'fault_detail': e.detail,
            'request_xml': getattr(client, 'xml_request', None),
            'response_xml': getattr(client, 'xml_response', None)
        }
        
    except Exception as e:
        return {
            'success': False,
            'error_type': 'GENERAL_ERROR',
            'message': str(e),
            'request_xml': getattr(client, 'xml_request', None) if 'client' in locals() else None
        }
```

### Debug and Logging Configuration
```python
def configure_soap_debugging():
    """Configure detailed SOAP debugging"""
    import logging
    
    # Set up logging
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Enable SOAP-specific logging
    soap_logger = logging.getLogger('pysimplesoap')
    soap_logger.setLevel(logging.DEBUG)
    
    # Create debug client
    client = pysimplesoap.SoapClient(
        wsdl=service_url,
        trace=True,  # Log all requests/responses
        exceptions=True  # Raise exceptions for debugging
    )
    
    return client
```

## Performance Optimization

### Client Caching
```python
class CachedSOAPClient:
    """SOAP client with caching capabilities"""
    
    def __init__(self, cache_timeout=3600):
        self.cache_timeout = cache_timeout
        self.clients = {}
        
    def get_client(self, wsdl_url, **kwargs):
        """Get cached client or create new one"""
        cache_key = f"{wsdl_url}_{hash(str(sorted(kwargs.items())))}"
        
        if cache_key not in self.clients:
            self.clients[cache_key] = {
                'client': pysimplesoap.SoapClient(wsdl=wsdl_url, **kwargs),
                'created': time.time()
            }
        
        # Check cache expiration
        cached_item = self.clients[cache_key]
        if time.time() - cached_item['created'] > self.cache_timeout:
            # Refresh client
            cached_item['client'] = pysimplesoap.SoapClient(wsdl=wsdl_url, **kwargs)
            cached_item['created'] = time.time()
        
        return cached_item['client']

# Global cached client instance
cached_soap_client = CachedSOAPClient()
```

### Asynchronous SOAP Calls
```python
def async_soap_calls():
    """Handle multiple SOAP calls asynchronously"""
    import threading
    from queue import Queue
    
    def soap_worker(queue, results, client_config):
        """Worker function for SOAP calls"""
        while True:
            item = queue.get()
            if item is None:
                break
                
            method_name, params, result_key = item
            
            try:
                client = pysimplesoap.SoapClient(**client_config)
                method = getattr(client, method_name)
                result = method(**params)
                results[result_key] = {'success': True, 'data': result}
            except Exception as e:
                results[result_key] = {'success': False, 'error': str(e)}
            
            queue.task_done()
    
    # Setup
    queue = Queue()
    results = {}
    client_config = {'wsdl': service_url, 'timeout': 30}
    
    # Start worker threads
    threads = []
    for i in range(3):  # 3 worker threads
        t = threading.Thread(target=soap_worker, 
                           args=(queue, results, client_config))
        t.start()
        threads.append(t)
    
    # Add tasks
    tasks = [
        ('GetUser', {'user_id': 1}, 'user1'),
        ('GetUser', {'user_id': 2}, 'user2'),
        ('GetUser', {'user_id': 3}, 'user3'),
    ]
    
    for task in tasks:
        queue.put(task)
    
    # Wait for completion
    queue.join()
    
    # Stop workers
    for i in range(3):
        queue.put(None)
    for t in threads:
        t.join()
    
    return results
```

## Best Practices

### Client Configuration
1. **Timeout Settings**: Always set appropriate timeouts
2. **Error Handling**: Implement comprehensive error handling
3. **Caching**: Cache WSDL documents and client instances
4. **Security**: Use secure authentication methods
5. **Logging**: Enable appropriate logging for debugging and monitoring

### Performance Guidelines
1. **Connection Reuse**: Reuse client instances when possible
2. **Batch Operations**: Combine multiple operations when supported
3. **Async Processing**: Use asynchronous calls for multiple services
4. **Resource Management**: Properly manage memory and connections

This module provides robust SOAP client capabilities for Web2py applications, enabling seamless integration with external web services while maintaining performance, security, and reliability standards.