# Carpool Records Validation Test Suite

## Overview
Comprehensive test suite for the carpool record validation system that checks for data inconsistencies between trip trajectories and duo validation results, focusing on error detection and quality assurance in carpool matching algorithms.

## File Location
`/test/testCheckCarpoolRecords.js`

## Dependencies
- `chai` - Assertion library with expect interface
- `sinon` - Test stubbing and mocking framework
- `moment` - Date and time manipulation library
- `@maas/core/bootstrap` - Application initialization
- `@app/src/models/TripTrajectory` - MongoDB trip trajectory model
- `@app/src/models/DuoValidatedResult` - Duo carpool validation results model

## Test Architecture

### Service Functions Under Test
```javascript
const {
  getErrorRecords,
  getPeriod,
  calcErrorRatio,
} = require('../src/services/checkDuoCarpool');
```

### Test Categories
1. **Unit Testing**: Individual function validation
2. **Component Testing**: Service integration with mocked data
3. **Integration Testing**: Full job execution with real database

## Unit Testing: Core Functions

### Period Calculation Testing
```javascript
describe('getPeriod testing', () => {
  it('returns an array with two elements', () => {
    const period = getPeriod();
    expect(period).to.have.length(2);
  });
  
  it('returns two ISO-formatted strings', () => {
    const period = getPeriod();
    const start = moment.utc(period[0]).format('YYYY-MM-DDTHH:mm:ssZ');
    const end = moment.utc(period[1]).format('YYYY-MM-DDTHH:mm:ssZ');
    
    expect(start).to.match(/^\d{4}-\d{2}-\d{2}T22:00:00\+00:00$/);
    expect(end).to.match(/^\d{4}-\d{2}-\d{2}T21:59:59\+00:00$/);
  });
});
```

#### Period Logic
- **Start Time**: Previous day 22:00:00 UTC (daily cycle start)
- **End Time**: Current day 21:59:59 UTC (daily cycle end)
- **Format**: ISO 8601 with timezone information
- **Purpose**: Defines 24-hour validation window for carpool records

### Error Ratio Calculation Testing
```javascript
describe('calculate error ratio testing', () => {
  it('should be 0', () => {
    const actual = calcErrorRatio(0, 0);
    expect(actual).to.equal(0);
  });
  
  it('should be 0.3333', () => {
    const actual = calcErrorRatio(5, 15);
    expect(actual).to.equal(0.3333);
  });
  
  it('should be 1', () => {
    const actual = calcErrorRatio(10, 10);
    expect(actual).to.equal(1);
  });
});
```

#### Ratio Calculation Logic
- **Formula**: `errorCount / totalCount` with 4 decimal precision
- **Edge Cases**: Returns 0 for zero denominators or numerators
- **Range**: Values between 0.0000 and 1.0000
- **Purpose**: Quality metrics for carpool validation accuracy

## Component Testing: Error Record Detection

### Mock Data Setup
```javascript
const mockDuoResults = (datetime) => {
  return [
    {
      score: 0,           // Error indicator (score = 0)
      driver_trip_id: 1,
      passenger_trip_id: 2,
      created_on: datetime,
    },
    {
      score: 50,          // Valid result (score > 0)
      driver_trip_id: 5,
      passenger_trip_id: 6,
      created_on: datetime,
    }
  ];
};
```

### Trajectory Stubbing Strategy
```javascript
const queryStubTrajectory = sinon.stub(TripTrajectory, 'find');
queryStubTrajectory
  .withArgs({ trip_id: { $in: [1, 2] } })
  .returns([
    { _id: 1, trip_id: 1 },
    { _id: 2, trip_id: 2 },
  ])
  .withArgs({ trip_id: { $in: [5, 6] } })
  .returns([]); // Missing trajectories indicate errors
```

### Error Detection Logic
```javascript
it('should return the expected result while given two abnormal duo records', async () => {
  const actual = await getErrorRecords(res);
  
  expect(actual).to.have.length(2);
  expect(actual).to.deep.equal([
    {
      recordId: 1,
      driverTripId: 1,
      passengerTripId: 2,
      createdOn: mockDataTime,
    },
    {
      recordId: 2,
      driverTripId: 3,
      passengerTripId: 4,
      createdOn: mockDataTime,
    },
  ]);
});
```

## Data Models

### Duo Validated Result Structure
```javascript
{
  id: 1,                    // Database primary key
  score: 0,                 // Validation score (0 = error)
  driver_trip_id: 1,        // Driver's trip identifier
  passenger_trip_id: 2,     // Passenger's trip identifier
  created_on: datetime      // Validation timestamp
}
```

### Trip Trajectory Structure
```javascript
{
  _id: 1,                   // MongoDB document ID
  trip_id: 1               // Trip identifier reference
}
```

### Error Record Output Structure
```javascript
{
  recordId: 1,              // Original duo result ID
  driverTripId: 1,          // Driver trip reference
  passengerTripId: 2,       // Passenger trip reference
  createdOn: datetime       // Error occurrence time
}
```

## Error Detection Criteria

