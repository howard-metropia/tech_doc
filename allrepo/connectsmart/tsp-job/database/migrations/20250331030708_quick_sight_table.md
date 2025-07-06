# Quick Sight Table Migration Documentation

## Quick Summary

The Quick Sight Table migration creates a comprehensive suite of database tables designed to support AWS QuickSight analytics and business intelligence reporting within the TSP Job service. This migration establishes multiple interconnected tables that collectively provide a complete data foundation for real-time analytics, user transaction tracking, payment processing, and comprehensive business intelligence dashboards. The migration includes core user management, transaction processing, transit ticketing, and activity tracking tables essential for multi-modal transportation analytics.

**Key Features:**
- Comprehensive user authentication and profile management system
- Multi-currency transaction processing with points, tokens, and traditional payments
- Advanced transit ticketing integration with Bytemark payment system
- Real-time activity tracking and behavioral analytics
- Campaign management and promotional code systems
- Referral tracking and user engagement metrics
- Comprehensive audit trails and temporal data management

## Technical Analysis

### Database Schema Structure

The migration implements a complex multi-table schema using raw SQL for optimal database-specific features:

```javascript
exports.up = async function (knex) {
  try {
    await knex.schema.raw('CREATE TABLE IF NOT EXISTS `points_transaction` (...)');
    await knex.schema.raw('CREATE TABLE IF NOT EXISTS `bytemark_order_payments` (...)');
    await knex.schema.raw('CREATE TABLE IF NOT EXISTS `bytemark_order_items` (...)');
    // ... multiple table creations
  } catch (e) {
    logger.error(e.message);
    throw new Error(e);
  }
};
```

### Core Table Specifications

**Points Transaction System:**
```sql
CREATE TABLE `points_transaction` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `activity_type` int NOT NULL,
  `points` decimal(10,2) NOT NULL,
  `balance` decimal(10,2) NOT NULL,
  `note` varchar(200) DEFAULT NULL,
  `created_on` datetime NOT NULL,
  `payer` int NOT NULL DEFAULT '0' COMMENT 'who pay the coins',
  `payee` int NOT NULL DEFAULT '0' COMMENT 'who receive the coins',
  `ref_transaction_id` int NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
```

**Token Transaction Management:**
```sql
CREATE TABLE `token_transaction` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL DEFAULT '0',
  `enterprise_id` int(11) DEFAULT NULL,
  `activity_type` int(11) DEFAULT NULL,
  `tokens` decimal(10,2) DEFAULT NULL,
  `balance` decimal(10,2) DEFAULT NULL,
  `campaign_id` int(11) DEFAULT NULL,
  `f_agency_id` int(11) NOT NULL DEFAULT '0',
  `f_token_id` int(11) NOT NULL DEFAULT '0',
  `issued_on` datetime DEFAULT CURRENT_TIMESTAMP,
  `expired_on` datetime DEFAULT CURRENT_TIMESTAMP,
  KEY `main_query_index_1` (`user_id`,`activity_type`,`f_agency_id`,`f_token_id`,`issued_on`,`expired_on`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
```

**Comprehensive User Management:**
```sql
CREATE TABLE `auth_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `first_name` varchar(128) DEFAULT NULL,
  `last_name` varchar(128) DEFAULT NULL,
  `email` varchar(512) DEFAULT NULL,
  `google_id` varchar(32) DEFAULT NULL,
  `facebook_id` varchar(32) DEFAULT NULL,
  `apple_id` varchar(512) DEFAULT NULL,
  `registration_latitude` double DEFAULT NULL,
  `registration_longitude` double DEFAULT NULL,
  `device_token` varchar(512) DEFAULT NULL,
  `enterprise_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
```

### Transit Integration Tables

**Bytemark Payment Processing:**
- `bytemark_order_payments`: Maps payment methods to transit orders
- `bytemark_order_items`: Tracks individual ticket items and passes
- `bytemark_pass`: Records pass usage and validation events

**Transit Activity Tracking:**
- `trip`: Comprehensive trip recording with multimodal support
- `cm_activity_location`: Advanced activity location clustering
- `user_rating`: Trip quality and satisfaction feedback

### Analytics and Campaign Management

