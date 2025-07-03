# tow-and-go-data-upload-s3.js

## Overview
Job module responsible for uploading Tow and Go traffic data to AWS S3 storage. This job processes and stores real-time traffic information including link IDs, segment IDs, and last modified timestamps to support the Tow and Go service's data synchronization pipeline.

## Purpose
- Upload Tow and Go traffic data to AWS S3 bucket for storage and processing
- Handle real-time traffic link and segment information
- Support data pipeline for traffic incident management
- Enable downstream processing and analysis of traffic data

## Key Features
- **S3 Integration**: Direct upload to AWS S3 storage infrastructure
- **JSON Data Processing**: Handles structured traffic data with link and segment mappings
- **Service Architecture**: Leverages TowAndGoService for data management
- **Flexible Input Handling**: Supports varying data structures including null segment IDs

## Dependencies
```javascript
const { TowAndGoService } = require('@app/src/services/towAndGoService');
```

## Core Function Structure
```javascript
module.exports = {
  inputs: {
    s3FileName: String,
    towAndGoData: String,
  },
  fn: async function (s3FileName, towAndGoData) {
    // Initialize TowAndGoService with filename
    // Upload data to S3 storage
  }
};
```

## Input Parameters

### s3FileName (String)
- **Purpose**: Specifies the target filename for S3 storage
- **Format**: String identifier for the uploaded file
- **Usage**: Used to initialize TowAndGoService instance
- **Required**: Yes

### towAndGoData (String)
- **Purpose**: JSON string containing traffic data to be uploaded
- **Format**: Stringified JSON with specific structure
- **Required**: Yes

## Data Structure Format

### Expected JSON Structure
```javascript
{
  "last_modified": 1684216515,
  "tow_and_go": [
    {
      "link_id": 17806054,
      "segment_id": 457160414
    },
    {
      "link_id": 17857682,
      "segment_id": 414984019
    },
    {
      "link_id": 17857686,
      "segment_id": null  // Supports null segment IDs
    }
  ]
}
```

### Data Components
- **last_modified**: Unix timestamp indicating when data was last updated
- **tow_and_go**: Array of traffic link objects
- **link_id**: Unique identifier for traffic link
- **segment_id**: Associated segment identifier (can be null)

## Processing Logic

### Main Execution Flow
1. **Service Initialization**: Create TowAndGoService instance with provided filename
2. **Data Upload**: Execute S3 upload using service method
3. **Completion**: Process completes with uploaded data available in S3

### Service Integration
```javascript
const towAndGoService = new TowAndGoService(s3FileName);
await towAndGoService.uploadTowAndGoDataToS3(towAndGoData);
```

## Service Architecture

### TowAndGoService Integration
- **Constructor**: Accepts filename parameter for S3 target identification
- **Upload Method**: `uploadTowAndGoDataToS3()` handles the actual S3 upload process
- **Data Processing**: Service manages JSON parsing and S3 client operations
- **Error Handling**: Service-level error management for upload failures

## S3 Storage Implementation

### Upload Process
- Data is uploaded to designated S3 bucket
- Filename specified via s3FileName parameter
- JSON data converted and stored as S3 object
- Supports large datasets with multiple traffic links

### Data Persistence
- Uploaded data becomes available for downstream processing
- S3 storage enables scalable data access
- Supports data synchronization with MongoDB
- Facilitates analytics and reporting workflows

## Error Handling Strategy
- Service-level error management within TowAndGoService
- S3 upload failures are handled by the underlying service
- Input validation occurs at service layer
- Comprehensive error logging through service implementation

## Use Cases

### Real-Time Traffic Data Upload
- Process incoming traffic link information
- Store current traffic conditions for analysis
- Support incident management workflows
- Enable traffic pattern recognition

### Data Pipeline Integration
- First stage in Tow and Go data processing pipeline
- Prepares data for MongoDB synchronization
- Supports batch and real-time processing modes
- Enables data archival and historical analysis

## Performance Considerations
- Lightweight job with minimal processing overhead
- S3 upload performance depends on data size and network conditions
- Service architecture enables efficient data handling
- Scalable design supports varying data volumes

## Integration Points
- **TowAndGoService**: Primary service for data upload operations
- **AWS S3**: Target storage platform for traffic data
- **Data Pipeline**: Feeds into MongoDB synchronization process
- **Traffic Systems**: Receives data from external traffic monitoring

## Configuration Requirements
- S3 bucket configuration within TowAndGoService
- AWS credentials and permissions for S3 access
- Network connectivity to AWS services
- Proper IAM roles for S3 upload operations

## Data Flow Architecture
```
Traffic Sources → Job Input → TowAndGoService → AWS S3 → MongoDB Sync
```

## Monitoring and Logging
- Service-level logging for upload operations
- S3 upload success/failure tracking
- Data integrity verification
- Performance metrics collection

## Security Considerations
- Secure handling of traffic data during upload
- AWS IAM-based access control for S3 operations
- Data encryption in transit and at rest
- Compliance with data privacy requirements

## Deployment Notes
- Requires AWS S3 access credentials
- Service dependencies must be properly configured
- Network connectivity to AWS services required
- Compatible with containerized deployment environments

## Future Enhancements
- Support for data compression before upload
- Batch upload optimization for large datasets
- Enhanced error recovery and retry mechanisms
- Advanced monitoring and alerting capabilities
- Support for multiple S3 destinations