# QuickSight ETL Service

## Quick Summary

The QuickSight ETL service is a high-performance data extraction, transformation, and loading system designed to synchronize data from the production portal database to a dedicated analytics dataset database for Amazon QuickSight reporting. This service handles incremental data replication across multiple critical tables while performing timezone conversions and batch processing optimizations to ensure efficient data pipeline operations.

**Key Features:**
- Incremental data synchronization with automatic change detection
- Batch processing for optimal performance and resource utilization
- Timezone conversion from UTC to Central Time for business analytics
- Multi-table replication with consistent data integrity
- Automated error handling and logging for monitoring
- Configurable batch sizes for scalable processing

## Technical Analysis

### Architecture Overview

The service implements a pull-based ETL pattern that identifies new records in the source database and replicates them to the target analytics database. It uses offset-based pagination and incremental ID tracking to ensure complete data coverage while minimizing processing overhead.

### Core Processing Pipeline

```javascript
const quickSightEtl = async () => {
  const tables = [
    'points_transaction', 'token_transaction', 'redeem_transaction',
    'bytemark_order_payments', 'bytemark_order_items', 'bytemark_pass',
    'trip', 'user_rating', 'referral_history', 'campaign',
    'cm_activity_location', 'campaign_promo_code', 'group_member',
    'telework', 'app_data', 'auth_user', 'user_label', 'auth_user_label'
  ];
  
  for (const table of tables) {
    await processTableReplication(table);
  }
};
```

### Incremental Data Detection

The service uses a sophisticated incremental processing mechanism:

```javascript
// Fetch the latest data from dataset to determine starting point
const datasetLatest = await datasetKnex(table)
  .orderBy('id', 'desc')
  .limit(1)
  .select('id');
const datasetLatestId = datasetLatest.length > 0 ? datasetLatest[0].id : 0;

// Process only new records beyond the latest ID
const portalData = await portalKnex(table)
  .where('id', '>', datasetLatestId)
  .offset(offset)
  .limit(BATCH_SIZE);
```

### Data Transformation Engine

The service performs comprehensive data transformation during the ETL process:

```javascript
const writeData = portalData.map((item) => {
  const dateColumns = [
    'created_on', 'modified_on', 'time_used', 'issued_on', 'expired_on',
    'started_on', 'ended_on', 'estimated_arrival_on', 'created_at', 'updated_at',
    'departure_time', 'arrival_time', 'departure_time_orig', 'job_time',
    'start_date', 'end_date'
  ];
  
  // Convert UTC timestamps to Central Time for business analytics
  dateColumns.forEach((col) => {
    if (item[col]) {
      item[col] = moment
        .utc(item[col])
        .tz('US/Central')
        .format('YYYY-MM-DD HH:mm:ss');
    }
  });
  
  return item;
});
```

### Batch Processing Optimization

The service implements efficient batch processing to handle large datasets:

```javascript
const BATCH_SIZE = 1000;

while (true) {
  const portalData = await portalKnex(table)
    .where('id', '>', datasetLatestId)
    .offset(offset)
    .limit(BATCH_SIZE);
  
  if (writeData.length) {
    await datasetKnex(table).insert(writeData);
  }
  
  if (portalData.length === 0 || portalData.length < BATCH_SIZE) {
    break; // End of data reached
  }
  
  offset += BATCH_SIZE;
}
```

### Error Handling and Monitoring

The service includes comprehensive logging for monitoring and debugging:

```javascript
logger.info(`Inserting ${table}, ${offset + writeData.length} rows`);
logger.info(`Finished ${table}, ${offset + portalData.length} rows`);
```

## Usage/Integration

### Primary Execution Pattern

#### 1. Scheduled ETL Processing
```javascript
const { quickSightEtl } = require('@app/src/services/quick-sight-etl');

// Execute complete ETL pipeline
await quickSightEtl();
console.log('QuickSight ETL process completed successfully');
```

#### 2. Individual Table Processing
```javascript
// Process specific table for targeted updates
async function processSpecificTable(tableName) {
  const tables = [tableName];
  
  for (const table of tables) {
    let offset = 0;
    
    const datasetLatest = await datasetKnex(table)
      .orderBy('id', 'desc')
      .limit(1)
      .select('id');
    const datasetLatestId = datasetLatest.length > 0 ? datasetLatest[0].id : 0;
    
    while (true) {
      const portalData = await portalKnex(table)
        .where('id', '>', datasetLatestId)
        .offset(offset)
        .limit(1000);
      
      if (portalData.length === 0) break;
      
      // Transform and insert data
      await datasetKnex(table).insert(transformData(portalData));
      offset += 1000;
    }
  }
}
```

