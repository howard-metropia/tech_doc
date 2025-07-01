# TSP API InfluxDB Service Documentation

## 🔍 Quick Summary (TL;DR)
The InfluxDB service provides time-series data writing capabilities for metrics collection, analytics, and monitoring using InfluxDB cloud database with configurable organization and bucket settings.

**Keywords:** influxdb | time-series-data | metrics-collection | analytics | monitoring | telemetry | data-points | timestamp-data

**Primary use cases:** Writing application metrics, storing telemetry data, logging time-series events, collecting performance data for analytics dashboards

**Compatibility:** Node.js >= 16.0.0, InfluxDB 2.x, cloud-based time-series database

## ❓ Common Questions Quick Index
- **Q: What data format is supported?** → Point-based data with tags, fields, measurement name, and optional timestamp
- **Q: How are credentials managed?** → Environment variables INFLUXDB_URL and INFLUXDB_TOKEN
- **Q: What's the default bucket?** → Configured via config.database.influx.bucket
- **Q: Are default tags applied?** → Yes, datacenter, project, and stage tags are automatically added
- **Q: What field types are supported?** → Currently only string fields via stringField() method
- **Q: Is timestamp required?** → No, defaults to current time if not provided

## 📋 Functionality Overview

**Non-technical explanation:** 
Think of this as a **data logger for time-stamped information**. When the app wants to track when things happen (like how many users logged in at 3 PM, or how long a trip took), this service writes that information to a specialized database that's really good at storing data with timestamps and finding patterns over time.

**Technical explanation:** 
A time-series database integration service that writes structured data points to InfluxDB. Each data point consists of a measurement name, tags for metadata, fields for actual values, and timestamps. Includes automatic default tagging for environment identification and promise-based asynchronous writing with error handling.

**Business value explanation:**
Essential for operational monitoring, performance analytics, and business intelligence. Enables real-time monitoring dashboards, trend analysis, capacity planning, and data-driven decision making. Critical for understanding user behavior patterns, system performance, and business metrics over time.

## 🔧 Technical Specifications

- **File:** `allrepo/connectsmart/tsp-api/src/services/influxDb.js`
- **Language:** JavaScript (ES2020)
- **Framework:** InfluxDB 2.x JavaScript client
- **Type:** Time-series Database Integration Service
- **File Size:** ~1.4 KB
- **Complexity Score:** ⭐ (Low - Simple write-only interface)

**Dependencies:**
- `@influxdata/influxdb-client`: InfluxDB JavaScript client library (**Critical**)
- `config`: Configuration management for database settings (**High**)

**Environment Variables:**
- `INFLUXDB_URL`: InfluxDB instance URL (**Critical**)
- `INFLUXDB_TOKEN`: Authentication token for InfluxDB access (**Critical**)

## 📝 Detailed Code Analysis

### Database Connection Setup

**Configuration Source:**
```javascript
const config = require('config').database.influx;

const db = new InfluxDB({
  url: process.env.INFLUXDB_URL,
  token: process.env.INFLUXDB_TOKEN,
});
```

**Default Tags Applied:**
- `datacenter`: Environment datacenter identifier
- `project`: Project name identifier  
- `stage`: Deployment stage (dev/staging/prod)

### write Function

**Purpose:** Writes time-series data points to InfluxDB

**Parameters:**
- `data`: Object containing:
  - `measurement`: String - InfluxDB measurement name (table equivalent)
  - `tags`: Object - Key-value pairs for metadata indexing
  - `fields`: Object - Key-value pairs for actual data values
  - `timestamp`: Date/String (optional) - Data point timestamp

**Returns:** Promise - Resolves on successful write, rejects on error

**Implementation Flow:**
1. **Parameter Extraction:** Destructures measurement, tags, fields, timestamp
2. **Write API Setup:** Configures InfluxDB write API with organization and bucket
3. **Default Tags:** Applies datacenter, project, stage tags automatically
4. **Timestamp Handling:** Uses provided timestamp or current time
5. **Point Construction:** Creates InfluxDB Point with measurement name
6. **Tag Application:** Adds all provided tags to the point
7. **Field Application:** Adds all provided fields as string fields
8. **Validation:** Ensures either tags or fields exist before writing
9. **Write Operation:** Writes point and flushes to database

