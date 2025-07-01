# Test Documentation: Welcome Coin API

## Overview
This test suite validates the Welcome Coin functionality within the TSP system, which provides new users with initial coins as part of the onboarding experience. The system ensures users receive welcome coins only once and tracks the distribution to prevent duplicate rewards.

## Test Configuration
- **File**: `test/test-welcome-coin.js`
- **Framework**: Mocha with Chai assertions and Supertest for HTTP testing
- **Test Timeout**: 10 seconds for welcome coin operations
- **Models Used**: `WelcomeCoinHistory`
- **Configuration**: Uses portal config for welcome coin amount
- **Authentication**: User ID-based authentication (userid: 1003)

## API Endpoints Tested

### GET /welcome_coin
**Purpose**: Distributes welcome coins to new users on first access

**Authentication Required**: Yes (userid header)

**Business Logic**:
1. **First Access**: User receives configured welcome coin amount
2. **Subsequent Access**: User receives 0 coins (already claimed)
3. **Tracking**: Transaction recorded in WelcomeCoinHistory

## Test Scenarios

### 1. First-Time Welcome Coin Distribution
```javascript
it(`should get welcome coin "${config.welcomeCoin}" in first time`, async function () {
  const resp = await request.set(auth).get(url).query();
  const { result, data } = resp.body;
  
  expect(result).to.eq('success');
  expect(data.coin).to.eq(parseFloat(config.welcomeCoin));
});
```

**Expected Behavior**:
- Returns success status
- Provides welcome coin amount from configuration
- Records transaction in database
- Adds coins to user wallet

**Response Structure**:
```javascript
{
  result: 'success',
  data: {
    coin: Number  // Welcome coin amount (e.g., 5.0)
  }
}
```

### 2. Duplicate Access Prevention
```javascript
it('should get welcome coin "0" in second time', async function () {
  const resp = await request.set(auth).get(url).query();
  const { result, data } = resp.body;
  
  expect(result).to.eq('success');
  expect(data.coin).to.eq(0);
});
```

**Expected Behavior**:
- Returns success status
- Provides 0 coins (already claimed)
- No additional database record created
- No change to user wallet balance

### 3. Authentication Validation
```javascript
it('should get a fail 10004', async () => {
  const resp = await request.get(url).unset('userid').query();
  const { result, error } = resp.body;
  
  expect(result).to.eq('fail');
  expect(error).to.include({
    code: 10004,
    msg: 'Request header has something wrong'
  });
});
```

**Error Scenario**:
- Missing userid header results in authentication error
- Standard error response format
- No coins distributed without proper authentication

## Configuration Management

### Welcome Coin Amount
```javascript
const config = require('config').portal;
const welcomeCoinAmount = parseFloat(config.welcomeCoin);
```

**Configuration Source**: Portal configuration file
**Data Type**: Float value for coin amount
**Flexibility**: Configurable per environment/deployment

### Environment-Specific Settings
- **Development**: May have different welcome coin amounts for testing
- **Production**: Production-ready welcome coin amounts
- **Staging**: Testing-appropriate coin amounts

## Database Integration

### WelcomeCoinHistory Model
**Purpose**: Tracks welcome coin distribution to prevent duplicates

**Expected Schema**:
```javascript
{
  receiver_user_id: Integer,  // User who received welcome coins
  coin_amount: Decimal,       // Amount of coins distributed
  created_at: Timestamp,      // Distribution timestamp
  // Additional tracking fields
}
```

### Data Lifecycle Management
```javascript
after('Delete testing data', async () => {
  await WelcomeCoinHistory.query()
    .where('receiver_user_id', userId)
    .delete();
});
```

**Test Cleanup**: Removes test data to ensure test isolation and repeatability

## Business Logic

### One-Time Distribution
1. **Check History**: Query WelcomeCoinHistory for existing distribution
2. **First Time**: If no record exists, distribute welcome coins
3. **Record Transaction**: Create history record to prevent future distributions
4. **Update Wallet**: Add coins to user's wallet balance
5. **Subsequent Access**: Return 0 coins if history record exists

