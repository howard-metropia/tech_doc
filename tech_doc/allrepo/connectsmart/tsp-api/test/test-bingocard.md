# Bingocard Service Test Suite

## Overview
Comprehensive test suite for the Bingocard service, covering both unit tests and integration tests for challenge participation functionality. Tests the `addToChallenge` method's ability to handle various campaign scenarios and user enrollment processes.

## File Purpose
- **Primary Function**: Test bingocard challenge enrollment logic
- **Type**: Unit and integration test suite
- **Role**: Validates challenge participation, user permissions, and welcome coin distribution

## Test Configuration

### Test Setup
- **Framework**: Mocha with Chai assertions
- **Mocking**: Sinon for external service mocking
- **Database**: Knex for direct database operations
- **HTTP Testing**: Supertest for integration tests
- **Test User**: User ID 1003
- **Test Campaign**: Campaign ID 1, Bingocard ID 1

### Dependencies
- `@maas/core/bootstrap`: Application bootstrapping
- `knex`: Direct database access
- `sinon`: Stubbing and mocking framework
- `superagent`: HTTP client for external service calls
- `chai`: Assertion library
- `supertest`: HTTP testing library

## Unit Test Scenarios

### Test Suite 1: User Not Joined Challenge

#### Setup
- **Campaign Data**: Active 30-day challenge with onboarding weight
- **User Status**: Not currently enrolled in challenge
- **External API Mock**: Returns successful challenge data and enrollment

#### Campaign Configuration
```javascript
{
  id: 1,
  title: "Explorer Challenge",
  description: "Complete this Challenge and earn rewards...",
  reward_type: 1,
  reward_amount: 3,
  image_url: "https://s3-us-east-2.amazonaws.com/smart-maas-develop/...",
  start_time: "YYYY-MM-DD HH:mm:ss",
  end_time: "YYYY-MM-DD HH:mm:ss",
  bingocard_id: 1,
  persona: "biking,carpool,driving,transit",
  gen_weight: "onboard",
  available_activity: [1, 2, 3, ..., 32],
  width: 3,
  height: 3,
  users: []
}
```

#### Test Validation
- **Result Type**: Object with user creation details
- **Created User ID**: Matches test user (1003)
- **Permissions**: Calendar and notification permissions from database
- **Expected Behavior**: User successfully added to challenge

### Test Suite 2: No Current Campaign Data

#### Setup
- **Campaign Data**: Empty campaign array
- **User Status**: No active campaigns available
- **External API Mock**: Returns empty data array

#### Test Validation
- **Created User ID**: 0 (no user created)
- **Permissions**: Based on actual user preferences (disabled)
- **Expected Behavior**: No enrollment occurs without active campaigns

### Test Suite 3: User Already in Challenge

#### Setup
- **Campaign Data**: Active campaign with user already enrolled
- **User Status**: Already participating in challenge
- **Users Array**: Contains test user ID in challenge data

#### Test Validation
- **Created User IDs**: Empty array (no new enrollment)
- **Permissions**: True (user has enabled permissions)
- **Expected Behavior**: No duplicate enrollment attempted

### Test Suite 4: Non-Onboarding Campaign

#### Setup
- **Campaign Weight**: "make_trips" instead of "onboard"
- **User Status**: User in campaign but not onboarding type
- **Gen Weight**: Different campaign targeting

#### Test Validation
- **Created User ID**: 0 (no enrollment for non-onboarding)
- **Permissions**: True (existing user permissions)
- **Expected Behavior**: Onboarding-specific campaigns only

## Integration Test Scenarios

### Welcome Coin Integration Test

#### Test Setup
```javascript
const auth = {
  userid: 1003,
  Authorization: 'Bearer {token}',
  'Content-Type': 'application/json',
  zone: 'America/Chicago'
};
```

#### Models Integration
- **AuthUsers**: User account management
- **WelcomeCoinHistory**: Coin distribution tracking
- **PointsTransaction**: Points and coin transactions

#### Test Flow
1. **Authentication**: Generate JWT token for test user
2. **Device Registration**: Set unique device ID for user
3. **Challenge Enrollment**: Mock successful campaign enrollment
4. **Welcome Coin Request**: Call getWelcomeCoin endpoint
5. **Validation**: Verify 3.5 coin reward distribution

#### Expected Behavior
```javascript
{
  "result": "success",
  "data": {
    "coin": 3.5
  }
}
```

