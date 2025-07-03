# TSP Job Service - InfluxDB Configuration

## Overview

The `config/database/influx.js` file manages InfluxDB configuration for the TSP Job service's time-series database requirements. InfluxDB is used for storing and analyzing metrics, performance data, service monitoring information, and time-based analytics across the MaaS platform.

## File Information

- **File Path**: `/config/database/influx.js`
- **File Type**: JavaScript Configuration Module
- **Primary Purpose**: InfluxDB connection and configuration management
- **Dependencies**: Environment variables for database credentials and settings

## Configuration Structure

### Primary InfluxDB Configuration
```javascript
module.exports = {
  bucket: process.env.INFLUXDB_BUCKET,
  token: process.env.INFLUXDB_TOKEN,
  url: process.env.INFLUXDB_URL,
  org: process.env.INFLUXDB_ORG,
  // ... additional configurations
};
```

## Configuration Components

### 1. Primary InfluxDB Instance
```javascript
bucket: process.env.INFLUXDB_BUCKET,
token: process.env.INFLUXDB_TOKEN,
url: process.env.INFLUXDB_URL,
org: process.env.INFLUXDB_ORG,
```

**Purpose**: Main InfluxDB instance for general application metrics
- **bucket**: Primary data storage bucket for application metrics
- **token**: Authentication token for API access
- **url**: InfluxDB server endpoint URL
- **org**: Organization identifier for multi-tenant setup

**Use Cases**:
- Application performance metrics
- Job execution statistics
- User activity analytics
- System health monitoring

### 2. UIS InfluxDB Instance
```javascript
uis_bucket: process.env.INFLUX_BUCKET_UIS,
uis_token: process.env.INFLUX_TOKEN,
uis_url: process.env.INFLUX_URL,
uis_org: process.env.INFLUX_ORG,
```

**Purpose**: Dedicated InfluxDB instance for UIS (Urban Intelligence System) data
- **uis_bucket**: Specialized bucket for urban intelligence metrics
- **uis_token**: Separate authentication for UIS-specific data
- **uis_url**: Potentially different InfluxDB instance for UIS
- **uis_org**: Organization scope for UIS data

**Use Cases**:
- Urban mobility pattern analysis
- Traffic flow metrics
- City-wide transportation analytics
- Infrastructure utilization data

### 3. Infrastructure Metadata
```javascript
datacenter: process.env.CLUSTER_DATACENTER,
project: process.env.PROJECT_NAME,
stage: process.env.PROJECT_STAGE,
```

**Purpose**: Infrastructure and deployment context information
- **datacenter**: Physical or cloud datacenter location
- **project**: Project identifier for metric grouping
- **stage**: Deployment environment (dev, staging, production)

**Usage**: These fields are used as tags in InfluxDB measurements for:
- Multi-environment metric separation
- Geographic performance analysis
- Project-based metric organization

### 4. Service Monitoring Configuration
```javascript
serviceMonitor: {
  bucket: process.env.INFLUXDB_SERVICE_MONITOR_BUCKET || 'service-monitoring',
  measurement: process.env.INFLUXDB_SERVICE_MONITOR_MEASUREMENT || 'vendor_latency',
  timeout: process.env.INFLUXDB_SERVICE_MONITOR_TIMEOUT || 2000,
}
```

**Purpose**: Specialized configuration for service monitoring metrics
- **bucket**: Dedicated bucket for service monitoring data
- **measurement**: Measurement name for vendor latency tracking
- **timeout**: Write timeout for monitoring data (milliseconds)

## InfluxDB Usage Patterns

### 1. Performance Metrics Collection
```javascript
const { InfluxDB, Point } = require('@influxdata/influxdb-client');
const config = require('../config/database/influx');

const influxDB = new InfluxDB({
  url: config.url,
  token: config.token
});

const writeAPI = influxDB.getWriteApi(config.org, config.bucket);

// Record job execution metrics
function recordJobMetrics(jobName, duration, success) {
  const point = new Point('job_execution')
    .tag('job_name', jobName)
    .tag('datacenter', config.datacenter)
    .tag('project', config.project)
    .tag('stage', config.stage)
    .floatField('duration_ms', duration)
    .booleanField('success', success)
    .timestamp(new Date());
    
  writeAPI.writePoint(point);
}
```

