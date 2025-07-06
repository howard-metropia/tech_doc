# SendEvent Model

## Overview
Event messaging and communication model for the TSP Job system. Handles queuing, processing, and delivery of user events, incentive notifications, and system communications through a flexible messaging infrastructure that supports various event types and delivery mechanisms.

## Model Definition
```javascript
const { Schema } = require('mongoose');
const conn = require('@maas/core/mongo')('cache');

const defaultSchema = new Schema({}, { strict: false });
const SendEvent = conn.model('send_event', defaultSchema);

module.exports = {
  SendEvent,
};
```

## Database Configuration
- **Database**: Cache MongoDB instance
- **Collection**: `send_event`
- **ORM**: Mongoose with dynamic schema
- **Connection**: Managed by @maas/core MongoDB connection pool
- **Schema Mode**: Non-strict (flexible document structure)

## Purpose
- User event messaging and notification delivery
- Incentive system communication processing
- System event broadcasting and distribution
- Multi-channel message routing and queuing
- Event-driven user engagement and interaction

## Key Features
- **Flexible Schema**: Dynamic document structure for various event types
- **Batch Processing**: Efficient bulk message handling
- **Multi-channel Support**: Various delivery mechanisms (push, email, SMS)
- **Event Queuing**: Reliable message queuing and processing
- **Delivery Tracking**: Comprehensive message status monitoring

## Event Data Structure
Flexible event message format supporting various communication types:

```javascript
{
  action: String,                // Event action type ('event', 'notification', 'broadcast')
  data: Array,                   // Event data payload array
  message_type: String,          // Message categorization
  priority: Number,              // Delivery priority (0-5)
  scheduled_at: Date,            // Scheduled delivery time
  created_at: Date,              // Event creation timestamp
  processed_at: Date,            // Processing timestamp
  status: String,                // Processing status
  delivery_channels: Array,      // Delivery method configuration
  metadata: Object               // Additional event metadata
}
```

## Usage Context
Primary usage in incentive event processing and user communication:

```javascript
// Send incentive events to users
const sendIncentiveEvents = async (eventDatas) => {
  const limitMax = 500; // Maximum events per batch
  const loop = Math.ceil(eventDatas.length / limitMax);

  for (let i = 0; i < loop; i++) {
    const sendData = eventDatas.slice(i * limitMax, limitMax);
    const message = {
      action: 'event',
      data: sendData,
    };
    
    try {
      for (let sdIndex = 0; sdIndex < sendData.length; sdIndex++) {
        const data = sendData[sdIndex];
        logger.info(
          `Send incentive event UserIds: ${data.userIds.join(',')} Name:${
            data.eventName
          } Meta:${JSON.stringify(data.eventMeta)}`,
        );
      }
      
      await SendEvent.create(message);
    } catch (err) {
      logger.warn(`Send event Error:${err.message}`);
    }
  }
};
```

## Event Types
- **Incentive Events**: Reward notifications and achievement alerts
- **System Notifications**: Platform updates and maintenance alerts
- **User Engagement**: Behavioral triggers and interaction prompts
- **Marketing Communications**: Promotional campaigns and offers
- **Safety Alerts**: Emergency notifications and travel warnings
- **Trip Updates**: Journey modifications and status changes

## Incentive Event Processing
Comprehensive incentive event data structure:

```javascript
const incentiveEventData = {
  eventName: 'achievement_unlocked',
  eventMeta: {
    achievement_id: 'eco_warrior_badge',
    points_earned: 500,
    badge_name: 'Eco Warrior',
    description: 'Completed 30 eco-friendly trips',
    unlock_timestamp: moment().unix(),
    reward_details: {
      bonus_points: 100,
      unlock_features: ['premium_routing'],
      discount_codes: ['ECO20']
    }
  },
  userIds: [12345, 67890, 54321],
  priority: 2,
  delivery_channels: ['push_notification', 'in_app'],
  localization: {
    en: {
      title: 'Achievement Unlocked!',
      message: 'Congratulations! You earned the Eco Warrior badge'
    },
    es: {
      title: '¡Logro Desbloqueado!',
      message: '¡Felicidades! Ganaste la insignia de Guerrero Ecológico'
    }
  }
};
```

