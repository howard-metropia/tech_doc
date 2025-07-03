# UserBadgeRelatedActivityLog Model

## Overview
User badge and achievement activity logging model for the TSP Job system. Tracks gamification activities, badge earning events, and user achievement progress.

## Model Definition
```javascript
const knex = require('@maas/core/mysql')('portal');
class UserBadgeRelatedActivityLog extends Model {
  static get tableName() {
    return 'user_badge_related_activity_log';
  }
}
module.exports = UserBadgeRelatedActivityLog.bindKnex(knex);
```

## Database Configuration
- **Database**: Portal MySQL instance
- **Table**: `user_badge_related_activity_log`
- **ORM**: Objection.js with Knex query builder

## Purpose
- Badge earning activity tracking
- Achievement progress logging
- Gamification event recording
- User engagement monitoring

## Activity Types
- **Badge Earned**: Achievement unlocked
- **Progress Update**: Milestone reached
- **Challenge Completed**: Goal achieved
- **Streak Maintained**: Consecutive actions
- **Level Up**: Tier advancement

## Key Features
- Comprehensive activity logging
- Achievement progress tracking
- Gamification support
- User engagement analytics

## Badge Categories
- **Transportation**: Travel-related achievements
- **Environmental**: Sustainability badges
- **Social**: Community participation
- **Loyalty**: Long-term engagement
- **Challenge**: Special accomplishments

## Integration Points
- **AuthUsers**: User identification
- **UserActions**: Activity correlation
- **CoinTransaction**: Reward distribution
- **PointsTransaction**: Points allocation

## Gamification Features
- Progress tracking
- Achievement unlocking
- Reward distribution
- Engagement measurement

## Analytics Applications
- User engagement analysis
- Achievement effectiveness
- Gamification optimization
- Behavioral pattern recognition

## Performance Features
- High-volume logging support
- Efficient activity queries
- Real-time badge processing
- Scalable for gamification

## Related Models
- AuthUsers: User identification
- UserActions: Activity tracking
- CoinTransaction: Rewards
- PointsTransaction: Points

## Development Notes
- Gamification system support
- High-volume logging requirements
- Real-time badge processing
- User engagement optimization