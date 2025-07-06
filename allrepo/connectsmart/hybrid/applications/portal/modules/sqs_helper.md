# AWS SQS Helper Module Documentation

## Overview
The AWS SQS Helper Module provides messaging queue functionality for the ConnectSmart Hybrid Portal application. It handles task queuing, event distribution, and incentive system integration with AWS SQS and MongoDB fallback storage.

## File Location
**Source**: `/home/datavan/METROPIA/metro_combine/allrepo/connectsmart/hybrid/applications/portal/modules/sqs_helper.py`

## Dependencies
- `json`: JSON data serialization
- `logging`: Event logging and debugging
- `boto3`: AWS SDK for SQS operations
- `math`: Mathematical operations for batching
- `gluon.contrib.appconfig.AppConfig`: Web2py configuration
- `typing.List`: Type hints
- `dataclasses.dataclass`: Data structure definitions

## Configuration
```python
configuration = AppConfig()
sqs = boto3.resource("sqs", region_name=configuration.take('aws.region'))
sqs_queue = sqs.get_queue_by_name(QueueName=configuration.take('aws.sqs_queue'))
```

## Global Logger
```python
logger = logging.getLogger('trip')
logger.setLevel(logging.DEBUG)
```

## Functions

### `send_sqs_task(action, data)`

#### Purpose
Send individual task messages to AWS SQS queue for background processing.

#### Parameters
- `action` (str): Task action type identifier
- `data` (dict): Task payload data

#### Message Structure
```python
{
    "action": str,      # Task type
    "data": dict        # Task payload
}
```

#### Process
1. Create message object with action and data
2. Send to configured SQS queue
3. Return SQS response

#### Usage Example
```python
# Send user registration task
send_sqs_task("user_registration", {
    "user_id": 12345,
    "email": "user@example.com",
    "registration_time": "2024-01-15T10:30:00Z"
})

# Send payment processing task
send_sqs_task("process_payment", {
    "payment_id": "pay_67890",
    "amount": 25.50,
    "user_id": 12345
})
```

### `send_sqs_event(event_datas)`

#### Purpose
Send bulk event data for incentive system processing with automatic batching and MongoDB fallback storage.

#### Parameters
- `event_datas` (list): List of event data objects

#### Event Data Structure
```python
{
    'userIds': List[str],       # List of affected user IDs
    'eventName': str,           # Event type name
    'eventMeta': dict           # Event metadata
}
```

#### Batching Configuration
- **Batch Size**: 500 events per message (configured by `limitMax`)
- **Loop Calculation**: `int(len(event_datas) / limitMax) + 1`

#### Process Flow
1. **Calculate Batches**: Determine number of batches needed
2. **Process Each Batch**:
   - Extract batch data using slice indexing
   - Create message with action 'event'
   - Log event details for each item
   - Store in MongoDB collection instead of SQS
   - Handle exceptions with warning logs

#### MongoDB Storage
```python
from mongo_helper import MongoManager
mongo = MongoManager.get()
mongo.send_event.insert_one(message)
```

#### Error Handling
```python
try:
    # Event processing
    logger.info(f"Send incentive event UserIds: {user_ids} Name:{event_name}")
    mongo.send_event.insert_one(message)
except Exception as err:
    logger.warn(f"Send event Error:{err}")
```

## Message Structures

### Task Message Format
```python
{
    "action": "task_type",
    "data": {
        # Task-specific payload
        "key": "value"
    }
}
```

### Event Message Format
```python
{
    'action': 'event',
    'data': [
        {
            'userIds': ['123', '456'],
            'eventName': 'trip_completed',
            'eventMeta': {
                'trip_id': 'trip_789',
                'distance': 5.2,
                'duration': 1800
            }
        }
        # ... more events in batch
    ]
}
```

## Usage Examples

### Basic Task Sending
```python
# Send ride booking task
send_sqs_task("book_ride", {
    "user_id": 12345,
    "pickup_location": {
        "lat": 37.7749,
        "lng": -122.4194
    },
    "destination": {
        "lat": 37.7849,
        "lng": -122.4094
    },
    "ride_type": "standard"
})
```

### Bulk Event Processing
```python
# Prepare multiple events
events = [
    {
        'userIds': ['123', '456'],
        'eventName': 'trip_completed',
        'eventMeta': {
            'trip_id': 'trip_001',
            'points_earned': 50
        }
    },
    {
        'userIds': ['789'],
        'eventName': 'referral_bonus',
        'eventMeta': {
            'referrer_id': '123',
            'bonus_amount': 100
        }
    }
]

# Send events (automatically batched)
send_sqs_event(events)
```

