# info-tile-second.js

## Overview
Job for managing the second phase of WTA (Washington Transit Agency) info tile experiment delivery. This job handles the progressive delivery of experiment tiles and coordinates the transition between different experiment phases based on user engagement and behavioral response patterns.

## File Location
- **Path**: `/allrepo/connectsmart/tsp-job/src/jobs/info-tile-second.js`
- **Module Type**: Scheduled Job
- **Export**: Job configuration with async function

## Key Dependencies
- `@app/src/services/queue` - SQS queue service for message delivery
- `@maas/core/log` - Structured logging utility
- `fs` - File system access for configuration management

## Core Functions

### Sequential Info Tile Processing
Manages the delivery of second-phase info tiles based on experimental timeline:
- **Phase 1**: Initial info tile processing (Sunday 8:00 PM)
- **Phase 2**: Follow-up info tile delivery (Tuesday 8:00 PM)
- Coordinates with queue service for cloud message delivery

### Campaign State Management
Tracks and updates experiment progression through different phases:
- `sent_process = 0`: Ready for first tile delivery
- `sent_process = 1`: First tile sent, ready for second tile
- `sent_process = 2`: Second tile sent, experiment complete

## Processing Flow

### 1. Cloud Message Test Delivery
```javascript
const data = {
  silent: false,
  notification_type: 1,
  user_list: [10449],           // Test user ID
  ended_on: '2022-12-31 20:00:00',
  title: Data.WCCTA[0].title,
  body: Data.WCCTA[0].body,
  meta: {
    title: Data.WCCTA[0].title,
    body: Data.WCCTA[0].body,
  },
};
await QueueService.sendTask('cloud_message', data);
```

### 2. First Tile Processing
```sql
SELECT * FROM hybrid.wta_info_tile 
WHERE sent_process = '0' 
  AND info_tile1 <= current_time;
```

### 3. Second Tile Processing
```sql
SELECT * FROM hybrid.wta_info_tile 
WHERE sent_process = '1' 
  AND info_tile2 <= current_time;
```

### 4. Status Updates
```sql
-- Mark first tile as sent
UPDATE hybrid.wta_info_tile 
SET sent_process = '1' 
WHERE id = '{id}';

-- Mark second tile as sent  
UPDATE hybrid.wta_info_tile 
SET sent_process = '2' 
WHERE id = '{id}';
```

## Data Models

### WTA Tile Configuration
```javascript
// From ./assets/wta_tile.json
{
  "WCCTA": [
    {
      "title": "string",
      "body": "string",
      "tile_name": "string"
    }
  ]
}
```

### Notification Structure
```javascript
{
  silent: boolean,              // Notification visibility
  notification_type: number,    // Type identifier (1 = standard)
  user_list: Array<number>,     // Target user IDs
  ended_on: string,            // Expiration timestamp
  title: string,               // Notification title
  body: string,                // Notification content
  meta: {                      // Additional metadata
    title: string,
    body: string
  }
}
```

### Experiment Timeline States
```javascript
{
  sent_process: 0,   // Initial state - ready for first tile
  sent_process: 1,   // First tile sent - ready for second tile
  sent_process: 2,   // Second tile sent - experiment complete
  info_tile1: datetime,  // First tile delivery time (Sunday 8:00 PM)
  info_tile2: datetime   // Second tile delivery time (Tuesday 8:00 PM)
}
```

## Business Logic

### Tile Type Classifications
Based on experimental design, supports multiple tile types:
```javascript
// Notification types from comments:
// 12  Suggestion: Info Card
// 13  Suggestion: Action Card - Go Later  
// 14  Suggestion: Action Card - Change Mode
// 15  Suggestion: Action Card - DUO
// 16  Suggestion: Action Card - DUO Accept
// 17  Suggestion: Action Card - DUO Reject
```

### Timeline Management
- **Sunday 8:00 PM**: First info tile delivery window
- **Tuesday 8:00 PM**: Second info tile delivery window
- **Timezone Awareness**: Accounts for different US timezones