**Implementation Detail:**
```javascript
write: async (data) => {
  return new Promise((resolve, reject) => {
    const { tags, fields, measurement, timestamp } = data;
    
    if (measurement) {
      const write = db
        .getWriteApi(config.org, config.bucket, 'ns')
        .useDefaultTags({
          datacenter: config.datacenter,
          project: config.project,
          stage: config.stage,
        });
        
      const writeTime = timestamp ? new Date(timestamp) : new Date();
      const influxData = new Point(measurement).timestamp(writeTime);
      
      // Apply tags and fields
      if (tags) {
        Object.keys(tags).forEach(key => influxData.tag(key, tags[key]));
      }
      if (fields) {
        Object.keys(fields).forEach(key => influxData.stringField(key, fields[key]));
      }
      
      // Write only if data exists
      if (Object.keys(tags).length || Object.keys(fields).length) {
        write.writePoint(influxData);
        write.flush()
          .then(() => resolve())
          .catch(err => reject(err));
      }
    }
  });
}
```

## 🚀 Usage Methods

### Basic Metrics Collection
```javascript
const influxDb = require('@app/src/services/influxDb');

async function logUserLogin(userId, loginMethod, ipAddress) {
  try {
    await influxDb.write({
      measurement: 'user_login',
      tags: {
        user_id: userId.toString(),
        login_method: loginMethod,
        ip_address: ipAddress
      },
      fields: {
        event: 'login_success',
        user_agent: 'mobile_app_v2.1',
        session_start: new Date().toISOString()
      },
      timestamp: new Date()
    });
    
    console.log('User login logged to InfluxDB');
  } catch (error) {
    console.error('Failed to log user login:', error);
  }
}
```

### Trip Analytics Tracking
```javascript
async function logTripCompletion(tripData) {
  const influxDb = require('@app/src/services/influxDb');
  
  try {
    await influxDb.write({
      measurement: 'trip_completion',
      tags: {
        trip_id: tripData.id.toString(),
        user_id: tripData.userId.toString(),
        travel_mode: tripData.travelMode,
        city: tripData.city,
        hour_of_day: new Date(tripData.endTime).getHours().toString()
      },
      fields: {
        distance: tripData.distance.toString(),
        duration: tripData.duration.toString(),
        cost: tripData.cost ? tripData.cost.toString() : '0',
        origin: tripData.origin,
        destination: tripData.destination,
        status: 'completed'
      },
      timestamp: tripData.endTime
    });
    
    console.log(`Trip ${tripData.id} logged to InfluxDB analytics`);
  } catch (error) {
    console.error('Failed to log trip completion:', error);
    // Don't fail the trip completion if logging fails
  }
}
```

### Performance Monitoring Service
```javascript
class PerformanceMonitor {
  constructor() {
    this.influxDb = require('@app/src/services/influxDb');
  }

  async logApiResponse(requestData, responseData) {
    try {
      await this.influxDb.write({
        measurement: 'api_response',
        tags: {
          endpoint: requestData.path,
          method: requestData.method,
          status_code: responseData.statusCode.toString(),
          user_id: requestData.headers.userid || 'anonymous'
        },
        fields: {
          response_time: responseData.responseTime.toString(),
          request_size: requestData.size ? requestData.size.toString() : '0',
          response_size: responseData.size ? responseData.size.toString() : '0',
          error_message: responseData.error || '',
          ip_address: requestData.ip
        }
      });
    } catch (error) {
      console.error('Failed to log API response metrics:', error);
    }
  }

  async logDatabaseQuery(queryData) {
    try {
      await this.influxDb.write({
        measurement: 'database_query',
        tags: {
          query_type: queryData.type,
          table_name: queryData.table,
          operation: queryData.operation
        },
        fields: {
          execution_time: queryData.executionTime.toString(),
          rows_affected: queryData.rowsAffected ? queryData.rowsAffected.toString() : '0',
          query_hash: queryData.queryHash || '',
          error: queryData.error || ''
        }
      });
    } catch (error) {
      console.error('Failed to log database query metrics:', error);
    }
  }

  async logSystemHealth() {
    const os = require('os');
    const process = require('process');
    
    try {
      await this.influxDb.write({
        measurement: 'system_health',
        tags: {
          hostname: os.hostname(),
          platform: os.platform(),
          node_version: process.version
        },
        fields: {
          memory_usage: process.memoryUsage().heapUsed.toString(),
          memory_total: os.totalmem().toString(),
          cpu_usage: process.cpuUsage().user.toString(),
          load_average: os.loadavg()[0].toString(),
          uptime: process.uptime().toString()
        }
      });
    } catch (error) {
      console.error('Failed to log system health metrics:', error);
    }
  }

  startPeriodicHealthChecks(intervalMs = 60000) {
    setInterval(() => {
      this.logSystemHealth();
    }, intervalMs);
    
    console.log(`System health monitoring started (${intervalMs}ms interval)`);
  }
}
```

