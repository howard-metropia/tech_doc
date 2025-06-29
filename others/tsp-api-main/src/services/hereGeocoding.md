# TSP API HERE Geocoding Service Documentation

## 🔍 Quick Summary (TL;DR)
The HERE Geocoding service provides location geocoding functionality using HERE Technologies API, converting addresses to coordinates and validating location accuracy for transportation routing.

**Keywords:** here-geocoding | address-geocoding | location-search | coordinate-conversion | here-api | geolocation | address-validation | spatial-analysis

**Primary use cases:** Converting addresses to GPS coordinates, validating location data, searching for places near specific coordinates, address resolution for routing

**Compatibility:** Node.js >= 16.0.0, HERE Maps API, axios HTTP client

## ❓ Common Questions Quick Index
- **Q: What is geocoding?** → Converting addresses into GPS coordinates (latitude/longitude)
- **Q: Which geocoding API is used?** → HERE Technologies Geocoding API
- **Q: How accurate are the results?** → Validates results within 150-meter radius
- **Q: What regions are supported?** → Currently configured for USA (countryCode:USA)
- **Q: How many locations can be processed?** → Designed for batch processing of multiple addresses
- **Q: Are Chinese addresses supported?** → Yes, includes Chinese address format validation

## 📋 Functionality Overview

**Non-technical explanation:** 
Think of this as a **digital address book translator**. When you type an address like "123 Main Street, Houston, TX", this service talks to HERE Maps to find the exact GPS coordinates (like 29.7604, -95.3698) so the navigation system knows exactly where to go. It also double-checks that the location makes sense and is close to where you expect it to be.

**Technical explanation:** 
A geocoding service that interfaces with HERE Technologies API to convert address strings into precise geographic coordinates. It performs parallel geocoding requests, validates results against distance thresholds, and includes special handling for Chinese address formats with regex-based validation.

**Business value explanation:**
Essential for accurate location-based services and routing. Enables precise navigation, improves user experience by validating addresses, reduces routing errors, and supports international address formats for global transportation services.

## 🔧 Technical Specifications

- **File:** `allrepo/connectsmart/tsp-api/src/services/hereGeocoding.js`
- **Language:** JavaScript (ES2020)
- **Framework:** Standalone service class
- **Type:** Geocoding Integration Service
- **File Size:** ~3.2 KB
- **Complexity Score:** ⭐⭐⭐ (Medium - External API integration with validation logic)

**Dependencies:**
- `axios`: HTTP client for API requests (**Critical**)
- `@app/src/services/twoPointLength`: Distance calculation utility (**Critical**)

## 📝 Detailed Code Analysis

### CallAllAPI Method

**Purpose:** Performs parallel geocoding for multiple addresses using HERE API

**Parameters:**
- `QueryArray`: Array of address strings to geocode
- `QueryLatLng`: Array of fallback coordinates
- `APIKey`: HERE API authentication key

**Processing Flow:**
1. **URL Construction:** Builds HERE API URLs with address queries and country restrictions
2. **Parallel Requests:** Executes multiple geocoding requests simultaneously
3. **Response Processing:** Extracts coordinates from API responses
4. **Fallback Handling:** Uses provided coordinates if geocoding fails
5. **Result Assembly:** Returns array of coordinate objects

**HERE API Integration:**
```javascript
const URL1 = 'https://geocode.search.hereapi.com/v1/geocode?q=' +
  encodeURI(QueryArray[0]) +
  '&apikey=' + APIKey +
  '&in=countryCode:USA&at=' + QueryLatLng[0] +
  '&limit=1';
```

**Response Processing:**
```javascript
const Geocoding = element.data.items.length == 1 && 
  element.data.items[0].access !== undefined
  ? {
      lat: element.data.items[0].access[0].lat,
      lng: element.data.items[0].access[0].lng,
    }
  : { lat: tempLatLng[0], lng: tempLatLng[1] };
```

