# Static/Constants Documentation: mock-data/ridehail.js

## 📋 File Overview
- **Purpose:** Provides comprehensive mock data for Uber ridehail API responses used in testing and development
- **Usage:** Used by test suites, development environments, and ridehail service integration testing
- **Type:** Mock data / Test fixtures / API response samples

## 🔧 Main Exports
```javascript
module.exports = {
  // ETA and fare estimation responses
  etaWithFareResponse,
  etaWithEstimationResponse,
  etaWithWrongFormatResponse,
  unavailableResponse,
  etaWithTwdResponse,
  // Access zones and pickup locations
  accessZonesWithHierarchicalResponse,
  accessZonesWithNonHierarchicalResponse,
  accessZonesWithEmptyResponse,
  // Trip management responses
  createGuestTripResponse,
  getTripDetailsResponse,
  completedTripDetailsResponse,
  receiptResponse
};
```

## 📝 Constants Reference
| Mock Data Type | Purpose | Key Features | Test Scenarios |
|----------------|---------|--------------|----------------|
| etaWithFareResponse | Uber fare estimates with upfront pricing | Multiple vehicle types, fare breakdowns, surge pricing | Normal fare requests, vehicle selection |
| etaWithEstimationResponse | Price ranges without upfront fares | Low/high estimates, pickup times | Markets without upfront pricing |
| unavailableResponse | Service unavailable scenarios | Null fares, no cars available | Service outages, low availability |
| etaWithTwdResponse | Taiwan market responses | TWD currency, local vehicle types | International market testing |
| accessZonesWithHierarchical | Airport pickup zones | Sub-zones, access points, wayfinding | Complex pickup locations |
| createGuestTripResponse | Trip booking responses | Guest user data, trip status | Guest trip creation flow |
| getTripDetailsResponse | Active trip information | Driver details, vehicle info, real-time location | Trip tracking features |
| completedTripDetailsResponse | Finished trip data | Final fare, trip metrics, receipt data | Trip completion handling |

## 💡 Usage Examples
```javascript
// Import mock data
const ridehailMocks = require('./static/mock-data/ridehail');

// Test fare estimation endpoint
const mockFareResponse = ridehailMocks.etaWithFareResponse;
console.log(mockFareResponse.product_estimates[0].estimate_info.fare.display); // '$11.96'

// Test surge pricing scenarios
const surgeResponse = ridehailMocks.createGuestTripSurgeResponse;
if (surgeResponse.code === 'surge') {
  // Handle surge confirmation flow
}

// Test access zones for airports
const airportZones = ridehailMocks.accessZonesWithHierarchicalResponse;
const pickupPoints = airportZones.master_zone.sub_zones[0].access_points;

// Test trip completion flow
const completedTrip = ridehailMocks.completedTripDetailsResponse;
const finalFare = completedTrip.client_fare; // '$10.41'
const tripDistance = completedTrip.trip_distance_miles; // 0.0177...
```

## ⚠️ Important Notes
- Mock data reflects real Uber API response structures for accurate testing
- Currency formats include both USD and TWD for international market support
- Fare IDs and timestamps are realistic but not production values
- Vehicle capacity and product types match actual Uber service offerings
- Access zones include realistic wayfinding instructions for user experience testing
- Error responses (surge, fare_expired) help test edge cases in payment flows

## 🏷️ Tags
**Keywords:** mock-data, uber-api, ridehail-testing, fare-estimation, trip-management, test-fixtures  
**Category:** #static #mock-data #ridehail #testing #uber-integration