### Incentive System Integration
```python
def award_trip_completion_points(user_ids, trip_data):
    event_data = [{
        'userIds': user_ids,
        'eventName': 'trip_completed',
        'eventMeta': {
            'trip_id': trip_data['id'],
            'distance': trip_data['distance'],
            'duration': trip_data['duration'],
            'points': calculate_points(trip_data),
            'timestamp': datetime.utcnow().isoformat()
        }
    }]
    
    send_sqs_event(event_data)
```

## Configuration Requirements

### AWS Configuration
```python
# Required configuration values
aws = {
    'region': 'us-west-2',           # AWS region
    'sqs_queue': 'portal-tasks'      # SQS queue name
}
```

### Environment Variables
```bash
export AWS_ACCESS_KEY_ID=your_access_key
export AWS_SECRET_ACCESS_KEY=your_secret_key
export AWS_DEFAULT_REGION=us-west-2
```

### IAM Permissions
```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "sqs:SendMessage",
                "sqs:GetQueueUrl",
                "sqs:GetQueueAttributes"
            ],
            "Resource": "arn:aws:sqs:region:account:queue-name"
        }
    ]
}
```

## Event Types

### Trip Events
```python
{
    'eventName': 'trip_completed',
    'eventMeta': {
        'trip_id': str,
        'distance': float,
        'duration': int,
        'points_earned': int
    }
}
```

### User Events
```python
{
    'eventName': 'user_registration',
    'eventMeta': {
        'registration_date': str,
        'referral_code': str,
        'initial_bonus': int
    }
}
```

### Payment Events
```python
{
    'eventName': 'payment_completed',
    'eventMeta': {
        'payment_id': str,
        'amount': float,
        'payment_method': str
    }
}
```

## Logging and Monitoring

### Event Logging Format
```python
logger.info(f"Send incentive event UserIds: {','.join(str(event_data['userIds']))} Name:{event_data['eventName']} Meta:{json.dumps(event_data['eventMeta'])}")
```

### Error Logging
```python
logger.warn(f"Send event Error:{err}")
```

### Log Levels
- **INFO**: Successful event processing
- **WARN**: Processing errors
- **DEBUG**: Detailed operation information

## Performance Considerations

### Batching Strategy
- **Batch Size**: 500 events maximum per message
- **Memory Efficiency**: Process batches sequentially
- **Network Optimization**: Reduce API calls through batching

### MongoDB Fallback
- **High Availability**: MongoDB storage when SQS unavailable
- **Consistency**: Event data preserved regardless of queue status
- **Performance**: Local MongoDB faster for bulk operations

## Storage Architecture

### Dual Storage Pattern
1. **Primary**: AWS SQS for task distribution
2. **Fallback**: MongoDB for event persistence
3. **Reliability**: Ensures no data loss

### MongoDB Collection Structure
```javascript
// send_event collection
{
    _id: ObjectId,
    action: "event",
    data: [
        {
            userIds: ["123", "456"],
            eventName: "trip_completed",
            eventMeta: { ... }
        }
    ],
    created_at: ISODate
}
```

## Error Recovery

### Exception Handling
- Try-catch blocks around critical operations
- Graceful degradation with warning logs
- Continue processing remaining batches on error

### Retry Logic
```python
# Consider implementing retry logic for transient failures
def send_with_retry(message, max_retries=3):
    for attempt in range(max_retries):
        try:
            # Send message
            break
        except Exception as e:
            if attempt == max_retries - 1:
                logger.error(f"Failed after {max_retries} attempts: {e}")
            else:
                logger.warn(f"Attempt {attempt + 1} failed, retrying: {e}")
```

## Integration Patterns

### Task Queue Integration
```python
# Background job processing
def process_user_action(user_id, action_type, data):
    send_sqs_task(f"user_{action_type}", {
        "user_id": user_id,
        "action_data": data,
        "timestamp": datetime.utcnow().isoformat()
    })
```

### Event-Driven Architecture
```python
# Trigger multiple related events
def handle_trip_completion(trip_data):
    events = []
    
    # Award completion points
    events.append({
        'userIds': [trip_data['driver_id'], trip_data['passenger_id']],
        'eventName': 'trip_completed',
        'eventMeta': trip_data
    })
    
    # Check milestone achievements
    if is_milestone_reached(trip_data['driver_id']):
        events.append({
            'userIds': [trip_data['driver_id']],
            'eventName': 'milestone_achieved',
            'eventMeta': {'milestone_type': 'trips_completed'}
        })
    
    send_sqs_event(events)
```

## Security Considerations
- AWS IAM role-based access control
- Message payload validation
- No sensitive data in log messages
- Secure MongoDB connection handling

## Related Components
- MongoDB Helper for data persistence
- AWS infrastructure configuration
- Incentive system processing
- Background job workers