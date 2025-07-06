# Local User Label Service Test Suite

## Overview
Comprehensive test suite for the local user label service that validates user classification logic for local vs. non-local users based on service area boundaries, enabling targeted campaigns and service offerings for geographic user segments.

## File Location
`/test/testLocalUserLabel.js`

## Dependencies
- `@maas/core/bootstrap` - Application initialization
- `chai` - Assertion library with expect interface
- `sinon` - Test stubbing and mocking framework
- `@app/src/models/AuthUserLabel` - User label database model
- `@maas/core/log` - Logging framework
- `@turf/turf` - Geospatial analysis toolkit
- `@app/src/services/localUserLabel` - Local user label service

## Test Architecture

### Service Functions Under Test
```javascript
const service = require('@app/src/services/localUserLabel');
```

### Core Functions Tested
- `switchToLocalUser(userId)` - Converts user to local status
- `setNonLocalUser(userId)` - Sets user as non-local
- `checkServiceArea(lat, lng)` - Validates coordinates within service area

### Test Categories
1. **Unit Testing**: Individual function logic with mocks
2. **Integration Testing**: Real service area validation

## Database Management

### Test Data Cleanup
```javascript
beforeEach(async () => {
  await AuthUserLabel.query()
    .where('user_id', 1)
    .whereIn('label_id', [2, 3])
    .delete(); // Clear the database before each test
});
```

### Stub Restoration
```javascript
afterEach(() => {
  sinon.restore();
});
```

## Unit Testing: User Classification

### Switch to Local User Testing

#### Successful Conversion
```javascript
it('should add local user label and remove non-local user label if conditions are met', async () => {
  const userId = 1;
  sinon.stub(AuthUserLabel, 'query').returns({
    findOne: sinon.stub()
      .onFirstCall().resolves(null) // No local user label
      .onSecondCall().resolves({}), // Has non-local user label
    insert: sinon.stub().resolves(),
    delete: () => ({ where: sinon.stub().resolves() }),
  });

  const result = await service.switchToLocalUser(userId);
  expect(result).to.be.true;
});
```

#### Already Local User
```javascript
it('should log and return false if user already has local user label', async () => {
  const userId = 1;
  const loggerSpy = sinon.spy(logger, 'info');
  sinon.stub(AuthUserLabel, 'query').returns({
    findOne: sinon.stub()
      .onFirstCall().resolves({}) // Has local user label
      .onSecondCall().resolves(null), // No non-local user label
  });

  const result = await service.switchToLocalUser(userId);
  expect(result).to.be.false;
  expect(loggerSpy.calledWith(`[switchToLocalUser] User ${userId} already in local user label`)).to.be.true;
});
```

#### Not in Non-Local Status
```javascript
it('should log and return false if user is not in non-local user label', async () => {
  const userId = 1;
  const loggerSpy = sinon.spy(logger, 'info');
  sinon.stub(AuthUserLabel, 'query').returns({
    findOne: sinon.stub()
      .onFirstCall().resolves(null) // No local user label
      .onSecondCall().resolves(null), // No non-local user label
    insert: sinon.stub().resolves(),
  });

  const result = await service.switchToLocalUser(userId);
  expect(result).to.be.false;
  expect(loggerSpy.calledWith(`[switchToLocalUser] User ${userId} not in non local user label`)).to.be.true;
});
```

### Set Non-Local User Testing

#### Successful Non-Local Assignment
```javascript
it('should add non-local user label if conditions are met', async () => {
  const userId = 1;
  sinon.stub(AuthUserLabel, 'query').returns({
    findOne: sinon.stub()
      .onFirstCall().resolves(null) // No local user label
      .onSecondCall().resolves(null), // No non-local user label
    insert: sinon.stub().resolves(),
  });

  const result = await service.setNonLocalUser(userId);
  expect(result).to.be.true;
});
```

#### Already Non-Local User
```javascript
it('should log and return false if user already has non-local user label', async () => {
  const userId = 1;
  const loggerSpy = sinon.spy(logger, 'info');
  sinon.stub(AuthUserLabel, 'query').returns({
    findOne: sinon.stub()
      .onFirstCall().resolves(null) // No local user label
      .onSecondCall().resolves({}), // Has non-local user label
  });

  const result = await service.setNonLocalUser(userId);
  expect(result).to.be.false;
  expect(loggerSpy.calledWith(`[setNonLocalUser] User ${userId} already in non local user label`)).to.be.true;
});
```

#### Has Local User Label
```javascript
it('should return false if user has local user label', async () => {
  const userId = 1;
  sinon.stub(AuthUserLabel, 'query').returns({
    findOne: sinon.stub()
      .onFirstCall().resolves({}) // Has local user label
      .onSecondCall().resolves(null), // No non-local user label
  });

  const result = await service.setNonLocalUser(userId);
  expect(result).to.be.false;
});
```

## Database Model Stubbing

### AuthUserLabel Query Mocking
```javascript
sinon.stub(AuthUserLabel, 'query').returns({
  findOne: sinon.stub()
    .onFirstCall().resolves(null)  // Local user label query
    .onSecondCall().resolves({}),  // Non-local user label query
  insert: sinon.stub().resolves(),
  delete: () => ({ where: sinon.stub().resolves() }),
});
```

### Query Chain Mocking
- **findOne**: Mocks label existence checks
- **insert**: Mocks label creation operations
- **delete**: Mocks label removal operations
- **where**: Mocks query filtering

