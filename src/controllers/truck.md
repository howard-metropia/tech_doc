# TSP API Truck Controller Documentation

## 🔍 Quick Summary (TL;DR)
The truck controller provides truck routing map data and road restrictions information for commercial vehicle navigation and route planning.

**Keywords:** truck-routing | commercial-vehicles | truck-restrictions | road-limitations | freight-navigation | commercial-routing | truck-maps | vehicle-restrictions

**Primary use cases:** Retrieving truck-specific map data, accessing commercial vehicle road restrictions, supporting freight route planning, providing truck navigation services

**Compatibility:** Node.js >= 16.0.0, Koa.js v2.x, truck routing services

## ❓ Common Questions Quick Index
- **Q: What is truck map data?** → Road restrictions and routing information for commercial vehicles
- **Q: How is data freshness handled?** → Uses last_modified parameter for incremental updates
- **Q: What truck restrictions are included?** → Height, weight, length, and hazmat restrictions
- **Q: Is authentication required?** → Yes, JWT authentication required
- **Q: How often is data updated?** → Based on service implementation and data sources
- **Q: Are different truck types supported?** → Yes, based on service configuration

## 📋 Functionality Overview

**Non-technical explanation:** 
Think of this as a **specialized GPS service for trucks**. Regular cars can drive on most roads, but trucks have special rules - they can't go under low bridges, on roads with weight limits, or in certain areas. This controller provides all that special truck information so truck drivers can plan safe and legal routes without getting stuck or fined.

**Technical explanation:** 
A lightweight Koa.js REST controller that serves truck-specific routing and restriction data. It provides incremental map updates based on modification timestamps and integrates with truck routing services to deliver commercial vehicle navigation data including road restrictions, weight limits, and route constraints.

**Business value explanation:**
Essential for freight and logistics operations, enabling safe and compliant commercial vehicle routing. Reduces violations, improves delivery efficiency, and supports logistics optimization by providing accurate truck-specific navigation data for route planning and fleet management systems.

## 🔧 Technical Specifications

- **File:** `allrepo/connectsmart/tsp-api/src/controllers/truck.js`
- **Language:** JavaScript (ES2020)
- **Framework:** Koa.js v2.x with @koa/router
- **Type:** Truck Routing Data Controller
- **File Size:** ~0.5 KB
- **Complexity Score:** ⭐ (Low - Single endpoint with service delegation)

**Dependencies:**
- `@koa/router`: HTTP routing framework (**Critical**)
- `koa-bodyparser`: Request body parsing (**Critical**)
- `@app/src/middlewares/auth`: JWT authentication (**Critical**)
- `@maas/core/response`: Standardized response formatting (**High**)
- `../services/truckService`: Truck mapping service (**Critical**)
- `../schemas/truckJoiSchema`: Input validation schemas (**Critical**)

## 📝 Detailed Code Analysis

### Truck Map Endpoint (`GET /truck/map`)

**Purpose:** Retrieves the latest truck routing map data with incremental update support

**Processing Flow:**
1. **Authentication:** JWT validation via auth middleware
2. **Parameter Validation:** Validates query string parameters (last_modified)
3. **Service Call:** Requests latest truck map data from service
4. **Response:** Returns truck routing data in standardized format

**Incremental Updates:**
```javascript
const { last_modified: lastModified } = 
  await validateQueryStringParams.validateAsync({
    ...ctx.query,
  });
const latestTruckMap = await truckMapService.getLatestTruckMap(lastModified);
```

**Service Pattern:**
- **Instantiation:** Creates TruckMapService instance
- **Method Call:** Delegates to getLatestTruckMap method
- **Caching:** Service handles data caching and freshness

## 🚀 Usage Methods

### Get Latest Truck Map Data
```bash
curl -X GET "https://api.tsp.example.com/api/v2/truck/map" \
  -H "Authorization: Bearer <JWT_TOKEN>"
```

### Get Incremental Updates
```bash
curl -X GET "https://api.tsp.example.com/api/v2/truck/map?last_modified=2024-06-20T10:30:00Z" \
  -H "Authorization: Bearer <JWT_TOKEN>"
```

### Check for Updates with Timestamp
```bash
curl -X GET "https://api.tsp.example.com/api/v2/truck/map?last_modified=1719331200" \
  -H "Authorization: Bearer <JWT_TOKEN>"
```

### JavaScript Client Example
```javascript
async function getTruckMapData(authToken, lastModified = null) {
  let url = '/api/v2/truck/map';
  
  if (lastModified) {
    const timestamp = typeof lastModified === 'string' 
      ? lastModified 
      : new Date(lastModified).toISOString();
    url += `?last_modified=${encodeURIComponent(timestamp)}`;
  }

  try {
    const response = await fetch(url, {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${authToken}`,
        'Content-Type': 'application/json'
      }
    });
    
    const result = await response.json();
    
    if (result.result === 'success') {
      console.log('Truck map data retrieved:', result.data);
      return result.data;
    } else {
      console.error('Failed to get truck map data:', result.error);
      throw new Error(result.error);
    }
  } catch (error) {
    console.error('Truck map request error:', error);
    throw error;
  }
}

// Usage examples
getTruckMapData(token); // Get full dataset

getTruckMapData(token, '2024-06-20T10:30:00Z'); // Get updates since timestamp

