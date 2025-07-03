# Ridehail Mock Data Collection

## Overview
**File**: `src/static/mock-data/ridehail.js`  
**Type**: Test Data Module  
**Purpose**: Comprehensive collection of mock response data for Uber ridehail API integration testing and development

## Core Functionality

### Mock Data Repository
This module provides a complete set of realistic mock responses that mirror the actual Uber Guest API responses, enabling comprehensive testing of ridehail integration features without requiring live API calls.

### Response Categories
The mock data covers the full lifecycle of ridehail operations including fare estimation, trip booking, status updates, access zones, and receipt generation.

## Fare Estimation Mock Data

### ETA with Fare Response
```javascript
const etaWithFareResponse = {
  etas_unavailable: false,
  fares_unavailable: false,
  product_estimates: [
    {
      estimate_info: {
        fare: {
          currency_code: 'USD',
          display: '$11.96',
          expires_at: 1558147984,
          fare_breakdown: [
            {
              name: 'Base Fare',
              type: 'base_fare',
              value: 11.96,
            },
          ],
          fare_id: '6e642142-27b8-49df-82e0-3d4a8633e79d',
          value: 11.96,
        },
        pickup_estimate: 4,
        trip: {
          distance_estimate: 0.44,
          distance_unit: 'mile',
          duration_estimate: 927,
          travel_distance_estimate: 0.45,
        },
      },
      product: {
        display_name: 'UberX',
        product_id: 'b8e5c464-5de2-4539-a35a-986d6e58f186',
        capacity: 4,
        description: 'Affordable rides, all to yourself',
        upfront_fare_enabled: true,
        scheduling_enabled: true,
        cancellation: {
          min_cancellation_fee: 5,
          cancellation_grace_period_threshold_sec: 120,
        },
      },
      fulfillment_indicator: 'GREEN',
    },
  ],
};
```

**Key Features**:
- **Multiple Product Types**: UberX, WAV (wheelchair accessible), Black, Black Hourly
- **Fare Information**: Detailed pricing with breakdown and expiration
- **Trip Estimates**: Distance, duration, and pickup time estimates
- **Product Details**: Vehicle capacity, descriptions, scheduling options
- **Fulfillment Indicators**: GREEN, YELLOW status indicators

### Product Variety Examples

#### UberX Standard Service
```javascript
{
  product: {
    display_name: 'UberX',
    description: 'Affordable rides, all to yourself',
    capacity: 4,
    product_group: 'uberx',
    scheduling_enabled: true,
  },
  estimate_info: {
    fare: { display: '$11.96', value: 11.96 },
    pickup_estimate: 4,
  },
}
```

#### Wheelchair Accessible Vehicle (WAV)
```javascript
{
  product: {
    display_name: 'WAV',
    description: 'Wheelchair-accessible rides',
    capacity: 4,
  },
  estimate_info: {
    pickup_estimate: 8,
    pricing_explanation: 'Fares are higher due to increased demand',
  },
}
```

#### Premium Black Service
```javascript
{
  product: {
    display_name: 'Black',
    description: 'Premium rides in luxury cars',
    advance_booking_type: 'RESERVE',
    reserve_info: {
      enabled: true,
      scheduled_threshold_minutes: 120,
      free_cancellation_threshold_minutes: 60,
    },
  },
  estimate_info: {
    fare: { display: '$28.00', value: 28 },
    no_cars_available: true,
  },
}
```

#### Hourly Service
```javascript
{
  product: {
    display_name: 'Black Hourly',
    description: 'Luxury rides by the hour with professional drivers',
  },
  estimate_info: {
    fare: {
      hourly: {
        tiers: [
          {
            amount: 135.32,
            time_in_mins: 120,
            distance: 30,
            formatted_time_and_distance_package: '2 hrs/30 miles',
          },
        ],
        overage_rates: {
          overage_rate_per_temporal_unit: 1.4,
          overage_rate_per_distance_unit: 3.55,
        },
      },
    },
  },
}
```

## Alternative Response Formats

