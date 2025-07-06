# TSP Job Service: carpoolTripProcessing.js

## Quick Summary

The `carpoolTripProcessing.js` service handles automated cleanup and processing of stalled carpool trips within the ConnectSmart platform. It identifies trips that have exceeded their estimated completion time without proper closure, automatically ends them, processes refunds, and notifies affected users. This service ensures data integrity and user experience by preventing zombie trip states.

## Technical Analysis

### Core Architecture

The service implements an automated trip lifecycle management system with the following components:

- **Zombie Trip Detection**: Identifies trips that have exceeded completion timeouts
- **Automated Trip Closure**: Programmatically ends stalled trips with appropriate data
- **Escrow Refund Processing**: Handles passenger refunds for incomplete trips
- **Relationship Cleanup**: Updates reservation statuses and removes pairing relationships
- **User Notification**: Informs passengers about automated trip closures

### Key Functions

#### carpoolTripProcessing()
Main processing function that identifies and handles stalled trips:
```javascript
const sql = `
select 
  t.id as trip_id, t.reservation_id, t.user_id, t.role,
  r.route_meter, r.origin as reservation_origin,
  // ... extensive trip and reservation data
from trip t
join reservation r on r.id = t.reservation_id
join duo_reservation drv on drv.reservation_id = r.id
// ... complex joins for carpool relationships
where 
  t.travel_mode = 100 
  and t.ended_on is null 
  and t.role = 1 
  and r.status = 60 
  and (select max(status) from duo_realtime where trip_id = driver_trip.id) < 8
  and date_add(t.estimated_arrival_on, interval 7200 second) < current_timestamp()
`;
```

#### endTrip()
Handles the technical closure of stalled trips:
```javascript
async function endTrip(tripId, endedOn, destination, lat, lon, eta, distance, passengerId, passengerTripId, partnerReservationId) {
  const data = {
    destination,
    destination_latitude: lat,
    destination_longitude: lon,
    ended_on: endedOn,
    distance,
    estimated_arrival_on: eta,
  };
  
  // Update both driver and passenger trips
  await knex('trip').where({ id: tripId }).update(data);
  await knex('trip').where({ id: passengerTripId }).update(data);
  
  // Add final realtime status
  await knex('duo_realtime').insert({
    trip_id: tripId,
    status: 11, // DUO_REALTIME_STATUS_ENDED
    latitude: lat,
    longitude: lon,
    estimated_arrival_time: dbtimeToTimestamp(eta),
    passenger_id: passengerId,
    record_on: jstimeToDbtime(new Date()),
  });
}
```

#### cancelCarpoolReutrnPassenger()
Simplified escrow refund processing for passengers:
```javascript
async function cancelCarpoolReutrnPassenger(passengerId, reservationId) {
  const escrow = await knex('escrow').where({ 
    user_id: passengerId, 
    reservation_id: reservationId 
  }).first();
  
  if (escrow) {
    const { escrowNet } = await escrowTotal(passengerId, reservationId);
    await knex.transaction(async trx => {
      if (escrowNet > 0) {
        await add_escrow_detail(
          trx, passengerId, escrow.id,
          activity_types.ESCROW_ACTIVITY_DEC_CARPOOL_CANCEL_BY_DRIVER_NO_SHOW,
          0 - escrowNet, reservationId, jstimeToDbtime(new Date())
        );
      }
      await close_escrow(trx, passengerId, reservationId);
    });
  }
}
```

#### renewCarpoolRelation()
Cleans up reservation relationships after trip processing:
```javascript
async function renewCarpoolRelation(driverReservationId, passengerReservationId) {
  await knex('reservation')
    .whereIn('id', [driverReservationId, passengerReservationId])
    .update({
      status: 52, // RESERVATION_STATUS_CANCELED_INACTION
      modified_on: jstimeToDbtime(new Date()),
    });
}
```

### Data Processing Logic

#### Distance Calculation Priority
The service uses a fallback hierarchy for trip distance:
```javascript
let distance = 0;
if (row.trip_distance) {
  distance = row.trip_distance; // Actual recorded distance
} else if (row.trip_trajectory_distance) {
  distance = row.trip_trajectory_distance; // Calculated trajectory
} else if (row.route_meter) {
  distance = row.route_meter; // Original route estimate
}
```

