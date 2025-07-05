# Truck Map Service

## Overview

The Truck Map Service manages truck routing and mapping data through a comprehensive workflow that includes S3 cloud storage, MongoDB persistence, and data validation. It provides synchronization capabilities between cloud storage and database systems while ensuring data integrity through schema validation.

## Service Information

- **Service Name**: Truck Map Service  
- **File Path**: `/src/services/TruckService.js`
- **Type**: Data Management & Validation Service
- **Dependencies**: AWS S3, MongoDB, Joi Schema Validation

## Class Structure

### TruckMapService

Main service class that encapsulates all truck map data operations with integrated validation and storage management.

**Constructor Dependencies**:
```javascript
constructor() {
  this.storage = new StorageS3();                          // S3 storage handler
  this.truckMapFileName = 'truck_map.json';                // S3 file identifier
  this.validatorTruckMapArray = TruckMapSchemas.ValidateTruckMapArray;
  this.validatorJsonFileContent = TruckMapSchemas.ValidateTruckMapJsonContent;
  this.validatorMongoDbData = TruckMapSchemas.ValidateTruckMapMongoDBData;
}
```

## Core Methods

### uploadTruckMapDataToS3(truckMapJsonContent)

Validates and uploads truck map data to AWS S3 cloud storage.

**Purpose**: Stores truck map configuration in cloud storage with validation
**Parameters**:
- `truckMapJsonContent` (string): JSON string containing truck map data
**Returns**: Promise (async function)

**Process Flow**:
1. **Content Parsing**: Parses JSON string to JavaScript object
2. **Schema Validation**: Validates against JSON file content schema
3. **S3 Upload**: Stores validated content to configured S3 bucket
4. **Error Propagation**: Throws validation or upload errors

**Usage Example**:
```javascript
const truckService = new TruckMapService();
const jsonContent = JSON.stringify({
  truck_map_array: [
    {
      zone_id: "zone_001",
      restrictions: ["weight_limit", "height_limit"],
      coordinates: [[lat1, lng1], [lat2, lng2], [lat3, lng3]]
    }
  ]
});

await truckService.uploadTruckMapDataToS3(jsonContent);
console.log('Truck map data uploaded successfully');
```

**Validation Requirements**:
- Valid JSON format
- Complies with TruckMapJsonContent schema
- Required fields present and properly typed
- Coordinate data in correct format

### getTruckMapJsonDataFromS3()

Retrieves and validates truck map data from AWS S3 storage.

**Purpose**: Fetches current truck map configuration from cloud storage
**Parameters**: None
**Returns**: Promise resolving to validated truck map object

**Process Flow**:
1. **S3 Retrieval**: Downloads truck_map.json from S3 bucket
2. **JSON Parsing**: Converts file content to JavaScript object
3. **Schema Validation**: Validates against JSON content schema
4. **Data Return**: Returns validated truck map object

**Usage Example**:
```javascript
const truckMapData = await truckService.getTruckMapJsonDataFromS3();
console.log(`Retrieved truck map with ${truckMapData.truck_map_array.length} zones`);

// Access truck map data
truckMapData.truck_map_array.forEach(zone => {
  console.log(`Zone ${zone.zone_id}: ${zone.restrictions.join(', ')}`);
});
```

**Error Scenarios**:
- **S3 Access Errors**: Network, authentication, or permission issues
- **File Not Found**: truck_map.json doesn't exist in S3
- **Invalid JSON**: Corrupted or malformed JSON content
- **Schema Violations**: Data doesn't match expected structure

### saveTruckMapToMongoDB(truckMapArrayData)

Validates and persists truck map array data to MongoDB collection.

**Purpose**: Stores truck map data in MongoDB with schema validation
**Parameters**:
- `truckMapArrayData` (array): Array of truck map zone objects
**Returns**: Promise resolving to saved MongoDB document

**Process Flow**:
1. **Array Validation**: Validates input against truck map array schema
2. **Document Creation**: Creates new TruckMapModel instance
3. **Database Save**: Persists document to MongoDB collection
4. **Error Handling**: Logs and re-throws save errors

**Usage Example**:
```javascript
const truckMapArray = [
  {
    zone_id: "downtown_001",
    name: "Downtown Truck Restriction Zone",
    restrictions: ["weight_limit_10t", "height_limit_4m"],
    coordinates: [
      [29.7604, -95.3698],
      [29.7749, -95.3659], 
      [29.7580, -95.3676]
    ],
    effective_hours: "06:00-22:00",
    days_of_week: ["monday", "tuesday", "wednesday", "thursday", "friday"]
  }
];

const savedDoc = await truckService.saveTruckMapToMongoDB(truckMapArray);
console.log(`Saved truck map document with ID: ${savedDoc._id}`);
```

**Data Structure Requirements**:
```javascript
{
  zone_id: String,           // Unique zone identifier
  name: String,              // Human-readable zone name
  restrictions: [String],    // Array of restriction types
  coordinates: [[Number]],   // Array of [lat, lng] coordinate pairs
  effective_hours: String,   // Time range (e.g., "06:00-22:00")
  days_of_week: [String]     // Array of day names
}
```

