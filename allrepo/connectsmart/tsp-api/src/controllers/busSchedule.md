# Bus Schedule Controller Documentation

## 🔍 **Quick Summary (TL;DR)**
- **Functional Description:** A comprehensive Houston Metro transit API controller providing real-time bus schedules, route information, station data, and favorite route management with GTFS data integration and MongoDB caching.
- **Core Keywords:** bus schedule | transit routes | GTFS | Houston Metro | real-time data | bus stations | route favorites | transit alerts | schedule timetable | public transportation
- **Primary Use Cases:** Mobile transit apps, route planning, real-time arrival predictions, transit alerts, favorite route management
- **Compatibility:** Node.js 14+, Koa.js framework, MySQL (GTFS), MongoDB (cache), multi-timezone support

## ❓ **Common Questions Quick Index**
1. **Q: How do I get all available bus routes?** → [Get Bus Routes](#get-bus-routes)
2. **Q: How do I get real-time bus arrival times?** → [Real-time Integration](#real-time-integration)
3. **Q: What's the difference between scheduled and real-time data?** → [Schedule vs Real-time](#schedule-vs-real-time)
4. **Q: How do I manage favorite routes for users?** → [Favorite Routes Management](#favorite-routes-management)
5. **Q: How are timezones handled for Houston Metro?** → [Timezone Handling](#timezone-handling)
6. **Q: What are UIS alerts and how do they work?** → [Transit Alerts](#transit-alerts)
7. **Q: How do I troubleshoot slow response times?** → [Performance Optimization](#performance-optimization)
8. **Q: How does the caching system work?** → [Caching Strategy](#caching-strategy)
9. **Q: What happens during service hours vs off-hours?** → [Service Time Logic](#service-time-logic)
10. **Q: How do I handle weekend vs weekday schedules?** → [Calendar Service](#calendar-service)

## 📋 **Functionality Overview**

### **Non-technical Explanation**
Think of this controller like a **digital transit information kiosk** - similar to the electronic displays at bus stops that show arrival times. Like a **personal travel assistant for public transit**, it combines official bus schedules with live traffic data to tell you exactly when the next bus will arrive. Just as a **smart city traffic management system** coordinates between printed timetables, GPS tracking, and service alerts, this API merges static route data with real-time vehicle positions and disruption notifications.

### **Technical Explanation** 
This is a **Koa.js REST API controller** implementing **GTFS (General Transit Feed Specification) data processing** with **hybrid database architecture**. It serves as a **transit data aggregation layer** combining MySQL-stored schedule data, MongoDB-cached real-time information, and dynamic service status calculations with timezone-aware processing for Houston Metro transit system.

### **Business Value**
- **Enhanced User Experience:** Provides accurate, real-time transit information reducing wait times
- **Operational Efficiency:** Reduces customer service inquiries through self-service data access
- **Data Integration:** Seamlessly combines static schedules with live operational data
- **User Engagement:** Favorite routes and personalized features increase app retention

### **System Architecture Context**
Central component of the **MaaS transit information system**, serving as the **primary transit data gateway** for mobile applications. Integrates with Houston Metro's real-time feeds, GTFS static data, and user preference systems to provide comprehensive transit services.

## 🔧 **Technical Specifications**

### **File Information**
- **Name:** busSchedule.js
- **Path:** `/src/controllers/busSchedule.js`
- **Type:** Koa.js REST API Controller
- **Language:** JavaScript (ES6+)
- **File Size:** ~65KB
- **Complexity Score:** ⭐⭐⭐⭐⭐ (Very High) - Complex GTFS processing with real-time integration

### **Dependencies**
| Dependency | Version | Purpose | Criticality |
|-----------|---------|---------|-------------|
| `@koa/router` | ^10.x | HTTP routing framework | High |
| `@maas/core/mysql` | Internal | Multiple database connections (houston, portal, gtfs) | Critical |
| `moment-timezone` | ^0.5.x | Timezone-aware date processing | Critical |
| `mongoose` | ^6.x | MongoDB ODM for real-time data | High |
| `joi` | ^17.x | Input validation schemas | High |
| `isodate` | ^6.x | ISO date parsing for MongoDB | Medium |

### **Database Schema Requirements**
- **MySQL GTFS:** routes, trips, stops, stop_times, calendar, agency tables
- **MySQL Portal:** bus_route_favorite table for user preferences  
- **MongoDB Cache:** BusRoutes, BusStations, HoustonBusRealtime collections

### **API Endpoints**
| Endpoint | Method | Purpose | Authentication |
|----------|--------|---------|----------------|
| `/api/v2/bus/route` | GET | Get all bus routes with favorites | Required |
| `/api/v2/bus/route/:routeID/stop` | GET | Get route stations and real-time data | Required |
| `/api/v2/bus/route/:routeID/:tripID/stop/:stopID/:direction` | GET | Get timetable for specific stop | Required |
| `/api/v2/bus/route/calendar/:routeID/:tripID/stop/:stopID/:direction` | GET | Get service calendar | Required |
| `/api/v2/bus/route/favorite` | GET | Get user's favorite routes | Required |
| `/api/v2/bus/route/favorite/add/:agencyID/:routeID` | POST | Add favorite route | Required |
| `/api/v2/bus/route/favorite/delete/:agencyID/:routeID` | DELETE | Remove favorite route | Required |
| `/api/v2/bus/route/:routeID/alert` | GET | Get route-specific alerts | Required |

## 📝 **Detailed Code Analysis**

### **Core Processing Flow**
1. **Timezone Calculation** (5-10ms) - Convert UTC to America/Chicago timezone
2. **Weekday Determination** (1-2ms) - Calculate service day for schedule lookup
3. **Cache Check** (20-100ms) - Query MongoDB for cached route/station data
4. **GTFS Query** (100-500ms) - Fallback to MySQL for fresh schedule data
5. **Real-time Integration** (200-800ms) - Merge with Houston Metro live feeds
6. **Response Assembly** (10-50ms) - Format combined data for client

### **Caching Strategy**
```javascript
// MongoDB cache with TTL (Time To Live)
const cacheExpiry = moment().endOf('week').format('YYYY-MM-DDTHH:mm:ssZ');
const cachedData = await BusRoutes.findOne({
  mrkTime: { $gte: isodate(nowTime) }
}).sort({ _id: -1 });
```

### **Real-time Data Integration**
```javascript
// Real-time arrival prediction
if (currentSecs >= startTime && currentSecs <= endTime && isServiceDay) {
  const realtimeData = await HoustonBusRealtime.findOne({
    _id: stopID,
    'routes._id': routeID
  });
  
  // Merge scheduled with real-time
  station.next_arrival_time = realtime.departure.time;
  station.trip_status = realtime.scheduleRelationship; // SKIPPED, CANCELED
}
```

### **Service Time Logic**
- **Operating Hours:** Dynamic calculation based on first/last departure times
- **Late Night Service:** Handles trips extending past midnight (24:00+ format)
- **End of Service Detection:** Automatically disables real-time queries during non-service hours

## 🚀 **Usage Methods**

### **Get All Bus Routes**
```javascript
const getBusRoutes = async (userToken) => {
  const response = await fetch('/api/v2/bus/route', {
    method: 'GET',
    headers: {
      'Authorization': `Bearer ${userToken}`,
      'userid': userId
    }
  });
  
  const data = await response.json();
  console.log('Available routes:', data.data.route);
  console.log('UIS alerts:', data.data.uis_alerts);
};
```

### **Get Real-time Station Data**
```javascript
const getStationData = async (routeId) => {
  const response = await fetch(`/api/v2/bus/route/${routeId}/stop`, {
    method: 'GET',
    headers: {
      'Authorization': `Bearer ${token}`,
      'userid': userId
    }
  });
  
  const data = await response.json();
  
  // Access directions
  const inbound = data.data.positive_direction;
  const outbound = data.data.opposite_direction;
  
  // Check service status
  if (inbound.last_trip_set_out === 1) {
    console.log('Inbound service has ended for the day');
  }
  
  // Real-time arrivals
  inbound.stations.forEach(station => {
    if (station.next_arrival_time) {
      console.log(`Next bus at ${station.stop_name}: ${station.next_arrival_time}`);
    }
  });
};
```

### **Manage Favorite Routes**
```javascript
const RouteManager = {
  async addFavorite(agencyId, routeId) {
    const response = await fetch(`/api/v2/bus/route/favorite/add/${agencyId}/${routeId}`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`,
        'userid': userId
      }
    });
    return response.json();
  },
  
  async removeFavorite(agencyId, routeId) {
    const response = await fetch(`/api/v2/bus/route/favorite/delete/${agencyId}/${routeId}`, {
      method: 'DELETE',
      headers: {
        'Authorization': `Bearer ${token}`,
        'userid': userId
      }
    });
    return response.json();
  },
  
  async getFavorites() {
    const response = await fetch('/api/v2/bus/route/favorite', {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${token}`,
        'userid': userId
      }
    });
    return response.json();
  }
};
```

## 📊 **Output Examples**

### **Bus Routes Response**
```json
{
  "success": true,
  "data": {
    "route": [
      {
        "type": "Bus",
        "name_int": 1,
        "route_id": "ME001",
        "route_short_name": "1",
        "route_long_name": "Westheimer",
        "route_color": "FF6B35",
        "first_headsign": "Eastbound to Downtown",
        "end_headsign": "Westbound to City Centre",
        "services": "c_23_c_24_c_25",
        "is_favorite": true,
        "is_uis_alert": false
      }
    ]
  }
}
```

### **Station Data with Real-time**
```json
{
  "success": true,
  "data": {
    "agency_name": "METRO",
    "sync_time": "2025-06-24T14:45:30+00:00",
    "route_id": "ME001",
    "positive_direction": {
      "trip_headsign": "Eastbound to Downtown",
      "direction": 0,
      "last_trip_set_out": 0,
      "stations": [
        {
          "stop_id": "ME1001",
          "stop_name": "Main St @ Bell St",
          "next_arrival_time": "2025-06-24T14:47:15+00:00",
          "trip_status": ""
        }
      ]
    },
    "uis_alerts": []
  }
}
```

## ⚠️ **Important Notes**

### **Performance Considerations**
- **Database Connection Pool:** Manages 3 separate MySQL connections (houston, portal, gtfs)
- **MongoDB Query Optimization:** Uses compound indexes on route_id and mrkTime
- **Real-time Data Throttling:** Only queries during service hours to reduce load
- **Caching TTL:** Route data cached until end of week, station data per request

### **Timezone Handling**
- **Primary Timezone:** America/Chicago (Houston local time)
- **Daylight Saving:** Automatic DST detection and adjustment
- **Late Night Service:** Handles overnight trips with 24+ hour format
- **Date Boundaries:** Correctly processes trips crossing midnight

### **Common Troubleshooting**

| Symptom | Diagnosis | Solution |
|---------|-----------|----------|
| Slow response (>2s) | MongoDB cache miss | Check MongoDB connection and cache expiry |
| Missing real-time data | Outside service hours | Verify current time vs service schedule |
| Incorrect timezone | DST calculation error | Validate moment-timezone configuration |
| 500 errors | Database timeout | Check GTFS database connectivity |
| Empty route list | GTFS data missing | Verify routes table has Houston Metro data |

## 🔗 **Related File Links**

### **Service Dependencies**
- **Bus Schedule Service:** [`/src/services/busSchedule.js`](../../../services/busSchedule.js) - Data reformatting logic
- **Validation Schemas:** [`/src/schemas/bus-schedule.js`](../../../schemas/bus-schedule.js) - Input validation

### **Database Models**
- **BusRoutes:** [`/src/models/BusRoutes.js`](../../../models/BusRoutes.js) - MongoDB route cache
- **BusStations:** [`/src/models/BusStations.js`](../../../models/BusStations.js) - MongoDB station cache
- **HoustonBusRealtime:** [`/src/models/HoustonBusRealtime.js`](../../../models/HoustonBusRealtime.js) - Real-time data

### **Testing Files**
- **Unit Tests:** [`/test/test-busSchedule.js`](../../../../test/test-busSchedule.js) - Controller functionality tests

## 🏷️ **Document Tags**

### **Keywords**
bus-schedule, transit-api, GTFS, Houston-Metro, real-time-transit, route-planning, public-transportation, MongoDB-cache, timezone-handling, transit-alerts, favorite-routes, schedule-timetable

### **Technical Tags**
`#controller` `#transit-api` `#GTFS` `#real-time-data` `#MongoDB-cache` `#MySQL` `#timezone` `#Houston-Metro` `#public-transit` `#route-planning` `#koa-framework` `#complex-logic`

### **Target Roles**
- **Transit App Developers** (Advanced) - Integration with transit systems
- **Backend Engineers** (Expert) - Complex data processing and optimization
- **Product Managers** (Intermediate) - Understanding transit features and capabilities
- **QA Engineers** (Advanced) - Testing complex time-based logic and data accuracy

### **Complexity Rating**
⭐⭐⭐⭐⭐ (Very High) - Complex GTFS data processing, multi-database coordination, real-time integration, timezone calculations, and service hour logic

### **Maintenance Level**
**High** - Requires ongoing monitoring of Houston Metro data feeds, cache optimization, database performance tuning, and timezone/DST updates

### **Business Criticality**
**Critical** - Core functionality for transit mobile applications, directly impacts user experience and app adoption for public transportation users

### **Related Topics**
Public Transportation, GTFS Standards, Real-time Transit Data, MongoDB Caching, Timezone Processing, Mobile Transit Apps, API Performance Optimization, Database Integration