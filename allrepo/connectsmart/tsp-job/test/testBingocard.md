# Bingocard Service Test Suite

## Overview
Comprehensive test suite for the bingocard service that validates the functionality of adding users to challenges based on incentive notifications and campaign eligibility criteria.

## File Location
`/test/testBingocard.js`

## Dependencies
- `@maas/core/bootstrap` - Application bootstrap
- `@maas/core/mysql` - MySQL database connection
- `sinon` - Test stubbing and mocking framework
- `chai` - Assertion library with expect interface
- `superagent` - HTTP client for API stubbing

## Test Architecture

### Core Service Under Test
```javascript
const bingocard = require('@app/src/services/bingocard');
```
Tests focus on the `addToChallenge()` and `addToChallengePD()` methods.

### Mock Data Configuration
```javascript
const userId = 1003;
const bingocardId = 1;
const campaignId = 1;
```

### Database Integration
- Uses real MySQL connection via `@maas/core/mysql`
- Manages `incentive_notify_queue` table for test data
- Performs cleanup operations in `before` and `after` hooks

## Test Categories

### 1. Campaign Data Available - User Not Joined
Tests the successful addition of users to challenges when:
- Valid campaign data exists
- User meets eligibility criteria
- User hasn't previously joined the challenge

#### Happy Path Test
```javascript
it('should add to challenge', async () => {
  const data = {
    user_id: userId,
    deliver_time: new Date(),
    deliver: 0,
    purpose: 'incentive',
    market: 'HCS',
    incentive_type: 'incentive open app',
    msg_content: 'test message',
  };
  const result = await bingocard.addToChallenge(notifyUsers);
  expect(result[0]).to.have.property('bingocard_id', bingocardId);
  expect(result[0].created_user_ids[0]).to.be.equal(userId);
});
```

#### Edge Cases
- **Empty notification array**: Returns empty result
- **Wrong market filter**: Only processes 'HCS' market users
- **Invalid incentive type**: Only processes 'incentive open app' type

### 2. No Current Campaign Data
Tests behavior when no active campaigns are available:
```javascript
sinon.stub(superagent, 'get').returns(Promise.resolve({
  body: { result: "success", data: [] }
}));
```
Expected result: Empty array returned.

### 3. User Already in Challenge
Tests prevention of duplicate challenge enrollments:
```javascript
users: [userId] // User already enrolled
```
Expected result: Empty array to prevent duplicate enrollment.

### 4. Post-Completion (PD) Challenge Logic
Complex test scenarios for users who have completed previous challenges:

#### Completed Challenge Scenario
```javascript
users: [{ 
  user_id: userId,
  status: 1, // Completed
  end_time: end_time,
  completed_on: completedOn 
}]
```
- Tests user eligibility for new challenges after completion
- Validates automatic enrollment in alternative challenges

#### Expired Challenge Scenario
```javascript
end_time: end_before // Past expiration
```
- Tests handling of expired but incomplete challenges
- Validates user re-enrollment eligibility

## Mock Implementation

### Campaign Data Structure
```javascript
{
  id: campaignId,
  title: "Explorer Challenge",
  description: "Complete this Challenge and earn rewards...",
  reward_type: 1,
  reward_amount: 3,
  image_url: "https://s3-us-east-2.amazonaws.com/smart-maas-develop/...",
  start_time: "2023-01-01 00:00:00",
  end_time: "2023-01-31 00:00:00",
  bingocard_id: bingocardId,
  persona: "biking,carpool,driving,transit",
  gen_weight: "onboard",
  available_activity: [1, 2, 3, ...32],
  width: 3,
  height: 3,
  users: []
}
```

### API Stubbing Strategy
```javascript
sinon.stub(superagent, 'get').returns(Promise.resolve(campaignResponse));
sinon.stub(superagent, 'post').returns({
  send: async () => Promise.resolve(enrollmentResponse)
});
```

## Business Logic Validation

### Market Filtering
- **HCS Market**: Houston ConnectSmart market users only
- **General Market**: Excluded from challenge eligibility
- **Validation**: Ensures geographic service area compliance

### Incentive Type Filtering
- **"incentive open app"**: Primary trigger for challenge enrollment
- **Alternative types**: Excluded to prevent inappropriate enrollments
- **Purpose**: Maintains challenge enrollment quality

### Status Management
- **Status 0**: Active/incomplete challenge
- **Status 1**: Completed challenge
- **Timing Logic**: Based on completion timestamps and expiration dates

## Data Flow Testing

### Input Validation
```javascript
const notifyUsers = [{
  user_id: userId,
  market: 'HCS',
  incentive_type: 'incentive open app',
  purpose: 'incentive'
}];
```

### Expected Outputs
```javascript
[{
  bingocard_id: bingocardId,
  created_user_ids: [userId]
}]
```

## Database Operations

### Test Data Setup
```javascript
await knex('incentive_notify_queue').insert(data);
```

### Cleanup Operations
```javascript
await knex('incentive_notify_queue').where({ user_id: userId }).del();
```

## Error Scenarios

### API Stub Restoration
```javascript
after(async () => {
  superagent.get.restore();
  superagent.post.restore();
});
```

### Race Condition Handling
Tests validate proper handling of concurrent user enrollments and campaign state changes.

## Integration Points

### External API Dependencies
- **Campaign Management API**: Retrieves active campaigns
- **Enrollment API**: Processes user challenge enrollments
- **Notification System**: Manages user communication

### Database Dependencies
- **incentive_notify_queue**: User notification tracking
- **Campaign Data**: Challenge configuration and rules
- **User Enrollment**: Challenge participation tracking

## Performance Considerations

### Stub Performance
- Uses synchronous Promise resolution for fast test execution
- Minimizes actual HTTP requests during testing
- Maintains test isolation through proper cleanup

### Database Efficiency
- Targeted record insertion and deletion
- Uses specific user IDs to avoid test interference
- Implements proper transaction boundaries

## Quality Assurance

### Test Coverage Areas
1. **Happy Path Scenarios**: Successful challenge enrollment
2. **Edge Cases**: Empty data, invalid filters
3. **Business Logic**: Market and incentive type validation
4. **State Management**: User enrollment status tracking
5. **Error Handling**: Missing data and invalid states

### Assertion Strategies
- **Type Validation**: Ensures correct data structures
- **Property Verification**: Validates expected object properties
- **Value Matching**: Confirms exact expected values
- **Array Validation**: Checks collection contents and length

## Maintenance Notes

### Test Data Management
- Uses consistent test user IDs across scenarios
- Implements comprehensive cleanup procedures
- Maintains database state isolation between tests

### Mock Configuration
- Centralizes stub configuration for maintainability
- Uses realistic mock data reflecting production scenarios
- Implements proper restoration procedures