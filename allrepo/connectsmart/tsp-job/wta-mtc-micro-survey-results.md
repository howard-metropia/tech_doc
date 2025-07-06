# wta-mtc-micro-survey-results.js

## Overview
Job for processing WTA/MTC micro-survey responses about bike ownership and integrating results into the MOD (Mode of Transportation) utility calculation system. Handles survey completion detection, campaign management, and updates transportation mode recommendations based on user responses.

## File Location
- **Path**: `/allrepo/connectsmart/tsp-job/src/jobs/wta-mtc-micro-survey-results.js`
- **Module Type**: Scheduled Job
- **Export**: Job configuration with async function

## Key Dependencies
- `@maas/core/mysql` - MySQL database connection (portal)
- `moment` / `moment-timezone` - Date/time manipulation
- `@maas/core/log` - Logging utility

## Core Functions

### Main Processing Function
Processes micro-survey responses and updates transportation mode calculations based on bike ownership data.

**Process Flow:**
1. Identify active micro-surveys within deadline
2. Check for user responses to bike ownership question
3. Process answered surveys and update MOD calculations
4. Close remaining reminder campaigns
5. Handle expired surveys with default values
6. Update survey tracking status

## Job Configuration

### Inputs
No input parameters required.

### Survey Processing
- **Response Detection**: Monitors `cm_microsurvey_record` table
- **MOD Integration**: Updates `cm_activity_mod.bike_own` field
- **Campaign Management**: Closes related campaigns
- **Status Tracking**: Updates survey completion status

## Processing Flow

### 1. Active Survey Identification
```sql
SELECT id, user_id, campaign_id
FROM hybrid.wta_mtc_microsurvey
WHERE sent_process = 0 
AND results >= '${current_time}'
```

### 2. Response Detection
For each active survey, checks all associated campaigns:
```sql
SELECT id FROM hybrid.cm_step 
WHERE campaign_id IN (${campaign_id_list}) 
AND choices IS NOT NULL
```

### 3. Answer Validation
```sql
SELECT answer FROM hybrid.cm_microsurvey_record 
WHERE step_id = ${step_id}
```

### 4. Response Analysis
```javascript
// Answer interpretation
const hasBike = answer == '[0]' ? 0 : 1; // [0] = No, other = Yes
let responseCount = 0;

// Count responses across all campaign attempts
for (const step of surveySteps) {
  responseCount += responses.length >= 1 ? 1 : 0;
}
```

### 5. Campaign Closure (If Answered)
```sql
UPDATE hybrid.cm_campaign 
SET status = '5'  -- Closed status
WHERE id IN (${campaign_id_list})
```

### 6. MOD System Integration
For users who own bikes:
```sql
SELECT id FROM hybrid.cm_activity_location 
WHERE user_id = ${user_id}
```

Then update bike utility:
```sql
UPDATE hybrid.cm_activity_mod 
SET bike_own = '1' 
WHERE activity_id = ${activity_id} 
AND travel_mode = 'bicycling'
```

### 7. Survey Status Update
```sql
UPDATE hybrid.wta_mtc_microsurvey 
SET sent_process = '1' 
WHERE id = ${survey_id}
```

### 8. Expired Survey Handling
```sql
SELECT id, user_id, campaign_id
FROM hybrid.wta_mtc_microsurvey
WHERE sent_process = 0 
AND results < '${current_time}'
```

Mark expired surveys:
```sql
UPDATE hybrid.wta_mtc_microsurvey 
SET sent_process = '2' 
WHERE id = ${survey_id}
```

## Data Models

### wta_mtc_microsurvey Tracking Table
```javascript
{
  id: number,
  user_id: number,
  experiment_group: string, // 'wta' or 'mtc'
  campaign_id: string,      // Comma-separated campaign IDs
  sent_process: number,     // 0: active, 1: completed, 2: expired
  results: datetime,        // Survey deadline
  created_on: datetime,
  modified_on: datetime
}
```

### cm_microsurvey_record Response Table
```javascript
{
  id: number,
  step_id: number,
  user_id: number,
  answer: string,      // '[0]' = No bike, '[1]' = Has bike
  created_on: datetime,
  modified_on: datetime
}
```

### cm_activity_location Reference Table
```javascript
{
  id: number,
  user_id: number,
  o_id: number,        // Origin location ID
  d_id: number,        // Destination location ID
  travel_mode: number,
  trip_count: number
}
```

### cm_activity_mod MOD Calculation Table
```javascript
{
  id: number,
  activity_id: number,
  travel_mode: string,    // 'bicycling', 'driving', etc.
  bike_own: number,       // 0: no bike, 1: has bike
  utility_score: float,
  created_on: datetime,
  modified_on: datetime
}
```

### cm_campaign Status Table
```javascript
{
  id: number,
  name: string,
  status: number,  // 1: Scheduled, 2: In progress, 3: Draft, 4: Stopped, 5: Closed
  start_time: datetime,
  end_time: datetime
}
```

## Business Logic

