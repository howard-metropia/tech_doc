# UberGuestRideLogs Model Documentation

## 📋 Model Overview
- **Purpose:** Tracks Uber ride logs for guest users and ride-hailing integration
- **Table/Collection:** uber_guest_ride_log
- **Database Type:** MySQL (portal database)
- **Relationships:** Links guest user rides with Uber service integration

## 🔧 Schema Definition
| **Field Name** | **Type** | **Required** | **Description** |
|----------------|----------|--------------|-----------------|
| id | INT | Yes | Primary key, auto-increment |
| guest_user_id | VARCHAR | No | Guest user identifier (non-registered users) |
| uber_request_id | VARCHAR | Yes | Uber API request identifier |
| uber_trip_id | VARCHAR | No | Uber trip identifier once assigned |
| ride_status | VARCHAR | No | Current ride status (requested, assigned, completed, cancelled) |
| origin_address | TEXT | No | Pickup location address |
| destination_address | TEXT | No | Drop-off location address |
| fare_estimate | DECIMAL | No | Estimated fare amount |
| actual_fare | DECIMAL | No | Final fare charged |
| request_time | TIMESTAMP | Yes | Time when ride was requested |
| completion_time | TIMESTAMP | No | Time when ride was completed |
| created_at | TIMESTAMP | Yes | Log entry creation timestamp |
| updated_at | TIMESTAMP | Yes | Last update timestamp |

## 🔑 Key Information
- **Primary Key:** id
- **Indexes:** guest_user_id, uber_request_id, uber_trip_id, ride_status
- **Unique Constraints:** uber_request_id
- **Default Values:** ride_status = 'requested', created_at = CURRENT_TIMESTAMP

## 📝 Usage Examples
```javascript
// Get guest user ride history
const guestRides = await UberGuestRideLogs.query()
  .where('guest_user_id', guestId)
  .orderBy('request_time', 'desc');

// Find active rides
const activeRides = await UberGuestRideLogs.query()
  .whereIn('ride_status', ['requested', 'assigned', 'in_progress']);

// Log new Uber ride request
await UberGuestRideLogs.query().insert({
  guest_user_id: guestId,
  uber_request_id: 'uber_req_123',
  origin_address: '123 Main St',
  destination_address: '456 Oak Ave',
  fare_estimate: 15.50,
  request_time: new Date()
});
```

## 🔗 Related Models
- Guest user tracking models
- Payment/billing models for ride charges
- Trip validation models for incentive programs

## 📌 Important Notes
- Specifically designed for guest (non-registered) users
- Integrates with Uber's ride-hailing API
- Tracks complete ride lifecycle from request to completion
- Used for analytics on guest user ride patterns
- Supports fare tracking and billing reconciliation

## 🏷️ Tags
**Keywords:** uber, ridehail, guest, logging, integration
**Category:** #model #database #ridehail #guest #mysql

---
Note: This model provides ride logging for guest users using Uber integration services.