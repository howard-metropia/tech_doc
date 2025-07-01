# Portal Wallet Controller

## Overview
Comprehensive digital wallet management controller for the ConnectSmart Portal, handling coin purchases, payment card management, auto-refill functionality, and Stripe payment integration. This controller manages the complete financial ecosystem within the mobility platform.

## File Details
- **Location**: `/applications/portal/controllers/wallet.py`
- **Type**: web2py Controller
- **Authentication**: JWT-based authentication required
- **Dependencies**: Stripe API, MongoDB, fraud prevention, notification systems

## Core Imports & Dependencies
```python
import json
import os
import json_response
from mongo_helper import MongoManager
from slack_helper import SlackManager
```

## Fraud Prevention System

### Daily Purchase Limits
```python
def _exceed_purchase_limit(user_id, points):
    """Check if user exceeds daily coin purchase limit"""
    date1 = request.utcnow - datetime.timedelta(days=1)
    
    # Get transactions from last 24 hours
    transactions = db(
        (db.purchase_transaction.user_id == user_id) &
        (db.purchase_transaction.created_on >= date1)
    ).select(db.purchase_transaction.ALL)
    
    total = sum(_.points for _ in transactions) + points
    limit = int(os.environ.get('COIN_PURCHASE_DAILY_LIMIT', 200))
    
    if total > limit:
        db.coin_activity_log.insert(user_id=user_id, activity_type=1)
        return True
    return False
```

### Account Blocking Logic
```python
def _whether_to_block(user_id, points):
    """Determine if user should be blocked for suspicious activity"""
    date1 = request.utcnow - datetime.timedelta(days=1)
    
    # Check for multiple limit violations
    logs = db(
        (db.coin_activity_log.user_id == user_id) &
        (db.coin_activity_log.activity_type == 1) &
        (db.coin_activity_log.created_on >= date1)
    ).select(db.coin_activity_log.ALL)
    
    if len(logs) > 1:
        # Send notification if not already sent
        notifies = db(
            (db.coin_activity_log.user_id == user_id) &
            (db.coin_activity_log.activity_type == 3) &
            (db.coin_activity_log.created_on >= date1)
        ).select(db.coin_activity_log.ALL)
        
        if len(notifies) == 0:
            table_user = auth.table_user()
            user = table_user(id=user_id)
            _email_notify_user(user)
            _email_notify(user, points)
            db.coin_activity_log.insert(user_id=user_id, activity_type=3)
        
        # Block user
        blocked = db(db.block_users.user_id == user_id).select().first()
        if blocked:
            blocked.update_record(is_deleted=False)
        else:
            db.block_users.insert(user_id=user_id, is_deleted=False)
        return True
    return False
```

## Core Wallet Functions

### `point()` - GET/POST Wallet Balance and Purchases
Manages wallet balance queries and coin purchases.

#### GET Wallet Balance
```
GET /api/v1/wallet/point
```

**Response Structure**:
```python
{
    "balance": float  # Current wallet balance
}
```

#### POST Purchase Coins
```
POST /api/v1/wallet/point
```

**Request Structure**:
```python
{
    "product_id": int,           # Points store product ID
    "transaction_token": "string", # Optional: payment token
    "payment_way": int           # Payment method identifier
}
```

**Purchase Flow**:
1. **Fraud Checking**: Validate against daily limits and suspicious activity
2. **Product Validation**: Verify product exists and is active
3. **Payment Processing**: Execute Stripe payment or use stored card
4. **Balance Update**: Add purchased coins to wallet
5. **Analytics Tracking**: Record purchase for analytics

```python
# Fraud prevention checks
if _exceed_purchase_limit(user_id, row.points):
    if _whether_to_block(user_id, row.points):
        return json_response.fail(ERROR_USER_COIN_SUSPENDED, 
            T('For your protection, we have temporarily limited your account...'))
    else:
        return json_response.fail(ERROR_COIN_PURCHASE_DAILY_LIMIT,
            T('For your safety, we limit the number of Coins purchased each day...'))

# Process payment
success, res = stripe_charge(row.amount, row.currency, row.points, user_id, 
                            transaction_token, customer_id)

# Update balance and record transaction
balance, pt_id = points_transaction(user_id, ACTIVITY_TYPE_PURCHASE, row.points, 
                                   note=note, notify=False, time=now)
```

### `point_history()` - GET Transaction History
Retrieves paginated wallet transaction history.

#### Endpoint
```
GET /api/v1/wallet/point_history?offset=0&perpage=10
```

**Response Structure**:
```python
{
    "transactions": [
        {
            "points": float,
            "created_on": "datetime",
            "activity_type": "string"
        }
    ],
    "next_offset": int,
    "total_count": int
}
```

