# TripActivityMapping Model

## Overview
Trip-activity relationship mapping model for the TSP Job system. Links trips to specific activities, purposes, and contexts for enhanced analytics and personalization.

## Model Definition
```javascript
const knex = require('@maas/core/mysql')('portal');
class TripActivityMapping extends Model {
  static get tableName() {
    return 'trip_activity_mapping';
  }
}
module.exports = TripActivityMapping.bindKnex(knex);
```

## Database Configuration
- **Database**: Portal MySQL instance
- **Table**: `trip_activity_mapping`
- **ORM**: Objection.js with Knex query builder
- **Connection**: Managed by @maas/core MySQL connection pool

## Purpose
- Trip purpose classification
- Activity-based trip analysis
- Context-aware transportation
- Behavioral pattern recognition

## Activity Types
- **Work**: Commuting and business trips
- **Shopping**: Retail and commercial visits
- **Recreation**: Entertainment and leisure
- **Healthcare**: Medical appointments
- **Education**: School and training trips
- **Social**: Personal and family visits

## Key Features
- Multi-purpose trip support
- Activity inference algorithms
- Context-aware mapping
- Purpose-based analytics

## Mapping Methods
- **User Declared**: Explicitly stated purposes
- **Location Inferred**: Destination-based detection
- **Pattern Based**: Historical behavior analysis
- **Time Based**: Schedule and timing inference
- **Machine Learning**: Automated classification

## Integration Points
- **Trips**: Trip identification
- **ActivityArea**: Location context
- **CmActivityLocation**: Activity locations
- **UserActions**: Behavioral patterns

## Usage Context
Used for trip purpose analysis, personalized recommendations, activity-based planning, and transportation demand modeling.

## Analytics Applications
- Activity-based demand forecasting
- Purpose-specific service optimization
- Behavioral pattern analysis
- Personalized trip suggestions

## Performance Features
- Efficient activity lookups
- Fast purpose classification
- Scalable mapping algorithms
- Real-time inference support

## Related Models
- Trips: Trip data
- ActivityArea: Activity zones
- CmActivityLocation: Location activities
- UserActions: User behavior

## API Integration
- Trip purpose endpoints
- Activity classification services
- Analytics APIs
- Recommendation systems

## Machine Learning
- Purpose prediction models
- Activity pattern recognition
- Behavioral classification
- Continuous learning systems

## Development Notes
- Complex classification logic
- Machine learning integration
- Privacy-conscious design
- Analytics optimization focus