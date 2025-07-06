# Gluon Contrib Redis Session Module

## Overview
Redis-based session storage for web2py applications. Provides scalable, distributed session management using Redis as the backend, enabling session sharing across multiple application servers.

## Module Information
- **Module**: `gluon.contrib.redis_session`
- **Dependencies**: redis-py
- **Purpose**: Distributed session storage
- **Use Case**: Multi-server deployments, scalability

## Key Features
- **Distributed Sessions**: Share sessions across servers
- **High Performance**: Redis in-memory storage
- **Scalability**: Horizontal scaling support
- **Persistence**: Optional session persistence
- **TTL Support**: Automatic session expiration

## Basic Usage

### Session Configuration
```python
from gluon.contrib.redis_session import RedisSession
import redis

# Configure Redis connection
redis_conn = redis.Redis(
    host='localhost',
    port=6379,
    db=1,  # Use separate DB for sessions
    decode_responses=True
)

# Configure session storage
session.connect(
    request, 
    response, 
    db=RedisSession(redis_conn)
)
```

### Load Balancer Setup
```python
# In models/db.py for load-balanced applications
if not request.env.web2py_runtime_gae:
    # Use Redis sessions for scalability
    session.connect(
        request,
        response,
        db=RedisSession(
            redis.Redis(**REDIS_CONFIG),
            session_cookie_name='web2py_session_id'
        )
    )
```

This module enables scalable session management for web2py applications in distributed environments.