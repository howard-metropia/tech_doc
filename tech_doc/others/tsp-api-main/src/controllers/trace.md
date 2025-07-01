# TSP API Trace Controller Documentation

## 🔍 Quick Summary (TL;DR)
The trace controller manages trip tracking, trajectory data collection, user location visits, ETA updates, and trip validation for comprehensive mobility analytics and real-time trip monitoring.

**Keywords:** trip-tracking | trajectory-data | location-tracking | eta-updates | trip-validation | mobility-analytics | gps-trace | carpool-management

**Primary use cases:** Recording trip trajectories, tracking user visits to locations, managing ETA changes for carpools, validating completed trips, collecting mobility data

**Compatibility:** Node.js >= 16.0.0, Koa.js v2.x, MySQL, MongoDB, compressed data support

## ❓ Common Questions Quick Index
- **Q: What data compression is supported?** → GZIP and ZIP compression for trajectory data
- **Q: How are carpool ETAs managed?** → Only drivers can update ETAs for carpool trips
- **Q: What happens when a trip is completed?** → Automatic trip validation is triggered
- **Q: Can passengers update trip ETAs?** → No, only drivers can update carpool trip ETAs
- **Q: How is location data stored?** → GPS coordinates with arrival/departure timestamps
- **Q: What trip validation rules exist?** → Speed, route adherence, and completion percentage checks

## 📋 Functionality Overview

**Non-technical explanation:** 
Think of this as a **comprehensive trip recorder** that tracks everything about your journey. It's like having a smart GPS that not only knows where you are, but also records your exact path, remembers the places you visit, and can even help coordinate with other people if you're carpooling. It keeps track of when you arrive and leave places, and makes sure your trips actually happened as planned.

**Technical explanation:** 
A sophisticated Koa.js controller that handles real-time trip tracking with compressed trajectory data ingestion, location visit recording, ETA management for carpool coordination, and automated trip validation. Integrates with both MySQL and MongoDB for comprehensive trip data management and supports role-based permissions for carpool participants.

**Business value explanation:**
Critical for mobility analytics, trip verification, and carpool coordination. Enables accurate mileage tracking, route optimization, carpool reliability, and data-driven insights for transportation planning. Supports compliance requirements and provides real-time coordination for shared mobility services.

## 🔧 Technical Specifications

- **File:** `allrepo/connectsmart/tsp-api/src/controllers/trace.js`
- **Language:** JavaScript (ES2020)
- **Framework:** Koa.js v2.x with @koa/router
- **Type:** Trip Tracking & Analytics Controller
- **File Size:** ~7.0 KB
- **Complexity Score:** ⭐⭐⭐⭐ (High - Multi-database operations, compression handling, role-based logic)

**Dependencies:**
- `@koa/router`: HTTP routing framework (**Critical**)
- `zlib`: Data compression/decompression (**Critical**)
- `raw-body`: Raw request body parsing (**Critical**)
- `@app/src/models/*`: Database models for trips, trajectories, visits (**Critical**)
- `@app/src/services/trip`: Trip validation service (**Critical**)
- `@maas/core/services/database`: MongoDB connection (**High**)
- `moment-timezone`: Date/time handling (**High**)
- `@app/src/middlewares/auth`: JWT authentication (**Critical**)

## 📝 Detailed Code Analysis

### Trip Trajectory Endpoint (`POST /trip_trajectory`)

**Purpose:** Records compressed GPS trajectory data for active trips

**Processing Flow:**
1. **Raw Data Extraction:** Gets compressed binary data from request
2. **Decompression:** Supports both GZIP and ZIP compression formats
3. **Data Processing:** Parses JSON and adds user context
4. **Storage:** Creates trajectory record in database
5. **Distance Update:** Updates trip with maximum recorded distance
6. **Completion Check:** Triggers validation if trip is marked complete

**Compression Handling:**
```javascript
const decompressed = ctx.is('application/gzip')
  ? gunzipSync(body)
  : unzipSync(body);
const data = JSON.parse(decompressed);
```

