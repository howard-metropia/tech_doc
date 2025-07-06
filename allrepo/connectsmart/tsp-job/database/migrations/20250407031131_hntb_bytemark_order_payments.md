# HNTB Bytemark Order Payments Migration Documentation

## Quick Summary

The HNTB Bytemark Order Payments migration creates a specialized table for tracking payment transactions within the HNTB transportation research platform's integration with Bytemark transit ticketing systems. This migration establishes the `hntb_bytemark_order_payments` table that captures detailed payment information for transit pass purchases, enabling researchers to analyze payment patterns, pricing effectiveness, and financial transaction flows within transit systems. The table serves as a critical component for understanding transit payment behaviors and supporting economic analysis of transportation interventions.

**Key Features:**
- Payment-based primary key system for unique transaction identification
- User correlation through flexible identification fields for behavioral tracking
- Order association linking payments to specific transit ticket purchases
- Payment type classification for multi-modal payment method analysis
- Precise financial tracking with double-precision pricing data
- Temporal logging for payment timing analysis and transaction audit trails
- Automatic timestamp management for data integrity and change tracking

## Technical Analysis

### Database Schema Structure

The migration implements a focused table schema optimized for transit payment tracking and financial analysis:

```javascript
const tableName = 'hntb_bytemark_order_payments';

exports.up = async function (knex) {
  try {
    await knex.schema.createTable(tableName, (table) => {
      table.integer('payment_id').unsigned().primary();
      table.string('user_id', 256).notNullable();
      table.integer('order_id').notNullable();
      table.string('payment_type', 32).notNullable();
      table.double('total_price').notNullable();
      table.dateTime('logged_on').notNullable().comment('The time that logged the bytemark pass');
      table.dateTime('created_on').notNullable().defaultTo(knex.raw('CURRENT_TIMESTAMP'));
      table.dateTime('modified_on').notNullable().defaultTo(knex.raw('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'));
      table.unique(['payment_id'], { indexName: 'payment_id' });
    });
  } catch (e) {
    logger.error(e.message);
    await knex.schema.dropTableIfExists(tableName);
    throw new Error(e);
  }
};
```

### Field Specifications and Data Types

**Primary Identification System:**
- `payment_id`: Unsigned integer serving as the primary key for unique payment identification
- Links directly to Bytemark payment processing system records
- Unique constraint ensures one-to-one relationship with payment transactions

**User and Order Association:**
- `user_id`: 256-character string field enabling cross-study user correlation
- Non-nullable constraint ensures every payment is associated with a research participant
- `order_id`: Integer field linking payments to specific transit ticket orders

**Payment Classification System:**
- `payment_type`: 32-character string field for payment method categorization
- Supports various payment types (credit card, mobile payment, transit card, etc.)
- Required field ensuring every payment has associated method classification

**Financial Data Management:**
- `total_price`: Double precision field for accurate monetary value storage
- Required field ensuring complete financial transaction recording
- Supports decimal precision for various currency denominations

**Temporal Data Tracking:**
- `logged_on`: DateTime field capturing when the Bytemark pass transaction was logged
- Includes descriptive comment for documentation clarity
- Enables analysis of payment processing timing and system performance
- `created_on`: Automatic timestamp generation using MySQL CURRENT_TIMESTAMP
- `modified_on`: Auto-updating timestamp with ON UPDATE CURRENT_TIMESTAMP trigger

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
- Automatic table cleanup on migration failure prevents inconsistent schema states
- Integration with @maas/core/log system for centralized error monitoring
- Exception re-throwing maintains proper error propagation through the system
- Transaction-safe operations ensure database consistency during deployment

### Rollback Implementation

```javascript
exports.down = async function (knex) {
  await knex.schema.dropTable(tableName);
};
```

The rollback function provides complete migration reversal by removing the entire table structure, ensuring clean environment restoration for testing and development scenarios.

## Usage/Integration

### Migration Execution Context

