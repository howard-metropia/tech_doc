# TransitAlertNotificationQueue Model

## Overview
Transit alert notification queue management model for the TSP Job system. Handles queuing, processing, and delivery tracking of public transportation alerts, service disruptions, and real-time transit notifications to users based on their travel patterns and preferences.

## Model Definition
```javascript
const { Model } = require('objection');
const knex = require('@maas/core/mysql')('portal');

class TransitAlertNotificationQueue extends Model {
  static get tableName() {
    return 'transit_alert_notification_queue';
  }
}

module.exports = TransitAlertNotificationQueue.bindKnex(knex);
```

## Database Configuration
- **Database**: Portal MySQL instance
- **Table**: `transit_alert_notification_queue`
- **ORM**: Objection.js with Knex query builder
- **Connection**: Managed by @maas/core MySQL connection pool

## Purpose
- Transit service alert notification management
- Real-time public transportation disruption alerts
- Route-specific transit notification delivery
- User transit preference-based targeting
- Service change and schedule update communication

## Key Features
- **Real-time Alerts**: Immediate transit disruption notifications
- **Route Targeting**: Specific transit line and stop notifications
- **User Preferences**: Personalized alert delivery based on usage patterns
- **Multi-modal Support**: Bus, rail, subway, and ferry alerts
- **Delivery Tracking**: Comprehensive notification status monitoring

## Database Schema
Expected table structure for transit alert notifications:

```sql
CREATE TABLE transit_alert_notification_queue (
  id INT AUTO_INCREMENT PRIMARY KEY,
  user_id INT NOT NULL,
  alert_id VARCHAR(100) NOT NULL,
  route_id VARCHAR(50),
  stop_id VARCHAR(50),
  notification_type INT NOT NULL,
  alert_type ENUM('service_disruption', 'delay', 'cancellation', 'schedule_change', 'emergency', 'maintenance') NOT NULL,
  severity ENUM('low', 'medium', 'high', 'critical') DEFAULT 'medium',
  title VARCHAR(255) NOT NULL,
  message TEXT NOT NULL,
  alert_data JSON,
  status ENUM('pending', 'processing', 'sent', 'failed') DEFAULT 'pending',
  priority INT DEFAULT 0,
  effective_from DATETIME,
  effective_until DATETIME,
  scheduled_at DATETIME,
  sent_at DATETIME,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  INDEX idx_user_id (user_id),
  INDEX idx_alert_id (alert_id),
  INDEX idx_route_id (route_id),
  INDEX idx_status (status),
  INDEX idx_scheduled_at (scheduled_at),
  INDEX idx_effective_period (effective_from, effective_until)
);
```

## Alert Types
- **Service Disruption**: Route closures and major service interruptions
- **Delay**: Schedule delays and timing adjustments
- **Cancellation**: Trip and service cancellations
- **Schedule Change**: Permanent or temporary schedule modifications
- **Emergency**: Safety and security alerts
- **Maintenance**: Planned maintenance and construction impacts

## Usage Context
Integrated with transit alert processing and notification delivery:

```javascript
// Queue transit alert notification
await TransitAlertNotificationQueue.query().insert({
  user_id: userId,
  alert_id: 'metro_red_line_2024_001',
  route_id: 'RED_LINE',
  stop_id: 'DOWNTOWN_STATION',
  notification_type: 94, // Transit alert notification type
  alert_type: 'service_disruption',
  severity: 'high',
  title: 'Red Line Service Disruption',
  message: 'Red Line service suspended between Downtown and Airport due to signal issues. Expected resolution in 45 minutes.',
  alert_data: {
    affected_routes: ['RED_LINE'],
    affected_stops: ['DOWNTOWN_STATION', 'MIDTOWN_STATION', 'AIRPORT_STATION'],
    alternative_routes: ['BLUE_LINE', 'BUS_RAPID_TRANSIT'],
    estimated_duration: 45,
    cause: 'signal_malfunction',
    contact_info: 'Call 511 for updates'
  },
  status: 'pending',
  priority: 2,
  effective_from: moment().format('YYYY-MM-DD HH:mm:ss'),
  effective_until: moment().add(1, 'hour').format('YYYY-MM-DD HH:mm:ss'),
  scheduled_at: moment().format('YYYY-MM-DD HH:mm:ss')
});
```

## Queue Processing Workflow
1. **Alert Ingestion**: Transit agency feeds generate alerts
2. **User Targeting**: Identify affected users based on travel patterns
3. **Prioritization**: Critical alerts processed immediately
4. **Localization**: Message translation and formatting
5. **Delivery**: Multi-channel notification distribution
6. **Tracking**: Delivery confirmation and engagement monitoring

