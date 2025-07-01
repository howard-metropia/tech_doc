# Store Controller

## Overview
The Store Controller manages the points-based marketplace within the MaaS platform, providing both user-facing shopping functionality and administrative tools for product management. It supports multiple product tiers including general, special, and exclusive offerings with time-based availability and user-specific access control.

## Technical Stack
- **Framework**: Web2py with RESTful API design
- **Authentication**: JWT for users, membership-based for admin
- **Database**: MySQL with relational product and user tables
- **Response Format**: JSON

## Architecture

### Core Components
- **Product Catalog**: Multi-tier product offerings (general, special, exclusive)
- **User Access Control**: Exclusive product user management
- **Time-based Availability**: Start/end date product scheduling
- **Administrative Interface**: Product creation and exclusive user assignment

### Database Schema
```sql
-- Main product store
points_store (
  id: int,
  sale_type: int,
  points: int,
  amount: int,
  original_amount: int,
  currency: varchar(3),
  display_rate: int,
  started_on: datetime,
  ended_on: datetime,
  created_on: datetime,
  modified_on: datetime
)

-- Exclusive product access control
exclusive_user (
  id: int,
  point_store_id: int,
  user_id: int
)
```

## API Endpoints

### GET /api/v1/store/point
Retrieve available point store products for authenticated user.

**Response:**
```json
{
  "success": true,
  "data": {
    "general_products": [
      {
        "id": 1,
        "points": 100,
        "amount": 999,
        "original_amount": 1099,
        "currency": "USD",
        "display_rate": 100,
        "ended_on": "2024-12-31T23:59:59Z"
      },
      {
        "id": 2,
        "points": 250,
        "amount": 2499,
        "original_amount": 2699,
        "currency": "USD",
        "display_rate": 100,
        "ended_on": null
      }
    ],
    "special_products": [
      {
        "id": 3,
        "points": 500,
        "amount": 4799,
        "original_amount": 4999,
        "currency": "USD",
        "display_rate": 100,
        "ended_on": "2024-06-30T23:59:59Z"
      }
    ]
  }
}
```

### POST /api/v1/store/point_product
Create a new point store product (Admin only).

**Request Body:**
```json
{
  "sale_type": 1,
  "points": 100,
  "amount": 999,
  "original_amount": 1099,
  "currency": "USD",
  "display_rate": 100,
  "started_on": "2024-01-01 00:00:00",
  "ended_on": "2024-12-31 23:59:59"
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "id": 4
  }
}
```

### POST /api/v1/store/exclusive_point_product
Assign users to exclusive point products (Admin only).

**Request Body:**
```json
{
  "product_id": 5,
  "user_ids": [123, 456, 789]
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "success": [123, 789],
    "existed": [456]
  }
}
```

## Product Tiers

### Sale Types
- **SALE_TYPE_GENERAL** (1): Available to all users
- **SALE_TYPE_SPECIAL** (2): Special promotions, available to all users
- **SALE_TYPE_EXCLUSIVE** (3): Restricted to specific users only

### Tier Logic
```python
def categorize_products(rows):
    """
    Categorize products by sale type for user display
    """
    general = []
    special = []
    
    for row in rows:
        product = create_product_dict(row)
        
        if row.sale_type == SALE_TYPE_GENERAL:
            general.append(product)
        else:  # SALE_TYPE_SPECIAL or SALE_TYPE_EXCLUSIVE
            special.append(product)
    
    return general, special
```

## Business Logic

### Product Availability Query
```sql
-- Active products with user access control
SELECT points_store.*, exclusive_user.id as exclusive_access
FROM points_store 
LEFT JOIN exclusive_user ON (
  points_store.id = exclusive_user.point_store_id AND 
  exclusive_user.user_id = :user_id
)
WHERE (
  -- Time-based availability
  ((points_store.started_on <= :now AND points_store.ended_on > :now) OR
   (points_store.started_on <= :now AND points_store.ended_on IS NULL))
) AND (
  -- Access control
  ((points_store.sale_type = :exclusive AND exclusive_user.user_id = :user_id) OR
   (points_store.sale_type != :exclusive))
)
```

### Exclusive User Management
```python
def assign_exclusive_users(product_id, user_ids):
    """
    Assign users to exclusive products with duplicate prevention
    """
    # Get existing assignments
    existing_users = get_existing_exclusive_users(product_id)
    
    success_users = []
    existed_users = []
    
    for user_id in user_ids:
        if user_id in existing_users:
            existed_users.append(user_id)
        else:
            db.exclusive_user.insert(
                point_store_id=product_id, 
                user_id=user_id
            )
            success_users.append(user_id)
    
    return success_users, existed_users
```

### Time-based Filtering
```python
def filter_active_products(current_time):
    """
    Filter products based on start/end date availability
    """
    return db(
        ((db.points_store.started_on <= current_time) & 
         (db.points_store.ended_on > current_time)) |
        ((db.points_store.started_on <= current_time) & 
         (db.points_store.ended_on == None))
    )
```

