# Slack Helper Module Documentation

## Overview
The Slack Helper Module provides comprehensive Slack Bot integration for the ConnectSmart Hybrid Portal application. It handles message sending, error reporting, and vendor failure notifications with structured formatting and robust error handling.

## File Location
**Source**: `/home/datavan/METROPIA/metro_combine/allrepo/connectsmart/hybrid/applications/portal/modules/slack_helper.py`

## Dependencies
- `json`: JSON data serialization
- `requests`: HTTP client for Slack API
- `datetime`: Timestamp generation

## Constants
- `URL`: Slack API endpoint (`https://slack.com/api/chat.postMessage`)

## Classes

### SlackBotResponse

#### Purpose
Standardized response object for Slack bot operations with status tracking and error handling.

#### Constructor
```python
def __init__(self, status, message=None, error=None)
```

#### Parameters
- `status` (str): Operation status ('success', 'failure', 'error')
- `message` (str, optional): Message that was sent
- `error` (str, optional): Error description

#### Methods

##### `__str__()` and `__repr__()`
**Purpose**: JSON string representation of response object
**Returns**: JSON formatted string with status, message, and error fields

#### Response Structure
```python
{
    'status': str,      # 'success', 'failure', or 'error'
    'message': str,     # Message content (if successful)
    'error': str        # Error description (if failed)
}
```

### SlackManager

#### Purpose
Main class managing Slack bot operations including configuration validation, message sending, and specialized vendor failure reporting.

#### Constructor
```python
def __init__(self, config, logger=None)
```

#### Parameters
- `config` (dict): Configuration dictionary with Slack settings
- `logger` (logging.Logger, optional): Logger instance for error reporting

#### Configuration Requirements
```python
{
    'slack': {
        'channel_id': str,                    # Main channel ID
        'vendor_failed_channel_id': str,      # Vendor failure channel
        'vendor_incorrect_channel_id': str,   # Vendor error channel
        'bot_token': str                      # Bot authentication token
    },
    'project': {
        'name': str,                          # Project name
        'stage': str                          # Environment stage
    }
}
```

#### Methods

##### `send(self, message)`
**Purpose**: Send text message to main Slack channel
**Parameters**:
- `message` (str): Message content to send

**Returns**: `SlackBotResponse` object

**Process**:
1. Create JSON payload with channel and message
2. Set authentication headers with bot token
3. Send POST request to Slack API
4. Parse response and create appropriate `SlackBotResponse`
5. Log errors if logger is available

##### `send_vendor_failed_msg(self, fields)`
**Purpose**: Send structured vendor failure notification with rich formatting
**Parameters**:
- `fields` (dict): Vendor failure information

**Returns**: `SlackBotResponse` object

**Required Fields**:
- `status`: Failure status
- `vendor`: Vendor name
- `vendorApi`: Vendor API endpoint
- `originApi`: Origin API endpoint
- `errorMsg`: Error message
- `meta`: Additional metadata

**Auto-added Fields**:
- `project`: Project name from config
- `stage`: Environment stage from config
- `time`: UTC timestamp in ISO format

## Message Formatting

### Standard Text Messages
```python
payload = {
    'channel': self.channel,
    'text': message
}
```

### Vendor Failure Messages (Structured Blocks)
```python
blocks = [{
    'type': 'section',
    'fields': [
        {
            'type': 'mrkdwn',
            'text': '*Field:*\nValue'
        }
    ]
}]
```

### Field Formatting Order
1. **Project**: Project name
2. **Stage**: Environment stage
3. **Status**: Failure status
4. **Time**: UTC timestamp
5. **Vendor**: Vendor service name
6. **VendorApi**: Vendor API endpoint
7. **OriginApi**: Origin API endpoint
8. **ErrorMsg**: Error message
9. **Meta**: Metadata (formatted as code block)

## Usage Examples

### Basic Setup
```python
config = {
    'slack': {
        'channel_id': 'C1234567890',
        'vendor_failed_channel_id': 'C0987654321',
        'vendor_incorrect_channel_id': 'C1122334455',
        'bot_token': 'xoxb-your-bot-token-here'
    },
    'project': {
        'name': 'ConnectSmart Portal',
        'stage': 'production'
    }
}

slack_manager = SlackManager(config, logger)
```

