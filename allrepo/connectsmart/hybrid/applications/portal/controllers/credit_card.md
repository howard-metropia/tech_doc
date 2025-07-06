# Credit Card Controller API Documentation

## Overview
The Credit Card Controller manages payment card information for the MaaS platform's wallet system. It integrates with TapPay payment processor to provide secure card storage, management, and payment processing capabilities for mobility services.

**File Path:** `/allrepo/connectsmart/hybrid/applications/portal/controllers/credit_card.py`

**Controller Type:** Authenticated Portal Controller

**Authentication:** JWT token required

## Features
- Secure credit card binding and storage via TapPay integration
- Card management (add, list, delete, set default)
- PCI-compliant payment processing
- Card brand identification and validation
- Default card management
- Automatic card replacement for updates

## API Endpoints

### Credit Card Management
**Endpoint:** `/credit_card/cards`
**Methods:** GET, POST, DELETE, PUT
**Authentication:** JWT token required

#### GET - List Credit Cards
Retrieves all credit cards associated with the user's account.

**Parameters:** None

**Response Format:**
```json
{
  "success": true,
  "data": {
    "cards": [
      {
        "id": "card_12345",
        "bin_code": "424242",
        "last_four": "4242",
        "brand": 1,
        "expire_year": 2025,
        "expire_month": 12,
        "default": true
      },
      {
        "id": "card_67890",
        "bin_code": "555555",
        "last_four": "4444",
        "brand": 2,
        "expire_year": 2024,
        "expire_month": 8,
        "default": false
      }
    ]
  }
}
```

**Status Codes:**
- `200`: Success

#### POST - Add Credit Card
Adds a new credit card using TapPay tokenization.

**Required Fields:**
- `prime`: TapPay prime token from frontend tokenization

**Request Example:**
```json
{
  "prime": "test_3a2fb2b7e892b914a03c95dd4dd5dc7970c908df67a49527c2d1dd4e2d8a2b1d"
}
```

**Response Format:**
```json
{
  "success": true,
  "data": {
    "cards": [
      {
        "id": "card_12345",
        "bin_code": "424242",
        "last_four": "4242",
        "brand": 1,
        "expire_year": 2025,
        "expire_month": 12,
        "default": true
      }
    ]
  }
}
```

**Status Codes:**
- `200`: Successfully added card
- `400`: Invalid parameters
- `403`: Card addition failed

#### DELETE - Remove Credit Card
Removes a credit card from the user's account.

**URL Parameter:**
- `card_id`: ID of card to remove

**Response Format:**
```json
{
  "success": true,
  "data": {
    "cards": []
  }
}
```

**Status Codes:**
- `200`: Successfully removed card
- `400`: Invalid parameters
- `403`: Card deletion failed or card not found

#### PUT - Set Default Card
Sets a specific card as the default payment method.

**URL Parameter:**
- `card_id`: ID of card to set as default

**Response Format:**
```json
{
  "success": true,
  "data": {
    "cards": [
      {
        "id": "card_12345",
        "bin_code": "424242",
        "last_four": "4242",
        "brand": 1,
        "expire_year": 2025,
        "expire_month": 12,
        "default": true
      }
    ]
  }
}
```

**Status Codes:**
- `200`: Successfully set as default
- `400`: Invalid parameters
- `403`: Card not found

## TapPay Integration

### Configuration Parameters
```python
TAPPAY_IS_SANDBOX = configuration.get("tappay.is_sandbox")
TAPPAY_PARTENR_KEY = configuration.get('tappay.partner_key')
TAPPAY_MERCHANT_ID = configuration.get('tappay.merchant_id')
PROJECT_NAME = configuration.get('project.name')
```

### Card Binding Process
1. Frontend tokenizes card details into `prime` token
2. Backend creates TapPay client with merchant credentials
3. Cardholder data is prepared from user profile
4. Card binding API call to TapPay with prime and cardholder info
5. Card metadata is stored locally with TapPay tokens

### TapPay Client Setup
```python
def __get_taypay_client():
    user_tappay_client = tappay.Client(
        is_sandbox=TAPPAY_IS_SANDBOX,
        partner_key=TAPPAY_PARTENR_KEY,
        merchant_id=TAPPAY_MERCHANT_ID
    )
    return user_tappay_client
```

## Data Model

### Credit Card Structure
```python
{
    "id": str,                    # TapPay card identifier
    "bin_code": str,              # First 6 digits of card number
    "last_four": str,             # Last 4 digits of card number
    "brand": int,                 # Mapped card brand identifier
    "expire_year": int,           # Expiration year
    "expire_month": int,          # Expiration month
    "default": bool               # Whether this is the default card
}
```

### Database Storage
```python
{
    "user_id": int,               # User identifier
    "card_id": str,               # TapPay card identifier
    "is_default": bool,           # Default card flag
    "card_token": str,            # TapPay card token
    "card_key": str,              # TapPay card key
    "tappay_member_id": str,      # TapPay member identifier
    "bin_code": str,              # Card BIN code
    "last_four": str,             # Last 4 digits
    "card_type": str,             # TapPay card type
    "funding": str,               # Card funding type
    "expiry_date": str            # YYYYMM format
}
```

