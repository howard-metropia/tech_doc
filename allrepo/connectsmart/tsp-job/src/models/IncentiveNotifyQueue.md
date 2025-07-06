# IncentiveNotifyQueue Model

## Overview
Incentive notification queue management model for the TSP Job system. Handles queuing, processing, and delivery tracking of incentive-based notifications to users, supporting gamification features, reward programs, and behavioral engagement initiatives within the mobility platform.

## Model Definition
```javascript
const { Model } = require('objection');
const knex = require('@maas/core/mysql')('portal');

class IncentiveNotifyQueue extends Model {
  static get tableName() {
    return 'incentive_notify_queue';
  }
}

module.exports = IncentiveNotifyQueue.bindKnex(knex);
```

## Database Configuration
- **Database**: Portal MySQL instance
- **Table**: `incentive_notify_queue`
- **ORM**: Objection.js with Knex query builder
- **Connection**: Managed by @maas/core MySQL connection pool

## Purpose
- Incentive notification queue management and processing
- User engagement and gamification support
- Reward program notification delivery
- Achievement and milestone alert coordination
- Behavioral incentive communication

## Key Features
- **Queue Management**: Ordered notification processing
- **Delivery Tracking**: Notification status monitoring
- **User Targeting**: Specific user incentive messaging
- **Batch Processing**: Efficient bulk notification handling
- **Retry Logic**: Failed notification recovery mechanisms

## Database Schema
Expected table structure for incentive notifications:

```sql
CREATE TABLE incentive_notify_queue (
  id INT AUTO_INCREMENT PRIMARY KEY,
  user_id INT NOT NULL,
  incentive_type VARCHAR(50) NOT NULL,
  notification_type INT NOT NULL,
  message_title VARCHAR(255),
  message_body TEXT,
  incentive_data JSON,
  status ENUM('pending', 'processing', 'sent', 'failed') DEFAULT 'pending',
  priority INT DEFAULT 0,
  scheduled_at DATETIME,
  sent_at DATETIME,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  INDEX idx_user_id (user_id),
  INDEX idx_status (status),
  INDEX idx_scheduled_at (scheduled_at),
  INDEX idx_priority (priority)
);
```

## Incentive Types
- **Achievement Rewards**: Milestone completion notifications
- **Point Earnings**: Credit and reward point alerts
- **Challenge Completions**: Gamification achievement notifications
- **Bonus Opportunities**: Special offer and promotion alerts
- **Streak Rewards**: Consecutive usage incentives
- **Referral Bonuses**: User referral program rewards

## Usage Context
Integrated with incentive processing jobs and notification systems:

```javascript
// Queue incentive notification
await IncentiveNotifyQueue.query().insert({
  user_id: userId,
  incentive_type: 'achievement_reward',
  notification_type: 85, // Achievement notification type
  message_title: 'Congratulations! Achievement Unlocked',
  message_body: 'You have completed the Weekly Commuter challenge',
  incentive_data: {
    achievement_id: 'weekly_commuter',
    points_earned: 500,
    badge_unlocked: 'eco_warrior'
  },
  status: 'pending',
  priority: 1,
  scheduled_at: moment().add(5, 'minutes').format('YYYY-MM-DD HH:mm:ss')
});
```

## Queue Processing Workflow
1. **Notification Creation**: Incentive events trigger queue entries
2. **Prioritization**: High-priority notifications processed first
3. **Scheduling**: Delivery timing optimization
4. **Processing**: Notification generation and delivery
5. **Status Tracking**: Delivery confirmation and error handling

## Notification Processing
Batch processing for efficient notification delivery:

```javascript
const processIncentiveQueue = async () => {
  const pendingNotifications = await IncentiveNotifyQueue.query()
    .where('status', 'pending')
    .where('scheduled_at', '<=', moment().format('YYYY-MM-DD HH:mm:ss'))
    .orderBy('priority', 'desc')
    .orderBy('scheduled_at', 'asc')
    .limit(100);

  for (const notification of pendingNotifications) {
    try {
      await IncentiveNotifyQueue.query()
        .findById(notification.id)
        .patch({ status: 'processing' });

      const result = await sendNotification(
        notification.user_id,
        notification.notification_type,
        notification.message_title,
        notification.message_body,
        notification.incentive_data
      );

      await IncentiveNotifyQueue.query()
        .findById(notification.id)
        .patch({ 
          status: 'sent',
          sent_at: moment().format('YYYY-MM-DD HH:mm:ss')
        });
    } catch (error) {
      await IncentiveNotifyQueue.query()
        .findById(notification.id)
        .patch({ status: 'failed' });
    }
  }
};
```