#### 3. Real-time Monitoring Integration
```javascript
// Enhanced ETL with monitoring and alerting
async function monitoredETL() {
  const startTime = Date.now();
  const results = {};
  
  try {
    await quickSightEtl();
    
    results.status = 'success';
    results.duration = Date.now() - startTime;
    results.processedTables = 18; // Number of tables in the pipeline
    
  } catch (error) {
    results.status = 'error';
    results.error = error.message;
    results.duration = Date.now() - startTime;
    
    // Send alert notification
    await sendETLAlert(results);
  }
  
  return results;
}
```

### Configuration and Scheduling

#### 1. Cron Job Integration
```bash
# Execute ETL every hour
0 * * * * /usr/local/bin/node /app/scripts/run-quicksight-etl.js

# Execute ETL every day at 2 AM
0 2 * * * /usr/local/bin/node /app/scripts/run-quicksight-etl.js
```

#### 2. Custom Batch Size Configuration
```javascript
// Configurable batch processing
const BATCH_CONFIGS = {
  small_tables: 2000,    // For tables with < 100K records
  medium_tables: 1000,   // For tables with 100K-1M records  
  large_tables: 500      // For tables with > 1M records
};

async function adaptiveBatchETL(table) {
  const recordCount = await portalKnex(table).count('id as count').first();
  const batchSize = getBatchSize(recordCount.count);
  
  // Use adaptive batch size for processing
  const portalData = await portalKnex(table)
    .where('id', '>', datasetLatestId)
    .offset(offset)
    .limit(batchSize);
}
```

#### 3. Data Quality Validation
```javascript
// Post-ETL data validation
async function validateETLResults() {
  const validationResults = {};
  
  const tables = ['points_transaction', 'trip', 'auth_user'];
  
  for (const table of tables) {
    const portalCount = await portalKnex(table).count('id as count').first();
    const datasetCount = await datasetKnex(table).count('id as count').first();
    
    validationResults[table] = {
      portalRecords: portalCount.count,
      datasetRecords: datasetCount.count,
      syncPercentage: (datasetCount.count / portalCount.count) * 100
    };
  }
  
  return validationResults;
}
```

## Dependencies

### Database Connectivity
- **@maas/core/mysql('portal')**: Source database connection for production data
- **@maas/core/mysql('dataset')**: Target database connection for analytics data
- **Knex.js**: SQL query builder and connection management

### Utility Libraries
- **moment-timezone**: Timezone conversion and date manipulation
- **@maas/core/log**: Centralized logging for monitoring and debugging

### Infrastructure Dependencies
- **MySQL Database Clusters**: Source portal and target dataset databases
- **Network Connectivity**: Reliable connection between database instances
- **AWS QuickSight**: Target analytics platform for the ETL data

### Configuration Dependencies
- **Database Credentials**: Secure access to both portal and dataset databases
- **Timezone Configuration**: Central Time conversion settings
- **Batch Size Parameters**: Performance tuning configurations

## Code Examples

### Complete ETL Pipeline with Error Recovery

