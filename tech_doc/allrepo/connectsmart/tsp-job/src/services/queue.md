# Queue Service

## Overview

The Queue service provides AWS SQS integration for asynchronous task processing, enabling reliable message delivery for notifications and background job processing.

## Service Information

- **Service Name**: Queue
- **File Path**: `/src/services/queue.js`
- **Type**: Message Queue Service
- **Dependencies**: AWS SDK, SQS

## Configuration

### AWS Setup
- **Region**: Configured from vendor.aws.region setting
- **Queue URL**: Specified in vendor.aws.sqs.queueUrl
- **Client**: AWS SQS v3 client with regional configuration

### SQS Client
```javascript
const client = new SQSClient({ region: awsConfig.region });
```

## Functions

### sendTask(action, data)

Sends asynchronous tasks to AWS SQS queue for background processing.

**Purpose**: Queues tasks for asynchronous execution by worker processes
**Parameters**:
- `action` (string): Task type identifier for worker routing
- `data` (object): Task payload containing processing information

**Returns**: Promise (logs response status)

**Message Structure**:
```javascript
const message = {
  action,    // Task type (e.g., 'cloud_message')
  data,      // Task payload
};
```

**Example**:
```javascript
await sendTask('cloud_message', {
  user_list: [12345],
  title: "Notification Title",
  body: "Message content",
  notification_type: 68
});
```

## Message Processing

### Task Structure
- **Action Field**: Determines worker task routing
- **Data Field**: Contains all task-specific information
- **JSON Serialization**: Automatic message body conversion

### Common Actions
- **cloud_message**: Push notification delivery
- **email_notification**: Email sending tasks
- **data_processing**: Background data analysis
- **report_generation**: Scheduled report creation

## AWS SQS Integration

### Message Delivery
- **Queue URL**: Configured SQS queue endpoint
- **Message Body**: JSON-serialized task data
- **Delivery Guarantee**: AWS SQS reliability features
- **Error Handling**: AWS SDK automatic retry logic

### Response Handling
- **Status Logging**: HTTP response code tracking
- **Success Confirmation**: 200 status code verification
- **Error Recovery**: Comprehensive error logging
- **Metadata Access**: AWS response metadata

## Error Handling

### SQS Failures
- **Network Issues**: AWS SDK handles connection problems
- **Authentication**: IAM permission validation
- **Queue Availability**: Service health checks
- **Message Size**: AWS SQS limits compliance

### Logging
- **Success Logging**: HTTP status code confirmation
- **Error Details**: Complete error message capture
- **Context Preservation**: Action and data logging
- **Debug Information**: AWS response metadata

### Recovery Mechanisms
- **AWS Retry Logic**: Built-in SDK retry handling
- **Error Propagation**: Calling service error handling
- **Queue Health**: Automatic AWS service recovery

## Integration Points

### Used By
- Send notification service
- Background job processors
- Scheduled task systems
- Event-driven workflows

### Worker Processes
- **Task Routing**: Action-based worker selection
- **Message Processing**: Queue consumer applications
- **Error Handling**: Dead letter queue support
- **Scaling**: Auto-scaling based on queue depth

## Performance Considerations

### Message Throughput
- **AWS SQS Limits**: Standard queue performance
- **Batch Operations**: Single message delivery
- **Concurrent Processing**: Multiple worker support
- **Queue Depth**: Monitoring and alerting

### Efficiency Optimization
- **Message Size**: Optimized payload structure
- **Connection Reuse**: SQS client instance reuse
- **Regional Deployment**: Client-queue region matching
- **Error Minimization**: Validation before sending

## Security Considerations

### AWS Security
- **IAM Permissions**: Least privilege access
- **Queue Encryption**: AWS SQS encryption at rest
- **Network Security**: VPC endpoint support
- **Access Logging**: CloudTrail integration

### Message Security
- **Data Sanitization**: Payload validation
- **Sensitive Data**: Avoid PII in queue messages
- **Message Expiration**: TTL configuration
- **Dead Letter Queues**: Failed message handling

## Monitoring and Observability

### Logging Features
- **Request Tracking**: Send operation logging
- **Response Monitoring**: Status code verification
- **Error Alerting**: Failed delivery notification
- **Performance Metrics**: Response time tracking

### AWS CloudWatch
- **Queue Metrics**: Message count, age, processing time
- **Error Rates**: Failed delivery tracking
- **Throughput**: Messages per second monitoring
- **Alarms**: Automated alerting on thresholds

## Usage Guidelines

1. **Action Naming**: Use clear, descriptive action identifiers
2. **Data Structure**: Keep payloads simple and serializable
3. **Error Handling**: Always handle potential queue failures
4. **Message Size**: Stay within AWS SQS limits (256KB)
5. **Security**: Avoid sensitive data in message payloads

## Limitations

### Current Implementation
- **Single Message**: No batch message support
- **Basic Error Handling**: Simple error logging
- **No Dead Letter Queue**: No automatic retry handling
- **Fixed Configuration**: No runtime queue selection

### AWS SQS Limits
- **Message Size**: 256KB maximum payload
- **Visibility Timeout**: 12 hours maximum
- **Message Retention**: 14 days maximum
- **Throughput**: Standard queue limitations

## Dependencies

- **@aws-sdk/client-sqs**: AWS SQS v3 client library
- **Config**: AWS configuration management
- **@maas/core/log**: Centralized logging system
- **AWS IAM**: Queue access permissions