## Batch Event Processing
Efficient bulk message processing with size limitations:

```javascript
const processSendEventQueue = async () => {
  const batchSize = 1000;
  
  try {
    const pendingEvents = await SendEvent.find({
      status: { $in: ['pending', 'retry'] },
      scheduled_at: { $lte: new Date() }
    })
    .sort({ priority: -1, created_at: 1 })
    .limit(batchSize);

    for (const event of pendingEvents) {
      try {
        await SendEvent.updateOne(
          { _id: event._id },
          { 
            status: 'processing',
            processed_at: new Date()
          }
        );

        const result = await processEventData(event);
        
        await SendEvent.updateOne(
          { _id: event._id },
          { 
            status: result.success ? 'completed' : 'failed',
            delivery_result: result,
            completed_at: new Date()
          }
        );

      } catch (error) {
        logger.error(`Event processing error: ${error.message}`);
        await SendEvent.updateOne(
          { _id: event._id },
          { 
            status: 'failed',
            error_message: error.message,
            failed_at: new Date()
          }
        );
      }
    }
  } catch (error) {
    logger.error(`SendEvent queue processing error: ${error.message}`);
  }
};
```

## Event Data Processing
Multi-format event data handling:

```javascript
const processEventData = async (event) => {
  const deliveryResults = [];
  
  try {
    if (event.action === 'event') {
      // Process incentive and user events
      for (const eventItem of event.data) {
        const result = await deliverIncentiveEvent(eventItem);
        deliveryResults.push(result);
      }
    } else if (event.action === 'notification') {
      // Process system notifications
      const result = await deliverSystemNotification(event.data);
      deliveryResults.push(result);
    } else if (event.action === 'broadcast') {
      // Process broadcast messages
      const result = await deliverBroadcastMessage(event.data);
      deliveryResults.push(result);
    }

    return {
      success: deliveryResults.every(r => r.success),
      results: deliveryResults,
      delivered_count: deliveryResults.filter(r => r.success).length,
      failed_count: deliveryResults.filter(r => !r.success).length
    };
  } catch (error) {
    return {
      success: false,
      error: error.message,
      delivered_count: 0,
      failed_count: event.data.length
    };
  }
};
```

## Multi-channel Delivery
Support for various communication channels:

```javascript
const deliverIncentiveEvent = async (eventData) => {
  const deliveryResults = {
    push_notification: false,
    in_app: false,
    email: false,
    sms: false
  };

  try {
    // Push notification delivery
    if (eventData.channels?.includes('push_notification')) {
      for (const userId of eventData.userIds) {
        const pushResult = await sendPushNotification(userId, {
          title: eventData.localization.en.title,
          body: eventData.localization.en.message,
          data: eventData.eventMeta
        });
        deliveryResults.push_notification = pushResult.success;
      }
    }

    // In-app notification
    if (eventData.channels?.includes('in_app')) {
      for (const userId of eventData.userIds) {
        await createInAppNotification(userId, {
          type: eventData.eventName,
          title: eventData.localization.en.title,
          message: eventData.localization.en.message,
          metadata: eventData.eventMeta
        });
        deliveryResults.in_app = true;
      }
    }

    // Email delivery
    if (eventData.channels?.includes('email')) {
      const emailResult = await sendBulkEmail(
        eventData.userIds,
        eventData.eventName,
        eventData.eventMeta
      );
      deliveryResults.email = emailResult.success;
    }

    return {
      success: Object.values(deliveryResults).some(r => r),
      channels: deliveryResults,
      user_count: eventData.userIds.length
    };
  } catch (error) {
    return {
      success: false,
      error: error.message,
      channels: deliveryResults
    };
  }
};
```

## Event Scheduling
Delayed and scheduled event processing:

```javascript
const scheduleEvent = async (eventData, scheduledTime) => {
  const scheduledEvent = {
    action: eventData.action,
    data: eventData.data,
    status: 'scheduled',
    priority: eventData.priority || 0,
    scheduled_at: new Date(scheduledTime),
    created_at: new Date(),
    metadata: {
      source: eventData.source || 'api',
      campaign_id: eventData.campaign_id,
      batch_id: eventData.batch_id
    }
  };

  const result = await SendEvent.create(scheduledEvent);
  
  logger.info(`Event scheduled: ${result._id} for ${scheduledTime}`);
  return result;
};
```

