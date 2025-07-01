# PySimpleSOAP Server Module

**File**: `gluon/contrib/pysimplesoap/server.py`  
**Type**: SOAP Server Implementation  
**Framework**: Web2py Gluon Framework  
**License**: LGPL 3.0

## Overview

This module provides the SOAP server implementation for exposing Python functions as SOAP web services. It includes automatic WSDL generation, request dispatching, type validation, and comprehensive fault handling for robust web service publishing.

## Core Classes

### SoapDispatcher Class
The main class for creating SOAP web services:

```python
class SoapDispatcher:
    def __init__(self, name, location, action=None, namespace=None,
                 documentation="", trace=False, debug=False,
                 ns_map={}, pretty=False, prefix="", 
                 soap_uri="http://schemas.xmlsoap.org/soap/envelope/",
                 soap_headers=None):
        # Initialize SOAP service dispatcher
```

### SoapFault Class
Exception class for SOAP server errors:

```python
class SoapFault(Exception):
    def __init__(self, faultcode=None, faultstring=None, detail=None):
        self.faultcode = faultcode or self.__class__.__name__
        self.faultstring = faultstring or ''
        self.detail = detail
```

## Key Features

### Service Publishing
- **Function Registration**: Expose Python functions as SOAP operations
- **WSDL Generation**: Automatic WSDL document creation
- **Type Validation**: Input/output parameter validation
- **Documentation**: Service and method documentation support

### Request Processing
- **SOAP Envelope Parsing**: Process incoming SOAP requests
- **Method Dispatching**: Route requests to appropriate functions
- **Parameter Conversion**: Convert SOAP parameters to Python objects
- **Response Generation**: Create SOAP response envelopes

## Usage Examples

### Basic SOAP Service
```python
from gluon.contrib import pysimplesoap

def create_basic_service():
    """Create basic SOAP service"""
    
    # Create dispatcher
    dispatcher = pysimplesoap.SoapDispatcher(
        name="BasicService",
        location="http://localhost:8080/soap",
        action="http://localhost:8080/soap",
        namespace="http://example.com/basicservice",
        documentation="Basic SOAP Service Example"
    )
    
    # Define service methods
    def add_numbers(a, b):
        """Add two numbers"""
        return a + b
    
    def get_greeting(name):
        """Get personalized greeting"""
        return f"Hello, {name}!"
    
    def get_current_time():
        """Get current server time"""
        import datetime
        return datetime.datetime.now().isoformat()
    
    # Register methods
    dispatcher.register_function(
        'AddNumbers', add_numbers,
        returns={'result': int},
        args={'a': int, 'b': int},
        doc="Add two integer numbers"
    )
    
    dispatcher.register_function(
        'GetGreeting', get_greeting,
        returns={'greeting': str},
        args={'name': str},
        doc="Get personalized greeting message"
    )
    
    dispatcher.register_function(
        'GetCurrentTime', get_current_time,
        returns={'timestamp': str},
        args={},
        doc="Get current server timestamp"
    )
    
    return dispatcher
```

