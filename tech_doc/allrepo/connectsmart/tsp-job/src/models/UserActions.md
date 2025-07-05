# UserActions Model

## Overview
User activity tracking model for the TSP Job system. Records user interactions, behaviors, and system events for analytics and personalization.

## Model Definition
```javascript
const knex = require('@maas/core/mysql')('portal');
class UserActions extends Model {
  static get tableName() {
    return 'user_actions';
  }
}
module.exports = UserActions.bindKnex(knex);
```

## Database Configuration
- **Database**: Portal MySQL instance
- **Table**: `user_actions`
- **ORM**: Objection.js with Knex query builder
- **Connection**: Managed by @maas/core MySQL connection pool

## Purpose
- User behavior tracking
- Activity analytics
- Personalization data collection
- System usage monitoring

## Action Types
- **App Interactions**: Screen views, button clicks
- **Trip Activities**: Trip planning, booking, completion
- **Feature Usage**: Feature adoption tracking
- **System Events**: Login, logout, error events
- **Business Events**: Purchases, ratings, sharing

## Key Features
- Comprehensive event tracking
- Real-time activity logging
- Behavioral pattern analysis
- Privacy-compliant data collection

## Integration Points
- **AuthUsers**: Action ownership
- **Trips**: Trip-related actions
- **UserRatings**: Rating activities
- **CoinTransaction**: Reward-triggering actions

## Usage Context
Used for user behavior analysis, personalization engines, feature usage analytics, and system performance monitoring.

## Analytics Capabilities
- User journey mapping
- Feature adoption metrics
- Conversion funnel analysis
- Retention and engagement tracking
- A/B testing support

## Performance Optimization
- Asynchronous event logging
- Batch processing for analytics
- Efficient time-series queries
- Optimized for high-volume writes

## Privacy Compliance
- User consent management
- Data anonymization options
- Retention policy enforcement
- GDPR compliance support

## Related Models
- AuthUsers: User identification
- Trips: Trip-related tracking
- UserRatings: Feedback actions
- UserBadgeRelatedActivityLog: Achievement tracking

## API Integration
- Event tracking endpoints
- Analytics reporting APIs
- Behavioral insights services
- Real-time monitoring

## Development Notes
- High-volume write operations
- Privacy-first design
- Analytics-optimized structure
- Real-time and batch processing support