## Payment Card Management

### `card()` - GET/POST/PUT/DELETE Card Management
Comprehensive payment card management with Stripe integration.

#### GET List Cards
```
GET /api/v1/wallet/card
```

**Response Structure**:
```python
{
    "cards": [
        {
            "id": "string",
            "brand": "string",
            "last4": "string",
            "expire_year": int,
            "expire_month": int,
            "default": bool,
            "postal_code": "string",
            "name": "string"
        }
    ],
    "last_payment_way": int
}
```

#### POST Add New Card
```python
def POST(**fields):
    token = fields['transaction_token']
    customer_id = _get_customer_id(user_id)
    
    if customer_id:
        # Add card to existing customer
        customer = _create_new_card(customer_id, token)
    else:
        # Create new customer and add card
        profile = user_profiles(db, [user_id])[0]
        customer = _create_customer(email, profile.get('full_name'))
        customer = _create_new_card(customer.id, token)
        
        # Store customer ID
        db.user_wallet.insert(user_id=user_id, stripe_customer_id=customer.id)
```

#### PUT Update Card
Supports updating card details and setting default card:
```python
{
    "card_id": "string",
    "expire_year": int,      # Optional
    "expire_month": int,     # Optional
    "postal_code": "string", # Optional
    "default": bool          # Optional
}
```

#### DELETE Remove Card
```python
def DELETE(**fields):
    card_id = fields['card_id']
    customer_id = _get_customer_id(user_id)
    
    customer = _delete_card(customer_id, card_id)
    payments = _get_payments(customer.id)
    cards = _get_cards(customer, payments)
    
    return json_response.success(dict(cards=cards))
```

## Auto-Refill System

### `setting()` - GET/PUT Auto-Refill Configuration
Manages automatic wallet refill settings and triggers.

#### GET Auto-Refill Settings
```
GET /api/v1/wallet/setting
```

**Response Structure**:
```python
{
    "customer": bool,        # Has payment method
    "auto_refill": bool,     # Auto-refill enabled
    "below_balance": float,  # Refill trigger threshold
    "refill_plan": {
        "id": int,
        "points": float,
        "amount": float,
        "currency": "string",
        "display_rate": float
    }
}
```

#### PUT Configure Auto-Refill
```python
{
    "auto_refill": bool,
    "below_balance": float,    # Required if auto_refill=true
    "refill_plan_id": int     # Required if auto_refill=true
}
```

**Auto-Refill Trigger Logic**:
```python
if auto_refill:
    uw = db(db.user_wallet.user_id == user_id).select().first()
    if uw and uw.stripe_customer_id and round(float(uw.balance) - float(below_balance), 2) < 0:
        # Calculate refill amount
        balance = uw.balance
        refill = db(db.refill_plan.id == uw.refill_plan_id).select().first()
        charge = float(refill.points) - float(balance)
        charge_amount = int(round(charge * refill.display_rate))
        
        # Process auto-refill payment
        success, res = stripe_charge(charge_amount, refill.currency, charge, user_id,
                                   customer_id=uw.stripe_customer_id)
```

## Stripe Integration

### Customer Management
```python
def _get_customer(id):
    """Retrieve Stripe customer"""
    import stripe
    stripe.api_key = configuration.get('stripe.api_key')
    return stripe.Customer.retrieve(id)

def _create_customer(email, name):
    """Create new Stripe customer"""
    import stripe
    stripe.api_key = configuration.get('stripe.api_key')
    return stripe.Customer.create(email=email, name=name)
```

### Payment Method Management
```python
def _get_payments(id):
    """Get customer payment methods"""
    import stripe
    stripe.api_key = configuration.get('stripe.api_key')
    payments = stripe.Customer.list_payment_methods(customer=id, type='card')
    return payments.data

def _get_cards(customer, payments):
    """Format payment methods for API response"""
    cards = []
    if payments:
        default_card_id = customer.default_source
        for source in payments:
            if source.object == 'payment_method' and source.type == 'card':
                card_info = dict(
                    id=source.id,
                    brand=source.card.brand,
                    last4=source.card.last4,
                    expire_year=source.card.exp_year,
                    expire_month=source.card.exp_month,
                    default=(default_card_id == source.id),
                    postal_code=source.billing_details.address.postal_code,
                    name=source.billing_details.name
                )
                cards.append(card_info)
    return cards
```

## Security Features

### Fraud Detection
- **Daily Limits**: Configurable daily purchase limits
- **Pattern Detection**: Multiple violation monitoring
- **Account Blocking**: Automatic suspicious account blocking
- **Email Notifications**: Fraud alert notifications

