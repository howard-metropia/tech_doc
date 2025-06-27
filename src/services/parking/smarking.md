# Smarking Parking Service Documentation

## 🔍 Quick Summary (TL;DR)

**One-sentence description:** A Node.js service module that integrates with Smarking's parking API to retrieve on-street parking locations and real-time garage occupancy data for MaaS (Mobility as a Service) applications.

**Core functionality keywords:** parking integration | smarking api | occupancy data | on-street parking | garage availability | real-time parking | mobility service | third-party integration | parking lot finder | location-based parking

**Primary use cases:**
- Finding on-street parking spots within geographic boundaries
- Retrieving real-time occupancy data for parking garages
- Supporting mobile apps with parking availability information

**Compatibility:** Node.js 14+, Koa.js framework, MongoDB, Axios HTTP client

## ❓ Common Questions Quick Index

- **Q: How do I get parking spots in a specific area?** → [getOnStreetParkingLot Usage](#basic-usage)
- **Q: How do I check garage occupancy rates?** → [getGaragesOccupancy Usage](#garage-occupancy-retrieval)
- **Q: What happens when Smarking API is down?** → [Error Handling](#error-handling-mechanism)
- **Q: How do I configure authentication?** → [Configuration](#configuration-parameters)
- **Q: What data format does it return?** → [Output Examples](#output-examples)
- **Q: Can I query multiple garages at once?** → [Batch Operations](#batch-operations)
- **Q: How do I troubleshoot API errors?** → [Troubleshooting](#troubleshooting-steps)
- **Q: What are the performance considerations?** → [Performance](#performance-characteristics)
- **Q: How do I handle rate limiting?** → [Rate Limiting](#rate-limiting-considerations)
- **Q: What security measures are implemented?** → [Security](#security-considerations)

## 📋 Functionality Overview

**Non-technical explanation:** 
Think of this service as a parking meter reader that works across an entire city. Like a parking attendant who can instantly tell you which spots are available and how full each garage is, this module connects to Smarking's smart parking system to provide real-time parking information. It's similar to a restaurant reservation system that shows table availability, but for parking spaces across urban areas.

**Technical explanation:** 
A lightweight integration service that wraps Smarking's REST API v3 endpoints, providing geospatial queries for on-street parking using MongoDB and HTTP requests for garage occupancy data with Bearer token authentication and concurrent request handling.

**Business value:** Enables mobility applications to provide accurate, real-time parking information, reducing urban congestion and improving user experience by helping drivers find available parking quickly.

**System context:** Part of the TSP (Transportation Service Provider) API within the MaaS platform, specifically handling parking vendor integrations alongside other mobility services like ridehail and bike sharing.

## 🔧 Technical Specifications

**File information:**
- Name: smarking.js
- Path: /src/services/parking/smarking.js
- Language: JavaScript (Node.js)
- Type: Service module/integration layer
- File size: ~90 lines
- Complexity: Medium (external API integration with error handling)

**Dependencies:**
- `config`: Configuration management (critical) - v3.3.x
- `@maas/core/log`: Logging framework (critical) - proprietary
- `axios`: HTTP client (critical) - v0.27.x
- `@app/src/models/smarking`: MongoDB model (critical) - proprietary

**Compatibility matrix:**
- Node.js: 14.0+ (recommended: 18.0+)
- Smarking API: v3 (current)
- MongoDB: 4.4+ for geospatial queries

**Configuration parameters:**
```javascript
config.vendor.parking.smarking = {
  url: "https://api.smarking.net", // Base API URL
  auth: {
    token: "Bearer_token_here" // Required Bearer token
  }
}
```

## 📝 Detailed Code Analysis

**Main function signatures:**
```javascript
// Retrieves on-street parking within bounding box
async getOnStreetParkingLot(input) -> Array<SmarkingStation>
// Parameters: input.boundingBox (string) - "lng1,lat1,lng2,lat2"
// Returns: Array of parking station documents

// Gets garage occupancy data for single/multiple garages
async getGaragesOccupancy(input) -> Array<Object> | Object
// Parameters: input.ids (Array) OR input.id (string)
// Returns: Occupancy data with station_id and value
```

**Execution flow:**
1. **On-street parking**: Parse bounding box → Build MongoDB query → Execute geospatial search
2. **Garage occupancy**: Validate input → Build HTTP requests → Execute concurrent API calls → Filter results

**Design patterns:**
- **Service layer pattern**: Clean separation of external API concerns
- **Promise concurrency**: Batch API requests using Promise.all()
- **Error boundary**: Graceful degradation with error logging

**Error handling mechanism:**
- API failures return empty arrays instead of throwing
- Individual garage request failures don't affect batch operations
- Comprehensive logging for debugging third-party integration issues

## 🚀 Usage Methods

**Basic usage:**
```javascript
const { getOnStreetParkingLot, getGaragesOccupancy } = require('./smarking');

// Find on-street parking in downtown area
const boundingBox = "-122.42,37.77,-122.41,37.78"; // SF coordinates
const parkingSpots = await getOnStreetParkingLot({ boundingBox });

// Check single garage occupancy
const occupancy = await getGaragesOccupancy({ id: "garage_123" });

// Batch check multiple garages
const batchOccupancy = await getGaragesOccupancy({ 
  ids: ["garage_123", "garage_456", "garage_789"] 
});
```

**Environment-specific configurations:**
```javascript
// Development
config.vendor.parking.smarking.url = "https://api-staging.smarking.net";

// Production
config.vendor.parking.smarking.url = "https://api.smarking.net";
```

## 📊 Output Examples

**Successful on-street parking output:**
```javascript
[
  {
    _id: "507f1f77bcf86cd799439011",
    locationType: "on-street",
    latitude: 37.7749,
    longitude: -122.4194,
    address: "123 Market St",
    maxDuration: 120,
    rate: 2.50
  }
]
```

**Garage occupancy output:**
```javascript
// Single garage
{ station_id: "garage_123", value: 85 } // 85% occupied

// Multiple garages
[
  { station_id: "garage_123", value: 85 },
  { station_id: "garage_456", value: 42 },
  { station_id: "garage_789", value: 98 }
]
```

**Error scenarios:**
- API timeout: Returns `[]` (empty array)
- Invalid coordinates: Returns `[]` with MongoDB query error logged
- Authentication failure: Returns `[]` with 401 error logged

## ⚠️ Important Notes

**Security considerations:**
- Bearer token stored in configuration (ensure secure config management)
- No input sanitization on bounding box (validate coordinates before calling)
- API responses logged in debug mode (avoid logging sensitive data)

**Performance considerations:**
- Concurrent requests for batch garage queries improve response time
- MongoDB geospatial queries require proper indexing on latitude/longitude
- No request caching implemented (consider Redis for high-traffic scenarios)

**Common troubleshooting steps:**
1. **401 Unauthorized**: Check Bearer token validity and expiration
2. **Empty results**: Verify bounding box coordinates and garage IDs
3. **Slow responses**: Check network connectivity to Smarking API
4. **MongoDB errors**: Ensure SmarkingStation model schema matches query structure

## 🔗 Related File Links

**Project structure:**
- **Models**: `/src/models/smarking.js` - MongoDB schema definition
- **Configuration**: `/config/default.js` - API credentials and URLs
- **Controllers**: `/src/controllers/parking.js` - HTTP endpoint handlers
- **Tests**: `/test/services/parking/smarking.test.js` - Unit tests

**Dependencies:**
- **Core logging**: `@maas/core/log` - Centralized logging framework
- **Database models**: `@app/src/models/` - MongoDB ODM models

## 📈 Use Cases

**Daily usage scenarios:**
- **Mobile app users**: Finding nearby parking before reaching destination
- **Fleet managers**: Monitoring parking availability for delivery vehicles
- **Urban planners**: Analyzing parking utilization patterns

**Development scenarios:**
- **Integration testing**: Validating third-party API connectivity
- **Performance testing**: Load testing batch occupancy requests
- **Error simulation**: Testing graceful degradation during API outages

**Anti-patterns:**
- ❌ Don't call without authentication configuration
- ❌ Don't ignore error responses (empty arrays may indicate failures)
- ❌ Don't make individual requests when batch operations are available

## 🛠️ Improvement Suggestions

**Performance optimizations:**
- **Caching layer**: Implement Redis caching for occupancy data (TTL: 2-5 minutes)
- **Request pooling**: Use HTTP/2 keep-alive connections for better performance
- **Response compression**: Enable gzip compression for API responses

**Feature enhancements:**
- **Rate limiting**: Implement exponential backoff for failed requests
- **Data validation**: Add input sanitization for coordinates and garage IDs
- **Monitoring**: Add metrics collection for API response times and success rates

**Maintenance recommendations:**
- **Monthly**: Review API token expiration and rotation schedule
- **Quarterly**: Update dependencies and review Smarking API changes
- **Annually**: Performance analysis and optimization review

## 🏷️ Document Tags

**Keywords:** smarking, parking-api, real-time-occupancy, on-street-parking, garage-availability, mongodb-geospatial, third-party-integration, maas-platform, mobility-services, location-based-services, parking-finder, urban-mobility, transportation-api, bearer-authentication, concurrent-requests

**Technical tags:** #parking-service #third-party-api #mongodb #axios #real-time-data #geospatial-query #maas-integration #koa-service

**Target roles:** Backend developers (intermediate), Integration engineers (advanced), Mobile app developers (basic), DevOps engineers (basic)

**Difficulty level:** ⭐⭐⭐ (3/5) - Requires understanding of async/await, MongoDB queries, HTTP client usage, and error handling patterns

**Maintenance level:** Medium - Requires monitoring of third-party API changes and token management

**Business criticality:** Medium - Important for parking features but not core system functionality

**Related topics:** RESTful APIs, geospatial databases, concurrent programming, authentication patterns, error handling strategies, mobile backend services