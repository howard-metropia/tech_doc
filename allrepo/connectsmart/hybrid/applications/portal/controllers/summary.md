# Portal Summary Controller

## Overview
Provides summary information and analytics for user wallet balances, transaction history, auto-refill settings, and special sales promotions. This controller serves as a central dashboard endpoint for user financial overview and promotional offerings.

## File Details
- **Location**: `/applications/portal/controllers/summary.py`
- **Type**: web2py Controller
- **Authentication**: JWT-based authentication required
- **Dependencies**: `json_response`, wallet system, points store

## Controller Functions

### `info()` - GET User Summary Information
Returns comprehensive user wallet and promotional information for dashboard display.

#### Endpoint
```
GET /api/v1/summary/info
```

#### Authentication
- **Required**: JWT token authentication
- **Authorization**: `@auth.allows_jwt()` and `@jwt_helper.check_token()`

#### Response Structure
```python
{
    "balance": 0,           # Current wallet balance
    "first_time": True,     # First-time user indicator
    "free_points": False,   # Free points availability
    "messages": False,      # Message notifications
    "auto_refill": {
        "enable": None,     # Auto-refill enabled status
        "below_balance": 0, # Threshold for auto-refill
        "refill_points": 0  # Points to add on refill
    },
    "special_sale": False   # Special promotions available
}
```

#### Business Logic

##### 1. Wallet Balance Retrieval
```python
sql = db.user_wallet.user_id == user_id
row = db(sql).select(
    db.user_wallet.balance, 
    db.user_wallet.auto_refill,
    db.user_wallet.below_balance, 
    db.refill_plan.points,
    left=db.refill_plan.on(db.user_wallet.refill_plan_id == db.refill_plan.id)
).first()
```

##### 2. First-Time User Detection
```python
row = find_points_transaction(user_id=user_id).first()
if row:
    result['first_time'] = False  # User has transaction history
```

##### 3. Special Sales Promotion Check
```python
sql2 = (((db.points_store.started_on <= now) & (db.points_store.ended_on > now)) |
        ((db.points_store.started_on <= now) & (db.points_store.ended_on == None))) &\
       (((db.points_store.sale_type == SALE_TYPE_EXCLUSIVE) & (db.exclusive_user.user_id == user_id)) |
        (db.points_store.sale_type == SALE_TYPE_SPECIAL))
```

## Data Flow

### Input Processing
1. **User Authentication**: JWT token validation
2. **User ID Extraction**: From authenticated session
3. **Current Time**: UTC timestamp for time-based queries

### Database Interactions
1. **Wallet Information**: User balance and auto-refill settings
2. **Transaction History**: Check for first-time user status
3. **Promotional Offers**: Active special sales and exclusive offers
4. **Refill Plans**: Associated auto-refill plan details

### Response Generation
1. **Balance Summary**: Current wallet state
2. **Auto-refill Status**: Configuration and thresholds
3. **Promotional Flags**: Available special offers
4. **User Engagement**: First-time user indicators

## Key Features

### 1. Wallet Management
- Real-time balance display
- Auto-refill configuration status
- Refill plan integration
- Transaction history indicators

### 2. Promotional System
- **Exclusive Sales**: User-specific promotional offers
- **Special Sales**: General promotional campaigns
- **Time-based Offers**: Active promotion filtering
- **Eligibility Check**: User-specific promotion access

### 3. User Experience Analytics
- First-time user identification
- Transaction history presence
- Engagement indicators
- Dashboard personalization data

### 4. Auto-refill Intelligence
```python
auto_refill = dict(
    enable=row.user_wallet.auto_refill,      # Auto-refill enabled
    below_balance=row.user_wallet.below_balance,  # Trigger threshold
    refill_points=row.refill_plan.points     # Refill amount
)
```

## Security Features

### Authentication Flow
1. **JWT Validation**: Token authenticity verification
2. **User Authorization**: Access control per user
3. **Session Management**: Secure user session handling

### Data Privacy
- User-specific data isolation
- Balance information protection
- Transaction history privacy

## Integration Points

### Wallet System
- **Balance Queries**: Real-time balance retrieval
- **Auto-refill Settings**: Configuration management
- **Refill Plans**: Plan details and pricing

### Promotional Engine
- **Sale Types**: Exclusive vs. special promotions
- **Eligibility Engine**: User-specific offer matching
- **Time-based Filtering**: Active promotion validation

### Analytics System
- **User Segmentation**: First-time vs. returning users
- **Engagement Tracking**: Transaction history analysis
- **Dashboard Metrics**: Summary data compilation

## Error Handling
- **Authentication Errors**: Invalid or expired JWT tokens
- **Database Errors**: Connection and query failures
- **Data Validation**: Missing or invalid user data

## Performance Considerations

### Query Optimization
- **Join Optimization**: Left joins for optional data
- **Index Usage**: User ID and time-based indexes
- **Result Limiting**: Efficient data retrieval

### Caching Strategy
- **User Balance**: Cacheable with invalidation
- **Promotional Data**: Time-based cache expiration
- **Transaction Flags**: Session-level caching

## Dependencies
- **json_response**: Standardized API responses
- **find_points_transaction**: Transaction history utility
- **JWT Authentication**: Token-based security
- **Wallet System**: Balance and auto-refill management
- **Promotional Engine**: Special sales and exclusive offers

## Usage Example
```python
# Client request
GET /api/v1/summary/info
Authorization: Bearer <jwt_token>

# Response
{
    "status": "success",
    "data": {
        "balance": 25.50,
        "first_time": false,
        "free_points": false,
        "messages": false,
        "auto_refill": {
            "enable": true,
            "below_balance": 10,
            "refill_points": 25
        },
        "special_sale": true
    }
}
```

This controller serves as a central dashboard endpoint, providing users with a comprehensive overview of their wallet status, auto-refill configuration, and available promotional opportunities within the ConnectSmart mobility platform.