#### Destination Resolution
Determines final destination using available data:
```javascript
const destination = {
  name: row.reservation_destination,
  address: row.reservation_destination,
  latitude: row.reservation_destination_latitude,
  longitude: row.reservation_destination_longitude,
};

// Override with trip-specific destination if available
if (row.trip_destination && row.trip_destination_latitude && row.trip_destination_longitude) {
  destination.name = row.trip_destination;
  destination.address = row.trip_destination;
  destination.latitude = row.trip_destination_latitude;
  destination.longitude = row.trip_destination_longitude;
}
```

## Usage/Integration

### Scheduled Execution

This service is typically executed as a scheduled job to process stalled trips:

```javascript
// Called by job scheduler (e.g., every 30 minutes)
const { carpoolTripProcessing } = require('./carpoolTripProcessing');

const results = await carpoolTripProcessing();
console.log(`Processed ${results.length} stalled trips`);
```

### Integration with Notification System

Automatically notifies affected passengers:
```javascript
const profile = (await profiles([row.passenger_id]))[0];
await sendNotification({
  userIds: [row.passenger_id],
  titleParams: [],
  bodyParams: [profile.full_name],
  type: notificationType.DUO_END_ZOMBIE_TRIP,
  meta: {},
  silent: false,
});
```

### Error Handling Strategy

Comprehensive error handling ensures partial processing continues:
```javascript
for (const row of rows) {
  let updatedTrip = {};
  try {
    // Process individual trip
    updatedTrip = await endTrip(/* parameters */);
    await renewCarpoolRelation(row.reservation_id, row.partner_reservation_id);
    // ... notification logic
  } catch (e) {
    logger.error(`[carpool_trip_processing] error: ${e.message}`);
    logger.debug(`[carpool_trip_processing] stack: ${e.stack}`);
  }
  result.push({ row, updatedTrip });
}
```

## Dependencies

### External Packages
- `@maas/core/log`: Centralized logging system
- `@maas/core/mysql`: Database connectivity for portal database

### Internal Services
- `@app/src/helpers/send-notification`: Push notification system
- `@app/src/static/defines`: Notification type constants
- `@app/src/services/user`: User profile management
- `@app/src/services/carpoolHandler`: Escrow operations
- `@app/src/services/escrow`: Escrow detail management

### Database Schema Dependencies
- **trip**: Core trip records
- **reservation**: Carpool reservations
- **duo_reservation**: Pairing relationships
- **duo_realtime**: Real-time trip status
- **escrow**: Financial escrow accounts
- **match_statistic**: Matching statistics

## Code Examples

### Manual Trip Processing
```javascript
const { carpoolTripProcessing } = require('./carpoolTripProcessing');

// Process all stalled trips
const processingResults = await carpoolTripProcessing();

processingResults.forEach(result => {
  console.log(`Trip ${result.row.trip_id} processed:`, result.updatedTrip);
});
```

### Individual Trip Closure
```javascript
// End a specific trip manually
const updatedTrip = await endTrip(
  12345,                    // tripId
  '2023-12-01 15:30:00',   // endedOn
  'Downtown Station',       // destination
  32.7767,                 // latitude
  -96.7970,                // longitude
  '2023-12-01 15:35:00',   // estimatedArrivalOn
  8500,                    // distance in meters
  67890,                   // passengerId
  54321,                   // passengerTripId
  98765                    // partnerReservationId
);
```

### Escrow Refund Processing
```javascript
// Process passenger refund for cancelled trip
await cancelCarpoolReutrnPassenger(
  67890,  // passengerId
  98765   // reservationId
);
```

### Time Conversion Utilities
```javascript
// Convert JavaScript time to database format
const dbTime = jstimeToDbtime(new Date());
console.log(dbTime); // "2023-12-01 15:30:00"

// Convert database time to timestamp
const timestamp = dbtimeToTimestamp('2023-12-01 15:30:00');
console.log(timestamp); // Unix timestamp
```

### Trip Query Results Structure
```javascript
// Each processed row contains:
{
  trip_id: 12345,
  reservation_id: 67890,
  user_id: 54321,
  role: 1, // Driver
  route_meter: 8500,
  reservation_origin: 'Home Address',
  reservation_destination: 'Work Address',
  trip_distance: 8200,
  passenger_id: 98765,
  partner_reservation_id: 11111
}
```

The carpoolTripProcessing service provides essential maintenance functionality for the carpool system, ensuring that stalled trips are properly closed, users are refunded appropriately, and the system maintains data integrity even when trips don't complete normally.