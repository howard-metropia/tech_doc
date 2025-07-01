# Portal Twilio Server Controller

## Overview
Manages Twilio-based voice communication services for the ConnectSmart Portal, providing secure token generation for voice calls and call routing functionality. This controller enables voice communication features within the mobility platform for user-to-user communication and customer support.

## File Details
- **Location**: `/applications/portal/controllers/twilio_server.py`
- **Type**: web2py Controller
- **Authentication**: JWT-based authentication required
- **Dependencies**: Twilio SDK, Slack integration, voice communication

## Configuration Constants
```python
TWILIO_ACCOUNT_SID        # Twilio account identifier
TWILIO_API_KEY           # Twilio API key
TWILIO_API_KEY_SECRET    # Twilio API key secret
TWILIO_ML_APNS_CERT_SID  # Apple Push Notification certificate
TWILIO_ML_FCM_CERT_SID   # Firebase Cloud Messaging certificate
TWILIO_ML_APP_SID        # Twilio application SID
TWILIO_FROM              # Default caller ID
TWILIO_CALL_TIME_LIMIT   # Maximum call duration
```

## Controller Functions

### `token()` - GET Voice Communication Token
Generates Twilio access tokens for voice communication with push notification support.

#### Endpoint
```
GET /api/v1/call_token?type=<apns|fcm>
```

#### Authentication
- **Required**: JWT token authentication
- **Authorization**: `@auth.allows_jwt()` and `@jwt_helper.check_token()`

#### Request Parameters
```python
{
    "type": "apns|fcm"  # Push notification service type
}
```

#### Response Structure
```python
{
    "token": "string",          # JWT token for Twilio voice calls
    "identity_prefix": "string" # Identity prefix for user identification
}
```

#### Token Generation Logic
```python
# Certificate selection based on platform
if type == 'apns':
    cert_sid = TWILIO_ML_APNS_CERT_SID    # iOS devices
elif type == 'fcm':
    cert_sid = TWILIO_ML_FCM_CERT_SID     # Android devices

# Identity generation
identity_prefix = TWILIO_ML_APP_SID + '_uid'
identity = identity_prefix + str(auth.user.id)

# Grant configuration
grant = VoiceGrant(
    push_credential_sid=cert_sid,
    outgoing_application_sid=TWILIO_ML_APP_SID
)

# Token creation
token = AccessToken(
    TWILIO_ACCOUNT_SID, 
    TWILIO_API_KEY, 
    TWILIO_API_KEY_SECRET,
    identity=identity
)
token.add_grant(grant)
```

### `make_call()` - POST Voice Call Routing
Handles TwiML generation for voice call routing and management.

#### Endpoint
```
POST /api/v1/make_call
```

#### Authentication
- **None Required**: Public webhook endpoint for Twilio

#### Request Parameters
```python
{
    "to": "string",    # Destination number or client identifier
    "from": "string"   # Caller identifier (optional)
}
```

#### Response
Returns TwiML (Twilio Markup Language) for call routing:
```xml
<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Dial callerId="+1234567890" timeLimit="3600">
        <Number>+1987654321</Number>
    </Dial>
</Response>
```

#### Call Routing Logic
```python
resp = VoiceResponse()

if to is None or len(to) == 0:
    # Default message for test calls
    resp.say("Congratulations! You have just made your first call! Good bye.")
else:
    # Configure caller ID
    if from_ is not None:
        dial = resp.dial(callerId=from_, time_limit=TWILIO_CALL_TIME_LIMIT)
    else:
        dial = resp.dial(callerId=TWILIO_FROM, time_limit=TWILIO_CALL_TIME_LIMIT)
    
    # Route to phone number or client
    phone_pattern = re.compile(r"^[\d\+\-\(\) ]+$")
    if phone_pattern.match(to):
        dial.number(to)      # Route to phone number
    else:
        dial.client(to)      # Route to Twilio client
```

## Voice Communication Features

### 1. Platform-Specific Push Notifications
- **iOS (APNS)**: Apple Push Notification service integration
- **Android (FCM)**: Firebase Cloud Messaging integration
- **Certificate Management**: Platform-specific certificate handling

### 2. Client Identity Management
```python
# User-specific identity generation
identity_prefix = TWILIO_ML_APP_SID + '_uid'
user_identity = identity_prefix + str(user_id)

# Enables user identification in voice calls
# Format: <app_sid>_uid<user_id>
```