**Distance Tracking:**
```javascript
const distance = Math.max(...data.trajectory.map((o) => o.distance ?? 0));
await Trips.query()
  .where('id', data.trip_id)
  .andWhere((queryBuilder) => {
    queryBuilder.where('distance', '<', distance).orWhereNull('distance');
  })
  .patch({ distance });
```

### User Visit Endpoint (`POST /user_visit`)

**Purpose:** Records user visits to specific locations with timestamps

**Data Structure:**
- User ID and coordinates
- Arrival and departure timestamps
- Operating system type
- Validation via schema

**Processing:**
```javascript
const record = {
  user_id: userid,
  arrival_date: value.arrival_date.getTime(),
  departure_date: value.departure_date.getTime(),
  longitude: value.longitude,
  latitude: value.latitude,
  os_type: value.os_type,
};
```

### ETA Changes Endpoint (`POST /eta_change/:trip_id`)

**Purpose:** Manages ETA updates with carpool role-based permissions

**Role Verification Logic:**

**Scheduled Carpool (DUO):**
```javascript
const reservation = await DuoReservations.query()
  .where('reservation_id', trip.reservation_id)
  .first();
if (reservation && reservation.role === 1) { // 1 = driver
  isDriver = true;
}
```

**Instant Carpool:**
```javascript
const carpoolData = await carpoolCollection.findOne({ 
  "driver.tripId": trip.id 
});
if (carpoolData) {
  isDriver = true;
}
```

**Timer Management:**
```javascript
const timerId = setTimeout(async () => {
  await validateTrip(trip_id);
}, (timestamp - Math.floor(Date.now() / 1000)) * 1000);
```

### Trip Validation Result Endpoint (`GET /validation_result/:trip_id`)

**Purpose:** Returns mock trip validation results with localized messages

**Travel Mode Mapping:**
```javascript
const travelModeDefine = {
  1: 'driving', 2: 'transit', 3: 'walking', 4: 'biking',
  5: 'intermodal', 6: 'trucking', 7: 'park and ride',
  8: 'ridehail', 100: 'carpooling', 101: 'carpooling'
};
```

## 🚀 Usage Methods

### Upload Compressed Trajectory Data
```bash
# Compress trajectory data and upload
echo '{"trip_id": 12345, "trajectory": [{"lat": 37.7749, "lng": -122.4194, "timestamp": 1719331200, "distance": 1.5}], "is_last": false}' | gzip | \
curl -X POST "https://api.tsp.example.com/api/v1/trace/trip_trajectory" \
  -H "Authorization: Bearer <JWT_TOKEN>" \
  -H "userid: usr_12345" \
  -H "Content-Type: application/gzip" \
  --data-binary @-
```

### Record User Visit
```bash
curl -X POST "https://api.tsp.example.com/api/v1/trace/user_visit" \
  -H "Authorization: Bearer <JWT_TOKEN>" \
  -H "userid: usr_12345" \
  -H "Content-Type: application/json" \
  -d '{
    "latitude": 37.7749,
    "longitude": -122.4194,
    "arrival_date": "2024-06-25T10:00:00Z",
    "departure_date": "2024-06-25T11:30:00Z",
    "os_type": "iOS"
  }'
```

### Update Trip ETA (Driver Only)
```bash
curl -X POST "https://api.tsp.example.com/api/v1/trace/eta_change/12345" \
  -H "Authorization: Bearer <JWT_TOKEN>" \
  -H "userid: usr_12345" \
  -H "Content-Type: application/json" \
  -d '{
    "ETA": "2024-06-25T15:30:00Z",
    "route": {
      "waypoints": [
        {"lat": 37.7749, "lng": -122.4194},
        {"lat": 37.7849, "lng": -122.4094}
      ],
      "distance": 2.5,
      "duration": 420
    }
  }'
```