## Product Data Structure

### Product Entity
```python
{
  "id": Integer,              # Unique product identifier
  "points": Integer,          # Points required for purchase
  "amount": Integer,          # Current price (in cents)
  "original_amount": Integer, # Original price (in cents)
  "currency": String,         # ISO currency code
  "display_rate": Integer,    # Display formatting rate
  "ended_on": DateTime        # Expiration date (null for indefinite)
}
```

### Pricing Model
- **Amount**: Current discounted price
- **Original Amount**: Regular price for discount calculation
- **Display Rate**: Currency formatting (typically 100 for cent display)
- **Points**: Required points for purchase

## Administrative Features

### Product Creation
```python
def create_product(sale_type, points, amount, original_amount, currency, display_rate, started_on=None, ended_on=None):
    """
    Create new point store product with validation
    """
    # Default start time to now if not specified
    if not started_on:
        started_on = request.utcnow
    
    # Validate sale type
    if sale_type not in [SALE_TYPE_GENERAL, SALE_TYPE_SPECIAL, SALE_TYPE_EXCLUSIVE]:
        raise ValueError("Invalid sale type")
    
    # Insert product
    product_id = db.points_store.insert(
        sale_type=sale_type,
        points=points,
        amount=amount,
        original_amount=original_amount,
        currency=currency.upper(),
        display_rate=display_rate,
        started_on=started_on,
        ended_on=ended_on,
        created_on=request.utcnow,
        modified_on=request.utcnow
    )
    
    return product_id
```

### Exclusive Access Control
```python
def validate_exclusive_product(product_id):
    """
    Validate product exists and is exclusive type
    """
    product = db(db.points_store.id == product_id).select().first()
    
    if not product:
        raise ProductNotFoundException()
    
    if product.sale_type != SALE_TYPE_EXCLUSIVE:
        raise InvalidSaleTypeException()
    
    return product
```

## Error Handling

### Common Errors
- `ERROR_BAD_REQUEST_BODY` (400): Invalid request parameters
- `ERROR_POINT_PRODUCT_NOT_FOUND` (404): Product not found
- `ERROR_SALE_TYPE_INVALID` (403): Invalid sale type
- `ERROR_EXCLUSIVE_SALE_TYPE_ONLY` (403): Operation requires exclusive product

### Validation Rules
- **Sale Type**: Must be 1, 2, or 3
- **Numeric Fields**: Points, amounts must be positive integers
- **Currency**: Must be valid 3-letter ISO code (uppercase)
- **Dates**: Must be valid datetime format
- **User IDs**: Must be array of integers

### Input Sanitization
```python
def validate_product_input(fields):
    """
    Validate and sanitize product creation input
    """
    try:
        sale_type = int(fields['sale_type'])
        points = int(fields['points'])
        amount = int(fields['amount'])
        original_amount = int(fields['original_amount'])
        currency = fields['currency'].upper()
        display_rate = int(fields['display_rate'])
        
        # Date parsing with optional fields
        started_on = parse_datetime(fields.get('started_on'))
        ended_on = parse_datetime(fields.get('ended_on'))
        
        return validated_data
    except (ValueError, TypeError, KeyError):
        raise ValidationException()
```

## Security Features

### Access Control
```python
@auth.allows_jwt()
@jwt_helper.check_token()
def point():
    # User authentication required
    
@auth.requires_membership('Metropia')
def point_product():
    # Admin-only product management
```

### User Isolation
- Exclusive products filtered by user ID
- No cross-user data access
- Secure user assignment validation

## Performance Considerations

### Database Optimization
- Indexed queries on sale_type and time ranges
- Efficient LEFT JOIN for exclusive user checking
- Minimal database roundtrips

### Caching Strategy
- Product catalog suitable for caching
- User-specific exclusive access caching
- Time-based cache invalidation

## Integration Points

### Points System
```python
# Integration with points transaction system
points_transaction(
    user_id=user_id,
    activity_type=ACTIVITY_TYPE_STORE_PURCHASE,
    points=-product.points,
    product_id=product.id
)
```

### User Management
```python
# User authentication integration
user_id = auth.user.id

# Admin membership validation
@auth.requires_membership('Metropia')
```

## Use Cases

### User Shopping Experience
1. Browse available products by tier
2. View pricing and discount information
3. Check exclusive product access
4. Purchase with points

### Administrative Management
1. Create new products with scheduling
2. Manage exclusive user access
3. Track product performance
4. Update pricing and availability

### Marketing Campaigns
- Time-limited special offers
- Exclusive user rewards
- Tiered pricing strategies
- Discount promotions

## Future Enhancements

### Potential Features
- Product categories and filtering
- Purchase history tracking
- Inventory management
- Dynamic pricing algorithms
- User recommendation system

### Analytics Integration
- Product popularity tracking
- Purchase pattern analysis
- Revenue optimization
- User engagement metrics

## Dependencies
- `json_response`: API response formatting
- `auth`: Authentication and authorization system
- `datetime`: Date/time parsing and validation