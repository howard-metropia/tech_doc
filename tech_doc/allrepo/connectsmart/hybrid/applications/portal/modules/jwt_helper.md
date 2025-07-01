# JWT Helper Module Documentation

## Overview
The JWT Helper Module provides JWT (JSON Web Token) authentication functionality for the ConnectSmart Hybrid Portal application. It implements token generation, validation, and user session management with Web2py integration.

## File Location
**Source**: `/home/datavan/METROPIA/metro_combine/allrepo/connectsmart/hybrid/applications/portal/modules/jwt_helper.py`

## Dependencies
- `calendar.timegm`: UTC timestamp generation
- `datetime`: Date and time operations
- `gluon`: Web2py framework components
- `json_response`: Custom JSON response formatting
- `gluon.serializers.json`: JSON serialization

## Classes

### JWTHelper

#### Purpose
Main class for handling JWT authentication operations including token generation and validation.

#### Configuration
- **Token Expiration**: 30 days (2,592,000 seconds)
- **Refresh Token Validity**: 7 days (604,800 seconds)

#### Methods

##### `__init__(self)`
**Purpose**: Initialize JWT helper with expiration timeframes
- Sets token expiration to 30 days
- Sets refresh token availability to 7 days

##### `generate_token(self, user_id)`
**Purpose**: Generate JWT token for authenticated user
**Parameters**:
- `user_id` (int): Database ID of the user

**Process**:
1. Generate UTC timestamp for current time and expiration
2. Query user's group membership from `auth_membership` table
3. Create JWT payload with user information
4. Generate signed token using Web2py's JWT handler

**Returns**: JWT token string

**Payload Structure**:
```python
{
    'iat': now,                    # Issued at timestamp
    'exp': exp,                    # Expiration timestamp
    'iss': 'Metropia Auth',        # Issuer
    'user': {'id': user_id},       # User information
    'user_groups': {'id': group_id}, # User group
    'hmac_key': ''                 # HMAC key placeholder
}
```

##### `check_token(self)`
**Purpose**: Decorator for validating JWT tokens in request headers
**Returns**: Decorator function

**Process**:
1. Extract user ID from HTTP header (`http_userid`)
2. Validate user exists in database
3. Set authenticated user in current auth context
4. Execute decorated action if validation passes

**Authentication Flow**:
- Receives user ID from TSP API JWT decoding
- Prevents duplicate login sessions
- Raises error for invalid users (code 10301)

## Functions

### `json_fail(http_status, **kwargs)`
**Purpose**: Generate standardized JSON error responses
**Parameters**:
- `http_status` (int): HTTP status code
- `**kwargs`: Additional error parameters

**Returns**: HTTP response with JSON error format

## Authentication Architecture

### Token Structure
- **Standard JWT**: RFC 7519 compliant
- **Issuer**: "Metropia Auth"
- **Expiration**: 30-day validity period
- **User Context**: Includes user ID and group membership

### Security Features
- **UTC Timestamps**: Consistent time handling
- **Group-based Authorization**: Role-based access control
- **Session Validation**: Prevents token reuse
- **Error Handling**: Standardized error responses

### Integration Points
- **Web2py Auth**: Native authentication system
- **TSP API**: Token validation coordination
- **Database**: User and group membership queries

## Usage Examples

### Token Generation
```python
jwt_helper = JWTHelper()
token = jwt_helper.generate_token(user_id=123)
```

### Route Protection
```python
@jwt_helper.check_token()
def protected_endpoint():
    # Access current.auth.login for user info
    return "Protected content"
```

### Error Response
```python
# Generates standardized error
raise json_fail(400, code=10301, msg='Authentication failed')
```

## Database Schema Integration

### Required Tables
- **auth_user**: User account information
- **auth_membership**: User-group relationships

### Query Pattern
```sql
SELECT group_id FROM auth_membership WHERE user_id = ?
```

## Error Codes
- **10301**: Authentication failure - invalid user

## Security Considerations
- **Token Expiration**: 30-day automatic expiration
- **User Validation**: Database verification required
- **Session Management**: Prevents concurrent sessions
- **Error Disclosure**: Generic error messages

## Performance Notes
- **Database Queries**: Single query per token generation
- **Memory Usage**: Minimal token payload
- **Cache Integration**: None implemented
- **Scalability**: Suitable for medium-scale deployments

## Configuration Requirements
- Web2py JWT handler must be configured
- Database connection for user/group queries
- Proper error handling setup

## Future Enhancements
- Token refresh mechanism
- Blacklist functionality
- Multi-tenant support
- Enhanced error reporting

## Related Components
- TSP API JWT validation
- User authentication flows
- Group-based permissions
- Session management system