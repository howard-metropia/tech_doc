# Portal Transaction Controller

## Overview
Manages financial transactions, payment processing, and transaction history for the ConnectSmart Portal, integrating with TapPay payment gateway for carpooling and mobility service payments. Provides comprehensive transaction management and reporting capabilities.

## File Details
- **Location**: `/applications/portal/controllers/transaction.py`
- **Type**: web2py Controller
- **Authentication**: JWT-based authentication required
- **Dependencies**: TapPay SDK, payment processing, transaction tracking

## Configuration
```python
TAPPAY_IS_SANDBOX = configuration.get("tappay.is_sandbox")
TAPPAY_PARTENR_KEY = configuration.get('tappay.partner_key')
TAPPAY_MERCHANT_ID = configuration.get('tappay.merchant_id')
PROJECT_NAME = configuration.get('project.name')
```

## Controller Functions

### `transaction()` - GET/POST Transaction Management
Handles payment processing and transaction retrieval for carpooling services.

#### GET - Retrieve Transaction Details
```
GET /api/v1/transaction?order_number=<order_number>
```

**Request Parameters**:
```python
{
    "order_number": "string"  # Unique transaction order number
}
```

**Response Structure**:
```python
{
    "amount": float,              # Transaction amount
    "status": int,               # Transaction status code
    "transaction_time_millis": int, # Transaction timestamp
    "last_four": "string",       # Last 4 digits of card
    "brand": "string"            # Card brand (Visa, MasterCard, etc.)
}
```

#### POST - Process New Transaction
```
POST /api/v1/transaction
```

**Request Parameters**:
```python
{
    "reservation_id": "string",  # Carpooling reservation ID
    "card_id": "string"         # Optional: specific card ID to use
}
```

**Business Logic Flow**:
1. **Reservation Validation**: Verify carpooling reservation exists
2. **Price Calculation**: Extract price from DUO reservation
3. **Payment Method**: Select default or specified card
4. **TapPay Processing**: Execute payment through TapPay gateway
5. **Transaction Recording**: Store transaction details in database

### `transaction_history()` - GET Transaction History
Retrieves paginated transaction history for authenticated user.

#### Endpoint
```
GET /api/v1/transaction_history?offset=0&perpage=10
```

**Request Parameters**:
```python
{
    "offset": int,    # Starting record offset (default: 0)
    "perpage": int    # Records per page (default: 10)
}
```

**Response Structure**:
```python
{
    "transactions": [
        {
            "amount": float,
            "status": int,
            "transaction_time_millis": int,
            "last_four": "string",
            "brand": "string",
            "order_number": "string"
        }
    ],
    "total_count": int,
    "next_offset": int
}
```

### `tappay_notify()` - POST TapPay Webhook
Handles TapPay payment gateway webhook notifications for transaction updates.

#### Endpoint
```
POST /api/v1/tappay_notify
```

**Webhook Payload**:
```python
{
    "order_number": "string",
    "bank_result_code": "string",
    "status": int,
    "rec_trade_id": "string",
    "bank_result_msg": "string",
    "bank_transaction_id": "string",
    "acquirer": "string",
    "transaction_time_millis": int,
    "msg": "string"
}
```

### `carpooling_transaction_history()` - GET Admin Transaction History
Administrative endpoint for comprehensive transaction reporting.

#### Authentication
- **Required**: Metropia role membership
- **Access Level**: Administrative only

#### GET - Comprehensive Transaction Report
```
GET /api/v1/carpooling_transaction_history?offset=0&perpage=10
```

**Response Structure**:
```python
{
    "transactions": [
        {
            "order_number": "string",
            "amount": float,
            "status": int,
            "transaction_time_millis": int,
            "last_four": "string",
            "brand": "string",
            "payee_user_id": int,
            "payee_bank_account_number": "string",
            "payee_bank_code": "string",
            "payee_bank_user_name": "string",
            "payee_bank_name": "string",
            "payee_id_number": "string",
            "payee_bank_branch": "string",
            "payee_address": "string",
            "payee_residence_address": "string",
            "payee_status": int,
            "modified_on": "datetime"
        }
    ],
    "total_count": int,
    "next_offset": int
}
```

#### PUT - Update Transaction Status
```
PUT /api/v1/carpooling_transaction_history
```

**Request Parameters**:
```python
{
    "order_number": "string",
    "status": int
}
```

## Payment Processing Architecture

### TapPay Integration
```python
def __get_taypay_client():
    """Initialize TapPay client with configuration"""
    user_tappay_client = tappay.Client(
        is_sandbox=TAPPAY_IS_SANDBOX,
        partner_key=TAPPAY_PARTENR_KEY,
        merchant_id=TAPPAY_MERCHANT_ID
    )
    return user_tappay_client
```

### Order Number Generation
```python
order_number = "{year}{month}{day}-{hour}{min}{sec}-{userid}{payeeid}".format(
    year=now.year,
    month=now.month,
    day=now.day,
    hour=now.hour,
    min=now.hour,  # Note: Appears to be a bug, should be minute
    sec=now.second,
    userid=user_id,
    payeeid=payee_user_id,
)
```

### Payment Execution
```python
result = user_tappay_client.pay_by_token(
    card_key=row.card_key,
    card_token=row.card_token,
    amount=price,
    details="metropia order",
    order_number=order_number
)
```

