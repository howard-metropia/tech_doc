# TSP API Reservations Service Documentation

## 🔍 Quick Summary (TL;DR)
The Reservations service manages trip reservations and carpooling with complex features including carpool matching, transit alerts, weather integration, HERE Maps routing, polyline processing, and comprehensive trip detail management for multi-modal transportation.

**Keywords:** reservation-management | carpool-matching | transit-alerts | weather-integration | here-routing | trip-details | polyline-processing | multi-modal-transport

**Primary use cases:** Creating trip reservations, managing carpool partnerships, handling transit alerts, integrating weather data, processing route polylines, managing trip conflicts, suggestion card integration

**Compatibility:** Node.js >= 16.0.0, MySQL and MongoDB databases, HERE Maps API, weather services, complex multi-table operations

## ❓ Common Questions Quick Index
- **Q: What types of reservations are supported?** → Public transit, driving, carpool (DUO), intermodal, park-and-ride
- **Q: How does carpool matching work?** → Partners matched by carpool_uuid with driver/passenger roles
- **Q: What transit alerts exist?** → Real-time bus route alerts from GTFS data
- **Q: How is weather integrated?** → AI-powered weather alerts with route-specific forecasts
- **Q: What conflict resolution exists?** → Automatic cancellation of overlapping unpaired reservations
- **Q: How are routes processed?** → HERE Maps routing with polyline encoding and GeoJSON conversion

## 📋 Functionality Overview

**Non-technical explanation:** 
Think of this as a **comprehensive trip booking system** that not only lets you reserve rides but also finds carpool partners, warns you about bus delays, tells you about weather along your route, and makes sure you don't accidentally book two trips at the same time.

**Technical explanation:** 
A sophisticated reservation management service handling multi-modal transportation bookings with integrated carpool matching, real-time transit alerts, AI-powered weather forecasting, HERE Maps route processing, conflict resolution, and comprehensive trip detail management.

**Business value explanation:**
Enables comprehensive trip planning and booking, supports revenue-generating carpool services, provides proactive user notifications for service disruptions, enhances user experience with weather-aware recommendations, and maintains data integrity through conflict management.

## 🔧 Technical Specifications

- **File:** `allrepo/connectsmart/tsp-api/src/services/reservations.js`
- **Language:** JavaScript (ES2020)
- **Framework:** Node.js with Objection.js ORM and Mongoose
- **Type:** Comprehensive Trip Reservation Management Service
- **File Size:** ~26.6 KB
- **Complexity Score:** ⭐⭐⭐⭐⭐ (Very High - Complex multi-service integration)

**Dependencies:**
- `moment-timezone`: Date/time handling with timezone support (**Critical**)
- `@maas/core/mysql`: Multi-database connectivity (**Critical**)
- `@app/src/services/hereRouting`: HERE Maps integration (**High**)
- `@app/src/services/weather`: Weather forecasting (**High**)
- `@app/src/services/hereMapPolylines`: Route encoding (**High**)
- Multiple models for complex data relationships (**Critical**)

## 📝 Detailed Code Analysis

### Core Service Functions

### getAll Function
**Purpose:** Retrieves user reservations with complex filtering and carpool data

**Parameters:**
- `userId`: Number - User identifier
- `travelMode`: Array - Allowed travel modes
- `offset`: Number - Pagination offset
- `perpage`: Number - Items per page
- `isToday`: Boolean - Today-only filter

**Complex SQL Query Logic:**
```sql
select reservation.*, case 
  when reservation.travel_mode in (${travelModeWithoutDUO}) 
then 
  reservation.estimated_arrival_on 
else case 
    when reservation.status = 1 
  then 
    reservation.started_off
  else case 
      when reservation.status in (11, 60)  
    then 
      date_add(reservation.overlap_on, interval (3600 - ms.time_to_dropoff) second)
    else 
      reservation.started_off 
    end
  end
end as expired_on
```
- Dynamic expiration time calculation based on travel mode and status
- Complex joins for DUO (carpool) reservation data
- Payment and validation status integration

### Carpool Partner Management

### getPairedPartners Function
**Purpose:** Retrieves matched carpool partners with detailed profile information