## Transit Alert Processing
Real-time processing with user impact analysis:

```javascript
const processTransitAlerts = async () => {
  const pendingAlerts = await TransitAlertNotificationQueue.query()
    .where('status', 'pending')
    .where('scheduled_at', '<=', moment().format('YYYY-MM-DD HH:mm:ss'))
    .where('effective_from', '<=', moment().format('YYYY-MM-DD HH:mm:ss'))
    .where('effective_until', '>=', moment().format('YYYY-MM-DD HH:mm:ss'))
    .orderBy('priority', 'desc')
    .orderBy('severity', 'desc')
    .limit(200);

  for (const alert of pendingAlerts) {
    try {
      await TransitAlertNotificationQueue.query()
        .findById(alert.id)
        .patch({ status: 'processing' });

      const notificationResult = await sendTransitNotification(
        alert.user_id,
        alert.notification_type,
        alert.title,
        alert.message,
        {
          alert_id: alert.alert_id,
          route_id: alert.route_id,
          stop_id: alert.stop_id,
          severity: alert.severity,
          alert_type: alert.alert_type,
          ...alert.alert_data
        }
      );

      await TransitAlertNotificationQueue.query()
        .findById(alert.id)
        .patch({ 
          status: 'sent',
          sent_at: moment().format('YYYY-MM-DD HH:mm:ss')
        });

    } catch (error) {
      logger.error(`Transit alert processing error: ${error.message}`);
      await TransitAlertNotificationQueue.query()
        .findById(alert.id)
        .patch({ status: 'failed' });
    }
  }
};
```

## Severity Management
Alert prioritization based on impact level:
- **Critical**: System-wide service failures
- **High**: Major route disruptions
- **Medium**: Moderate delays and schedule changes
- **Low**: Minor delays and informational updates

## User Targeting Strategy
Intelligent user selection based on transit usage patterns:

```javascript
const getAffectedUsers = async (routeId, stopIds) => {
  // Find users with recent transit activity on affected routes
  const affectedUsers = await knex('trip_records')
    .join('auth_users', 'trip_records.user_id', 'auth_users.id')
    .leftJoin('user_config', 'auth_users.id', 'user_config.user_id')
    .where('trip_records.travel_mode', 3) // Transit mode
    .whereIn('trip_records.route_id', [routeId])
    .where('trip_records.created_at', '>', moment().subtract(30, 'days').toDate())
    .where(function() {
      this.where('user_config.uis_setting->$.transit_alert', 'true')
          .orWhereNull('user_config.uis_setting->$.transit_alert');
    })
    .select('auth_users.id as user_id', 'auth_users.device_language')
    .groupBy('auth_users.id');

  return affectedUsers;
};
```

## Alert Data Structure
Comprehensive alert metadata for enhanced notifications:

```javascript
const alertData = {
  alert_id: 'metro_blue_line_maintenance_2024_015',
  route_type: 'subway',
  affected_routes: ['BLUE_LINE'],
  affected_stops: [
    { stop_id: 'CENTRAL_STATION', stop_name: 'Central Station' },
    { stop_id: 'UNIVERSITY_STATION', stop_name: 'University Station' }
  ],
  alternative_routes: [
    { route_id: 'BUS_45', route_name: 'Express Bus 45' },
    { route_id: 'GREEN_LINE', route_name: 'Green Line Metro' }
  ],
  service_impact: {
    delay_minutes: 15,
    frequency_reduction: '50%',
    last_train_affected: true
  },
  cause: 'scheduled_maintenance',
  contact_info: {
    phone: '1-800-TRANSIT',
    website: 'https://transit.city.gov/alerts',
    twitter: '@CityTransit'
  },
  updates_available: true
};
```

## Multi-language Support
Localized alert messages for diverse user base:

```javascript
const getLocalizedTransitMessage = (alertType, language, data) => {
  const messages = {
    en: {
      service_disruption: {
        title: 'Service Disruption',
        template: '{route} service disrupted. {cause}. Expected duration: {duration} minutes.'
      },
      delay: {
        title: 'Service Delay',
        template: '{route} experiencing {delay_minutes} minute delays due to {cause}.'
      }
    },
    es: {
      service_disruption: {
        title: 'Interrupción del Servicio',
        template: 'Servicio {route} interrumpido. {cause}. Duración esperada: {duration} minutos.'
      },
      delay: {
        title: 'Retraso del Servicio',
        template: '{route} experimenta retrasos de {delay_minutes} minutos debido a {cause}.'
      }
    }
  };
  
  const message = messages[language]?.[alertType] || messages.en[alertType];
  return formatTemplate(message.template, data);
};
```