**Campaign System:**
```sql
CREATE TABLE `campaign` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `ap_campaign_id` int(11) NOT NULL DEFAULT '0',
  `token_id` int(11) NOT NULL DEFAULT '0',
  `name` varchar(32) NOT NULL DEFAULT '',
  `tokens` decimal(10,2) NOT NULL DEFAULT '0.00',
  PRIMARY KEY (`id`),
  UNIQUE KEY `ap_campaign_id` (`ap_campaign_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
```

**User Labeling and Segmentation:**
- `user_label`: Categorical user classification system
- `auth_user_label`: Many-to-many user-label relationships
- `referral_history`: User acquisition and referral tracking

### Error Handling and Transaction Safety

```javascript
catch (e) {
  logger.error(e.message);
  throw new Error(e);
}
```

**Safety Features:**
- Comprehensive error logging through @maas/core/log system
- Transaction-safe table creation with IF NOT EXISTS clauses
- Proper exception handling and error propagation

### Rollback Implementation

```javascript
exports.down = async function (knex) {
  const tables = [
    'points_transaction', 'token_transaction', 'bytemark_order_payments',
    'auth_user', 'trip', 'campaign', 'user_label', 'auth_user_label'
    // ... complete table list
  ];
  
  await Promise.all(
    tables.map(async (table) => {
      try {
        await knex.schema.raw(`DROP TABLE IF EXISTS ${table}`);
      } catch (e) {
        logger.error(e.message);
      }
    })
  );
};
```

## Usage/Integration

### Migration Execution Context

**Database Connection:**
- Utilizes Knex.js with raw SQL for database-specific optimizations
- Operates within the TSP Job service database infrastructure
- Integrates with AWS QuickSight for real-time analytics and reporting

**Migration Timing:**
- Timestamp: March 31, 2025, 03:07:08 GMT (20250331030708)
- Represents major analytics infrastructure deployment
- Establishes foundation for comprehensive business intelligence capabilities

### Integration with AWS QuickSight

**Analytics Workflow:**
1. Transactional data flows into core tables (points, tokens, trips)
2. User activity captured through auth_user and trip tables
3. Campaign effectiveness tracked through campaign and token_transaction tables
4. QuickSight connects to tables for real-time dashboard generation
5. Complex analytics queries supported through optimized indexing
6. Business intelligence reports generated for stakeholder consumption

**Dashboard Applications:**
- Real-time transaction volume and revenue analytics
- User engagement and retention metrics
- Transit system utilization patterns
- Campaign performance and ROI analysis
- Geographic activity distribution and hotspot identification

### Application Integration Points

**Service Layer Integration:**
```javascript
// Transaction processing example
const processPointsTransaction = async (transactionData) => {
  const transaction = await knex.transaction();
  
  try {
    // Insert points transaction
    const [transactionId] = await transaction('points_transaction').insert({
      user_id: transactionData.userId,
      activity_type: transactionData.activityType,
      points: transactionData.points,
      balance: await calculateNewBalance(transactionData.userId, transactionData.points),
      note: transactionData.note,
      created_on: new Date(),
      payer: transactionData.payer,
      payee: transactionData.payee
    });
    
    // Update user balance
    await transaction('auth_user')
      .where('id', transactionData.userId)
      .update({ modified_on: new Date() });
    
    await transaction.commit();
    return transactionId;
  } catch (error) {
    await transaction.rollback();
    throw error;
  }
};
```

**Analytics Integration:**
- Powers real-time QuickSight dashboards and reports
- Supports complex business intelligence queries across multiple tables
- Enables predictive analytics through historical data analysis
- Facilitates A/B testing and campaign optimization

## Dependencies

### Core Framework Dependencies

**Knex.js Query Builder:**
- Version compatibility with TSP Job service Knex configuration
- Raw SQL capabilities for database-specific optimizations
- Transaction management for complex multi-table operations

**@maas/core/log System:**
```javascript
const { logger } = require('@maas/core/log');
```
- Centralized logging for migration operations and error tracking
- Structured error reporting for database operations
- Integration with monitoring and alerting systems

### Database Requirements

**MySQL Database System:**
- Requires MySQL 5.7+ for JSON, spatial, and advanced indexing features
- UTF8MB4 character set support for international data
- InnoDB storage engine for ACID compliance and foreign key support

**Performance Optimization:**
- Complex indexing strategies for analytics queries
- Partitioning support for large transaction tables
- Connection pooling for high-volume operations

### External Service Dependencies

**AWS QuickSight Integration:**
- Database connectivity and authentication configuration
- IAM roles and permissions for QuickSight data access
- Network connectivity between QuickSight and database infrastructure

**Payment System Integration:**
- Bytemark API connectivity for transit payment processing
- Stripe integration for traditional payment methods
- Real-time transaction validation and processing capabilities

## Code Examples

### Migration Execution Commands

**Running the Migration:**
```bash
# Execute migration in TSP Job service context
cd allrepo/connectsmart/tsp-job
npx knex migrate:up --env production

