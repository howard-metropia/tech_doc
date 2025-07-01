# XML-RPC Module

## Overview
The XML-RPC module provides XML-RPC (Remote Procedure Call) server capabilities for web2py applications. It enables applications to expose Python functions as web services that can be called remotely using the XML-RPC protocol. This module offers a simple, standards-based approach to creating web APIs for inter-system communication.

## Core Components

### handler() Function
Main XML-RPC request handler that processes incoming XML-RPC calls.

```python
def handler(request, response, methods):
    """
    Handle XML-RPC requests
    
    Args:
        request: Web2py request object
        response: Web2py response object  
        methods: List of functions to expose via XML-RPC
    
    Returns:
        XML-RPC response data
    """
    response.session_id = None  # Disable sessions for XML-RPC
    
    # Create dispatcher
    dispatcher = SimpleXMLRPCDispatcher(allow_none=True, encoding=None)
    
    # Register methods
    for method in methods:
        dispatcher.register_function(method)
    
    # Enable introspection
    dispatcher.register_introspection_functions()
    
    # Set response headers
    response.headers["Content-Type"] = "text/xml"
    
    # Get dispatch function
    dispatch = getattr(dispatcher, "_dispatch", None)
    
    # Process request and return response
    return dispatcher._marshaled_dispatch(request.body.read(), dispatch)
```

### SimpleXMLRPCDispatcher
Uses Python's built-in XML-RPC dispatcher with platform compatibility.

**Python 2:**
```python
from SimpleXMLRPCServer import SimpleXMLRPCDispatcher
```

**Python 3:**
```python
from xmlrpc.server import SimpleXMLRPCDispatcher
```

## Usage Examples

### Basic XML-RPC Service
```python
# In controller (e.g., default.py)
def xmlrpc():
    """XML-RPC service endpoint"""
    
    def add(x, y):
        """Add two numbers"""
        return x + y
    
    def multiply(x, y):
        """Multiply two numbers"""
        return x * y
    
    def get_user_info(user_id):
        """Get user information"""
        user = db.auth_user(user_id)
        if user:
            return {
                'id': user.id,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email
            }
        else:
            raise Exception("User not found")
    
    # Expose methods via XML-RPC
    from gluon.xmlrpc import handler
    return handler(request, response, [add, multiply, get_user_info])
```

### Database Operations
```python
def xmlrpc():
    """XML-RPC service with database operations"""
    
    def create_post(title, content, author_id):
        """Create a new blog post"""
        try:
            post_id = db.posts.insert(
                title=title,
                content=content,
                author_id=author_id,
                created_on=request.now
            )
            db.commit()
            return post_id
        except Exception as e:
            db.rollback()
            raise Exception(str(e))
    
    def get_posts(limit=10):
        """Get recent posts"""
        posts = db(db.posts).select(
            orderby=~db.posts.created_on,
            limitby=(0, limit)
        )
        return [
            {
                'id': post.id,
                'title': post.title,
                'content': post.content,
                'created_on': str(post.created_on)
            }
            for post in posts
        ]
    
    def update_post(post_id, title=None, content=None):
        """Update existing post"""
        post = db.posts(post_id)
        if not post:
            raise Exception("Post not found")
        
        update_data = {}
        if title is not None:
            update_data['title'] = title
        if content is not None:
            update_data['content'] = content
        
        if update_data:
            post.update_record(**update_data)
            db.commit()
            return True
        return False
    
    return handler(request, response, [create_post, get_posts, update_post])
```

### Authentication and Security
```python
def xmlrpc():
    """Secured XML-RPC service"""
    
    def authenticate(username, password):
        """Authenticate user and return session token"""
        user = db(db.auth_user.email == username).select().first()
        if user and auth.verify_password(password, user.password):
            # Create session token
            import uuid
            token = str(uuid.uuid4())
            db.user_sessions.insert(
                user_id=user.id,
                token=token,
                created_on=request.now
            )
            db.commit()
            return token
        else:
            raise Exception("Invalid credentials")
    
    def get_protected_data(token):
        """Get data that requires authentication"""
        session = db(db.user_sessions.token == token).select().first()
        if not session:
            raise Exception("Invalid or expired token")
        
        # Check token age (e.g., 1 hour expiry)
        import datetime
        if (request.now - session.created_on).seconds > 3600:
            raise Exception("Token expired")
        
        # Return protected data
        user = db.auth_user(session.user_id)
        return {
            'user_id': user.id,
            'profile': user.profile,
            'permissions': get_user_permissions(user.id)
        }
    
    return handler(request, response, [authenticate, get_protected_data])
```

