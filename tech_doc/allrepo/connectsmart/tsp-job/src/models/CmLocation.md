# CmLocation Model

## Overview
Campaign management location model for the TSP Job system. Handles location-based campaigns, geographic targeting, and location-specific marketing initiatives.

## Model Definition
```javascript
const knex = require('@maas/core/mysql')('portal');
class CmLocation extends Model {
  static get tableName() {
    return 'cm_location';
  }
}
module.exports = CmLocation.bindKnex(knex);
```

## Database Configuration
- **Database**: Portal MySQL instance
- **Table**: `cm_location`
- **ORM**: Objection.js with Knex query builder

## Purpose
- Location-based campaign management
- Geographic marketing targeting
- Location-specific promotions
- Regional service campaigns

## Location Types
- **Points of Interest**: Specific venues and landmarks
- **Geographic Regions**: Cities, neighborhoods, districts
- **Service Areas**: Transportation service boundaries
- **Commercial Zones**: Business and retail areas
- **Transit Hubs**: Stations and transportation centers

## Key Features
- Precise geographic targeting
- Campaign location management
- Regional promotion support
- Location-based analytics

## Campaign Applications
- **Regional Promotions**: Area-specific offers
- **Event-Based Campaigns**: Location-tied events
- **Service Launches**: Geographic rollouts
- **Seasonal Campaigns**: Location-specific timing

## Integration Points
- **CmActivityLocation**: Activity-location relationships
- **ActivityArea**: Geographic boundaries
- **Trips**: Location-based trip analysis
- **UserActions**: Location-specific behaviors

## Geographic Features
- Coordinate-based positioning
- Radius-based targeting
- Polygon boundary definition
- Multi-location campaigns

## Analytics Support
- Location performance metrics
- Regional campaign effectiveness
- Geographic user behavior
- Spatial campaign analysis

## Related Models
- CmActivityLocation: Activity relationships
- ActivityArea: Geographic boundaries
- Trips: Location-based trips
- CmActivityMod: Activity modifications

## Development Notes
- Geographic precision critical
- Campaign targeting focus
- Analytics integration important
- Spatial query optimization needed