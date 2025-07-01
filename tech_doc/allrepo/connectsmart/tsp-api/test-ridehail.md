# TSP API Test Suite - Ridehail Service Tests

## Overview
The `test-ridehail.js` file contains comprehensive integration tests for the ridehail service functionality, covering pickup point discovery, Uber estimation API integration, and complete ridehail service workflows.

## File Location
`/allrepo/connectsmart/tsp-api/test/test-ridehail.js`

## Dependencies
- **supertest**: HTTP assertion library for API testing
- **chai**: Testing assertions and expectations
- **@maas/core**: Core MaaS framework components
- **Models**: Trips, RidehailTrips for database operations

## Test Architecture

### API Testing Setup
```javascript
const createApp = require('@maas/core/api');
const { getRouter } = require('@maas/core');
const app = createApp();
const router = getRouter();
const request = supertest.agent(app.listen());
```

### Authentication Configuration
```javascript
const auth = {
  authorization: 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...',
  userid: 1003,
  'Content-Type': 'application/json'
};
```

## Test Categories

### 1. Pickup Point Discovery API

**Endpoint**: `GET /pickup_point`

**Purpose**: Retrieve available ridehail pickup locations near specified coordinates

#### Successful Pickup Point Retrieval
```javascript
describe('[GET] /pickup_point', async () => {
  const lat = 40.7517665;  // New York coordinates
  const lng = -73.98786252;
  
  it('should get access zones', async function () {
    this.timeout(10000);
    const resp = await request
      .set(auth)
      .get(`${url}/?latitude=${lat}&longitude=${lng}`);
    
    const { result, data } = resp.body;
    expect(result).to.eq('success');
    expect(data.access_points).length.to.gt(0);
    
    // Validate pickup point structure
    expect(data.access_points[0]).to.includes.keys([
      'id',
      'latitude', 
      'longitude',
      'label'
    ]);
  });
});
```

#### Parameter Validation Tests
```javascript
it('should be failed with error code: 10001 while missing longitude parameter', async () => {
  const resp = await request.set(auth).get(`${url}/?latitude=${lat}`);
  const { result, error } = resp.body;
  
  expect(result).to.eq('fail');
  expect(error).to.include({
    code: 10001,
    msg: '"longitude" is required'
  });
});

it('should be failed with error code: 10001 while missing latitude parameter', async () => {
  const resp = await request.set(auth).get(`${url}/?longitude=${lng}`);
  const { result, error } = resp.body;
  
  expect(result).to.eq('fail');
  expect(error).to.include({
    code: 10001,
    msg: '"latitude" is required'
  });
});
```

#### Authentication Validation
```javascript
it('should be failed with error code: 10003 while missing auth token', async () => {
  const resp = await request
    .get(`${url}/?latitude=${lat}&longitude=${lng}`)
    .unset('authorization');
  
  const { result, error } = resp.body;
  expect(result).to.eq('fail');
  expect(error).to.include({
    code: 10003,
    msg: 'Token required'
  });
});
```

### 2. Uber Estimation API

**Endpoint**: `POST /uber_estimation`

**Purpose**: Get fare estimates and availability for Uber rides

#### Input Data Structure
```javascript
const inputData = {
  pickup: {
    latitude: 29.756065,
    longitude: -95.4077633
  },
  dropoff: {
    latitude: 29.717299,
    longitude: -95.402483
  }
};
```

#### Estimation Request Tests
```javascript
describe('[POST] /uber_estimation', () => {
  const url = router.url('createUberEta');
  
  it('should return Uber fare estimates', async function () {
    this.timeout(15000);
    const resp = await request
      .set(auth)
      .post(url)
      .send(inputData);
    
    const { result, data } = resp.body;
    expect(result).to.eq('success');
    
    // Validate estimation response structure
    expect(data).to.be.an('array');
    if (data.length > 0) {
      expect(data[0]).to.includes.keys([
        'product_id',
        'product_display',
        'fare_display',
        'fare_currency',
        'pickup_eta',
        'trip_duration',
        'no_cars_available'
      ]);
    }
  });
});
```

## Pickup Point System

### Access Zone Management
- **Geographic Coverage**: Define ridehail service areas
- **Pickup Optimization**: Strategic pickup point placement
- **Real-time Availability**: Dynamic pickup point status

### Response Data Structure
```javascript
{
  result: 'success',
  data: {
    access_points: [
      {
        id: number,
        latitude: number,
        longitude: number,
        label: string,
        type: string,
        availability: boolean,
        walking_distance: number
      }
    ]
  }
}
```

### Location Services Integration
- **Coordinate Validation**: Ensure valid latitude/longitude ranges
- **Proximity Calculation**: Find nearest available pickup points
- **Service Area Verification**: Confirm coverage within operational zones

## Uber API Integration