## Integration Points
- **TransitAlert**: Core transit alert data model
- **TripRecords**: User transit usage patterns
- **UserConfig**: User notification preferences
- **NotificationRecord**: Delivery tracking and analytics
- **GTFS Data**: Real-time transit feed integration

## Real-time Processing
Integration with GTFS-RT feeds for immediate alert processing:

```javascript
const processGTFSRTAlerts = async (gtfsRTFeed) => {
  for (const alert of gtfsRTFeed.entity) {
    if (alert.alert) {
      const affectedUsers = await getAffectedUsersByAlert(alert);
      
      for (const user of affectedUsers) {
        await TransitAlertNotificationQueue.query().insert({
          user_id: user.user_id,
          alert_id: alert.id,
          route_id: extractRouteId(alert),
          notification_type: 94,
          alert_type: classifyAlertType(alert),
          severity: calculateSeverity(alert),
          title: getLocalizedTitle(alert, user.language),
          message: getLocalizedMessage(alert, user.language),
          alert_data: parseAlertData(alert),
          status: 'pending',
          priority: calculatePriority(alert),
          effective_from: moment.unix(alert.alert.active_period[0].start).format('YYYY-MM-DD HH:mm:ss'),
          effective_until: moment.unix(alert.alert.active_period[0].end).format('YYYY-MM-DD HH:mm:ss'),
          scheduled_at: moment().format('YYYY-MM-DD HH:mm:ss')
        });
      }
    }
  }
};
```

## Performance Features
- **MySQL Indexing**: Optimized for time-sensitive queries
- **Batch Processing**: Efficient bulk notification handling
- **Connection Pooling**: Managed database connections
- **Priority Queuing**: Critical alert prioritization

## Cleanup and Maintenance
Automated queue maintenance and archival:

```javascript
const cleanupTransitAlertQueue = async () => {
  // Remove expired alerts
  await TransitAlertNotificationQueue.query()
    .where('effective_until', '<', moment().format('YYYY-MM-DD HH:mm:ss'))
    .where('status', 'sent')
    .delete();

  // Archive old notifications
  const oldNotifications = await TransitAlertNotificationQueue.query()
    .where('sent_at', '<', moment().subtract(7, 'days').format('YYYY-MM-DD HH:mm:ss'))
    .where('status', 'sent');

  // Move to archive table and delete from active queue
  if (oldNotifications.length > 0) {
    await knex('transit_alert_notification_archive').insert(oldNotifications);
    await TransitAlertNotificationQueue.query()
      .whereIn('id', oldNotifications.map(n => n.id))
      .delete();
  }
};
```

## Analytics and Reporting
Comprehensive metrics for alert effectiveness:

```javascript
const generateAlertAnalytics = async (startDate, endDate) => {
  const analytics = await TransitAlertNotificationQueue.query()
    .select(
      'alert_type',
      'severity',
      knex.raw('COUNT(*) as total_sent'),
      knex.raw('AVG(TIMESTAMPDIFF(SECOND, scheduled_at, sent_at)) as avg_delivery_time'),
      knex.raw('COUNT(CASE WHEN status = "failed" THEN 1 END) as failed_count')
    )
    .where('created_at', '>=', startDate)
    .where('created_at', '<=', endDate)
    .groupBy('alert_type', 'severity');

  return analytics;
};
```

## Error Handling
Comprehensive error management with retry logic:

```javascript
const retryFailedTransitAlerts = async () => {
  const failedAlerts = await TransitAlertNotificationQueue.query()
    .where('status', 'failed')
    .where('updated_at', '>', moment().subtract(2, 'hours').format('YYYY-MM-DD HH:mm:ss'))
    .where('effective_until', '>', moment().format('YYYY-MM-DD HH:mm:ss'))
    .limit(100);

  for (const alert of failedAlerts) {
    await TransitAlertNotificationQueue.query()
      .findById(alert.id)
      .patch({ 
        status: 'pending',
        scheduled_at: moment().add(5, 'minutes').format('YYYY-MM-DD HH:mm:ss')
      });
  }
};
```

## Related Models
- TransitAlert: Core transit alert management
- TripRecords: User transit usage tracking
- AuthUsers: User identification and preferences
- NotificationRecord: Delivery confirmation and analytics
- UserConfig: User notification settings

## API Integration
- GTFS-RT feed processing
- Transit agency alert systems
- User notification preferences
- Real-time service status
- Alert delivery analytics

## Development Notes
- Critical for public transportation user experience
- Requires real-time processing capabilities
- Supports multiple transit agencies and modes
- Optimized for high-volume alert distribution
- Integration with external transit data feeds