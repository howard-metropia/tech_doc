# Refill Plan Controller

## Overview
The Refill Plan Controller provides a simple API to retrieve available point refill plans for the MaaS platform's payment system. It serves as a catalog service for users to view available point packages and their pricing information.

## Technical Stack
- **Framework**: Web2py with RESTful API design
- **Authentication**: JWT-based authentication
- **Database**: MySQL for refill plan storage
- **Response Format**: JSON

## Architecture

### Core Components
- **Plan Catalog**: Read-only access to available refill plans
- **Pricing Display**: Multi-currency support with display rates
- **Simple Service**: Lightweight catalog retrieval

### Database Schema
```sql
refill_plan (
  id: int,
  points: decimal(10,2),
  amount: decimal(10,2),
  currency: varchar(3),
  display_rate: int
)
```

## API Endpoints

### GET /api/v1/refill_plan/refill_plan
Retrieve all available refill plans.

**Response:**
```json
{
  "success": true,
  "data": {
    "plans": [
      {
        "id": 1,
        "points": 100.0,
        "amount": 9.99,
        "currency": "USD",
        "display_rate": 100
      },
      {
        "id": 2,
        "points": 500.0,
        "amount": 49.99,
        "currency": "USD", 
        "display_rate": 100
      },
      {
        "id": 3,
        "points": 1000.0,
        "amount": 99.99,
        "currency": "USD",
        "display_rate": 100
      }
    ]
  }
}
```

## Business Logic

### Plan Structure
Each refill plan contains:
- **ID**: Unique plan identifier
- **Points**: Number of points awarded
- **Amount**: Price in specified currency
- **Currency**: ISO currency code (USD, EUR, etc.)
- **Display Rate**: Rate for currency display formatting

### Pricing Model
- Fixed point packages at various price tiers
- Multi-currency support for international users
- Display rate handling for proper currency formatting

### Value Proposition
- Bulk purchase discounts (implied by tiered pricing)
- Clear point-to-currency conversion
- Transparent pricing structure

## Data Model

### Refill Plan Entity
```python
{
  "id": Integer,           # Unique identifier
  "points": Decimal,       # Points awarded
  "amount": Decimal,       # Price in currency
  "currency": String,      # ISO currency code
  "display_rate": Integer  # Display formatting rate
}
```

### Currency Handling
- ISO 4217 currency codes (USD, EUR, GBP, etc.)
- Decimal precision for accurate pricing
- Display rate for proper currency formatting

## Implementation Details

### Database Query
```python
def GET():
    rows = db().select(
        db.refill_plan.id,
        db.refill_plan.points, 
        db.refill_plan.amount,
        db.refill_plan.currency,
        db.refill_plan.display_rate
    )
    
    return json_response.success(dict(plans=rows.as_list()))
```

### Response Format
- Standard JSON response wrapper
- Plans array containing all available options
- Consistent field naming and types

## Security Features

### Authentication
- JWT authentication required
- Token validation via `@jwt_helper.check_token()`
- User session verification

### Access Control
- Read-only operation (GET only)
- No user-specific data filtering
- Public catalog nature with authentication gate

## Performance Considerations

### Caching Strategy
- Simple query with no complex joins
- Suitable for response caching
- Minimal database load

### Scalability
- Lightweight catalog service
- No user-specific processing
- Efficient for high-frequency requests

## Error Handling

### Validation
- No input parameters to validate
- Simple database query error handling
- Standard HTTP status codes

### Response Consistency
- Always returns plans array (empty if none available)
- Consistent JSON structure
- Proper error response format

## Integration Points

### Payment System
- Plan IDs used in payment processing
- Amount and currency for payment gateway integration
- Points value for account crediting

### User Interface
- Display rate for proper currency formatting
- Plan comparison data
- Pricing tier visualization

### Points System
```python
# Integration with points_transaction for purchases
points_transaction(
    user_id=user_id,
    activity_type=ACTIVITY_TYPE_PURCHASE,
    points=plan.points,
    amount=plan.amount
)
```

## Use Cases

### Point Purchase Flow
1. User views available refill plans
2. Selects desired plan based on points/price ratio
3. Proceeds to payment with plan ID
4. Points credited upon successful payment

### Pricing Display
- Mobile app plan selection screens
- Web interface pricing tables
- Promotional material generation

### Plan Comparison
- Value analysis (points per dollar)
- Bulk discount visualization
- Currency conversion support

## Configuration

### Plan Management
- Database-driven plan configuration
- Administrative interface for plan updates
- Dynamic pricing support

### Currency Support
- Multi-currency plan offerings
- Localized pricing display
- Exchange rate considerations

## Future Enhancements

### Potential Features
- User-specific plan recommendations
- Dynamic pricing based on usage patterns
- Promotional plan support
- Subscription-based plans

### Analytics Integration
- Plan popularity tracking
- Conversion rate monitoring
- Revenue optimization

## Dependencies
- `json_response`: API response formatting
- `auth`: JWT authentication system
- `db`: Database connection and querying

## Related Services
- Payment processing controllers
- Points transaction management
- User account management
- Currency conversion services

## Administrative Considerations

### Plan Maintenance
- Regular pricing review
- Currency rate updates
- Plan performance analysis
- Market competition monitoring

### Business Intelligence
- Purchase pattern analysis
- Revenue per plan tracking
- User conversion funnels
- Pricing optimization opportunities