```javascript
const getPairedPartners = async (selfReservation, includeProfile) => {
  const partners = await Reservation.query()
    .where('carpool_uuid', selfReservation.carpool_uuid)
    .whereNot('id', selfReservation.id)
    .whereIn('status', [Reservation.status.MATCHED, Reservation.status.STARTED])
    .withGraphFetched('[duoReservation]');

  const riders = await Promise.all(
    partners.map(async (partner) => {
      const rider = {
        offer_id: partner.duoReservation?.offer_id,
        reservation_id: partner.id,
        role: partner.role,
        origin: { /* location data */ },
        destination: { /* location data */ }
      };
      
      // Dynamic pricing calculation
      if (ENABLE_UNIT_PRICE === 'true') {
        const driverUnitPrice = selfReservation.role === Reservation.role.DRIVER
          ? selfReservation.unit_price
          : partner.unit_price;
        price = parseFloat(driverUnitPrice * riderRouteMeter);
        
        if (selfReservation.role === Reservation.role.PASSENGER) {
          price += parseFloat(escrow.passengerTransactionFee);
        } else {
          price -= parseFloat(escrow.driverTransactionFee);
        }
      }
      
      return rider;
    })
  );
};
```
- Fetches partners by shared carpool_uuid
- Dynamic pricing based on driver's unit price and rider's route distance
- Includes transaction fees based on user role

### Transit Alert System

### checkTransitAlertForReservations Function
**Purpose:** Checks reservations against real-time transit alerts

```javascript
async function checkTransitAlertForReservations(reservations, userId) {
  const eventRouteMapping = await searchOngoingEvents();
  const routeIdList = Array.from(new Set(eventRouteMapping.map(route => route.route_id)));
  
  for (const reservation of reservations) {
    if (!isAlertTarget(reservation)) continue;
    
    const tripDetail = await TripDetails.query()
      .where('user_id', userId)
      .where('reservation_id', reservation.id)
      .first();
      
    if (tripDetail) {
      tripDetail.sections = JSON.parse(tripDetail.steps);
      for (const section of tripDetail.sections) {
        if (section.type === 'transit' && section.transport.mode === 'bus') {
          if (routeIdList.includes(section.transport.route_id)) {
            reservation.is_uis_alert = true;
          }
        }
      }
    }
  }
}
```
- Queries GTFS database for ongoing transit alerts
- Matches bus route IDs against affected routes
- Sets alert flags on relevant reservations

### Weather Integration

### getWeatherInfo Function
**Purpose:** Provides AI-powered weather alerts for trip routes

```javascript
const getWeatherInfo = async (tripDetail) => {
  const polyline = [];
  const travelModeSet = new Set();
  
  tripDetail.sections.forEach((section) => {
    const sectionTravelMode = defines.travelMode[section.type];
    if (defines.weather.appliedTravelMode.includes(sectionTravelMode)) {
      if (section.polyline) {
        polyline.push(section.polyline);
        travelModeSet.add(section.type);
      }
    }
  });
  
  const decodeRoutes = [];
  route.polyline.forEach((line) => {
    const coordinates = poly.decode(line).polyline;
    decodeRoutes.push(transToGEOJson(coordinates));
  });
  
  if (route.decodeRoutes && route.decodeRoutes.length > 0) {
    const criticalResult = await weather.getGridOfCritical([route]);
    result = await weather.getGridsofRoutes([route]);
  }
  
  // AI message generation for different weather scenarios
  const message = await weather.getAIMessage(weatherInfos, language, tripInfo, timing);
};
```
- Extracts polylines from trip sections
- Decodes HERE Maps polylines to coordinates
- Integrates critical weather events with regular forecasts
- Generates AI-powered contextual weather messages

### Reservation Creation

### create Function
**Purpose:** Creates new reservations with comprehensive conflict management

```javascript
create: async (input) => {
  const curTime = moment.utc().format(TIME_FORMAT);
  
  // Fetch last app location from MongoDB
  const [lastAppLocation] = await AppStates.find({ user_id: userId })
    .sort({ timestamp: -1 })
    .limit(1);
    
  // Insert reservation data
  const insertResult = await Reservation.query().insert(inserDate);
  
  // Generate route polyline using HERE Maps
  const hereRoutingResult = await hereRouting('car', originCoords, destCoords, 'polyline', 'POST Reservation');
  
  const oCoordinates = poly.decode(polyline).polyline;
  const rCoordinates = oCoordinates.map(place => [place[1], place[0]]);
  
  // Store polyline data in MongoDB
  await ReservationPolyline.updateOne(
    { reservation_id: insertResult.id },
    {
      reservation_id: insertResult.id,
      polyline,
      trip_geojson: {
        type: 'LineString',
        coordinates: rCoordinates
      }
    },
    { upsert: true }
  );
  
  // Handle conflicts and suggestion cards
  const conflictOfferIds = cancelUnpairedConflict(userId, input.started_on, input.estimated_arrival_on);
  if (input.card_id) {
    await updateSuggestionCard(userId, input.card_id);
  }
  
  return { id: insertResult.id, conflictOfferIds };
}
```

