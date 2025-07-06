# TSP Job Test: Token Notification System Test Documentation

## Quick Summary

**Purpose**: Comprehensive test suite for token notification system that validates token acquisition and expiration notifications for agency-managed campaigns.

**Key Features**:
- Tests token acquisition notifications (`tokenGetNotification`)
- Tests token expiration notifications (`tokenExpireNotification`)
- Validates notification delivery across multiple database tables
- Handles scenarios with partially used and fully used tokens
- Ensures proper cleanup and message content validation

**Technology Stack**: Mocha testing framework, Chai assertions, Knex.js for database operations

## Technical Analysis

### Code Structure

The test file implements three distinct test suites for different token notification scenarios:

```javascript
// Core service imports
const {
  tokenGetNotification,
  tokenExpireNotification,
} = require('@app/src/services/tokenNotification');

// Database and logging
const knex = require('@maas/core/mysql')('portal');
const { logger } = require('@maas/core/log');
```

### Key Components

**Database Schema Integration**:
- `agency`: Agency management and identification
- `token_campaign`: Token campaign definitions and lifecycle
- `campaign`: Individual campaigns linked to tokens
- `token_transaction`: Transaction history for token usage
- `notification`: Core notification records
- `notification_msg`: Message content and formatting
- `notification_user`: User-specific notification delivery

**Test Data Generation**:
```javascript
// Dynamic ID generation to avoid conflicts
const agency = await knex('agency').max('ap_agency_id as ap_agency_id');
if (agency.length > 0 && agency[0].ap_agency_id)
  apAgencyId = agency[0].ap_agency_id + 1;
```

**Notification Flow Validation**:
- Creates test agencies, tokens, and campaigns
- Generates token transactions with different activity types
- Validates notification creation and content
- Ensures proper user targeting and message delivery

### Implementation Details

**Test Suite Organization**:
1. **Token Acquisition Tests**: Validates notifications when tokens are issued
2. **Token Expiration Tests**: Tests notifications when tokens expire with remaining balance
3. **Partial Usage Tests**: Handles tokens with some usage before expiration
4. **Full Usage Tests**: Ensures no notifications for fully consumed tokens

**Token Transaction Types**:
```javascript
// Activity type 1: Token acquisition/issuance
activity_type: 1,
tokens: amount  // Positive value for credit

// Activity type 2: Token usage/consumption  
activity_type: 2,
tokens: used    // Negative value for debit
```

**Notification Data Structure**:
```javascript
const notificationId = result.notificationId;
const notificationMsgId = result.notificationMsgId;
const notificationUserId = result.notificationUserId;
```

## Usage/Integration

### Test Execution

**Running Token Notification Tests**:
```bash
# Run complete token notification test suite
npm test test/testTokenNotification.js

# Run with debug logging
DEBUG=* npm test test/testTokenNotification.js
```

**Test Environment Requirements**:
- MySQL portal database with complete schema
- Existing user records in `auth_user` table
- Proper database permissions for CRUD operations

### Service Integration

**Notification Service Usage**:
```javascript
// Get token notifications
const results = await tokenGetNotification();

// Expire token notifications  
const results = await tokenExpireNotification();
```

**Database Transaction Flow**:
1. Create agency and token campaign
2. Generate token transactions (issuance and usage)
3. Trigger notification services
4. Validate notification records across related tables
5. Clean up test data

### Integration Points

**Agency Management**:
- Integrates with agency registration system
- Requires valid agency configurations
- Links to external Admin Platform agency IDs

**Campaign Management**:
- Connects with campaign lifecycle management
- Handles token allocation and tracking
- Manages expiration dates and business rules

## Dependencies

### Core Dependencies

**Testing Framework**:
- `chai`: Assertion library with `assert` interface
- `mocha`: Test runner framework (implicit)

**Database Layer**:
- `@maas/core/mysql`: MySQL connection management
- `knex`: SQL query builder and migration tool

**Services**:
- `@app/src/services/tokenNotification`: Core notification service
- `@maas/core/log`: Logging infrastructure with configurable levels

### Database Schema Dependencies

**Required Tables**:
```sql
-- Agency management
agency (id, name, ap_agency_id)

-- Token and campaign definitions  
token_campaign (id, ap_token_id, name, issued_on, expired_on, agency_id)
campaign (id, name, token_id, ap_campaign_id, tokens)

-- Transaction tracking
token_transaction (id, activity_type, campaign_id, user_id, tokens, ...)

-- Notification system
notification (id, msg_data, ...)
notification_msg (id, msg_body, ...)  
notification_user (id, user_id, ...)

-- User management
auth_user (id, ...)
```

