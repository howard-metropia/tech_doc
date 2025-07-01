# Card Setting API Test Suite

## Overview
Comprehensive test suite for the Card Setting API, validating payment card management functionality including card creation, retrieval, updates, and deletion. Tests Stripe payment integration and error handling scenarios.

## File Purpose
- **Primary Function**: Test payment card management operations
- **Type**: Integration test suite
- **Role**: Validates Stripe payment card CRUD operations and error handling

## Test Configuration

### Test Setup
- **Framework**: Mocha with Chai assertions
- **HTTP Testing**: Supertest for API endpoint testing
- **Payment Processing**: Stripe integration testing
- **Test User**: User ID 1003
- **Database Models**: AuthUsers, UserWallets

### Dependencies
- `@maas/core/bootstrap`: Application bootstrapping
- `@maas/core/api`: API application factory
- `@maas/core`: Router and core utilities
- `stripe`: Stripe payment processing library
- `supertest`: HTTP assertion library
- `chai`: Assertion library
- `AuthUsers`: User authentication model
- `UserWallets`: User payment wallet model

## Test Scenarios

### POST /card_setting - Card Creation

#### Test Case 1: Add New Payment Card
**Purpose**: Test successful card creation with Stripe token
**Input**: 
```javascript
{ transaction_token: 'tok_visa' }
```

**Expected Response**:
```javascript
{
  "result": "success",
  "data": {
    "cards": [{
      "id": "string",
      "brand": "visa",
      "last4": "4242",
      "expire_year": 2025,
      "expire_month": currentMonth + 1,
      "default": false,
      "postal_code": null,
      "name": null
    }]
  }
}
```

**Validation Steps**:
1. Submit Stripe test token
2. Verify success response
3. Validate card properties structure
4. Confirm Visa card details
5. Store card ID for subsequent tests

### GET /card_setting - Card Retrieval

#### Test Case 1: Get User's Card List
**Purpose**: Retrieve all payment cards for authenticated user
**Expected Behavior**:
- Returns user's payment cards
- First card becomes default automatically
- Card data includes all required properties

**Response Validation**:
```javascript
expect(data.cards[0]).to.includes.keys([
  'id', 'brand', 'last4', 'expire_year',
  'expire_month', 'default', 'postal_code', 'name'
]);
```

### PUT /card_setting - Card Updates

#### Test Case 1: Update Card Information
**Purpose**: Test card detail modification
**Input Data**:
```javascript
{
  card_id: cardId,
  expire_year: 2030,
  expire_month: 12,
  postal_code: '85740',
  default: true
}
```

**Validation**:
- Card updated successfully
- All provided fields modified
- Response contains updated card data
- Card marked as default

### DELETE /card_setting - Card Deletion

#### Test Case 1: Remove Payment Card
**Purpose**: Test card removal from user account
**Input**: Card ID as query parameter
**Expected Behavior**:
- Card removed from user account
- Empty cards array returned
- Stripe customer card deleted

## Error Handling Test Cases

### Authentication Errors (Code 10003)

#### Missing Authorization Token
**Trigger**: Request without Authorization header
**Response**:
```javascript
{
  "result": "fail",
  "error": {
    "code": 10003,
    "msg": "Token required"
  }
}
```

**Affected Endpoints**:
- POST /card_setting
- GET /card_setting
- PUT /card_setting
- DELETE /card_setting

### Validation Errors (Code 10002)

#### Missing Required Fields
**POST without transaction_token**:
```javascript
{
  "error": {
    "code": 10002,
    "msg": "\"transaction_token\" is required"
  }
}
```

**PUT without card_id**:
```javascript
{
  "error": {
    "code": 10002,
    "msg": "\"card_id\" is required"
  }
}
```

**DELETE without card_id**:
```javascript
{
  "error": {
    "code": 10002,
    "msg": "\"card_id\" is required"
  }
}
```

## Stripe Integration Testing

### Customer Deletion Scenarios

#### Test Case 1: Deleted Stripe Customer (Code 23006)
**Setup**: Delete Stripe customer before operations
**Process**:
```javascript
const stripe = Stripe(stripeConfig.apiKey);
const customer = await stripe.customers.del(userStripe.stripe_customer_id);
```

**Expected Behavior**:
- All card operations fail with code 23006
- Error message: "Customer was deleted in Stripe"
- Affected operations: GET, POST, PUT, DELETE

