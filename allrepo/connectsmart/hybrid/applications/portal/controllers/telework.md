# Portal Telework Controller

## Overview
Manages telework and enterprise integration features for the ConnectSmart Portal, handling employee verification, enterprise group management, and telework status updates. This controller facilitates seamless integration between mobility services and enterprise telework programs.

## File Details
- **Location**: `/applications/portal/controllers/telework.py`
- **Type**: web2py Controller
- **Authentication**: JWT-based authentication required
- **Dependencies**: `json_response`, `EnterpriseHelper`

## Controller Functions

### `enterprise()` - POST Enterprise Telework Management
Handles enterprise telework verification and user cleanup operations.

#### Endpoint
```
POST /api/v1/telework/enterprise
```

#### Authentication
- **Required**: JWT token authentication
- **Authorization**: `@auth.allows_jwt()` and `@jwt_helper.check_token()`

#### Request Parameters
```python
{
    "enterprise_id": int,  # Enterprise organization ID
    "user_id": int        # Target user ID
}
```

#### Business Logic
1. **Enterprise Verification**: Validates user's telework status with enterprise system
2. **Email Verification Check**: Removes unverified enterprise associations
3. **Data Cleanup**: Cleans up invalid or unverified enterprise records

```python
enterprise_result = enterprise_helper.get_enterprise_telework(user_id)
for row in enterprise_result['list']:
    if row['email_verify_status'] == False and row['enterprise_id'] == enterprise_id:
        db((db.enterprise.user_id == user_id) & 
           (db.enterprise.enterprise_id == enterprise_id)).delete()
```

### `employee()` - GET/POST Employee Telework Operations
Manages employee telework status and enterprise associations.

#### GET Employee Telework Status
```
GET /api/v1/telework/employee
```

Returns current employee's telework configuration and enterprise associations.

**Response Structure**:
```python
{
    "security_key": "string",  # User security key
    "list": [                  # Enterprise associations
        {
            "enterprise_id": int,
            "enterprise_name": "string",
            "telework_enabled": bool,
            "email_verify_status": bool
        }
    ]
}
```

#### POST Update Telework Status
```
POST /api/v1/telework/employee
```

**Request Parameters**:
```python
{
    "enterprise_id": int,     # Enterprise organization ID
    "chk_telework": bool     # Telework enabled status
}
```

**Business Logic**:
```python
enterprise_result = enterprise_helper.update_telework_enterprise(
    auth.user.id, enterprise_id, is_telework
)
```

### `search()` - GET Enterprise Search
Searches for enterprise organizations by email domain for telework enrollment.

#### Endpoint
```
GET /api/v1/telework/search?email=example@company.com
```

#### Request Parameters
```python
{
    "email": "string"  # Email address to search enterprise by domain
}
```

#### Response Structure
```python
{
    "security_key": "string",
    "list": [
        {
            "enterprise_id": int,
            "enterprise_name": "string",
            "domain": "string",
            "status": int  # 0: available, 4: already used
        }
    ]
}
```

#### Business Logic
1. **Domain Extraction**: Extracts domain from email address
2. **Enterprise Matching**: Finds enterprises associated with email domain
3. **Status Validation**: Checks if user can join enterprise
4. **Availability Check**: Ensures enterprise telework program is active

## Key Features

### 1. Enterprise Integration
- **Multi-Enterprise Support**: Users can be associated with multiple enterprises
- **Email Domain Verification**: Automatic enterprise matching by email domain
- **Status Management**: Track verification and enrollment status

### 2. Telework Status Management
- **Enable/Disable Telework**: Individual telework status control
- **Real-time Updates**: Immediate status synchronization
- **Enterprise Coordination**: Integrated with enterprise HR systems

### 3. Verification System
```python
# Email verification status check
if row['email_verify_status'] == False:
    # Remove unverified associations
    db((db.enterprise.user_id == user_id) & 
       (db.enterprise.enterprise_id == enterprise_id)).delete()
```

### 4. Error Handling
- **Parameter Validation**: Type and presence validation
- **Enterprise API Errors**: External service error handling
- **Status Conflicts**: Duplicate enrollment prevention

## Enterprise Helper Integration

### API Communication
```python
enterprise_helper = EnterpriseHelper(ENTERPRISE_URL)

# Get telework information
enterprise_result = enterprise_helper.get_enterprise_telework(user_id)

# Update telework status
enterprise_result = enterprise_helper.update_telework_enterprise(
    user_id, enterprise_id, is_telework
)

# Search enterprises by email
enterprise_result = enterprise_helper.search_telework_enterprise(
    email, user_id
)
```

### Response Handling
All enterprise helper operations return standardized responses with error handling:
```python
try:
    enterprise_result = enterprise_helper.get_enterprise_telework(auth.user.id)
except Exception:
    response.status = 502
    return json_response.fail(ERROR_DISPATCH_ENTERPRISE_FAILED, 
                             T('Dispatch Enterprise failed'))
```

## Security Features

### Authentication & Authorization
- **JWT Token Validation**: Secure user authentication
- **User Context**: Operations scoped to authenticated user
- **Enterprise Verification**: Email domain-based access control

### Data Protection
- **User Isolation**: Enterprise data scoped per user
- **Email Privacy**: Secure email domain verification
- **Status Integrity**: Verified status requirements

## Error Codes & Messages

### Parameter Errors
- **ERROR_BAD_REQUEST_BODY**: Invalid or missing parameters
- **ERROR_BAD_REQUEST_PARAMS**: Invalid query parameters

### Enterprise API Errors
- **ERROR_DISPATCH_ENTERPRISE_FAILED**: External enterprise API failure
- **ERROR_NO_MATCHING**: No enterprise found for email domain
- **ERROR_ALREADY_BEEN_USED**: Email already associated with enterprise

## Integration Points

### Enterprise HR Systems
- **Employee Verification**: Real-time status validation
- **Telework Policies**: Enterprise-specific telework rules
- **Domain Management**: Email domain-based access control

### Mobility Platform
- **Trip Planning**: Telework status affects route recommendations
- **Incentive Programs**: Enterprise-specific reward structures
- **Analytics**: Telework pattern analysis

### User Profile System
- **Enterprise Associations**: Multi-enterprise user profiles
- **Verification Status**: Email and enterprise verification tracking
- **Security Keys**: User session and security management

## Database Schema

### Enterprise Table
```python
db.enterprise:
    user_id: int          # Foreign key to auth_user
    enterprise_id: int    # Enterprise organization ID
    email_verify_status: bool  # Email verification status
    telework_enabled: bool     # Telework participation status
```

## Usage Examples

### Search Enterprise by Email
```python
# Request
GET /api/v1/telework/search?email=john.doe@acmecorp.com

# Response
{
    "status": "success",
    "data": {
        "security_key": "abc123",
        "list": [
            {
                "enterprise_id": 12345,
                "enterprise_name": "ACME Corporation",
                "domain": "acmecorp.com",
                "status": 0
            }
        ]
    }
}
```

### Update Telework Status
```python
# Request
POST /api/v1/telework/employee
{
    "enterprise_id": 12345,
    "chk_telework": true
}

# Response
{
    "status": "success",
    "data": {
        "security_key": "abc123",
        "telework_enabled": true,
        "enterprise_id": 12345
    }
}
```

This controller enables seamless integration between ConnectSmart's mobility services and enterprise telework programs, providing comprehensive enterprise user management and telework status tracking capabilities.