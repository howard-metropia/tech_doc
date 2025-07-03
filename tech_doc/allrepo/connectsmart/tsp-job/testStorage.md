# AWS S3 Storage Service Test Suite

## Overview
Focused test suite for the AWS S3 storage service that validates cloud storage operations including file upload, content retrieval, and JSON data management. This test ensures reliable integration with AWS S3 for persistent file storage and data management within the TSP Job system.

## File Location
`/test/testStorage.js`

## Technical Analysis

### Core Service Under Test
```javascript
const { StorageS3 } = require('@app/src/helpers/storage');
const storage = new StorageS3();
```

The StorageS3 helper class provides a simplified interface for AWS S3 operations, abstracting complex S3 SDK interactions into convenient methods for file management.

### Dependencies
- `chai` - Assertion library with expect interface for validation
- `@app/src/helpers/storage` - Custom S3 storage helper implementation
- AWS S3 SDK (implicitly) - Amazon Web Services S3 client library

### Test Architecture

#### Storage Instance Creation
```javascript
const storage = new StorageS3();
```

Creates a configured S3 storage instance using environment-based AWS credentials and bucket configuration.

#### Extended Timeout Configuration
```javascript
}, 10000);  // 10 second timeout for S3 operations
```

Accounts for network latency and S3 response times, ensuring tests don't fail due to normal cloud service delays.

### S3 Operations Testing

#### File Upload and Retrieval Workflow
```javascript
describe('uploadFileContentToS3File', () => {
  it('should access S3 bucket successfully', async () => {
    const jsonFileName = "S3-upload-test-file.json";
    const jsonContent = '{"hello": "world!"}';
    
    // Upload operation
    const uploadResult = await storage.uploadFileContentToS3File(jsonFileName, jsonContent);
    expect(uploadResult.$metadata.httpStatusCode).be.equal(200);
    
    // Retrieval operation
    const uploadedContent = await storage.getJsonDataFromS3(jsonFileName);
    expect(uploadedContent).to.deep.equal(JSON.parse(jsonContent));
  }, 10000);
});
```

This comprehensive test validates the complete upload-retrieve cycle ensuring data integrity and proper S3 integration.

## Usage/Integration

### File Upload Operations
```javascript
// Upload string content as file
const uploadResult = await storage.uploadFileContentToS3File(
  'data/report-2024.json',           // S3 key/filename
  JSON.stringify(reportData)         // File content as string
);

// Verify successful upload
if (uploadResult.$metadata.httpStatusCode === 200) {
  console.log('File uploaded successfully');
}
```

### JSON Data Retrieval
```javascript
// Retrieve and parse JSON data
const jsonData = await storage.getJsonDataFromS3('data/report-2024.json');
console.log('Retrieved data:', jsonData);

// Direct object comparison
expect(jsonData).to.deep.equal(originalData);
```

### Error Handling Pattern
```javascript
try {
  const result = await storage.uploadFileContentToS3File(filename, content);
  return result;
} catch (error) {
  if (error.code === 'NoSuchBucket') {
    console.error('S3 bucket does not exist');
  } else if (error.code === 'AccessDenied') {
    console.error('Insufficient S3 permissions');
  } else {
    console.error('S3 operation failed:', error.message);
  }
  throw error;
}
```

## Code Examples

### Basic File Operations
```javascript
describe('S3 File Management', () => {
  const storage = new StorageS3();
  
  it('should handle various file types', async () => {
    // Upload text file
    const textResult = await storage.uploadFileContentToS3File(
      'test-files/sample.txt',
      'This is a test file'
    );
    expect(textResult.$metadata.httpStatusCode).to.equal(200);
    
    // Upload JSON data
    const jsonData = { users: [{ id: 1, name: 'John' }] };
    const jsonResult = await storage.uploadFileContentToS3File(
      'test-files/data.json',
      JSON.stringify(jsonData, null, 2)
    );
    expect(jsonResult.$metadata.httpStatusCode).to.equal(200);
    
    // Retrieve and validate JSON
    const retrievedData = await storage.getJsonDataFromS3('test-files/data.json');
    expect(retrievedData).to.deep.equal(jsonData);
  });
});
```