### Payment Security
- **Stripe Integration**: PCI-compliant payment processing
- **Token-based Payments**: No raw card data storage
- **Customer Isolation**: User-specific payment data access
- **Error Monitoring**: Slack integration for payment failures

### Input Validation
```python
# Card validation
if customer_card.address_zip_check != 'pass':
    return json_response.fail(ERROR_CARD_VALIDATION_FAILED, 
                             T('Card validation failed'))

# Parameter validation
required_fields = ['transaction_token']
if not verify_required_fields(required_fields, fields):
    return json_response.fail(ERROR_BAD_REQUEST_BODY, T('Invalid parameters'))
```

## Notification System

### Fraud Alerts
```python
def _email_notify_user(user):
    """Send fraud alert to user"""
    project = configuration.get('project.name', '')
    subject = 'Customer Support at %s' % project
    msg = '''Good afternoon, %s this is Aranza with %s. I wanted to reach out to you because our system triggered a potential fraud alert...''' % (user.first_name, project)
    mail.send(to=[user.email], message=msg, subject=subject)

def _email_notify(user, points):
    """Send fraud alert to operations team"""
    email_list = configuration.get('tango.alert_notify_email', ['operations@metropia.com'])
    subject = '[%s] Purchase Coins Daily Quota Alert (user_id: %s)' % (project, user.id)
    # ... send detailed alert
```

### Slack Integration
```python
slack_manager.send_vendor_failed_msg({
    'status': 'ERROR',
    'vendor': 'Stripe',
    'vendorApi': 'Customer.retrieve',
    'originApi': '[GET] /api/v1/card_setting',
    'errorMsg': '%s' % e,
    'meta': json.dumps({'customer_id': customer_id})
})
```

## Analytics Integration

### Purchase Tracking
```python
# Location-based analytics
mongo = MongoManager.get()
lastlatlon = list(mongo.app_state.find({'user_id': user_id}).sort("timestamp", -1).limit(1))
if len(lastlatlon) > 0:
    lat = lastlatlon[0]['latitude']
    lon = lastlatlon[0]['longitude']

# Record purchase analytics
db.app_data.insert(
    user_id=user_id, 
    user_action='PurchasePoints',
    refid=transaction_id, 
    points=row.points,
    price=row.amount,
    lat=lat, 
    lon=lon, 
    email=email,
    gmt_time=now
)
```

## Error Handling

### Payment Errors
```python
ERROR_CARD_CREATE_FAILED = "Create a card failed"
ERROR_CARD_UPDATE_FAILED = "Card update failed"
ERROR_CARD_DELETE_FAILED = "Card delete failed"
ERROR_CARD_VALIDATION_FAILED = "Card validation failed"
ERROR_CUSTOMER_CREATE_FAILED = "Create failed in Stripe customer"
ERROR_CUSTOMER_WAS_DELETED = "Customer was deleted in Stripe"
```

### Wallet Errors
```python
ERROR_POINT_PRODUCT_NOT_FOUND = "Coin product not found"
ERROR_POINT_PRODUCT_EXPIRED = "Coin product has expired"
ERROR_USER_COIN_SUSPENDED = "Account temporarily limited"
ERROR_COIN_PURCHASE_DAILY_LIMIT = "Daily purchase limit reached"
```

## Dependencies
- **Stripe API**: Payment processing and card management
- **MongoDB**: User analytics and app state tracking
- **SMTP**: Email notification system
- **Slack Helper**: Error monitoring and alerting
- **Points System**: Wallet balance and transaction management

## Usage Examples

### Purchase Coins
```python
# Request
POST /api/v1/wallet/point
{
    "product_id": 1,
    "transaction_token": "tok_visa_debit",
    "payment_way": 1
}

# Response
{
    "status": "success",
    "data": {
        "balance": 125.50
    }
}
```

### Add Payment Card
```python
# Request
POST /api/v1/wallet/card
{
    "transaction_token": "tok_visa_1234"
}

# Response
{
    "status": "success",
    "data": {
        "cards": [
            {
                "id": "card_1234",
                "brand": "Visa",
                "last4": "4242",
                "expire_year": 2025,
                "expire_month": 12,
                "default": true,
                "postal_code": "12345",
                "name": "John Doe"
            }
        ]
    }
}
```

### Configure Auto-Refill
```python
# Request
PUT /api/v1/wallet/setting
{
    "auto_refill": true,
    "below_balance": 10,
    "refill_plan_id": 3
}

# Response: Auto-refill configuration confirmation
# If balance is below threshold, immediate refill is triggered
```

This controller provides comprehensive wallet management capabilities for the ConnectSmart mobility platform, ensuring secure payment processing, fraud prevention, and seamless financial transactions across all mobility services.