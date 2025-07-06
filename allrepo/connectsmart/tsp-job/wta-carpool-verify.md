# wta-carpool-verify.js

## Overview
Job for verifying WTA (Washington Transit Authority) carpool experiment participation and awarding points to users who completed qualifying carpool trips. Manages the entire lifecycle of carpool verification including trip validation, point allocation, campaign notifications, and status updates.

## File Location
- **Path**: `/allrepo/connectsmart/tsp-job/src/jobs/wta-carpool-verify.js`
- **Module Type**: Scheduled Job
- **Export**: Job configuration with async function

## Key Dependencies
- `@maas/core/mysql` - MySQL database connection (portal)
- `geo-point-in-polygon` - Geographic polygon containment checking
- `@app/src/services/incentiveUtility` - Incentive calculation utilities
- `@app/src/services/sendMail` - Email notification service
- `moment` / `moment-timezone` - Date/time manipulation
- `config` - Application configuration
- `ejs` - Template rendering engine
- `hashids/cjs` - Hash ID generation
- `@maas/core/log` - Logging utility
- `@app/src/services/wallet` - Wallet and points transaction services

## Core Functions

### Main Processing Function
Verifies active WTA carpool experiments and processes successful carpool trip completions.

**Process Flow:**
1. Find active carpool experiments within date range
2. Validate qualifying carpool trips for each user
3. Create notification campaigns for successful participants
4. Award points through wallet system
5. Update carpool experiment status
6. Mark expired experiments as inactive

## Job Configuration

### Inputs
No input parameters required.

### WTA Carpool Verification
- **Experiment Table**: `hybrid.wta_carpool`
- **Trip Validation**: `hybrid.trip` with travel_mode = 100 (carpool)
- **Point Allocation**: Uses wallet service for transaction management
- **Campaign System**: Creates info tiles for user notifications

## Processing Flow

### 1. Active Experiment Identification
```sql
SELECT * FROM hybrid.wta_carpool 
WHERE start_date <= NOW() 
AND end_date >= NOW() 
AND status = 0
```

### 2. Trip Qualification Validation
For each active carpool experiment:
```sql
SELECT * FROM hybrid.trip 
WHERE ended_on <= '${end_date}'
AND ended_on >= '${start_date}'
AND user_id = '${user_id}'
AND travel_mode = 100
```

### 3. Campaign Notification Creation
Creates three-part campaign system:
- **Main Campaign**: Info tile notification about point award
- **Step Configuration**: Message content and action type
- **User Association**: Links campaign to specific user

### 4. Points Transaction Processing
```javascript
await pointsTransaction(
  user_id,
  6, // activity_type for carpool
  currentCoins,
  'wta_carpool_point',
  false
);
```

### 5. Status Management
Updates experiment status:
- `status = '1'`: Successfully completed and points awarded
- `status = '2'`: Expired without completion
- Records associated trip ID for audit trail

## Data Models

### wta_carpool Table Structure
```javascript
{
  id: number,
  user_id: number,
  start_date: datetime,
  end_date: datetime,
  point: number,
  status: number, // 0: active, 1: completed, 2: expired
  carpool_trip_id: number,
  created_on: datetime,
  modified_on: datetime
}
```

### trip Table Reference
```javascript
{
  id: number,
  user_id: number,
  travel_mode: number, // 100 = carpool
  ended_on: datetime,
  o_lat: float,
  o_lng: float,
  d_lat: float,
  d_lng: float
}
```

### Campaign System Tables
```javascript
// cm_campaign
{
  id: number,
  name: string,
  description: string,
  type_id: number,
  start_time: datetime,
  end_time: datetime,
  status: number
}

// cm_step
{
  id: number,
  campaign_id: number,
  title: string,
  body: string,
  action_type: number,
  step_no: number
}

// cm_campaign_user
{
  id: number,
  campaign_id: number,
  step_id: number,
  user_id: number,
  status: number,
  is_active: boolean
}
```

## Business Logic

### Carpool Trip Validation
- **Travel Mode**: Must be mode 100 (carpool)
- **Time Window**: Trip end time must fall within experiment date range
- **User Association**: Must match registered carpool experiment user
- **Status Verification**: Experiment must be in active status (0)

### Point Award Calculation
```javascript
// Retrieve current balance
const currentBalance = knexRows5[0].length == 0 ? 0 : parseFloat(knexRows5[0][0].balance);
const newBalance = currentBalance + parseFloat(experimentPoints);
```

### Campaign Notification System
- **Campaign Type**: Info tile (type_id = 1)
- **Message Template**: "Congratulation!! You has earned ${points} coin(s)."
- **Duration**: 8-hour active window (480 minutes)
- **Creator**: 'black.tseng@metropia.com'
- **Timezone**: America/Los_Angeles

### Status Management Logic
```javascript
// Success criteria
if (qualifying_trip_found) {
  status = '1'; // Completed successfully
  carpool_trip_id = trip.id;
  award_points();
  create_notification();
}

// Expiration handling
if (end_date < current_time && status == '0') {
  status = '2'; // Expired
}
```

## Error Handling
- Continues processing if individual experiments fail
- Handles missing wallet records gracefully (defaults to 0 balance)
- Logs all SQL operations for debugging
- Maintains data integrity through transaction management

## Integration Points
- **Wallet Service**: Points allocation and balance management
- **Trip Tracking**: Integration with trip recording system
- **Campaign Management**: Notification and info tile system
- **Email System**: User notification capabilities
- **Geographic Services**: Location-based validation support

## Performance Considerations
- Sequential processing to maintain data integrity
- Efficient SQL queries with proper indexing
- Minimal database calls through batch operations
- Proper transaction management for point allocation

## Security Considerations
- Parameterized SQL queries to prevent injection
- Wallet service integration for secure transactions
- Proper user association validation
- Audit trail maintenance through logging

## Usage Scenarios
- Daily verification of completed carpool experiments
- Point allocation for successful carpool participation
- User engagement through gamification rewards
- Transportation behavior modification incentives
- Research data collection for carpool effectiveness

## Configuration Dependencies
- Database connection to portal MySQL instance
- Wallet service configuration for point transactions
- Campaign system setup for notification delivery
- Email service configuration for user communications
- Geographic utility services for location validation

## Monitoring and Logging
- SQL query execution logging
- Point transaction confirmation
- Campaign creation verification
- Status update tracking
- Error condition reporting

## Data Flow
1. **Source**: Active WTA carpool experiments from database
2. **Validation**: Trip records matching experiment criteria
3. **Processing**: Point calculation and wallet integration
4. **Notification**: Campaign creation for user engagement
5. **Storage**: Status updates and audit trail maintenance
6. **Cleanup**: Expired experiment status management

## Notes
- Supports WTA-specific carpool incentive programs
- Integrates with comprehensive mobility gamification system
- Maintains detailed audit trail for research purposes
- Handles both successful completion and expiration scenarios
- Critical component of transportation behavior modification research
- Uses standardized wallet service for consistent point management