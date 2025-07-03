# Send Event Helper

## Overview
**File**: `src/helpers/send-event.js`  
**Type**: Event Utility  
**Purpose**: Sends incentive events through SQS queue with batching support (currently uses local database)

## Core Function

### Event Sending
```javascript
module.exports = async (eventDatas) => {
  const limitMax = 500; // SQS batch limit
  const loop = Math.ceil(eventDatas.length / limitMax);
  
  // Process events in batches
  // Log event details
  // Store in local database (SQS commented out)
}
```

## Configuration

### SQS Integration (Commented)
```javascript
// const client = new SQSClient({ region: awsConfig.region });
// const { $metadata } = await client.send(
//   new SendMessageCommand({
//     MessageBody: JSON.stringify(message),
//     QueueUrl: awsConfig.sqs.queueUrl,
//   }),
// );
```

### Current Implementation
- **Database Storage**: Uses SendEvent model for persistence
- **SQS Code**: Present but commented out
- **AWS Integration**: Ready for activation

## Event Data Structure

### Input Format
```javascript
[
  {
    eventName: 'trip_completed',
    eventMeta: {
      trip_id: '12345',
      distance: 1500,
      mode: 'transit'
    },
    userIds: [101, 102, 103]
  }
]
```

### Message Format
```javascript
{
  action: 'event',
  data: [
    {
      eventName: 'string',
      eventMeta: {},
      userIds: [number]
    }
  ]
}
```

## Batching Logic

### Batch Processing
- **Batch Size**: 500 events maximum per batch
- **Loop Calculation**: `Math.ceil(eventDatas.length / limitMax)`
- **Sequential Processing**: Processes batches in order

### Batch Creation
```javascript
const sendData = eventDatas.slice(i * limitMax, limitMax);
```

## Logging

### Event Information
```javascript
logger.info(
  `Send incentive event UserIds: ${data.userIds.join(',')} Name:${data.eventName} Meta:${JSON.stringify(data.eventMeta)}`
);
```

### Log Content
- **User IDs**: Comma-separated list of target users
- **Event Name**: Type of incentive event
- **Event Metadata**: Full event data as JSON

## Dependencies

### External Libraries
- `@maas/core/log`: Logging functionality
- `@app/src/models/SendEvent`: Database model for event storage

### AWS Dependencies (Commented)
- `@aws-sdk/client-sqs`: SQS client for message queuing
- `config`: AWS configuration access

## Usage Examples

### Single Event
```javascript
const sendEvent = require('./send-event');

await sendEvent([
  {
    eventName: 'trip_completed',
    eventMeta: {
      trip_id: 'abc123',
      distance: 2500,
      duration: 1800
    },
    userIds: [12345]
  }
]);
```

### Multiple Events
```javascript
const events = [
  {
    eventName: 'signup_bonus',
    eventMeta: { bonus_amount: 5.00 },
    userIds: [101, 102]
  },
  {
    eventName: 'referral_reward',
    eventMeta: { referrer_id: 99, amount: 2.50 },
    userIds: [103]
  }
];

await sendEvent(events);
```

### Large Batch
```javascript
// Automatically handles batching for 1000+ events
const largeEventList = generateEvents(1500);
await sendEvent(largeEventList);
```

## Error Handling

### Try-Catch Structure
```javascript
try {
  // Event processing and database storage
  SendEvent.create(message);
} catch (err) {
  logger.warn(`Send event Error:${err.message}`);
}
```

### Error Recovery
- **Logs Warnings**: Non-fatal error handling
- **Continues Processing**: Doesn't stop on individual failures
- **No Retry Logic**: Failed events not automatically retried

## Database Integration

### SendEvent Model
- **Purpose**: Stores event data for processing
- **Schema**: Contains action and data fields
- **Persistence**: Local database storage

### Message Storage
```javascript
const message = {
  action: 'event',
  data: sendData,
};
SendEvent.create(message);
```

## Performance Considerations

### Batching Benefits
- **Reduced API Calls**: Fewer SQS requests
- **Improved Throughput**: Higher event processing rate
- **Cost Optimization**: Lower AWS costs per event

### Memory Usage
- **Slice Operations**: Efficient array slicing
- **Sequential Processing**: Avoids memory spikes
- **Logging**: Consider log volume for large batches

## Migration to SQS

### Current State
- **Database**: Events stored locally
- **SQS Code**: Ready but commented out
- **Configuration**: AWS config present but unused

### Activation Steps
1. **Uncomment SQS Code**: Enable AWS SDK usage
2. **Configure Credentials**: Set up AWS authentication
3. **Test Integration**: Verify SQS connectivity
4. **Remove Database**: Migrate from local storage

## Event Types

### Common Events
- **trip_completed**: Trip completion rewards
- **signup_bonus**: New user incentives
- **referral_reward**: User referral bonuses
- **milestone_achieved**: Achievement rewards

### Event Metadata
- **Flexible Structure**: Any JSON-serializable data
- **Trip Data**: Distance, duration, mode information
- **User Data**: User-specific reward information
- **Context**: Additional event context

## Integration Points

### Incentive Engine
- **Event Processing**: Downstream event processing
- **Reward Calculation**: Event-driven reward computation
- **User Notifications**: Event-triggered notifications

### Analytics
- **Event Tracking**: Monitor event types and volumes
- **User Engagement**: Track user participation
- **Performance Metrics**: Event processing performance

## Configuration Requirements

### AWS Configuration (Future)
```javascript
vendor: {
  aws: {
    region: 'us-east-1',
    sqs: {
      queueUrl: 'https://sqs.us-east-1.amazonaws.com/123456789/events'
    }
  }
}
```

### Database Configuration
- **SendEvent Model**: Configured in models directory
- **Connection**: Uses application database connection

## Monitoring

### Metrics to Track
- **Event Volume**: Events processed per time period
- **Batch Efficiency**: Average batch sizes
- **Error Rates**: Failed event processing
- **Processing Latency**: Time to process batches

### Logging Strategy
- **Individual Events**: Detailed event information
- **Batch Processing**: Batch size and timing
- **Error Tracking**: Failure reasons and context

## Testing Considerations

### Unit Tests
```javascript
// Mock dependencies
jest.mock('@app/src/models/SendEvent');
jest.mock('@maas/core/log');

// Test batch processing
const events = new Array(1500).fill(mockEvent);
await sendEvent(events);
```

### Integration Tests
- **Database Storage**: Verify event persistence
- **Batch Logic**: Test large event arrays
- **Error Scenarios**: Test failure handling

## Security Notes

### Data Privacy
- **User IDs**: Logs contain user identifiers
- **Event Metadata**: May contain sensitive information
- **Access Control**: Restrict access to event data

### Validation
- **Input Sanitization**: Validate event data structure
- **User Authorization**: Verify user permissions
- **Rate Limiting**: Consider event submission limits