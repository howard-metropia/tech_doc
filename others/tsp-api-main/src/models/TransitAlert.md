# TransitAlert Model

## 📋 Model Overview
- **Purpose:** Manages transit alerts for RideMetro transit system
- **Table/Collection:** ridemetro_transit_alert
- **Database Type:** MySQL (gtfs)
- **Relationships:** BelongsTo TransitAlertRoute

## 🔧 Schema Definition
*Schema fields are not explicitly defined in the model. Database table structure would need to be verified.*
- **event_id** | **String/Integer** | **Required** | **Alert event identifier**

## 🔑 Key Information
- **Primary Key:** Not explicitly defined (likely `id` or `event_id`)
- **Indexes:** event_id (foreign key)
- **Unique Constraints:** Not specified
- **Default Values:** Not specified

## 📝 Usage Examples
```javascript
// Basic query example
const alerts = await TransitAlert.query().where('status', 'active');

// With route relation
const alertsWithRoute = await TransitAlert.query()
  .withGraphFetched('route')
  .where('event_id', 'ALERT_123');
```

## 🔗 Related Models
- `TransitAlertRoute` - Related through ridemetro_transit_alert_join_route table

## 📌 Important Notes
- Specific to RideMetro transit system
- Uses GTFS database for transit data
- Connected to routes through join table
- Part of real-time transit information system

## 🏷️ Tags
**Keywords:** transit, alert, ridemetro, gtfs, route
**Category:** #model #database #transit #alert #gtfs