### Score-Based Validation
- **Score = 0**: Indicates validation failure or error
- **Score > 0**: Indicates successful carpool validation
- **Threshold Logic**: Only zero scores are flagged as errors

### Trajectory Consistency Check
- **Missing Trajectories**: Trips without trajectory data are errors
- **Data Integrity**: Validates relationship between duo results and trip data
- **Cross-Reference**: Ensures both driver and passenger trips have trajectories

## Integration Testing: Full Job Execution

### Test Setup Strategy
```javascript
describe('integration testing', function () {
  this.timeout(20 * 1000); // 20-second timeout
  
  let mockDuo, mockTraj;
  const mockDuoIdList = [];
  
  before(async () => {
    const mockTime = moment.utc().subtract(4, 'hours').toISOString();
    mockDuo = mockDuoResults(mockTime);
    
    // Insert mock duo validation results
    await Promise.all(
      mockDuo.map(async (duo) => {
        const res = await DuoValidatedResult.query().insert(duo);
        mockDuoIdList.push(res.id);
      })
    );
    
    // Insert mock trajectory data
    mockTraj = mockTrajectories();
    await TripTrajectory.insertMany(mockTraj);
  });
});
```

### Mock Trajectory Data
```javascript
const mockTrajectories = () => {
  return [
    { _id: 1, trip_id: 1 },
    { _id: 2, trip_id: 2 },
    { _id: 3, trip_id: 3 },
    { _id: 4, trip_id: 4 },
  ];
};
```

### Cleanup Operations
```javascript
after(async () => {
  // Clean up duo validation results
  await DuoValidatedResult.query()
    .delete()
    .where('id', 'in', mockDuoIdList);
  
  // Clean up trajectory data
  const targetIds = mockTraj.map((traj) => traj._id);
  await TripTrajectory.deleteMany({ _id: { $in: targetIds } });
});
```

### Job Execution Test
```javascript
it('should process without any exception', async () => {
  try {
    await job.fn();
  } catch (err) {
    expect.fail('job.fn() should not throw an exception');
  }
});
```

## Business Logic

### Carpool Validation Pipeline
1. **Duo Creation**: Algorithm creates driver-passenger pairs
2. **Score Calculation**: Validates pair compatibility and quality
3. **Trajectory Verification**: Confirms trip execution data exists
4. **Error Flagging**: Identifies inconsistencies for investigation

### Quality Metrics
- **Error Ratio**: Percentage of failed validations
- **Data Completeness**: Trajectory coverage for validated pairs
- **Temporal Analysis**: Error patterns over time periods

### Data Integrity Checks
- **Cross-Reference Validation**: Duo results must have corresponding trajectories
- **Score Consistency**: Zero scores indicate algorithm failures
- **Temporal Alignment**: Created timestamps must align with trip times

## Performance Considerations

### Database Optimization
- **Batch Operations**: Uses Promise.all for parallel inserts
- **Targeted Queries**: Specific trip ID queries with $in operator
- **Index Usage**: Relies on proper indexing for trip_id fields

### Mock Data Efficiency
- **Minimal Data Sets**: Small but representative test data
- **Focused Testing**: Targets specific error conditions
- **Fast Execution**: Quick setup and teardown procedures

## Error Scenarios

### Data Inconsistency Types
1. **Missing Trajectories**: Duo results without trajectory data
2. **Zero Scores**: Algorithm validation failures
3. **Orphaned Records**: Trajectories without duo validation
4. **Timing Misalignment**: Temporal inconsistencies between records

### Error Reporting Format
```javascript
{
  recordId: 1,              // For traceability
  driverTripId: 1,          // Driver investigation
  passengerTripId: 2,       // Passenger investigation
  createdOn: datetime       // Temporal analysis
}
```

## Quality Assurance

### Test Coverage Areas
1. **Period Calculation**: Time window determination
2. **Error Ratio Math**: Statistical calculation accuracy
3. **Error Detection**: Comprehensive error identification
4. **Data Cleanup**: Proper test isolation

### Validation Strategies
- **Deep Equality**: Exact object structure validation
- **Length Checks**: Result count verification
- **Exception Handling**: Error condition testing
- **Regex Matching**: Time format validation

## Maintenance Considerations

### Data Model Evolution
- **Schema Changes**: May require test data updates
- **New Error Types**: Additional validation criteria
- **Performance Tuning**: Query optimization requirements

### Integration Dependencies
- **InfluxDB Integration**: Commented out for testing flexibility
- **Real-time Processing**: Job scheduling considerations
- **Alert Systems**: Error notification integration

## Monitoring and Alerting

### Error Detection Workflow
1. **Daily Execution**: Checks previous 24-hour period
2. **Error Identification**: Flags problematic records
3. **Metric Calculation**: Computes quality ratios
4. **Alert Generation**: Notifies operations team of issues

### Quality Metrics
- **Error Count**: Total problematic records found
- **Error Ratio**: Percentage of total validations that failed
- **Trend Analysis**: Pattern recognition over time
- **Impact Assessment**: Business impact of validation failures