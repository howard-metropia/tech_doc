# Update Cluster ID Job

## Overview
Job that synchronizes cluster IDs between MongoDB cluster_trips collection and MySQL cm_cluster_id table, ensuring that all cluster identifiers from MongoDB are properly represented in the MySQL database for cross-database referencing and analytics. This maintains data consistency across the hybrid database architecture.

## File Location
`/src/jobs/update-cluster-id.js`

## Dependencies
- `@maas/core/log` - Logging framework for operational monitoring
- `@app/src/models/CmClusterId` - MySQL model for cluster ID management
- `@app/src/models/ClusterTrips` - MongoDB model for cluster trip data

## Job Configuration

### Inputs
```javascript
inputs: {}  // No input parameters - processes all clusters automatically
```

### Processing Mode
- **Automatic Processing**: Discovers and synchronizes all cluster IDs
- **Incremental Updates**: Only inserts missing cluster IDs
- **Data Integrity**: Maintains referential consistency across databases

## Data Source Analysis

### MongoDB Cluster Trips Collection
```javascript
const getClusterTrips = async () => {
  try {
    const resp = await ClusterTrips.find().lean();
    return resp || [];
  } catch (e) {
    logger.error(`[update-cluster-id][getClusterTrips] error: ${e.message}`);
    return [];
  }
};
```

**Features**:
- Retrieves all cluster documents from MongoDB
- Uses lean queries for performance optimization
- Comprehensive error handling with fallback empty array
- Source of truth for cluster existence

### MySQL Cluster ID Table
```javascript
const existingRows = await CmClusterId.query().select('cluster_id');
const existingIds = new Set(existingRows.map(row => row.cluster_id));
```

**Structure**:
- Maintains cluster_id references in MySQL
- Enables cross-database joins and queries
- Supports relational database operations on cluster data

## Synchronization Logic

### Missing Cluster Detection
```javascript
const missingClusters = [];
for (const cluster of clusterList) {
  const clusterId = cluster._id?.toString();
  if (clusterId && !existingIds.has(clusterId)) {
    missingClusters.push(clusterId);
  }
}
```

**Detection Process**:
1. **ID Extraction**: Converts MongoDB ObjectId to string format
2. **Existence Check**: Uses Set for O(1) lookup performance
3. **Validation**: Ensures valid cluster ID before processing
4. **Collection**: Builds list of missing cluster IDs for batch processing

### Incremental Insert Strategy
```javascript
for (const clusterId of missingClusters) {
  await CmClusterId.query().insert({ cluster_id: clusterId });
  logger.info(`[update-cluster-id] Inserted cluster_id: ${clusterId}`);
}
```

**Benefits**:
- **Sequential Processing**: Avoids concurrent insert conflicts
- **Individual Logging**: Tracks each insert operation
- **Error Isolation**: Single cluster failures don't affect others
- **Audit Trail**: Complete record of synchronization activities

## Data Type Handling

### ObjectId to String Conversion
```javascript
const clusterId = cluster._id?.toString();
```

**Considerations**:
- MongoDB uses ObjectId format for document identifiers
- MySQL requires string representation for storage
- Safe navigation operator prevents null reference errors
- Consistent string format across database systems

### Validation Logic
```javascript
if (clusterId && !existingIds.has(clusterId)) {
  missingClusters.push(clusterId);
}
```

**Validation Steps**:
1. **Existence Check**: Ensures clusterId is not null/undefined
2. **Duplication Prevention**: Verifies ID not already in MySQL
3. **Type Safety**: Handles potential type conversion issues

## Performance Optimization

### Set-Based Lookups
```javascript
const existingIds = new Set(existingRows.map(row => row.cluster_id));
```

**Advantages**:
- **O(1) Lookup Time**: Efficient existence checking
- **Memory Efficient**: Optimal for large datasets
- **Fast Comparison**: Outperforms array-based searches

### Lean Queries
```javascript
const resp = await ClusterTrips.find().lean();
```