### ETA with Estimation Range
```javascript
const etaWithEstimationResponse = {
  product_estimates: [
    {
      estimate_info: {
        estimate: {
          display: '$13-16',
          low_estimate: 13,
          high_estimate: 16,
          currency_code: 'USD',
        },
        pickup_estimate: 3,
      },
    },
  ],
};
```

**Use Case**: When exact fares aren't available, provides price ranges

### Wrong Format Response
```javascript
const etaWithWrongFormatResponse = {
  product_estimates: [
    {
      estimate_info: {
        fare: {
          display: 'Select Time',  // Non-standard display format
          value: 23.97,
        },
      },
    },
  ],
};
```

**Purpose**: Tests error handling for malformed API responses

### Unavailable Service Response
```javascript
const unavailableResponse = {
  etas_unavailable: false,
  fares_unavailable: true,
  product_estimates: [
    {
      estimate_info: {
        estimate: null,
        fare: null,
        pickup_estimate: 4,
      },
    },
  ],
};
```

**Scenario**: Service unavailable or pricing temporarily disabled

## Access Zones Mock Data

### Hierarchical Zone Structure
```javascript
const accessZonesWithHierarchicalResponse = {
  bounding_box: {
    north_east_lat: 40.64579533968136,
    north_east_lng: -73.77217574100271,
    south_west_lat: 40.63680466031865,
    south_west_lng: -73.78402425899729,
  },
  master_zone: {
    id: 'bee23dac-5a74-46ca-a9bd-147253f34ee9',
    name: 'John F. Kennedy International Airport',
    categories: ['airport'],
    sub_zones: [
      {
        id: '5c944720-b172-42d3-b74c-5b0b8f8e682f',
        name: 'Terminal 4, Arrivals',
        access_points: [
          {
            id: '7dd8e48e-2635-489f-8fb3-306d9f47b521',
            label: 'Pick-Up A',
            latitude: 40.6442406,
            longitude: -73.7835249,
            rider_wayfinding_note: 'Meet your driver curbside on the Arrivals level',
          },
        ],
      },
    ],
  },
};
```

**Features**:
- **Complex Hierarchy**: Master zones with sub-zones
- **Multiple Access Points**: Specific pickup locations
- **Wayfinding Instructions**: Detailed pickup guidance
- **Geographic Boundaries**: Bounding box coordinates

### Non-Hierarchical Zone
```javascript
const accessZonesWithNonHierarchicalResponse = {
  master_zone: {
    id: '7d9968b3-be48-42c2-9eef-1018a24423b3',
    name: 'Times Square',
    categories: ['train', 'marketplace_optimization'],
    access_points: [
      {
        label: 'W 47th St. & Broadway',
        latitude: 40.75962698997689,
        longitude: -73.98535697956041,
        rider_wayfinding_note: 'Meet your driver on the NW corner',
      },
    ],
    sub_zones: null,
  },
};
```

**Use Case**: Simple zones without sub-zone complexity

### Empty Zone Response
```javascript
const accessZonesWithEmptyResponse = {
  master_zone: null,
  access_points: [
    {
      id: '90f5c43c-4c60-4409-b4bf-e4ebe0ffc4cf',
      latitude: 37.8020597,
      longitude: -122.4180167,
      label: 'Leavenworth St',
    },
  ],
};
```

**Scenario**: Areas with direct access points but no formal zones

## Trip Management Mock Data

### Create Guest Trip Response
```javascript
const createGuestTripResponse = {
  request_id: 'e249c871-7711-4c26-b06c-679cbad6a7c2',
  product_id: 'a1111c8c-c720-46c3-8534-2fcdd730040d',
  status: 'processing',
  surge_multiplier: 1,
  guest: {
    guest_id: 'b625d1f7-411c-53a8-b2e0-decb81551c2f',
    first_name: 'Jane',
    last_name: 'Doe',
    phone_number: '+14155550000',
    email: 'jane@example.com',
    locale: 'en',
  },
};
```

