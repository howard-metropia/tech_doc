# Storage Helper

## Overview
**File**: `src/helpers/storage.js`  
**Type**: Cloud Storage Utility  
**Purpose**: Provides AWS S3 integration for file upload and JSON data retrieval

## Class Structure

### StorageS3 Class
```javascript
class StorageS3 {
  constructor() {
    this.s3Client = new S3Client({ region: awsConfig.region });
    this.s3BucketName = awsConfig.s3.bucketName;
  }
}
```

## Core Methods

### File Upload
```javascript
async uploadFileContentToS3File(fileName, fileContent) {
  const objBuffer = Buffer.from(fileContent);
  const params = {
    Bucket: this.s3BucketName,
    Key: fileName,
    Body: objBuffer,
    ContentType: "application/json",
  };
  // Upload to S3 and return result
}
```

### JSON Data Retrieval
```javascript
async getJsonDataFromS3(s3JsonFileKeyName) {
  // Download file from S3
  // Convert stream to string
  // Parse JSON and return
}
```

## Configuration

### AWS Setup
- **S3Client**: Uses AWS SDK v3
- **Region**: From AWS configuration
- **Bucket**: Configured bucket name

### Dependencies
```javascript
const { S3Client, PutObjectCommand, GetObjectCommand } = require("@aws-sdk/client-s3");
const config = require('config');
const awsConfig = config.get('vendor.aws');
```

## Upload Functionality

### File Content Upload
- **Input**: fileName (string), fileContent (string)
- **Processing**: Converts content to Buffer
- **Content-Type**: Fixed as "application/json"
- **Output**: S3 upload result

### Upload Parameters
```javascript
{
  Bucket: this.s3BucketName,
  Key: fileName,
  Body: objBuffer,
  ContentType: "application/json",
}
```

## Download Functionality

### Stream Processing
```javascript
const streamToString = (stream) => new Promise((resolve, reject) => {
  const chunks = [];
  stream.on('data', (chunk) => chunks.push(chunk));
  stream.on('error', reject);
  stream.on('end', () => resolve(Buffer.concat(chunks).toString('utf-8')));
});
```

### JSON Parsing
- **Stream Conversion**: Converts ReadableStream to string
- **JSON Parsing**: Parses string to JavaScript object
- **Error Handling**: Returns null on failure

## Error Handling

### Upload Errors
```javascript
try {
  const result = await this.s3Client.send(command);
  return result;
} catch (error) {
  logger.error(`Error uploading file: ${error}`);
  throw new MaasError(
    ERROR_CODE.ERROR_THIRD_PARTY_FAILED,
    'warn',
    'ERROR_THIRD_PARTY_FAILED',
    200,
  );
}
```

### Download Errors
```javascript
try {
  const response = await this.s3Client.send(command);
  // Process response
} catch (error) {
  logger.error(`Error reading S3 file (${s3JsonFileKeyName}): ${error}`);
  return null;
}
```

## Usage Examples

### File Upload
```javascript
const { StorageS3 } = require('./storage');

const storage = new StorageS3();
const jsonData = JSON.stringify({ key: 'value' });

const result = await storage.uploadFileContentToS3File(
  'data/file.json',
  jsonData
);
```

### JSON Retrieval
```javascript
const storage = new StorageS3();

const data = await storage.getJsonDataFromS3('data/config.json');
if (data) {
  console.log('Retrieved data:', data);
} else {
  console.log('File not found or invalid JSON');
}
```

### Error Handling Usage
```javascript
try {
  await storage.uploadFileContentToS3File('test.json', content);
  console.log('Upload successful');
} catch (error) {
  if (error instanceof MaasError) {
    console.log('AWS S3 error:', error.message);
  }
}
```

## Dependencies

### AWS SDK
- **@aws-sdk/client-s3**: S3 operations
- **Version**: AWS SDK v3
- **Commands**: PutObjectCommand, GetObjectCommand

### Internal Dependencies
- **config**: Configuration management
- **@maas/core**: Error handling (MaasError)
- **@maas/core/log**: Logging functionality

## Configuration Requirements

### AWS Configuration
```javascript
vendor: {
  aws: {
    region: 'us-east-1',
    s3: {
      bucketName: 'your-bucket-name'
    }
  }
}
```

### Environment Variables
- **AWS_ACCESS_KEY_ID**: AWS access credentials
- **AWS_SECRET_ACCESS_KEY**: AWS secret credentials
- **AWS_REGION**: Optional, can use config instead

## Performance Considerations

### Stream Processing
- **Memory Efficient**: Streams large files without loading entirely
- **Chunk Processing**: Processes data in chunks
- **UTF-8 Encoding**: Specific to text/JSON files

### Instantiation
- **Per-Operation**: New instance per operation
- **Connection Reuse**: S3 client reuses connections
- **Regional**: Uses single region configuration

## Limitations

### Content Type
- **Fixed Type**: Always sets "application/json"
- **Text Files Only**: Designed for JSON/text content
- **No Binary**: Not suitable for binary files

### Error Recovery
- **No Retry**: No automatic retry logic
- **Null Returns**: Download failures return null
- **Exception Throwing**: Upload failures throw exceptions

## Security Considerations

### Access Control
- **IAM Permissions**: Requires appropriate S3 permissions
- **Bucket Policies**: Should implement bucket-level security
- **Encryption**: No client-side encryption implemented

### Data Privacy
- **File Names**: Logged in error messages
- **Content**: JSON content may contain sensitive data
- **Access Logs**: Consider S3 access logging

## Integration Points

### Common Use Cases
- **Configuration Storage**: Application configuration files
- **Data Backup**: Backup application data
- **Cache Storage**: Storing computed results
- **Report Generation**: Storing generated reports

### Service Integration
- **Job Processing**: Store job results
- **Data Pipeline**: Intermediate data storage
- **Analytics**: Export data for analysis

## Testing

### Unit Tests
```javascript
// Mock AWS S3 Client
jest.mock('@aws-sdk/client-s3');

const mockSend = jest.fn();
S3Client.mockImplementation(() => ({ send: mockSend }));
```

### Integration Tests
- **Real S3**: Test against actual S3 instance
- **Permissions**: Verify upload/download permissions
- **Error Cases**: Test network failures, invalid files

## Monitoring

### Metrics to Track
- **Upload Success Rate**: Successful uploads vs failures
- **Download Success Rate**: Successful retrievals vs failures
- **File Sizes**: Monitor uploaded file sizes
- **Performance**: Upload/download times

### Logging
- **Error Logging**: Detailed error information
- **Operation Logging**: Track S3 operations
- **Performance Logging**: Operation duration

## Best Practices

### File Naming
- **Consistent Structure**: Use consistent file naming patterns
- **Path Organization**: Organize files in logical directory structure
- **Unique Names**: Avoid file name collisions

### Content Management
- **JSON Validation**: Validate JSON before upload
- **Size Limits**: Consider file size limitations
- **Compression**: Consider compression for large files

## Future Enhancements

### Potential Improvements
- **Content Type Detection**: Automatic content type detection
- **Binary Support**: Support for binary file uploads
- **Retry Logic**: Automatic retry for failed operations
- **Streaming Upload**: Support for large file streaming

### Advanced Features
- **Encryption**: Client-side encryption support
- **Compression**: Automatic compression/decompression
- **Metadata**: Custom metadata support
- **Versioning**: S3 versioning integration