### Get Trip Validation Results
```bash
curl -X GET "https://api.tsp.example.com/api/v1/trace/validation_result/12345" \
  -H "Authorization: Bearer <JWT_TOKEN>" \
  -H "userid: usr_12345"
```

## 📊 Output Examples

### Successful Trajectory Upload
```json
{
  "result": "success",
  "data": {}
}
```

### Successful User Visit Recording
```json
{
  "result": "success",
  "data": {}
}
```

### ETA Update Response (Driver)
```json
{
  "result": "success",
  "data": {}
}
```

### ETA Update Response (Passenger)
```json
{
  "result": "success",
  "data": {
    "message": "ETA change request received. Note: Only driver's ETA updates affect the trip."
  }
}
```

### Trip Validation Results
```json
{
  "result": "success",
  "data": {
    "validation_time": "2024-06-25 14:30:00",
    "message": "Your driving trip didn't meet validation rules.",
    "failed_reason": [
      "Your driving speed didn't align with the standard for this travel mode.",
      "You didn't follow the planned route closely enough.",
      "You didn't complete enough of the planned trip."
    ]
  }
}
```

### Error Responses
```json
{
  "error": "ERROR_BAD_REQUEST_BODY",
  "message": "Invalid request body",
  "code": 400
}
```

```json
{
  "error": "ERROR_NOT_FOUND",
  "message": "Trip not found",
  "code": 404
}
```

## ⚠️ Important Notes

### Data Compression
- **Supported Formats:** GZIP and ZIP compression
- **Content-Type:** Must specify 'application/gzip' for GZIP data
- **Performance:** Compression reduces bandwidth usage significantly
- **Error Handling:** Decompression failures result in 400 errors

### Carpool Role Management
- **Driver Authority:** Only drivers can update trip ETAs
- **Role Sources:** DuoReservations (scheduled) and MongoDB (instant)
- **Permission Check:** Validates role before allowing ETA updates
- **Passenger Notifications:** Passengers receive acknowledgment but no changes

### Trip Validation
- **Automatic Triggers:** Trip completion and ETA changes trigger validation
- **Async Processing:** Uses setImmediate for non-blocking validation
- **Timer Management:** Scheduled validation based on ETA timestamps
- **Queue System:** Prevents duplicate validation timers

### Database Operations
- **Multi-Database:** Uses both MySQL (structured data) and MongoDB (carpool data)
- **Atomic Updates:** Distance updates use conditional queries
- **Foreign Keys:** Maintains referential integrity across models
- **Indexing:** Requires proper indexing for performance

### Validation Rules (Mock Implementation)
Current validation endpoint returns mock data with these criteria:
- **Speed Validation:** Checks if speed aligns with travel mode
- **Route Adherence:** Verifies following planned route
- **Completion Percentage:** Ensures minimum trip completion
- **Localization:** Error messages support internationalization

### Security Considerations
- **Authentication:** All endpoints require valid JWT tokens
- **Data Compression:** Verify decompressed data size limits
- **User Context:** Always validates user ownership of trips
- **Role Verification:** Multi-source role checking for carpool operations

### Performance Optimizations
- **Compression:** Reduces network overhead for trajectory data
- **Async Processing:** Non-blocking trip validation
- **Conditional Updates:** Only updates distance when improved
- **Timer Management:** Efficient scheduling for validation

## 🔗 Related File Links

- **Trip Models:** `allrepo/connectsmart/tsp-api/src/models/Trips.js`
- **Trajectory Model:** `allrepo/connectsmart/tsp-api/src/models/TripTrajectorys.js`
- **User Visit Model:** `allrepo/connectsmart/tsp-api/src/models/UserVisit.js`
- **Validation Schema:** `allrepo/connectsmart/tsp-api/src/schemas/trace.js`
- **Trip Service:** `allrepo/connectsmart/tsp-api/src/services/trip.js`
- **Travel Modes:** `allrepo/connectsmart/tsp-api/src/static/defines.js`

---
*This controller provides comprehensive trip tracking and validation capabilities essential for mobility analytics and carpool coordination.*