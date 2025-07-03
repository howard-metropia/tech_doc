# DBUsers Model

## Overview
Dataset-specific user model for analytics and data processing operations in the TSP Job system. Handles user data in the dataset database layer.

## Model Definition
```javascript
const knex = require('@maas/core/mysql')('dataset');
class DBUsers extends Model {
  static get tableName() {
    return 'DBUser';
  }
}
module.exports = DBUsers.bindKnex(knex);
```

## Database Configuration
- **Database**: Dataset MySQL instance
- **Table**: `DBUser`
- **ORM**: Objection.js with Knex query builder
- **Connection**: Managed by @maas/core MySQL connection pool

## Purpose
- User data analytics and processing
- Dataset-specific user information storage
- Analytics pipeline user management
- Data warehouse user entity

## Key Features
- Dataset database connectivity
- Analytics-focused user data structure
- Separation from operational user data
- Optimized for data processing workflows

## Integration Points
- **Analytics Services**: User behavior analysis
- **Data Processing**: Batch user data operations
- **Reporting Systems**: User metrics and statistics
- **ETL Pipelines**: User data transformation

## Usage Context
Used in data analytics, reporting, and batch processing operations where user information needs to be accessed from the dataset database rather than the operational portal database.

## Database Schema
The model maps to the `DBUser` table which contains:
- User analytical data
- Processed user metrics
- Historical user information
- Analytics-specific user attributes

## Performance Considerations
- Optimized for analytical queries
- Batch processing friendly structure
- Separate from transactional database
- Indexed for reporting performance

## Data Flow
- Receives data from portal AuthUsers
- Processes user information for analytics
- Supports ETL operations
- Feeds reporting and dashboard systems

## Related Models
- AuthUsers: Source user data
- Trips: User travel analytics
- UserActions: User behavior tracking
- ClusterTrips: User pattern analysis

## API Integration
Used by:
- Analytics services
- Reporting endpoints
- Data processing jobs
- Dashboard data feeds

## Development Notes
- Separated from operational data for performance
- Follows dataset model naming conventions
- Supports complex analytical queries
- Compatible with data warehouse patterns