### 2. Service Monitoring Integration
```javascript
// Monitor vendor service latency
async function monitorVendorLatency(vendorName, operation, latency) {
  const point = new Point(config.serviceMonitor.measurement)
    .tag('vendor', vendorName)
    .tag('operation', operation)
    .tag('datacenter', config.datacenter)
    .floatField('latency_ms', latency)
    .timestamp(new Date());
    
  const writeAPI = influxDB.getWriteApi(
    config.org, 
    config.serviceMonitor.bucket
  );
  
  writeAPI.writePoint(point);
  
  // Ensure data is written within timeout
  await writeAPI.close();
}
```

### 3. UIS Analytics Integration
```javascript
// Record UIS-specific metrics
const uisInfluxDB = new InfluxDB({
  url: config.uis_url,
  token: config.uis_token
});

const uisWriteAPI = uisInfluxDB.getWriteApi(config.uis_org, config.uis_bucket);

function recordUrbanMetrics(zoneId, trafficDensity, transitUsage) {
  const point = new Point('urban_mobility')
    .tag('zone_id', zoneId)
    .tag('city', 'metropolitan_area')
    .floatField('traffic_density', trafficDensity)
    .intField('transit_usage', transitUsage)
    .timestamp(new Date());
    
  uisWriteAPI.writePoint(point);
}
```

## Metric Categories

### 1. Application Performance Metrics
- **job_execution**: Job processing times and success rates
- **api_latency**: HTTP endpoint response times
- **database_queries**: Database operation performance
- **memory_usage**: Application memory consumption
- **cpu_utilization**: Processor usage patterns

### 2. Business Metrics
- **trip_bookings**: Trip reservation statistics
- **user_engagement**: User interaction patterns
- **revenue_tracking**: Financial transaction metrics
- **service_utilization**: Feature usage analytics

### 3. Infrastructure Metrics
- **system_health**: Server and container health
- **network_latency**: Network performance data
- **storage_usage**: Disk and object storage metrics
- **error_rates**: Application and system error frequencies

### 4. Service Monitoring Metrics
- **vendor_latency**: Third-party service response times
- **api_availability**: External service uptime tracking
- **integration_errors**: Failed external service calls
- **cost_tracking**: Usage-based cost monitoring

## Data Retention and Management

### Retention Policies
```javascript
// Example retention policy configuration
const retentionPolicies = {
  'real-time': {
    duration: '1h',
    aggregation: 'none'
  },
  'hourly': {
    duration: '7d',
    aggregation: '1h'
  },
  'daily': {
    duration: '90d',
    aggregation: '1d'
  },
  'monthly': {
    duration: '2y',
    aggregation: '30d'
  }
};
```

### Data Downsampling
```javascript
// Automatic data downsampling for long-term storage
const downsampleTask = `
from(bucket: "${config.bucket}")
  |> range(start: -1h)
  |> aggregateWindow(every: 1m, fn: mean)
  |> to(bucket: "${config.bucket}_hourly")
`;
```

## Security Configuration

### Authentication
- **Token-based Authentication**: Uses InfluxDB tokens for API access
- **Organization Isolation**: Separate organizations for different data types
- **Bucket-level Security**: Granular access control per data bucket

### Network Security
```javascript
// TLS configuration for secure connections
const secureInfluxDB = new InfluxDB({
  url: config.url,
  token: config.token,
  transportOptions: {
    rejectUnauthorized: true,
    ca: fs.readFileSync('path/to/ca-cert.pem'),
    cert: fs.readFileSync('path/to/client-cert.pem'),
    key: fs.readFileSync('path/to/client-key.pem')
  }
});
```

## Performance Optimization

