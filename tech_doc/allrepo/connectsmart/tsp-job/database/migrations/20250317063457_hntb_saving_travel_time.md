# HNTB Saving Travel Time Migration Documentation

## Quick Summary

The HNTB Saving Travel Time migration creates a specialized table for tracking travel time savings and trip efficiency metrics within the HNTB transportation research platform. This migration establishes the `hntb_saving_travel_time` table that captures temporal trip data for analyzing travel time improvements, route optimization effectiveness, and transportation mode efficiency studies. The table serves as a critical component for measuring the impact of transportation interventions and policy changes.

**Key Features:**
- Trip-based primary key system linking to existing trip records
- User correlation through flexible user identification fields
- Activity-based trip categorization for behavioral analysis
- Comprehensive temporal tracking with precise start and end times
- Travel mode classification for multi-modal efficiency comparison
- Automatic timestamp management for data integrity and audit trails

## Technical Analysis

### Database Schema Structure

The migration implements a focused table schema optimized for travel time analysis and trip efficiency research:

```javascript
const tableName = 'hntb_saving_travel_time';

exports.up = async function (knex) {
  try {
    await knex.schema.createTable(tableName, (table) => {
      table.integer('trip_id').unsigned().primary();
      table.string('user_id', 256).notNullable();
      table.integer('activity_id').notNullable();
      table.dateTime('started_on').notNullable().comment('The time that start the trip');
      table.dateTime('ended_on').notNullable().comment('The time that end the trip');
      table.tinyint('mode').notNullable().defaultTo(0);
      table.dateTime('created_on').notNullable().defaultTo(knex.raw('CURRENT_TIMESTAMP'));
      table.dateTime('modified_on').notNullable().defaultTo(knex.raw('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'));
      table.unique(['trip_id'], { indexName: 'trip_id' });
    });
  } catch (e) {
    logger.error(e.message);
    await knex.schema.dropTableIfExists(tableName);
    throw new Error(e);
  }
};
```

### Field Specifications and Data Types

**Primary Identification:**
- `trip_id`: Unsigned integer serving as the primary key for unique trip identification
- Links directly to trip records in the broader HNTB system
- Unique constraint ensures one-to-one relationship with trip data

**User and Activity Association:**
- `user_id`: 256-character string field enabling user correlation across studies
- Non-nullable constraint ensures every record is associated with a research participant
- `activity_id`: Integer field linking trips to specific activity categories or research protocols

**Temporal Data Management:**
- `started_on`: DateTime field capturing precise trip initiation timestamp
- `ended_on`: DateTime field recording exact trip completion time
- Both fields include descriptive comments for documentation clarity
- Enables calculation of total travel time and efficiency metrics

**Travel Mode Classification:**
- `mode`: Tinyint field for compact transportation mode storage
- Default value of 0 provides baseline mode classification
- Required field ensuring every trip has associated mode data for analysis

**Audit Trail Management:**
- `created_on`: Automatic timestamp generation using MySQL CURRENT_TIMESTAMP
- `modified_on`: Auto-updating timestamp with ON UPDATE CURRENT_TIMESTAMP trigger
- Provides complete audit trail for data integrity and change tracking

### Error Handling and Transaction Safety

The migration implements comprehensive error handling with automatic cleanup mechanisms:

```javascript
catch (e) {
  logger.error(e.message);
  await knex.schema.dropTableIfExists(tableName);
  throw new Error(e);
}
```

**Safety Features:**
- Automatic table cleanup on migration failure prevents partial schema states
- Integration with @maas/core/log system for centralized error tracking
- Exception re-throwing maintains proper error propagation chain
- Transaction-safe operations ensure database consistency

### Rollback Implementation

```javascript
exports.down = async function (knex) {
  await knex.schema.dropTable(tableName);
};
```

The rollback function provides clean migration reversal by completely removing the table structure, ensuring complete cleanup for development and testing scenarios.

## Usage/Integration

### Migration Execution Context

**Database Connection:**
- Utilizes Knex.js query builder for database schema management
- Operates within the TSP Job service database infrastructure
- Integrates with the comprehensive HNTB research platform ecosystem

**Migration Timing:**
- Timestamp: March 17, 2025, 06:34:57 GMT (20250317063457)
- Follows foundational HNTB trip and rating migrations
- Precedes specialized alert and targeting system implementations

### Integration with Transportation Research

