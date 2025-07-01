# Reward Controller

## Overview
The Reward Controller manages gift card redemption and rewards distribution within the MaaS platform, integrating with TangoCard API for physical gift card fulfillment. It provides comprehensive fraud prevention, daily limits, and multi-tier notification systems for secure reward processing.

## Technical Stack
- **Framework**: Web2py with RESTful API design
- **Authentication**: JWT-based authentication
- **External API**: TangoCard integration for gift card fulfillment
- **Database**: MySQL for gift cards, transactions, and activity logging
- **Messaging**: Slack notifications for fraud alerts
- **Security**: HTTPBasicAuth for TangoCard API
- **Email**: SMTP integration for user notifications

## Architecture

### Core Components
- **Gift Card Catalog**: Multi-category gift card offerings
- **TangoCard Integration**: External API for gift card delivery
- **Fraud Prevention**: Multi-layered security and monitoring
- **Daily Limits**: Rolling 24-hour redemption limits
- **Alert System**: Slack and email notifications
- **Activity Logging**: Comprehensive audit trail

### Database Schema
```sql
-- Gift card categories
giftcard_category (
  id: int,
  category_name: varchar,
  image: varchar
)

-- Gift card products
giftcard (
  id: int,
  category_id: int,
  points: decimal(10,2),
  amount: decimal(10,2),
  currency: varchar(3),
  utid: varchar
)

-- Redemption transactions
redeem_transaction (
  id: int,
  user_id: int,
  giftcard_id: int,
  points: decimal(10,2),
  amount: decimal(10,2),
  currency: varchar(3),
  transaction_id: varchar,
  created_on: datetime
)

-- Activity logging for fraud detection
coin_activity_log (
  id: int,
  user_id: int,
  activity_type: int,
  created_on: datetime
)
```

## API Endpoints

### GET /api/v1/reward/gift_card
Retrieve available gift card categories and products.

**Response:**
```json
{
  "success": true,
  "data": {
    "giftcards": [
      {
        "category_id": 1,
        "name": "Retail",
        "image": "retail_category.png",
        "items": [
          {
            "id": 101,
            "points": 1000,
            "amount": 1000,
            "currency": "USD",
            "display_rate": 100
          },
          {
            "id": 102,
            "points": 2500,
            "amount": 2500,
            "currency": "USD",
            "display_rate": 100
          }
        ]
      },
      {
        "category_id": 2,
        "name": "Dining",
        "image": "dining_category.png",
        "items": [
          {
            "id": 201,
            "points": 1500,
            "amount": 1500,
            "currency": "USD",
            "display_rate": 100
          }
        ]
      }
    ]
  }
}
```

### POST /api/v1/reward/redeem
Redeem points for a gift card.

**Request Body:**
```json
{
  "id": 101,
  "email": "user@example.com"
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "balance": 2500.50
  }
}
```

## TangoCard Integration

### Configuration
```python
TANGO_URL = configuration.get('tango.url')
TANGO_PLATFORM_NAME = configuration.get('tango.platform_name')
TANGO_PLATFORM_KEY = configuration.get('tango.platform_key')
TANGO_ACCOUNT_ID = configuration.get('tango.account_id')
TANGO_CUSTOMER_ID = configuration.get('tango.customer_id')
TANGO_SENDER_EMAIL = configuration.get('tango.sender_email')
TANGO_SENDER_NAME = configuration.get('tango.sender_name')
```

