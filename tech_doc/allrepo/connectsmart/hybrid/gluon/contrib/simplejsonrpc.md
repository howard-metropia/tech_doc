# Gluon Contrib SimpleJSONRPC Module

## Overview
JSON-RPC implementation for web2py applications. Provides JSON-RPC 2.0 server and client functionality for building remote procedure call APIs using JSON as the data format.

## Module Information
- **Module**: `gluon.contrib.simplejsonrpc`
- **Purpose**: JSON-RPC server/client implementation
- **Standards**: JSON-RPC 2.0 specification
- **Transport**: HTTP-based RPC communication

## Key Features
- **JSON-RPC 2.0**: Full specification compliance
- **Server/Client**: Both server and client implementations
- **Web2py Integration**: Seamless web2py controller integration
- **Error Handling**: Proper RPC error handling
- **Batch Requests**: Support for batch RPC calls

## Basic Usage

### JSON-RPC Server
```python
from gluon.contrib.simplejsonrpc import JsonRpcServer

def jsonrpc():
    """JSON-RPC endpoint"""
    
    def add(a, b):
        """Add two numbers"""
        return a + b
    
    def get_user(user_id):
        """Get user by ID"""
        user = db.users[user_id]
        if user:
            return {'id': user.id, 'name': user.name, 'email': user.email}
        else:
            raise Exception("User not found")
    
    # Create RPC server
    server = JsonRpcServer()
    server.register_function(add)
    server.register_function(get_user)
    
    # Process request
    return server.handle_request(request.body.read())
```

### JSON-RPC Client
```python
from gluon.contrib.simplejsonrpc import JsonRpcClient

# Create client
client = JsonRpcClient('http://localhost:8000/myapp/default/jsonrpc')

# Call remote methods
result = client.add(5, 3)
print(f"5 + 3 = {result}")

user = client.get_user(123)
print(f"User: {user['name']}")
```

### API Integration
```python
def create_api():
    """Create comprehensive JSON-RPC API"""
    
    # User management methods
    def create_user(name, email, password):
        user_id = db.users.insert(
            name=name,
            email=email,
            password=CRYPT()(password)[0]
        )
        db.commit()
        return {'user_id': user_id, 'message': 'User created successfully'}
    
    def update_user(user_id, **kwargs):
        user = db.users[user_id]
        if not user:
            raise Exception("User not found")
        
        user.update_record(**kwargs)
        db.commit()
        return {'message': 'User updated successfully'}
    
    def delete_user(user_id):
        user = db.users[user_id]
        if not user:
            raise Exception("User not found")
        
        db(db.users.id == user_id).delete()
        db.commit()
        return {'message': 'User deleted successfully'}
    
    # Data retrieval methods
    def list_users(limit=10, offset=0):
        users = db(db.users).select(
            limitby=(offset, offset + limit)
        )
        return [
            {'id': user.id, 'name': user.name, 'email': user.email}
            for user in users
        ]
    
    # Register methods
    server = JsonRpcServer()
    server.register_function(create_user)
    server.register_function(update_user)
    server.register_function(delete_user)
    server.register_function(list_users)
    
    return server.handle_request(request.body.read())
```

This module enables JSON-RPC API development for web2py applications, providing standardized remote procedure call functionality.