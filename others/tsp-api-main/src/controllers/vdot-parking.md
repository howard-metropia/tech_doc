# TSP API VDOT Parking Controller Documentation

## 🔍 Quick Summary (TL;DR)
The VDOT parking controller provides comprehensive parking lot information by combining INRIX real-time parking data with Virginia Department of Transportation (VDOT) parking stations for enhanced parking availability and location services.

**Keywords:** vdot-parking | inrix-parking | parking-availability | real-time-parking | parking-lots | off-street-parking | parking-occupancy | location-based-parking

**Primary use cases:** Finding available parking spaces, retrieving real-time parking occupancy, locating parking lots near destinations, integration with VDOT parking infrastructure

**Compatibility:** Node.js >= 16.0.0, Koa.js v2.x, INRIX API, VDOT parking systems, MongoDB

## ❓ Common Questions Quick Index
- **Q: What parking data sources are used?** → INRIX real-time data and VDOT parking stations
- **Q: How is parking availability calculated?** → Based on total spaces minus occupied spaces
- **Q: What geographic filtering is supported?** → Latitude/longitude with radius and bounding box
- **Q: Are parking rates included?** → Yes, fare descriptions and rate information
- **Q: How is data quality monitored?** → Automated validation with Slack alerts for poor data
- **Q: What parking types are supported?** → Off-street lots, surface parking, structures, subterranean

## 📋 Functionality Overview

**Non-technical explanation:** 
Think of this as a **smart parking finder** that knows about parking lots in real-time. It combines information from multiple sources - like live parking space counts from sensors and official parking facility data from the Virginia Department of Transportation. When you need to park somewhere, it can tell you exactly how many spaces are available, what it costs, and where to find it.

**Technical explanation:** 
A comprehensive Koa.js controller that aggregates parking data from INRIX real-time parking services and VDOT parking station databases. It performs geographic filtering, calculates occupancy rates, validates data quality, and provides standardized parking lot information with availability, pricing, and facility details.

**Business value explanation:**
Essential for smart city initiatives and transportation planning. Reduces traffic congestion by helping drivers find parking efficiently, supports urban mobility planning, enables parking optimization strategies, and provides valuable analytics for transportation authorities and parking management companies.

## 🔧 Technical Specifications

- **File:** `allrepo/connectsmart/tsp-api/src/controllers/vdot-parking.js`
- **Language:** JavaScript (ES2020)
- **Framework:** Koa.js v2.x with @koa/router
- **Type:** Parking Data Aggregation Controller
- **File Size:** ~6.0 KB
- **Complexity Score:** ⭐⭐⭐⭐ (High - Multi-source data aggregation with complex processing)

**Dependencies:**
- `moment-timezone`: Date/time handling (**High**)
- `@koa/router`: HTTP routing framework (**Critical**)
- `@maas/core/log`: Logging infrastructure (**High**)
- `@app/src/middlewares/auth`: JWT authentication (**Critical**)
- `@app/src/services/parking`: INRIX parking service integration (**Critical**)
- `@app/src/services/response`: Response formatting (**High**)
- `@app/src/services/dataAccuracySlackWarning`: Data quality monitoring (**High**)
- `@app/src/models/ParkingStation`: VDOT parking station model (**Critical**)

## 📝 Detailed Code Analysis

### VDOT Parking Endpoint (`GET /vdot-parking`)

**Purpose:** Retrieves comprehensive parking information by combining INRIX and VDOT data sources

**Required Parameters:**
- `lat`: Latitude coordinate
- `lng`: Longitude coordinate  
- `radius`: Search radius
- `bounding_box`: Geographic boundary (format: "lng1,lat1,lng2,lat2")

**Processing Flow:**
1. **Parameter Validation:** Validates required location and boundary parameters
2. **Authentication Check:** Ensures valid user ID in headers
3. **INRIX Data Retrieval:** Fetches real-time off-street parking data
4. **Data Processing:** Transforms INRIX data to standardized format
5. **VDOT Data Integration:** Adds VDOT parking stations not covered by INRIX
6. **Quality Validation:** Checks data accuracy and sends alerts if needed
7. **Response Assembly:** Returns combined parking lot information