### CheckAddress Static Method

**Purpose:** Validates geocoded addresses using distance and format checks

**Parameters:**
- `Ary`: Array of geocoding results from HERE API
- `Querylocation`: Original query coordinates for distance validation

**Validation Logic:**
1. **Distance Check:** Validates results within 150-meter radius
2. **Chinese Address Validation:** Uses regex patterns for Chinese address formats
3. **Format Verification:** Checks address structure and components
4. **Coordinate Selection:** Returns best matching coordinates

**Chinese Address Regex Patterns:**
```javascript
const REG = new RegExp('.*[縣|市]+.*[鄉|鎮|區|村|里]+.*[村|里|路|段|街|道]+');
const REG2 = new RegExp('.*[No.]+.*[村|里|路|段|街|道]+.*[鄉|鎮|區|村|里]+.*[縣|市]+');
```

**Distance Validation:**
```javascript
if (TwoPointLength(
  parseFloat(Querylatlng[0]),
  parseFloat(Querylatlng[1]),
  parseFloat(element.access[0].lat),
  parseFloat(element.access[0].lng),
  'K'
) <= QueryRange) {
  // Process valid result
}
```

## 🚀 Usage Methods

### Basic Geocoding
```javascript
const hereGeocoding = require('@app/src/services/hereGeocoding');

// Geocode multiple addresses
const addresses = [
  '1600 Amphitheatre Parkway, Mountain View, CA',
  '1 Infinite Loop, Cupertino, CA'
];

const fallbackCoords = [
  '37.4219999,-122.0840575',
  '37.3318456,-122.0296002'
];

const apiKey = 'YOUR_HERE_API_KEY';

try {
  const results = await hereGeocoding.CallAllAPI(addresses, fallbackCoords, apiKey);
  console.log('Geocoding results:', results);
  // Results: [{ lat: 37.4219999, lng: -122.0840575 }, ...]
} catch (error) {
  console.error('Geocoding failed:', error);
}
```

### Address Validation
```javascript
// Validate geocoded results
const geocodingResults = [
  {
    address: { label: '台北市信義區信義路五段7號' },
    access: [{ lat: 25.0330, lng: 121.5654 }]
  }
];

const queryLocation = '25.0330,121.5654';

const validatedResult = hereGeocoding.CheckAddress(geocodingResults, queryLocation);

if (validatedResult.lat && validatedResult.lng) {
  console.log('Valid address found:', validatedResult);
} else {
  console.log('Address validation failed');
}
```

### Route Planning Integration
```javascript
class RoutePlanningService {
  constructor(apiKey) {
    this.apiKey = apiKey;
    this.geocoding = require('@app/src/services/hereGeocoding');
  }

  async planRoute(originAddress, destinationAddress) {
    try {
      // Prepare addresses and fallback coordinates
      const addresses = [originAddress, destinationAddress];
      const fallbackCoords = ['0,0', '0,0']; // Will be replaced with actual geocoding

      // Geocode both addresses
      const coordinates = await this.geocoding.CallAllAPI(
        addresses, 
        fallbackCoords, 
        this.apiKey
      );

      const origin = coordinates[0];
      const destination = coordinates[1];

      if (!origin.lat || !destination.lat) {
        throw new Error('Failed to geocode one or more addresses');
      }

      console.log(`Route from ${origin.lat},${origin.lng} to ${destination.lat},${destination.lng}`);
      
      // Continue with route calculation...
      return this.calculateRoute(origin, destination);
      
    } catch (error) {
      console.error('Route planning failed:', error);
      throw error;
    }
  }
}
```