```javascript
// Enhanced ETL service with comprehensive error handling
class QuickSightETLManager {
  constructor() {
    this.BATCH_SIZE = 1000;
    this.MAX_RETRIES = 3;
    this.tables = [
      'points_transaction', 'token_transaction', 'redeem_transaction',
      'bytemark_order_payments', 'bytemark_order_items', 'bytemark_pass',
      'trip', 'user_rating', 'referral_history', 'campaign',
      'cm_activity_location', 'campaign_promo_code', 'group_member',
      'telework', 'app_data', 'auth_user', 'user_label', 'auth_user_label'
    ];
  }
  
  async executeETL() {
    const results = {
      startTime: new Date(),
      tables: {},
      summary: { success: 0, failed: 0, totalRecords: 0 }
    };
    
    for (const table of this.tables) {
      try {
        const tableResult = await this.processTableWithRetry(table);
        results.tables[table] = tableResult;
        results.summary.success++;
        results.summary.totalRecords += tableResult.recordsProcessed;
        
      } catch (error) {
        logger.error(`Failed to process table ${table}:`, error);
        results.tables[table] = { error: error.message, recordsProcessed: 0 };
        results.summary.failed++;
      }
    }
    
    results.endTime = new Date();
    results.duration = results.endTime - results.startTime;
    
    return results;
  }
  
  async processTableWithRetry(table, retryCount = 0) {
    try {
      return await this.processTable(table);
    } catch (error) {
      if (retryCount < this.MAX_RETRIES) {
        logger.warn(`Retrying table ${table}, attempt ${retryCount + 1}`);
        await this.delay(1000 * (retryCount + 1)); // Exponential backoff
        return await this.processTableWithRetry(table, retryCount + 1);
      }
      throw error;
    }
  }
  
  async processTable(table) {
    let offset = 0;
    let totalRecords = 0;
    
    // Get latest ID from dataset
    const datasetLatest = await datasetKnex(table)
      .orderBy('id', 'desc')
      .limit(1)
      .select('id');
    const datasetLatestId = datasetLatest.length > 0 ? datasetLatest[0].id : 0;
    
    logger.info(`Processing table ${table} from ID ${datasetLatestId}`);
    
    while (true) {
      const portalData = await portalKnex(table)
        .where('id', '>', datasetLatestId)
        .offset(offset)
        .limit(this.BATCH_SIZE);
      
      if (portalData.length === 0) {
        break;
      }
      
      // Transform data
      const writeData = this.transformData(portalData);
      
      // Insert batch
      if (writeData.length > 0) {
        await datasetKnex(table).insert(writeData);
        totalRecords += writeData.length;
        
        logger.info(`${table}: Inserted batch ${offset}-${offset + writeData.length}`);
      }
      
      if (portalData.length < this.BATCH_SIZE) {
        break; // End of data
      }
      
      offset += this.BATCH_SIZE;
    }
    
    logger.info(`Completed table ${table}: ${totalRecords} records processed`);
    
    return {
      recordsProcessed: totalRecords,
      startId: datasetLatestId,
      batchesProcessed: Math.ceil(totalRecords / this.BATCH_SIZE)
    };
  }
  
  transformData(data) {
    const dateColumns = [
      'created_on', 'modified_on', 'time_used', 'issued_on', 'expired_on',
      'started_on', 'ended_on', 'estimated_arrival_on', 'created_at', 'updated_at',
      'departure_time', 'arrival_time', 'departure_time_orig', 'job_time',
      'start_date', 'end_date'
    ];
    
    return data.map((item) => {
      dateColumns.forEach((col) => {
        if (item[col]) {
          item[col] = moment
            .utc(item[col])
            .tz('US/Central')
            .format('YYYY-MM-DD HH:mm:ss');
        }
      });
      return item;
    });
  }
  
  delay(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
  }
}
```

### Performance Monitoring and Optimization

```javascript
// Advanced ETL performance monitoring
class ETLPerformanceMonitor {
  constructor() {
    this.metrics = {
      tableStats: {},
      overallStats: {}
    };
  }
  
  async analyzeETLPerformance() {
    const startTime = Date.now();
    
    // Analyze each table's characteristics
    const tables = [
      'points_transaction', 'trip', 'auth_user', 'telework'
    ];
    
    for (const table of tables) {
      this.metrics.tableStats[table] = await this.analyzeTable(table);
    }
    
    // Generate optimization recommendations
    const recommendations = this.generateOptimizationRecommendations();
    
    this.metrics.overallStats = {
      analysisTime: Date.now() - startTime,
      totalTables: tables.length,
      recommendations
    };
    
    return this.metrics;
  }
  
  async analyzeTable(table) {
    const portalStats = await portalKnex(table)
      .select(
        knex.raw('COUNT(*) as total_records'),
        knex.raw('MAX(id) as max_id'),
        knex.raw('MIN(id) as min_id'),
        knex.raw('AVG(LENGTH(JSON_OBJECT(*))) as avg_row_size')
      )
      .first();
    
    const datasetStats = await datasetKnex(table)
      .select(
        knex.raw('COUNT(*) as total_records'),
        knex.raw('MAX(id) as max_id')
      )
      .first();
    
    const syncLag = portalStats.max_id - datasetStats.max_id;
    const syncPercentage = (datasetStats.total_records / portalStats.total_records) * 100;
    
    return {
      portal: portalStats,
      dataset: datasetStats,
      syncLag,
      syncPercentage,
      recommendedBatchSize: this.calculateOptimalBatchSize(portalStats)
    };
  }
  
  calculateOptimalBatchSize(stats) {
    const avgRowSize = stats.avg_row_size || 1000;
    const totalRecords = stats.total_records;
    
    // Optimize batch size based on record size and volume
    if (avgRowSize > 5000 || totalRecords > 1000000) {
      return 500; // Large records or high volume
    } else if (avgRowSize > 2000 || totalRecords > 100000) {
      return 1000; // Medium records or volume
    } else {
      return 2000; // Small records or volume
    }
  }
  
  generateOptimizationRecommendations() {
    const recommendations = [];
    
    Object.entries(this.metrics.tableStats).forEach(([table, stats]) => {
      if (stats.syncPercentage < 95) {
        recommendations.push(`Table ${table} sync is ${stats.syncPercentage.toFixed(1)}% - investigate sync issues`);
      }
      
      if (stats.syncLag > 10000) {
        recommendations.push(`Table ${table} has high sync lag: ${stats.syncLag} records behind`);
      }
      
      if (stats.recommendedBatchSize !== 1000) {
        recommendations.push(`Table ${table} should use batch size ${stats.recommendedBatchSize} instead of default 1000`);
      }
    });
    
    return recommendations;
  }
}
```

