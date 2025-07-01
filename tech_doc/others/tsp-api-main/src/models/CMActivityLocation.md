# CMActivityLocation Model Documentation

## 📋 Model Overview
- **Purpose:** Stores campaign management activity location data for targeted campaigns
- **Table/Collection:** cm_activity_location
- **Database Type:** MySQL
- **Relationships:** Related to campaign management and user activities

## 🔧 Schema Definition
| **Field Name** | **Type** | **Required** | **Description** |
|----------------|----------|--------------|------------------|
| id | Integer | Yes | Primary key (auto-increment) |
| campaign_id | Integer | - | Associated campaign identifier |
| activity_id | Integer | - | Activity identifier |
| location_type | String | - | Type of location (poi, address, etc.) |
| location_data | JSON | - | Geographic location data |
| latitude | Decimal | - | Latitude coordinate |
| longitude | Decimal | - | Longitude coordinate |
| radius | Integer | - | Geofence radius in meters |
| address | String | - | Human-readable address |
| name | String | - | Location name/label |
| is_active | Boolean | - | Whether location is active |
| created_at | DateTime | - | Record creation timestamp |
| updated_at | DateTime | - | Record update timestamp |

## 🔑 Key Information
- **Primary Key:** id
- **Indexes:** Likely on campaign_id, activity_id, latitude+longitude
- **Unique Constraints:** None
- **Default Values:** Auto-generated timestamps, is_active default true

## 📝 Usage Examples
```javascript
// Add location to campaign activity
const location = await CMActivityLocation.query().insert({
  campaign_id: 123,
  activity_id: 456,
  location_type: 'poi',
  latitude: 37.7749,
  longitude: -122.4194,
  radius: 100,
  name: 'Downtown Mall',
  is_active: true
});

// Find nearby campaign locations
const nearbyLocations = await CMActivityLocation.query()
  .where('is_active', true)
  .whereRaw(`
    ST_Distance_Sphere(
      POINT(longitude, latitude),
      POINT(?, ?)
    ) <= radius
  `, [userLng, userLat]);
```

## 🔗 Related Models
- **Campaigns**: Locations belong to specific campaigns
- **Activities**: Activities can have multiple locations
- **UserActivities**: User interactions with location-based activities

## 📌 Important Notes
- Used for location-based campaign targeting
- Supports geofencing with configurable radius
- Geographic queries require spatial indexing
- Part of campaign management (CM) system

## 🏷️ Tags
**Keywords:** campaign-management, location, geofencing, targeting
**Category:** #model #database #campaigns #geospatial