### INRIX Data Processing
```javascript
const inrixParkingLot = await ParkingService.inrix.getOffStreetParkingLot({
  lat, lng, boundingBox, radius
});

await Promise.all(
  inrixParkingLot.map(async (elem) => {
    const obj = {
      availableLots: elem.occupancy?.available || -1,
      usedLots: elem.spacesTotal - (elem.occupancy?.available || 0)
    };
    
    const inrixData = {
      parkinglot_uid: elem.id.toString(),
      name: elem.name,
      total_lots: elem.spacesTotal,
      available_lots: obj.availableLots,
      status: getOpenStatus(elem.isOpen, elem.spacesTotal, obj.availableLots),
      space_type: getSpaceType(elem.format),
      // ... additional fields
    };
    offStreet.push(inrixData);
  })
);
```

### VDOT Data Integration
```javascript
const vdotParkingData = await getVdotData({lat, lng, boundingBox, radius});

vdotParkingData.forEach((station) => {
  if (station.inrix_lot_id === '') { // Only add if not already in INRIX
    const occupancy = calculateOccupancy(station);
    const tempObj = {
      parkinglot_uid: station.parking_lot_id,
      name: station.name,
      available_lots: station.free_spaces,
      total_lots: station.total_spaces,
      status: getStatus(occupancy),
      // ... additional fields
    };
    offStreet.push(tempObj);
  }
});
```

### Data Quality Validation
```javascript
const dataAccuracyValidation = (parkingLotData) => {
  if (parkingLotData.length > 10) {
    let poorDataCount = 0;
    parkingLotData.forEach((data) => {
      if (data.available_lots === -1) {
        poorDataCount++;
      }
    });
    return (poorDataCount / parkingLotData.length) <= 0.9;
  }
  return true;
};
```

## 🚀 Usage Methods

### Basic Parking Search
```bash
curl -X GET "https://api.tsp.example.com/api/v2/vdot-parking?lat=38.9072&lng=-77.0369&radius=1000&bounding_box=-77.0469,38.8972,-77.0269,38.9172" \
  -H "Authorization: Bearer <JWT_TOKEN>" \
  -H "userid: usr_12345"
```

### Downtown Area Parking Search
```bash
curl -X GET "https://api.tsp.example.com/api/v2/vdot-parking?lat=38.8951&lng=-77.0364&radius=2000&bounding_box=-77.0564,38.8751,-77.0164,38.9151" \
  -H "Authorization: Bearer <JWT_TOKEN>" \
  -H "userid: usr_12345"
```

### JavaScript Client Example
```javascript
async function findParking(authToken, userId, location, radiusMeters = 1000) {
  // Calculate bounding box (simplified)
  const lat = location.latitude;
  const lng = location.longitude;
  const offset = radiusMeters / 111000; // Rough conversion to degrees
  
  const boundingBox = [
    lng - offset, // min lng
    lat - offset, // min lat  
    lng + offset, // max lng
    lat + offset  // max lat
  ].join(',');

  const params = new URLSearchParams({
    lat: lat,
    lng: lng,
    radius: radiusMeters,
    bounding_box: boundingBox
  });

  try {
    const response = await fetch(`/api/v2/vdot-parking?${params}`, {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${authToken}`,
        'userid': userId
      }
    });
    
    const result = await response.json();
    
    if (result.result === 'success') {
      console.log(`Found ${result.data.parking_lot.length} parking lots`);
      return {
        offStreet: result.data.parking_lot,
        onStreet: result.data.on_street
      };
    } else {
      console.error('Parking search failed:', result.error);
      throw new Error(result.error);
    }
  } catch (error) {
    console.error('Parking search error:', error);
    throw error;
  }
}

// Usage examples
findParking(token, 'usr_12345', {
  latitude: 38.9072,
  longitude: -77.0369
}, 1500);