### Experiment Progression
```javascript
// Experiment flow:
// Phase 1: info_tile1 delivery (Sunday)
// Phase 2: info_tile2 delivery (Tuesday) 
// Phase 3: Behavior monitoring period
// Phase 4: Results analysis
```

## Queue Service Integration

### Cloud Message Delivery
```javascript
await QueueService.sendTask('cloud_message', {
  silent: false,
  notification_type: 1,
  user_list: targetUsers,
  ended_on: expirationTime,
  title: tileContent.title,
  body: tileContent.body,
  meta: additionalData
});
```

### Message Types
- **Info Cards**: Informational content about travel alternatives
- **Action Cards**: Interactive prompts for behavior change
- **DUO Cards**: Carpooling-specific messaging

## Database Operations

### Query Patterns
```sql
-- Find eligible first tiles
SELECT * FROM hybrid.wta_info_tile 
WHERE sent_process = '0' 
  AND info_tile1 <= NOW();

-- Find eligible second tiles  
SELECT * FROM hybrid.wta_info_tile 
WHERE sent_process = '1' 
  AND info_tile2 <= NOW();
```

### Update Operations
```sql
-- Progress to next phase
UPDATE hybrid.wta_info_tile 
SET sent_process = CASE 
  WHEN sent_process = '0' THEN '1'
  WHEN sent_process = '1' THEN '2'
END
WHERE id = target_id;
```

## Configuration Management

### File-Based Configuration
```javascript
const File = await fs.readFileSync('./assets/wta_tile.json', 'utf8');
const Data = JSON.parse(File);
```

### Market-Specific Content
- Supports multiple markets (WCCTA, etc.)
- Market-specific tile content and messaging
- Localized content based on geographic region

## Error Handling
- Graceful handling of missing configuration files
- Validates tile content before queue submission
- Continues processing despite individual tile failures
- Comprehensive logging of all operations

## Performance Considerations

### Batch Processing
- Processes multiple tiles in single execution
- Efficient database queries with appropriate indexing
- Minimizes queue service calls

### Resource Management
- File system access optimized with synchronous reads
- Database connections managed efficiently
- Queue service integration handles delivery failures

## Integration Points

### Queue Service
- Interfaces with SQS-based message delivery system
- Handles cloud push notification routing
- Manages delivery confirmation and retries

### Experiment Framework
- Coordinates with info-tile-first.js for initial setup
- Links to info-tile-results.js for outcome analysis
- Integrates with campaign management system

### Configuration System
- Loads market-specific tile configurations
- Supports dynamic content based on experiment parameters
- Maintains consistency across experiment phases

## Monitoring and Logging
```javascript
logger.info(SQL);              // Query execution logging
logger.info(Rows);             // Results set logging  
logger.info(Rows[index].id);   // Individual tile processing
```

## Usage Scenarios
- **Progressive Experiment Delivery**: Multi-phase campaign execution
- **Behavioral Intervention**: Timed delivery of mobility suggestions
- **Market Testing**: Geographic-specific content delivery
- **Research Coordination**: Academic study timeline management

## Timezone Considerations
- **Multi-timezone Support**: Handles various US timezones
- **Local Time Delivery**: Ensures appropriate delivery timing
- **DST Handling**: Accounts for daylight saving time changes

## Data Flow
```
Configuration Load → Eligible Tile Query → Queue Service Delivery → 
Status Update → Next Phase Preparation
```

## Experimental Design Support
This job supports sophisticated experimental designs:
- **Randomized Delivery**: Supports different tile types
- **Temporal Control**: Precise timing for behavioral studies
- **Market Segmentation**: Geographic and demographic targeting
- **Progressive Disclosure**: Phased information delivery

## Notes
- Critical component in multi-phase WTA experiments
- Coordinates timing across multiple experiment components
- Supports research-grade experimental controls
- Designed for scalability across multiple markets
- Maintains experimental integrity through precise state management