### Web2py SOAP Service Integration
```python
def soap_endpoint():
    """Web2py SOAP service endpoint"""
    from gluon.contrib import pysimplesoap
    
    # Create dispatcher
    dispatcher = pysimplesoap.SoapDispatcher(
        name="Web2pyService",
        location=URL('default', 'soap_endpoint', scheme=True),
        action=URL('default', 'soap_endpoint', scheme=True),
        namespace="http://web2py.com/services",
        documentation="Web2py SOAP Services"
    )
    
    # Database operations
    def get_user_by_id(user_id):
        """Get user information by ID"""
        user = db.auth_user(user_id)
        if not user:
            raise pysimplesoap.SoapFault("UserNotFound", "User not found")
        
        return {
            'id': user.id,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'registration_date': user.registration_key or ''
        }
    
    def create_user(email, first_name, last_name, password):
        """Create new user account"""
        try:
            # Validate email
            if db(db.auth_user.email == email).count():
                raise pysimplesoap.SoapFault("EmailExists", "Email already registered")
            
            # Create user
            user_id = db.auth_user.insert(
                email=email,
                first_name=first_name,
                last_name=last_name,
                password=db.auth_user.password.validate(password)[0]
            )
            db.commit()
            
            return {
                'user_id': user_id,
                'success': True,
                'message': 'User created successfully'
            }
            
        except Exception as e:
            db.rollback()
            raise pysimplesoap.SoapFault("CreateUserFailed", str(e))
    
    def get_user_count():
        """Get total number of users"""
        count = db(db.auth_user.id > 0).count()
        return {'count': count}
    
    # Register database operations
    dispatcher.register_function(
        'GetUserById', get_user_by_id,
        returns={
            'id': int, 'email': str, 'first_name': str,
            'last_name': str, 'registration_date': str
        },
        args={'user_id': int},
        doc="Retrieve user information by user ID"
    )
    
    dispatcher.register_function(
        'CreateUser', create_user,
        returns={'user_id': int, 'success': bool, 'message': str},
        args={'email': str, 'first_name': str, 'last_name': str, 'password': str},
        doc="Create new user account"
    )
    
    dispatcher.register_function(
        'GetUserCount', get_user_count,
        returns={'count': int},
        args={},
        doc="Get total number of registered users"
    )
    
    # Handle requests
    if request.env.request_method == 'POST':
        # Process SOAP request
        response.headers['Content-Type'] = 'text/xml; charset=utf-8'
        soap_request = request.body.read()
        return dispatcher.dispatch(soap_request)
    else:
        # Return WSDL
        response.headers['Content-Type'] = 'text/xml; charset=utf-8'
        return dispatcher.wsdl()
```

### Complex Type Handling
```python
def complex_type_service():
    """SOAP service with complex types"""
    from gluon.contrib import pysimplesoap
    
    dispatcher = pysimplesoap.SoapDispatcher(
        name="ComplexTypeService",
        location=URL('default', 'complex_soap', scheme=True),
        action=URL('default', 'complex_soap', scheme=True),
        namespace="http://example.com/complex"
    )
    
    def process_order(order_data):
        """Process order with complex data structure"""
        # order_data structure:
        # {
        #     'customer': {'name': str, 'email': str, 'phone': str},
        #     'items': [{'product_id': int, 'quantity': int, 'price': float}],
        #     'shipping_address': {'street': str, 'city': str, 'state': str, 'zip': str}
        # }
        
        # Validate order data
        if not order_data.get('customer') or not order_data.get('items'):
            raise pysimplesoap.SoapFault("InvalidOrder", "Order must include customer and items")
        
        # Calculate total
        total = sum(item['quantity'] * item['price'] for item in order_data['items'])
        
        # Create order record
        order_id = db.orders.insert(
            customer_name=order_data['customer']['name'],
            customer_email=order_data['customer']['email'],
            total_amount=total,
            status='pending'
        )
        
        # Create order items
        for item in order_data['items']:
            db.order_items.insert(
                order_id=order_id,
                product_id=item['product_id'],
                quantity=item['quantity'],
                price=item['price']
            )
        
        db.commit()
        
        return {
            'order_id': order_id,
            'total_amount': total,
            'status': 'created',
            'message': 'Order processed successfully'
        }
    
    def get_order_status(order_id):
        """Get order status and details"""
        order = db.orders(order_id)
        if not order:
            raise pysimplesoap.SoapFault("OrderNotFound", "Order not found")
        
        # Get order items
        items = db(db.order_items.order_id == order_id).select()
        
        return {
            'order_id': order.id,
            'customer_name': order.customer_name,
            'total_amount': float(order.total_amount),
            'status': order.status,
            'item_count': len(items),
            'created_date': order.created_on.isoformat() if order.created_on else ''
        }
    
    # Register complex type methods
    dispatcher.register_function(
        'ProcessOrder', process_order,
        returns={
            'order_id': int,
            'total_amount': float,
            'status': str,
            'message': str
        },
        args={
            'order_data': {
                'customer': {'name': str, 'email': str, 'phone': str},
                'items': [{'product_id': int, 'quantity': int, 'price': float}],
                'shipping_address': {'street': str, 'city': str, 'state': str, 'zip': str}
            }
        },
        doc="Process customer order with complex data structure"
    )
    
    dispatcher.register_function(
        'GetOrderStatus', get_order_status,
        returns={
            'order_id': int,
            'customer_name': str,
            'total_amount': float,
            'status': str,
            'item_count': int,
            'created_date': str
        },
        args={'order_id': int},
        doc="Get order status and summary information"
    )
    
    return dispatcher
```