### Gift Card Redemption
```python
def _tango_redeem(utid, email, first_name, last_name, amount, currency):
    """
    Process gift card redemption through TangoCard API
    """
    url = TANGO_URL + '/orders'
    payload = {
        'accountIdentifier': TANGO_ACCOUNT_ID,
        'amount': amount,
        'customerIdentifier': TANGO_CUSTOMER_ID,
        'utid': utid,
        'recipient': {
            'email': email,
            'firstName': first_name,
            'lastName': last_name
        },
        'sender': {
            'email': TANGO_SENDER_EMAIL,
            'firstName': TANGO_SENDER_NAME,
            'lastName': ''
        },
        'sendEmail': 'true',
        'etid': 'E000000'
    }
    
    response = requests.post(
        url,
        json=payload,
        headers={'Content-Type': 'application/json'},
        auth=HTTPBasicAuth(TANGO_PLATFORM_NAME, TANGO_PLATFORM_KEY)
    )
    
    if response.status_code == 201:
        return True, response.json()['referenceOrderID']
    else:
        return False, None
```

### Account Balance Monitoring
```python
def _tango_accounts():
    """
    Check TangoCard account balance for insufficient funds monitoring
    """
    url = TANGO_URL + '/accounts/' + TANGO_ACCOUNT_ID
    response = requests.get(
        url,
        headers={'Content-Type': 'application/json'},
        auth=HTTPBasicAuth(TANGO_PLATFORM_NAME, TANGO_PLATFORM_KEY)
    )
    
    if response.status_code == 200:
        return True, response.json()
    else:
        return False, None
```

## Fraud Prevention System

### Daily Limit Enforcement
```python
def _exceed_redeem_limit(user_id, amount):
    """
    Check if redemption exceeds rolling 24-hour limit
    Default limit: $100 USD
    """
    limit = int(os.environ.get('REDEEM_DAILY_LIMIT', 100))
    start = datetime.datetime.now(tz=utc) - datetime.timedelta(days=1)
    
    sum_query = db.redeem_transaction.amount.sum()
    row = db(
        (db.redeem_transaction.user_id == user_id) & 
        (db.redeem_transaction.created_on > start.strftime("%Y-%m-%d %H:%M:%S"))
    ).select(sum_query).first()
    
    current_total = int(row[sum_query]) if row[sum_query] else 0
    
    if current_total + int(amount) > limit:
        # Log suspicious activity
        db.coin_activity_log.insert(user_id=user_id, activity_type=2)
        return True
    
    return False
```

### Multi-Tier Alert System
```python
def _whether_to_block(user_id, row, email):
    """
    Determine if user should be blocked based on activity patterns
    Escalates to email notifications after multiple violations
    """
    date1 = request.utcnow - datetime.timedelta(days=1)
    
    # Check violation count in last 24 hours
    logs = db(
        (db.coin_activity_log.user_id == user_id) &
        (db.coin_activity_log.activity_type == 2) &
        (db.coin_activity_log.created_on >= date1)
    ).select()
    
    if len(logs) > 1:
        # Check if already notified
        notifies = db(
            (db.coin_activity_log.user_id == user_id) &
            (db.coin_activity_log.activity_type == 4) &
            (db.coin_activity_log.created_on >= date1)
        ).select()
        
        if len(notifies) == 0:
            # Send first notification
            _email_notify(user, row, email)
            db.coin_activity_log.insert(user_id=user_id, activity_type=4)
    
    return False
```

## Notification System

### Slack Integration
```python
slack_manager = SlackManager(configuration, logger)

def send_vendor_alerts():
    """
    Send Slack notifications for TangoCard API failures
    """
    slack_manager.send_vendor_failed_msg({
        'status': 'ERROR',
        'vendor': 'TangoCard',
        'vendorApi': '/orders',
        'originApi': '[POST] /api/v1/redeem',
        'errorMsg': error_message,
        'meta': json.dumps(error_context)
    })
```

### Email Notifications
```python
def _email_notify(user, row, email):
    """
    Send email alerts to administrators for suspicious activity
    Includes detailed transaction information and SOP links
    """
    mail = Mail()
    mail.settings.server = configuration.get('smtp.server')
    mail.settings.sender = configuration.get('smtp.sender')
    mail.settings.login = configuration.get('smtp.login')
    
    limit = int(os.environ.get('REDEEM_DAILY_LIMIT', 100))
    subject = f'[{project}] Tango Gift Card Daily Quota Alert (user_id: {user.id})'
    
    # Detailed HTML email with transaction details
    message = generate_fraud_alert_email(user, row, email, limit)
    
    mail.send(to=alert_email_list, message=message, subject=subject)
```

