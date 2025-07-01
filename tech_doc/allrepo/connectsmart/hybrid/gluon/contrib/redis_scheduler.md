# Gluon Contrib Redis Scheduler Module

## Overview
Redis-based task scheduler for web2py applications. Provides distributed task scheduling and background job processing using Redis as the message broker and coordination layer.

## Module Information
- **Module**: `gluon.contrib.redis_scheduler`
- **Dependencies**: redis-py, web2py scheduler
- **Purpose**: Distributed task scheduling
- **Use Case**: Background jobs, distributed processing

## Key Features
- **Distributed Processing**: Multiple worker support
- **Redis Backend**: High-performance message queuing
- **Task Persistence**: Reliable job execution
- **Scalability**: Horizontal scaling support
- **Monitoring**: Job status tracking

## Basic Usage

### Scheduler Setup
```python
from gluon.contrib.redis_scheduler import RedisScheduler

# Configure Redis scheduler
scheduler = RedisScheduler(
    db,
    redis_host='localhost',
    redis_port=6379,
    redis_db=0
)

# Define tasks
def send_email(to, subject, body):
    # Email sending logic
    import smtplib
    # ... email implementation
    return f"Email sent to {to}"

# Schedule task
task_id = scheduler.queue_task(
    'send_email',
    pvars={'to': 'user@example.com', 'subject': 'Hello', 'body': 'Test message'},
    timeout=300
)
```

### Background Processing
```python
# Start scheduler worker
if __name__ == '__main__':
    scheduler.loop()
```

This module enables scalable background task processing for web2py applications using Redis as the coordination backend.