**Database Connection:**
- Utilizes Knex.js query builder for standardized database schema management
- Operates within the TSP Job service database infrastructure
- Integrates with the comprehensive HNTB research platform ecosystem

**Migration Timing:**
- Timestamp: April 7, 2025, 03:11:31 GMT (20250407031131)
- Follows comprehensive QuickSight analytics infrastructure deployment
- Supports specialized Bytemark payment integration and financial analysis

### Integration with Bytemark Payment System

**Payment Transaction Workflow:**
1. User initiates transit pass purchase through Bytemark system
2. Payment processing completed with method and amount tracking
3. Transaction logged with temporal data for research analysis
4. Payment record created with comprehensive metadata
5. Financial data aggregated for pricing and economic analysis
6. Research insights generated from payment pattern analysis

**Research Applications:**
- Transit payment method preference analysis and trends
- Pricing sensitivity studies for different user segments
- Payment processing performance and timing analysis
- Economic impact assessment of transit pricing policies
- Cross-modal payment behavior comparison and research
- Financial transaction flow analysis for system optimization

### Application Integration Points

**Service Layer Integration:**
```javascript
// Example usage in Bytemark payment processing services
const paymentData = {
  payment_id: bytemarkResponse.paymentId,
  user_id: authenticatedUser.id,
  order_id: transitOrder.id,
  payment_type: classifyPaymentMethod(paymentInfo),
  total_price: calculateTotalPrice(orderItems),
  logged_on: new Date(bytemarkResponse.timestamp)
};

await knex('hntb_bytemark_order_payments').insert(paymentData);

// Query payment patterns for analysis
const paymentPatterns = await knex('hntb_bytemark_order_payments')
  .where('payment_type', paymentType)
  .whereBetween('logged_on', dateRange)
  .select('*')
  .orderBy('logged_on', 'desc');
```

**Analytics Integration:**
- Powers financial dashboard analytics and revenue tracking
- Enables payment method effectiveness analysis and optimization
- Supports pricing strategy research and policy development
- Facilitates economic impact studies of transportation interventions

## Dependencies

### Core Framework Dependencies

**Knex.js Query Builder:**
- Version compatibility with TSP Job service Knex configuration
- Requires MySQL database connection with appropriate financial data handling
- Utilizes Knex migration system for version control and deployment automation

**@maas/core/log System:**
```javascript
const { logger } = require('@maas/core/log');
```
- Integrates with centralized logging infrastructure for comprehensive error tracking
- Provides structured error reporting and audit trail capabilities
- Supports distributed logging across the microservice architecture

### Database Requirements

**MySQL Database System:**
- Requires MySQL 5.7+ for proper double precision handling and timestamp functionality
- Utilizes CURRENT_TIMESTAMP and ON UPDATE CURRENT_TIMESTAMP features
- Depends on proper timezone configuration for accurate temporal tracking

**Financial Data Handling:**
- Double precision support for accurate monetary value storage
- Proper decimal handling for currency calculations and aggregations
- Character set support for international payment type descriptions

### External Service Dependencies

**Bytemark API Integration:**
- Real-time connectivity with Bytemark transit ticketing platform
- Payment processing webhook integration for transaction notifications
- API authentication and security token management
- Transaction validation and reconciliation capabilities

**HNTB Research Platform:**
- Coordinates with payment processing systems for transaction validation
- Integrates with user management systems for participant tracking
- Connects with order management systems for comprehensive transaction recording
- Supports financial analysis tools and reporting systems

## Code Examples

### Migration Execution Commands

**Running the Migration:**
```bash
# Execute migration in TSP Job service context
cd allrepo/connectsmart/tsp-job
npx knex migrate:up --env production

# Verify migration status and table structure
npx knex migrate:status
mysql -e "DESCRIBE hntb_bytemark_order_payments;"
```

