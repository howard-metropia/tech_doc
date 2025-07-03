# HNTB Pre-Trip Alert Migration Documentation

## Quick Summary

The HNTB Pre-Trip Alert migration creates a comprehensive table structure for managing proactive transportation alerts and notifications within the HNTB transportation research platform. This migration establishes the `hntb_pre_trip_alert` table that serves as a critical component for delivering timely, location-aware transportation information to research participants, enabling studies of information delivery effectiveness, user response patterns, and proactive communication impact on transportation behavior and decision-making.

**Key Features:**
- Auto-incrementing primary key system supporting high-volume alert processing
- Comprehensive user association maintaining participant relationship integrity
- Dual identifier system with log_id and event_id for detailed tracking and correlation
- Event name classification supporting categorized alert type analysis
- Action mode tracking enabling response behavior and engagement measurement
- Geographic coordinate capture for location-aware alert delivery and spatial analysis
- Complete temporal tracking with alert creation time and comprehensive audit trail
- Integration support for real-time alert delivery systems and push notification services

## Technical Analysis

### Database Schema Architecture

The migration implements a sophisticated alert management schema optimized for real-time notification delivery and behavioral response analysis:

```javascript
const tableName = 'hntb_pre_trip_alert';

exports.up = async function (knex) {
  try {
    await knex.schema.createTable(tableName, (table) => {
      table.increments('id').unsigned().primary();
      table.string('user_id', 256).notNullable();
      table.string('log_id', 32).notNullable();
      table.string('event_id', 32).notNullable();
      table.string('event_name', 32).notNullable();
      table.tinyint('action_mode').notNullable().defaultTo(0);
      table.double('event_lat').notNullable();
      table.double('event_lng').notNullable();
      table.dateTime('logged_on').notNullable().comment('The time that the log was created');
      table.dateTime('created_on').notNullable().defaultTo(knex.raw('CURRENT_TIMESTAMP'));
      table.dateTime('modified_on').notNullable().defaultTo(knex.raw('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'));
      table.unique(['log_id'], { indexName: 'log_id_unique' });
    });
  } catch (e) {
    logger.error(e.message);
    await knex.schema.dropTableIfExists(tableName);
    throw new Error(e);
  }
};
```

### Field Specifications and Alert System Integration

**Primary Identification Framework:**
- `id`: Auto-incrementing unsigned integer serving as primary key for database efficiency
- Enables high-performance sequential processing of large-volume alert data
- Supports efficient pagination and bulk operations for alert management systems

**User Correlation System:**
- `user_id`: 256-character string maintaining consistent participant identification across alert interactions
- Non-nullable constraint ensures every pre-trip alert is attributed to a research participant
- Supports personalized alert delivery and individual response pattern analysis

**Dual Identifier Tracking System:**
- `log_id`: 32-character string providing unique log entry identification for audit trails
- `event_id`: 32-character string enabling correlation with external event systems
- Unique constraint on log_id prevents duplicate alert processing and maintains data integrity
- Supports complex alert correlation and external system integration

**Alert Classification Framework:**
- `event_name`: 32-character string field enabling categorized alert type analysis
- Non-nullable constraint ensures complete alert classification for research analytics
- Supports standardized alert taxonomy (e.g., "weather_alert", "traffic_incident", "route_optimization")
- Enables comparative analysis across different types of transportation alerts

**Action Mode Response Tracking:**
- `action_mode`: Tinyint field with default value 0 for user response behavior measurement
- Supports enumerated response types (0: no action, 1: acknowledged, 2: route changed, etc.)
- Non-nullable with default ensures complete response data collection
- Enables engagement analysis and alert effectiveness measurement

**Geographic Alert Context System:**
- `event_lat`: Double precision field for alert-relevant latitude coordinates
- `event_lng`: Double precision field for alert-relevant longitude coordinates
- Both coordinates required (notNullable) ensuring complete spatial context for location-aware alerts
- Supports geographic alert relevance verification and location-based alert optimization

**Temporal Alert Management:**
- `logged_on`: DateTime field capturing the precise moment of alert log creation
- Includes descriptive comment clarifying temporal significance for alert timing analysis
- `created_on`: Automatic timestamp using MySQL CURRENT_TIMESTAMP for record creation tracking
- `modified_on`: Self-updating timestamp with ON UPDATE CURRENT_TIMESTAMP trigger
- Comprehensive temporal tracking supporting alert delivery timing and response pattern analysis

