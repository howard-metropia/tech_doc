# twoPointLength.js Documentation

## 🔍 Quick Summary (TL;DR)

Calculates the distance between two geographic coordinates using the Haversine formula, supporting multiple units of measurement.

**Keywords:** distance calculation | haversine formula | geographic distance | coordinates | latitude longitude | miles | kilometers | nautical miles | geo distance

**Primary Use Cases:**
- Calculate distances between user locations
- Determine proximity for location-based services
- Validate trip distances for fare calculations

**Compatibility:** Node.js 14+, Pure JavaScript (no external dependencies)

## ❓ Common Questions Quick Index

- [How to calculate distance between two points?](#usage-methods)
- [What units are supported?](#technical-specifications)
- [Why is my distance calculation wrong?](#important-notes)
- [How accurate is the calculation?](#functionality-overview)
- [What's the maximum distance it can calculate?](#output-examples)
- [How to convert between units?](#usage-methods)
- [What coordinate format is required?](#technical-specifications)
- [How to troubleshoot zero distance results?](#important-notes)

## 📋 Functionality Overview

**Non-technical explanation:** This service is like a digital tape measure for the Earth. Just as you might measure the distance between two cities on a map, this function calculates the "as the crow flies" distance between any two points on Earth using their GPS coordinates.

**Technical explanation:** Implements the Haversine formula to calculate the great-circle distance between two points on a sphere given their longitude and latitude coordinates, accounting for Earth's curvature.

**Business value:** Essential for location-based features including fare calculations, proximity searches, delivery radius validation, and trip distance verification.

**System context:** Core utility used throughout the TSP API for distance-based calculations in trip planning, fare estimation, and location services.

## 🔧 Technical Specifications

- **File:** twoPointLength.js
- **Path:** /src/services/twoPointLength.js
- **Type:** Pure function utility
- **Size:** ~1KB
- **Complexity:** Low

**Dependencies:** None (pure JavaScript)

**Parameters:**
- `lat1` (Number) - First point latitude (-90 to 90)
- `lon1` (Number) - First point longitude (-180 to 180)
- `lat2` (Number) - Second point latitude (-90 to 90)
- `lon2` (Number) - Second point longitude (-180 to 180)
- `unit` (String) - Output unit: 'K' (kilometers), 'N' (nautical miles), default (miles)

**Return Value:** Number - Distance in specified unit

## 📝 Detailed Code Analysis

**Algorithm:** Haversine Formula
1. Convert degrees to radians
2. Calculate differences in coordinates
3. Apply Haversine formula using spherical trigonometry
4. Convert result to requested unit

**Mathematical Formula:**
```
a = sin²(Δφ/2) + cos φ1 ⋅ cos φ2 ⋅ sin²(Δλ/2)
c = 2 ⋅ atan2(√a, √(1−a))
d = R ⋅ c
```

**Unit Conversions:**
- Base calculation in miles (statute miles)
- Kilometers: miles × 1.609344 × 1000 (returns meters)
- Nautical miles: miles × 0.8684

**Edge Cases:**
- Same coordinates return 0
- Handles coordinate wraparound
- Clamps arc cosine input to prevent errors

## 🚀 Usage Methods

**Basic Distance Calculation:**
```javascript
const TwoPointLength = require('./services/twoPointLength');

// New York to Los Angeles (miles)
const distance = TwoPointLength(40.7128, -74.0060, 34.0522, -118.2437);
// Returns: ~2445 miles

// Same calculation in kilometers
const distanceKm = TwoPointLength(40.7128, -74.0060, 34.0522, -118.2437, 'K');
// Returns: ~3935000 meters
```

**Proximity Check:**
```javascript
// Check if two points are within 5km
const isNearby = (lat1, lon1, lat2, lon2) => {
  const distance = TwoPointLength(lat1, lon1, lat2, lon2, 'K');
  return distance <= 5000; // 5km in meters
};
```

**Trip Distance Validation:**
```javascript
// Validate trip distance for fare calculation
const validateTripDistance = (pickup, dropoff) => {
  const distance = TwoPointLength(
    pickup.lat, pickup.lon,
    dropoff.lat, dropoff.lon,
    'K'
  );
  return {
    distanceMeters: distance,
    distanceKm: distance / 1000,
    isValid: distance > 100 && distance < 100000 // 100m to 100km
  };
};
```

## 📊 Output Examples

**Short Distance (within city):**
```javascript
TwoPointLength(37.7749, -122.4194, 37.7849, -122.4094)
// Returns: 0.87 miles

TwoPointLength(37.7749, -122.4194, 37.7849, -122.4094, 'K')
// Returns: 1400 (meters)
```

**Long Distance (cross-country):**
```javascript
TwoPointLength(40.7128, -74.0060, 34.0522, -118.2437)
// Returns: 2445.56 miles

TwoPointLength(40.7128, -74.0060, 34.0522, -118.2437, 'N')
// Returns: 2123.51 nautical miles
```

**Same Location:**
```javascript
TwoPointLength(37.7749, -122.4194, 37.7749, -122.4194)
// Returns: 0
```

## ⚠️ Important Notes

**Accuracy Considerations:**
- Assumes perfect sphere (Earth is actually ellipsoid)
- Accuracy decreases for very short distances (<1m)
- Most accurate for distances 1km to 20,000km
- Does not account for elevation differences

**Common Issues:**
1. **Wrong unit confusion:** 'K' returns meters, not kilometers
2. **Coordinate order:** Ensure lat/lon order is correct
3. **Decimal degrees:** Use decimal, not degrees/minutes/seconds

**Performance:**
- O(1) constant time complexity
- No external API calls
- Suitable for real-time calculations

## 🔗 Related File Links

**Used By:**
- `/services/trip.js` - Trip distance validation
- `/services/intermodal.js` - Multi-modal route planning
- `/services/parking.js` - Nearby parking search
- `/services/ridehail.js` - Ride distance estimation

**Similar Utilities:**
- `/services/hereRouting.js` - Road distance calculations
- `/services/verifyGeoFormat.js` - Coordinate validation
- `/services/reformatHere.js` - Coordinate formatting

## 📈 Use Cases

**Real-time Applications:**
- User proximity to destinations
- Delivery radius validation
- Geofencing calculations

**Analytics:**
- Trip distance statistics
- Coverage area analysis
- User movement patterns

**Business Logic:**
- Distance-based pricing
- Service area validation
- Route optimization

## 🛠️ Improvement Suggestions

**Accuracy Enhancements:**
- Implement Vincenty formula for better accuracy
- Add elevation consideration
- Support different Earth radius models

**API Improvements:**
- Add batch distance calculation
- Support different coordinate systems
- Return additional metrics (bearing, midpoint)

**Performance:**
- Memoize frequently calculated distances
- Add input validation
- Implement distance matrix for multiple points

## 🏷️ Document Tags

**Keywords:** distance calculation | haversine | geographic distance | coordinates | latitude | longitude | miles | kilometers | nautical miles | great circle | spherical distance | GPS distance | location services

**Technical Tags:** #utility #geography #calculation #distance #coordinates

**Target Roles:** Backend Developer (All levels), GIS Developer

**Difficulty Level:** ⭐⭐ (Simple algorithm, important utility)

**Maintenance Level:** Low (mathematical formula rarely changes)

**Business Criticality:** High (core calculation for many features)

**Related Topics:** Geographic Information Systems (GIS), Coordinate systems, Map projections, Location-based services