**Benefits**:
- **Reduced Memory Usage**: Skips Mongoose document hydration
- **Faster Processing**: Raw JavaScript objects
- **Lower Overhead**: Minimal object creation

## Error Handling Strategy

### Function-Level Error Handling
```javascript
const getClusterTrips = async () => {
  try {
    const resp = await ClusterTrips.find().lean();
    return resp || [];
  } catch (e) {
    logger.error(`[update-cluster-id][getClusterTrips] error: ${e.message}`);
    return [];
  }
};
```

### Job-Level Error Management
```javascript
try {
  logger.info(`[update-cluster-id] start`);
  // Main processing logic
  logger.info(`[update-cluster-id] job end`);
} catch (e) {
  logger.error(`[update-cluster-id] error: ${e.message}`);
  logger.info(`[update-cluster-id] stack: ${e.stack}`);
}
```

**Error Recovery**:
- **Graceful Degradation**: Empty arrays on query failures
- **Detailed Logging**: Error messages and stack traces
- **Operational Continuity**: Job completes even with partial failures

## Logging and Monitoring

### Progress Tracking
```javascript
logger.info(`[update-cluster-id] start`);
logger.info(`[update-cluster-id] No clusters found`);
logger.info(`[update-cluster-id] Inserted cluster_id: ${clusterId}`);
logger.info(`[update-cluster-id] job end`);
```

### Operational Visibility
- **Job Lifecycle**: Start and end timestamps
- **Processing Statistics**: Number of clusters processed
- **Individual Operations**: Each cluster ID insertion logged
- **Error Diagnostics**: Detailed error information

## Data Consistency Management

### Cross-Database Synchronization
The job ensures consistency between:
- **MongoDB cluster_trips**: Source collection with cluster data
- **MySQL cm_cluster_id**: Reference table for relational operations

### Referential Integrity
- **One-Way Sync**: MongoDB is source of truth for cluster existence
- **Reference Table**: MySQL table serves as lookup for cluster IDs
- **Foreign Key Support**: Enables joins with other MySQL tables

## Business Logic Integration

### Cluster Management Workflow
1. **Cluster Creation**: New clusters created in MongoDB
2. **ID Synchronization**: This job ensures MySQL references
3. **Cross-Database Queries**: Applications can join cluster data
4. **Analytics Support**: Enables relational analysis of cluster data

### Use Cases
- **Reporting**: SQL-based reporting on cluster analytics
- **Data Warehousing**: ETL processes requiring cluster references
- **Application Queries**: Hybrid queries across database systems
- **Data Migration**: Consistent cluster references during migrations

## Integration Points

### MongoDB Collections
- **cluster_trips**: Source collection for cluster data
- **Related Collections**: Other collections referencing cluster IDs

### MySQL Tables
- **cm_cluster_id**: Target table for cluster ID references
- **Related Tables**: Tables with foreign key relationships to clusters

## Schedule Context
Typically scheduled to run regularly (daily or hourly) to:
- Maintain synchronization between MongoDB and MySQL
- Ensure new clusters are immediately available for SQL queries
- Support real-time analytics requiring cluster references
- Prevent referential integrity issues in hybrid database operations

## Performance Characteristics

### Scalability Considerations
- **Incremental Processing**: Only processes new cluster IDs
- **Efficient Queries**: Uses optimized database operations
- **Memory Management**: Handles large cluster datasets efficiently
- **Batch Processing**: Could be enhanced for bulk insertions

### Database Load Management
- **Read-Heavy Operations**: Minimal write operations to both databases
- **Sequential Inserts**: Avoids concurrent write conflicts
- **Connection Pooling**: Efficient database connection usage

## Business Impact
- **Data Consistency**: Maintains hybrid database integrity
- **Analytics Support**: Enables cross-database cluster analysis
- **Application Performance**: Provides efficient cluster lookups
- **System Reliability**: Prevents referential integrity errors
- **Operational Efficiency**: Automates database synchronization tasks
- **Development Support**: Simplifies application database queries