getTruckMapData(token, new Date('2024-06-20')); // Get updates since date
```

## 📊 Output Examples

### Full Truck Map Data
```json
{
  "result": "success",
  "data": {
    "last_modified": "2024-06-25T14:30:00Z",
    "version": "2024.06.25",
    "restrictions": [
      {
        "road_id": "highway_101_north",
        "restriction_type": "weight_limit",
        "max_weight_tons": 40,
        "coordinates": [
          {"lat": 37.7749, "lng": -122.4194},
          {"lat": 37.7849, "lng": -122.4094}
        ]
      },
      {
        "road_id": "bridge_golden_gate",
        "restriction_type": "height_limit",
        "max_height_meters": 4.2,
        "coordinates": [
          {"lat": 37.8199, "lng": -122.4783}
        ]
      }
    ],
    "truck_routes": [
      {
        "route_id": "truck_route_001",
        "name": "Commercial Corridor",
        "allowed_vehicles": ["truck", "delivery", "freight"],
        "restrictions": {
          "max_length_meters": 18.3,
          "max_width_meters": 2.6,
          "hazmat_allowed": false
        }
      }
    ],
    "prohibited_areas": [
      {
        "area_id": "downtown_core",
        "name": "Downtown Restricted Zone",
        "coordinates": [
          {"lat": 37.7749, "lng": -122.4194},
          {"lat": 37.7849, "lng": -122.4094},
          {"lat": 37.7849, "lng": -122.4294},
          {"lat": 37.7749, "lng": -122.4394}
        ],
        "time_restrictions": [
          {
            "days": ["monday", "tuesday", "wednesday", "thursday", "friday"],
            "start_time": "07:00",
            "end_time": "19:00"
          }
        ]
      }
    ]
  }
}
```

### Incremental Update Response
```json
{
  "result": "success",
  "data": {
    "last_modified": "2024-06-25T14:30:00Z",
    "has_updates": true,
    "updated_restrictions": [
      {
        "road_id": "highway_280_south",
        "restriction_type": "temporary_closure",
        "effective_from": "2024-06-25T06:00:00Z",
        "effective_until": "2024-06-25T18:00:00Z",
        "reason": "construction"
      }
    ],
    "removed_restrictions": [
      "temp_restriction_001"
    ]
  }
}
```

### No Updates Available
```json
{
  "result": "success",
  "data": {
    "last_modified": "2024-06-25T14:30:00Z",
    "has_updates": false,
    "message": "No updates available since last check"
  }
}
```

### Validation Error
```json
{
  "error": "ValidationError",
  "message": "Invalid query parameters",
  "details": [
    {
      "field": "last_modified",
      "message": "last_modified must be a valid ISO date string or Unix timestamp"
    }
  ]
}
```

## ⚠️ Important Notes

### Truck Restriction Types
Common restriction categories included:
- **Weight Limits:** Maximum gross vehicle weight allowed
- **Height Clearances:** Bridge and overpass height restrictions
- **Length Restrictions:** Maximum vehicle length limits
- **Width Limits:** Road width constraints for oversized vehicles
- **Hazmat Restrictions:** Hazardous material transportation limits
- **Time Restrictions:** Time-based access limitations
- **Seasonal Restrictions:** Weather or seasonal access limits

### Data Freshness Management
- **Incremental Updates:** Only returns changes since last_modified timestamp
- **Timestamp Formats:** Supports ISO 8601 strings and Unix timestamps
- **Version Control:** Data includes version information for tracking
- **Cache Efficiency:** Reduces bandwidth with incremental updates

### Truck Route Planning
Key features for commercial vehicle routing:
- **Designated Truck Routes:** Pre-approved commercial corridors
- **Prohibited Areas:** Zones where trucks are restricted
- **Time-based Restrictions:** Rush hour or business hour limitations
- **Vehicle Type Specific:** Different rules for different truck types

### Authentication and Security
- **JWT Required:** All requests must include valid authentication
- **User Context:** May track which users access truck data
- **Rate Limiting:** May implement limits on data requests
- **Data Access:** Controls which users can access truck routing data

### Service Integration
- **External Data Sources:** May integrate with DOT and mapping providers
- **Real-time Updates:** Supports dynamic restriction updates
- **Multi-region Support:** Can handle different geographical areas
- **Data Validation:** Ensures restriction data accuracy

### Performance Considerations
- **Caching Strategy:** Service implements efficient data caching
- **Incremental Loading:** Reduces data transfer with timestamp filtering
- **Compression:** Large datasets may be compressed
- **CDN Distribution:** Map data may be distributed via CDN

### Use Cases
- **Fleet Management:** Route planning for commercial fleets
- **Logistics Optimization:** Efficient freight route calculation
- **Compliance Management:** Ensuring regulatory compliance
- **Navigation Apps:** Truck-specific GPS navigation
- **Load Planning:** Vehicle selection based on route restrictions

## 🔗 Related File Links

- **Truck Service:** `allrepo/connectsmart/tsp-api/src/services/truckService.js`
- **Validation Schema:** `allrepo/connectsmart/tsp-api/src/schemas/truckJoiSchema.js`
- **Authentication:** `allrepo/connectsmart/tsp-api/src/middlewares/auth.js`
- **Related Controllers:** Route planning and mapping controllers

---
*This controller provides essential truck routing data for commercial vehicle navigation and compliance management.*