### Batch Writing
```javascript
// Optimize writes with batching
class InfluxBatchWriter {
  constructor() {
    this.points = [];
    this.batchSize = 100;
    this.flushInterval = 5000; // 5 seconds
    this.setupFlushTimer();
  }
  
  addPoint(measurement, tags, fields) {
    const point = new Point(measurement);
    
    Object.entries(tags).forEach(([key, value]) => {
      point.tag(key, value);
    });
    
    Object.entries(fields).forEach(([key, value]) => {
      if (typeof value === 'number') {
        point.floatField(key, value);
      } else if (typeof value === 'boolean') {
        point.booleanField(key, value);
      } else {
        point.stringField(key, value.toString());
      }
    });
    
    this.points.push(point);
    
    if (this.points.length >= this.batchSize) {
      this.flush();
    }
  }
  
  async flush() {
    if (this.points.length === 0) return;
    
    const writeAPI = influxDB.getWriteApi(config.org, config.bucket);
    writeAPI.writePoints(this.points);
    await writeAPI.close();
    
    this.points = [];
  }
}
```

### Query Optimization
```javascript
// Optimized queries for dashboard data
const queryAPI = influxDB.getQueryApi(config.org);

async function getJobMetrics(timeRange = '-1h') {
  const query = `
    from(bucket: "${config.bucket}")
      |> range(start: ${timeRange})
      |> filter(fn: (r) => r._measurement == "job_execution")
      |> group(columns: ["job_name"])
      |> aggregateWindow(every: 1m, fn: mean)
      |> yield(name: "mean")
  `;
  
  const result = [];
  return new Promise((resolve, reject) => {
    queryAPI.queryRows(query, {
      next(row, tableMeta) {
        const record = tableMeta.toObject(row);
        result.push(record);
      },
      error(error) {
        reject(error);
      },
      complete() {
        resolve(result);
      }
    });
  });
}
```

## Monitoring and Alerting

### Health Checks
```javascript
async function checkInfluxDBHealth() {
  try {
    const health = await influxDB.health();
    return {
      status: health.status,
      message: health.message,
      timestamp: new Date().toISOString()
    };
  } catch (error) {
    return {
      status: 'unhealthy',
      error: error.message,
      timestamp: new Date().toISOString()
    };
  }
}
```

### Automated Alerting
```javascript
// Set up alerts for critical metrics
async function setupAlerts() {
  const alerts = [
    {
      name: 'High Job Failure Rate',
      query: `
        from(bucket: "${config.bucket}")
          |> range(start: -5m)
          |> filter(fn: (r) => r._measurement == "job_execution")
          |> filter(fn: (r) => r.success == false)
          |> count()
      `,
      threshold: 10,
      action: 'slack_notification'
    },
    {
      name: 'High Vendor Latency',
      query: `
        from(bucket: "${config.serviceMonitor.bucket}")
          |> range(start: -5m)
          |> filter(fn: (r) => r._measurement == "${config.serviceMonitor.measurement}")
          |> mean()
      `,
      threshold: 5000, // 5 seconds
      action: 'email_alert'
    }
  ];
  
  // Implement alert evaluation logic
  for (const alert of alerts) {
    await evaluateAlert(alert);
  }
}
```

## Integration Examples

### Dashboard Integration
```javascript
// Grafana dashboard queries
const dashboardQueries = {
  jobThroughput: `
    from(bucket: "${config.bucket}")
      |> range(start: -1h)
      |> filter(fn: (r) => r._measurement == "job_execution")
      |> aggregateWindow(every: 1m, fn: count)
  `,
  
  vendorLatency: `
    from(bucket: "${config.serviceMonitor.bucket}")
      |> range(start: -24h)
      |> filter(fn: (r) => r._measurement == "${config.serviceMonitor.measurement}")
      |> group(columns: ["vendor"])
      |> aggregateWindow(every: 1h, fn: mean)
  `
};
```

### Data Export
```javascript
// Export data for analysis
async function exportMetrics(startTime, endTime, measurement) {
  const query = `
    from(bucket: "${config.bucket}")
      |> range(start: ${startTime}, stop: ${endTime})
      |> filter(fn: (r) => r._measurement == "${measurement}")
      |> pivot(rowKey:["_time"], columnKey: ["_field"], valueColumn: "_value")
  `;
  
  const data = await queryAPI.collectRows(query);
  return data;
}
```

This InfluxDB configuration provides a robust foundation for time-series data management in the TSP Job service, supporting comprehensive monitoring, analytics, and performance optimization across the entire MaaS platform.