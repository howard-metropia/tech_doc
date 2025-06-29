# RoadTemporaryClosure Model Documentation

## 📋 Model Overview
- **Purpose:** Manages temporary road closures and traffic restrictions
- **Table/Collection:** road_temporary_closure
- **Database Type:** MySQL
- **Relationships:** May reference road networks and incident reports

## 🔧 Schema Definition
| **Field Name** | **Type** | **Required** | **Description** |
|----------------|----------|--------------|------------------|
| id | Integer | Yes | Primary key (auto-increment) |
| road_name | String | - | Name of affected road |
| location | String | - | Specific location description |
| closure_type | String | - | Type of closure (full, partial, lane) |
| start_date | DateTime | - | Closure start date and time |
| end_date | DateTime | - | Expected closure end date |
| reason | String | - | Reason for closure |
| description | Text | - | Detailed closure description |
| latitude | Decimal | - | Latitude coordinate |
| longitude | Decimal | - | Longitude coordinate |
| affected_direction | String | - | Traffic direction affected |
| alternative_route | Text | - | Suggested detour information |
| status | String | - | Active, scheduled, completed |
| authority | String | - | Agency responsible for closure |
| contact_info | String | - | Contact information |
| created_at | DateTime | - | Record creation timestamp |
| updated_at | DateTime | - | Record update timestamp |

## 🔑 Key Information
- **Primary Key:** id
- **Indexes:** Likely on road_name, status, start_date, latitude+longitude
- **Unique Constraints:** None
- **Default Values:** Auto-generated timestamps

## 📝 Usage Examples
```javascript
// Get active road closures
const activeClosures = await RoadTemporaryClosure.query()
  .where('status', 'active')
  .where('start_date', '<=', new Date())
  .where('end_date', '>=', new Date());

// Find closures by location
const nearbyClosures = await RoadTemporaryClosure.query()
  .whereRaw(`
    ST_Distance_Sphere(
      POINT(longitude, latitude),
      POINT(?, ?)
    ) <= 5000
  `, [userLng, userLat]);

// Schedule new closure
const closure = await RoadTemporaryClosure.query().insert({
  road_name: 'Main Street',
  location: 'Between 1st and 2nd Ave',
  closure_type: 'full',
  start_date: startDate,
  end_date: endDate,
  reason: 'Construction',
  status: 'scheduled'
});
```

## 🔗 Related Models
- **ConstructionZone**: May reference related construction activities
- **TrafficIncidents**: Related to incident-based closures
- **RoadNetwork**: References road infrastructure data

## 📌 Important Notes
- Time-based closure management with start/end dates
- Geographic coordinates for location-based queries
- Status tracking for closure lifecycle
- Alternative route suggestions for user guidance
- Authority and contact information for coordination

## 🏷️ Tags
**Keywords:** road-closure, temporary, traffic, construction
**Category:** #model #database #transportation #incidents