### Batch File Operations
```javascript
describe('Batch S3 Operations', () => {
  it('should handle multiple file uploads', async () => {
    const storage = new StorageS3();
    const files = [
      { name: 'file1.json', content: '{"test": 1}' },
      { name: 'file2.json', content: '{"test": 2}' },
      { name: 'file3.json', content: '{"test": 3}' }
    ];
    
    // Upload all files
    const uploadPromises = files.map(file => 
      storage.uploadFileContentToS3File(`batch/${file.name}`, file.content)
    );
    const uploadResults = await Promise.all(uploadPromises);
    
    // Verify all uploads succeeded
    uploadResults.forEach(result => {
      expect(result.$metadata.httpStatusCode).to.equal(200);
    });
    
    // Retrieve and validate all files
    const retrievePromises = files.map(file =>
      storage.getJsonDataFromS3(`batch/${file.name}`)
    );
    const retrievedData = await Promise.all(retrievePromises);
    
    // Validate content integrity
    retrievedData.forEach((data, index) => {
      expect(data).to.deep.equal(JSON.parse(files[index].content));
    });
  });
});
```

### Content Type Handling
```javascript
describe('Content Type Management', () => {
  it('should handle different content types', async () => {
    const storage = new StorageS3();
    
    // Upload with explicit content type
    const csvContent = 'name,age\nJohn,30\nJane,25';
    const csvResult = await storage.uploadFileContentToS3File(
      'data/users.csv',
      csvContent,
      'text/csv'
    );
    expect(csvResult.$metadata.httpStatusCode).to.equal(200);
    
    // Upload binary data (base64 encoded)
    const imageData = 'iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChwGA60e6kgAAAABJRU5ErkJggg==';
    const imageResult = await storage.uploadFileContentToS3File(
      'images/test.png',
      imageData,
      'image/png',
      'base64'
    );
    expect(imageResult.$metadata.httpStatusCode).to.equal(200);
  });
});
```

### Storage Configuration Testing
```javascript
describe('Storage Configuration', () => {
  it('should use correct bucket and region', async () => {
    const storage = new StorageS3();
    
    // Test with environment-specific configuration
    const testFile = `config-test-${Date.now()}.json`;
    const testData = { 
      environment: process.env.NODE_ENV,
      timestamp: new Date().toISOString()
    };
    
    const uploadResult = await storage.uploadFileContentToS3File(
      testFile,
      JSON.stringify(testData)
    );
    
    expect(uploadResult.$metadata.httpStatusCode).to.equal(200);
    expect(uploadResult.$metadata.attempts).to.be.at.least(1);
    
    // Verify data integrity
    const retrievedData = await storage.getJsonDataFromS3(testFile);
    expect(retrievedData.environment).to.equal(process.env.NODE_ENV);
  });
});
```

## Integration Points

### AWS S3 Service Integration
- **Bucket Management**: Configured S3 bucket access with proper permissions
- **Authentication**: AWS IAM roles and credentials for secure access
- **Region Configuration**: Optimized region selection for performance
- **Error Handling**: Comprehensive AWS service error management

### Application Data Management
- **Configuration Storage**: Environment-specific configuration files
- **Report Generation**: Automated report file storage and retrieval
- **Backup Operations**: Data backup and archival capabilities
- **Content Distribution**: File serving for web applications

### Security and Access Control
- **IAM Permissions**: Least-privilege access configuration
- **Encryption**: Server-side encryption for sensitive data
- **Access Logging**: S3 access logging for audit trails
- **Cross-Origin Resource Sharing**: CORS configuration for web access

### Performance Optimization
- **Transfer Acceleration**: S3 Transfer Acceleration for global access
- **Multipart Uploads**: Efficient handling of large files
- **Caching Strategies**: CloudFront integration for content delivery
- **Compression**: Automatic compression for text-based files

### Monitoring and Maintenance
- **CloudWatch Integration**: Monitoring storage usage and performance
- **Lifecycle Policies**: Automated data archival and cleanup
- **Versioning**: File version management and rollback capabilities
- **Cost Optimization**: Storage class optimization for different data types

This test suite ensures the S3 storage service provides reliable, performant cloud storage capabilities that integrate seamlessly with the TSP Job system's file management requirements while maintaining data integrity and proper error handling.