### Balance Monitoring
```python
# Low balance alerts
TANGO_INSUFFICIENT_LEVEL = int(configuration.get('tango.insufficient_balance', 30))

if balance < TANGO_INSUFFICIENT_LEVEL:
    msg = f'TangoCard balance ({balance}) below threshold ({TANGO_INSUFFICIENT_LEVEL})'
    slack_manager.send(msg)
```

## Activity Logging

### Activity Types
- **Type 2**: Daily limit violation
- **Type 4**: Email notification sent

### Audit Trail
```python
# Record redemption transaction
db.redeem_transaction.insert(
    user_id=user_id,
    giftcard_id=giftcard_id,
    points=points,
    amount=amount,
    currency=currency,
    transaction_id=tango_transaction_id,
    created_on=now
)

# Record app activity
db.app_data.insert(
    user_id=user_id,
    user_action='Redeem',
    lat=location_lat,
    lon=location_lon,
    gmt_time=now,
    local_time=user_local_time,
    created_on=now,
    modified_on=now
)
```

## Error Handling

### Common Errors
- `ERROR_BAD_REQUEST_BODY` (400): Invalid request parameters
- `ERROR_POINT_INSUFFICIENT` (403): Insufficient points balance
- `ERROR_REDEEMED_FAILED` (403): TangoCard API failure
- `ERROR_REDEEM_DAILY_LIMIT` (403): Daily limit exceeded

### TangoCard Error Handling
```python
try:
    success, transaction_id = _tango_redeem(utid, email, first_name, last_name, amount, currency)
    if not success:
        return json_response.fail(ERROR_REDEEMED_FAILED, T('TangoCard redeem failed'))
except Exception as e:
    slack_manager.send_vendor_failed_msg(error_details)
    return json_response.fail(ERROR_REDEEMED_FAILED, T('TangoCard redeem failed'))
```

## Business Logic

### Points Deduction
```python
# Calculate new balance
available_balance = get_available_points(user_id)
new_balance = round(float(available_balance) - float(points), 2)

if new_balance < 0:
    return json_response.fail(ERROR_POINT_INSUFFICIENT, T('Insufficient coin'))

# Process points transaction
balance, _ = points_transaction(
    user_id, 
    ACTIVITY_TYPE_REDEMPTION, 
    -points,  # Negative for deduction
    note=transaction_id,
    notify=False,
    time=now
)
```

### Gift Card Display
```python
# Format display amounts (multiply by 100 for cents display)
for item in items:
    item['display_rate'] = 100
    item['amount'] = item['amount'] * 100
```

## Security Features

### User Blocking
```python
def is_blocked_user(user_id):
    """
    Check if user is blocked from redemptions
    Integrated fraud prevention system
    """
    blocked = db(db.block_users.user_id == user_id).select().first()
    if blocked and not blocked.is_deleted:
        raise BlockedUserException()
```

### Input Validation
- Email format validation
- Gift card ID existence checking
- Points balance verification
- User authentication requirements

## Performance Considerations

### Caching Strategy
- Gift card catalog caching
- User balance caching
- Activity log optimization
- Email template caching

### Database Optimization
- Indexed queries for daily limit checks
- Efficient redemption transaction logging
- Optimized gift card catalog queries

## Configuration Management
- Environment-based daily limits
- TangoCard API credentials
- SMTP server configuration
- Slack webhook settings
- Alert recipient lists

## Dependencies
- `requests`: HTTP client for TangoCard API
- `json`: JSON data processing
- `json_response`: API response formatting
- `mongo_helper`: MongoDB integration for location tracking
- `datetime_utils`: Timezone conversion utilities
- `slack_helper`: Slack notification system
- `auth`: User authentication
- `points_transaction`: Points management system