## Advanced Features

### Authentication and Security
```python
def secure_soap_service():
    """SOAP service with authentication"""
    from gluon.contrib import pysimplesoap
    
    dispatcher = pysimplesoap.SoapDispatcher(
        name="SecureService",
        location=URL('default', 'secure_soap', scheme=True, host=True),
        action=URL('default', 'secure_soap', scheme=True, host=True),
        namespace="https://secure.example.com/services"
    )
    
    def authenticate_request(username, password):
        """Authenticate SOAP request"""
        # Check credentials
        user = db((db.auth_user.email == username) & 
                 (db.auth_user.password == db.auth_user.password.validate(password)[0])).select().first()
        
        if not user:
            raise pysimplesoap.SoapFault("AuthenticationFailed", "Invalid credentials")
        
        return user
    
    def secure_get_user_data(username, password, target_user_id):
        """Secure method requiring authentication"""
        # Authenticate first
        auth_user = authenticate_request(username, password)
        
        # Check authorization (example: users can only access their own data)
        if auth_user.id != target_user_id and not auth_user.is_admin:
            raise pysimplesoap.SoapFault("AccessDenied", "Access denied")
        
        # Return user data
        target_user = db.auth_user(target_user_id)
        if not target_user:
            raise pysimplesoap.SoapFault("UserNotFound", "User not found")
        
        return {
            'id': target_user.id,
            'email': target_user.email,
            'first_name': target_user.first_name,
            'last_name': target_user.last_name
        }
    
    # Register secure method
    dispatcher.register_function(
        'SecureGetUserData', secure_get_user_data,
        returns={'id': int, 'email': str, 'first_name': str, 'last_name': str},
        args={'username': str, 'password': str, 'target_user_id': int},
        doc="Securely retrieve user data with authentication"
    )
    
    return dispatcher
```

### Error Handling and Logging
```python
def logging_soap_service():
    """SOAP service with comprehensive logging"""
    from gluon.contrib import pysimplesoap
    import logging
    
    # Configure logging
    soap_logger = logging.getLogger('soap_service')
    soap_logger.setLevel(logging.INFO)
    
    dispatcher = pysimplesoap.SoapDispatcher(
        name="LoggingService",
        location=URL('default', 'logging_soap', scheme=True),
        action=URL('default', 'logging_soap', scheme=True),
        namespace="http://example.com/logging",
        trace=True  # Enable request/response tracing
    )
    
    def logged_operation(operation_type, data):
        """Operation with comprehensive logging"""
        request_id = str(uuid.uuid4())
        
        try:
            # Log incoming request
            soap_logger.info(f"Request {request_id}: {operation_type} operation started")
            soap_logger.debug(f"Request {request_id}: Data = {data}")
            
            # Process operation
            if operation_type == 'create':
                result = db.data_table.insert(content=data)
                db.commit()
                soap_logger.info(f"Request {request_id}: Created record {result}")
                
            elif operation_type == 'read':
                result = db(db.data_table.id == int(data)).select().first()
                if not result:
                    raise pysimplesoap.SoapFault("NotFound", "Record not found")
                result = result.as_dict()
                soap_logger.info(f"Request {request_id}: Retrieved record")
                
            elif operation_type == 'update':
                record_id, new_data = data.split(':', 1)
                updated = db(db.data_table.id == int(record_id)).update(content=new_data)
                db.commit()
                if not updated:
                    raise pysimplesoap.SoapFault("NotFound", "Record not found")
                result = {'updated': True, 'id': int(record_id)}
                soap_logger.info(f"Request {request_id}: Updated record {record_id}")
                
            elif operation_type == 'delete':
                deleted = db(db.data_table.id == int(data)).delete()
                db.commit()
                if not deleted:
                    raise pysimplesoap.SoapFault("NotFound", "Record not found")
                result = {'deleted': True, 'id': int(data)}
                soap_logger.info(f"Request {request_id}: Deleted record {data}")
                
            else:
                raise pysimplesoap.SoapFault("InvalidOperation", "Unsupported operation")
            
            # Log successful completion
            soap_logger.info(f"Request {request_id}: Operation completed successfully")
            
            return {
                'request_id': request_id,
                'success': True,
                'result': result
            }
            
        except pysimplesoap.SoapFault:
            # Re-raise SOAP faults
            soap_logger.error(f"Request {request_id}: SOAP fault occurred")
            raise
            
        except Exception as e:
            # Log and convert other exceptions
            soap_logger.error(f"Request {request_id}: Unexpected error: {str(e)}")
            raise pysimplesoap.SoapFault("InternalError", f"Internal server error: {str(e)}")
    
    # Register logged operation
    dispatcher.register_function(
        'LoggedOperation', logged_operation,
        returns={'request_id': str, 'success': bool, 'result': dict},
        args={'operation_type': str, 'data': str},
        doc="Perform operation with comprehensive logging"
    )
    
    return dispatcher
```

