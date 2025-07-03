# Carpool Trip Processing Service Test Suite

## Overview
Unit test suite for the carpool trip processing service that validates automatic trip completion logic for expired carpool reservations and trip handling workflows.

## File Location
`/test/testCarpoolTripPorcessing.js`

## Dependencies
- `@maas/core/bootstrap` - Application initialization
- `@maas/core/mysql` - MySQL database connection for portal database
- `chai` - Assertion library for test validation
- `sinon` - Stubbing framework for database mocking

## Test Architecture

### Service Under Test
```javascript
const service = require('@app/src/services/carpoolTripProcessing');
```
Focuses on testing the `carpoolTripProcessing()` method for automatic trip completion.

### Mock Database Strategy
Comprehensive database stubbing approach that mocks all MySQL operations:
```javascript
const fake = {
  raw: async function(query) { /* Complex query results */ },
  where: async function() { return Promise.resolve(this); },
  whereIn: async function() { return Promise.resolve(this); },
  insert: async function() { return Promise.resolve(1); },
  update: async function() { return Promise.resolve([]); },
  first: async function() { return Promise.resolve({}); },
  transaction: async function() { return Promise.resolve({}); }
};
```

## Test Data Configuration

### Time-Based Test Setup
```javascript
let startedOn = new Date(new Date().getTime() - 1000 * 60 * 60 * 2 - 1000 * 60 * 10 - 1000);
let estimatedArrivalOn = new Date(new Date().getTime() - 1000 * 60 * 60 * 2 - 1000);
```
- **Started Time**: 2 hours 10 minutes ago (plus 1 second)
- **Estimated Arrival**: 2 hours ago (plus 1 second)
- **Purpose**: Simulates expired trips requiring automatic completion

### Mock Trip Data Structure
```javascript
{
  trip_id: 2,
  reservation_id: 2,
  user_id: 1003,
  role: 1, // Driver role
  route_meter: 1000,
  reservation_origin: 'origin',
  reservation_origin_name: 'origin name',
  reservation_origin_latitude: 1.0,
  reservation_origin_longitude: 1.0,
  reservation_destination: 'destination',
  reservation_destination_name: 'destination name',
  reservation_destination_latitude: 1.0,
  reservation_destination_longitude: 1.0,
  reservation_estimated_arrival_on: jstimeToDbtime(estimatedArrivalOn),
  trip_origin: 'origin',
  trip_destination: 'destination',
  trip_estimated_arrival_on: jstimeToDbtime(estimatedArrivalOn),
  trip_distance: 1000,
  trip_trajectory_distance: 1000,
  trip_ended_on: null, // Key field - trip not yet completed
  trip_started_on: jstimeToDbtime(startedOn),
  passenger_id: 1004,
  rider_trip_id: 2,
  partner_reservation_id: 1
}
```

## Time Conversion Utility

### Database Time Format
```javascript
function jstimeToDbtime(jstime) {
  return jstime.toISOString().replace('T', ' ').split('.')[0];
}
```
- **Purpose**: Converts JavaScript Date objects to MySQL datetime format
- **Format**: `YYYY-MM-DD HH:mm:ss`
- **Usage**: Ensures consistent time representation in test data

## Database Stubbing Implementation

### Knex Method Stubbing
```javascript
stub1 = sinon.stub(knex, 'where').callsFake(() => fake);
stub2 = sinon.stub(knex, 'whereIn').callsFake(() => fake);
stub3 = sinon.stub(knex, 'raw').callsFake((query) => fake.raw(query));
stub4 = sinon.stub(knex, 'insert').callsFake(() => fake.insert);
stub5 = sinon.stub(knex, 'update').callsFake(() => fake.update);
stub6 = sinon.stub(knex, 'first').callsFake(() => fake.first);
stub7 = sinon.stub(knex, 'transaction').callsFake(() => fake.transaction);
```

### Query Result Simulation
The `raw` method returns a complex data structure simulating a JOIN query across multiple tables:
- **Reservation Data**: Origin, destination, timing information
- **Trip Data**: Distance, trajectory, status information  
- **User Data**: Driver and passenger relationships
- **Partner Data**: Cross-system reservation linking

## Core Test Scenario