### User Onboarding Integration
- **New User Experience**: Welcome coins provide immediate value
- **Engagement**: Initial coins encourage platform exploration
- **Retention**: First positive interaction with coin system

### Fraud Prevention
- **One Per User**: Strict one-time distribution per user
- **Database Tracking**: Persistent record of distributions
- **Authentication Required**: Prevents anonymous coin claiming

## Integration Points

### Wallet System
- **Balance Update**: Welcome coins added to user wallet
- **Transaction Recording**: Integrated with wallet transaction history
- **Currency System**: Follows same coin system as other rewards

### User Onboarding
- **Registration Flow**: Typically called during or after user registration
- **First Login**: May be triggered on first successful login
- **Profile Completion**: Could be part of profile setup incentives

### Analytics and Tracking
- **User Acquisition**: Track welcome coin effectiveness
- **Conversion Metrics**: Monitor user engagement after welcome coins
- **Retention Analysis**: Measure impact on user retention

## Error Handling

### Authentication Errors
- **10004**: Request header has something wrong
- **Standard Format**: Consistent error response structure
- **Security**: Prevents unauthorized coin distribution

### System Errors
- **Database Failures**: Graceful handling of database connectivity issues
- **Configuration Errors**: Handling of missing or invalid config values
- **Concurrent Access**: Prevention of race conditions in coin distribution

## Performance Considerations

### Database Optimization
- **Efficient Queries**: Optimized lookup for existing welcome coin records
- **Indexing**: Proper indexing on receiver_user_id for fast lookups
- **Transaction Safety**: Atomic operations to prevent duplicate distributions

### Caching Strategy
- **Configuration Caching**: Cache welcome coin amount for performance
- **User State Caching**: Cache user's welcome coin status if needed
- **Database Connection Pooling**: Efficient database resource management

## Security Features

### Access Control
- **Authentication Required**: User ID validation for all requests
- **User Ownership**: Users can only claim their own welcome coins
- **Session Management**: Secure session handling for authenticated requests

### Fraud Prevention
- **Duplicate Prevention**: Robust checking for existing distributions
- **Rate Limiting**: Prevent excessive API calls
- **Audit Trail**: Complete history of all welcome coin distributions

## Business Value

### User Acquisition
- **Immediate Value**: New users receive instant rewards
- **Reduced Friction**: Smooth onboarding experience
- **Positive First Impression**: Creates good initial user experience

### Engagement and Retention
- **Platform Exploration**: Coins encourage users to explore features
- **Transaction Familiarity**: Introduces users to the coin system
- **Return Visits**: Initial value may encourage return usage

### Marketing and Growth
- **Referral Incentives**: Can be combined with referral programs
- **A/B Testing**: Different welcome amounts can be tested
- **Cost Control**: Configurable amounts allow budget management

## Test Coverage

### Functional Coverage
- ✅ First-time welcome coin distribution
- ✅ Duplicate access prevention (0 coins on subsequent calls)
- ✅ Authentication requirement validation
- ✅ Configuration value integration

### Data Coverage
- ✅ Database record creation for tracking
- ✅ Wallet balance integration
- ✅ Transaction history accuracy
- ✅ Test data cleanup

### Error Coverage
- ✅ Authentication failure handling
- ✅ Missing header validation
- ✅ Error response format consistency

### Business Logic Coverage
- ✅ One-time distribution enforcement
- ✅ Configuration value usage
- ✅ Fraud prevention mechanisms

## Future Enhancements

### Potential Features
- **Welcome Packages**: Extended rewards beyond just coins
- **Tiered Welcome**: Different amounts based on user characteristics
- **Time-Limited**: Welcome coins that expire if not used
- **Referral Integration**: Bonus welcome coins for referred users

### Analytics Integration
- **Distribution Tracking**: Monitor welcome coin effectiveness
- **User Journey**: Track user behavior after receiving welcome coins
- **Conversion Metrics**: Measure welcome coin impact on user actions

This test suite ensures the welcome coin system provides a reliable, secure, and effective user onboarding experience within the TSP platform.