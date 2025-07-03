# action-tile-results.js

## Overview
Job module that processes the results of WTA (Washington Transportation Authority) action tile experiments, determining user progression based on point earnings and managing transitions to the next experimental phase.

## Purpose
- Evaluate second-week action tile experiment outcomes
- Check if users earned points through behavioral changes
- Manage user progression to third-week WTA experiments
- Update experiment tracking and completion status

## Key Features
- **Results Evaluation**: Determines experiment success based on point earnings
- **User Progression**: Routes users to next experiment phase if needed
- **State Management**: Updates tracking status to prevent duplicate processing
- **Point Verification**: Cross-references wallet transactions with campaign interactions

## Dependencies
```javascript
const knex = require('@maas/core/mysql')('portal');
const { logger } = require('@maas/core/log');
const { targetTable } = require('@app/src/services/wallet');
```

## Core Processing Logic

### Main Function Structure
```javascript
module.exports = {
  inputs: {},
  fn: async function () {
    // Process completed action tile experiments
    // Evaluate point earnings and determine next steps
    // Update experiment status and user progression
  }
};
```

### Experiment Completion Query
```sql
SELECT *, MAX(results) AS final_results
FROM hybrid.wta_action_tile
WHERE sent_process = 0
GROUP BY user_id
HAVING final_results <= '2022-03-31 12:30:06';
```

### Point Verification Query
```sql
SELECT hybrid.wta_action_tile.id, hybrid.wta_action_tile.user_id,
( SELECT points FROM hybrid.${targetTable} 
  WHERE hybrid.${targetTable}.user_id = hybrid.wta_action_tile.user_id 
  AND hybrid.${targetTable}.note LIKE CONCAT('card_id: ', hybrid.cm_step.id) 
  LIMIT 1) AS point_status
FROM hybrid.wta_action_tile LEFT JOIN hybrid.cm_step
ON hybrid.wta_action_tile.campaign_id = hybrid.cm_step.campaign_id
WHERE hybrid.wta_action_tile.user_id = ? AND hybrid.wta_action_tile.sent_process = 0
HAVING !ISNULL(point_status);
```

## Processing Flow

### 1. Identify Completed Experiments
- Query users with finished action tile periods
- Group by user to get final experiment dates
- Filter based on completion timeline

### 2. Point Status Verification
- Check wallet transactions for campaign-related points
- Match campaign IDs with transaction notes
- Verify point earnings from behavioral changes

### 3. Status Updates
```javascript
// Update token status for users who earned points
const SQL3 = `
  UPDATE hybrid.wta_action_tile SET tokens_status = '1' WHERE id = '${recordId}';
`;

// Mark experiment as processed
const SQL4 = `
  UPDATE hybrid.wta_action_tile SET sent_process = '1' WHERE user_id = '${userId}';
`;
```

### 4. Experiment Progression Logic
```javascript
if (pointsEarned == 0) {
  // User didn't earn points - advance to WTA experiment
  const SQL5 = `
    INSERT INTO hybrid.wta_experiment (
      user_id,
      departure_time,
      travel_mode
    ) VALUES (?, ?, ?);
  `;
}
```

## Database Tables

### Primary Tables
- `hybrid.wta_action_tile` - Second-week experiment tracking
- `hybrid.wta_experiment` - Third-week experiment enrollment
- `hybrid.cm_step` - Campaign step definitions
- `hybrid.${targetTable}` - User wallet transactions

### Key Fields
- `sent_process` - Processing status flag (0: pending, 1: processed)
- `tokens_status` - Point earning status (1: earned points)
- `point_status` - Transaction verification result
- `final_results` - Experiment completion timestamp

## Experiment Transition Logic

### Success Path (Points Earned)
1. User completed behavioral change and earned points
2. Update `tokens_status = '1'` in action tile record
3. Mark experiment as processed
4. No further experiment enrollment needed

### Continuation Path (No Points)
1. User did not earn points from behavioral change
2. Enroll user in `wta_experiment` table for third week
3. Transfer user data (departure_time, travel_mode)
4. Mark experiment as processed

## Error Handling
- Database query error logging through logger service
- Transaction rollback capability for data consistency
- Duplicate processing prevention through status flags

## Performance Considerations
- Efficient GROUP BY queries to avoid duplicate processing
- Indexed lookups on user_id and campaign_id fields
- Batch processing of user records
- Single transaction per user for consistency

## Monitoring and Logging
```javascript
const DBstartTime = Date.now();
logger.info(SQL); // Query logging
logger.info(knexRows[index].user_id); // User processing tracking
```

## Integration Points
- **Wallet Service**: Point transaction verification
- **Campaign System**: Action tile campaign data
- **Experiment Framework**: User progression management
- **Database Layer**: MySQL portal database operations

## Usage Patterns
- Scheduled execution after action tile experiment periods
- Batch processing of all completed experiments
- One-time processing per experiment period per user

## State Management
- Uses `sent_process` flag to prevent duplicate processing
- Maintains experiment continuity through user data transfer
- Tracks point earning status for analytics and reporting

## Business Logic
- Second-week experiment evaluation based on behavioral change
- Automatic enrollment in third-week experiments for continued engagement
- Point-based success measurement for intervention effectiveness

## Data Flow
1. **Input**: Completed action tile experiments from database
2. **Processing**: Point verification and status evaluation
3. **Output**: Updated experiment status and potential third-week enrollment
4. **Tracking**: Process completion flags and status updates