## External Service Mocking

### Campaign API Mock
```javascript
sinon.stub(superagent, 'get').returns(Promise.resolve({
  body: {
    result: "success",
    data: [/* campaign data */]
  }
}));
```

### Enrollment API Mock
```javascript
sinon.stub(superagent, 'post').returns({
  send: async () => {
    return Promise.resolve({
      body: {
        result: "success",
        data: {
          bingocard_id: 1,
          created_user_ids: [1003]
        }
      }
    });
  }
});
```

## Database Operations

### User Preferences Setup
```javascript
await knex('auth_user')
  .where({ id: userId })
  .update({ 
    per_calendar: 1, 
    per_push_notification: 1 
  });
```

### Test Data Cleanup
```javascript
// Remove notification queue entries
await knex('incentive_notify_queue')
  .where({ user_id: userId })
  .del();

// Remove welcome coin history
await WelcomeCoinHistory.query()
  .where({ receiver_user_id: userId })
  .del();

// Remove points transactions
await PointsTransaction.query()
  .where({ 
    user_id: userId,
    activity_type: PointsTransaction.activityTypes.incentive,
    note: 'welcome coin'
  })
  .del();
```

## Service Integration Points

### Bingocard Service Methods
- **addToChallenge(userId)**: Main enrollment method
- **Campaign Validation**: Active campaign checking
- **User Permissions**: Calendar and notification preferences
- **Enrollment Logic**: Duplicate prevention and validation

### External Dependencies
- **Campaign Management Service**: Campaign data retrieval
- **Enrollment Service**: User challenge registration
- **Notification Service**: Permission management
- **Reward Service**: Welcome coin distribution

## Permission Management

### Permission Types
- **Calendar Permission**: Access to user calendar events
- **Push Notification Permission**: Send notifications to user
- **Permission Source**: Database user preferences

### Permission Validation
```javascript
expect(result.permissions.calendar).to.be.equal(user.per_calendar === 1);
expect(result.permissions.notification).to.be.equal(user.per_push_notification === 1);
```

## Campaign Logic

### Campaign Eligibility
- **Active Campaigns**: Within start and end time range
- **Onboarding Weight**: "onboard" type campaigns for new users
- **User Enrollment**: Check existing participation
- **Persona Matching**: Campaign target audience alignment

### Enrollment Rules
- **Single Enrollment**: Prevent duplicate registrations
- **Campaign Type**: Onboarding vs. ongoing campaigns
- **User Capacity**: Campaign participant limits
- **Time Windows**: Campaign active periods

## Error Handling

### External Service Failures
- **Campaign API**: Handle service unavailability
- **Enrollment API**: Handle registration failures
- **Database Errors**: Transaction rollback and cleanup

### Data Validation
- **User Existence**: Validate user ID
- **Campaign Data**: Validate campaign structure
- **Permission Data**: Validate user preferences

## Performance Considerations

### Mock Performance
- **Instant Responses**: Mocked external services
- **Database Operations**: Direct SQL for efficiency
- **Test Isolation**: Independent test execution

### Production Implications
- **External API Latency**: Real service response times
- **Database Load**: Campaign enrollment volume
- **Cache Strategy**: Campaign data caching

## Test Data Management

### Consistent Test State
- **User Permissions**: Predictable permission settings
- **Campaign Dates**: Dynamic date generation
- **Device IDs**: Unique device registration

### Cleanup Strategy
- **Between Tests**: Remove test-specific data
- **After Suites**: Restore database state
- **Mock Cleanup**: Restore original functions

## Security Considerations

### Authentication Testing
- **JWT Tokens**: Valid token generation
- **User Context**: Proper user identification
- **Authorization**: Permission-based access

### Data Protection
- **Test Data**: Non-production sensitive data
- **User Privacy**: Test user isolation
- **Campaign Data**: Secure campaign information

## Maintenance Notes

### Mock Maintenance
- **API Changes**: Update mocks with service changes
- **Data Structure**: Maintain campaign data format
- **Response Formats**: Keep response structures current

### Test Coverage
- **Edge Cases**: Additional scenario coverage
- **Error Conditions**: More failure testing
- **Integration Points**: Extended service testing

### Future Enhancements
- **Multiple Campaigns**: Test concurrent campaign handling
- **Campaign Types**: Test different campaign categories
- **User Segments**: Test persona-based enrollment
- **Reward Variations**: Test different reward types