### Data Quality Validation System

```javascript
// Comprehensive data quality validation for ETL results
class ETLDataQualityValidator {
  constructor() {
    this.validationRules = {
      'points_transaction': {
        requiredFields: ['user_id', 'points', 'created_on'],
        numericFields: ['points', 'user_id'],
        dateFields: ['created_on']
      },
      'trip': {
        requiredFields: ['user_id', 'started_on', 'distance'],
        numericFields: ['distance', 'user_id'],
        dateFields: ['started_on', 'ended_on']
      },
      'auth_user': {
        requiredFields: ['id', 'email', 'created_on'],
        dateFields: ['created_on', 'last_login']
      }
    };
  }
  
  async validateETLResults() {
    const validationResults = {
      timestamp: new Date(),
      tables: {},
      overallScore: 0
    };
    
    for (const [table, rules] of Object.entries(this.validationRules)) {
      validationResults.tables[table] = await this.validateTable(table, rules);
    }
    
    // Calculate overall quality score
    const scores = Object.values(validationResults.tables).map(t => t.qualityScore);
    validationResults.overallScore = scores.reduce((a, b) => a + b, 0) / scores.length;
    
    return validationResults;
  }
  
  async validateTable(table, rules) {
    const validation = {
      table,
      issues: [],
      qualityScore: 100
    };
    
    // Check record count consistency
    const portalCount = await portalKnex(table).count('id as count').first();
    const datasetCount = await datasetKnex(table).count('id as count').first();
    
    const countDiff = portalCount.count - datasetCount.count;
    if (countDiff > 0) {
      validation.issues.push(`Missing ${countDiff} records in dataset`);
      validation.qualityScore -= Math.min(50, (countDiff / portalCount.count) * 100);
    }
    
    // Validate data integrity
    const sampleData = await datasetKnex(table).limit(100);
    
    for (const row of sampleData) {
      // Check required fields
      for (const field of rules.requiredFields || []) {
        if (row[field] === null || row[field] === undefined) {
          validation.issues.push(`Missing required field ${field} in record ${row.id}`);
          validation.qualityScore -= 1;
        }
      }
      
      // Validate numeric fields
      for (const field of rules.numericFields || []) {
        if (row[field] !== null && isNaN(row[field])) {
          validation.issues.push(`Invalid numeric value in field ${field}: ${row[field]}`);
          validation.qualityScore -= 1;
        }
      }
      
      // Validate date fields
      for (const field of rules.dateFields || []) {
        if (row[field] && !moment(row[field]).isValid()) {
          validation.issues.push(`Invalid date in field ${field}: ${row[field]}`);
          validation.qualityScore -= 1;
        }
      }
    }
    
    validation.qualityScore = Math.max(0, validation.qualityScore);
    
    return validation;
  }
}
```

This QuickSight ETL service provides a robust, scalable data pipeline that ensures analytics teams have access to timely, accurate, and properly formatted data for business intelligence and reporting purposes.