### Business Metrics Dashboard
```javascript
class BusinessMetricsCollector {
  constructor() {
    this.influxDb = require('@app/src/services/influxDb');
  }

  async trackUserEngagement(userId, action, details = {}) {
    try {
      await this.influxDb.write({
        measurement: 'user_engagement',
        tags: {
          user_id: userId.toString(),
          action: action,
          platform: details.platform || 'unknown',
          app_version: details.appVersion || 'unknown'
        },
        fields: {
          session_duration: details.sessionDuration ? details.sessionDuration.toString() : '0',
          screen_name: details.screenName || '',
          feature_used: details.feature || '',
          interaction_count: details.interactions ? details.interactions.toString() : '1'
        }
      });
    } catch (error) {
      console.error('Failed to track user engagement:', error);
    }
  }

  async trackRevenueEvent(eventData) {
    try {
      await this.influxDb.write({
        measurement: 'revenue_event',
        tags: {
          user_id: eventData.userId.toString(),
          event_type: eventData.type,
          payment_method: eventData.paymentMethod,
          currency: eventData.currency || 'USD'
        },
        fields: {
          amount: eventData.amount.toString(),
          transaction_id: eventData.transactionId,
          service_fee: eventData.serviceFee ? eventData.serviceFee.toString() : '0',
          promotion_code: eventData.promotionCode || '',
          merchant: eventData.merchant || ''
        }
      });
    } catch (error) {
      console.error('Failed to track revenue event:', error);
    }
  }

  async trackTripDemand(origin, destination, requestTime) {
    try {
      await this.influxDb.write({
        measurement: 'trip_demand',
        tags: {
          origin_zone: this.getZoneFromCoordinates(origin),
          destination_zone: this.getZoneFromCoordinates(destination),
          hour_of_day: new Date(requestTime).getHours().toString(),
          day_of_week: new Date(requestTime).getDay().toString()
        },
        fields: {
          origin_lat: origin.latitude.toString(),
          origin_lng: origin.longitude.toString(),
          destination_lat: destination.latitude.toString(),
          destination_lng: destination.longitude.toString(),
          request_timestamp: requestTime.toISOString()
        },
        timestamp: requestTime
      });
    } catch (error) {
      console.error('Failed to track trip demand:', error);
    }
  }

  getZoneFromCoordinates(coordinates) {
    // Simplified zone mapping - in practice, this would be more sophisticated
    const lat = coordinates.latitude;
    const lng = coordinates.longitude;
    
    if (lat >= 29.7 && lat <= 29.8 && lng >= -95.4 && lng <= -95.3) {
      return 'downtown_houston';
    } else if (lat >= 29.8 && lat <= 29.9 && lng >= -95.5 && lng <= -95.4) {
      return 'northwest_houston';
    } else {
      return 'other_houston';
    }
  }

  async generateDailyReport() {
    const today = new Date();
    const yesterday = new Date(today.getTime() - 24 * 60 * 60 * 1000);
    
    console.log(`Daily metrics report for ${yesterday.toDateString()}`);
    
    // In a real implementation, this would query InfluxDB for aggregated data
    // For now, we'll just log that we're tracking the metrics
    
    try {
      await this.influxDb.write({
        measurement: 'daily_report_generated',
        tags: {
          report_type: 'daily_summary',
          date: yesterday.toISOString().split('T')[0]
        },
        fields: {
          report_status: 'completed',
          generation_time: new Date().toISOString(),
          data_quality: 'good'
        }
      });
    } catch (error) {
      console.error('Failed to log daily report generation:', error);
    }
  }
}
```