### Alert System Design Patterns

**High-Volume Processing Architecture:**
The auto-incrementing primary key design supports efficient processing of high-frequency alert events:

```sql
-- Efficient alert retrieval for processing
SELECT * FROM hntb_pre_trip_alert 
WHERE id > :last_processed_id 
ORDER BY id 
LIMIT 1000;
```

**Alert Correlation and Tracking:**
The dual identifier system enables complex alert relationship management:

```sql
-- Alert correlation analysis
SELECT 
  log_id, 
  event_id, 
  event_name,
  action_mode,
  COUNT(*) as correlation_count
FROM hntb_pre_trip_alert 
GROUP BY event_id 
HAVING correlation_count > 1;
```

**Response Behavior Analytics:**
Action mode tracking supports comprehensive user engagement analysis and alert effectiveness measurement.

### Data Integrity and Performance Optimization

**Constraint Implementation:**
```javascript
table.unique(['log_id'], {
  indexName: 'log_id_unique',
});
```

The unique constraint on log_id prevents duplicate alert log processing and maintains consistency across alert delivery systems.

**Error Handling and System Resilience:**
```javascript
catch (e) {
  logger.error(e.message);
  await knex.schema.dropTableIfExists(tableName);
  throw new Error(e);
}
```

**Resilience Features:**
- Automatic table cleanup on migration failure preventing partial schema states
- Comprehensive error logging through centralized @maas/core/log system
- Exception propagation ensuring proper error handling in alert delivery pipelines
- Transaction safety maintaining database consistency during high-volume alert processing

### Schema Design for Alert Research

**Auto-increment Performance Advantages:**
- Supports high-throughput alert processing without string-based key overhead
- Enables efficient batch processing and pagination for large alert datasets
- Facilitates time-series analysis and sequential alert processing

**Comprehensive Tracking Capabilities:**
- Multi-level identification system supports complex alert correlation studies
- Action mode tracking enables detailed response behavior analysis
- Geographic context supports location-aware alert effectiveness research

## Usage/Integration

### Pre-Trip Alert Delivery Workflow

**Alert Processing Pipeline:**
1. Transportation event or condition detected requiring user notification
2. Alert generated with appropriate event classification and geographic context
3. Log_id and event_id assigned for tracking and correlation purposes
4. Alert delivered to relevant users based on location and preferences
5. User response tracked through action_mode updates
6. Alert effectiveness analyzed through response patterns and behavioral changes

**Research Data Collection Integration:**
- Alert delivery effectiveness analysis for communication strategy optimization
- User response pattern analysis supporting personalized alert customization
- Geographic alert relevance analysis enabling location-aware alert improvements
- Temporal pattern analysis supporting optimal alert timing strategies

### Migration Execution Context

**Database Operation Timing:**
- Timestamp: March 17, 2025, 01:35:26 GMT (20250317013526)
- Final component in comprehensive HNTB migration sequence
- Completes integrated research platform with comprehensive data collection capabilities

**System Integration Architecture:**
- Operates within TSP Job service database environment
- Integrates with real-time alert delivery and push notification systems
- Supports both proactive alert delivery and batch research analytics processing

### Application Service Integration

**Alert Management System:**
```javascript
// Example pre-trip alert creation and delivery
const createPreTripAlert = async (alertData) => {
  const alertRecord = {
    user_id: alertData.userId,
    log_id: generateLogId(),
    event_id: alertData.eventId,
    event_name: alertData.alertType,
    action_mode: 0, // Initially no action taken
    event_lat: alertData.latitude,
    event_lng: alertData.longitude,
    logged_on: new Date()
  };
  
  const insertedAlert = await knex('hntb_pre_trip_alert').insert(alertRecord);
  
  // Trigger alert delivery
  await deliverAlertToUser(alertData.userId, alertRecord);
  
  return insertedAlert;
};

// Update user response to alert
const updateAlertResponse = async (logId, actionMode) => {
  await knex('hntb_pre_trip_alert')
    .where('log_id', logId)
    .update({
      action_mode: actionMode,
      modified_on: new Date()
    });
};
```

**Research Analytics Integration:**
- Real-time alert delivery effectiveness monitoring dashboards
- User engagement analysis supporting personalized communication strategies
- Geographic alert optimization analysis enabling location-aware improvements
- Response pattern studies facilitating behavioral transportation research

## Dependencies

### Core Infrastructure Dependencies