### Batch Processing Example
```javascript
async function processBatchGeocoding(addressList, apiKey) {
  const batchSize = 10; // Process in batches to avoid rate limits
  const results = [];

  for (let i = 0; i < addressList.length; i += batchSize) {
    const batch = addressList.slice(i, i + batchSize);
    const fallbackCoords = batch.map(() => '0,0'); // Default fallbacks

    try {
      console.log(`Processing batch ${Math.floor(i/batchSize) + 1}...`);
      
      const batchResults = await hereGeocoding.CallAllAPI(
        batch,
        fallbackCoords,
        apiKey
      );
      
      results.push(...batchResults);
      
      // Rate limiting delay
      await new Promise(resolve => setTimeout(resolve, 1000));
      
    } catch (error) {
      console.error(`Batch ${Math.floor(i/batchSize) + 1} failed:`, error);
      // Add null results for failed batch
      results.push(...new Array(batch.length).fill({ lat: null, lng: null }));
    }
  }

  return results;
}
```

## 📊 Output Examples

### Successful Geocoding Results
```javascript
// Input addresses
const addresses = [
  'Space Needle, Seattle, WA',
  'Golden Gate Bridge, San Francisco, CA'
];

// Output coordinates
[
  { lat: 47.6205, lng: -122.3493 },
  { lat: 37.8199, lng: -122.4783 }
]
```

### Chinese Address Validation
```javascript
// Input: Chinese address with proper format
const chineseAddress = {
  address: { label: '台北市信義區信義路五段7號' },
  access: [{ lat: 25.0330, lng: 121.5654 }]
};

// Output: Valid coordinates
{ lat: 25.0330, lng: 121.5654 }

// Input: Invalid format or too far
// Output: { lat: null, lng: null }
```

### API Error Handling
```javascript
// Network error or invalid API key
{
  error: {
    message: 'Request failed with status code 401',
    code: 'UNAUTHORIZED'
  }
}

// No results found
{
  results: [
    { lat: 0, lng: 0 }, // Fallback coordinates used
    { lat: 0, lng: 0 }
  ]
}
```

## ⚠️ Important Notes

### HERE API Configuration
- **Country Restriction:** Currently limited to USA (`countryCode:USA`)
- **Result Limit:** Set to 1 result per query (`limit=1`)
- **Authentication:** Requires valid HERE API key
- **Rate Limiting:** Default retry delay of 5000ms configured

### Validation Parameters
- **Distance Threshold:** 150-meter radius for result validation
- **Chinese Address Support:** Regex patterns for traditional Chinese addresses
- **Fallback Strategy:** Uses provided coordinates when geocoding fails
- **Access Point Priority:** Prefers access coordinates over general location

### Error Handling
- **Network Failures:** Automatic axios retry with 5-second delay
- **API Errors:** Graceful degradation to fallback coordinates
- **Invalid Results:** Distance and format validation prevents bad data
- **Parallel Processing:** Promise.all handles multiple requests efficiently

### Performance Considerations
- **Parallel Requests:** Simultaneous geocoding for better performance
- **Result Caching:** Consider implementing caching for frequently used addresses
- **Rate Limiting:** Monitor HERE API usage limits
- **Batch Processing:** Suitable for processing multiple addresses

### International Support
- **Chinese Addresses:** Special regex validation for Chinese address formats
- **Address Components:** Recognizes Chinese administrative divisions (縣, 市, 鄉, 鎮, 區, etc.)
- **Format Flexibility:** Handles different Chinese address ordering patterns
- **Cultural Adaptation:** Addresses specific Chinese addressing conventions

### Geographic Accuracy
- **Access Points:** Prioritizes vehicular access coordinates
- **Distance Validation:** Ensures results are within reasonable proximity
- **Coordinate Precision:** Returns decimal degree coordinates
- **Error Bounds:** 150-meter tolerance for location matching

## 🔗 Related File Links

- **Distance Calculation:** `allrepo/connectsmart/tsp-api/src/services/twoPointLength.js`
- **HERE Routing Service:** `allrepo/connectsmart/tsp-api/src/services/hereRouting.js`
- **Routing Controllers:** Controllers that use geocoding for address resolution

---
*This service provides essential geocoding functionality for accurate location-based transportation services using HERE Technologies API.*