// Find parking near specific address
findParking(token, 'usr_12345', {
  latitude: 38.8951, // White House area
  longitude: -77.0364
}, 500);
```

## 📊 Output Examples

### Successful Parking Search Response
```json
{
  "result": "success",
  "data": {
    "parking_lot": [
      {
        "price": -1,
        "parkinglot_uid": "inrix_12345",
        "name": "Downtown Parking Garage",
        "address": "123 Main St. Washington, DC 20001, US",
        "image": "https://parking-photos.example.com/garage123.jpg",
        "total_lots": 250,
        "available_lots": 47,
        "used_lots": 203,
        "status": 1,
        "space_type": "plane",
        "lat": 38.9072,
        "lng": -77.0369,
        "service_time": "Mon-Fri: 6:00 AM - 10:00 PM",
        "fare": -1,
        "fare_category": "per_unit",
        "fare_limit": 0,
        "fare_desc": "$2.50/hour weekdays\n$1.50/hour evenings\n$5.00 daily maximum",
        "tel": "+1-202-555-0123",
        "height_limit": "6'8\"",
        "note": "Covered parking available",
        "rate": 19
      },
      {
        "price": -1,
        "parkinglot_uid": "vdot_67890",
        "name": "Metro Station Parking",
        "address": "456 Transit Way, Arlington, VA 22202",
        "image": "",
        "total_lots": 180,
        "available_lots": 12,
        "used_lots": 168,
        "status": 1,
        "space_type": "tower",
        "lat": 38.8977,
        "lng": -77.0365,
        "service_time": "24/7",
        "fare": -1,
        "fare_category": "",
        "fare_limit": 0,
        "fare_desc": "$4.95 all day",
        "tel": "",
        "height_limit": "",
        "note": "",
        "rate": 93
      }
    ],
    "on_street": []
  }
}
```

### Error Responses

**Missing Parameters:**
```json
{
  "error": "ERROR_BAD_REQUEST_PARAMS",
  "message": "Required parameters missing",
  "code": 400
}
```

**Missing User ID:**
```json
{
  "error": "ERROR_BAD_REQUEST_HEADER_USER_ID",
  "message": "User ID required in headers",
  "code": 400
}
```

## ⚠️ Important Notes

### Parking Status Codes
- **1**: Open with available spaces (total > 0, available > 0)
- **2**: Open but full (total > 0, available = 0) 
- **3**: Open with unknown availability (no data)
- **4**: Closed
- **5**: Unknown status

### Space Types
- **plane**: Indoor/covered parking (Structure, Subterranean)
- **tower**: Outdoor surface parking (Surface)
- **other**: Default/unknown type

### Data Sources

**INRIX Real-time Data:**
- Live occupancy information
- Rate card details
- Operating hours
- Photo thumbnails
- Navigation addresses

**VDOT Parking Stations:**
- Government parking facilities
- Real-time space counts
- Cost information
- Contact details
- Facility specifications

### Data Quality Monitoring
- **Validation Threshold:** Flags if >90% of lots have no availability data
- **Slack Alerts:** Automatically notifies team of data quality issues
- **Minimum Dataset:** Only validates when >10 parking lots returned
- **Accuracy Metrics:** Tracks percentage of lots with real-time data

### Geographic Filtering
- **Bounding Box:** Format "lng1,lat1,lng2,lat2" 
- **Radius:** Search radius in meters
- **Coordinate System:** WGS84 (standard GPS coordinates)
- **Performance:** MongoDB geospatial queries for VDOT data

### Rate Information
- **Dynamic Pricing:** Some lots have time-based rates
- **Rate Cards:** Detailed pricing structures from INRIX
- **Cost Descriptions:** Human-readable fare information
- **Currency:** Assumed USD (no currency field)

### Integration Considerations
- **Deduplication:** VDOT lots already in INRIX are excluded
- **Data Freshness:** INRIX provides real-time updates
- **Fallback Data:** VDOT provides coverage where INRIX unavailable
- **Performance:** Parallel processing of data sources

## 🔗 Related File Links

- **Parking Service:** `allrepo/connectsmart/tsp-api/src/services/parking.js`
- **Parking Station Model:** `allrepo/connectsmart/tsp-api/src/models/ParkingStation.js`
- **Response Service:** `allrepo/connectsmart/tsp-api/src/services/response.js`
- **Data Quality Service:** `allrepo/connectsmart/tsp-api/src/services/dataAccuracySlackWarning.js`
- **Error Codes:** `allrepo/connectsmart/tsp-api/src/static/error-code.js`

---
*This controller provides comprehensive parking information by combining real-time commercial data with government parking infrastructure for optimal parking discovery.*