### File Operations
```python
def xmlrpc():
    """XML-RPC service with file operations"""
    
    def upload_file(filename, data, description=None):
        """Upload file via XML-RPC"""
        import base64
        import os
        
        try:
            # Decode base64 data
            file_data = base64.b64decode(data)
            
            # Generate safe filename
            import uuid
            safe_filename = "%s_%s" % (uuid.uuid4(), filename)
            file_path = os.path.join(request.folder, 'uploads', safe_filename)
            
            # Save file
            with open(file_path, 'wb') as f:
                f.write(file_data)
            
            # Record in database
            file_id = db.files.insert(
                original_name=filename,
                stored_name=safe_filename,
                description=description,
                size=len(file_data),
                uploaded_on=request.now
            )
            db.commit()
            
            return file_id
            
        except Exception as e:
            raise Exception("Upload failed: %s" % str(e))
    
    def download_file(file_id):
        """Download file via XML-RPC"""
        import base64
        import os
        
        file_record = db.files(file_id)
        if not file_record:
            raise Exception("File not found")
        
        file_path = os.path.join(request.folder, 'uploads', file_record.stored_name)
        
        if not os.path.exists(file_path):
            raise Exception("File not found on disk")
        
        # Read and encode file
        with open(file_path, 'rb') as f:
            file_data = f.read()
        
        return {
            'filename': file_record.original_name,
            'data': base64.b64encode(file_data).decode('utf-8'),
            'size': len(file_data),
            'description': file_record.description
        }
    
    return handler(request, response, [upload_file, download_file])
```

## Client Integration

### Python Client
```python
import xmlrpc.client

# Connect to XML-RPC service
server = xmlrpc.client.ServerProxy('http://localhost:8000/myapp/default/xmlrpc')

# Call remote methods
result = server.add(5, 3)
print("5 + 3 =", result)

# Get user information
user_info = server.get_user_info(1)
print("User:", user_info)

# Handle errors
try:
    user_info = server.get_user_info(999)
except xmlrpc.client.Fault as fault:
    print("Error:", fault.faultString)
```

### JavaScript Client
```javascript
// Using a JavaScript XML-RPC library
const client = new XMLRPCClient('http://localhost:8000/myapp/default/xmlrpc');

// Call remote method
client.call('add', [5, 3], function(error, result) {
    if (error) {
        console.error('Error:', error);
    } else {
        console.log('5 + 3 =', result);
    }
});

// Async/await style
async function getUserInfo(userId) {
    try {
        const userInfo = await client.call('get_user_info', [userId]);
        console.log('User:', userInfo);
    } catch (error) {
        console.error('Error:', error.message);
    }
}
```

### PHP Client
```php
<?php
// PHP XML-RPC client
$client = new XMLRPCClient('http://localhost:8000/myapp/default/xmlrpc');

// Call remote method
$result = $client->call('add', array(5, 3));
echo "5 + 3 = " . $result . "\n";

// Handle errors
try {
    $userInfo = $client->call('get_user_info', array(999));
} catch (Exception $e) {
    echo "Error: " . $e->getMessage() . "\n";
}
?>
```

## Advanced Features

### Custom Data Types
```python
def xmlrpc():
    """XML-RPC with custom data types"""
    
    def get_complex_data():
        """Return complex data structure"""
        return {
            'timestamp': str(request.now),
            'server_info': {
                'version': '2.21.1',
                'platform': 'web2py'
            },
            'data': [
                {'id': 1, 'name': 'Item 1', 'active': True},
                {'id': 2, 'name': 'Item 2', 'active': False}
            ],
            'metadata': {
                'total_count': 2,
                'page_size': 10,
                'has_more': False
            }
        }
    
    def process_array(items):
        """Process array of items"""
        results = []
        for item in items:
            if isinstance(item, dict) and 'value' in item:
                results.append(item['value'] * 2)
            else:
                results.append(str(item).upper())
        return results
    
    return handler(request, response, [get_complex_data, process_array])
```

### Introspection Support
```python
def xmlrpc():
    """XML-RPC with introspection enabled"""
    
    def system_list_methods():
        """List all available methods (automatic)"""
        pass  # Handled by introspection
    
    def system_method_help(method_name):
        """Get help for specific method (automatic)"""
        pass  # Handled by introspection
    
    def add(x, y):
        """Add two numbers together.
        
        Args:
            x (int/float): First number
            y (int/float): Second number
            
        Returns:
            int/float: Sum of x and y
        """
        return x + y
    
    # Introspection methods are automatically registered
    return handler(request, response, [add])
```