**Migration Rollback:**
```bash
# Rollback specific migration
npx knex migrate:down --env production

# Rollback to previous version
npx knex migrate:rollback --to=20250407031131
```

### Database Interaction Examples

**Payment Transaction Recording:**
```javascript
const knex = require('./database/connection');

// Process Bytemark payment transaction
const processPaymentTransaction = async (bytemarkData, userContext) => {
  const paymentRecord = {
    payment_id: bytemarkData.payment_id,
    user_id: userContext.research_id,
    order_id: bytemarkData.order_id,
    payment_type: normalizePaymentType(bytemarkData.payment_method),
    total_price: parseFloat(bytemarkData.amount),
    logged_on: new Date(bytemarkData.timestamp)
  };
  
  const result = await knex('hntb_bytemark_order_payments').insert(paymentRecord);
  return result;
};

// Query payment data with filtering
const getPaymentTransactions = async (filters) => {
  let query = knex('hntb_bytemark_order_payments');
  
  if (filters.userId) {
    query = query.where('user_id', filters.userId);
  }
  
  if (filters.paymentType) {
    query = query.where('payment_type', filters.paymentType);
  }
  
  if (filters.dateRange) {
    query = query.whereBetween('logged_on', filters.dateRange);
  }
  
  if (filters.priceRange) {
    query = query.whereBetween('total_price', [filters.priceRange.min, filters.priceRange.max]);
  }
  
  return await query
    .select('*')
    .orderBy('logged_on', 'desc')
    .limit(filters.limit || 100);
};
```

**Financial Analysis Queries:**
```javascript
// Payment method distribution analysis
const analyzePaymentMethods = async (timeframe = 30) => {
  return await knex('hntb_bytemark_order_payments')
    .select('payment_type')
    .count('* as transaction_count')
    .sum('total_price as total_revenue')
    .avg('total_price as avg_transaction_value')
    .where('logged_on', '>=', knex.raw(`DATE_SUB(NOW(), INTERVAL ${timeframe} DAY)`))
    .groupBy('payment_type')
    .orderBy('total_revenue', 'desc');
};

// User spending pattern analysis
const analyzeUserSpending = async (userId) => {
  const spendingData = await knex('hntb_bytemark_order_payments')
    .where('user_id', userId)
    .select(
      knex.raw('COUNT(*) as total_transactions'),
      knex.raw('SUM(total_price) as total_spent'),
      knex.raw('AVG(total_price) as avg_transaction'),
      knex.raw('MIN(total_price) as min_transaction'),
      knex.raw('MAX(total_price) as max_transaction'),
      knex.raw('MIN(logged_on) as first_payment'),
      knex.raw('MAX(logged_on) as latest_payment')
    )
    .first();
  
  const monthlySpending = await knex('hntb_bytemark_order_payments')
    .where('user_id', userId)
    .select(
      knex.raw('YEAR(logged_on) as year'),
      knex.raw('MONTH(logged_on) as month'),
      knex.raw('COUNT(*) as transactions'),
      knex.raw('SUM(total_price) as monthly_total')
    )
    .groupBy('year', 'month')
    .orderBy(['year', 'month']);
  
  return { overview: spendingData, monthly: monthlySpending };
};

// Revenue trend analysis
const analyzeRevenueTrends = async (period = 'daily') => {
  let dateFormat;
  let groupBy;
  
  switch (period) {
    case 'hourly':
      dateFormat = 'DATE_FORMAT(logged_on, "%Y-%m-%d %H:00:00")';
      groupBy = 'hour';
      break;
    case 'daily':
      dateFormat = 'DATE(logged_on)';
      groupBy = 'date';
      break;
    case 'weekly':
      dateFormat = 'YEARWEEK(logged_on)';
      groupBy = 'week';
      break;
    case 'monthly':
      dateFormat = 'DATE_FORMAT(logged_on, "%Y-%m")';
      groupBy = 'month';
      break;
    default:
      dateFormat = 'DATE(logged_on)';
      groupBy = 'date';
  }
  
  return await knex('hntb_bytemark_order_payments')
    .select(knex.raw(`${dateFormat} as ${groupBy}`))
    .count('* as transactions')
    .sum('total_price as revenue')
    .avg('total_price as avg_transaction_value')
    .where('logged_on', '>=', knex.raw('DATE_SUB(NOW(), INTERVAL 90 DAY)'))
    .groupBy(knex.raw(dateFormat))
    .orderBy(groupBy);
};
```