## Performance Optimization

### Caching and Performance
```python
def optimized_soap_service():
    """Performance-optimized SOAP service"""
    from gluon.contrib import pysimplesoap
    
    # Cache for expensive operations
    operation_cache = {}
    
    dispatcher = pysimplesoap.SoapDispatcher(
        name="OptimizedService",
        location=URL('default', 'optimized_soap', scheme=True),
        action=URL('default', 'optimized_soap', scheme=True),
        namespace="http://example.com/optimized"
    )
    
    def cached_expensive_operation(input_data):
        """Expensive operation with caching"""
        cache_key = hashlib.md5(str(input_data).encode()).hexdigest()
        
        # Check cache
        if cache_key in operation_cache:
            cache_entry = operation_cache[cache_key]
            if time.time() - cache_entry['timestamp'] < 300:  # 5 minutes
                return cache_entry['result']
        
        # Perform expensive calculation
        import time
        time.sleep(0.1)  # Simulate expensive operation
        result = {
            'processed_data': input_data.upper(),
            'processing_time': 0.1,
            'timestamp': time.time()
        }
        
        # Cache result
        operation_cache[cache_key] = {
            'result': result,
            'timestamp': time.time()
        }
        
        return result
    
    def bulk_operation(data_list):
        """Process multiple items efficiently"""
        results = []
        
        # Process in batches for better performance
        batch_size = 10
        for i in range(0, len(data_list), batch_size):
            batch = data_list[i:i+batch_size]
            
            # Batch database operations
            batch_results = []
            for item in batch:
                # Simulate processing
                batch_results.append({
                    'input': item,
                    'processed': item * 2 if isinstance(item, (int, float)) else str(item).upper()
                })
            
            results.extend(batch_results)
        
        return {
            'total_processed': len(results),
            'results': results
        }
    
    # Register optimized methods
    dispatcher.register_function(
        'CachedExpensiveOperation', cached_expensive_operation,
        returns={'processed_data': str, 'processing_time': float, 'timestamp': float},
        args={'input_data': str},
        doc="Expensive operation with result caching"
    )
    
    dispatcher.register_function(
        'BulkOperation', bulk_operation,
        returns={'total_processed': int, 'results': list},
        args={'data_list': list},
        doc="Process multiple items efficiently in batches"
    )
    
    return dispatcher
```

## Best Practices

### Service Design Guidelines
1. **Clear Interfaces**: Define clear input/output parameters
2. **Error Handling**: Use SOAP faults for proper error communication
3. **Documentation**: Provide comprehensive service documentation
4. **Validation**: Validate all input parameters
5. **Security**: Implement proper authentication and authorization

### Performance Considerations
1. **Caching**: Cache expensive operations and results
2. **Batch Processing**: Support bulk operations when possible
3. **Database Optimization**: Use efficient database queries
4. **Resource Management**: Properly manage memory and connections
5. **Monitoring**: Log service usage and performance metrics

### Security Best Practices
1. **Authentication**: Implement robust authentication mechanisms
2. **Input Validation**: Validate and sanitize all input data
3. **Error Messages**: Don't expose sensitive information in error messages
4. **Rate Limiting**: Implement rate limiting for service calls
5. **Audit Logging**: Log all service operations for security auditing

This module provides comprehensive SOAP server capabilities for Web2py applications, enabling the exposure of application functionality as standards-compliant web services while maintaining security, performance, and reliability.