### Conflict Resolution

### cancelUnpairedConflict Function
**Purpose:** Automatically cancels time-conflicting unpaired reservations

```javascript
const cancelUnpairedConflict = async (userId, startOn, endOn) => {
  const conflicts = await Reservation.query()
    .where('user_id', userId)
    .whereIn('status', [Reservation.status.NONE, Reservation.status.SEARCHING, Reservation.status.CHOOSING, Reservation.status.PENDING]);
    
  await Promise.all(
    conflicts.map(async (conflict) => {
      const conflictStart = conflict.started_on;
      const conflictEnd = conflict.started_off || conflict.estimated_arrival_on;
      
      if (moment(startOn).isBetween(conflictStart, conflictEnd, null, '[]') ||
          moment(endOn).isBetween(conflictStart, conflictEnd, null, '[]')) {
        
        if (conflict.duoReservation) {
          await Reservation.query().findById(conflict.id).patch({
            status: Reservation.status.REPEALED_CONFLICT
          });
        } else {
          await Reservation.query().findById(conflict.id).delete();
        }
      }
    })
  );
};
```

## 🚀 Usage Methods

### Basic Reservation Management
```javascript
const reservationService = require('@app/src/services/reservations');

// Get user reservations
const reservations = await reservationService.getAll({
  userId: 12345,
  travelMode: [2, 5, 7], // PUBLIC_TRANSIT, INTERMODAL, PARK_AND_RIDE
  offset: 0,
  perpage: 10,
  isToday: false
});

// Create new reservation
const newReservation = await reservationService.create({
  userId: 12345,
  travel_mode: 2,
  name: "Work Commute",
  origin: {
    name: "Home",
    address: "123 Main St",
    latitude: 29.7604,
    longitude: -95.3698,
    access_latitude: 0,
    access_longitude: 0
  },
  destination: {
    name: "Office", 
    address: "456 Business Ave",
    latitude: 29.7500,
    longitude: -95.3600,
    access_latitude: 0,
    access_longitude: 0
  },
  started_on: "2024-06-25 08:00:00",
  estimated_arrival_on: "2024-06-25 09:00:00",
  zone: "America/Chicago"
});

// Get trip details with weather
const tripDetail = await reservationService.getTripDetail({
  userId: 12345,
  reservationId: 67890,
  language: 'en'
});
```

### Advanced Carpool Management
```javascript
class CarpoolManager {
  constructor() {
    this.reservationService = require('@app/src/services/reservations');
  }

  async createCarpoolReservation(driverData, passengerData) {
    const carpoolUuid = require('uuid').v4();
    
    // Create driver reservation
    const driverReservation = await this.reservationService.create({
      ...driverData,
      travel_mode: 100, // DUO
      role: 1, // DRIVER
      carpool_uuid: carpoolUuid
    });
    
    // Create passenger reservation  
    const passengerReservation = await this.reservationService.create({
      ...passengerData,
      travel_mode: 100, // DUO
      role: 2, // PASSENGER
      carpool_uuid: carpoolUuid
    });
    
    return {
      driverReservationId: driverReservation.id,
      passengerReservationId: passengerReservation.id,
      carpoolUuid
    };
  }

  async getPartnerDetails(reservationId, userId) {
    const reservations = await this.reservationService.getAll({
      userId,
      travelMode: [100],
      offset: 0,
      perpage: 50,
      isToday: false
    });
    
    const myReservation = reservations.reservations.find(r => r.id === reservationId);
    if (myReservation && myReservation.riders) {
      return myReservation.riders.map(rider => ({
        userId: rider.user.user_id,
        name: `${rider.user.name.first_name} ${rider.user.name.last_name}`,
        rating: rider.user.rating,
        role: rider.role,
        price: rider.price,
        vehicle: rider.user.vehicle,
        timeToPickup: rider.time_to_pickup,
        timeToDropoff: rider.time_to_dropoff
      }));
    }
    
    return [];
  }
}
```

## 📊 Output Examples

