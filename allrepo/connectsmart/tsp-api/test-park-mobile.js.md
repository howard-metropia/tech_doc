# test-park-mobile.js Technical Documentation

## Purpose

Comprehensive integration test suite for ParkMobile parking service integration, covering rate queries, parking session management, payment processing, and reminder functionality.

## Core Functionality

### ParkMobile Service Integration

#### 1. Rate Zone Query
- **Route**: `pmRateZone`
- **Method**: GET
- **Purpose**: Get parking rates and time options for a zone
- **API**: `https://api.parkmobile.io/platformrates/v1/rates/zone`

#### 2. Rate Price Calculation
- **Route**: `pmRatePrice`
- **Method**: GET  
- **Purpose**: Calculate parking cost for specific duration
- **API**: `https://api.parkmobile.io/platformrates/v1/rates/price`

#### 3. Start Parking Session
- **Route**: `pmStartParking`
- **Method**: POST
- **Purpose**: Activate parking session with payment
- **API**: `https://api.parkmobile.io/platformrates/v1/rates/activate`

#### 4. Set Parking Reminder
- **Route**: `pmSetReminder`
- **Method**: PUT
- **Purpose**: Configure expiration alerts

#### 5. List Parking Events
- **Route**: `pmListParkingEvents`
- **Method**: GET
- **Purpose**: Get user's active/recent parking sessions

## Test Data Structure

### Mock Parking Station
```javascript
const mockParkingStation = {
  _id: 'TestStation',
  station_id: 987654321,
  last_modified: '2023-01-13T08:12:32.660+0000',
  latitude: 29.750024,
  longitude: -95.361655,
};
```

### Test Parameters
```javascript
const testUserId = 1003;
const fakeLpn = 'ABC1234567';        // License plate
const testZone = '987654321';        // Parking zone
const fakeTimeBlockId = '12345';     // Duration option
const hardcodedArea = 953;           // Geographic area
```

## API Response Structures

### Rate Zone Response
```javascript
const successRateZoneResponse = {
  hasDurationSelections: true,
  startTimeUtc: '2023-08-03T01:18:55',
  maxPerSessionMinutes: 180,
  maxSelectableMinutes: 222,
  timeZoneStandardName: 'Central Standard Time',
  isParkingAllowed: true,
  parkingNotAllowedReason: '',
  preDefinedTmeBlocks: [{
    timeBlockValue: 222,
    name: 'Maximum parking time',
    timeBlockUnit: 'Minutes',
    timeBlockId: 409491,
  }],
  durationSelections: {
    timeBlockId: 0,
    hasHourMinuteSelections: true,
    hourMinuteDurationSelections: [
      { minutes: [12, 24, 36, 48] },
      { hour: 1, minutes: [0, 12, 24, 36, 48] },
      { hour: 2, minutes: [0, 12, 24, 36, 48] },
      { hour: 3, minutes: [0, 12, 24, 36, 42] },
    ]
  }
};
```

### Price Response
```javascript
const successRatePriceResponse = {
  price: {
    parkingPrice: 0,
    transactionFee: 0,
    totalPrice: 0,
  },
  parkingStartTimeLocal: '2023-06-01T15:36:15',
  parkingStopTimeLocal: '2023-06-01T17:59:59',
  isParkingAllowed: true,
  maxParkingTime: { hours: 1, days: 0, minutes: 0, totalMinutes: 0 },
  timeZoneStandardName: 'Central Standard Time',
  currency: 'USD',
  currencySymbol: '$',
};
```

### Activation Response
```javascript
const successRateActivateResponse = {
  sessionId: 'IC73443624523235N',
  lpn: fakeLpn,
  zone: `${hardcodedArea}${testZone}`,
  price: { parkingPrice: 0, transactionFee: 0, totalPrice: 0 },
  startTimeUTC: moment.utc().format('YYYY-MM-DDTHH:mm:ss') + 'Z',
  stopTimeUTC: moment.utc().add(1, 'hours').format('YYYY-MM-DDTHH:mm:ss') + 'Z',
  createdAt: moment.utc().format('YYYY-MM-DDTHH:mm:ss') + 'Z',
};
```

## Service Logic

### TimeBlockId Handling
```javascript
const replaceZeroTimeBlockId = (input) => {
  // Replaces zero timeBlockId with valid one from preDefinedTmeBlocks
  if (input.isParkingAllowed && 
      input.durationSelections.hasHourMinuteSelections &&
      input.durationSelections.timeBlockId === 0) {
    
    const validTimeBlockId = input.preDefinedTmeBlocks[0].timeBlockId;
    input.durationSelections.timeBlockId = validTimeBlockId;
  }
  return input;
};
```

## Data Models

### PmApiToken
- **Purpose**: Store ParkMobile API authentication tokens
- **Fields**: `token`, `expires`