### Simple Message Sending
```python
# Send notification message
response = slack_manager.send("User registration completed successfully")

if response.status == 'success':
    print("Message sent successfully")
else:
    print(f"Failed to send message: {response.error}")
```

### Vendor Failure Notification
```python
# Report vendor API failure
failure_data = {
    'status': 'FAILED',
    'vendor': 'RideShare API',
    'vendorApi': '/api/v1/book-ride',
    'originApi': '/portal/book-ride',
    'errorMsg': 'Connection timeout after 30 seconds',
    'meta': {
        'user_id': 12345,
        'ride_id': 'ride_789',
        'retry_count': 3,
        'request_data': {
            'pickup': 'Location A',
            'destination': 'Location B'
        }
    }
}

response = slack_manager.send_vendor_failed_msg(failure_data)
```

### Error Handling Pattern
```python
try:
    response = slack_manager.send("Important notification")
    
    if response.status != 'success':
        # Handle Slack API failure
        logger.error(f"Slack notification failed: {response.error}")
        
except Exception as e:
    # Handle unexpected errors
    logger.error(f"Unexpected error in Slack notification: {e}")
```

## Authentication

### Bot Token Format
```python
headers = {
    'Content-Type': 'application/json; charset=utf-8',
    'Authorization': 'Bearer ' + self.token
}
```

### Token Configuration
- Environment variables recommended for tokens
- Support for multiple channel configurations
- Flexible configuration hierarchy

## Error Handling

### HTTP Status Codes
- **200-299**: Success responses
- **401**: Authentication error
- **400-499**: Client errors
- **500-599**: Server errors

### Response Status Mapping
```python
if response.ok:
    res = SlackBotResponse('success', message=message)
else:
    res = SlackBotResponse('failure', error=response.text)
```

### Exception Handling
```python
try:
    response = requests.post(URL, data=payload, headers=headers)
except requests.RequestException as e:
    res = SlackBotResponse('error', error=str(e))
```

## Logging Integration

### Logger Usage
```python
if hasattr(self, 'logger') and not res.status == 'success':
    self.logger.warn(res)
```

### Log Levels
- **WARNING**: Failed Slack operations
- **INFO**: Successful operations (optional)
- **ERROR**: Configuration or system errors

## Configuration Validation

### Required Configuration Checks
```python
if 'slack' not in config:
    raise ValueError('Configuration missing required section')

if 'channel_id' not in slack_config or 'bot_token' not in slack_config:
    raise ValueError('Configuration missing required items')
```

### Flexible Configuration Access
```python
# Support both nested and flat configuration styles
self.channel = config.get('slack.channel_id') or slack_config['channel_id']
```

## Multi-Channel Support

### Channel Types
- **Main Channel**: General notifications
- **Vendor Failed Channel**: API failure reports
- **Vendor Incorrect Channel**: Data validation errors

### Channel Selection
Different message types automatically route to appropriate channels based on method used.

## Message Block Structure

### Slack Block Kit Format
```python
{
    'type': 'section',
    'fields': [
        {
            'type': 'mrkdwn',
            'text': '*Key:*\nValue'
        }
    ]
}
```

### Metadata Formatting
Special formatting for metadata fields:
```python
# Regular fields
text = '*%s:*\n%s' % (key.capitalize(), fields[key])

# Metadata (code block)
text = '*%s:*\n```%s```' % (key.capitalize(), fields[key])
```

## Performance Considerations
- Synchronous HTTP requests (consider async for high volume)
- Request timeout handling
- Connection pooling for multiple messages
- Rate limiting awareness

## Security Features
- Bot token authentication
- HTTPS communication
- No sensitive data in message content
- Structured error reporting without exposing internals

## Integration Patterns
- Vendor API monitoring
- System health notifications
- User activity alerts
- Error escalation workflows

## Related Components
- Vendor API integration
- Error handling system
- Logging infrastructure
- Monitoring and alerting