**Travel Time Analysis Workflow:**
1. Trip initiation triggers record creation with start timestamp
2. Activity classification applied based on trip purpose or research protocol
3. Travel mode detection and recording for efficiency comparison
4. Trip completion triggers end timestamp recording
5. Travel time calculations performed using temporal data
6. Efficiency metrics generated for comparative analysis

**Research Data Applications:**
- Travel time savings calculations for policy impact assessment
- Mode choice efficiency analysis across different transportation options
- Temporal pattern recognition for peak hour optimization
- User behavior tracking across different activity types
- Longitudinal studies of transportation improvement initiatives

### Application Integration Points

**Service Layer Integration:**
```javascript
// Example usage in travel time analysis services
const travelTimeData = {
  trip_id: tripRecord.id,
  user_id: authenticatedUser.id,
  activity_id: classifyActivity(tripPurpose),
  started_on: tripRecord.departure_time,
  ended_on: new Date(),
  mode: detectTravelMode(tripRecord.trajectory)
};

await knex('hntb_saving_travel_time').insert(travelTimeData);

// Calculate travel time savings
const travelDuration = new Date(travelTimeData.ended_on) - new Date(travelTimeData.started_on);
const expectedDuration = await calculateExpectedTravelTime(tripRecord);
const timeSavings = expectedDuration - travelDuration;
```

**Analytics Integration:**
- Powers real-time travel time efficiency dashboards
- Supports comparative analysis across different transportation modes
- Enables activity-based travel pattern analysis
- Facilitates policy impact measurement and reporting

## Dependencies

### Core Framework Dependencies

**Knex.js Query Builder:**
- Version compatibility with TSP Job service Knex configuration
- Requires MySQL database connection with appropriate schema privileges
- Utilizes Knex migration system for version control and deployment management

**@maas/core/log System:**
```javascript
const { logger } = require('@maas/core/log');
```
- Integrates with centralized logging infrastructure for error tracking
- Provides structured error reporting and audit trail capabilities
- Supports distributed logging across microservice architecture

### Database Requirements

**MySQL Database System:**
- Requires MySQL 5.7+ for proper timestamp handling and trigger support
- Utilizes CURRENT_TIMESTAMP and ON UPDATE CURRENT_TIMESTAMP features
- Depends on proper timezone configuration for accurate temporal calculations

**Schema Permissions:**
- CREATE TABLE privileges for schema modification operations
- DROP TABLE privileges for rollback and cleanup operations
- INDEX creation permissions for unique constraint implementation

### Platform Integration Dependencies

**HNTB Research Platform:**
- Coordinates with trip management systems for trip_id validation
- Integrates with user management systems for participant tracking
- Connects with activity classification systems for research categorization
- Supports data export pipelines for research analysis tools

**TSP Job Service Architecture:**
- Operates within TSP Job microservice context
- Utilizes shared database connection pooling for performance
- Integrates with background job processing systems for data analysis

## Code Examples

### Migration Execution Commands

**Running the Migration:**
```bash
# Execute migration in TSP Job service context
cd allrepo/connectsmart/tsp-job
npx knex migrate:up --env production

# Verify migration status and table creation
npx knex migrate:status
npx knex migrate:current
```

**Migration Rollback:**
```bash
# Rollback specific migration
npx knex migrate:down --env production

# Rollback to specific version
npx knex migrate:rollback --to=20250317063457
```

### Database Interaction Examples

**Travel Time Data Recording:**
```javascript
const knex = require('./database/connection');

// Insert travel time record
const newTravelTimeRecord = await knex('hntb_saving_travel_time').insert({
  trip_id: 789012,
  user_id: 'research_participant_456',
  activity_id: 101, // Commute activity
  started_on: '2025-03-17 08:15:00',
  ended_on: '2025-03-17 08:45:00',
  mode: 1 // Public transit
});

// Query travel time data with temporal filtering
const recentTravelTimes = await knex('hntb_saving_travel_time')
  .where('started_on', '>=', knex.raw('DATE_SUB(NOW(), INTERVAL 7 DAY)'))
  .where('mode', 1)
  .orderBy('started_on', 'desc')
  .limit(50);
```

