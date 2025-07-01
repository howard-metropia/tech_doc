# TapPay Payment Integration Module Documentation

## Overview
The TapPay Payment Integration Module provides comprehensive payment processing functionality for the ConnectSmart Hybrid Portal application. It's an extended implementation of the TapPay Python SDK, offering credit card payments, tokenization, refunds, and advanced payment features with TWD currency support.

## File Location
**Source**: `/home/datavan/METROPIA/metro_combine/allrepo/connectsmart/hybrid/applications/portal/modules/tappay.py`

## Dependencies
- `sys`, `os`: System and environment operations
- `logging`: Payment operation logging
- `platform.python_version`: Runtime version detection
- `requests`: HTTP client for TapPay API communication

## Module Information
- **Version**: 0.4.0
- **Base**: Extended from PyPI tappay package
- **API**: TapPay REST API integration
- **Currency**: Taiwan Dollar (TWD) support

## Exception Classes

### Exceptions Hierarchy
```python
class Exceptions:
    class Error(Exception):              # Base exception class
    class ClientError(Error):            # 4xx HTTP status errors
    class ServerError(Error):            # 5xx HTTP status errors  
    class AuthenticationError(ClientError): # 401 authentication failures
```

## Model Classes

### Models.Currencies
**Purpose**: Supported currency constants
- `TWD`: Taiwan Dollar (primary supported currency)

### Models.CardHolderData
**Purpose**: Credit card holder information structure

#### Constructor
```python
def __init__(self, phone_number, name, email, 
             zip_code=None, address=None, 
             national_id=None, member_id=None)
```

#### Required Fields
- `phone_number` (str): Card holder phone number
- `name` (str): Card holder full name
- `email` (str): Card holder email address

#### Optional Fields
- `zip_code` (str): Postal code
- `address` (str): Billing address
- `national_id` (str): National identification number
- `member_id` (str): Merchant member ID

#### Methods
##### `to_dict(self)`
**Purpose**: Convert card holder data to dictionary format for API requests
**Returns**: Dictionary with card holder information

## Client Class

### Constructor
```python
def __init__(self, is_sandbox, partner_key=None, 
             merchant_id=None, app_name=None, app_version=None)
```

#### Parameters
- `is_sandbox` (bool): Environment flag (sandbox vs production)
- `partner_key` (str, optional): TapPay partner key
- `merchant_id` (str, optional): TapPay merchant ID
- `app_name` (str, optional): Application name for user-agent
- `app_version` (str, optional): Application version for user-agent

#### Environment Configuration
- **Sandbox**: `sandbox.tappaysdk.com`
- **Production**: `prod.tappaysdk.com`

#### Authentication
- Partner key from parameter or environment variable `TAPPAY_PARTNER_KEY`
- Merchant ID from parameter or environment variable `TAPPAY_MERCHANT_ID`

### Core Payment Methods

#### `pay_by_prime(self, prime, amount, details, card_holder_data, **kwargs)`
**Purpose**: Process payment using prime token from TapPay frontend SDK

**Parameters**:
- `prime` (str): Prime token from TapPay SDK
- `amount` (int): Payment amount in cents
- `details` (str): Transaction description
- `card_holder_data` (CardHolderData): Card holder information
- `**kwargs`: Additional payment parameters

**Returns**: API response dictionary

**Example**:
```python
card_holder = Models.CardHolderData(
    phone_number="+886912345678",
    name="張三",
    email="user@example.com"
)

response = client.pay_by_prime(
    prime="prime_token_from_frontend",
    amount=2500,  # $25.00 in cents
    details="Product purchase",
    card_holder_data=card_holder
)
```

#### `pay_by_token(self, card_key, card_token, amount, details, **kwargs)`
**Purpose**: Process payment using stored card tokens

**Parameters**:
- `card_key` (str): Previously obtained card key
- `card_token` (str): Previously obtained card token
- `amount` (int): Payment amount in cents
- `details` (str): Transaction description
- `**kwargs`: Additional payment parameters

**Returns**: API response dictionary