**Database Constraints**:
- Foreign key relationships between agencies, tokens, and campaigns
- Proper indexing on user_id and campaign_id fields
- Date range validation for token validity periods

## Code Examples

### Basic Test Setup Pattern

```javascript
describe('test get token notification', () => {
  let agencyId = null;
  let tokenId = null;
  let campaignId = null;
  let userId = null;
  let transactionId = null;
  const amount = 5;
  let results = [];

  before(async () => {
    // Generate unique IDs to avoid conflicts
    const agency = await knex('agency').max('ap_agency_id as ap_agency_id');
    if (agency.length > 0 && agency[0].ap_agency_id)
      apAgencyId = agency[0].ap_agency_id + 1;

    // Create test agency
    agencyName = `test Agency`;
    [agencyId] = await knex('agency').insert({
      name: agencyName,
      ap_agency_id: apAgencyId,
    });

    // Setup token campaign and transactions
    // ... detailed setup code
  });

  after(async () => {
    // Comprehensive cleanup
    await knex('agency').where({ id: agencyId }).delete();
    await knex('token_campaign').where({ id: tokenId }).delete();
    await knex('campaign').where({ id: campaignId }).delete();
    // ... cleanup all related records
  });
});
```

### Token Transaction Creation

```javascript
// Create token issuance transaction
[transactionId] = await knex('token_transaction').insert({
  activity_type: 1,  // Acquisition
  campaign_id: tokenId,
  ap_campaign_id: campaignId,
  f_agency_id: apAgencyId,
  agency_name: agencyName,
  f_token_id: apTokenId,
  token_name: `test Token ${apTokenId}`,
  f_campaign_id: apCampaignId,
  campaign_name: `test Campaign ${apCampaignId}`,
  issued_on: issuedOn,
  expired_on: expiredOn,
  user_id: userId,
  tokens: amount,  // Positive value for credit
});

// Create token usage transaction
[transactionId2] = await knex('token_transaction').insert({
  activity_type: 2,  // Usage
  // ... same campaign details
  tokens: used,  // Negative value for debit
});
```

### Notification Validation Pattern

```javascript
it('send one get token notification', async () => {
  results = await tokenGetNotification();
  assert.isTrue(results.length > 0);
  
  for (const result of results) {
    // Validate notification record
    const notifications = await knex('notification').where({
      id: result.notificationId,
    });
    assert.isTrue(notifications.length > 0);
    
    // Check message data structure
    for (const notification of notifications) {
      assert.equal(JSON.parse(notification.msg_data).agency_id, apAgencyId);
    }
    
    // Validate message content
    const notificationMsgs = await knex('notification_msg').where({
      id: result.notificationMsgId,
    });
    assert.isTrue(notificationMsgs.length > 0);
    
    for (const notificationMsg of notificationMsgs) {
      logger.info(notificationMsg.msg_body);
      assert.isTrue(
        notificationMsg.msg_body.indexOf(amount.toString()) > -1,
        'Should contain token amount number.'
      );
      assert.isTrue(
        notificationMsg.msg_body.indexOf(agencyName) > -1,
        'Should contain agency name.'
      );
    }
    
    // Validate user targeting
    const notificationUsers = await knex('notification_user').where({
      id: result.notificationUserId,
    });
    assert.isTrue(notificationUsers.length > 0);
    
    for (const notificationUser of notificationUsers) {
      assert.equal(notificationUser.user_id, userId);
    }
  }
});
```

### Expiration Scenarios

```javascript
describe('test all used token expired notification', () => {
  // Setup with fully consumed tokens
  const amount = 5;
  const used = -5;  // Fully consumed
  
  it('will not send token expire notification', async () => {
    results = await tokenExpireNotification();
    assert.isTrue(results.length === 0);  // No notifications expected
  });
});

describe('test some used token expired notification', () => {
  // Setup with partially consumed tokens
  const amount = 5;
  const used = -2.5;  // Partially consumed
  
  it('send one token expire notification', async () => {
    results = await tokenExpireNotification();
    assert.isTrue(results.length > 0);  // Notifications expected
    // ... validation similar to acquisition tests
  });
});
```

This comprehensive test suite ensures the token notification system correctly handles all scenarios from token issuance through expiration, while maintaining data integrity across the complex multi-table notification architecture.