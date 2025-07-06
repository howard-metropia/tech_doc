# HoustonRoutes Model

## 📋 Model Overview
- **Purpose:** Manages transit route information for Houston Metro system
- **Table/Collection:** routes
- **Database Type:** MySQL (houston)
- **Relationships:** None defined

## 🔧 Schema Definition
*Schema fields are not explicitly defined in the model. Database table structure would need to be verified.*

## 🔑 Key Information
- **Primary Key:** Not explicitly defined (likely `id`)
- **Indexes:** Not specified
- **Unique Constraints:** Not specified
- **Default Values:** Not specified

## 📝 Usage Examples
```javascript
// Basic query example
const routes = await Routes.query().where('status', 'active');

// Get routes by type
const busRoutes = await Routes.query().where('route_type', 'bus');
```

## 🔗 Related Models
- No explicit relationships defined
- Part of Houston Metro transit system

## 📌 Important Notes
- Minimal model with only table name definition
- Uses dedicated Houston database connection
- Part of Houston Metro transit integration
- Uses Objection.js ORM with MySQL houston database

## 🏷️ Tags
**Keywords:** houston, routes, transit, metro, gtfs
**Category:** #model #database #houston #routes #transit