# pmParkingEvents Model Documentation

## 📋 Model Overview
- **Purpose:** Logs ParkMobile parking events with API responses and user context
- **Table/Collection:** pm_parking_events
- **Database Type:** MongoDB
- **Relationships:** Links to users via user_id for parking event tracking

## 🔧 Schema Definition
- **Field Name** | **Type** | **Required** | **Description**
- _id | String | No | Custom string identifier
- card | String | No | Payment card identifier used
- http_status | Number or String | No | HTTP response status code
- response | Object | No | API response data from ParkMobile
- payload | Object | No | Request payload sent to ParkMobile
- user_id | Number | No | Reference to user who initiated event
- createdAt | Date | Auto | Timestamp when record was created
- updatedAt | Date | Auto | Timestamp when record was last updated

## 🔑 Key Information
- **Primary Key:** _id (custom String type)
- **Indexes:** No custom indexes defined
- **Unique Constraints:** None explicitly defined
- **Default Values:** 
  - createdAt and updatedAt (automatic timestamps)

## 📝 Usage Examples
```javascript
// Find parking events for a specific user
const userEvents = await PmParkingEvents.find({ user_id: 12345 });

// Find recent successful parking events
const successfulEvents = await PmParkingEvents.find({
  http_status: 200,
  createdAt: { $gte: new Date(Date.now() - 24*60*60*1000) }
});

// Log a new parking event
const parkingEvent = new PmParkingEvents({
  _id: 'unique-event-id',
  card: 'card-12345',
  http_status: 200,
  response: { success: true, session_id: 'abc123' },
  payload: { zone: 'downtown', duration: 120 },
  user_id: 67890
});
```

## 🔗 Related Models
- **User models** - Referenced by user_id for event attribution
- **Payment models** - Related through card payment processing
- **Parking session models** - Connected via parking transaction flow

## 📌 Important Notes
- Uses automatic timestamps for audit trail
- Custom string _id instead of MongoDB ObjectId
- Stores both request payload and response for debugging
- HTTP status can be Number or String type for flexibility
- Connected to 'dataset' MongoDB database for operational logging
- Critical for ParkMobile API integration monitoring and troubleshooting

## 🏷️ Tags
**Keywords:** parkmobile, parking, events, logging, api, integration
**Category:** #model #database #mongodb #parking #logging