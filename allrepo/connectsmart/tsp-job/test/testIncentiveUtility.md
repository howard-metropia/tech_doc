# Incentive Utility Service Test Suite

## Overview
Test suite for the incentive utility service that validates the functionality of timezone-based user filtering and internal user exclusion logic, ensuring proper user segmentation for incentive campaigns and notifications.

## File Location
`/test/testIncentiveUtility.js`

## Dependencies
- `@maas/core/mysql` - MySQL database connection for portal database
- `@app/src/services/incentiveUtility` - Incentive utility service functions
- `chai` - Assertion library with expect interface

## Test Architecture

### Service Function Under Test
```javascript
const utils = require('@app/src/services/incentiveUtility');
```
Focuses on testing the `getTimeZoneUsers()` method for user filtering and segmentation.

### Database Integration
- Uses real MySQL connection for testing
- Manages test data in `market_user` and `internal_user_tag` tables
- Implements comprehensive cleanup procedures

## Test Data Management

### Random Tag Generation
```javascript
const tag = `${Math.floor(Math.random() * Number.MAX_SAFE_INTEGER)}`;
```
- **Purpose**: Ensures unique tag identification for test isolation
- **Range**: Uses maximum safe integer for uniqueness
- **Cleanup**: Enables precise test data cleanup

### Test User Selection
```javascript
before(async () => {
  const rows = await knex('internal_user_tag')
    .groupBy('user_id')
    .select('user_id');
  const internals = rows.map((row) => row.user_id);
  
  user = await knex('market_user')
    .whereIn('user_in_market', ['HCS', 'general'])
    .whereNotIn('user_id', internals)
    .first();
    
  await knex('internal_user_tag').insert({ user_id: 1003, tag });
});
```

#### User Selection Logic
1. **Internal User Query**: Gets all users with internal tags
2. **Market User Filter**: Finds users in HCS or general markets
3. **Exclusion Filter**: Selects users NOT in internal user list
4. **Test Setup**: Creates internal tag for user 1003

## Core Functionality Testing

### Market User Inclusion Test
```javascript
it('user should be in market_user', async () => {
  const targets = await utils.getTimeZoneUsers(['HCS', 'general']);
  let found = false;
  for (const target of targets) {
    if (target.user_id === user.user_id) {
      found = true;
    }
  }
  expect(found).to.be.true;
});
```

#### Validation Logic
- **Market Filtering**: Verifies users in specified markets are included
- **Search Algorithm**: Iterates through results to find specific user
- **Assertion**: Confirms user presence in filtered results

### Internal User Exclusion Test
```javascript
it('should filtered by internal user list', async () => {
  await knex('internal_user_tag').insert({
    user_id: user.user_id,
    tag,
  });
  
  let found = false;
  const targets = await utils.getTimeZoneUsers(['HCS', 'general']);
  for (const target of targets) {
    if (target.user_id === user.user_id) {
      found = true;
    }
  }
  expect(found).to.be.false;
});
```

#### Exclusion Logic
1. **Tag Addition**: Adds user to internal_user_tag table
2. **Filter Application**: Calls getTimeZoneUsers with market filters
3. **Result Verification**: Confirms user is excluded from results
4. **Business Rule**: Internal users should not receive general incentives

## Database Schema Interactions

### Market User Table
- **user_id**: User identifier
- **user_in_market**: Market designation ('HCS', 'general', etc.)
- **Purpose**: Defines which users belong to which markets

### Internal User Tag Table
- **user_id**: User identifier
- **tag**: Classification tag for internal users
- **Purpose**: Flags internal users who should be excluded from campaigns

## Business Logic Validation

### Market Segmentation
```javascript
const targets = await utils.getTimeZoneUsers(['HCS', 'general']);
```
- **Market Arrays**: Accepts array of market identifiers
- **Inclusive Filter**: Users in ANY specified market are included
- **Geographic Segmentation**: Enables market-specific campaigns

### Internal User Filtering
- **Exclusion Rule**: Internal users are filtered out regardless of market
- **Tag-Based Logic**: Uses internal_user_tag table for identification
- **Priority**: Internal status overrides market membership

## Data Cleanup Strategy

### Test Isolation
```javascript
after(async () => {
  if (user) {
    await knex('internal_user_tag').where('user_id', user.user_id).del();
  }
  await knex('internal_user_tag').where({ user_id: 1003, tag }).del();
});
```

