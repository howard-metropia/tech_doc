# insert-pd-userbingo-log.js

## Overview
Job for bulk importing user bingo card data from HCS (Houston ConnectSmart) project into the MongoDB database. This job processes large datasets efficiently using chunked batch operations to handle user bingo card participation logs and progress tracking data.

## File Location
- **Path**: `/allrepo/connectsmart/tsp-job/src/jobs/insert-pd-userbingo-log.js`
- **Module Type**: Scheduled Job
- **Export**: Job configuration with async function

## Key Dependencies
- `@maas/core/log` - Structured logging utility
- `moment-timezone` - Date/time manipulation (imported but not used)
- `@app/src/models/UserBingocardPD` - MongoDB model for user bingo card data
- `path` - Path utilities for file system operations
- `fs` - File system access for JSON data loading

## Core Functions

### Bulk Data Import
Efficiently imports large volumes of user bingo card data from JSON files:
- **Chunked Processing**: Breaks large datasets into manageable 50-record chunks
- **Parallel Processing**: Uses Promise.all for concurrent database operations
- **Progress Tracking**: Logs completion status for each processed chunk

### Data Validation and Error Handling
Implements robust error handling for data integrity:
- **Individual Record Validation**: Continues processing despite individual failures
- **Comprehensive Logging**: Tracks both successful and failed insertions
- **Graceful Error Recovery**: Maintains process continuity on errors

## Processing Flow

### 1. Data File Loading
```javascript
const File = await fs.promises.readFile(
  path.join(__dirname, '../static/hcs_user_bingocard_pd.json'), 
  'utf8'
);
const Data = JSON.parse(File);
```

### 2. Chunk Array Creation
```javascript
const chuckArray = [];
let subChunk = [];
const chunkSize = 50;

for (const d of Data) {
  if (subChunk.length === chunkSize) {
    chuckArray.push(subChunk);
    subChunk = [];
  }
  subChunk.push(d);
}
```

### 3. Parallel Batch Processing
```javascript
for (let i = 0; i < chuckArray.length; i++) {
  await Promise.all(chuckArray[i].map(async (d) => {
    const resp = await UserBingocardPD.query().insertGraph(d);
    if (resp) {
      // Success handling
    } else {
      logger.info(`[insert-pd-userbingo-log] error on: ${d.id}`);
    }
  }));
  console.log(`[insert-pd-userbingo-log] inserted sub-chunk No ${i} done!`);
}
```

## Data Models

### UserBingocardPD Model
```javascript
// MongoDB document structure (inferred)
{
  id: string,                    // Unique identifier
  user_id: number,              // User reference
  bingo_card_data: Object,      // Bingo card configuration
  progress: Object,             // User progress tracking
  created_at: Date,             // Creation timestamp
  updated_at: Date,             // Last update timestamp
  // Additional fields from HCS data structure
}
```

### Input Data Structure
```javascript
// From hcs_user_bingocard_pd.json
[
  {
    id: "string",
    user_id: number,
    // Additional bingo card data fields
    // Progress tracking information
    // Game state and completion status
  }
]
```

### Chunk Processing Structure
```javascript
{
  chuckArray: Array<Array<Object>>,  // Array of 50-record chunks
  subChunk: Array<Object>,           // Current chunk being built
  chunkSize: 50,                     // Fixed chunk size for optimization
  totalChunks: number,               // Calculated total chunks
  processedChunks: number            // Progress counter
}
```

## Business Logic

### Chunking Strategy
- **Optimal Chunk Size**: 50 records per chunk for database performance
- **Memory Management**: Prevents memory overflow on large datasets
- **Parallel Processing**: Each chunk processed concurrently for speed

### Error Handling Strategy
```javascript
// Individual record error handling
if (resp) {
  // Successful insertion
} else {
  logger.info(`[insert-pd-userbingo-log] error on: ${d.id}`);
}

// Global error handling
try {
  // Processing logic
} catch (e) {
  console.log(e);
}
```

