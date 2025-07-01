# Gluon Contrib SMS Utils Module

## Overview
SMS messaging utilities for web2py applications. Provides SMS sending capabilities through various SMS gateway providers with a unified API interface.

## Module Information
- **Module**: `gluon.contrib.sms_utils`
- **Purpose**: SMS messaging functionality
- **Providers**: Multiple SMS gateway support
- **Integration**: Web2py application integration

## Key Features
- **Multiple Providers**: Support for various SMS gateways
- **Unified API**: Consistent interface across providers
- **Error Handling**: Robust error handling and retry logic
- **Template Support**: SMS template functionality
- **Delivery Tracking**: Message delivery status tracking

## Basic Usage

### Simple SMS Sending
```python
from gluon.contrib.sms_utils import SMS

# Configure SMS provider
sms = SMS(
    provider='twilio',
    account_sid='your_account_sid',
    auth_token='your_auth_token',
    from_number='+1234567890'
)

# Send SMS
result = sms.send(
    to='+1987654321',
    message='Hello from web2py!'
)

if result.success:
    print(f"SMS sent successfully: {result.message_id}")
else:
    print(f"SMS failed: {result.error}")
```

### Bulk SMS
```python
def send_bulk_sms(recipients, message):
    """Send SMS to multiple recipients"""
    
    results = []
    for phone_number in recipients:
        result = sms.send(
            to=phone_number,
            message=message
        )
        results.append({
            'phone': phone_number,
            'success': result.success,
            'message_id': result.message_id if result.success else None,
            'error': result.error if not result.success else None
        })
    
    return results

# Usage
recipients = ['+1234567890', '+1987654321', '+1122334455']
message = "Important notification from MyApp"
results = send_bulk_sms(recipients, message)
```

### Web2py Integration
```python
def notify_user(user_id, message_type, **kwargs):
    """Send SMS notification to user"""
    
    user = db.users[user_id]
    if not user or not user.phone:
        return False, "User phone number not available"
    
    # Get message template
    template = db(
        (db.sms_templates.type == message_type) &
        (db.sms_templates.active == True)
    ).select().first()
    
    if not template:
        return False, "SMS template not found"
    
    # Format message
    message = template.content.format(**kwargs)
    
    # Send SMS
    result = sms.send(
        to=user.phone,
        message=message
    )
    
    # Log SMS
    db.sms_log.insert(
        user_id=user_id,
        phone_number=user.phone,
        message=message,
        message_type=message_type,
        success=result.success,
        message_id=result.message_id,
        error_message=result.error,
        sent_at=datetime.datetime.now()
    )
    
    db.commit()
    return result.success, result.message_id if result.success else result.error
```

This module provides comprehensive SMS messaging capabilities for web2py applications with support for multiple SMS gateway providers.