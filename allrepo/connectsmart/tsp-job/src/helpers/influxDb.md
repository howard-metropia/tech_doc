# InfluxDB Helper

## Overview
**File**: `src/helpers/influxDb.js`  
**Type**: Database Utility  
**Purpose**: Provides interface for writing time-series data to InfluxDB with automatic type detection

## Configuration

### Database Connection
```javascript
const db = new InfluxDB({
  url: config.url,
  token: config.token,
});
```

### Write Instance Setup
```javascript
const writeInstance = db
  .getWriteApi(config.org, config.bucket, 'ns')
  .useDefaultTags({
    datacenter: config.datacenter,
    project: config.project,
    stage: config.stage,
  });
```

## Core Function

### Write Data
```javascript
const write = async (data, isPolymorphic = false) => {
  return new Promise((resolve, reject) => {
    const { tags, fields, measurement, timestamp } = data;
    // Process and write data point
  });
}
```

## Data Structure

### Input Data Format
```javascript
{
  measurement: 'metric_name',
  timestamp: Date,           // Optional, defaults to now
  tags: {                   // Optional metadata
    key1: 'value1',
    key2: 'value2'
  },
  fields: {                 // Required data values
    field1: value1,
    field2: value2
  }
}
```

### Default Tags
- **datacenter**: Environment datacenter
- **project**: Project identifier
- **stage**: Environment stage (dev/staging/prod)

## Type Handling

### Polymorphic Mode
```javascript
const setFieldsByType = (fields, influxData) => {
  switch (typeof value) {
    case 'number':
      influxData.floatField(key, value);
      break;
    case 'boolean':
      influxData.booleanField(key, value);
      break;
    case 'string':
      influxData.stringField(key, value);
      break;
    default:
      influxData.stringField(key, value.toString());
  }
};
```

### Non-Polymorphic Mode
- **Default**: All fields treated as strings
- **Method**: `influxData.stringField(key, fields[key])`

## Features

### Automatic Timestamps
- **Default**: Uses current time if not provided
- **Custom**: Accepts timestamp in data object
- **Format**: JavaScript Date object

### Tag Processing
- **Metadata**: Key-value pairs for data categorization
- **Indexing**: Tags are indexed for fast queries
- **Immutable**: Tags cannot be changed after write

### Field Processing
- **Data Values**: Actual metric values
- **Type Detection**: Automatic in polymorphic mode
- **Validation**: Ensures at least one field or tag exists

## Usage Examples

### Basic Write
```javascript
const { write } = require('./influxDb');

await write({
  measurement: 'trip_metrics',
  fields: {
    distance: 1500,
    duration: 900
  },
  tags: {
    mode: 'transit',
    city: 'austin'
  }
});
```

### Polymorphic Write
```javascript
await write({
  measurement: 'user_activity',
  fields: {
    user_id: 12345,        // number -> floatField
    is_active: true,       // boolean -> booleanField
    status: 'online'       // string -> stringField
  }
}, true); // isPolymorphic = true
```

### Timestamped Write
```javascript
await write({
  measurement: 'events',
  timestamp: new Date('2023-01-01T12:00:00Z'),
  fields: {
    event_type: 'login',
    user_count: 1
  }
});
```

## Dependencies

### External Libraries
- `@influxdata/influxdb-client`: InfluxDB v2 client
- `config`: Configuration management

### Configuration Requirements
```javascript
database: {
  influx: {
    url: 'https://influx.example.com',
    token: 'your-token',
    org: 'organization',
    bucket: 'bucket-name',
    datacenter: 'us-east-1',
    project: 'maas-platform',
    stage: 'production'
  }
}
```

## Error Handling

### Promise-Based
- **Resolve**: On successful write
- **Reject**: On write failure with error details

### Validation
- **Required Fields**: Measurement name required
- **Data Presence**: At least one tag or field required
- **Type Safety**: Automatic type conversion in polymorphic mode

### Error Cases
```javascript
// Missing measurement
write({ fields: { value: 1 } }); // Skips write

// No data
write({ measurement: 'test' }); // Skips write

// InfluxDB errors
write(validData).catch(err => {
  console.error('Write failed:', err);
});
```

## Performance Considerations

### Batching
- **Single Point**: Each call writes one data point
- **Flush**: Explicit flush after each write
- **Optimization**: Consider batching for high-volume writes

### Memory Usage
- **Stateless**: No internal state maintained
- **Connection**: Reuses database connection
- **Cleanup**: Automatic cleanup after writes

## Integration Points

### Common Use Cases
- **Trip Metrics**: Distance, duration, costs
- **User Analytics**: Activity, engagement metrics
- **System Monitoring**: Performance, error rates
- **Business Intelligence**: Revenue, usage statistics

### Data Pipeline
- **Collection**: From various application components
- **Processing**: Optional data transformation
- **Storage**: Time-series data in InfluxDB
- **Visualization**: Grafana, custom dashboards

## Time Series Concepts

### Measurements
- **Purpose**: Logical grouping (like table name)
- **Examples**: trips, users, events, metrics

### Tags
- **Indexed**: Fast query performance
- **Categorical**: Dimensions for grouping/filtering
- **Examples**: city, mode, user_type

### Fields
- **Values**: Actual metric data
- **Types**: Numbers, strings, booleans
- **Examples**: distance, duration, count

## Monitoring

### Write Performance
- **Latency**: Monitor write response times
- **Throughput**: Track writes per second
- **Errors**: Monitor failed writes

### Data Quality
- **Schema Validation**: Ensure consistent field types
- **Completeness**: Monitor missing data
- **Accuracy**: Validate data ranges

## Best Practices

### Schema Design
- **Consistent Types**: Use polymorphic mode for type safety
- **Tag Cardinality**: Limit unique tag combinations
- **Field Selection**: Choose appropriate field types

### Performance
- **Batch Writes**: Group related data points
- **Tag Strategy**: Use tags for filtering, fields for values
- **Retention**: Configure appropriate data retention

## Security Considerations

### Access Control
- **Token-Based**: Uses InfluxDB tokens
- **Permissions**: Write-only access recommended
- **Network**: Secure connection to InfluxDB

### Data Privacy
- **PII**: Avoid storing personal identifiers
- **Anonymization**: Use hashed or encoded identifiers
- **Compliance**: Consider data retention requirements

## Testing

### Unit Tests
```javascript
// Mock InfluxDB client
const mockWriteApi = {
  writePoint: jest.fn(),
  flush: jest.fn().mockResolvedValue(),
  useDefaultTags: jest.fn().mockReturnThis()
};
```

### Integration Tests
- **Real InfluxDB**: Test against actual instance
- **Data Validation**: Verify written data
- **Error Scenarios**: Test failure conditions