### Error Handling and Logging
```python
def xmlrpc():
    """XML-RPC with comprehensive error handling"""
    
    import logging
    logger = logging.getLogger('xmlrpc')
    
    def safe_divide(x, y):
        """Safely divide two numbers"""
        try:
            logger.info("Dividing %s by %s", x, y)
            
            if y == 0:
                raise Exception("Division by zero not allowed")
            
            result = x / y
            logger.info("Result: %s", result)
            return result
            
        except Exception as e:
            logger.error("Error in safe_divide: %s", str(e))
            raise  # Re-raise to send to client
    
    def validate_and_process(data):
        """Validate input and process"""
        try:
            # Input validation
            if not isinstance(data, dict):
                raise Exception("Data must be a dictionary")
            
            if 'required_field' not in data:
                raise Exception("Missing required field")
            
            # Process data
            result = process_data(data)
            
            # Log success
            logger.info("Successfully processed data for %s", 
                       data.get('user_id', 'unknown'))
            
            return result
            
        except Exception as e:
            logger.error("Validation/processing error: %s", str(e))
            raise
    
    return handler(request, response, [safe_divide, validate_and_process])
```

## Configuration and Security

### Request Validation
```python
def xmlrpc():
    """XML-RPC with request validation"""
    
    # Validate request source
    allowed_ips = ['127.0.0.1', '192.168.1.0/24']
    client_ip = request.env.remote_addr
    
    if not is_allowed_ip(client_ip, allowed_ips):
        raise HTTP(403, "Access denied")
    
    # Rate limiting
    if is_rate_limited(client_ip):
        raise HTTP(429, "Too many requests")
    
    def protected_method(token, data):
        """Method requiring authentication"""
        if not validate_token(token):
            raise Exception("Invalid authentication token")
        
        return process_protected_data(data)
    
    return handler(request, response, [protected_method])
```

### CORS Support
```python
def xmlrpc():
    """XML-RPC with CORS support"""
    
    # Handle CORS preflight
    if request.env.request_method == 'OPTIONS':
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'POST, OPTIONS'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
        return ''
    
    # Set CORS headers for actual request
    response.headers['Access-Control-Allow-Origin'] = '*'
    
    def cross_origin_method(data):
        """Method accessible from browser"""
        return {'status': 'success', 'data': data}
    
    return handler(request, response, [cross_origin_method])
```

## Performance Optimization

### Caching
```python
def xmlrpc():
    """XML-RPC with caching"""
    
    @cache.action(time_expire=300)  # Cache for 5 minutes
    def get_expensive_data(category):
        """Get data that's expensive to compute"""
        # Expensive operation
        return expensive_computation(category)
    
    def get_cached_result(cache_key):
        """Get result from cache"""
        result = cache.ram(cache_key, lambda: None, time_expire=0)
        if result is None:
            raise Exception("Cache miss")
        return result
    
    return handler(request, response, [get_expensive_data, get_cached_result])
```

### Connection Pooling
```python
def xmlrpc():
    """XML-RPC optimized for database connections"""
    
    def bulk_operation(items):
        """Perform bulk database operations"""
        try:
            # Use transaction for bulk operations
            with db.execution_context():
                results = []
                for item in items:
                    result = db.table.insert(**item)
                    results.append(result)
                db.commit()
                return results
        except Exception as e:
            db.rollback()
            raise Exception("Bulk operation failed: %s" % str(e))
    
    return handler(request, response, [bulk_operation])
```

## Testing

### Unit Testing
```python
def test_xmlrpc_methods():
    """Test XML-RPC methods"""
    
    # Test add function
    def add(x, y):
        return x + y
    
    assert add(2, 3) == 5
    assert add(-1, 1) == 0
    
    # Test with XML-RPC handler
    from gluon.xmlrpc import handler
    
    # Mock request/response
    class MockRequest:
        def __init__(self, body):
            self.body = MockBody(body)
    
    class MockBody:
        def __init__(self, data):
            self.data = data
        def read(self):
            return self.data
    
    class MockResponse:
        def __init__(self):
            self.headers = {}
            self.session_id = None
    
    # Test XML-RPC call
    xml_request = '''<?xml version="1.0"?>
    <methodCall>
        <methodName>add</methodName>
        <params>
            <param><value><int>5</int></value></param>
            <param><value><int>3</int></value></param>
        </params>
    </methodCall>'''
    
    request = MockRequest(xml_request.encode('utf-8'))
    response = MockResponse()
    
    result = handler(request, response, [add])
    assert '8' in result  # Result should contain 8
```

## Best Practices

### API Design
1. Use clear, descriptive method names
2. Implement proper error handling
3. Validate all inputs
4. Document method signatures
5. Version your API appropriately

### Security
1. Implement authentication for sensitive operations
2. Validate and sanitize all inputs
3. Use HTTPS in production
4. Implement rate limiting
5. Log security events

### Performance
1. Cache expensive operations
2. Use database transactions appropriately
3. Implement pagination for large results
4. Monitor response times
5. Optimize database queries

## See Also
- XML-RPC specification (http://xmlrpc.scripting.com/spec.html)
- Python xmlrpc documentation
- Web2py services and APIs guide
- RESTful web services comparison