#### Cleanup Components
1. **Dynamic User Cleanup**: Removes tags for discovered test user
2. **Static User Cleanup**: Removes tags for hardcoded test user (1003)
3. **Tag-Specific Cleanup**: Uses unique tag for precise deletion
4. **Conditional Cleanup**: Only cleans if user was found

## Service Integration Points

### Incentive Campaign System
- **User Targeting**: Identifies eligible users for campaigns
- **Market Segmentation**: Enables market-specific incentive programs
- **Exclusion Logic**: Prevents internal users from receiving customer incentives

### Notification System
- **Recipient Lists**: Generates user lists for notifications
- **Filtering Rules**: Applies business rules for message targeting
- **Compliance**: Ensures internal users don't receive customer communications

## Performance Considerations

### Database Queries
- **Indexed Lookups**: Relies on proper indexing for user_id fields
- **Market Filtering**: Efficient WHERE IN operations
- **Exclusion Joins**: Optimized NOT IN subqueries

### Result Set Management
- **Large User Sets**: Handles potentially large market user populations
- **Memory Efficiency**: Processes results without loading entire tables
- **Pagination Support**: Could support pagination for large markets

## Error Handling

### Missing Data Scenarios
- **No Market Users**: Handles empty market_user results
- **No Internal Tags**: Functions correctly when internal_user_tag is empty
- **Invalid Markets**: Graceful handling of non-existent market codes

### Data Consistency
- **Referential Integrity**: Handles orphaned records appropriately
- **Concurrent Modifications**: Manages concurrent tag additions/removals
- **Transaction Boundaries**: Ensures consistent data state during tests

## Testing Patterns

### State-Based Testing
1. **Initial State**: User without internal tag
2. **State Change**: Add internal tag to user
3. **Result Verification**: Confirm filtering behavior change
4. **Cleanup**: Restore initial state

### Assertion Strategies
- **Boolean Flags**: Uses found/not found pattern for verification
- **Array Iteration**: Searches through result arrays for specific users
- **Expectation Validation**: Clear true/false assertions

## Quality Assurance

### Test Coverage Areas
1. **Market Inclusion**: Verifies users in target markets are included
2. **Internal Exclusion**: Confirms internal users are filtered out
3. **Data Integrity**: Ensures proper database operations
4. **Edge Cases**: Handles missing or invalid data

### Validation Approaches
- **Functional Testing**: Tests actual service behavior
- **Database Integration**: Validates real database operations
- **Business Logic**: Confirms filtering rules are applied correctly

## Maintenance Considerations

### Schema Evolution
- **New Markets**: Addition of new market types
- **Tag Structure**: Changes to internal user tagging system
- **Performance Optimization**: Query optimization requirements

### Business Rule Changes
- **Filtering Criteria**: Updates to user exclusion rules
- **Market Definitions**: Changes to market segmentation logic
- **Internal User Classification**: Modified internal user identification

## Security Implications

### Data Privacy
- **User Segmentation**: Ensures proper user data handling
- **Internal User Protection**: Prevents exposure of internal user data
- **Access Control**: Maintains appropriate data access boundaries

### Test Data Security
- **Cleanup Procedures**: Prevents test data from affecting production
- **Unique Identifiers**: Uses random tags to avoid conflicts
- **Isolation**: Maintains test independence

## Integration Testing Opportunities

### Full Campaign Pipeline
- **User Selection**: getTimeZoneUsers as first step
- **Campaign Targeting**: Integration with campaign management
- **Notification Delivery**: End-to-end testing with notification system

### Market Management
- **User Market Changes**: Testing market reassignment scenarios
- **Dynamic Filtering**: Real-time market-based filtering
- **Reporting Integration**: User counts by market for analytics

## Business Applications

### Incentive Campaigns
- **Geographic Targeting**: Market-specific incentive programs
- **User Segmentation**: Targeted campaigns for different user groups
- **Exclusion Management**: Prevent internal users from customer campaigns

### Communication Systems
- **Notification Targeting**: Send messages to specific markets
- **Survey Distribution**: Target surveys to appropriate user groups
- **Policy Updates**: Communicate changes to relevant user segments

## Monitoring and Analytics

### User Distribution Metrics
- **Market Sizes**: Track user counts by market
- **Internal User Ratios**: Monitor internal vs external user ratios
- **Filtering Effectiveness**: Measure accuracy of user segmentation

### Performance Metrics
- **Query Performance**: Monitor database query execution times
- **Result Set Sizes**: Track typical result set sizes for capacity planning
- **Error Rates**: Monitor filtering operation success rates