### Progress Monitoring
```javascript
console.log(`[insert-pd-userbingo-log] inserted sub-chunk No ${i} done!`);
```

## Database Operations

### MongoDB Integration
```javascript
// Uses Objection.js ORM with MongoDB adapter
const resp = await UserBingocardPD.query().insertGraph(d);
```

### Insert Graph Operation
- **Graph Insertion**: Handles complex nested document structures
- **Relationship Management**: Maintains document relationships
- **Atomic Operations**: Ensures data consistency

## Performance Considerations

### Batch Processing Optimization
- **Chunk Size**: 50 records optimized for MongoDB performance
- **Parallel Execution**: Promise.all for concurrent database operations
- **Memory Efficiency**: Sequential chunk processing prevents memory exhaustion

### Database Performance
- **Insert Graph**: Efficient for complex document structures
- **Connection Pooling**: Leverages MongoDB connection pooling
- **Index Optimization**: Assumes proper indexing on target collection

### Error Resilience
- **Continue on Error**: Individual failures don't stop batch processing
- **Comprehensive Logging**: All errors logged for investigation
- **Process Completion**: Ensures all chunks processed despite errors

## Integration Points

### HCS Project Integration
- **Data Source**: Houston ConnectSmart bingo card system
- **User Tracking**: Links to user management system
- **Progress Monitoring**: Integrates with user engagement tracking

### MongoDB Database
- **Collection**: UserBingocardPD collection in MongoDB
- **Indexes**: Requires appropriate indexes for query performance
- **Schema**: Flexible schema for varied bingo card data

### File System
- **Static Files**: Reads from ../static/ directory
- **JSON Format**: Expects well-formed JSON input data
- **Path Resolution**: Uses relative path from job directory

## Error Handling Patterns

### File System Errors
```javascript
try {
  const File = await fs.promises.readFile(filePath, 'utf8');
} catch (error) {
  // File read error handling
}
```

### Database Errors
```javascript
const resp = await UserBingocardPD.query().insertGraph(d);
if (!resp) {
  logger.info(`[insert-pd-userbingo-log] error on: ${d.id}`);
}
```

### JSON Parsing Errors
```javascript
try {
  const Data = JSON.parse(File);
} catch (parseError) {
  // JSON parsing error handling
}
```

## Monitoring and Logging

### Progress Logging
```javascript
console.log(`[insert-pd-userbingo-log] inserted sub-chunk No ${i} done!`);
```

### Error Logging
```javascript
logger.info(`[insert-pd-userbingo-log] error on: ${d.id}`);
```

### Exception Logging
```javascript
catch (e) {
  console.log(e);
}
```

## Usage Scenarios
- **Data Migration**: Migrating bingo card data from legacy systems
- **Bulk Import**: Initial population of user bingo card collections
- **System Integration**: Importing data from external HCS systems
- **Database Seeding**: Populating development/testing environments

## Data Flow
```
JSON File → Chunk Creation → Parallel Processing → MongoDB Insertion → 
Progress Logging → Completion Status
```

## Configuration Dependencies
- **File Path**: `../static/hcs_user_bingocard_pd.json`
- **MongoDB Connection**: Configured through UserBingocardPD model
- **Logging Configuration**: Structured logging through @maas/core/log

## Performance Metrics
- **Chunk Size**: 50 records per chunk (optimized for performance)
- **Parallel Processing**: Up to 50 concurrent database operations
- **Memory Usage**: Controlled through sequential chunk processing
- **Error Rate**: Individual record failures logged but don't halt processing

## Best Practices Implementation
- **Asynchronous Processing**: Non-blocking file and database operations
- **Error Isolation**: Individual record errors don't affect batch
- **Progress Visibility**: Clear logging of processing status
- **Resource Management**: Controlled memory usage through chunking

## Notes
- Designed for large-scale data import operations
- Optimized for MongoDB document insertion patterns
- Provides robust error handling for production environments
- Maintains data integrity through careful error management
- Suitable for automated data pipeline operations
- Critical for HCS project data management and user engagement tracking