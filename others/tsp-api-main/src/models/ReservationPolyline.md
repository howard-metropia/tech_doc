# ReservationPolyline Model Documentation

## 📋 Model Overview
- **Purpose:** Stores reservation polyline data with GeoJSON trip geometry
- **Table/Collection:** reservation_polyline
- **Database Type:** MongoDB
- **Relationships:** Links to reservations and users via IDs

## 🔧 Schema Definition
- **Field Name** | **Type** | **Required** | **Description**
- reservation_id | Number | Yes | Reference to reservation record
- trip_geojson | Object (GeoJSON) | No | LineString geometry for trip route
- user_id | Number | Yes | Reference to user who owns reservation
- created_on | String | Yes | Timestamp of record creation
- polyline | String | Yes | Encoded polyline representation of route

### Nested Schema: tripLineSchema
- **type** | String | Yes | Must be "LineString" for GeoJSON
- **coordinates** | Array of Arrays | Yes | Array of [longitude, latitude] coordinate pairs

## 🔑 Key Information
- **Primary Key:** _id (MongoDB default)
- **Indexes:** 
  - reservation_id (single field index)
  - trip_geojson (2dsphere geospatial index)
- **Unique Constraints:** None explicitly defined
- **Default Values:** None specified

## 📝 Usage Examples
```javascript
// Find reservation polylines by reservation ID
const polylines = await ReservationPolyline.find({ reservation_id: 12345 });

// Create new reservation polyline
const reservationPolyline = new ReservationPolyline({
  reservation_id: 12345,
  user_id: 67890,
  created_on: new Date().toISOString(),
  polyline: "encodedPolylineString",
  trip_geojson: {
    type: "LineString",
    coordinates: [[-122.4194, 37.7749], [-122.4094, 37.7849]]
  }
});
```

## 🔗 Related Models
- **Reservations** - Referenced by reservation_id
- **Users** - Referenced by user_id
- **Trip management models** - Related through reservation system

## 📌 Important Notes
- Uses 2dsphere index for efficient geospatial queries on trip_geojson
- Stores both encoded polyline and GeoJSON formats for flexibility
- Created_on field stored as string rather than Date object
- Optimized for location-based queries and route visualization

## 🏷️ Tags
**Keywords:** reservation, polyline, geojson, route, trip, geospatial
**Category:** #model #database #mongodb #geospatial #reservation