### syncTruckMapFromS3ToMongoDb(truckMapJsonContent)

Comprehensive synchronization workflow that updates both S3 and MongoDB with new data.

**Purpose**: Synchronizes truck map data across storage systems with validation
**Parameters**:
- `truckMapJsonContent` (string, optional): New truck map JSON content
**Returns**: Promise (async function)

**Synchronization Process**:
1. **Conditional Upload**: Uploads new content to S3 if provided
2. **Data Retrieval**: Fetches current data from S3
3. **Array Extraction**: Extracts truck_map_array from JSON structure
4. **MongoDB Save**: Persists array data to MongoDB
5. **Validation Check**: Validates latest MongoDB record

**Usage Scenarios**:

**Scenario 1: Update with new data**
```javascript
const newTruckMapData = JSON.stringify({
  truck_map_array: [...updatedZones],
  metadata: {
    updated_at: new Date().toISOString(),
    version: "2.1"
  }
});

await truckService.syncTruckMapFromS3ToMongoDb(newTruckMapData);
console.log('Truck map synchronized with new data');
```

**Scenario 2: Sync existing S3 data to MongoDB**
```javascript
// Sync without uploading new data
await truckService.syncTruckMapFromS3ToMongoDb();
console.log('MongoDB synchronized with current S3 data');
```

**Error Handling**:
- **Upload Failures**: S3 upload errors halt the process
- **Retrieval Failures**: S3 download errors prevent synchronization
- **Save Failures**: MongoDB errors are logged and propagated
- **Validation Failures**: Schema violations stop the sync process

### validateLatestTruckMap()

Validates the most recently stored truck map document in MongoDB.

**Purpose**: Ensures data integrity of latest MongoDB truck map record
**Parameters**: None  
**Returns**: Promise (async function)

**Validation Process**:
1. **Latest Record Query**: Finds most recent document by created_at timestamp
2. **Document Conversion**: Converts Mongoose document to plain object
3. **Schema Validation**: Validates against MongoDB data schema
4. **Silent Success**: No action needed if validation passes

**Usage Example**:
```javascript
await truckService.validateLatestTruckMap();
console.log('Latest truck map validation completed successfully');
```

**Query Logic**:
```javascript
const latestDocument = await TruckMapModel.findOne(
  {},                           // No filter - all documents
  {},                           // No field projection
  { sort: { created_at: -1 } }  // Sort by created_at descending
);
```

**Validation Scenarios**:
- **No Documents**: Gracefully handles empty collection
- **Valid Data**: Silent success for compliant documents
- **Invalid Data**: Throws validation errors with details
- **Schema Evolution**: Detects incompatible document structures

## Data Schemas & Validation

### Truck Map Array Schema
Validates individual truck zone configurations:
```javascript
// Example valid truck map zone
{
  zone_id: "zone_001",                    // Required unique identifier
  name: "Downtown Commercial District",   // Human-readable name
  restrictions: [                         // Array of restriction types
    "weight_limit_10t",
    "height_limit_4m", 
    "hazmat_prohibited"
  ],
  coordinates: [                          // Polygon boundary points
    [29.7604, -95.3698],
    [29.7749, -95.3659],
    [29.7580, -95.3676],
    [29.7604, -95.3698]                   // Closed polygon
  ],
  effective_hours: "06:00-22:00",         // Time restrictions
  days_of_week: ["monday", "tuesday", "wednesday", "thursday", "friday"]
}
```

### JSON File Content Schema
Validates complete S3 file structure:
```javascript
{
  truck_map_array: [...],                 // Array of truck zones
  metadata: {                             // Optional metadata
    version: "2.1",
    updated_at: "2024-01-01T00:00:00Z",
    updated_by: "system"
  }
}
```

### MongoDB Data Schema
Validates persisted document structure:
```javascript
{
  _id: ObjectId,                          // MongoDB document ID
  truck_map: [...],                       // Truck map zone array
  created_at: Date,                       // Document creation timestamp
  updated_at: Date                        // Last modification timestamp
}
```

## Storage Integration

### AWS S3 Integration
The service integrates with AWS S3 for cloud storage:

**Storage Configuration**:
- **Bucket**: Configured in StorageS3 helper
- **File Name**: 'truck_map.json' (configurable)
- **Format**: JSON with UTF-8 encoding
- **Access**: Requires appropriate S3 permissions

**S3 Operations**:
```javascript
// Upload operation
await this.storage.uploadFileContentToS3File(fileName, jsonContent);

// Download operation  
const jsonData = await this.storage.getJsonDataFromS3(fileName);
```

### MongoDB Integration
MongoDB storage provides persistent data management:

**Collection Structure**:
- **Model**: TruckMapModel (Mongoose schema)
- **Collection**: Typically 'truckmaps' (configurable)
- **Indexing**: Automatic indexing on created_at for sorting
- **Versioning**: Multiple documents maintain historical data

**Document Lifecycle**:
1. **Creation**: New documents added via save operations
2. **Querying**: Latest document retrieved by timestamp
3. **Validation**: Schema validation on save and retrieval
4. **Retention**: Historical documents preserved for audit

