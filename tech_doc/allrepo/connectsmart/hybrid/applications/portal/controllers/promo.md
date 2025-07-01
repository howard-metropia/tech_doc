# Promo Controller

## Overview
The Promo Controller manages promotional code redemption and maintenance within the MaaS platform, supporting dual-table promotion systems for different user types and providing administrative tools for promotion management.

## Technical Stack
- **Framework**: Web2py with RESTful API design
- **Authentication**: JWT for users, membership-based for admin
- **Database**: MySQL with dual promotion tracking tables
- **Code Generation**: Random alphanumeric promotion codes
- **Response Format**: JSON

## Architecture

### Core Components
- **Code Redemption**: User-facing promotion code redemption
- **Administrative Management**: Admin tools for promotion CRUD
- **Dual Table System**: Separate tracking for different promotion types
- **Points Integration**: Automatic points award upon redemption

### Database Schema
```sql
-- Main promotion table
promotion (
  id: int,
  code: varchar(10),
  points: decimal(10,2),
  started_on: datetime,
  ended_on: datetime,
  created_on: datetime,
  modified_on: datetime
)

-- Standard user redemptions
promotion_redeem (
  id: int,
  user_id: int,
  promotion_id: int,
  point_transaction_id: int,
  created_on: datetime
)

-- Upgrade user redemptions  
promotion_redeem_upgrade (
  id: int,
  user_id: int,
  promotion_id: int,
  point_transaction_id: int,
  created_on: datetime
)
```

## API Endpoints

### POST /api/v1/promo/redeem
Redeem a promotional code for points.

**Request Body:**
```json
{
  "code": "ABC123DEF4"
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "points": 50.0
  }
}
```

**Business Logic:**
1. Validate promotion code exists and is active
2. Check code hasn't been redeemed by user
3. Award points via points_transaction system
4. Record redemption in appropriate table

### POST /api/v1/promo/maintain
Create a new promotion code (Admin only).

**Request Body:**
```json
{
  "points": 100,
  "started_on": "2024-01-01 00:00:00",
  "ended_on": "2024-12-31 23:59:59"
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "code": "XYZ789ABC1"
  }
}
```

### PUT /api/v1/promo/maintain/{promotion_id}
Update an existing promotion (Admin only).

**Request Body:**
```json
{
  "points": 150,
  "started_on": "2024-01-01 00:00:00",
  "ended_on": "2024-12-31 23:59:59"
}
```

**Response:**
```json
{
  "success": true
}
```

## Business Logic

### Promotion Code Generation
```python
def generate_promo_code():
    """Generate random 10-character alphanumeric code"""
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(10))
```

### Dual Table System
The system uses two redemption tables based on the `targetTable` configuration:

```python
if doubles['targetTable'] == 'points_transaction':
    # Use promotion_redeem table
    table = db.promotion_redeem
else:
    # Use promotion_redeem_upgrade table  
    table = db.promotion_redeem_upgrade
```

### Promotion Validation
```sql
-- Active promotion check
(promotion.started_on <= now AND promotion.ended_on > now) OR
(promotion.started_on <= now AND promotion.ended_on IS NULL)
```

### Redemption Prevention
- Left join with redemption tables to check existing redemptions
- User-specific validation prevents duplicate redemptions
- Code expiration checking

## Administrative Features

### Promotion Creation
- Random code generation
- Configurable point values
- Flexible start/end date scheduling
- Immediate activation support

### Promotion Updates
- Modify point values
- Adjust validity periods
- Administrative oversight required

### Access Control
```python
@auth.requires_membership('Metropia')
def maintain():
    # Admin-only promotion management
```

## Error Handling

### Common Errors
- `ERROR_BAD_REQUEST_BODY` (400): Invalid request parameters
- `ERROR_PROMO_CODE_INVALID` (403): Code not found or expired
- `ERROR_PROMO_CODE_HAS_REDEEMED` (403): Already redeemed by user
- `ERROR_PROMOTION_NOT_FOUND` (404): Promotion ID not found

### Validation Rules
- Required fields validation
- Date format validation
- Points value validation
- Code uniqueness enforcement

## Points Integration

### Points Transaction
```python
balance, pt_id = points_transaction(
    user_id=user_id,
    activity_type=ACTIVITY_TYPE_PROMOTION_CODE,
    points=promotion_points,
    notify=False,
    time=now
)
```

### Activity Types
- `ACTIVITY_TYPE_PROMOTION_CODE`: Designated activity type for promotions
- Automatic balance calculation
- Transaction ID tracking for audit trail

## Date and Time Handling

### Timezone Awareness
- UTC timestamp handling with `request.utcnow`
- Flexible end date support (NULL for indefinite)
- Date string parsing with format validation

### Validity Periods
```python
datetime.datetime.strptime(date_string, '%Y-%m-%d %H:%M:%S')
```

## Security Features

### Access Control
- JWT authentication for user redemptions
- Membership-based authorization for admin functions
- User isolation in redemption tracking

### Code Security
- Random code generation prevents guessing
- Single-use codes per user
- Expiration date enforcement

### Input Validation
- Parameter existence checking
- Data type validation
- SQL injection prevention

## Performance Considerations

### Database Optimization
- Indexed promotion codes for fast lookup
- Efficient join queries for redemption checking
- Minimal database roundtrips

### Code Generation
- Fast random string generation
- Collision avoidance (10-character alphanumeric)
- Immediate code availability

## Configuration

### Table Selection
```python
doubles['targetTable']  # 'points_transaction' or other
```

### Activity Types
- Configured promotion activity type constants
- Integration with points system

## Integration Points

### Points System
```python
from points_transaction import points_transaction

# Award points for promotion redemption
balance, transaction_id = points_transaction(...)
```

### Authentication System
```python
@auth.allows_jwt()
@jwt_helper.check_token()
# User authentication

@auth.requires_membership('Metropia')  
# Admin authentication
```

### Response Formatting
```python
import json_response

return json_response.success(data)
return json_response.fail(error_code, message)
```

## Use Cases

### Marketing Campaigns
- Time-limited promotional codes
- Points-based user acquisition
- Seasonal campaign support

### User Engagement
- Reward program integration
- Gamification elements
- Retention incentives

### Administrative Control
- Campaign management
- Code distribution tracking
- Performance analytics

## Monitoring and Analytics
- Redemption rate tracking
- Code usage patterns
- Points distribution monitoring
- Campaign effectiveness measurement

## Dependencies
- `string`: Code generation utilities
- `random`: Random code generation
- `datetime`: Date/time handling
- `json_response`: API response formatting
- `auth`: Authentication and authorization
- `points_transaction`: Points award system