### Surge Pricing Response
```javascript
const createGuestTripSurgeResponse = {
  code: 'surge',
  message: 'Fare is higher than normal, request again to confirm',
  metadata: {
    fare_id: 'dcf8a733-7f11-4544-a9c7-ddea71e46146',
    fare_display: '$12-15',
    multiplier: 1.4,
    expires_at: 1501684062,
  },
};
```

### Fare Expired Response
```javascript
const createGuestTripExpiredResponse = {
  code: 'fare_expired',
  message: 'The fare estimate has expired, request again to confirm',
  metadata: {
    fare_id: 'dcf8a733-7f11-4544-a9c7-ddea71e46146',
    multiplier: 1,
  },
};
```

## Trip Status Tracking

### Active Trip Details
```javascript
const getTripDetailsResponse = {
  begin_trip_time: 1564758770000,
  destination: {
    address: 'Bryant Park, New York, NY 10018',
    eta: 18,
    latitude: 40.7535965,
    longitude: -73.9832326,
  },
  driver: {
    id: '42d53206-d8ba-5d5e-9f9b-c9e4a33d3a4c',
    name: 'Joe',
    phone_number: '+11234567891',
    rating: 4.9,
    pin_based_phone_number: {
      phone_number: '+11234567890',
      pin: '12345678',
    },
  },
  status: 'accepted',
  vehicle: {
    license_plate: 'ABCD1234',
    make: 'Oldsmobile',
    model: 'Intrigue',
    vehicle_color_name: 'white',
  },
};
```

### Completed Trip Details
```javascript
const completedTripDetailsResponse = {
  status: 'completed',
  can_tip: true,
  client_fare: '$10.41',
  dropoff_time: 1564758815000,
  trip_distance_miles: 0,
  trip_duration_seconds: 900,
  waypoints: [
    {
      latitude: 40.7741769,
      longitude: -73.9849118,
      type: 'pickup',
    },
    {
      latitude: 40.7535965,
      longitude: -73.9832326,
      type: 'dropoff',
    },
  ],
};
```

### Canceled Trip Scenarios

#### Driver Canceled
```javascript
const driverCanceledTripDetailsResponse = {
  status: 'driver_canceled',
  cancellation_info: {
    cancellation_time_stamp: 1694674602000,
    cancellation_type: 'RIDER_NO_SHOW',
    driver_arrived_time_stamp: 1694673912000,
    driver_wait_time_minutes: 11,
  },
  client_fare: '$6.00',
  is_eligible_for_refund: false,
};
```

#### Rider Canceled
```javascript
const riderCanceledTripDetailsResponse = {
  status: 'rider_canceled',
  client_fare: '$0.00',
  status_detail: 'coordinator_canceled',
  trip_distance_miles: 0,
  trip_duration_seconds: 0,
};
```

#### No Drivers Available
```javascript
const noDriversAvailableResponse = {
  status: 'no_drivers_available',
  client_fare: '0.00',
  trip_distance_miles: 0,
  trip_duration_seconds: 0,
};
```

## Receipt and Billing Mock Data

### Standard Receipt
```javascript
const receiptResponse = {
  request_id: 'ce24b18a-a89c-4137-90a2-2b4f3568aa35',
  charges: [
    {
      name: 'Time',
      amount: 0.06,
    },
    {
      name: 'Base Fare',
      amount: 2.64,
    },
    {
      name: '$5.62 Minimum',
      amount: 1.57,
    },
  ],
  total_owed: '$5.67',
  total_fare: '$5.67',
  subtotal: '$4.27',
  currency_code: 'USD',
  duration: '00:10:24',
  distance: '8.21',
  distance_label: 'miles',
  charge_adjustments: [
    {
      name: 'Booking Fee',
      amount: 1.35,
      type: 'transport.fare.platform_fee',
    },
    {
      name: 'Texas Regulatory Recovery Fee',
      amount: 0.05,
      type: 'transport.fare.charges.regulatory_recovery_surcharge',
    },
  ],
};
```