**Travel Time Analysis Queries:**
```javascript
// Calculate average travel times by mode
const modeEfficiency = await knex('hntb_saving_travel_time')
  .select('mode')
  .avg(knex.raw('TIMESTAMPDIFF(MINUTE, started_on, ended_on) as avg_duration'))
  .count('* as trip_count')
  .groupBy('mode')
  .orderBy('avg_duration');

// Activity-based travel pattern analysis
const activityPatterns = await knex('hntb_saving_travel_time')
  .select('activity_id')
  .avg(knex.raw('TIMESTAMPDIFF(MINUTE, started_on, ended_on) as avg_duration'))
  .min(knex.raw('TIMESTAMPDIFF(MINUTE, started_on, ended_on) as min_duration'))
  .max(knex.raw('TIMESTAMPDIFF(MINUTE, started_on, ended_on) as max_duration'))
  .count('* as frequency')
  .groupBy('activity_id')
  .having('frequency', '>', 10);

// Time-of-day efficiency analysis
const hourlyEfficiency = await knex('hntb_saving_travel_time')
  .select(knex.raw('HOUR(started_on) as departure_hour'))
  .avg(knex.raw('TIMESTAMPDIFF(MINUTE, started_on, ended_on) as avg_duration'))
  .count('* as trips')
  .groupBy(knex.raw('HOUR(started_on)'))
  .orderBy('departure_hour');
```

### Travel Time Calculation Functions

**Duration Analysis Implementation:**
```javascript
// Travel time efficiency calculator
const calculateTravelEfficiency = async (userId, activityId, timeRange) => {
  const travelTimes = await knex('hntb_saving_travel_time')
    .where('user_id', userId)
    .where('activity_id', activityId)
    .whereBetween('started_on', timeRange)
    .select('*');

  const durations = travelTimes.map(record => ({
    duration: new Date(record.ended_on) - new Date(record.started_on),
    mode: record.mode,
    tripId: record.trip_id
  }));

  return {
    averageDuration: durations.reduce((sum, d) => sum + d.duration, 0) / durations.length,
    modeDistribution: groupBy(durations, 'mode'),
    totalTrips: durations.length,
    timeRange: timeRange
  };
};

// Mode comparison analysis
const compareModeEfficiency = async (modes, dateRange) => {
  const comparison = {};
  
  for (const mode of modes) {
    const modeData = await knex('hntb_saving_travel_time')
      .where('mode', mode)
      .whereBetween('started_on', dateRange)
      .select(knex.raw('AVG(TIMESTAMPDIFF(MINUTE, started_on, ended_on)) as avg_duration'))
      .select(knex.raw('COUNT(*) as trip_count'))
      .first();
    
    comparison[mode] = {
      averageDuration: parseFloat(modeData.avg_duration),
      tripCount: parseInt(modeData.trip_count),
      efficiency: calculateEfficiencyScore(modeData.avg_duration, mode)
    };
  }
  
  return comparison;
};
```

### Error Handling and Validation

**Data Validation Patterns:**
```javascript
// Travel time record validation
const validateTravelTimeData = (data) => {
  const errors = [];
  
  if (!data.trip_id || data.trip_id <= 0) {
    errors.push('Valid trip_id required');
  }
  
  if (!data.user_id || data.user_id.length > 256) {
    errors.push('Valid user_id required (max 256 characters)');
  }
  
  if (!data.activity_id) {
    errors.push('Activity ID is required');
  }
  
  const startTime = new Date(data.started_on);
  const endTime = new Date(data.ended_on);
  
  if (startTime >= endTime) {
    errors.push('End time must be after start time');
  }
  
  if ((endTime - startTime) > 24 * 60 * 60 * 1000) {
    errors.push('Travel duration exceeds maximum allowed (24 hours)');
  }
  
  if (data.mode < 0 || data.mode > 255) {
    errors.push('Mode value must be between 0 and 255');
  }
  
  if (errors.length > 0) {
    throw new ValidationError(errors.join(', '));
  }
};

// Safe insertion with validation
const insertTravelTimeRecord = async (data) => {
  validateTravelTimeData(data);
  
  try {
    const result = await knex('hntb_saving_travel_time').insert(data);
    logger.info(`Travel time record inserted for trip ${data.trip_id}`);
    return result;
  } catch (error) {
    if (error.code === 'ER_DUP_ENTRY') {
      throw new Error(`Travel time record already exists for trip ${data.trip_id}`);
    }
    logger.error(`Failed to insert travel time record: ${error.message}`);
    throw error;
  }
};
```

This migration establishes essential infrastructure for measuring and analyzing travel time efficiency within the HNTB transportation research platform, enabling comprehensive studies of transportation improvements and policy interventions.