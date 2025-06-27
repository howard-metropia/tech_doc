# TransitAlertRoute Model Documentation

## 📋 Model Overview
- **Purpose:** Links transit alerts to specific routes in the RideMetro system
- **Table/Collection:** ridemetro_transit_alert_join_route
- **Database Type:** MySQL (gtfs database)
- **Relationships:** Junction table connecting transit alerts to routes

## 🔧 Schema Definition
| **Field Name** | **Type** | **Required** | **Description** |
|----------------|----------|--------------|-----------------|
| id | INT | Yes | Primary key, auto-increment |
| alert_id | INT | Yes | Foreign key to transit alerts table |
| route_id | VARCHAR | Yes | GTFS route identifier |
| route_short_name | VARCHAR | No | Route short name (e.g., "82") |
| route_long_name | VARCHAR | No | Route long name (e.g., "Westheimer") |
| affected_direction | INT | No | Direction affected (0=both, 1=inbound, 2=outbound) |
| created_at | TIMESTAMP | Yes | Record creation timestamp |
| updated_at | TIMESTAMP | Yes | Last update timestamp |

## 🔑 Key Information
- **Primary Key:** id
- **Indexes:** alert_id, route_id, (alert_id, route_id) composite
- **Unique Constraints:** (alert_id, route_id) combination
- **Default Values:** created_at = CURRENT_TIMESTAMP

## 📝 Usage Examples
```javascript
// Basic query example
const alertRoutes = await TransitAlertRoute.query()
  .where('alert_id', alertId);

// Get all alerts for a specific route
const routeAlerts = await TransitAlertRoute.query()
  .where('route_id', 'METRO_82')
  .orderBy('created_at', 'desc');

// Find alerts affecting specific direction
const inboundAlerts = await TransitAlertRoute.query()
  .where('route_id', routeId)
  .whereIn('affected_direction', [0, 1]); // Both or inbound
```

## 🔗 Related Models
- Transit alerts table (parent alert information)
- GTFS routes table (route details)
- Transit schedule tables for affected services

## 📌 Important Notes
- Part of GTFS (General Transit Feed Specification) implementation
- Route IDs follow GTFS standard format
- Affected direction allows granular alert targeting
- Used for real-time transit service disruption notifications

## 🏷️ Tags
**Keywords:** transit, alerts, routes, gtfs, ridemetro
**Category:** #model #database #transit #mysql

---
Note: This junction table enables many-to-many relationships between transit alerts and routes.