### Response Interpretation
```javascript
// Survey answer format analysis
const bikeOwnership = {
  '[0]': 0,    // User selected "NO" - no bike access
  '[1]': 1,    // User selected "Yes" - has bike access
  'default': 0 // No response defaults to no bike
};
```

### MOD Utility Impact
Bike ownership directly affects transportation mode recommendations:
```javascript
// Utility calculation modification
if (bike_own == 1) {
  // Positive bike utility - user more likely to get bike recommendations
  bike_utility_bonus = 0; // Neutral/positive weighting
} else {
  // Penalty for no bike access
  bike_utility_penalty = -10; // Configurable negative weight
}
```

### Survey Completion Logic
```javascript
if (responseCount >= 1) {
  // User answered at least one survey attempt
  closeRemainingCampaigns();
  updateMODCalculations();
  markSurveyCompleted();
} else if (currentTime > surveyDeadline) {
  // Survey expired without response
  markSurveyExpired();
  // Default to "no bike" in MOD calculations
}
```

### Campaign Status Management
- **Status 1**: Scheduled (waiting to send)
- **Status 2**: In progress (sent to user)
- **Status 3**: Draft (not yet active)
- **Status 4**: Stopped (manually halted)
- **Status 5**: Closed (completed or cancelled)

## Error Handling
- Continues processing if individual surveys fail
- Handles missing response records gracefully
- Validates campaign existence before updates
- Comprehensive logging for debugging
- Maintains data integrity through proper transaction handling

## Integration Points
- **Campaign Management System**: Controls survey delivery and status
- **MOD Calculation Engine**: Integrates bike ownership into utility functions
- **User Activity Tracking**: Links responses to user location patterns
- **Transportation Recommendation System**: Influences mode choice suggestions
- **Experiment Analytics**: Provides data for research analysis

## Performance Considerations
- Efficient SQL queries with proper indexing
- Batch processing of related surveys
- Minimal database calls through strategic query design
- Proper cleanup of completed/expired surveys

## Security Considerations
- Parameterized SQL queries prevent injection attacks
- User privacy maintained through controlled data access
- Audit trail through comprehensive logging
- Secure handling of survey response data

## MOD System Integration Details

### Bike Utility Calculation
The survey response directly impacts how the system calculates bike mode utility:
```javascript
// Before survey: Default bike utility calculation
bike_utility = base_utility + distance_factor + weather_factor;

// After survey (bike owner): Enhanced bike utility
bike_utility = base_utility + distance_factor + weather_factor + (bike_own * 0);

// After survey (no bike): Penalized bike utility  
bike_utility = base_utility + distance_factor + weather_factor + (bike_own * -10);
```

### Activity Location Mapping
Survey responses are applied to all user activity locations:
```javascript
// Get all user habitual trips
const userActivities = getUserActivityLocations(user_id);

// Update bike ownership for each activity
userActivities.forEach(activity => {
  updateBikeMOD(activity.id, bikeOwnershipStatus);
});
```

## Usage Scenarios
- Daily processing of micro-survey responses
- Transportation recommendation personalization
- User behavior modification research
- MOD algorithm optimization
- Experiment outcome analysis

## Configuration Dependencies
- Database access to campaign and survey tables
- MOD calculation system configuration
- Survey response tracking setup
- Campaign management system integration
- Transportation utility calculation parameters

## Monitoring and Logging
- Active survey identification logging
- Response detection and interpretation
- MOD system update confirmation
- Campaign closure verification
- Expired survey handling status

## Data Flow
1. **Source**: Active micro-surveys from tracking table
2. **Detection**: Survey response monitoring and validation
3. **Processing**: Answer interpretation and business logic application
4. **Integration**: MOD system updates for transportation recommendations
5. **Cleanup**: Campaign closure and status management
6. **Tracking**: Survey completion status recording

## Response Processing Workflow

### Successful Response Path
1. Detect user response to bike ownership question
2. Interpret answer (Yes/No bike access)
3. Close all remaining reminder campaigns
4. Update MOD bike utility for all user activities
5. Mark survey as completed (sent_process = 1)

### Expiration Handling Path
1. Identify surveys past deadline without response
2. Mark as expired (sent_process = 2)
3. Default to "no bike" assumption in MOD calculations
4. Maintain audit trail for research analysis

## Survey Analytics Integration
- **Response Rate Tracking**: Monitors completion vs. expiration rates
- **Timing Analysis**: Tracks which reminder attempt gets responses
- **Behavioral Correlation**: Links bike ownership to mode choice patterns
- **Experiment Effectiveness**: Measures survey impact on recommendations

## Notes
- Critical component of personalized transportation recommendation system
- Processes responses from companion micro-survey creation job
- Integrates directly with MOD utility calculation algorithms
- Supports both WTA and MTC experimental frameworks
- Handles both successful responses and non-response scenarios gracefully
- Maintains comprehensive audit trail for research validation
- Uses configurable utility penalties for flexible algorithm tuning
- Essential for transportation behavior modification research infrastructure