### Payment Processing Integration

**Bytemark Webhook Processing:**
```javascript
// Process incoming Bytemark payment notifications
const processBytemarkWebhook = async (webhookData) => {
  try {
    // Validate webhook signature
    const isValid = await validateBytemarkSignature(webhookData);
    if (!isValid) {
      throw new Error('Invalid webhook signature');
    }
    
    // Extract payment information
    const paymentInfo = {
      payment_id: webhookData.payment_id,
      user_id: await mapBytemarkUserToResearchId(webhookData.user_id),
      order_id: webhookData.order_id,
      payment_type: normalizePaymentType(webhookData.payment_method),
      total_price: parseFloat(webhookData.amount),
      logged_on: new Date(webhookData.timestamp)
    };
    
    // Check for duplicate processing
    const existingPayment = await knex('hntb_bytemark_order_payments')
      .where('payment_id', paymentInfo.payment_id)
      .first();
    
    if (existingPayment) {
      logger.warn(`Duplicate payment processing attempt: ${paymentInfo.payment_id}`);
      return existingPayment;
    }
    
    // Insert payment record
    const result = await knex('hntb_bytemark_order_payments').insert(paymentInfo);
    
    // Trigger analytics update
    await updatePaymentAnalytics(paymentInfo);
    
    logger.info(`Payment processed successfully: ${paymentInfo.payment_id}`);
    return result;
    
  } catch (error) {
    logger.error(`Bytemark webhook processing failed: ${error.message}`);
    throw error;
  }
};

// Payment type normalization
const normalizePaymentType = (rawPaymentMethod) => {
  const paymentTypeMap = {
    'credit_card': 'credit_card',
    'debit_card': 'debit_card',
    'apple_pay': 'mobile_payment',
    'google_pay': 'mobile_payment',
    'transit_card': 'transit_card',
    'bank_transfer': 'bank_transfer',
    'digital_wallet': 'digital_wallet'
  };
  
  return paymentTypeMap[rawPaymentMethod.toLowerCase()] || 'other';
};

// Real-time analytics update
const updatePaymentAnalytics = async (paymentData) => {
  // Update daily revenue cache
  await updateDailyRevenueCache(paymentData.logged_on, paymentData.total_price);
  
  // Update payment method statistics
  await updatePaymentMethodStats(paymentData.payment_type, paymentData.total_price);
  
  // Update user spending profile
  await updateUserSpendingProfile(paymentData.user_id, paymentData.total_price);
  
  // Trigger real-time dashboard refresh
  await triggerDashboardUpdate('payments', paymentData);
};
```

### Financial Reporting and Analytics