# Verify table creation and structure
mysql -e "SHOW TABLES LIKE '%transaction%';"
mysql -e "DESCRIBE points_transaction;"
```

**Migration Rollback:**
```bash
# Rollback all QuickSight tables
npx knex migrate:down --env production

# Verify cleanup
mysql -e "SHOW TABLES;"
```

### Complex Analytics Queries

**Revenue Analytics:**
```javascript
// Daily revenue analysis across all payment types
const getDailyRevenue = async (dateRange) => {
  const pointsRevenue = await knex('points_transaction')
    .select(knex.raw('DATE(created_on) as date'))
    .sum('points as total_points')
    .whereBetween('created_on', dateRange)
    .where('points', '>', 0)
    .groupBy(knex.raw('DATE(created_on)'));
  
  const tokenRevenue = await knex('token_transaction')
    .select(knex.raw('DATE(created_on) as date'))
    .sum('tokens as total_tokens')
    .whereBetween('created_on', dateRange)
    .where('tokens', '>', 0)
    .groupBy(knex.raw('DATE(created_on)'));
  
  const bytemarkRevenue = await knex('bytemark_order_payments')
    .select(knex.raw('DATE(created_on) as date'))
    .sum('total_price as total_amount')
    .whereBetween('created_on', dateRange)
    .groupBy(knex.raw('DATE(created_on)'));
  
  return { pointsRevenue, tokenRevenue, bytemarkRevenue };
};
```

**User Engagement Analytics:**
```javascript
// Comprehensive user activity analysis
const getUserEngagementMetrics = async (timeframe = 30) => {
  const baseQuery = knex('auth_user as u')
    .leftJoin('points_transaction as pt', 'u.id', 'pt.user_id')
    .leftJoin('token_transaction as tt', 'u.id', 'tt.user_id')
    .leftJoin('trip as t', 'u.id', 't.user_id')
    .where('u.created_on', '>=', knex.raw(`DATE_SUB(NOW(), INTERVAL ${timeframe} DAY)`));
  
  const engagement = await baseQuery
    .select('u.id', 'u.first_name', 'u.last_name', 'u.enterprise_id')
    .count('pt.id as points_transactions')
    .count('tt.id as token_transactions')
    .count('t.id as trips')
    .sum('pt.points as total_points')
    .sum('tt.tokens as total_tokens')
    .groupBy('u.id', 'u.first_name', 'u.last_name', 'u.enterprise_id')
    .having('points_transactions', '>', 0)
    .orHaving('token_transactions', '>', 0)
    .orHaving('trips', '>', 0)
    .orderBy('total_points', 'desc');
  
  return engagement;
};
```

**Campaign Performance Analysis:**
```javascript
// Campaign effectiveness and ROI calculation
const analyzeCampaignPerformance = async (campaignId) => {
  const campaignData = await knex('campaign')
    .where('ap_campaign_id', campaignId)
    .first();
  
  const tokenDistribution = await knex('token_transaction')
    .where('ap_campaign_id', campaignId)
    .select(
      knex.raw('COUNT(DISTINCT user_id) as unique_recipients'),
      knex.raw('SUM(tokens) as total_distributed'),
      knex.raw('AVG(tokens) as avg_per_user'),
      knex.raw('MIN(issued_on) as campaign_start'),
      knex.raw('MAX(issued_on) as campaign_end')
    )
    .first();
  
  const userEngagement = await knex('token_transaction as tt')
    .join('trip as t', 'tt.user_id', 't.user_id')
    .where('tt.ap_campaign_id', campaignId)
    .where('t.started_on', '>=', knex.ref('tt.issued_on'))
    .select(
      knex.raw('COUNT(DISTINCT tt.user_id) as engaged_users'),
      knex.raw('COUNT(t.id) as post_campaign_trips'),
      knex.raw('AVG(DATEDIFF(t.started_on, tt.issued_on)) as avg_days_to_engagement')
    )
    .first();
  
  return {
    campaign: campaignData,
    distribution: tokenDistribution,
    engagement: userEngagement,
    engagementRate: userEngagement.engaged_users / tokenDistribution.unique_recipients
  };
};
```

### Real-time Dashboard Queries

**Trip Analytics for QuickSight:**
```javascript
// Optimized queries for QuickSight dashboard consumption
const getTripAnalytics = async () => {
  // Hourly trip distribution
  const hourlyTrips = await knex('trip')
    .select(
      knex.raw('HOUR(started_on) as hour'),
      knex.raw('DAYOFWEEK(started_on) as day_of_week'),
      'travel_mode'
    )
    .count('* as trip_count')
    .avg('distance as avg_distance')
    .where('started_on', '>=', knex.raw('DATE_SUB(NOW(), INTERVAL 7 DAY)'))
    .groupBy('hour', 'day_of_week', 'travel_mode')
    .orderBy(['day_of_week', 'hour']);
  
  // Geographic activity hotspots
  const activityHotspots = await knex('cm_activity_location')
    .select('o_id', 'd_id', 'travel_mode')
    .count('* as frequency')
    .avg('probability_driving as avg_drive_prob')
    .avg('probability_transit as avg_transit_prob')
    .groupBy('o_id', 'd_id', 'travel_mode')
    .having('frequency', '>', 10)
    .orderBy('frequency', 'desc')
    .limit(100);
  
  return { hourlyTrips, activityHotspots };
};
```

### Data Validation and Integrity

**Multi-table Validation:**
```javascript
// Comprehensive data integrity validation
const validateQuickSightData = async () => {
  const validationResults = {};
  
  // Check transaction balance consistency
  const balanceConsistency = await knex.raw(`
    SELECT 
      user_id,
      COUNT(*) as transaction_count,
      SUM(points) as total_points_change,
      MAX(balance) as final_balance,
      (SELECT SUM(points) FROM points_transaction pt2 
       WHERE pt2.user_id = pt1.user_id AND pt2.id <= MAX(pt1.id)) as calculated_balance
    FROM points_transaction pt1
    GROUP BY user_id
    HAVING final_balance != calculated_balance
  `);
  
  // Verify referral integrity
  const referralIntegrity = await knex('referral_history as rh')
    .leftJoin('auth_user as sender', 'rh.sender_user_id', 'sender.id')
    .leftJoin('auth_user as receiver', 'rh.receiver_user_id', 'receiver.id')
    .whereNull('sender.id')
    .orWhereNull('receiver.id')
    .select('rh.*');
  
  // Check campaign token allocation
  const campaignTokens = await knex('campaign')
    .leftJoin('token_transaction', 'campaign.ap_campaign_id', 'token_transaction.ap_campaign_id')
    .select('campaign.ap_campaign_id', 'campaign.tokens as allocated')
    .sum('token_transaction.tokens as distributed')
    .groupBy('campaign.ap_campaign_id', 'campaign.tokens')
    .having('distributed', '>', knex.ref('allocated'));
  
  return {
    balanceInconsistencies: balanceConsistency[0],
    brokenReferrals: referralIntegrity,
    overDistributedCampaigns: campaignTokens
  };
};

// Automated data quality monitoring
const monitorDataQuality = async () => {
  const issues = [];
  
  // Check for duplicate transactions
  const duplicateTransactions = await knex('points_transaction')
    .select('user_id', 'created_on', 'points', 'activity_type')
    .count('* as count')
    .groupBy('user_id', 'created_on', 'points', 'activity_type')
    .having('count', '>', 1);
  
  if (duplicateTransactions.length > 0) {
    issues.push({ type: 'duplicate_transactions', count: duplicateTransactions.length });
  }
  
  // Check for invalid geographic coordinates
  const invalidCoordinates = await knex('auth_user')
    .where(function() {
      this.where('registration_latitude', '>', 90)
        .orWhere('registration_latitude', '<', -90)
        .orWhere('registration_longitude', '>', 180)
        .orWhere('registration_longitude', '<', -180);
    })
    .count('* as count')
    .first();
  
  if (invalidCoordinates.count > 0) {
    issues.push({ type: 'invalid_coordinates', count: invalidCoordinates.count });
  }
  
  return issues;
};
```

This migration establishes the complete analytical foundation for AWS QuickSight integration, providing comprehensive transaction tracking, user management, and business intelligence capabilities essential for modern transportation service analytics and reporting.