#### Test Case 2: Non-Existent Stripe Customer (Code 23014)
**Setup**: Remove customer ID from user wallet
**Expected Behaviors**:
- **GET**: Returns empty cards array with null last_payment_way
- **PUT/DELETE**: Fail with "Not any card create" message
- **POST**: Creates new Stripe customer automatically

## Authentication Setup

### JWT Token Preparation
```javascript
before('prepare testing data', async () => {
  const { access_token: accessToken } = await AuthUsers.query()
    .select('access_token')
    .findById(userId);
  auth.Authorization = 'Bearer ' + accessToken;
});
```

### Request Headers
```javascript
const auth = {
  userid: userId,
  'Content-Type': 'application/json',
  Authorization: 'Bearer {token}'
};
```

## Stripe Test Data

### Test Tokens
- **tok_visa**: Stripe test token for Visa card
- **Card Details**: 4242 last four digits
- **Expiration**: Future date for testing

### Card Properties
```javascript
{
  id: "stripe_card_id",
  brand: "visa",
  last4: "4242",
  expire_year: 2025,
  expire_month: number,
  default: boolean,
  postal_code: string|null,
  name: string|null
}
```

## Database Integration

### UserWallets Model
- **stripe_customer_id**: Links user to Stripe customer
- **payment_way**: Default payment method tracking
- **Card Storage**: Stripe handles card storage securely

### Data Cleanup
```javascript
after('remove customer id', async () => {
  await UserWallets.query()
    .where('user_id', userId)
    .update({ stripe_customer_id: '' });
});
```

## Security Considerations

### PCI Compliance
- **No Card Storage**: Cards stored in Stripe, not locally
- **Token Usage**: Secure token-based card creation
- **User Isolation**: Cards scoped to authenticated user

### Data Protection
- **Sensitive Data**: Only last 4 digits and metadata stored
- **Secure Transmission**: HTTPS for all card operations
- **Access Control**: User authentication required

## Payment Flow Integration

### Card Lifecycle
1. **Token Generation**: Client-side Stripe token creation
2. **Server Processing**: Token exchange for stored card
3. **Card Management**: Update, default setting, deletion
4. **Payment Processing**: Use stored cards for transactions

### Default Card Logic
- **First Card**: Automatically becomes default
- **Multiple Cards**: Explicit default setting
- **Default Updates**: Only one default card per user

## API Endpoint Details

### URL Patterns
- **Create Card**: `POST /card_setting`
- **Get Cards**: `GET /card_setting`
- **Update Card**: `PUT /card_setting`
- **Delete Card**: `DELETE /card_setting`

### Request/Response Formats

#### Card Creation Request
```javascript
{
  "transaction_token": "tok_visa"
}
```

#### Card Update Request
```javascript
{
  "card_id": "string",
  "expire_year": number,
  "expire_month": number,
  "postal_code": "string",
  "default": boolean
}
```

## Error Recovery Testing

### Stripe Service Failures
- **Network Issues**: Handle Stripe API unavailability
- **Invalid Tokens**: Handle expired or invalid tokens
- **Rate Limiting**: Handle Stripe rate limits

### Database Failures
- **Connection Issues**: Handle database unavailability
- **Transaction Failures**: Ensure data consistency
- **Rollback Scenarios**: Handle partial operation failures

## Performance Considerations

### Stripe API Calls
- **Response Time**: Stripe API latency
- **Rate Limits**: Stripe request quotas
- **Retry Logic**: Handle temporary failures

### Database Operations
- **User Queries**: Efficient user data retrieval
- **Card Lookups**: Fast card information access
- **Transaction Safety**: Atomic operations

## Test Environment Configuration

### Stripe Test Environment
- **Test API Keys**: Non-production Stripe configuration
- **Test Tokens**: Predefined test card tokens
- **Safe Testing**: No real payment processing

### Database State
- **Test User**: Consistent test user (1003)
- **Clean State**: Proper setup and teardown
- **Isolation**: Tests don't interfere with each other

## Maintenance Notes

### Stripe Integration Updates
- **API Versions**: Keep Stripe API version current
- **Test Tokens**: Verify test tokens remain valid
- **Error Handling**: Update error code handling

### Test Coverage Expansion
- **Additional Card Types**: Test more card brands
- **Edge Cases**: More error scenario testing
- **Performance**: Add response time validation

### Future Enhancements
- **Multiple Cards**: Test multiple card management
- **Payment Methods**: Add other payment method types
- **Webhooks**: Test Stripe webhook handling
- **Subscriptions**: Test recurring payment setup