## Error Handling and Retry Logic
Comprehensive error management with retry mechanisms:

```javascript
const retryFailedEvents = async () => {
  const maxRetries = 3;
  const retryDelay = 15; // minutes
  
  const failedEvents = await SendEvent.find({
    status: 'failed',
    retry_count: { $lt: maxRetries },
    failed_at: { 
      $lt: moment().subtract(retryDelay, 'minutes').toDate() 
    }
  }).limit(100);

  for (const event of failedEvents) {
    try {
      await SendEvent.updateOne(
        { _id: event._id },
        { 
          status: 'retry',
          retry_count: (event.retry_count || 0) + 1,
          scheduled_at: moment().add(retryDelay, 'minutes').toDate(),
          last_retry_at: new Date()
        }
      );
    } catch (error) {
      logger.error(`Retry scheduling error: ${error.message}`);
    }
  }

  return failedEvents.length;
};
```

## Performance Features
- **MongoDB Indexing**: Optimized for status and scheduling queries
- **Batch Processing**: Efficient bulk event handling
- **Connection Pooling**: Managed database connections
- **Memory Optimization**: Streaming for large event datasets

## Analytics and Metrics
Event delivery and engagement tracking:

```javascript
const generateEventMetrics = async (startDate, endDate) => {
  const pipeline = [
    {
      $match: {
        created_at: { $gte: startDate, $lte: endDate }
      }
    },
    {
      $group: {
        _id: {
          action: '$action',
          status: '$status'
        },
        count: { $sum: 1 },
        total_users: { $sum: { $size: '$data.userIds' } }
      }
    },
    {
      $group: {
        _id: '$_id.action',
        statuses: {
          $push: {
            status: '$_id.status',
            count: '$count',
            total_users: '$total_users'
          }
        }
      }
    }
  ];

  const metrics = await SendEvent.aggregate(pipeline);
  return metrics;
};
```

## Cleanup and Maintenance
Automated cleanup of processed events:

```javascript
const cleanupProcessedEvents = async () => {
  const retentionDays = 30;
  const cleanupDate = moment().subtract(retentionDays, 'days').toDate();
  
  // Archive completed events older than retention period
  const completedEvents = await SendEvent.find({
    status: 'completed',
    completed_at: { $lt: cleanupDate }
  });

  if (completedEvents.length > 0) {
    // Move to archive collection
    await SendEventArchive.insertMany(completedEvents);
    
    // Remove from active collection
    await SendEvent.deleteMany({
      _id: { $in: completedEvents.map(e => e._id) }
    });
  }

  // Remove failed events older than retention period
  await SendEvent.deleteMany({
    status: 'failed',
    failed_at: { $lt: cleanupDate },
    retry_count: { $gte: 3 }
  });

  return {
    archived: completedEvents.length,
    cleaned: await SendEvent.countDocuments({
      status: 'failed',
      failed_at: { $lt: cleanupDate }
    })
  };
};
```

## Integration Points
- **Incentive Engine**: Reward and achievement event generation
- **Notification Service**: Multi-channel message delivery
- **User Engagement**: Behavioral trigger processing
- **Analytics Platform**: Event tracking and reporting
- **Campaign Management**: Marketing communication delivery

## Related Models
- IncentiveNotifyQueue: Incentive-specific notification queue
- NotificationRecord: Delivery confirmation tracking
- AuthUsers: User identification and preferences
- UserConfig: User communication settings and preferences

## API Integration
- Push notification services (FCM, APNs)
- Email delivery platforms (SendGrid, SES)
- SMS gateway services
- In-app messaging systems
- Analytics and tracking platforms

## Development Notes
- Critical for user engagement and retention
- Requires reliable message queuing infrastructure
- Supports multiple delivery channels and formats
- Optimized for high-volume event processing
- Integration with external communication services and analytics platforms