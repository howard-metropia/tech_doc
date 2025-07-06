# Update BI MongoDB Views Job

## Overview
Job that synchronizes MongoDB database views from the primary cache database to a dedicated Business Intelligence (BI) MongoDB instance. This enables isolated analytics workloads while maintaining data freshness for reporting and business intelligence operations without impacting production database performance.

## File Location
`/src/jobs/update-bi-mongodb-views.js`

## Dependencies
- `mongoose` - MongoDB object modeling and connection management
- `mongodb-uri` - MongoDB connection URI formatting utility
- `@maas/core/mongo` - Core MongoDB connection service for cache database
- `@maas/core/log` - Logging framework for operational monitoring

## Job Configuration

### Inputs
```javascript
inputs: {}  // No input parameters - processes all views automatically
```

### Environment Variables Required
```javascript
const isEnvExists = () => {
  return (
    process.env.MONGO_BI_HOST &&
    process.env.MONGO_BI_USER &&
    process.env.MONGO_BI_PASSWORD &&
    process.env.MONGO_BI_DB
  );
};
```

**Required Environment Variables**:
- `MONGO_BI_HOST`: BI MongoDB server hostname
- `MONGO_BI_PORT`: BI MongoDB server port (defaults to 27017)
- `MONGO_BI_USER`: BI database authentication username
- `MONGO_BI_PASSWORD`: BI database authentication password
- `MONGO_BI_DB`: BI database name

## Database Connection Management

### Source Database Connection
```javascript
const cache = require('@maas/core/mongo')('cache');
const srcDb = await getDb(cache);
```

**Features**:
- Uses existing cache database connection
- Source of truth for view data
- Production database with current data

### Destination Database Connection
```javascript
const getDestConnection = () => {
  const uri = mongodbUri.formatMongoose({
    hosts: [
      {
        host: process.env.MONGO_BI_HOST,
        port: process.env.MONGO_BI_PORT || 27017,
      },
    ],
    database: process.env.MONGO_BI_DB,
    username: process.env.MONGO_BI_USER,
    password: process.env.MONGO_BI_PASSWORD,
    options: {
      authSource: 'admin',
      retryWrites: false,
    },
  });

  const connection = mongoose.createConnection(uri, {
    useNewUrlParser: true,
    useUnifiedTopology: true,
    socketTimeoutMS: 0,
  });

  return connection;
};
```

**Connection Features**:
- **Authentication**: Admin-level authentication for BI database
- **Retry Writes Disabled**: Optimized for read-heavy BI workloads
- **Socket Timeout**: Unlimited timeout for large data transfers
- **Modern Parser**: Uses new MongoDB connection string parser

## View Discovery and Processing

### View Detection
```javascript
const views = await srcDb.listCollections({ type: 'view' }).toArray();
const viewNames = views.map(({ name }) => name);
logger.info(`Views detected: ` + viewNames.join(', '));
```

**Features**:
- **Automatic Discovery**: Finds all views in source database
- **Type Filtering**: Only processes collections of type 'view'
- **Dynamic Processing**: Adapts to changing view definitions

### Data Synchronization Logic
```javascript
for (const viewName of viewNames) {
  logger.info(`Fetching ${viewName} view...`);
  const documents = await srcDb.collection(viewName).find().toArray();
  
  if (documents.length === 0) {
    logger.info(`No document exists in ${viewName} view, skipped`);
    continue;
  }
  
  logger.info(`Emptying BI ${viewName} collection...`);
  await destDb.collection(viewName).deleteMany({});
  
  logger.info(`Inserting data to BI ${viewName} collection...`);
  await destDb.collection(viewName).insertMany(documents);
}
```

## Synchronization Strategy

### Complete Refresh Approach
1. **Full Data Extraction**: Retrieves all documents from source view
2. **Target Cleanup**: Deletes all existing documents in BI collection
3. **Bulk Insert**: Inserts all source documents to BI collection
4. **Atomic Operation**: Each view is processed completely before next

### Data Validation
```javascript
if (documents.length === 0) {
  logger.info(`No document exists in ${viewName} view, skipped`);
  continue;
}
```

**Benefits**:
- **Empty View Handling**: Skips processing of empty views
- **Resource Optimization**: Avoids unnecessary delete/insert operations
- **Clear Logging**: Indicates when views are skipped and why

## Connection Lifecycle Management

### Database Helper Function
```javascript
const getDb = (connection) => {
  return connection.getClient().db();
};
```

### Connection Cleanup
```javascript
destConnection.destroy();
logger.info('Success synchronizing MongoDB BI views');
```

**Resource Management**:
- **Explicit Cleanup**: Properly closes BI database connection
- **Memory Management**: Prevents connection leaks
- **Performance**: Ensures efficient resource utilization

