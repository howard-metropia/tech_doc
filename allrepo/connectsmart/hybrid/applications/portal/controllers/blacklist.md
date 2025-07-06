# Blacklist Controller API Documentation

## Overview
The Blacklist Controller manages user blocking functionality in the MaaS platform. It allows users to block other users from interacting with them in carpool matching, messaging, and other social features within the mobility ecosystem.

**File Path:** `/allrepo/connectsmart/hybrid/applications/portal/controllers/blacklist.py`

**Controller Type:** Authenticated Portal Controller

**Authentication:** JWT token required

## Features
- User-to-user blocking functionality
- Blacklist management (add, view, remove)
- User privacy and safety controls
- Automatic conflict resolution via update_or_insert
- RESTful API design with proper HTTP methods

## API Endpoints

### Blacklist Management
**Endpoint:** `/blacklist/blacklist`
**Methods:** GET, POST, DELETE
**Authentication:** JWT token required

#### POST - Add User to Blacklist
Adds a user to the current user's blacklist.

**Required Fields:**
- `reject_user_id`: ID of user to block

**Request Example:**
```json
{
  "reject_user_id": 123
}
```

**Response Format:**
```json
{
  "success": true,
  "data": {
    "id": 456
  }
}
```

**Status Codes:**
- `201`: Successfully added to blacklist
- `400`: Invalid parameters

**Headers:**
- `Location`: URL of the newly created blacklist entry

#### GET - List Blacklisted Users
Retrieves the current user's blacklist.

**Parameters:**
- `sequence_id` (optional): Specific blacklist entry ID

**Response Format:**
```json
{
  "success": true,
  "data": {
    "blacklist": [
      {
        "id": 456,
        "reject_user_id": 123
      },
      {
        "id": 789,
        "reject_user_id": 456
      }
    ]
  }
}
```

**Status Codes:**
- `200`: Success
- `400`: Invalid parameters

#### DELETE - Remove User from Blacklist
Removes a user from the current user's blacklist.

**Required Fields:**
- `reject_user_id`: ID of user to unblock

**Request Example:**
```json
{
  "reject_user_id": 123
}
```

**Response Format:**
```json
{
  "success": true
}
```