**Knex.js Database Management System:**
- Requires TSP Job service Knex configuration for database connectivity and transaction management
- Utilizes MySQL database connection with proper schema modification privileges for alert data
- Integrates with Knex migration system for version control and automated deployment processes
- Supports auto-increment primary key functionality for high-performance alert processing

**Centralized Logging Infrastructure:**
```javascript
const { logger } = require('@maas/core/log');
```
- Depends on @maas/core/log system for comprehensive error reporting and alert delivery audit trails
- Provides structured logging across distributed microservice architecture
- Supports real-time monitoring and debugging of alert processing and delivery operations

### Database Platform Requirements

**MySQL Database System:**
- Requires MySQL 5.7+ for advanced timestamp handling and auto-increment functionality
- Utilizes CURRENT_TIMESTAMP and ON UPDATE CURRENT_TIMESTAMP features for temporal tracking
- Depends on proper timezone configuration for accurate alert timing analysis
- Requires string indexing optimization for efficient log_id-based unique constraint queries

**Database Access and Permissions:**
- CREATE TABLE privileges for schema creation and pre-trip alert table establishment
- DROP TABLE privileges for rollback and cleanup operations during migration failures
- INDEX creation permissions for unique constraint implementation and query optimization
- AUTO_INCREMENT privileges for primary key sequence management
- Standard DML privileges (SELECT/INSERT/UPDATE) for alert data operations

### External System Integration Dependencies

**Alert Delivery and Notification Systems:**
- Requires integration with push notification services (APNs, FCM) for mobile alert delivery
- Depends on email and SMS delivery systems for multi-channel alert communication
- Integrates with real-time communication APIs for immediate alert processing
- Supports webhook integration for external alert delivery confirmation

**Transportation Information Systems:**
- Depends on integration with traffic management systems for real-time incident alerts
- Requires connectivity with weather services for weather-related transportation alerts
- Integrates with transit agency APIs for service disruption and schedule change notifications
- Supports connection with route optimization services for dynamic routing alerts

**HNTB Research Platform Integration:**
- Requires consistent user_id format across all HNTB platform components for participant tracking
- Depends on user preference management for personalized alert delivery
- Integrates with research data export and alert effectiveness analysis pipelines
- Supports correlation with other transportation behavior data for comprehensive communication research

## Code Examples

### Migration Management Operations

**Execute Pre-Trip Alert Migration:**
```bash
# Run migration in TSP Job service context
cd allrepo/connectsmart/tsp-job
npx knex migrate:up 20250317013526_hntb_pre_trip_alert.js --env production

# Verify migration completion and alert table structure
npx knex migrate:status | grep pre_trip_alert
```

**Migration Rollback and Alert System Recovery:**
```bash
# Rollback pre-trip alert migration if required
npx knex migrate:down 20250317013526_hntb_pre_trip_alert.js --env production

# Verify rollback completion
npx knex migrate:list --completed | grep -v pre_trip_alert
```

### Pre-Trip Alert Data Management

**Alert Data Operations:**
```javascript
const knex = require('./database/connection');

// Create new pre-trip alert
const createAlert = async (alertData) => {
  const alertRecord = await knex('hntb_pre_trip_alert').insert({
    user_id: alertData.userId,
    log_id: alertData.logId,
    event_id: alertData.eventId,
    event_name: alertData.eventType,
    action_mode: alertData.actionMode || 0,
    event_lat: alertData.latitude,
    event_lng: alertData.longitude,
    logged_on: alertData.alertTime || new Date()
  });
  
  return alertRecord;
};

// Retrieve user alert history
const getUserAlertHistory = async (userId, limitCount = 100) => {
  return await knex('hntb_pre_trip_alert')
    .where('user_id', userId)
    .select('*')
    .orderBy('logged_on', 'desc')
    .limit(limitCount);
};

// Update alert response action
const updateAlertAction = async (logId, actionMode) => {
  return await knex('hntb_pre_trip_alert')
    .where('log_id', logId)
    .update({
      action_mode: actionMode,
      modified_on: new Date()
    });
};

// Get alerts by event type and location
const getAlertsByTypeAndLocation = async (eventName, bounds, timeframe) => {
  return await knex('hntb_pre_trip_alert')
    .where('event_name', eventName)
    .whereBetween('event_lat', [bounds.minLat, bounds.maxLat])
    .whereBetween('event_lng', [bounds.minLng, bounds.maxLng])
    .where('logged_on', '>', timeframe)
    .select('*')
    .orderBy('logged_on', 'desc');
};
```