### 3. Call Routing Intelligence
- **Phone Number Detection**: Regex-based phone number validation
- **Client Routing**: Direct client-to-client communication
- **Fallback Handling**: Default messages for invalid destinations

### 4. Call Duration Management
```python
# Configurable call time limits
time_limit=TWILIO_CALL_TIME_LIMIT  # Prevents excessive call costs
```

## Security Features

### Authentication & Authorization
- **JWT Validation**: Secure token generation for authenticated users
- **User Context**: Tokens tied to specific user identities
- **Platform Verification**: Valid platform type validation

### Error Handling & Monitoring
```python
# Slack integration for error monitoring
slack_manager = SlackManager(configuration, logger)

# Error notification
slack_manager.send_vendor_failed_msg({
    'status': 'ERROR',
    'vendor': 'Twilio',
    'vendorApi': 'token',
    'originApi': '[GET] /api/v1/call_token',
    'errorMsg': T('Invalid parameters'),
    'meta': json.dumps(fields)
})
```

### Input Validation
- **Parameter Presence**: Required parameter validation
- **Type Validation**: Platform type verification
- **Phone Format**: Phone number format validation

## Integration Points

### Mobile Applications
- **Voice SDK Integration**: Twilio Voice SDK implementation
- **Push Notifications**: Incoming call notifications
- **Call Controls**: Answer, decline, mute, hold functionality

### Carpooling Services
- **Driver-Passenger Communication**: Direct voice communication
- **Customer Support**: Support call routing
- **Emergency Services**: Emergency contact capabilities

### Platform Services
- **User Management**: User identity integration
- **Session Management**: Call session tracking
- **Analytics**: Call quality and usage metrics

## TwiML Response Examples

### Standard Phone Call
```xml
<Response>
    <Dial callerId="+15551234567" timeLimit="3600">
        <Number>+15559876543</Number>
    </Dial>
</Response>
```

### Client-to-Client Call
```xml
<Response>
    <Dial callerId="client:driver_123" timeLimit="3600">
        <Client>passenger_456</Client>
    </Dial>
</Response>
```

### Default Test Call
```xml
<Response>
    <Say>Congratulations! You have just made your first call! Good bye.</Say>
</Response>
```

## Error Codes & Messages

### Token Generation Errors
- **ERROR_BAD_REQUEST_PARAMS**: Invalid platform type or missing parameters
- **Slack Notification**: Automatic error reporting to operations team

### Call Routing Errors
- **Invalid Destination**: Empty or malformed destination
- **Authentication Failure**: Invalid caller credentials

## Monitoring & Analytics

### Slack Integration
Real-time error monitoring and alerting:
```python
slack_manager.send_vendor_failed_msg({
    'status': 'ERROR',
    'vendor': 'Twilio',
    'vendorApi': 'token_generation',
    'originApi': '[GET] /api/v1/call_token',
    'errorMsg': 'Platform type validation failed',
    'meta': json.dumps({'requested_type': invalid_type})
})
```

### Call Quality Tracking
- **Token Usage**: Track token generation frequency
- **Call Duration**: Monitor call length and costs
- **Platform Distribution**: iOS vs Android usage patterns

## Dependencies
- **Twilio Voice SDK**: Voice communication infrastructure
- **Twilio JWT**: Access token generation
- **Slack Helper**: Error monitoring and alerting
- **Regular Expressions**: Phone number validation
- **JSON**: Data serialization for monitoring

## Usage Examples

### Generate iOS Voice Token
```python
# Request
GET /api/v1/call_token?type=apns
Authorization: Bearer <jwt_token>

# Response
{
    "status": "success",
    "data": {
        "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
        "identity_prefix": "APb1234567890abcdef_uid"
    }
}
```

### Make Voice Call
```python
# Request
POST /api/v1/make_call
{
    "to": "+15551234567",
    "from": "client:user_123"
}

# Response (TwiML)
<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Dial callerId="client:user_123" timeLimit="3600">
        <Number>+15551234567</Number>
    </Dial>
</Response>
```

### Client-to-Client Call
```python
# Request
POST /api/v1/make_call
{
    "to": "passenger_456",
    "from": "client:driver_123"
}

# Response (TwiML)
<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Dial callerId="client:driver_123" timeLimit="3600">
        <Client>passenger_456</Client>
    </Dial>
</Response>
```

This controller enables secure, scalable voice communication within the ConnectSmart mobility platform, supporting both direct phone calls and client-to-client communication with comprehensive monitoring and error handling capabilities.