# wta-mtc-micro-survey.js

## Overview
Job for creating and scheduling micro-survey campaigns asking participants about bike ownership in WTA/MTC experiments. Implements automated follow-up system with multiple reminder attempts and integrates responses into MOD (Mode of Transportation) utility calculations for personalized transportation recommendations.

## File Location
- **Path**: `/allrepo/connectsmart/tsp-job/src/jobs/wta-mtc-micro-survey.js`
- **Module Type**: Scheduled Job
- **Export**: Job configuration with async function

## Key Dependencies
- `@maas/core/mysql` - MySQL database connection (portal)
- `moment-timezone` - Date/time manipulation with timezone support
- `@maas/core/log` - Logging utility

## Core Functions

### Main Processing Function
Creates micro-survey campaigns for new experiment participants to collect bike ownership data critical for transportation mode recommendations.

**Process Flow:**
1. Identify new participants from WTA consent forms and MTC signups
2. Create scheduled micro-survey campaigns with retry logic
3. Set up campaign steps for bike ownership question
4. Associate campaigns with target users
5. Record campaign metadata for tracking

## Job Configuration

### Inputs
No input parameters required.

### Survey Configuration
- **Question**: "Do you own or have routine access to a bike?"
- **Response Options**: "Yes" / "NO"
- **Retry Schedule**: 3 attempts with 2-day intervals
- **Start Delay**: 2 days after consent/signup

## Processing Flow

### 1. New Participant Identification
```sql
SELECT user_id, 'wta' AS experiment_group, modified_on FROM(
  SELECT * FROM hybrid.wta_agree WHERE wta_agree = 1
) AS Table1 WHERE NOT EXISTS (
  SELECT user_id FROM hybrid.wta_mtc_microsurvey 
  WHERE user_id = Table1.user_id
)
UNION
SELECT user_id, 'mtc' as experiment_group, modified_date AS modified_on 
FROM hybrid.mtc_user_signup WHERE NOT EXISTS (
  SELECT user_id FROM hybrid.wta_mtc_microsurvey 
  WHERE user_id = hybrid.mtc_user_signup.user_id
)
```

### 2. Campaign Creation Loop
For each new participant, creates 3 scheduled campaigns:
- **Campaign 1**: 2 days after consent/signup
- **Campaign 2**: 4 days after consent/signup (if no response)
- **Campaign 3**: 6 days after consent/signup (if no response)

### 3. Campaign Configuration
```javascript
// Main campaign settings
{
  name: 'WTA_Experiment_MicroSurvey',
  type_id: '5', // Microsurvey type
  start_time: modified_on + (startDay * iteration),
  end_time: start_time + 1 day,
  change_mode_transport: '3', // Bike mode
  status: '1' // Active
}
```

### 4. Survey Question Setup
```javascript
// Step 1: Introduction
{
  title: 'Can you answer a quick question?',
  action_type: '5', // Microsurvey
  choice_type: '0', // Intro step
  step_no: '1'
}

// Step 2: Bike ownership question
{
  title: 'Do you own or have routine access to a bike?',
  choices: '[{"que":"Yes","nextCard":0},{"que":"NO","nextCard":0}]',
  action_type: '5', // Microsurvey
  choice_type: '1', // Choice question
  step_no: '2'
}
```

### 5. User Campaign Association
```javascript
{
  campaign_id: campaign_id,
  step_id: intro_step_id,
  user_id: participant_id,
  end_time: '2022-12-31 07:00:00',
  reply_status: '1', // Awaiting response
  is_active: '1'
}
```

## Data Models

### wta_agree Table Reference
```javascript
{
  id: number,
  user_id: number,
  wta_agree: boolean, // 1 = agreed
  resend: number,
  modified_on: datetime
}
```

### mtc_user_signup Table Reference
```javascript
{
  id: number,
  user_id: number,
  first_name: string,
  last_name: string,
  e_mail: string,
  phone_number: string,
  modified_date: datetime
}
```

### wta_mtc_microsurvey Tracking Table
```javascript
{
  id: number,
  user_id: number,
  experiment_group: string, // 'wta' or 'mtc'
  campaign_id: string,      // Comma-separated campaign IDs
  sent_process: number,     // 0: pending, 1: completed, 2: expired
  results: datetime,        // Final survey deadline
  created_on: datetime,
  modified_on: datetime
}
```