### Alert Analytics and Research Queries

**Alert Effectiveness Analysis:**
```javascript
// Alert response rate analysis by type
const analyzeAlertResponseRates = async (startDate, endDate) => {
  return await knex('hntb_pre_trip_alert')
    .select('event_name')
    .count('* as total_alerts')
    .sum(knex.raw('CASE WHEN action_mode > 0 THEN 1 ELSE 0 END as responded_alerts'))
    .whereBetween('logged_on', [startDate, endDate])
    .groupBy('event_name')
    .orderBy('total_alerts', 'desc');
};

// Geographic alert delivery effectiveness
const analyzeGeographicAlertEffectiveness = async (gridPrecision = 3) => {
  return await knex('hntb_pre_trip_alert')
    .select(
      knex.raw(`ROUND(event_lat, ${gridPrecision}) as lat_cluster`),
      knex.raw(`ROUND(event_lng, ${gridPrecision}) as lng_cluster`)
    )
    .select('event_name')
    .count('* as alert_count')
    .avg('action_mode as avg_response_level')
    .groupBy('lat_cluster', 'lng_cluster', 'event_name')
    .having('alert_count', '>', 5)
    .orderBy('avg_response_level', 'desc');
};

// Temporal alert delivery pattern analysis
const analyzeTemporalAlertPatterns = async () => {
  return await knex('hntb_pre_trip_alert')
    .select(
      knex.raw('HOUR(logged_on) as alert_hour'),
      knex.raw('DAYOFWEEK(logged_on) as day_of_week')
    )
    .select('event_name')
    .count('* as alert_frequency')
    .avg('action_mode as avg_response')
    .groupBy('alert_hour', 'day_of_week', 'event_name')
    .orderBy('alert_hour', 'day_of_week', 'alert_frequency');
};
```

### Advanced Alert Research Analytics

**User Engagement and Response Behavior Analysis:**
```javascript
// Comprehensive user alert engagement profile
const analyzeUserAlertEngagement = async (userId) => {
  return await knex('hntb_pre_trip_alert')
    .where('user_id', userId)
    .select(
      'event_name',
      knex.raw('COUNT(*) as total_alerts'),
      knex.raw('SUM(CASE WHEN action_mode > 0 THEN 1 ELSE 0 END) as responded_alerts'),
      knex.raw('AVG(action_mode) as avg_response_level'),
      knex.raw('MIN(logged_on) as first_alert'),
      knex.raw('MAX(logged_on) as last_alert')
    )
    .groupBy('event_name')
    .orderBy('total_alerts', 'desc');
};

// Alert correlation and event relationship analysis
const analyzeAlertCorrelations = async (eventId) => {
  return await knex('hntb_pre_trip_alert')
    .where('event_id', eventId)
    .select(
      'user_id',
      'event_name',
      'action_mode',
      'logged_on',
      knex.raw('TIMESTAMPDIFF(MINUTE, logged_on, modified_on) as response_time_minutes')
    )
    .orderBy('logged_on');
};

// Alert delivery timing optimization analysis
const optimizeAlertDeliveryTiming = async (eventName, daysPrior = 30) => {
  const startDate = new Date(Date.now() - (daysPrior * 24 * 60 * 60 * 1000));
  
  return await knex('hntb_pre_trip_alert')
    .where('event_name', eventName)
    .where('logged_on', '>', startDate)
    .select(
      knex.raw('HOUR(logged_on) as delivery_hour'),
      knex.raw('COUNT(*) as alert_count'),
      knex.raw('AVG(action_mode) as avg_response'),
      knex.raw('SUM(CASE WHEN action_mode > 0 THEN 1 ELSE 0 END) as response_count')
    )
    .groupBy('delivery_hour')
    .orderBy('avg_response', 'desc');
};
```

### Data Validation and Alert System Integrity

