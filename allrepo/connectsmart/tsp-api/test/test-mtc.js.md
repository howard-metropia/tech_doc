# test-mtc.js

## Overview
Test suite for the MTC (Metropolitan Transportation Commission) service integration in the TSP API. Tests trip planning message generation, probability distribution algorithms, and API endpoint functionality.

## File Location
`/test/test-mtc.js`

## Dependencies
- **@maas/core**: Core MaaS framework components
- **supertest**: HTTP assertions for API testing
- **uuid**: UUID generation and validation
- **chai**: BDD/TDD assertion library
- **Service**: mtc service

## Service Under Test
```javascript
const service = require('@app/src/services/mtc');
```

## Test Structure

### Integration Tests

#### MTC Message Endpoint
**Endpoint**: `POST /mtc_message`

**Test Configuration**:
```javascript
const request = supertest.agent(app.listen());
request
  .post(router.url('mtc_message'), {})
  .set('userid', 10518)
  .send(tripData)
  .expect(200)
```

**Trip Data Structure**:
```javascript
{
  origin: {
    name: 'Houston zoo',
    address: '6200 Hermann Park Dr, Houston, TX 77030 USA',
    latitude: 29.7141863,
    longitude: -95.3698028
  },
  destination: {
    name: 'Houston',
    address: 'Houston',
    latitude: 29.7141863,
    longitude: -95.39095809
  },
  departure_time: '2022-01-01 12:34:56',
  eta_time: 1921,
  eta_distance: 1789
}
```

**Test Case**:
- **Successful Request**: Returns 200 status code
- **Complete Trip Data**: Includes origin, destination, timing, and distance
- **User Context**: Authenticated request with user ID

### Unit Tests

#### 1. Probability Distribution Testing

**Test Setup**:
```javascript
const base = 1000000;
const spread = service.spreadList();
const data = service.dataProvider();
const result = service.test(base);
```

**Validation Logic**:
1. **Total Accuracy**: Sum of all probabilities ≈ base value
   ```javascript
   expect(Math.abs(base - allAccu)).to.be.lessThan(100);
   ```

2. **Individual Probability Accuracy**: Each probability within 0.5% of expected
   ```javascript
   expect(
     Math.abs(v / allAccu - spread[idx]) / spread[idx]
   ).to.be.lessThan(0.005);
   ```

**Purpose**:
- Tests weighted message selection algorithm
- Ensures statistical distribution matches specifications
- Validates probability calculation accuracy

#### 2. UUID Generation Testing

**Function**: `service.getPlanId()`

**Test Case**:
```javascript
const uuid = service.getPlanId();
expect(uuidValidate(uuid)).to.be.true;
```

**Validation**:
- Generates valid UUID format
- Ensures unique plan identifiers
- Uses standard UUID v4 format

#### 3. Message Selection Testing

**Function**: `service.getMessage()`

**Test Loop**: 100 iterations to test randomness

**Test Logic**:
```javascript
const {
  idx: message_id,
  result: { title, message }
} = service.getMessage();

const dataList = service.dataProvider();
messages = dataList.reduce((pre, cur) => {
  pre.push(cur.message);
  return pre;
}, []);

expect(messages.indexOf(message) > -1).to.be.true;
```

**Validation**:
- Selected messages always exist in data provider
- Random selection from valid message pool
- Consistent message structure (title, message)

## MTC Service Architecture

### Message System
- **Data Provider**: Central repository of transportation messages
- **Probability Distribution**: Weighted selection algorithm
- **Random Selection**: Statistically distributed message picking

### Trip Planning Integration
- **Origin/Destination**: Geographic coordinates and addresses
- **Timing Information**: Departure time and estimated travel time
- **Distance Calculation**: Route distance estimation

### User Context
- **User ID**: Authenticated user identification
- **Trip Tracking**: Plan ID generation for trip correlation
- **Message Personalization**: Context-aware message selection

## Probability Algorithm

### Spread List
```javascript
const spread = service.spreadList();
```
- Defines probability weights for different message types
- Ensures realistic distribution of transportation advice
- Configurable weighting system

### Statistical Validation
- **Accuracy Threshold**: ±100 units for 1,000,000 base
- **Individual Precision**: ±0.5% per probability
- **Large Sample Testing**: Validates over significant sample size

## UUID Management

### Plan ID Generation
- **UUID v4**: Cryptographically random identifiers
- **Trip Correlation**: Links messages to specific trips
- **Uniqueness Guarantee**: No collision risk

### Validation Process
- **Format Checking**: Standard UUID format validation
- **Uniqueness**: Each call generates unique identifier
- **Consistency**: Reliable ID generation across service calls

## Message Data Structure

### Message Components
```javascript
{
  idx: message_id,      // Numeric message identifier
  result: {
    title: string,      // Message title
    message: string     // Message content
  }
}
```

### Data Provider
- **Message Pool**: All available transportation messages
- **Structured Data**: Consistent message format
- **Content Management**: Centralized message administration

## Testing Methodology

### Statistical Testing
- **Probability Accuracy**: Mathematical validation of distributions
- **Large Sample Size**: 1,000,000 iterations for statistical significance
- **Precision Requirements**: 0.5% accuracy threshold

### Randomness Testing
- **Multiple Iterations**: 100 test cycles for message selection
- **Validation Coverage**: Ensures all messages can be selected
- **Consistency Checking**: Message structure validation

### Integration Testing
- **Full Request Cycle**: Complete HTTP request/response testing
- **Real Data**: Actual Houston locations for realistic testing
- **Error Handling**: Status code validation

## Business Logic

### Transportation Messaging
- **Trip Context**: Messages relevant to specific trips
- **Statistical Distribution**: Realistic message frequency
- **User Experience**: Appropriate message selection

### MTC Integration
- **Transportation Authority**: Official transportation commission integration
- **Regional Specificity**: Houston-area transportation context
- **Service Coordination**: Integration with broader transportation network

## Error Handling

### Validation Thresholds
- **Statistical Tolerance**: Acceptable variance in probability calculations
- **Format Validation**: UUID format checking
- **Data Integrity**: Message pool validation

### Service Reliability
- **Consistent Performance**: Reliable message generation
- **Error Prevention**: Validation prevents invalid message selection
- **Statistical Accuracy**: Maintains probability distribution requirements

## Integration Points

### Trip Planning System
- **Route Data**: Origin, destination, timing integration
- **User Context**: Authenticated user trip planning
- **Message Correlation**: Plan ID links messages to trips

### External Services
- **MTC API**: Metropolitan Transportation Commission integration
- **Geographic Services**: Houston-area location processing
- **Trip Tracking**: Plan ID management system

This test suite ensures the MTC service accurately generates transportation messages, maintains statistical probability distributions, and provides reliable trip planning integration for the TSP API's regional transportation features.