## Business Logic Rules

### Local User Conversion Rules
1. **Prerequisite**: User must have non-local label
2. **Action**: Remove non-local label and add local label
3. **Exclusion**: Cannot convert if already local
4. **Validation**: Must not be in local status already

### Non-Local User Assignment Rules
1. **Prerequisite**: User must not have local label
2. **Action**: Add non-local label
3. **Exclusion**: Cannot assign if already non-local
4. **Priority**: Local status takes precedence

### Label Precedence
- **Local Label**: Higher priority status
- **Non-Local Label**: Default external user status
- **Mutual Exclusion**: User cannot have both labels simultaneously

## Integration Testing: Service Area Validation

### Outside Service Area Test
```javascript
it('checkServiceArea run outside of NoVA should fail', () => {
  const lat = 10;
  const lng = 20;
  const result = service.checkServiceArea(lat, lng);
  expect(result).to.be.false;
});
```

### Inside Service Area Test
```javascript
it('checkServiceArea run inside of NoVA should pass', () => {
  const lat = 29.76328;   // Houston coordinates
  const lng = -95.36327;
  const result = service.checkServiceArea(lat, lng);
  expect(result).to.be.true;
});
```

## Geographic Service Area

### Test Coordinates
- **Outside Area**: (10, 20) - Generic coordinates outside service area
- **Inside Area**: (29.76328, -95.36327) - Houston, Texas coordinates

### Service Area Definition
- **Primary Area**: Houston metropolitan area (based on coordinates)
- **Boundary Logic**: Uses geospatial polygon intersection
- **Geographic Precision**: Coordinate-based boundary validation

## Label ID Configuration

### Label Identifiers
```javascript
.whereIn('label_id', [2, 3])
```
- **Label ID 2**: Likely local user label identifier
- **Label ID 3**: Likely non-local user label identifier
- **Database Schema**: Predefined label classification system

## Logging Integration

### Log Message Validation
```javascript
const loggerSpy = sinon.spy(logger, 'info');
expect(loggerSpy.calledWith(`[switchToLocalUser] User ${userId} already in local user label`)).to.be.true;
```

### Log Message Patterns
- **Function Context**: Includes function name in log messages
- **User Context**: Includes user ID for traceability
- **Status Information**: Describes current user label status
- **Action Results**: Logs outcome of label operations

## Error Handling Scenarios

### Database Operation Failures
- **Insert Failures**: Handle label creation errors
- **Delete Failures**: Manage label removal errors
- **Query Failures**: Handle label lookup errors
- **Transaction Consistency**: Maintain data integrity

### Business Logic Violations
- **Invalid State Transitions**: Prevent illegal label changes
- **Concurrent Modifications**: Handle race conditions
- **Data Inconsistency**: Detect and resolve inconsistent states

## Performance Considerations

### Database Efficiency
- **Indexed Queries**: User ID and label ID indexing
- **Minimal Operations**: Efficient label existence checks
- **Transaction Scope**: Atomic label update operations

### Geospatial Performance
- **Coordinate Validation**: Fast point-in-polygon checks
- **Caching Opportunities**: Service area boundary caching
- **Spatial Indexing**: Geographic lookup optimization

## Service Integration Points

### User Management System
- **User Classification**: Enables user segmentation
- **Service Eligibility**: Determines service availability
- **Campaign Targeting**: Supports targeted user campaigns

### Geographic Services
- **Location Validation**: Validates user location data
- **Service Area Management**: Manages service boundaries
- **Compliance**: Ensures service area compliance

## Quality Assurance

### Test Coverage Areas
1. **State Transitions**: All valid label state changes
2. **Business Rules**: Label assignment and removal rules
3. **Error Conditions**: Invalid operations and edge cases
4. **Geographic Validation**: Service area boundary testing

### Assertion Strategies
- **Boolean Results**: Success/failure validation
- **Log Verification**: Proper logging behavior
- **State Validation**: Database state consistency
- **Geographic Testing**: Coordinate boundary validation

## Maintenance Considerations

### Label System Evolution
- **New Labels**: Additional user classification types
- **Rule Changes**: Updated business logic for label assignment
- **Performance Optimization**: Query and geospatial improvements

### Service Area Updates
- **Boundary Changes**: Geographic service area modifications
- **Coordinate Systems**: Coordinate system updates
- **Accuracy Improvements**: Enhanced boundary precision

## Security Considerations

### User Data Privacy
- **Label Information**: Sensitive user classification data
- **Location Data**: Geographic information privacy
- **Access Control**: Restricted label modification permissions

### Data Integrity
- **Label Consistency**: Prevents conflicting user labels
- **Audit Trail**: Tracks label change history
- **Validation**: Ensures only valid label transitions

## Business Applications

### User Segmentation
- **Local Users**: Residents within service area
- **Non-Local Users**: Visitors or users outside primary service area
- **Service Differentiation**: Different services for different user types

### Campaign Management
- **Targeted Promotions**: Location-based campaign targeting
- **Service Announcements**: Area-specific notifications
- **Feature Access**: Geography-based feature availability

## Monitoring and Analytics

### Label Distribution Metrics
- **Local vs Non-Local**: Ratio of user types
- **Geographic Distribution**: User distribution across service areas
- **Label Changes**: Frequency of status transitions

### Service Area Analytics
- **Boundary Crossings**: Users entering/leaving service areas
- **Usage Patterns**: Service usage by geographic segments
- **Growth Metrics**: Service area expansion analytics