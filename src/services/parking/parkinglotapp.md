# ParkingLotApp Service Documentation

## 🔍 Quick Summary (TL;DR)
ParkingLotApp service integrates with third-party parking lot data providers to fetch off-street parking information based on location and user preferences, enabling real-time parking availability searches for MaaS applications.

**Keywords:** parking | off-street | parkinglot | location-based | oauth | vendor-integration | mobility | radius-search | bounding-box | preference-filtering | taiwan-parking | third-party-api

**Primary Use Cases:**
- Find nearby parking lots within specified radius or bounding box
- Filter parking results by user preferences (price, operator, distance)
- Authenticate with ParkingLotApp vendor API using OAuth2 client credentials

**Compatibility:** Node.js 14+, Koa.js framework, Axios HTTP client

## ❓ Common Questions Quick Index
- **Q: How do I find parking lots near a location?** → [Usage Methods](#usage-methods)
- **Q: What user preferences can filter parking results?** → [Detailed Code Analysis](#detailed-code-analysis)
- **Q: How does OAuth authentication work with the vendor?** → [Technical Specifications](#technical-specifications)
- **Q: What parking operators are supported?** → [Output Examples](#output-examples)
- **Q: How to troubleshoot 401 authentication errors?** → [Important Notes](#important-notes)
- **Q: What's the maximum search radius allowed?** → [Usage Methods](#usage-methods)
- **Q: How are parking prices filtered?** → [Detailed Code Analysis](#detailed-code-analysis)
- **Q: What if the vendor API is down?** → [Important Notes](#important-notes)
- **Q: How to optimize search performance?** → [Improvement Suggestions](#improvement-suggestions)
- **Q: What data format does the API return?** → [Output Examples](#output-examples)

## 📋 Functionality Overview
**Non-technical:** Like a smart parking finder app that remembers your preferences - if you prefer cheaper lots under $5/hour within walking distance, it filters out expensive or distant options. It's like having a personal parking assistant that knows Taiwan's major parking operators (嘟嘟房, Times, 聯通) and can find government vs. private lots based on your needs.

**Technical:** OAuth2-authenticated HTTP service client that queries ParkingLotApp vendor API for geospatial parking data with user preference filtering, implementing automatic token refresh and configurable search parameters.

**Business Value:** Enables seamless parking discovery within MaaS platforms, improving user experience by providing personalized parking recommendations and reducing time spent searching for suitable parking spots.

**System Context:** Part of TSP-API's parking services ecosystem, integrating vendor data with internal user preference management to provide unified parking search capabilities.

## 🔧 Technical Specifications
- **File:** parkinglotapp.js (192 lines, Medium complexity)
- **Path:** /src/services/parking/parkinglotapp.js
- **Language:** JavaScript (Node.js)
- **Dependencies:**
  - `config` (Critical) - Application configuration management
  - `@maas/core/log` (Critical) - Structured logging framework
  - `axios` (Critical) - HTTP client for API requests
  - `@app/src/models/Preference` (High) - User preference data model
- **Environment Variables:**
  - `vendor.parking.parkinglotapp.url` - API base URL
  - `vendor.parking.parkinglotapp.auth.client_id` - OAuth client ID
  - `vendor.parking.parkinglotapp.auth.client_secret` - OAuth client secret
- **System Requirements:**
  - Node.js 14+ with ES6 module support
  - Network access to vendor API endpoints
  - Database access for user preferences

## 📝 Detailed Code Analysis
**Main Functions:**
```javascript
// OAuth2 token acquisition with client credentials flow
async getAuthorization() → Promise<string>

// Location-based parking search with preference filtering  
async getOffStreetParkingLot(input) → Promise<Array<ParkingLot>>
```

**Execution Flow:**
1. Request interceptor adds OAuth bearer token to all API calls
2. Response interceptor handles 401 errors with automatic token refresh
3. `getOffStreetParkingLot` fetches user preferences from database
4. Constructs query parameters (location, radius/bounding box, filters)
5. Makes authenticated API request to vendor
6. Applies client-side preference filtering (operator keywords, price limits)

**Key Patterns:**
- **Interceptor Pattern:** Automatic authentication handling with retry logic
- **Strategy Pattern:** Multiple search modes (radius vs bounding box)
- **Filter Pattern:** Configurable operator and price filtering

**Error Handling:** Graceful degradation with empty array return on API failures, automatic 401 retry with token refresh.

## 🚀 Usage Methods
**Basic Search by Coordinates:**
```javascript
const parkingService = require('./parkinglotapp');

// Search within 1600m radius (default)
const result = await parkingService.getOffStreetParkingLot({
  lat: 25.0330,
  lng: 121.5654,
  userId: 'user123',
  radius: 1600
});
```

**Bounding Box Search:**
```javascript
// Search within specific geographic bounds
const result = await parkingService.getOffStreetParkingLot({
  lat: 25.0330,
  lng: 121.5654,
  userId: 'user123',
  boundingBox: 'sw_lat,sw_lng,ne_lat,ne_lng'
});
```

**Configuration Requirements:**
- Maximum radius: 1600 meters (enforced by service)
- User preferences stored in database with JSON structure
- OAuth credentials must be configured in vendor.parking.parkinglotapp config

## 📊 Output Examples
**Successful Response:**
```json
[
  {
    "id": "lot_001",
    "name": "嘟嘟房台北車站停車場",
    "lat": 25.0478,
    "lng": 121.5170,
    "price": 30,
    "distance": 450,
    "operator": "嘟嘟房",
    "availability": 25
  }
]
```

**Empty Results (No parking found):**
```json
[]
```

**Supported Parking Operators:**
- Type 1: 特約 (Contract parking)
- Type 2: 公有/公共 (Public parking)
- Type 3: 嘟嘟房 (DuDuFang)
- Type 4: 聯通 (Taiwan Unicom)
- Type 5: Times (Times Parking)
- Type 6: 詮營 (Quan Ying)
- Type 7: 歐特儀 (Auto Meter)
- Type 8: 博客 (Blogger)

## ⚠️ Important Notes
**Security Considerations:**
- OAuth tokens stored in memory only, not persisted
- Client credentials must be secured in environment configuration
- API requests include client UID for request tracking

**Troubleshooting 401 Errors:**
1. Check client_id and client_secret configuration
2. Verify network connectivity to OAuth endpoint
3. Confirm vendor API scope permissions (third-party-app parking-sections)

**Performance Gotchas:**
- Default 1600m radius enforced to prevent excessive data transfer
- User preference queries executed on every search (consider caching)
- Synchronous preference filtering may impact performance with large result sets

**Rate Limiting:** Vendor API may impose rate limits; implement request throttling for high-volume usage.

## 🔗 Related File Links
**Dependencies:**
- `/src/models/Preference.js` - User parking preference data model
- `/config/default.js` - Vendor API configuration
- `@maas/core/log` - Logging framework configuration

**Related Services:**
- `/src/services/parking/` - Other parking service integrations
- `/src/controllers/parking.js` - Parking API endpoints
- `/src/middleware/auth.js` - User authentication middleware

## 📈 Use Cases
**Daily Operations:**
- Mobile app users searching for nearby parking before driving
- Integration with navigation systems for parking-aware routing
- Real-time parking availability checks during peak hours

**Development Integration:**
- Parking service aggregation with multiple vendor APIs
- User preference learning and recommendation systems
- Location-based service optimization

**Scaling Scenarios:**
- High-traffic periods require caching and rate limiting
- Multi-city expansion needs vendor API regional configuration
- Real-time updates require webhook or polling mechanisms

## 🛠️ Improvement Suggestions
**Performance Optimization:**
- Implement Redis caching for user preferences (reduce database queries by 80%)
- Add request deduplication for identical location searches
- Implement parallel vendor API calls for comprehensive coverage

**Feature Enhancements:**
- Add parking lot booking/reservation capabilities
- Implement real-time availability polling
- Add walking time calculation from destination

**Code Quality:**
- Extract operator keyword matching to configuration file
- Add input validation for coordinates and search parameters
- Implement circuit breaker pattern for vendor API resilience

## 🏷️ Document Tags
**Keywords:** parking-lot-app, oauth2-client, vendor-integration, location-based-search, preference-filtering, axios-interceptors, taiwan-parking, off-street-parking, geospatial-query, client-credentials, parking-operators, radius-search, bounding-box-search, automatic-retry, token-refresh

**Technical Tags:** #parking-service #vendor-api #oauth2 #geospatial #koa-service #taiwan #preference-filter #location-search

**Target Roles:** Backend developers (intermediate), MaaS platform engineers, Parking system integrators

**Difficulty Level:** ⭐⭐⭐ (Moderate - requires understanding of OAuth2, geospatial concepts, and vendor API integration patterns)

**Maintenance Level:** Medium (OAuth credentials rotation, vendor API changes, preference schema updates)

**Business Criticality:** High (Core parking discovery functionality for end users)

**Related Topics:** Vendor API integration, Geospatial services, User preference management, Authentication patterns, Taiwan parking ecosystem