**Example**:
```python
response = client.pay_by_token(
    card_key="card_key_12345",
    card_token="card_token_67890",
    amount=1500,
    details="Subscription payment"
)
```

### Refund Operations

#### `refund(self, rec_trade_id, amount, **kwargs)`
**Purpose**: Process payment refund

**Parameters**:
- `rec_trade_id` (str): TapPay transaction record ID
- `amount` (int): Refund amount in cents
- `**kwargs`: Additional refund parameters

**Returns**: API response dictionary

#### `cancel_refund(self, rec_trade_id, **kwargs)`
**Purpose**: Cancel previously issued refund

**Parameters**:
- `rec_trade_id` (str): Transaction record ID
- `**kwargs`: Additional parameters

### Record Management

#### `get_records(self, filters_dict, page=0, records_per_page=50, order_by_dict=None)`
**Purpose**: Query historical transaction records

**Parameters**:
- `filters_dict` (dict): TapPay-defined filter criteria
- `page` (int): Page number (default: 0)
- `records_per_page` (int): Records per page (default: 50)
- `order_by_dict` (dict, optional): Sort criteria

**Returns**: Paginated transaction records

**Example**:
```python
filters = {
    "time": {
        "start_time": 1640995200,  # Unix timestamp
        "end_time": 1641081600
    }
}

records = client.get_records(
    filters_dict=filters,
    page=0,
    records_per_page=20
)
```

### Advanced Features

#### `capture_today(self, rec_trade_id)`
**Purpose**: Capture authorized payment
**Parameters**: `rec_trade_id` (str): Transaction record ID

#### `cancel_capture(self, rec_trade_id)`
**Purpose**: Cancel payment capture
**Parameters**: `rec_trade_id` (str): Transaction record ID

#### `get_trade_history(self, rec_trade_id)`
**Purpose**: Get detailed transaction history
**Parameters**: `rec_trade_id` (str): Transaction record ID

### Card Management

#### `bind_card(self, prime, card_holder_data, **kwargs)`
**Purpose**: Bind credit card for future payments

**Parameters**:
- `prime` (str): Prime token from frontend SDK
- `card_holder_data` (CardHolderData): Card holder information
- `**kwargs`: Additional binding parameters

**Returns**: Card key and token for future payments

#### `remove_card(self, card_key, card_token)`
**Purpose**: Remove bound credit card

**Parameters**:
- `card_key` (str): Card key to remove
- `card_token` (str): Card token to remove

## HTTP Client Implementation

### Request Headers
```python
headers = {
    'Content-Type': 'application/json',
    'User-Agent': 'tappay-python/{version} python/{py_version} {app}/{app_version}',
    'x-api-key': partner_key
}
```

### Response Handling
- **200-299**: Success responses (return JSON)
- **204**: No content (return None)
- **401**: Authentication error (raise AuthenticationError)
- **400-499**: Client errors (raise ClientError)
- **500-599**: Server errors (raise ServerError)

### Logging Integration
```python
logger = logging.getLogger("tappay")

# Request logging
logger.debug("POST to: {}".format(uri))
logger.debug("POST headers: {}".format(headers))
logger.debug("POST params: {}".format(params))

# Response logging
logger.debug("response status: {}".format(response.status_code))
logger.debug("response content: {}".format(response.content))
```

## Usage Examples

### Basic Setup
```python
# Initialize client
client = Client(
    is_sandbox=True,  # Use sandbox for testing
    partner_key="partner_key_from_tappay",
    merchant_id="merchant_id_from_tappay",
    app_name="ConnectSmart Portal",
    app_version="1.0.0"
)
```

### Complete Payment Flow
```python
# 1. Create card holder data
card_holder = Models.CardHolderData(
    phone_number="+886912345678",
    name="張小明",
    email="user@example.com",
    zip_code="10001",
    address="台北市信義區信義路五段7號"
)

# 2. Process payment
try:
    response = client.pay_by_prime(
        prime="prime_from_frontend_sdk",
        amount=2500,  # $25.00
        details="商品購買 - 會員方案",
        card_holder_data=card_holder
    )
    
    if response.get('status') == 0:  # Success
        print(f"Payment successful: {response['rec_trade_id']}")
    else:
        print(f"Payment failed: {response['msg']}")
        
except Exceptions.AuthenticationError:
    print("Authentication failed - check partner key")
except Exceptions.ClientError as e:
    print(f"Client error: {e}")
except Exceptions.ServerError as e:
    print(f"Server error: {e}")
```

