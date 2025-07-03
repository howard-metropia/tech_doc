# TSP Job Service - AWS Configuration

## Overview

The `config/vendor/aws.js` file manages Amazon Web Services (AWS) configuration for the TSP Job service's cloud infrastructure integration. This configuration provides access to essential AWS services including Simple Queue Service (SQS) for message queuing and Simple Storage Service (S3) for object storage.

## File Information

- **File Path**: `/config/vendor/aws.js`
- **File Type**: JavaScript Configuration Module
- **Primary Purpose**: AWS services configuration for cloud infrastructure integration
- **Dependencies**: Environment variables for AWS credentials and service endpoints

## Configuration Structure

```javascript
module.exports = {
  region: process.env.AWS_REGION,
  sqs: {
    queueUrl: process.env.AWS_SQS_QUEUE_URL,
  },
  s3: {
    bucketName: process.env.AWS_S3_BUCKET_NAME,
  },
};
```

## Configuration Components

### 1. Regional Configuration
```javascript
region: process.env.AWS_REGION
```

**Purpose**: Specifies the AWS region for all service operations
- **Common Values**: `us-east-1`, `us-west-2`, `eu-west-1`, `ap-southeast-1`
- **Impact**: Affects latency, compliance, and data sovereignty
- **Usage**: Applied to all AWS service clients for consistent regional deployment

**Regional Considerations**:
- Latency optimization based on user geographic distribution
- Compliance requirements for data residency
- Service availability and disaster recovery planning
- Cost optimization through regional pricing differences

### 2. Simple Queue Service (SQS) Configuration
```javascript
sqs: {
  queueUrl: process.env.AWS_SQS_QUEUE_URL,
}
```

**Purpose**: Message queuing service for asynchronous job processing
- **Queue URL**: Complete SQS queue endpoint for message operations
- **Message Processing**: Handles background job distribution and processing
- **Scalability**: Enables horizontal scaling of job workers

**Use Cases**:
- Background job processing (incentive calculations, report generation)
- Asynchronous task distribution across multiple workers
- Decoupling of service components for improved reliability
- Dead letter queue handling for failed message processing
- Message ordering and deduplication for critical operations

### 3. Simple Storage Service (S3) Configuration
```javascript
s3: {
  bucketName: process.env.AWS_S3_BUCKET_NAME,
}
```