## Database Schema

### Table: wallet_user_cards
- `user_id` (FOREIGN KEY): Reference to user
- `card_id`: TapPay card identifier
- `is_default`: Default card status
- `card_token`: Encrypted card token
- `card_key`: TapPay card key
- `tappay_member_id`: TapPay member ID
- `bin_code`: Bank identification number
- `last_four`: Last 4 card digits
- `card_type`: Card type from TapPay
- `funding`: Funding source type
- `expiry_date`: Expiration date (YYYYMM)

## Card Brand Mapping

### Brand Identification
The system maps TapPay card types to internal brand identifiers:
```python
def card_brand_mapping(card_type):
    # Maps TapPay card types to standardized brand codes
    # Returns integer brand identifier
```

**Common Brands:**
- Visa: 1
- Mastercard: 2
- JCB: 3
- American Express: 4

## Security Features

### PCI Compliance
- No raw card data stored locally
- TapPay tokenization for card security
- Encrypted token storage
- Secure communication with TapPay APIs

### Data Protection
- Card tokens encrypted in database
- Minimal card data exposure (only last 4 digits and expiry)
- Secure card removal with TapPay cleanup

### Authentication
- JWT token validation for all operations
- User-scoped card access (users can only access own cards)
- Permission validation for card operations

## Helper Functions

### `__get_cards(user_id)`
Retrieves and formats all cards for a user.
- Queries database for user's cards
- Maps card types to brand identifiers
- Formats expiry dates from YYYYMM to separate year/month
- Returns structured card list

### `__reset_default_card(user_id)`
Resets current default card status.
- Finds existing default card
- Sets `is_default` to False
- Prepares for new default card assignment

### `__remove_card(card_token, card_key)`
Removes card from TapPay system.
- Creates TapPay client
- Calls TapPay card removal API
- Handles cleanup of external card storage

## Error Handling

### TapPay API Errors
```python
if result["status"] != 0:
    logger.error('[TapPay] Add new card failure reason: %s' % result["msg"])
    response.status = 403
    return json_response.fail(ERROR_CARD_ADD_FAILED, T('Add new card failed'))
```

### Error Codes
- `ERROR_BAD_REQUEST_BODY`: Invalid request parameters
- `ERROR_CARD_ADD_FAILED`: TapPay card binding failure
- `ERROR_CARD_DELETE_FAILED`: TapPay card removal failure
- `ERROR_NOT_FOUND_CARD`: Card not found for user

### Exception Handling
- Graceful TapPay API failure handling
- Database transaction rollback on errors
- Comprehensive error logging

## Usage Examples

### Add New Card
```bash
curl -X POST /credit_card/cards \
  -H "Authorization: Bearer <jwt_token>" \
  -H "Content-Type: application/json" \
  -d '{"prime": "test_3a2fb2b7e892b914a03c95dd4dd5dc7970c908df67a49527c2d1dd4e2d8a2b1d"}'
```

### List User Cards
```bash
curl -X GET /credit_card/cards \
  -H "Authorization: Bearer <jwt_token>"
```

### Remove Card
```bash
curl -X DELETE /credit_card/cards/card_12345 \
  -H "Authorization: Bearer <jwt_token>"
```

### Set Default Card
```bash
curl -X PUT /credit_card/cards/card_12345 \
  -H "Authorization: Bearer <jwt_token>"
```

## Integration Points

### Payment Processing
- Links to transaction processing workflows
- Default card selection for automatic payments
- Card validation for payment authorization

### Wallet System
- Integrates with wallet balance management
- Supports top-up and payment operations
- Links to transaction history

### Mobile Applications
- Frontend tokenization integration
- Secure card addition workflows
- Card management UI support

## TapPay API Integration

### Card Binding
```python
result = user_tappay_client.bind_card(
    prime=prime,
    card_holder_data=cardholder
)
```

### Card Removal
```python
taypay_client.remove_card(card_key, card_token)
```

### Cardholder Data Structure
```python
cardholder = tappay.Models.CardHolderData(
    phone_number=user.phone_number,
    name='{} {}'.format(user.first_name, user.last_name),
    email=user.email,
    member_id='{}-{}'.format(PROJECT_NAME, user_id)
)
```

## Performance Optimization

### Database Efficiency
- Indexed user_id for fast card lookups
- Minimal data storage (only essential card metadata)
- Efficient default card management

### API Optimization
- Cached card brand mappings
- Batch operations where possible
- Optimized TapPay client reuse

## Compliance and Regulation

### PCI DSS Compliance
- No storage of sensitive card data
- Tokenization for all card operations
- Secure transmission to payment processors

### Data Retention
- Automatic cleanup on card removal
- Compliant data handling practices
- Audit trails for card operations

## Troubleshooting

### Common Issues
1. **TapPay Prime Token Errors**: Validate frontend tokenization
2. **Card Binding Failures**: Check TapPay configuration and credentials
3. **Default Card Issues**: Verify card ownership and existence
4. **Card Removal Failures**: Check TapPay API connectivity

### Debug Information
- Comprehensive TapPay API response logging
- Card operation audit trails
- Error context preservation for troubleshooting