### Reservation List Response
```json
{
  "total_count": 5,
  "next_offset": 10,
  "reservations": [
    {
      "id": 12345,
      "travel_mode": 2,
      "name": "Morning Commute",
      "role": null,
      "origin": {
        "name": "Home",
        "address": "123 Main St, Houston, TX",
        "latitude": 29.7604,
        "longitude": -95.3698
      },
      "destination": {
        "name": "Downtown Office",
        "address": "456 Business Ave, Houston, TX", 
        "latitude": 29.7500,
        "longitude": -95.3600
      },
      "started_on": "2024-06-25T13:00:00.000Z",
      "estimated_arrival_on": "2024-06-25T14:00:00.000Z",
      "status": 50,
      "is_uis_alert": true
    }
  ],
  "security_key": "abc123xyz"
}
```

### Trip Detail with Weather
```json
{
  "trip_detail_uuid": "123e4567-e89b-12d3-a456-426614174000",
  "user_id": 12345,
  "name": "Morning Commute",
  "reservation_id": 67890,
  "started_on": "2024-06-25T13:00:00.000Z",
  "ended_on": "2024-06-25T14:00:00.000Z",
  "estimated_time": 60,
  "total_price": 2.50,
  "sections": [
    {
      "type": "pedestrian",
      "transport": {"mode": "pedestrian"},
      "departure": {"time": "2024-06-25T13:00:00.000Z"},
      "arrival": {"time": "2024-06-25T13:05:00.000Z"}
    },
    {
      "type": "transit",
      "transport": {
        "mode": "bus",
        "route_id": "82",
        "is_uis_alert": true
      },
      "departure": {"time": "2024-06-25T13:10:00.000Z"},
      "arrival": {"time": "2024-06-25T13:50:00.000Z"}
    }
  ],
  "weather_alert": {
    "id": 67890,
    "title": "Weather Alert",
    "description": "Light rain expected during your trip. Consider bringing an umbrella.",
    "info_url": "https://weather.example.com/rain",
    "last_expire_time": "2024-06-25T18:00:00.000Z"
  }
}
```

### Carpool Partners Response
```json
{
  "riders": [
    {
      "offer_id": 54321,
      "reservation_id": 98765,
      "role": 2,
      "user": {
        "user_id": 11111,
        "name": {
          "first_name": "John",
          "last_name": "Doe"
        },
        "avatar": "https://s3.amazonaws.com/bucket/avatar123.jpg",
        "rating": 4.8
      },
      "origin": {
        "name": "Passenger Pickup",
        "latitude": 29.7610,
        "longitude": -95.3690
      },
      "destination": {
        "name": "Passenger Dropoff", 
        "latitude": 29.7480,
        "longitude": -95.3580
      },
      "price": 8.50,
      "time_to_pickup": 300,
      "time_to_dropoff": 180
    }
  ]
}
```

## ⚠️ Important Notes

### Complex Data Relationships
- **Multi-Database Architecture:** Uses both MySQL and MongoDB for different data types
- **Carpool Matching:** Complex partner matching via carpool_uuid and role-based pricing
- **Dynamic Pricing:** Unit price calculations with transaction fees based on user roles
- **Transit Integration:** Real-time GTFS alert monitoring with route-specific targeting

### Real-Time Features
- **Transit Alerts:** Live bus route disruption notifications from GTFS data
- **Weather Integration:** AI-powered weather alerts with route-specific forecasting
- **Conflict Resolution:** Automatic cancellation of overlapping reservations
- **Location Tracking:** Integration with user's last known app location

### Performance Considerations
- **Complex SQL Queries:** Optimized multi-table joins for carpool and payment data
- **Pagination Support:** Efficient offset-based pagination for large datasets
- **Async Processing:** Parallel processing of weather and transit alert data
- **Polyline Caching:** HERE Maps polyline storage for route visualization

### Business Logic Implementation
- **Travel Mode Support:** Handles driving, transit, carpool, intermodal, and park-and-ride
- **Role-Based Pricing:** Different fee structures for drivers vs passengers
- **Suggestion Card Integration:** Links with campaign management system
- **Trip Detail Management:** Comprehensive trip planning data storage

## 🔗 Related File Links

- **HERE Routing Service:** `allrepo/connectsmart/tsp-api/src/services/hereRouting.js`
- **Weather Service:** `allrepo/connectsmart/tsp-api/src/services/weather.js`
- **Polyline Service:** `allrepo/connectsmart/tsp-api/src/services/hereMapPolylines.js`
- **Reservation Models:** `allrepo/connectsmart/tsp-api/src/models/Reservations.js`

---
*This service provides comprehensive trip reservation management with advanced carpool matching, real-time alerts, and weather integration for the TSP platform.*