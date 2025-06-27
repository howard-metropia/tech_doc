# Construction Zone Controller Documentation

## 🔍 Quick Summary (TL;DR)
This controller provides endpoints for managing and querying road construction zone data. Its primary function is to identify relevant construction events that intersect with a user's planned route polylines, and it also includes endpoints for creating and testing construction event data.

**Keywords:** construction-zone | work-zone | road-closure | traffic-alert | geospatial | polyline | route-intersection | turfjs | wZDX | road-events | traffic-management

**Primary use cases:** 
- Alerting users about construction zones along their navigation route.
- Ingesting and creating new construction zone events in the system (testing/admin).
- Debugging and testing construction zone notification messages.

**Compatibility:** Node.js >= 16.0.0, Koa.js v2.x, Turf.js for geospatial calculations.

## ❓ Common Questions Quick Index
- **Q: How do I get construction alerts for a specific trip?** → [POST /construction_alerts](#post-construction_alerts)
- **Q: What format should the route `polyline` be in?** → HERE Maps encoded polyline format.
- **Q: What is `wZDX`?** → A data specification for work zone data exchange. This controller's output is formatted to be compatible with it.
- **Q: How does the route intersection logic work?** → It decodes polylines and uses geospatial services to find intersections. See [Execution Flow Analysis](#execution-flow-analysis).
- **Q: What is the purpose of the `/construction_events` endpoint?** → It's a testing/admin endpoint to create new construction events.
- **Q: Can I test notification messages?** → Yes, using the `/construction_testing_message` endpoint.
- **Q: What happens if a polyline is invalid?** → It's logged and skipped; the request doesn't fail.

## 📋 Functionality Overview

**Non-technical explanation:** 
Think of this controller as a specialized **traffic advisor for road work**. Before you start a trip, you give your planned route to the advisor (`POST /construction_alerts`). The advisor checks its master map of all known construction zones and roadblocks. It then gives you back a list of only the construction events that are directly on your path, so you know what to expect. It also has back-office functions for city planners to add new construction zones to the master map (`POST /construction_events`) and to preview the warning messages that will be sent to drivers (`POST /construction_testing_message`).

**Technical explanation:** 
A Koa.js controller with three `POST` endpoints for handling construction zone data. The main public-facing endpoint, `/construction_alerts`, accepts an array of routes (each with encoded polylines), decodes them, and calls a service (`mergeAllConstructionEvents`) to perform geospatial intersection analysis against a database of construction events. It then returns a GeoJSON `FeatureCollection` of matching events formatted according to the WZDx (Work Zone Data Exchange) specification. The other two endpoints, `/construction_events` and `/construction_testing_message`, serve administrative/testing purposes for creating events and testing notification content, respectively.

**Business value explanation:**
This controller provides a critical safety and convenience feature for any navigation or transportation application. By proactively warning users about construction zones, it helps them avoid delays, navigate more safely, and have a better overall trip experience. This improves user trust and application utility. The administrative endpoints streamline the process of managing and verifying road work data, ensuring the information provided to users is accurate and up-to-date.

## 🔧 Technical Specifications

- **File:** `allrepo/connectsmart/tsp-api/src/controllers/construction-zone.js`
- **Language:** JavaScript (ES2020)
- **Framework:** Koa.js v2.x with @koa/router
- **Type:** REST API Controller
- **File Size:** ~8 KB
- **Complexity Score:** ⭐⭐⭐⭐ (High - Complex geospatial logic, data transformation, and multiple distinct endpoints.)

**Dependencies (Criticality Level):**
- `@koa/router`, `koa-bodyparser`: Core routing and body parsing (**Critical**).
- `moment-timezone`: Date and time manipulation (**High**).
- `@turf/turf`: Used by downstream services for geospatial calculations (**Critical** for logic).
- `uuid`: For generating unique IDs for new events (**Medium**).
- `@app/src/services/hereMapPolylines`: For decoding route polylines (**Critical**).
- `@app/src/services/constructionZone`: Contains the core business logic (**Critical**).
- `@app/src/models/ConstructionZone`: The database model for construction events (**Critical**).
- `@app/src/helpers/pd-debug-module`: A debug helper to disable the feature for specific test users (**Medium**).

## 📝 Detailed Code Analysis

### `POST /construction_alerts`
This is the primary endpoint for client applications.

**Execution Flow Analysis:**
1.  **Authentication & Input Validation**: The request is authenticated, and the body is validated to ensure it contains a `routes` array.
2.  **Debug Mode Check**: It checks if the `userId` is in a special debug group for this feature. If so, it immediately returns an empty `FeatureCollection` and stops processing. This is a useful pattern for A/B testing or canary rollouts.
3.  **Polyline Decoding**: It iterates through each route and each polyline within that route.
    - It calls `poly.decode(line)` to convert the HERE Maps encoded string into an array of coordinates.
    - A `try...catch` block gracefully handles decoding errors, logging them but not failing the entire request.
    - The decoded coordinates are converted into GeoJSON format.
4.  **Intersection Service**: It passes all the decoded routes to the `mergeAllConstructionEvents` service. This service is the heart of the feature, performing the complex geospatial queries to find which construction events intersect with the provided route geometries.
5.  **Result Aggregation**: The results from the service are returned per-route. The code then aggregates these results, merging duplicate events that may appear on multiple routes and compiling a unique list of matching construction zones.
6.  **WZDx Formatting**: The final, unique list of events is formatted into a WZDx-compliant `FeatureCollection` JSON object and returned to the client.

### `POST /construction_events`
This is a testing or administrative endpoint for creating events.

**Execution Flow Analysis:**
1.  **Authentication & Input Validation**: Secures the endpoint and validates the incoming `events` array.
2.  **Event Iteration**: It iterates through each event object provided in the request.
3.  **Data Hydration & Formatting**: For each event, it:
    - Generates a UUID if one isn't provided.
    - Parses start and end times using `moment`.
    - Determines geometry, either using a provided Polygon or generating a default area using `getArea()`.
    - Extracts or determines cross-street information.
    - Builds a complete `eventObj` that conforms to the `ConstructionZone` model schema, which is based on the WZDx specification.
4.  **Database Insertion**: It calls `ConstructionZone.create(eventObj)` to insert the new event into the database. This is done for all events in parallel using `Promise.all`.
5.  **Response**: Returns a simple "OK" message on success.

## 🚀 Usage Methods

**Base URL:** `https://api.tsp.example.com/api/v2`

**Headers (for all requests):**
- `Authorization`: `Bearer <YOUR_JWT_TOKEN>`
- `userid`: `usr_...` (The user's ID)
- `Content-Type`: `application/json`

### Get Construction Alerts for a Route
```bash
curl -X POST "https://api.tsp.example.com/api/v2/construction_alerts" \
  -H "Authorization: Bearer <TOKEN>" \
  -H "userid: usr_123" \
  -H "Content-Type: application/json" \
  -d '{
    "routes": [
      {
        "id": "route_01",
        "polyline": ["grqkFfymbQnKzA_@...", "another_encoded_polyline_segment..."]
      }
    ]
  }'
```

### Create a Test Construction Event
```bash
curl -X POST "https://api.tsp.example.com/api/v2/construction_events" \
  -H "Authorization: Bearer <TOKEN>" \
  -H "userid: admin_usr_456" \
  -H "Content-Type: application/json" \
  -d '{
    "events": [
      {
        "id": "test_event_01",
        "lat": 29.7604,
        "lng": -95.3698,
        "location": "Main St at Texas Ave",
        "roadway_names": ["Main St"],
        "direction": "northbound",
        "start_time": "2024-01-01T09:00:00Z",
        "end_time": "2024-01-05T17:00:00Z",
        "lanes": "one right lane closed",
        "impacted_level": "medium"
      }
    ]
  }'
```

## 📊 Output Examples

### Successful `/construction_alerts` Response
The output is a GeoJSON FeatureCollection compliant with the WZDx specification.
```json
{
  "result": "success",
  "data": {
    "type": "FeatureCollection",
    "road_event_feed_info": {
      "publisher": "Houston TranStar",
      "version": "4.2",
      "update_date": "2024-06-25T12:00:00Z",
      "data_sources": [ ... ]
    },
    "features": [
      {
        "type": "Feature",
        "properties": {
          "core_details": {
            "data_source_id": "some_event_id",
            "event_type": "work-zone",
            "road_names": ["I-45"],
            "direction": "northbound",
            ...
          },
          "start_date": "2024-06-25T14:00:00.000Z",
          "end_date": "2024-06-26T22:00:00.000Z",
          "extensions": {
            "matched_route_id": ["route_01"]
          }
        },
        "geometry": {
          "type": "Polygon",
          "coordinates": [ ... ]
        }
      }
    ]
  }
}
```

## ⚠️ Important Notes
- **Geospatial Complexity**: The core logic is highly dependent on the accuracy of the underlying geospatial services (`hereMapPolylines`, `constructionZone` service with Turf.js). Errors in these can lead to incorrect alerts.
- **Data Format (WZDx)**: The controller's primary purpose is to transform various inputs into the standardized WZDx v4.2 format. Understanding this spec is key to understanding the code's output.
- **Error Handling**: The controller gracefully handles polyline decoding errors on a per-polyline basis, which makes it robust. However, failures in the main service call or database will still result in a server error.

## 🔗 Related File Links
- **Core Logic:** `allrepo/connectsmart/tsp-api/src/services/constructionZone.js`
- **Database Model:** `allrepo/connectsmart/tsp-api/src/models/ConstructionZone.js`
- **Input Schemas:** `allrepo/connectsmart/tsp-api/src/schemas/construction-zone.js`
- **Polyline Decoding:** `allrepo/connectsmart/tsp-api/src/services/hereMapPolylines.js`
- **Debug Module:** `allrepo/connectsmart/tsp-api/src/helpers/pd-debug-module.js`

---
*This documentation was generated to provide a comprehensive overview of the `construction-zone.js` controller, its endpoints, and its role in providing route-based traffic alerts.* 