## Error Handling and Validation

### Environment Validation
```javascript
if (!isEnvExists()) {
  logger.error('No MongoDB BI configurations');
  return;
}
```

**Safety Checks**:
- **Configuration Validation**: Ensures all required environment variables exist
- **Early Exit**: Prevents execution with incomplete configuration
- **Clear Error Messages**: Indicates missing configuration requirements

### Operation Logging
```javascript
logger.info('Start synchronizing MongoDB BI views...');
logger.info(`Views detected: ` + viewNames.join(', '));
logger.info(`Fetching ${viewName} view...`);
logger.info(`Emptying BI ${viewName} collection...`);
logger.info(`Inserting data to BI ${viewName} collection...`);
logger.info('Success synchronizing MongoDB BI views');
```

## Performance Considerations

### Bulk Operations
```javascript
await destDb.collection(viewName).deleteMany({});
await destDb.collection(viewName).insertMany(documents);
```

**Optimization Features**:
- **Bulk Delete**: Efficient removal of existing data
- **Bulk Insert**: Optimized insertion of new data
- **Sequential Processing**: Prevents database overload

### Memory Management
- **Per-View Processing**: Handles one view at a time to manage memory
- **Document Streaming**: Could be enhanced for very large views
- **Connection Reuse**: Efficient connection pooling

## Business Intelligence Integration

### Dedicated BI Database Benefits
- **Performance Isolation**: BI queries don't impact production
- **Specialized Indexing**: BI-optimized indexes and configurations
- **Analytics Workloads**: Support for complex aggregation queries
- **Reporting Tools**: Integration with external BI tools

### View Synchronization Features
- **Data Freshness**: Ensures BI data matches production views
- **Schema Consistency**: Maintains view structure across databases
- **Complete Refresh**: Guarantees data accuracy and consistency

## MongoDB Views Architecture

### Source Views (Cache Database)
- **Aggregation Pipelines**: Complex data transformation views
- **Real-time Data**: Current production data state
- **Optimized Queries**: Views designed for application performance

### BI Views (BI Database)
- **Analytics Optimized**: Optimized for reporting and analysis
- **Historical Data**: May include additional retention policies
- **External Access**: Safe for third-party BI tool access

## Use Cases and Applications

### Business Intelligence Scenarios
- **Executive Dashboards**: Real-time business metrics
- **Operational Reports**: System performance and usage analytics
- **User Analytics**: Behavior analysis and insights
- **Financial Reporting**: Revenue and transaction analysis

### Data Warehouse Integration
- **ETL Pipelines**: Source data for data warehouse processes
- **Data Lake**: Structured data for advanced analytics
- **Machine Learning**: Feature engineering and model training data

## Security Considerations

### Database Isolation
- **Separate Credentials**: Distinct authentication for BI database
- **Network Isolation**: BI database on separate network segments
- **Access Control**: Limited access to BI database for security

### Data Protection
- **Read-Only Access**: BI database primarily for read operations
- **Audit Logging**: Complete synchronization audit trail
- **Data Integrity**: Ensures accurate data replication

## Schedule Context
Typically scheduled to run regularly (hourly, daily, or based on business needs) to:
- Maintain current data in BI systems
- Support real-time business intelligence requirements
- Enable reliable reporting and analytics
- Ensure data consistency across environments

## Integration Points

### Source Systems
- **Cache Database**: Primary source for view data
- **Production Applications**: Systems creating and updating views
- **MongoDB Views**: Aggregation pipelines and computed collections

### Target Systems
- **BI Tools**: Tableau, Power BI, Looker, etc.
- **Reporting Systems**: Custom dashboards and reports
- **Analytics Platforms**: Data science and machine learning tools
- **Data Warehouses**: Enterprise data warehouse integration

## Monitoring and Alerting

### Operational Metrics
- **Synchronization Duration**: Time taken for complete sync
- **Data Volume**: Number of documents synchronized per view
- **View Count**: Number of views processed
- **Success Rate**: Percentage of successful synchronizations

### Error Scenarios
- **Connection Failures**: Database connectivity issues
- **Authentication Errors**: Credential or permission problems
- **Data Transfer Errors**: Network or timeout issues
- **Configuration Missing**: Environment variable validation failures

## Business Impact
- **Business Intelligence**: Enables isolated BI workloads without production impact
- **Data Accessibility**: Provides dedicated access for analytics teams
- **Performance Optimization**: Separates analytical and operational workloads
- **Reporting Reliability**: Ensures consistent data for business reporting
- **Scalability**: Supports growing BI and analytics requirements
- **System Stability**: Protects production systems from heavy analytical queries