## Priority Management
Notification prioritization system:
- **Priority 0**: Standard notifications
- **Priority 1**: Important achievements
- **Priority 2**: Time-sensitive offers
- **Priority 3**: Critical rewards
- **Priority 4**: Emergency incentives

## Status Management
Comprehensive notification lifecycle tracking:
- **pending**: Queued for delivery
- **processing**: Currently being sent
- **sent**: Successfully delivered
- **failed**: Delivery unsuccessful

## Integration Points
- **Incentive Engine**: Reward calculation and distribution
- **User Activity**: Behavior tracking and analysis
- **Achievement System**: Milestone and badge management
- **Notification Service**: Message delivery infrastructure
- **Analytics**: Engagement and effectiveness tracking

## Gamification Support
Enhanced user engagement through structured incentives:

```javascript
const incentiveData = {
  achievement_type: 'carbon_savings',
  points_earned: 250,
  streak_count: 7,
  next_milestone: 1000,
  badge_progress: {
    current: 7,
    required: 10,
    badge_name: 'Green Commuter'
  },
  rewards: {
    points: 250,
    unlocked_features: ['premium_routing'],
    discount_codes: ['ECO15']
  }
};
```

## Retry Mechanism
Failed notification recovery system:

```javascript
const retryFailedNotifications = async () => {
  const failedNotifications = await IncentiveNotifyQueue.query()
    .where('status', 'failed')
    .where('updated_at', '>', moment().subtract(1, 'hour').format('YYYY-MM-DD HH:mm:ss'))
    .limit(50);

  for (const notification of failedNotifications) {
    await IncentiveNotifyQueue.query()
      .findById(notification.id)
      .patch({ 
        status: 'pending',
        scheduled_at: moment().add(15, 'minutes').format('YYYY-MM-DD HH:mm:ss')
      });
  }
};
```

## Performance Features
- **MySQL Indexing**: Optimized for queue processing queries
- **Batch Processing**: Efficient bulk notification handling
- **Connection Pooling**: Managed database connections
- **Priority Queuing**: Smart notification ordering

## Message Localization
Multi-language support for global user base:

```javascript
const getLocalizedMessage = (incentiveType, language, data) => {
  const messages = {
    en: {
      achievement_reward: {
        title: 'Achievement Unlocked!',
        body: `Congratulations! You earned ${data.points_earned} points`
      }
    },
    es: {
      achievement_reward: {
        title: '¡Logro Desbloqueado!',
        body: `¡Felicidades! Ganaste ${data.points_earned} puntos`
      }
    }
  };
  return messages[language]?.[incentiveType] || messages.en[incentiveType];
};
```

## Analytics Integration
Tracking notification effectiveness and user engagement:

```javascript
const trackNotificationMetrics = async (notification) => {
  await IncentiveNotifyQueue.query()
    .findById(notification.id)
    .patch({
      metrics_data: {
        delivery_time: moment().diff(notification.created_at, 'seconds'),
        user_timezone: notification.user_timezone,
        device_type: notification.device_type,
        engagement_score: calculateEngagementScore(notification)
      }
    });
};
```

## Error Handling
Comprehensive error management with detailed logging:

```javascript
try {
  await processIncentiveQueue();
} catch (error) {
  logger.error(`IncentiveNotifyQueue processing error: ${error.message}`);
  // Alert system notification for critical failures
}
```

## Queue Maintenance
Automated cleanup and archival processes:

```javascript
const cleanupQueue = async () => {
  // Archive old sent notifications
  await IncentiveNotifyQueue.query()
    .where('status', 'sent')
    .where('sent_at', '<', moment().subtract(30, 'days').format('YYYY-MM-DD HH:mm:ss'))
    .delete();

  // Remove old failed notifications
  await IncentiveNotifyQueue.query()
    .where('status', 'failed')
    .where('updated_at', '<', moment().subtract(7, 'days').format('YYYY-MM-DD HH:mm:ss'))
    .delete();
};
```

## Related Models
- AuthUsers: User identification and preferences
- PointsTransaction: Reward point management
- UserBadgeRelatedActivityLog: Achievement tracking
- NotificationRecord: Delivery confirmation logging

## API Integration
- Incentive calculation endpoints
- Queue status monitoring
- Notification delivery tracking
- User engagement analytics
- Gamification progress updates

## Development Notes
- Critical for user engagement and retention
- Requires reliable queue processing infrastructure
- Supports complex incentive logic and calculations
- Optimized for high-volume notification delivery
- Integration with behavioral analytics and user segmentation