## Transaction Data Model

### Wallet User Transactions Table
```python
db.wallet_user_transactions:
    user_id: int                    # Payer user ID
    payee_user_id: int             # Recipient user ID
    amount: decimal                # Transaction amount
    status: int                    # Transaction status
    order_number: string           # Unique order identifier
    transaction_time_millis: int   # Transaction timestamp
    last_four: string              # Card last 4 digits
    card_type: string              # Card brand/type
    rec_trade_id: string           # TapPay transaction ID
    bank_transaction_id: string    # Bank reference ID
    acquirer: string               # Payment acquirer
    return_msg: string             # TapPay response message
    bank_result_code: string       # Bank result code
    bank_result_msg: string        # Bank result message
```

### Transaction Status Table
```python
db.wallet_transaction_status:
    transaction_id: int   # Foreign key to wallet_user_transactions
    payee_status: int    # Payee transaction status
    modified_on: datetime # Last modification timestamp
```

## Carpooling Integration

### DUO Reservation Processing
1. **Reservation Lookup**: Find all reservations for the offer
2. **Driver Identification**: Identify driver (role == 1) in reservation group
3. **Price Extraction**: Get carpooling price from DUO reservation
4. **Payment Processing**: Execute payment from passenger to driver

```python
# Find all reservations for the offer
row1 = db(db.duo_reservation.reservation_id == reservation_id).select(db.duo_reservation.offer_id).first()
row2 = db(db.duo_reservation.offer_id == row1.offer_id).select(db.duo_reservation.reservation_id)

# Identify driver and extract price
for r in row2:
    row = db(
        (db.reservation.id == r.reservation_id) &
        (db.reservation.role == 1)  # Driver role
    ).select(
        db.reservation.user_id, 
        db.duo_reservation.price,
        left=db.duo_reservation.on(db.reservation.id == db.duo_reservation.reservation_id)
    ).first()
```

## Security Features

### Authentication & Authorization
- **JWT Authentication**: Secure user authentication for all endpoints
- **Role-based Access**: Administrative endpoints restricted to Metropia role
- **User Context**: Transactions scoped to authenticated user

### Payment Security
- **TapPay Integration**: PCI-compliant payment processing
- **Token-based Payments**: No raw card data storage
- **Transaction Verification**: Webhook validation for payment confirmation

### Data Protection
- **Card Data Security**: Only last 4 digits and brand stored
- **Transaction Isolation**: User-specific transaction access
- **Audit Trail**: Comprehensive transaction logging

## Error Handling

### Payment Errors
```python
ERROR_NOT_FOUND_CARD = "Card not found"
ERROR_CALL_TAPPAY_FAILED = "TapPay API call failed"
ERROR_NOT_FOUND_RESERVATION = "Reservation not found"
ERROR_NOT_FOUNT_TRANSACTION = "Transaction not found"
```

### Validation Errors
- **Parameter Validation**: Required field checking
- **Amount Validation**: Price format and range validation
- **Card Validation**: Payment method verification

## Utility Functions

### Card Brand Mapping
```python
from utils import card_brand_mapping

# Maps card type codes to user-friendly brand names
brand = card_brand_mapping(row.card_type)
```

### Payee Information Retrieval
```python
def _get_payee_info(user_id):
    """Retrieves bank account information for payee"""
    sql = db.wallet_user_bank_account.user_id == user_id
    row = db(sql).select(db.wallet_user_bank_account.ALL).first()
    return {
        "bank_account_number": row.bank_account_number,
        "bank_code": row.bank_code,
        "bank_user_name": row.bank_user_name,
        # ... additional bank details
    }
```

## Performance Considerations

### Database Optimization
- **Transaction Indexing**: Optimized queries for transaction lookup
- **Pagination Support**: Efficient large dataset handling
- **Join Optimization**: Efficient payee information retrieval

### External API Management
- **TapPay Rate Limiting**: Appropriate API call management
- **Timeout Handling**: Robust external service integration
- **Retry Logic**: Payment processing resilience

## Dependencies
- **TapPay SDK**: Payment gateway integration
- **json_response**: Standardized API responses
- **card_brand_mapping**: Card type utility functions
- **Wallet System**: User wallet and card management
- **DUO Reservation System**: Carpooling reservation integration

## Usage Examples

### Process Carpooling Payment
```python
# Request
POST /api/v1/transaction
{
    "reservation_id": "67890",
    "card_id": "card_abc123"
}

# Response
{
    "status": "success",
    "data": {
        "amount": 12.50,
        "status": 0,
        "transaction_time_millis": 1639123456,
        "last_four": "4321",
        "brand": "Visa"
    }
}
```

### Retrieve Transaction History
```python
# Request
GET /api/v1/transaction_history?offset=0&perpage=5

# Response
{
    "status": "success",
    "data": {
        "transactions": [
            {
                "amount": 12.50,
                "status": 0,
                "transaction_time_millis": 1639123456,
                "last_four": "4321",
                "brand": "Visa",
                "order_number": "20211210-143000-12345678"
            }
        ],
        "total_count": 1,
        "next_offset": 1
    }
}
```

This controller provides comprehensive transaction management capabilities for carpooling payments, integrating securely with TapPay payment gateway while maintaining detailed transaction records and administrative oversight capabilities.