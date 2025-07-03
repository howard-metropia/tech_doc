# UserRatings Model

## Overview
User rating and feedback management model for the TSP Job system. Handles user-generated ratings, reviews, and feedback across various services and experiences.

## Model Definition
```javascript
const knex = require('@maas/core/mysql')('portal');
class UserRatings extends Model {
  static get tableName() {
    return 'user_ratings';
  }
}
module.exports = UserRatings.bindKnex(knex);
```

## Database Configuration
- **Database**: Portal MySQL instance
- **Table**: `user_ratings`
- **ORM**: Objection.js with Knex query builder
- **Connection**: Managed by @maas/core MySQL connection pool

## Purpose
- User experience rating collection
- Service quality feedback
- Trip and service evaluation
- Community-driven quality metrics

## Key Features
- Multi-category rating system
- Review and comment support
- Rating aggregation capabilities
- Quality assurance mechanisms

## Rating Categories
- **Trip Experience**: Overall journey satisfaction
- **Service Quality**: Provider performance
- **Route Efficiency**: Path optimization feedback
- **App Usability**: User interface experience
- **Customer Support**: Help and assistance quality
- **Pricing Fairness**: Cost satisfaction

## Integration Points
- **AuthUsers**: Rating authorship
- **Trips**: Trip-specific ratings
- **UserActions**: Rating behavior tracking
- **HntbRating**: Specialized rating extensions

## Usage Context
Used for collecting user feedback, improving service quality, generating analytics reports, and providing community-driven quality metrics.

## Database Schema
Typical fields include:
- User ID reference
- Rated entity type and ID
- Rating score (1-5 scale)
- Review text content
- Rating categories
- Timestamps and metadata

## Quality Assurance
- Duplicate rating prevention
- Spam and abuse detection
- Rating authenticity verification
- Moderation workflow support

## Analytics Integration
- Rating trend analysis
- Service quality metrics
- User satisfaction tracking
- Performance improvement insights

## Performance Considerations
- Indexed rating lookups
- Efficient aggregation queries
- Cached rating summaries
- Optimized for high-volume operations

## Related Models
- AuthUsers: Rating ownership
- Trips: Trip rating relationships
- UserActions: Rating activity tracking
- HntbRating: Extended rating features

## API Integration
- Rating submission endpoints
- Review management APIs
- Analytics and reporting services
- Quality metrics dashboards

## Business Logic
- Rating validation rules
- Aggregation calculations
- Trend analysis algorithms
- Quality scoring mechanisms

## Development Notes
- Supports various rating scales
- Extensible for new rating categories
- Analytics-optimized structure
- Moderation and quality control features