### Campaign System Tables
```javascript
// cm_campaign
{
  id: number,
  name: string,
  description: string,
  type_id: number, // 5 = Microsurvey
  start_time: datetime,
  end_time: datetime,
  change_mode_transport: number, // 3 = bike
  status: number // 1 = active
}

// cm_step  
{
  id: number,
  campaign_id: number,
  title: string,
  choices: string, // JSON array for options
  step_no: number,
  action_type: number, // 5 = Microsurvey
  choice_type: number // 0 = intro, 1 = choice
}

// cm_campaign_user
{
  id: number,
  campaign_id: number,
  step_id: number,
  user_id: number,
  end_time: datetime,
  status: number,
  reply_status: number, // 1 = awaiting response
  is_active: boolean
}
```

## Business Logic

### Survey Scheduling Strategy
```javascript
const startDay = 2; // Start 2 days after consent/signup
const resend = 3;   // 3 total attempts

for (let i = 1; i <= resend; i++) {
  const scheduleTime = modified_on + (startDay * i) days;
  // Create campaign for this schedule slot
}
```

### Campaign ID Tracking
```javascript
// Build comma-separated campaign ID string
campaignId += i == resend ? 
  resultSQL1[0].insertId : 
  resultSQL1[0].insertId + ',';
```

### Response Integration with MOD System
Survey responses feed into the MOD (Mode of Transportation) utility calculation:
- **Bike ownership = Yes**: Increases bike mode utility
- **Bike ownership = No**: Applies -10 penalty to bike utility
- **No response**: Defaults to "no bike" (penalty applied)

### Experiment Group Handling
- **WTA Group**: Users who agreed to WTA consent form
- **MTC Group**: Users who signed up for MTC experiment
- **Unified Processing**: Both groups receive identical micro-survey

## Error Handling
- Continues processing if individual campaigns fail
- Validates user existence before campaign creation
- Handles database transaction failures gracefully
- Comprehensive logging for debugging campaign creation

## Integration Points
- **WTA Consent System**: Triggers surveys after consent agreement
- **MTC Signup System**: Triggers surveys after experiment enrollment
- **Campaign Management**: Creates info tiles and notifications
- **MOD Calculation Engine**: Survey responses influence transportation recommendations
- **User Engagement System**: Part of broader gamification framework

## Performance Considerations
- Batch processes multiple campaigns per user efficiently
- Minimizes database calls through strategic query design
- Uses efficient date calculations for scheduling
- Proper indexing on user_id and campaign relationships

## Security Considerations
- Parameterized SQL queries prevent injection attacks
- User data privacy maintained through campaign system
- Controlled access to participant information
- Audit trail through comprehensive logging

## Survey Response Processing
Survey responses are processed by companion job `wta-mtc-micro-survey-results.js`:
- **Response Detection**: Monitors for user answers
- **MOD Integration**: Updates bike ownership in activity calculations
- **Campaign Closure**: Stops remaining reminder campaigns
- **Status Tracking**: Marks surveys as completed or expired

## Usage Scenarios
- Post-consent bike ownership data collection
- Transportation mode preference analysis
- MOD utility function personalization
- User segmentation for targeted interventions
- Research data collection for behavior modeling

## Configuration Dependencies
- Campaign management system configuration
- Database permissions for campaign table access
- Micro-survey template and question setup
- MOD calculation system integration
- User engagement notification system

## Monitoring and Logging
- New participant identification logging
- Campaign creation confirmation
- SQL query execution tracking
- Scheduling verification
- Integration point validation

## Data Flow
1. **Source**: WTA consent agreements and MTC signups
2. **Processing**: New participant identification and filtering
3. **Campaign Creation**: Multiple scheduled micro-survey campaigns
4. **User Association**: Campaign-user relationship establishment
5. **Tracking**: Survey metadata and status recording
6. **Integration**: MOD system preparation for response processing

## Survey Question Design
- **Simple Binary Choice**: Reduces user friction and increases response rates
- **Clear Language**: "Do you own or have routine access to a bike?"
- **Relevant Options**: "Yes" vs "NO" (intentional capitalization in data)
- **Single Question**: Minimizes survey fatigue

## Follow-up Strategy
- **Multi-attempt**: 3 scheduled reminders over 6 days
- **Automated**: No manual intervention required
- **Intelligent**: Stops additional reminders once answered
- **Graceful Degradation**: Assumes "no bike" if no response

## Notes
- Critical component of personalized transportation recommendation system
- Integrates bike ownership data into broader mobility analysis
- Supports both WTA and MTC experimental frameworks
- Designed for minimal user burden while maximizing data collection
- Feeds directly into algorithmic mode choice recommendations
- Part of comprehensive user behavior modification research infrastructure
- Maintains strict privacy controls while enabling personalization