# RidehailTrips Model Documentation

## 📋 Model Overview
- **Purpose:** Manages ridehail trip records and booking information
- **Table/Collection:** ridehail_trip
- **Database Type:** MySQL
- **Relationships:** References users, vehicles, and payment records

## 🔧 Schema Definition
| **Field Name** | **Type** | **Required** | **Description** |
|----------------|----------|--------------|------------------|
| id | Integer | Yes | Primary key (auto-increment) |
| user_id | Integer | - | User who booked the ride |
| driver_id | Integer | - | Assigned driver ID |
| vehicle_id | Integer | - | Vehicle used for trip |
| trip_status | String | - | Requested, accepted, in_progress, completed, cancelled |
| pickup_address | String | - | Pickup location address |
| pickup_lat | Decimal | - | Pickup latitude |
| pickup_lng | Decimal | - | Pickup longitude |
| destination_address | String | - | Destination address |
| destination_lat | Decimal | - | Destination latitude |
| destination_lng | Decimal | - | Destination longitude |
| requested_at | DateTime | - | Trip request timestamp |
| accepted_at | DateTime | - | When driver accepted |
| pickup_at | DateTime | - | Actual pickup time |
| completed_at | DateTime | - | Trip completion time |
| fare_amount | Decimal | - | Total fare amount |
| payment_method | String | - | Payment method used |
| rating | Integer | - | User rating (1-5) |
| created_at | DateTime | - | Record creation timestamp |
| updated_at | DateTime | - | Record update timestamp |

## 🔑 Key Information
- **Primary Key:** id
- **Indexes:** Likely on user_id, driver_id, trip_status, requested_at
- **Unique Constraints:** None
- **Default Values:** Auto-generated timestamps

## 📝 Usage Examples
```javascript
// Book new ridehail trip
const trip = await RidehailTrips.query().insert({
  user_id: userId,
  pickup_address: 'Downtown Mall',
  pickup_lat: 37.7749,
  pickup_lng: -122.4194,
  destination_address: 'Airport Terminal',
  destination_lat: 37.6213,
  destination_lng: -122.3790,
  trip_status: 'requested'
});

// Get user's active trips
const activeTrips = await RidehailTrips.query()
  .where('user_id', userId)
  .whereIn('trip_status', ['requested', 'accepted', 'in_progress']);

// Complete trip
await RidehailTrips.query()
  .where('id', tripId)
  .patch({
    trip_status: 'completed',
    completed_at: new Date(),
    fare_amount: 25.50
  });
```

## 🔗 Related Models
- **AuthUsers**: Trip belongs to specific user
- **Drivers**: Trip assigned to specific driver
- **Vehicles**: References vehicle used for trip
- **Payments**: Associated payment transactions

## 📌 Important Notes
- Core model for ridehail service operations
- Tracks complete trip lifecycle from request to completion
- Geographic coordinates for pickup and destination
- Status-based workflow management
- Payment and rating integration

## 🏷️ Tags
**Keywords:** ridehail, trips, booking, transportation
**Category:** #model #database #ridehail #trips