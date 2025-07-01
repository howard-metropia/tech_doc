# TSP API Bus Schedule Controller Documentation

## 🔍 Quick Summary (TL;DR)
The bus schedule controller is a complex data aggregation endpoint responsible for fetching, combining, and formatting bus route and stop information from multiple data sources, including GTFS feeds, real-time data, and user-specific data like favorites.

**Keywords:** bus-schedule | GTFS | transit | real-time-bus | bus-routes | bus-stops | transportation-api | tsp-api | koa-router | knex | mysql | mongodb

**Primary use cases:** Displaying bus routes in a mobile app, fetching stops for a specific route, getting real-time bus locations, finding nearby bus stations.

**Compatibility:** Node.js >=16.0.0, Koa.js v2.x, Knex.js, Mongoose, `moment-timezone`

## ❓ Common Questions Quick Index
- **Q: How do I get a list of all bus routes?** → [Get All Bus Routes](#get-all-bus-routes-get-busroute)
- **Q: How can I find the bus stops for a specific route?** → [Get Bus Stops for a Route](#get-bus-stops-for-a-route-get-busroutestop)
- **Q: Is there a way to see where buses are right now?** → [Get Real-time Bus Data](#get-real-time-bus-data-get-busrealtime)
- **Q: How do I find bus stations near a specific location?** → [Find Nearby Bus Stations](#find-nearby-bus-stations-get-busstation)
- **Q: What data sources are being used?** → [Data Source Integration](#data-source-integration)
- **Q: Why is this controller connecting to so many databases?** → [Architecture and Design](#architecture-and-design)
- **Q: How is caching implemented for performance?** → [Caching Strategy](#caching-strategy)

## 📋 Functionality Overview

**Non-technical explanation:** 
Think of this controller as a **central dispatch for a city's bus system**. It's connected to multiple information sources: the master schedule book (GTFS database), live GPS trackers on the buses (real-time database), the list of all bus stops (station database), and a list of your personal favorite routes (user profile database). When you ask "What are my bus options?", this dispatcher quickly gathers information from all these sources, cross-references them, and presents you with a neat, personalized list of routes, telling you which ones have active alerts and which ones are your favorites.

**Technical explanation:** 
A multi-endpoint Koa.js REST controller that serves as a data aggregation and formatting layer for Houston's bus transit data. It connects to three different MySQL database instances (`houston`, `portal`, `gtfs`) via Knex.js and also uses a MongoDB instance for caching route data. The controller handles complex raw SQL queries, joins data from different schemas, and leverages `moment-timezone` for correct date/time handling based on the 'America/Chicago' timezone. It provides endpoints for fetching routes, stops, real-time vehicle positions, and nearby stations.

**Business value explanation:**
This controller is the backbone of the transit features within the MaaS application. It provides the essential, up-to-date, and personalized information that users need to plan their journeys using public transportation. Its performance and accuracy directly impact user trust and the usability of the bus travel module.

## 🔧 Technical Specifications

- **File:** `allrepo/connectsmart/tsp-api/src/controllers/busSchedule.js`
- **Language:** JavaScript (ES2020)
- **Framework:** Koa.js v2.x with @koa/router
- **Type:** REST API Controller
- **Complexity Score:** ⭐⭐⭐⭐⭐ (Very High - multiple database connections, complex raw SQL, data aggregation, caching logic)

**Dependencies (Criticality Level):**
- `@koa/router`: HTTP routing framework (**Critical**)
- `koa-bodyparser`: Request body parsing (**Critical**)
- `knex`: SQL query builder for multiple MySQL connections (**Critical**)
- `mongoose` (via models): ODM for MongoDB connection (**Critical**)
- `@app/src/middlewares/auth`: JWT authentication middleware (**Critical**)
- `@app/src/services/busSchedule`: Business logic service for data reformatting (**Critical**)
- `moment-timezone`: Timezone handling library (**Critical**)
- `isodate`: ISO date string conversion (**High**)

### Data Source Integration
This controller is unique in its complex data source requirements:
1.  **`houston` (MySQL via Knex):** Appears to be a primary application database.
2.  **`portal` (MySQL via Knex):** Used to fetch user-specific data like `bus_route_favorite`.
3.  **`gtfs` (MySQL via Knex):** Contains the core GTFS (General Transit Feed Specification) data, including routes, stops, trips, and calendar information.
4.  **MongoDB (via Mongoose Models):** Used as a cache for pre-processed route data (`BusRoutes` model) to avoid expensive SQL queries on every request.

## 📝 Detailed Code Analysis

### Key Endpoints

#### Get All Bus Routes (`GET /bus/route`)
- **Purpose:** Fetches a comprehensive list of all bus routes.
- **Logic:**
    1.  Determines the current day of the week in the 'America/Chicago' timezone.
    2.  Fetches the user's favorite routes from the `portal` database.
    3.  Fetches the GTFS calendar data.
    4.  **Implements a caching strategy:**
        - It first tries to fetch formatted route data from the `BusRoutes` collection in MongoDB.
        - If a valid cache entry exists (`mrkTime` is not expired), it uses the cached data.
        - **If the cache is stale or empty**, it executes a very large, complex raw SQL query against the `gtfs` database to build the route list from scratch.
        - The result of the SQL query is then saved back to the MongoDB cache with a new expiration time.
    5.  The combined data is passed to the `busSchedule.reformat` service to be structured for the client.
    6.  It also queries for active transit alerts and flags the affected routes.
- **Complexity:** High. The raw SQL query is intricate and the cache-aside pattern adds significant logical branching.

#### Get Bus Stops for a Route (`GET /bus/route/:routeID/stop`)
- **Purpose:** Fetches all the bus stops for a given route ID.
- **Logic:**
    1.  Validates the `:routeID` parameter.
    2.  Fetches route details and user's favorite stops.
    3.  **Implements a caching strategy** similar to the `/bus/route` endpoint, using the `BusStations` MongoDB collection.
    4.  If the cache is stale, it executes multiple complex raw SQL queries to get the stops for both directions of the route.
    5.  Results are saved to the MongoDB cache.
    6.  The `busSchedule.reformatStations` service is used to format the final output.

#### Get Real-time Bus Data (`GET /bus/realtime/:routeID`)
- **Purpose:** Provides the live GPS locations of buses operating on a specific route.
- **Logic:**
    1.  Fetches real-time data from the `HoustonBusRealtime` MongoDB collection.
    2.  This data is likely populated by a separate background process that ingests a real-time feed. The controller only reads from it.

#### Find Nearby Bus Stations (`GET /bus/station`)
- **Purpose:** Finds bus stations within a certain radius of a given latitude and longitude.
- **Logic:**
    1.  Validates `lat` and `lon` query parameters.
    2.  Executes a raw SQL query using the **Haversine formula** to calculate distances and find stations within the specified radius (defaulting to 1609 meters, or ~1 mile).
    3.  Fetches the user's favorite stops to flag them in the results.

### Architecture and Design
- **Data-Centric Controller:** This controller's primary role is to be a data aggregator. It contains a lot of data access logic that in a stricter separation-of-concerns architecture might live entirely within the service layer.
- **Performance Optimization:** The heavy use of caching (MongoDB as a cache for MySQL queries) and complex, hand-tuned raw SQL indicates that performance is a major concern for these endpoints. The raw queries are likely designed to be faster than what the Knex query builder could produce for such complex joins.
- **Legacy Code:** The presence of many commented-out code blocks suggests a history of evolution and experimentation.

## 🚀 Usage Methods

### Get All Bus Routes (`GET /api/v2/bus/route`)
```bash
curl -X GET "https://api.tsp.example.com/api/v2/bus/route" \
  -H "Authorization: Bearer <YOUR_JWT_TOKEN>" \
  -H "userid: usr_12345"
```

### Get Stops for Route 82 (`GET /api/v2/bus/route/82/stop`)
```bash
curl -X GET "https://api.tsp.example.com/api/v2/bus/route/82/stop" \
  -H "Authorization: Bearer <YOUR_JWT_TOKEN>" \
  -H "userid: usr_12345"
```

### Get Real-time info for Route 82 (`GET /api/v2/bus/realtime/82`)
```bash
curl -X GET "https://api.tsp.example.com/api/v2/bus/realtime/82" \
  -H "Authorization: Bearer <YOUR_JWT_TOKEN>"
```

### Find Nearby Stations
```bash
curl -X GET "https://api.tsp.example.com/api/v2/bus/station?lat=29.7604&lon=-95.3698" \
  -H "Authorization: Bearer <YOUR_JWT_TOKEN>" \
  -H "userid: usr_12345"
```

## ⚠️ Important Notes

### Caching Strategy
The controller employs a time-based, cache-aside pattern using MongoDB. A request for routes or stops first checks Mongo. If a non-expired document is found, it's used. If not, the system falls back to the authoritative source (MySQL `gtfs` database), performs the expensive query, and then populates the cache with the results and a new expiration time (`mrkTime`). This is critical for performance.

### Timezone Dependency
All date and time calculations are hardcoded to the `'America/Chicago'` timezone. This is a critical assumption for the service to function correctly.

### Haversine Formula
The nearby station search uses a raw SQL implementation of the Haversine formula to calculate great-circle distances on a sphere. This is an efficient way to perform location-based queries directly in the database.

### Troubleshooting Guide

1.  **Symptom: Routes are missing or outdated.**
    *   **Diagnosis:** The MongoDB cache (`busroutes` collection) might be stale and the fallback query is failing, or the underlying GTFS data in MySQL is old.
    *   **Solution:** Check the `mrkTime` in the `busroutes` documents in MongoDB. If expired, check server logs for errors during the MySQL fallback query. Verify the GTFS data itself is up-to-date.

2.  **Symptom: API response is very slow.**
    *   **Diagnosis:** This is likely a cache miss, forcing the controller to execute the complex raw SQL queries.
    *   **Solution:** This is expected on a cache miss. If it happens frequently, the cache TTL might be too short, or the caching mechanism might be failing. Investigate logs for cache hit/miss rates.

3.  **Symptom: Nearby stations are not accurate.**
    *   **Diagnosis:** The latitude/longitude passed to the API might be incorrect, or the radius calculation in the Haversine formula might not suit the use case.
    *   **Solution:** Verify the coordinates. Check the hardcoded radius (1609 meters) in the SQL query within the `/bus/station` endpoint logic.

## 🔗 Related File Links

- **Services:** `allrepo/connectsmart/tsp-api/src/services/busSchedule.js`
- **Models:** `allrepo/connectsmart/tsp-api/src/models/BusRoutes.js`, `BusStations.js`, `HoustonMetro.js`, `HoustonBusRealtime.js`
- **Schemas:** `allrepo/connectsmart/tsp-api/src/schemas/bus-schedule.js`
- **Middleware:** `allrepo/connectsmart/tsp-api/src/middlewares/auth.js`

---
*This documentation was generated based on the provided template and source file.*