**Purpose**: Object storage service for file management and data archival
- **Bucket Name**: S3 bucket identifier for file operations
- **Object Storage**: Handles document storage, reports, and media files
- **Durability**: Provides 99.999999999% (11 9's) durability

**Use Cases**:
- Trip documentation and receipt storage
- Analytics report file storage
- User-generated content (profile pictures, trip photos)
- Data backup and archival
- Static asset hosting for web applications

## AWS Service Integration

### SQS Implementation
```javascript
const AWS = require('aws-sdk');
const config = require('../config/vendor/aws');

// Configure AWS SDK
AWS.config.update({
  region: config.region,
  accessKeyId: process.env.AWS_ACCESS_KEY_ID,
  secretAccessKey: process.env.AWS_SECRET_ACCESS_KEY
});

const sqs = new AWS.SQS();

class SQSManager {
  static async sendMessage(messageBody, messageAttributes = {}) {
    const params = {
      QueueUrl: config.sqs.queueUrl,
      MessageBody: JSON.stringify(messageBody),
      MessageAttributes: messageAttributes
    };
    
    try {
      const result = await sqs.sendMessage(params).promise();
      return {
        success: true,
        messageId: result.MessageId,
        md5: result.MD5OfBody
      };
    } catch (error) {
      console.error('SQS send message error:', error);
      throw error;
    }
  }
  
  static async receiveMessages(maxMessages = 10, waitTimeSeconds = 20) {
    const params = {
      QueueUrl: config.sqs.queueUrl,
      MaxNumberOfMessages: maxMessages,
      WaitTimeSeconds: waitTimeSeconds,
      MessageAttributeNames: ['All']
    };
    
    try {
      const result = await sqs.receiveMessage(params).promise();
      return result.Messages || [];
    } catch (error) {
      console.error('SQS receive message error:', error);
      throw error;
    }
  }
  
  static async deleteMessage(receiptHandle) {
    const params = {
      QueueUrl: config.sqs.queueUrl,
      ReceiptHandle: receiptHandle
    };
    
    try {
      await sqs.deleteMessage(params).promise();
      return { success: true };
    } catch (error) {
      console.error('SQS delete message error:', error);
      throw error;
    }
  }
  
  static async sendBatchMessages(messages) {
    const entries = messages.map((message, index) => ({
      Id: index.toString(),
      MessageBody: JSON.stringify(message.body),
      MessageAttributes: message.attributes || {}
    }));
    
    const params = {
      QueueUrl: config.sqs.queueUrl,
      Entries: entries
    };
    
    try {
      const result = await sqs.sendMessageBatch(params).promise();
      return {
        successful: result.Successful,
        failed: result.Failed
      };
    } catch (error) {
      console.error('SQS batch send error:', error);
      throw error;
    }
  }
  
  static async getQueueAttributes() {
    const params = {
      QueueUrl: config.sqs.queueUrl,
      AttributeNames: ['All']
    };
    
    try {
      const result = await sqs.getQueueAttributes(params).promise();
      return result.Attributes;
    } catch (error) {
      console.error('SQS get attributes error:', error);
      throw error;
    }
  }
}
```

### S3 Implementation
```javascript
const s3 = new AWS.S3();

class S3Manager {
  static async uploadFile(key, body, contentType = 'application/octet-stream', metadata = {}) {
    const params = {
      Bucket: config.s3.bucketName,
      Key: key,
      Body: body,
      ContentType: contentType,
      Metadata: metadata,
      ServerSideEncryption: 'AES256'
    };
    
    try {
      const result = await s3.upload(params).promise();
      return {
        success: true,
        location: result.Location,
        etag: result.ETag,
        key: result.Key
      };
    } catch (error) {
      console.error('S3 upload error:', error);
      throw error;
    }
  }
  
  static async downloadFile(key) {
    const params = {
      Bucket: config.s3.bucketName,
      Key: key
    };
    
    try {
      const result = await s3.getObject(params).promise();
      return {
        body: result.Body,
        contentType: result.ContentType,
        lastModified: result.LastModified,
        metadata: result.Metadata
      };
    } catch (error) {
      console.error('S3 download error:', error);
      throw error;
    }
  }
  
  static async deleteFile(key) {
    const params = {
      Bucket: config.s3.bucketName,
      Key: key
    };
    
    try {
      await s3.deleteObject(params).promise();
      return { success: true };
    } catch (error) {
      console.error('S3 delete error:', error);
      throw error;
    }
  }
  
  static async listFiles(prefix = '', maxKeys = 1000) {
    const params = {
      Bucket: config.s3.bucketName,
      Prefix: prefix,
      MaxKeys: maxKeys
    };
    
    try {
      const result = await s3.listObjectsV2(params).promise();
      return {
        objects: result.Contents,
        count: result.KeyCount,
        isTruncated: result.IsTruncated,
        nextToken: result.NextContinuationToken
      };
    } catch (error) {
      console.error('S3 list error:', error);
      throw error;
    }
  }
  
  static async generatePresignedUrl(key, expiresIn = 3600) {
    const params = {
      Bucket: config.s3.bucketName,
      Key: key,
      Expires: expiresIn
    };
    
    try {
      const url = await s3.getSignedUrlPromise('getObject', params);
      return { url, expiresIn };
    } catch (error) {
      console.error('S3 presigned URL error:', error);
      throw error;
    }
  }
  
  static async copyFile(sourceKey, destinationKey) {
    const params = {
      Bucket: config.s3.bucketName,
      CopySource: `${config.s3.bucketName}/${sourceKey}`,
      Key: destinationKey
    };
    
    try {
      const result = await s3.copyObject(params).promise();
      return {
        success: true,
        etag: result.ETag,
        lastModified: result.LastModified
      };
    } catch (error) {
      console.error('S3 copy error:', error);
      throw error;
    }
  }
}
```

## Job Processing Integration

### SQS-Based Job Queue
```javascript
class JobProcessor {
  static async enqueueJob(jobType, jobData, priority = 0) {
    const message = {
      jobId: `${jobType}_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`,
      jobType: jobType,
      payload: jobData,
      priority: priority,
      createdAt: new Date().toISOString(),
      retryCount: 0
    };
    
    const messageAttributes = {
      jobType: {
        DataType: 'String',
        StringValue: jobType
      },
      priority: {
        DataType: 'Number',
        StringValue: priority.toString()
      }
    };
    
    return await SQSManager.sendMessage(message, messageAttributes);
  }
  
  static async processJobs() {
    while (true) {
      try {
        const messages = await SQSManager.receiveMessages(10, 20);
        
        if (messages.length === 0) {
          continue;
        }
        
        for (const message of messages) {
          try {
            const jobData = JSON.parse(message.Body);
            await this.executeJob(jobData);
            await SQSManager.deleteMessage(message.ReceiptHandle);
          } catch (jobError) {
            console.error('Job execution error:', jobError);
            // Handle failed job (dead letter queue, retry logic, etc.)
            await this.handleFailedJob(message, jobError);
          }
        }
      } catch (error) {
        console.error('Job processing error:', error);
        await new Promise(resolve => setTimeout(resolve, 5000)); // Wait 5 seconds before retry
      }
    }
  }
  
  static async executeJob(jobData) {
    const { jobType, payload } = jobData;
    
    switch (jobType) {
      case 'generate-report':
        return await this.generateReport(payload);
      case 'process-trip':
        return await this.processTrip(payload);
      case 'send-notification':
        return await this.sendNotification(payload);
      default:
        throw new Error(`Unknown job type: ${jobType}`);
    }
  }
  
  static async generateReport(payload) {
    // Generate report logic
    const report = await createReport(payload);
    
    // Upload report to S3
    const reportKey = `reports/${payload.userId}/${payload.reportId}.pdf`;
    await S3Manager.uploadFile(reportKey, report.buffer, 'application/pdf', {
      userId: payload.userId,
      reportType: payload.reportType,
      generatedAt: new Date().toISOString()
    });
    
    return { reportKey, size: report.buffer.length };
  }
}
```

### File Management Integration
```javascript
class FileManager {
  static async storeUserDocument(userId, documentType, fileBuffer, fileName) {
    const fileExtension = fileName.split('.').pop();
    const key = `users/${userId}/documents/${documentType}/${Date.now()}.${fileExtension}`;
    
    const result = await S3Manager.uploadFile(key, fileBuffer, this.getContentType(fileExtension), {
      userId: userId,
      documentType: documentType,
      originalFileName: fileName,
      uploadedAt: new Date().toISOString()
    });
    
    return {
      fileId: key,
      url: await S3Manager.generatePresignedUrl(key, 86400), // 24 hours
      ...result
    };
  }
  
  static async getUserDocuments(userId, documentType = null) {
    const prefix = documentType 
      ? `users/${userId}/documents/${documentType}/`
      : `users/${userId}/documents/`;
    
    const result = await S3Manager.listFiles(prefix);
    
    const documents = await Promise.all(
      result.objects.map(async (obj) => {
        const url = await S3Manager.generatePresignedUrl(obj.Key, 3600);
        return {
          key: obj.Key,
          size: obj.Size,
          lastModified: obj.LastModified,
          url: url.url
        };
      })
    );
    
    return documents;
  }
  
  static getContentType(extension) {
    const contentTypes = {
      'pdf': 'application/pdf',
      'jpg': 'image/jpeg',
      'jpeg': 'image/jpeg',
      'png': 'image/png',
      'gif': 'image/gif',
      'doc': 'application/msword',
      'docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
      'txt': 'text/plain'
    };
    
    return contentTypes[extension.toLowerCase()] || 'application/octet-stream';
  }
}
```

## Performance Optimization

### Connection Management
```javascript
// Optimize AWS SDK configuration
AWS.config.update({
  region: config.region,
  maxRetries: 3,
  retryDelayOptions: {
    customBackoff: function(retryCount) {
      return Math.pow(2, retryCount) * 100;
    }
  },
  httpOptions: {
    timeout: 30000,
    connectTimeout: 5000
  }
});

// SQS optimization
const optimizedSQS = new AWS.SQS({
  maxRetries: 3,
  retryDelayOptions: {
    base: 300
  }
});

// S3 optimization with transfer acceleration
const optimizedS3 = new AWS.S3({
  useAccelerateEndpoint: true,
  signatureVersion: 'v4',
  s3DisableBodySigning: false
});
```

### Batch Operations
```javascript
class BatchOperations {
  static async batchUploadFiles(files) {
    const uploadPromises = files.map(file => 
      S3Manager.uploadFile(file.key, file.body, file.contentType, file.metadata)
    );
    
    const results = await Promise.allSettled(uploadPromises);
    
    return {
      successful: results.filter(r => r.status === 'fulfilled').map(r => r.value),
      failed: results.filter(r => r.status === 'rejected').map(r => r.reason)
    };
  }
  
  static async batchProcessMessages(messages) {
    const chunks = [];
    for (let i = 0; i < messages.length; i += 10) {
      chunks.push(messages.slice(i, i + 10));
    }
    
    const results = [];
    for (const chunk of chunks) {
      const result = await SQSManager.sendBatchMessages(chunk);
      results.push(result);
    }
    
    return results;
  }
}
```

## Monitoring and Health Checks

### Service Health Monitoring
```javascript
class AWSHealthMonitor {
  static async checkSQSHealth() {
    try {
      const start = Date.now();
      const attributes = await SQSManager.getQueueAttributes();
      const latency = Date.now() - start;
      
      return {
        status: 'healthy',
        latency: latency,
        queueDepth: parseInt(attributes.ApproximateNumberOfMessages),
        messagesInFlight: parseInt(attributes.ApproximateNumberOfMessagesNotVisible),
        oldestMessage: attributes.ApproximateAgeOfOldestMessage
      };
    } catch (error) {
      return {
        status: 'unhealthy',
        error: error.message
      };
    }
  }
  
  static async checkS3Health() {
    try {
      const start = Date.now();
      await s3.headBucket({ Bucket: config.s3.bucketName }).promise();
      const latency = Date.now() - start;
      
      const listResult = await S3Manager.listFiles('', 1);
      
      return {
        status: 'healthy',
        latency: latency,
        bucket: config.s3.bucketName,
        objectCount: listResult.count,
        accessible: true
      };
    } catch (error) {
      return {
        status: 'unhealthy',
        error: error.message,
        bucket: config.s3.bucketName
      };
    }
  }
  
  static async getAWSStatus() {
    const [sqsHealth, s3Health] = await Promise.all([
      this.checkSQSHealth(),
      this.checkS3Health()
    ]);
    
    return {
      region: config.region,
      services: {
        sqs: sqsHealth,
        s3: s3Health
      },
      overall: sqsHealth.status === 'healthy' && s3Health.status === 'healthy' 
        ? 'healthy' 
        : 'degraded'
    };
  }
}
```

### Cost Monitoring
```javascript
class AWSCostMonitor {
  static async estimateS3Costs(operations) {
    // Simplified cost estimation
    const pricing = {
      storage: 0.023, // per GB per month
      requests: {
        put: 0.0005, // per 1000 requests
        get: 0.0004  // per 1000 requests
      },
      dataTransfer: 0.09 // per GB out to internet
    };
    
    const costs = {
      storage: (operations.storageGB || 0) * pricing.storage,
      putRequests: (operations.putRequests || 0) / 1000 * pricing.requests.put,
      getRequests: (operations.getRequests || 0) / 1000 * pricing.requests.get,
      dataTransfer: (operations.dataTransferGB || 0) * pricing.dataTransfer
    };
    
    return {
      breakdown: costs,
      total: Object.values(costs).reduce((sum, cost) => sum + cost, 0)
    };
  }
  
  static async estimateSQSCosts(messageCount) {
    const costPerMillion = 0.40;
    return (messageCount / 1000000) * costPerMillion;
  }
}
```

## Security Configuration

### IAM and Access Control
```javascript
// Example IAM policy requirements (not in code, but documentation)
const requiredIAMPolicy = {
  Version: '2012-10-17',
  Statement: [
    {
      Effect: 'Allow',
      Action: [
        'sqs:SendMessage',
        'sqs:ReceiveMessage',
        'sqs:DeleteMessage',
        'sqs:GetQueueAttributes'
      ],
      Resource: process.env.AWS_SQS_QUEUE_ARN
    },
    {
      Effect: 'Allow',
      Action: [
        's3:GetObject',
        's3:PutObject',
        's3:DeleteObject',
        's3:ListBucket'
      ],
      Resource: [
        `arn:aws:s3:::${config.s3.bucketName}`,
        `arn:aws:s3:::${config.s3.bucketName}/*`
      ]
    }
  ]
};

// Encryption configuration
const encryptionConfig = {
  s3: {
    ServerSideEncryption: 'AES256',
    // or for KMS encryption:
    // ServerSideEncryption: 'aws:kms',
    // SSEKMSKeyId: process.env.AWS_KMS_KEY_ID
  },
  sqs: {
    // SQS encryption is configured at queue level
    KmsMasterKeyId: process.env.AWS_SQS_KMS_KEY_ID
  }
};
```

This AWS configuration provides a robust foundation for cloud service integration in the TSP Job service, enabling scalable message processing through SQS and reliable file storage through S3, with comprehensive monitoring, security, and cost management capabilities.