### Card Tokenization
```python
# Bind card for future payments
try:
    bind_response = client.bind_card(
        prime="prime_token",
        card_holder_data=card_holder
    )
    
    if bind_response.get('status') == 0:
        card_key = bind_response['card_key']
        card_token = bind_response['card_token']
        
        # Store tokens securely for future use
        save_user_payment_method(user_id, card_key, card_token)
        
        # Use tokens for payment
        payment_response = client.pay_by_token(
            card_key=card_key,
            card_token=card_token,
            amount=1000,
            details="Monthly subscription"
        )
        
except Exception as e:
    print(f"Card binding failed: {e}")
```

### Refund Processing
```python
# Process refund
try:
    refund_response = client.refund(
        rec_trade_id="TT12345678901234567890",
        amount=1500  # Partial refund
    )
    
    if refund_response.get('status') == 0:
        print("Refund processed successfully")
    else:
        print(f"Refund failed: {refund_response['msg']}")
        
except Exception as e:
    print(f"Refund error: {e}")
```

### Transaction History
```python
# Get transaction records
filters = {
    "time": {
        "start_time": int(time.time()) - 86400,  # Last 24 hours
        "end_time": int(time.time())
    },
    "amount": {
        "gte": 1000,  # Minimum $10
        "lte": 10000  # Maximum $100
    }
}

try:
    records = client.get_records(
        filters_dict=filters,
        records_per_page=50
    )
    
    for record in records.get('trade_records', []):
        print(f"Transaction: {record['rec_trade_id']} - ${record['amount']/100}")
        
except Exception as e:
    print(f"Failed to retrieve records: {e}")
```

## Configuration Best Practices

### Environment Variables
```bash
# Sandbox
export TAPPAY_PARTNER_KEY="partner_key_sandbox"
export TAPPAY_MERCHANT_ID="merchant_id_sandbox"

# Production
export TAPPAY_PARTNER_KEY="partner_key_production"  
export TAPPAY_MERCHANT_ID="merchant_id_production"
```

### Security Considerations
- Store API keys as environment variables
- Use sandbox for development and testing
- Implement proper error handling for payment failures
- Log payment attempts for audit purposes
- Validate amounts and currency before processing
- Secure storage of card tokens
- Regular key rotation

## Error Handling Patterns

### Payment Validation
```python
def process_payment_safely(client, payment_data):
    try:
        # Validate input
        if payment_data['amount'] <= 0:
            raise ValueError("Invalid payment amount")
            
        # Process payment
        response = client.pay_by_prime(**payment_data)
        
        # Check TapPay response
        if response.get('status') != 0:
            raise PaymentError(response.get('msg', 'Payment failed'))
            
        return response
        
    except Exceptions.AuthenticationError:
        logger.error("TapPay authentication failed")
        raise
    except Exceptions.ClientError as e:
        logger.error(f"TapPay client error: {e}")
        raise
    except Exception as e:
        logger.error(f"Unexpected payment error: {e}")
        raise
```

## Integration with Portal System

### Payment Processing Pipeline
1. **Frontend**: Collect payment info and generate prime token
2. **Backend**: Receive prime token and process payment
3. **Database**: Store transaction records
4. **Notifications**: Send payment confirmations
5. **Reconciliation**: Match payments with TapPay records

### Database Schema Integration
```sql
CREATE TABLE payments (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    rec_trade_id VARCHAR(255) UNIQUE,
    amount DECIMAL(10,2),
    status ENUM('pending', 'completed', 'failed', 'refunded'),
    payment_method VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## Related Components
- User profile management
- Order processing system
- Notification services
- Audit logging system
- Financial reporting tools