### Fare Estimation Service
```javascript
const uberEstimationFlow = {
  // 1. Validate pickup/dropoff coordinates
  validateCoordinates: (pickup, dropoff) => {
    return isValidLatLng(pickup) && isValidLatLng(dropoff);
  },
  
  // 2. Request Uber API estimates
  requestEstimates: async (pickup, dropoff) => {
    const response = await uberAPI.estimates({
      start_latitude: pickup.latitude,
      start_longitude: pickup.longitude,
      end_latitude: dropoff.latitude,
      end_longitude: dropoff.longitude
    });
    return response;
  },
  
  // 3. Process and format response
  formatEstimates: (rawEstimates) => {
    return rawEstimates.map(estimate => ({
      product_id: estimate.product_id,
      product_display: estimate.display_name,
      fare_display: estimate.estimate,
      fare_currency: estimate.currency_code,
      pickup_eta: estimate.pickup_estimate,
      trip_duration: estimate.duration_estimate,
      no_cars_available: estimate.no_cars_available
    }));
  }
};
```

### Error Handling
- **Network Failures**: Uber API connectivity issues
- **Rate Limiting**: API quota management
- **Invalid Responses**: Malformed data handling
- **Service Unavailability**: No drivers available scenarios

## Database Models Integration

### Trips Model
```javascript
const Trip = {
  user_id: number,
  travel_mode: number, // RIDEHAIL mode
  origin: string,
  origin_latitude: number,
  origin_longitude: number,
  destination: string,
  destination_latitude: number,
  destination_longitude: number,
  started_on: datetime,
  ended_on: datetime,
  distance: number,
  ridehail_trip_id: number
};
```

### RidehailTrips Model
```javascript
const RidehailTrip = {
  trip_id: number,
  product_id: string,
  fare_id: string,
  pickup_latitude: number,
  pickup_longitude: number,
  dropoff_latitude: number,
  dropoff_longitude: number,
  estimated_fare: number,
  actual_fare: number,
  status: string,
  driver_id: string,
  vehicle_details: object
};
```

## API Error Codes

### Standard Error Responses
```javascript
const ERROR_CODES = {
  10001: 'Validation Error - Missing required parameter',
  10002: 'Validation Error - Invalid parameter format',
  10003: 'Authentication Error - Token required',
  10004: 'Authorization Error - Invalid permissions',
  10005: 'Service Error - External API failure'
};
```

### Error Response Format
```javascript
{
  result: 'fail',
  error: {
    code: number,
    msg: string,
    details?: object
  }
}
```

## Testing Strategies

### Integration Testing
- **End-to-End Workflows**: Complete ridehail booking flow
- **API Integration**: External service connectivity
- **Database Operations**: Data persistence and retrieval
- **Authentication Flow**: Token validation and authorization

### Mock Data Testing
- **Uber API Mocking**: Simulated responses for consistent testing
- **Location Data**: Predefined coordinate sets for testing
- **User Scenarios**: Different user types and permissions

### Performance Testing
```javascript
describe('Performance Tests', () => {
  it('should respond within acceptable time limits', async function () {
    this.timeout(10000);
    const startTime = Date.now();
    
    const resp = await request
      .set(auth)
      .get(`/pickup_point?latitude=${lat}&longitude=${lng}`);
    
    const endTime = Date.now();
    const responseTime = endTime - startTime;
    
    expect(resp.statusCode).to.eq(200);
    expect(responseTime).to.be.lessThan(5000); // 5 second max
  });
});
```

## Service Integration Points

### Location Services
- **GPS Coordinate Processing**: Real-time location handling
- **Geofencing**: Service area boundary enforcement
- **Mapping Integration**: Route calculation and display

### Payment Processing
- **Fare Calculation**: Dynamic pricing integration
- **Payment Methods**: Multiple payment option support
- **Transaction Tracking**: Payment status monitoring

### Notification Services
- **Ride Status Updates**: Real-time trip notifications
- **Driver Notifications**: Pickup and arrival alerts
- **User Communications**: Service updates and confirmations

## Quality Assurance

### Data Validation
- **Coordinate Range Validation**: Ensure realistic GPS coordinates
- **Service Area Coverage**: Verify pickup points within service zones
- **Fare Accuracy**: Validate estimated vs actual pricing

### Reliability Testing
- **Network Resilience**: Handle API failures gracefully
- **Data Consistency**: Maintain accurate trip and fare records
- **User Experience**: Smooth ridehail booking experience

### Security Considerations
- **Authentication Validation**: Secure API access
- **Data Protection**: User location privacy
- **Payment Security**: Secure financial transactions

This comprehensive test suite ensures the ridehail service provides reliable pickup point discovery, accurate fare estimation, and seamless integration with Uber's ridehail platform while maintaining high standards for performance, security, and user experience.