**Status Codes:**
- `200`: Successfully removed from blacklist
- `400`: Invalid parameters
- `403`: No permissions (user doesn't own the blacklist entry)

## Data Model

### Blacklist Entry Structure
```python
{
    "id": int,                    # Auto-generated blacklist entry ID
    "user_id": int,               # User who created the blacklist entry
    "reject_user_id": int         # User being blocked
}
```

## Database Schema

### Table: blacklist
- `id` (PRIMARY KEY): Auto-increment identifier
- `user_id` (FOREIGN KEY): Reference to blocking user
- `reject_user_id` (FOREIGN KEY): Reference to blocked user
- Unique constraint on (user_id, reject_user_id) pairs

## Authentication & Security

### JWT Authentication
- `@auth.allows_jwt()`: Enables JWT token authentication
- `@jwt_helper.check_token()`: Validates token integrity
- User identification through `auth.user.id`

### Access Control
- Users can only manage their own blacklist entries
- Permission validation prevents unauthorized removals
- User-scoped queries ensure data isolation

## Implementation Details

### Database Operations

#### CREATE - Add to Blacklist
```python
_id = db.blacklist.update_or_insert(
    (db.blacklist.user_id == auth.user.id) & 
    (db.blacklist.reject_user_id == reject_user_id),
    user_id=auth.user.id, 
    reject_user_id=reject_user_id
)
```

**Features:**
- Uses `update_or_insert` to prevent duplicates
- Automatically handles existing entries
- Returns entry ID for new or existing records

#### READ - Retrieve Blacklist
```python
# Get all blacklist entries for user
rows = db(db.blacklist.user_id == auth.user.id).select()

# Get specific blacklist entry
rows = db((db.blacklist.id == sequence_id) & 
          (db.blacklist.user_id == auth.user.id)).select()
```

#### DELETE - Remove from Blacklist
```python
row = db(
    (db.blacklist.user_id == auth.user.id) &
    (db.blacklist.reject_user_id == reject_user_id)
).select().first()

if row and row.user_id == auth.user.id:
    row.delete_record()
```

### Permission Validation
Ensures users can only modify their own blacklist entries:
```python
if not row or row.user_id != auth.user.id:
    response.status = 403
    return json_response.fail(ERROR_NO_CREATOR_PERMISSIONS, T('No permissions'))
```

## Error Handling

### Parameter Validation
- Integer validation for user IDs
- Required field checking
- Type safety for all parameters

### Error Codes
- `ERROR_BAD_REQUEST_BODY`: Invalid request parameters
- `ERROR_BAD_REQUEST_PARAMS`: Invalid URL parameters
- `ERROR_NO_CREATOR_PERMISSIONS`: Unauthorized access attempt

### Error Response Format
```json
{
  "success": false,
  "error_code": "ERROR_NO_CREATOR_PERMISSIONS",
  "message": "No permissions"
}
```

## Usage Examples

### Block a User
```bash
curl -X POST /blacklist/blacklist \
  -H "Authorization: Bearer <jwt_token>" \
  -H "Content-Type: application/json" \
  -d '{"reject_user_id": 123}'
```

### View Blacklist
```bash
curl -X GET /blacklist/blacklist \
  -H "Authorization: Bearer <jwt_token>"
```

### View Specific Entry
```bash
curl -X GET /blacklist/blacklist/456 \
  -H "Authorization: Bearer <jwt_token>"
```

### Unblock a User
```bash
curl -X DELETE /blacklist/blacklist \
  -H "Authorization: Bearer <jwt_token>" \
  -H "Content-Type: application/json" \
  -d '{"reject_user_id": 123}'
```

## Integration Points

### Carpool Matching System
- Prevents blocked users from being matched
- Filters blocked users from carpool suggestions
- Ensures user safety and privacy preferences

### Messaging System
- Blocks direct messages from blacklisted users
- Prevents notification delivery from blocked users
- Maintains communication boundaries

### Social Features
- Hides blocked users from group recommendations
- Prevents blocked users from joining user's groups
- Filters blocked users from search results

## Business Logic Integration

### Carpool Filtering
```python
# Example integration with carpool matching
def filter_blacklisted_users(user_id, potential_matches):
    blacklisted_users = get_user_blacklist(user_id)
    return [match for match in potential_matches 
            if match.user_id not in blacklisted_users]
```

### Group Management
- Automatic removal from shared groups when blocked
- Prevention of group invitations to blocked users
- Conflict resolution in group activities

## Performance Considerations

### Query Optimization
- Indexed user_id for fast blacklist lookups
- Composite index on (user_id, reject_user_id)
- Efficient duplicate prevention with update_or_insert

### Caching Strategy
```sql
-- Optimized query structure
CREATE INDEX idx_blacklist_user ON blacklist (user_id);
CREATE UNIQUE INDEX idx_blacklist_pair ON blacklist (user_id, reject_user_id);
```

### Scalability
- Lightweight table structure
- Minimal data storage per entry
- Efficient bulk operations for system-wide filtering

## Privacy & Safety Features

### User Protection
- Immediate effect on blocking
- Bidirectional blocking support
- Transparent user control

### Data Minimization
- Stores only essential blocking relationship
- No additional metadata or history
- Simple removal process

## Monitoring & Analytics

### Usage Metrics
- Blacklist creation frequency
- Most commonly blocked users
- User safety trend analysis
- Platform harassment indicators

### Health Monitoring
- Database performance on blacklist queries
- API response times
- Error rate tracking

## Troubleshooting

### Common Issues
1. **Duplicate Entries**: Handled automatically by update_or_insert
2. **Permission Errors**: Check user authentication and ownership
3. **Invalid User IDs**: Validate user existence before blocking
4. **Database Constraints**: Ensure foreign key relationships exist

### Debug Strategies
- Log blacklist operations for audit trails
- Monitor failed blocking attempts
- Track permission violation patterns
- Validate user relationship data consistency

## Administrative Tools

### Support Functions
- Admin override for emergency unblocking
- Bulk blacklist management for abuse cases
- User relationship analysis tools
- Harassment pattern detection

### Compliance Features
- Audit trail for blocking actions
- Data export for user requests
- Account deletion cleanup procedures
- Regulatory compliance reporting