## Error Handling & Logging

### Comprehensive Error Management
```javascript
try {
  return await truckMap.save();
} catch (error) {
  logger.warn(`[sync_truck_map_data_to_mangodb] error: ${error.message}`);
  throw error;
}
```

### Error Categories
- **Validation Errors**: Schema compliance failures
- **Storage Errors**: S3 upload/download failures  
- **Database Errors**: MongoDB connection or save failures
- **Network Errors**: Connectivity issues with external services

### Logging Strategy
- **Warn Level**: Non-critical errors with recovery options
- **Error Context**: Specific operation context in log messages
- **Error Propagation**: Re-throw errors for upstream handling
- **Operation Tracking**: Log successful operations for monitoring

## Performance Considerations

### Data Size Management
- **JSON Parsing**: Efficient parsing of large truck map files
- **Memory Usage**: Optimized object handling for large datasets
- **Network Transfer**: Compressed data transfer to/from S3
- **Database Operations**: Efficient MongoDB operations

### Caching Strategy
```javascript
// Consider implementing caching for frequently accessed data
class TruckMapService {
  constructor() {
    this.cache = new Map();
    this.cacheTimeout = 5 * 60 * 1000; // 5 minutes
  }
  
  async getCachedTruckMap() {
    const cached = this.cache.get('truck_map');
    if (cached && (Date.now() - cached.timestamp) < this.cacheTimeout) {
      return cached.data;
    }
    
    const data = await this.getTruckMapJsonDataFromS3();
    this.cache.set('truck_map', { data, timestamp: Date.now() });
    return data;
  }
}
```

### Optimization Recommendations
- **Lazy Loading**: Load truck map data only when needed
- **Incremental Updates**: Update only changed zones
- **Connection Pooling**: Efficient database connection management
- **Batch Processing**: Handle multiple zones in single operations

## Security Considerations

### Access Control
- **S3 Permissions**: Restricted access to truck map bucket
- **MongoDB Security**: Database authentication and authorization
- **Input Validation**: Comprehensive schema validation
- **Data Sanitization**: Clean input data before processing

### Data Integrity
- **Schema Validation**: Multi-layer validation ensures data quality
- **Atomic Operations**: Consistent state across storage systems
- **Backup Strategy**: S3 provides durable backup storage
- **Version Control**: MongoDB maintains historical versions

### Audit Trail
```javascript
// Enhanced logging for audit requirements
const auditLog = {
  operation: 'sync_truck_map',
  timestamp: new Date().toISOString(),
  user_id: context.user_id,
  source: 's3',
  destination: 'mongodb',
  record_count: truckMapArray.length
};

logger.info('Truck map sync audit:', auditLog);
```

## Integration Points

### Used By
- **Truck Routing Services**: Route optimization with restriction data
- **Navigation APIs**: Real-time truck route calculation
- **Admin Interfaces**: Truck map configuration management
- **Scheduled Jobs**: Automated data synchronization

### External Dependencies
- **StorageS3**: AWS S3 storage management helper
- **TruckMapModel**: Mongoose model for MongoDB operations
- **TruckMapSchemas**: Joi validation schema definitions
- **@maas/core/log**: Centralized logging system

## Deployment & Configuration

### Environment Configuration
```javascript
// Required environment variables
{
  AWS_ACCESS_KEY_ID: "...",              // S3 access credentials
  AWS_SECRET_ACCESS_KEY: "...",          // S3 secret key
  AWS_REGION: "us-east-1",               // S3 bucket region
  S3_BUCKET_NAME: "truck-maps",          // S3 bucket name
  MONGODB_URI: "mongodb://...",          // MongoDB connection string
}
```

### Service Initialization
```javascript
const { TruckMapService } = require('@app/src/services/TruckService');

// Initialize service with dependencies
const truckService = new TruckMapService();

// Verify service health
await truckService.validateLatestTruckMap();
console.log('Truck map service initialized successfully');
```

## Testing Strategies

### Unit Testing
```javascript
const { TruckMapService } = require('@app/src/services/TruckService');

describe('TruckMapService', () => {
  let service;
  
  beforeEach(() => {
    service = new TruckMapService();
  });
  
  test('validates truck map array data', async () => {
    const validData = [
      {
        zone_id: "test_zone",
        restrictions: ["weight_limit"],
        coordinates: [[0, 0], [1, 1], [0, 1], [0, 0]]
      }
    ];
    
    await expect(service.saveTruckMapToMongoDB(validData)).resolves.toBeDefined();
  });
});
```

### Integration Testing
- **S3 Connectivity**: Test S3 upload and download operations
- **MongoDB Operations**: Verify database save and retrieval
- **Schema Validation**: Test validation with various data formats
- **End-to-End Sync**: Complete synchronization workflow testing

## Dependencies

- **@app/src/helpers/storage**: StorageS3 class for AWS S3 operations
- **@app/src/models/TruckModel**: TruckMapModel for MongoDB operations
- **@app/src/schemas/truckSchema**: TruckMapSchemas for validation
- **@maas/core/log**: Centralized logging system