**Comprehensive Payment Reports:**
```javascript
// Generate detailed payment analysis report
const generatePaymentReport = async (reportConfig) => {
  const report = {
    summary: {},
    trends: {},
    userAnalysis: {},
    paymentMethods: {}
  };
  
  // Overall summary statistics
  report.summary = await knex('hntb_bytemark_order_payments')
    .select(
      knex.raw('COUNT(*) as total_transactions'),
      knex.raw('COUNT(DISTINCT user_id) as unique_users'),
      knex.raw('SUM(total_price) as total_revenue'),
      knex.raw('AVG(total_price) as avg_transaction'),
      knex.raw('MIN(logged_on) as first_transaction'),
      knex.raw('MAX(logged_on) as latest_transaction')
    )
    .whereBetween('logged_on', reportConfig.dateRange)
    .first();
  
  // Revenue trends over time
  report.trends = await knex('hntb_bytemark_order_payments')
    .select(knex.raw('DATE(logged_on) as date'))
    .count('* as daily_transactions')
    .sum('total_price as daily_revenue')
    .whereBetween('logged_on', reportConfig.dateRange)
    .groupBy(knex.raw('DATE(logged_on)'))
    .orderBy('date');
  
  // User segmentation analysis
  report.userAnalysis = await knex('hntb_bytemark_order_payments')
    .select('user_id')
    .count('* as transaction_count')
    .sum('total_price as total_spent')
    .whereBetween('logged_on', reportConfig.dateRange)
    .groupBy('user_id')
    .orderBy('total_spent', 'desc');
  
  // Payment method breakdown
  report.paymentMethods = await knex('hntb_bytemark_order_payments')
    .select('payment_type')
    .count('* as usage_count')
    .sum('total_price as method_revenue')
    .avg('total_price as avg_amount')
    .whereBetween('logged_on', reportConfig.dateRange)
    .groupBy('payment_type')
    .orderBy('method_revenue', 'desc');
  
  return report;
};

// Performance and efficiency metrics
const analyzePaymentPerformance = async () => {
  // Payment processing time analysis
  const processingTimes = await knex('hntb_bytemark_order_payments')
    .select(
      knex.raw('payment_type'),
      knex.raw('AVG(TIMESTAMPDIFF(SECOND, created_on, logged_on)) as avg_processing_seconds'),
      knex.raw('MAX(TIMESTAMPDIFF(SECOND, created_on, logged_on)) as max_processing_seconds'),
      knex.raw('COUNT(*) as sample_size')
    )
    .where('logged_on', '>=', knex.raw('DATE_SUB(NOW(), INTERVAL 30 DAY)'))
    .groupBy('payment_type')
    .orderBy('avg_processing_seconds');
  
  // Error rate analysis (requires additional error tracking)
  const errorRates = await analyzePaymentErrors();
  
  return { processingTimes, errorRates };
};
```

### Error Handling and Data Validation

**Comprehensive Payment Validation:**
```javascript
// Validate payment transaction data
const validatePaymentData = (data) => {
  const errors = [];
  
  if (!data.payment_id || data.payment_id <= 0) {
    errors.push('Valid payment_id required');
  }
  
  if (!data.user_id || data.user_id.length > 256) {
    errors.push('Valid user_id required (max 256 characters)');
  }
  
  if (!data.order_id) {
    errors.push('Order ID is required');
  }
  
  if (!data.payment_type || data.payment_type.length > 32) {
    errors.push('Valid payment_type required (max 32 characters)');
  }
  
  if (!data.total_price || data.total_price < 0) {
    errors.push('Valid positive total_price required');
  }
  
  if (!data.logged_on || new Date(data.logged_on) > new Date()) {
    errors.push('Valid logged_on timestamp required (cannot be in future)');
  }
  
  if (errors.length > 0) {
    throw new ValidationError(errors.join(', '));
  }
};

// Safe payment insertion with duplicate handling
const insertPaymentSafely = async (data) => {
  validatePaymentData(data);
  
  try {
    const result = await knex('hntb_bytemark_order_payments').insert(data);
    logger.info(`Payment transaction recorded: ${data.payment_id}`);
    return result;
  } catch (error) {
    if (error.code === 'ER_DUP_ENTRY') {
      logger.warn(`Duplicate payment transaction: ${data.payment_id}`);
      return await knex('hntb_bytemark_order_payments')
        .where('payment_id', data.payment_id)
        .first();
    }
    logger.error(`Failed to record payment transaction: ${error.message}`);
    throw error;
  }
};
```

This migration establishes essential infrastructure for comprehensive Bytemark payment tracking and analysis within the HNTB transportation research platform, enabling detailed financial analysis, payment behavior studies, and economic impact assessment of transit system interventions.