### Event-Driven Analytics
```javascript
class EventAnalyticsCollector {
  constructor() {
    this.influxDb = require('@app/src/services/influxDb');
    this.eventQueue = [];
    this.batchSize = 10;
    this.flushInterval = 5000; // 5 seconds
    
    this.startBatchProcessor();
  }

  async queueEvent(eventData) {
    this.eventQueue.push({
      ...eventData,
      queuedAt: new Date()
    });

    // Flush immediately if batch size reached
    if (this.eventQueue.length >= this.batchSize) {
      await this.flushEvents();
    }
  }

  async flushEvents() {
    if (this.eventQueue.length === 0) return;

    const eventsToProcess = this.eventQueue.splice(0);
    
    console.log(`Flushing ${eventsToProcess.length} events to InfluxDB`);

    // Process events in parallel
    const writePromises = eventsToProcess.map(event => 
      this.influxDb.write(event).catch(error => {
        console.error('Failed to write event:', error);
        // Re-queue failed events for retry
        this.eventQueue.push(event);
      })
    );

    await Promise.allSettled(writePromises);
  }

  startBatchProcessor() {
    setInterval(() => {
      this.flushEvents();
    }, this.flushInterval);
    
    console.log('Batch event processor started');
  }

  async trackFeatureUsage(userId, featureName, context = {}) {
    await this.queueEvent({
      measurement: 'feature_usage',
      tags: {
        user_id: userId.toString(),
        feature: featureName,
        context: context.screen || 'unknown'
      },
      fields: {
        usage_count: '1',
        session_id: context.sessionId || '',
        previous_feature: context.previousFeature || '',
        time_spent: context.timeSpent ? context.timeSpent.toString() : '0'
      }
    });
  }

  async trackError(errorData) {
    await this.queueEvent({
      measurement: 'application_error',
      tags: {
        error_type: errorData.type,
        severity: errorData.severity || 'error',
        component: errorData.component || 'unknown'
      },
      fields: {
        error_message: errorData.message,
        stack_trace: errorData.stackTrace || '',
        user_id: errorData.userId ? errorData.userId.toString() : '',
        request_id: errorData.requestId || '',
        context: JSON.stringify(errorData.context || {})
      }
    });
  }

  async trackCustomEvent(eventName, eventData) {
    await this.queueEvent({
      measurement: 'custom_event',
      tags: {
        event_name: eventName,
        category: eventData.category || 'general',
        source: eventData.source || 'api'
      },
      fields: {
        data: JSON.stringify(eventData),
        value: eventData.value ? eventData.value.toString() : '',
        user_id: eventData.userId ? eventData.userId.toString() : ''
      }
    });
  }
}
```

### Configuration and Testing
```javascript
class InfluxDbManager {
  constructor() {
    this.influxDb = require('@app/src/services/influxDb');
  }

  async testConnection() {
    try {
      await this.influxDb.write({
        measurement: 'connection_test',
        tags: {
          test_type: 'connectivity',
          timestamp: Date.now().toString()
        },
        fields: {
          status: 'success',
          message: 'Connection test successful'
        }
      });
      
      console.log('InfluxDB connection test successful');
      return { success: true };
    } catch (error) {
      console.error('InfluxDB connection test failed:', error);
      return { success: false, error: error.message };
    }
  }

  async writeTestData(sampleSize = 100) {
    const startTime = Date.now();
    const errors = [];
    
    for (let i = 0; i < sampleSize; i++) {
      try {
        await this.influxDb.write({
          measurement: 'test_data',
          tags: {
            test_run: startTime.toString(),
            data_point: i.toString(),
            batch: Math.floor(i / 10).toString()
          },
          fields: {
            value: (Math.random() * 100).toString(),
            category: ['A', 'B', 'C'][i % 3],
            timestamp: new Date().toISOString()
          }
        });
      } catch (error) {
        errors.push({ index: i, error: error.message });
      }
    }
    
    const endTime = Date.now();
    const duration = endTime - startTime;
    
    return {
      sampleSize,
      duration,
      errors: errors.length,
      successRate: ((sampleSize - errors.length) / sampleSize * 100).toFixed(2),
      errorsDetails: errors
    };
  }

  validateConfiguration() {
    const requiredEnvVars = ['INFLUXDB_URL', 'INFLUXDB_TOKEN'];
    const missingVars = requiredEnvVars.filter(varName => !process.env[varName]);
    
    if (missingVars.length > 0) {
      return {
        valid: false,
        errors: [`Missing environment variables: ${missingVars.join(', ')}`]
      };
    }

    const config = require('config').database.influx;
    const requiredConfigKeys = ['org', 'bucket', 'datacenter', 'project', 'stage'];
    const missingConfig = requiredConfigKeys.filter(key => !config[key]);
    
    if (missingConfig.length > 0) {
      return {
        valid: false,
        errors: [`Missing configuration keys: ${missingConfig.join(', ')}`]
      };
    }

    return { valid: true, errors: [] };
  }

  async runDiagnostics() {
    console.log('Running InfluxDB diagnostics...');
    
    const results = {
      configuration: this.validateConfiguration(),
      connection: await this.testConnection(),
      performance: null
    };

    if (results.connection.success) {
      results.performance = await this.writeTestData(50);
    }

    return results;
  }
}
```