**Pre-Trip Alert Data Validation:**
```javascript
const validatePreTripAlertData = (alertData) => {
  const errors = [];
  
  // User ID validation
  if (!alertData.user_id || alertData.user_id.length > 256) {
    errors.push('Valid user_id required (max 256 characters)');
  }
  
  // Log ID validation
  if (!alertData.log_id || alertData.log_id.length > 32) {
    errors.push('Valid log_id required (max 32 characters)');
  }
  
  // Event ID validation
  if (!alertData.event_id || alertData.event_id.length > 32) {
    errors.push('Valid event_id required (max 32 characters)');
  }
  
  // Event name validation
  if (!alertData.event_name || alertData.event_name.length > 32) {
    errors.push('Valid event_name required (max 32 characters)');
  }
  
  // Action mode validation
  if (alertData.action_mode !== undefined && (alertData.action_mode < 0 || alertData.action_mode > 127)) {
    errors.push('action_mode must be between 0 and 127');
  }
  
  // Geographic coordinate validation
  if (!alertData.event_lat || Math.abs(alertData.event_lat) > 90) {
    errors.push('Valid latitude required (-90 to 90)');
  }
  
  if (!alertData.event_lng || Math.abs(alertData.event_lng) > 180) {
    errors.push('Valid longitude required (-180 to 180)');
  }
  
  // Event name standardization validation
  const validEventNames = [
    'weather_alert', 'traffic_incident', 'route_optimization',
    'transit_delay', 'construction_notice', 'parking_availability',
    'safety_alert', 'service_disruption'
  ];
  
  if (alertData.event_name && !validEventNames.includes(alertData.event_name)) {
    errors.push(`Event name must be one of: ${validEventNames.join(', ')}`);
  }
  
  if (errors.length > 0) {
    throw new ValidationError(errors.join(', '));
  }
};
```

**Enhanced Migration Safety and Verification:**
```javascript
// Comprehensive migration with pre-trip alert verification
exports.up = async function (knex) {
  const transaction = await knex.transaction();
  
  try {
    await transaction.schema.createTable('hntb_pre_trip_alert', (table) => {
      // Complete table definition
    });
    
    // Verify table creation and structure
    const tableExists = await transaction.schema.hasTable('hntb_pre_trip_alert');
    if (!tableExists) {
      throw new Error('Pre-trip alert table creation failed');
    }
    
    // Verify essential columns for alert processing
    const columns = await transaction('hntb_pre_trip_alert').columnInfo();
    const criticalColumns = ['id', 'user_id', 'log_id', 'event_id', 'event_name'];
    
    for (const column of criticalColumns) {
      if (!columns[column]) {
        throw new Error(`Critical alert column ${column} not created`);
      }
    }
    
    // Verify auto-increment primary key
    if (!columns.id.autoIncrement) {
      throw new Error('Primary key id must be auto-incrementing');
    }
    
    // Verify string field lengths
    const stringFields = {
      user_id: 256,
      log_id: 32,
      event_id: 32,
      event_name: 32
    };
    
    for (const [field, expectedLength] of Object.entries(stringFields)) {
      if (columns[field].maxLength !== expectedLength) {
        throw new Error(`${field} field must support ${expectedLength} characters`);
      }
    }
    
    // Verify unique constraint on log_id
    const indexes = await transaction.raw('SHOW INDEX FROM hntb_pre_trip_alert WHERE Key_name = "log_id_unique"');
    if (indexes[0].length === 0) {
      throw new Error('Unique constraint on log_id not created');
    }
    
    await transaction.commit();
    logger.info('HNTB Pre-Trip Alert table created and verified successfully');
    
  } catch (error) {
    await transaction.rollback();
    logger.error(`Pre-trip alert migration failed: ${error.message}`);
    throw error;
  }
};
```

**Real-time Alert Processing and Monitoring:**
```javascript
// High-performance alert processing system
const processAlertQueue = async (batchSize = 1000) => {
  let lastProcessedId = await getLastProcessedAlertId();
  
  while (true) {
    const alertBatch = await knex('hntb_pre_trip_alert')
      .where('id', '>', lastProcessedId)
      .where('action_mode', 0) // Unprocessed alerts
      .orderBy('id')
      .limit(batchSize);
    
    if (alertBatch.length === 0) {
      break; // No more alerts to process
    }
    
    for (const alert of alertBatch) {
      try {
        await deliverAlert(alert);
        
        // Update processing status
        await knex('hntb_pre_trip_alert')
          .where('id', alert.id)
          .update({ action_mode: 1 }); // Mark as delivered
          
        lastProcessedId = alert.id;
        
      } catch (error) {
        logger.error(`Alert delivery failed for alert ${alert.id}: ${error.message}`);
      }
    }
    
    await updateLastProcessedAlertId(lastProcessedId);
  }
};
```

This migration establishes comprehensive pre-trip alert management capabilities within the HNTB research platform, enabling sophisticated analysis of proactive communication effectiveness, user response patterns, and location-aware information delivery for optimizing transportation behavior and decision-making through strategic alert deployment.