### PmPriceObjects (MongoDB)
- **Purpose**: Cache pricing calculations
- **Fields**: Price details, zone info, payment status

### PmParkingEvent (MySQL)
- **Purpose**: Track parking sessions
- **Fields**: User, zone, timing, license plate, status

### PmParkingEvents (MongoDB)
- **Purpose**: Log all parking transactions
- **Fields**: Request/response data, HTTP status

## Payment Integration

### Payment Types
- **Coins**: Platform currency payment
- **Credit Card**: External payment method

### Point Transaction Flow
```javascript
// Parking fee transaction (activity_type: 13)
const parkingFeeTransaction = {
  activity_type: 13,
  payer: testUserId,
  payee: 2105,  // Parking fee account
  points: -1.25,
  note: eventId
};

// Transaction fee (activity_type: 14)  
const transactionFeeTransaction = {
  activity_type: 14,
  payer: testUserId,
  payee: 2104,  // Transaction fee account
  points: -0.2,
  note: eventId
};
```

## Error Handling

### Authentication Errors
- **Code 10004**: Missing user ID header
- **Code 40202**: ParkMobile API authentication failure

### Validation Errors
- **Code 10001**: Invalid parameters
- **Code 10002**: Missing required fields

### Business Logic Errors
- **Code 40210**: Duplicate parking session
- **Code 23018**: Insufficient coin balance
- **Code 40205**: ParkMobile service error
- **Code 40211**: Payment processing failure

### License Plate Validation
```javascript
// Valid format: alphanumeric, 3-12 characters
const lpnPattern = /^[A-Z0-9]{3,12}$/i;
```

## Third-Party Monitoring

### Error Tracking
```javascript
const eventEmitter = require('@app/src/helpers/third-party-monitor');

eventEmitter.setReceiver({
  send: (error) => {
    // Log: status, vendorApi, errorMsg, meta
    console.log(`Error: ${error.status} - ${error.errorMsg}`);
  }
});
```

### API Monitoring
- **Success Tracking**: Response time and success rates
- **Error Logging**: Failed requests with full context
- **Vendor API**: Track specific ParkMobile endpoints

## Security Features

### Data Protection
```javascript
const shouldNotIncludeCreditCardInfo = (list) => {
  list.forEach((item) => {
    expect(item).to.have.property('cardAlias');
    ['cc_number', 'expiry_month', 'expiry_year', 'cvv', 'zip_code']
      .forEach((field) => {
        expect(item).to.not.have.property(field);
      });
  });
};
```

### Sensitive Data Handling
- **Credit Card Info**: Never stored in logs
- **Card Alias**: Safe reference to payment method
- **Transaction Logs**: Sanitized request/response data

## Reminder System

### Alert Configuration
```javascript
const reminderData = {
  id: parkingEventId,
  alert_before: 5  // Minutes before expiration
};
```

### Alert Timing Validation
- **Minimum**: 5 minutes before expiration
- **Maximum**: 30 minutes before expiration
- **Validation**: Must be less than total parking duration

## Event Lifecycle Management

### Parking Status Flow
1. **ON_GOING**: Active parking session
2. **ALERTED**: Expiration warning sent
3. **FINISHED**: Session completed normally
4. **EXPIRED**: Session expired without extension

### Event Filtering
- **Active Events**: ON_GOING, ALERTED statuses
- **Recent Events**: FINISHED within 24 hours
- **Excluded**: EXPIRED events older than 24 hours

## Integration Testing

### Mock Strategy
- **Nock**: HTTP request mocking for ParkMobile API
- **Response Codes**: 200 (success), 401/403 (auth), 500 (error)
- **Timeout Testing**: Network timeout simulation

### Database Testing
- **Transaction Isolation**: Each test cleans up after itself
- **Data Consistency**: Verify all related records created/updated
- **Referential Integrity**: Maintain relationships between models

## Performance Considerations

### Caching Strategy
- **Price Objects**: Cache pricing calculations
- **API Tokens**: Reuse valid authentication tokens
- **Station Data**: Cache parking station information

### Timeout Management
- **API Calls**: 10-second timeout for ParkMobile requests
- **Test Timeouts**: Extended timeouts for complex operations

## Usage Examples

### Getting Zone Rates
```javascript
const config = {
  headers: { userid: testUserId, 'Content-Type': 'application/json' },
  params: { zone: testZone }
};

const response = await httpClient.get('/api/v2/parking/rate-zone', config);
```

### Starting Parking Session
```javascript
const postData = {
  price_id: uuid,
  lpn: 'ABC1234',
  lpnState: 'TX',
  payment_type: 'coin'
};

const response = await httpClient.post('/api/v2/parking/start', postData, config);
```

This test suite ensures robust ParkMobile integration, covering rate queries, payment processing, session management, and comprehensive error handling with proper security measures.