### Canceled Trip Receipt
```javascript
const canceledReceipt = {
  charges: [
    {
      name: 'Cancellation Fee',
      amount: 5.25,
    },
  ],
  total_owed: '$5.31',
  duration: '',
  distance: '0',
  charge_adjustments: [
    {
      name: 'Texas Regulatory Recovery Fee',
      amount: 0.06,
    },
  ],
};
```

### Receipt Not Found
```javascript
const receiptNotFoundResponse = {
  message: "No receipt available. This may be because you weren't charged.",
  metadata: {
    statusCode: '404',
  },
  code: 'entity_not_found',
};
```

## Usage and Integration

### Test Environment Setup
```javascript
const ridehailMocks = require('@app/src/static/mock-data/ridehail');

// Mock Uber API responses in tests
jest.mock('uber-guest-api', () => ({
  getETA: jest.fn(() => Promise.resolve(ridehailMocks.etaWithFareResponse)),
  createTrip: jest.fn(() => Promise.resolve(ridehailMocks.createGuestTripResponse)),
  getTripDetails: jest.fn(() => Promise.resolve(ridehailMocks.getTripDetailsResponse)),
}));
```

### Development Environment
```javascript
// Use mock data when API is unavailable
const useRealAPI = process.env.NODE_ENV === 'production';

const getETAData = async (params) => {
  if (useRealAPI) {
    return await uberAPI.getETA(params);
  } else {
    return ridehailMocks.etaWithFareResponse;
  }
};
```

### Error Scenario Testing
```javascript
// Test different error scenarios
const testErrorScenarios = [
  {
    name: 'Surge Pricing',
    response: ridehailMocks.createGuestTripSurgeResponse,
  },
  {
    name: 'Fare Expired',
    response: ridehailMocks.createGuestTripExpiredResponse,
  },
  {
    name: 'No Drivers',
    response: ridehailMocks.noDriversAvailableResponse,
  },
];
```

## Data Validation and Schema

### Response Validation
```javascript
const validateETAResponse = (response) => {
  return (
    response &&
    Array.isArray(response.product_estimates) &&
    typeof response.etas_unavailable === 'boolean' &&
    typeof response.fares_unavailable === 'boolean'
  );
};

const validateTripResponse = (response) => {
  return (
    response &&
    response.request_id &&
    response.status &&
    response.guest
  );
};
```

### Schema Testing
```javascript
describe('Ridehail Mock Data Schema', () => {
  test('ETA response should match expected schema', () => {
    const response = ridehailMocks.etaWithFareResponse;
    expect(validateETAResponse(response)).toBe(true);
  });
  
  test('Trip creation response should be valid', () => {
    const response = ridehailMocks.createGuestTripResponse;
    expect(validateTripResponse(response)).toBe(true);
  });
});
```

## Performance Testing

### Load Testing Data
```javascript
// Generate multiple mock responses for load testing
const generateMockETAResponses = (count) => {
  return Array.from({ length: count }, (_, index) => ({
    ...ridehailMocks.etaWithFareResponse,
    product_estimates: ridehailMocks.etaWithFareResponse.product_estimates.map(
      estimate => ({
        ...estimate,
        estimate_info: {
          ...estimate.estimate_info,
          pickup_estimate: Math.floor(Math.random() * 15) + 1,
        },
      })
    ),
  }));
};
```

## Best Practices

### Mock Data Management
- **Realistic Data**: Use realistic values that match production patterns
- **Edge Cases**: Include edge cases and error scenarios
- **Consistency**: Maintain consistent data formats across responses
- **Updates**: Keep mock data synchronized with API changes

### Testing Strategy
- **Comprehensive Coverage**: Test all response types and scenarios
- **Error Handling**: Include error responses and edge cases
- **Performance**: Use mock data for performance testing
- **Integration**: Validate integration with real API responses

### Maintenance Guidelines
- **Version Control**: Track changes to mock data structures
- **Documentation**: Document the purpose of each mock response
- **Validation**: Regularly validate against actual API responses
- **Cleanup**: Remove obsolete mock data when API changes

This comprehensive mock data collection enables thorough testing of ridehail integration features, ensuring robust error handling and complete coverage of Uber Guest API scenarios without requiring live API access during development and testing phases.