## 📊 Output Examples

### Successful Write Operation
```javascript
// Input data
const tripData = {
  measurement: 'trip_completion',
  tags: {
    trip_id: '12345',
    user_id: '67890',
    travel_mode: 'driving'
  },
  fields: {
    distance: '15420',
    duration: '1800',
    cost: '12.50'
  }
};

// Result: Promise resolves with no return value
// Data written to InfluxDB with automatic default tags
```

### Performance Test Results
```json
{
  "sampleSize": 100,
  "duration": 2340,
  "errors": 2,
  "successRate": "98.00",
  "errorsDetails": [
    {
      "index": 45,
      "error": "Network timeout"
    },
    {
      "index": 78,
      "error": "Invalid field value"
    }
  ]
}
```

### Configuration Validation
```json
{
  "valid": true,
  "errors": [],
  "config": {
    "url": "https://us-east-1-1.aws.cloud2.influxdata.com",
    "org": "metropia",
    "bucket": "tsp-metrics",
    "datacenter": "us-east-1",
    "project": "tsp-api",
    "stage": "production"
  }
}
```

### Diagnostics Report
```json
{
  "configuration": {
    "valid": true,
    "errors": []
  },
  "connection": {
    "success": true
  },
  "performance": {
    "sampleSize": 50,
    "duration": 1240,
    "errors": 0,
    "successRate": "100.00"
  }
}
```

## ⚠️ Important Notes

### Configuration Requirements
```javascript
// Environment Variables (Required)
{
  "INFLUXDB_URL": "https://your-influx-instance.com",
  "INFLUXDB_TOKEN": "your-access-token"
}

// Config Object Structure
{
  "database": {
    "influx": {
      "org": "organization-name",
      "bucket": "bucket-name", 
      "datacenter": "us-east-1",
      "project": "project-name",
      "stage": "production"
    }
  }
}
```

### Data Type Limitations
- **Field Types:** Currently only supports string fields via `stringField()`
- **Tag Values:** All tag values are converted to strings
- **Timestamps:** Accepts Date objects or ISO strings
- **Precision:** Nanosecond precision configured ('ns')

### Performance Considerations
- **Single Write:** Each call writes one data point
- **Batch Writing:** Consider batching for high-volume scenarios
- **Async Operations:** All writes are asynchronous with promises
- **Error Handling:** Write failures should be caught and handled gracefully

### Default Tags Applied
Every data point automatically includes:
```javascript
{
  datacenter: config.datacenter,
  project: config.project,
  stage: config.stage
}
```

### Validation Logic
- **Measurement Required:** Function returns early if no measurement provided
- **Data Validation:** Checks for existence of tags OR fields before writing
- **Empty Data:** Skips write if both tags and fields are empty
- **Chinese Comments:** Code includes comments in Chinese for team clarity

### Error Scenarios
- **Network Issues:** Connection timeouts or network failures
- **Authentication:** Invalid token or expired credentials
- **Schema Errors:** Invalid tag/field names or values
- **Quota Limits:** InfluxDB usage quota exceeded
- **Configuration Missing:** Environment variables or config not set

### Security Considerations
- **Token Security:** Store INFLUXDB_TOKEN securely
- **Data Sensitivity:** Be mindful of PII in tags/fields
- **Network Security:** Use HTTPS connections
- **Access Control:** Limit token permissions to write-only

### Monitoring and Alerting
- **Write Success Rate:** Monitor for failed writes
- **Response Times:** Track write operation latency
- **Data Quality:** Validate data completeness
- **Quota Usage:** Monitor InfluxDB usage limits

### Best Practices
- **Tag vs Field:** Use tags for metadata, fields for measured values
- **Tag Cardinality:** Keep tag value combinations reasonable
- **Timestamp Precision:** Use appropriate precision for use case
- **Batch Operations:** Implement batching for high-volume scenarios

## 🔗 Related File Links

- **Configuration:** `config/default.js` - InfluxDB configuration settings
- **Analytics Controllers:** Controllers that generate metrics data
- **Monitoring Services:** Services that consume InfluxDB data for dashboards
- **Performance Middleware:** Middleware that tracks API performance metrics

---
*This service provides essential time-series data collection capabilities for analytics, monitoring, and business intelligence in the TSP platform.*