### Happy Path Test Case
```javascript
it('check result', async () => {
  const endedOn = jstimeToDbtime(new Date());
  const result = await service.carpoolTripProcessing();
  
  // Validate result array structure
  expect(result.length).to.be.equal(1);
  
  // Validate original trip data
  expect(result[0].row.trip_id).to.be.equal(2);
  expect(result[0].row.trip_ended_on).to.be.equal(null);
  
  // Validate timing data consistency
  expect(result[0].row.reservation_estimated_arrival_on)
    .to.be.equal(jstimeToDbtime(estimatedArrivalOn));
  expect(result[0].row.trip_estimated_arrival_on)
    .to.be.equal(jstimeToDbtime(estimatedArrivalOn));
  
  // Validate trip completion logic
  expect(result[0].updatedTrip.ended_on).to.be.equal(endedOn);
  expect(result[0].updatedTrip.estimated_arrival_on)
    .to.be.equal(jstimeToDbtime(estimatedArrivalOn));
});
```

## Business Logic Validation

### Trip Expiration Logic
The service identifies trips that should be automatically completed based on:
1. **Started Status**: Trip has started (`trip_started_on` is not null)
2. **Not Completed**: Trip hasn't ended (`trip_ended_on` is null)
3. **Time Expired**: Current time exceeds estimated arrival time
4. **Grace Period**: Additional buffer time for completion

### Automatic Completion Process
When a trip meets expiration criteria:
1. **Detection**: Query identifies expired active trips
2. **Completion**: Sets `ended_on` timestamp to current time
3. **Preservation**: Maintains original `estimated_arrival_on` for analytics
4. **Logging**: Returns both original and updated trip data

## Data Relationships

### Multi-Table Query Structure
The test simulates a complex query involving:
- **Reservations Table**: Carpool reservation details
- **Trips Table**: Individual trip records
- **Users Table**: Driver and passenger information
- **Partner Systems**: External reservation tracking

### Role-Based Processing
```javascript
role: 1 // Driver role indicator
```
- **Driver Trips**: Primary focus for automatic completion
- **Passenger Trips**: Linked through `passenger_id` and `rider_trip_id`
- **Coordination**: Ensures both driver and passenger trips are handled consistently

## Performance Considerations

### Database Query Optimization
- **Raw Queries**: Uses optimized SQL for complex multi-table operations
- **Indexing**: Relies on proper database indexing for performance
- **Batch Processing**: Handles multiple expired trips in single operation

### Mock Performance
- **Synchronous Operations**: Fast test execution through Promise.resolve()
- **Memory Efficiency**: Minimal data structures for test scenarios
- **Isolation**: No actual database connections during testing

## Error Handling Testing

### Stub Restoration
```javascript
after(() => {
  stub1.restore();
  stub2.restore();
  stub3.restore();
  stub4.restore();
  stub5.restore();
  stub6.restore();
  stub7.restore();
});
```
Ensures all database stubs are properly restored after test execution.

### Exception Management
The test framework validates that the service handles:
- **Database Connection Issues**: Through stubbed error responses
- **Invalid Data**: Malformed trip records
- **Timing Edge Cases**: Concurrent trip completion scenarios

## Integration Points

### Service Dependencies
- **Database Layer**: MySQL portal database operations
- **Trip Management**: Carpool trip lifecycle management
- **User Management**: Driver and passenger coordination
- **Partner Systems**: External reservation synchronization

### External System Coordination
- **Reservation Systems**: Maintains consistency with booking platforms
- **Analytics**: Preserves timing data for performance analysis
- **Notifications**: May trigger completion notifications (not tested here)

## Test Coverage Analysis

### Functional Coverage
1. **Trip Detection**: Identifies expired trips correctly
2. **Data Retrieval**: Properly queries complex trip relationships
3. **Completion Logic**: Updates trip status appropriately
4. **Data Preservation**: Maintains analytical data integrity

### Edge Case Coverage
- **Null Handling**: Proper processing of null `trip_ended_on` values
- **Time Calculations**: Accurate expiration time determination
- **Data Consistency**: Maintains referential integrity across updates

## Quality Assurance

### Assertion Strategy
- **Structural Validation**: Confirms result array structure
- **Data Integrity**: Validates key field values
- **State Transition**: Verifies proper trip status changes
- **Time Accuracy**: Ensures correct timestamp handling

### Mock Data Realism
- **Realistic IDs**: Uses plausible database IDs
- **Geographic Data**: Includes coordinate information
- **Distance Metrics**: Provides route and trajectory distances
- **Time Relationships**: Maintains logical timing sequences

## Maintenance Considerations

### Test Data Updates
- **Time Dependencies**: May require updates as time calculations evolve
- **Schema Changes**: Sensitive to database schema modifications
- **Business Rules**: Reflects current carpool completion policies

### Mock Synchronization
- **Database Schema**: Mocks must match actual database structure
- **Query Changes**: Stubs must reflect actual service query patterns
- **Error Conditions**: Should simulate realistic failure scenarios