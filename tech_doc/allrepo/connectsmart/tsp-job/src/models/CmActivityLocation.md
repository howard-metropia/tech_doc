# CmActivityLocation Model

## Overview
Campaign management activity-location relationship model for the TSP Job system. Links activities to specific locations for targeted campaigns and location-based promotions.

## Model Definition
```javascript
const knex = require('@maas/core/mysql')('portal');
class CmActivityLocation extends Model {
  static get tableName() {
    return 'cm_activity_location';
  }
}
module.exports = CmActivityLocation.bindKnex(knex);
```

## Database Configuration
- **Database**: Portal MySQL instance
- **Table**: `cm_activity_location`
- **ORM**: Objection.js with Knex query builder

## Purpose
- Activity-location relationship management
- Location-based activity targeting
- Geographic campaign coordination
- Spatial activity analysis

## Relationship Types
- **Activity Venues**: Where activities occur
- **Service Locations**: Transportation service points
- **Promotion Areas**: Marketing campaign zones  
- **Event Locations**: Special event venues

## Key Features
- Many-to-many relationship support
- Geographic activity mapping
- Location-based targeting
- Spatial relationship analysis

## Activity Categories
- **Transportation**: Transit stops, stations
- **Commercial**: Shopping, dining venues
- **Recreation**: Entertainment, sports facilities
- **Business**: Offices, meeting locations
- **Healthcare**: Medical facilities

## Integration Points
- **CmLocation**: Location definitions
- **ActivityArea**: Geographic boundaries
- **CmActivityMod**: Activity modifications
- **Trips**: Location-based trip analysis

## Campaign Applications
- Location-specific promotions
- Activity-based targeting
- Geographic campaign optimization
- Venue-specific offers

## Spatial Analysis
- Activity density mapping
- Location popularity metrics
- Geographic distribution analysis
- Accessibility assessments

## Performance Features
- Efficient relationship queries
- Spatial indexing support
- Fast location-activity lookups
- Scalable for large datasets

## Related Models
- CmLocation: Location data
- ActivityArea: Geographic regions
- CmActivityMod: Activity changes
- Trips: Trip-location analysis

## Development Notes
- Relationship model design
- Spatial query optimization
- Campaign targeting support
- Analytics integration essential