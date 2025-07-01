# MicroSurvey Controller

## Overview
The MicroSurvey Controller manages interactive micro-surveys within the MaaS platform, enabling targeted user engagement through step-by-step survey campaigns. This controller handles survey workflow, response tracking, and points-based reward distribution.

## Technical Stack
- **Framework**: Web2py
- **Authentication**: JWT-based with token validation
- **Database**: MySQL with campaign tables (cm_*)
- **Messaging**: AWS SQS for notifications
- **Response Format**: JSON

## Architecture

### Core Components
- **Campaign Management**: Multi-step survey campaigns with configurable flows
- **Response Tracking**: User answer recording and status management
- **Points System**: Reward distribution for survey completion
- **Notification System**: Push notifications for survey progression

### Database Schema
```sql
-- Campaign structure
cm_campaign (id, points, type_id, created_on)
cm_step (id, campaign_id, step_no, choices, action_type)
cm_campaign_user (user_id, campaign_id, step_id, status, points)
cm_user_record (user_id, campaign_id, action_type, points, reply_status)
```

## API Endpoints

### POST /api/v1/microsurvey/first
Accept or reject the first survey card in a campaign.

**Request Body:**
```json
{
  "card_id": 123,
  "accept": true
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "points": 5.0
  }
}
```

**Status Mapping:**
- `1`: Accepted (proceed to next step)
- `2`: Completed with points
- `3`: Skipped/rejected

### POST /api/v1/microsurvey/submit
Submit answers for a survey step and proceed to next step or complete.

**Request Body:**
```json
{
  "card_id": "456",
  "answer": [0, 2],
  "points": 5.0
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "points": 5.0,
    "next": true
  }
}
```

**Flow Logic:**
1. Validate answers against available choices
2. Determine next step based on answer logic
3. Award points if survey completed
4. Send notification for next step or completion

### POST /api/v1/microsurvey/skip
Skip the current survey step and end the campaign.

**Request Body:**
```json
{
  "card_id": "789"
}
```

**Response:**
```json
{
  "success": true
}
```

## Business Logic

### Survey Flow Management
```python
def microsurvey_next_card(choices, answer):
    """
    Determines next survey step based on user responses
    Returns step number (>0) or 0 for completion
    """
    # Complex logic based on choice mapping
    # Returns next step ID or 0 for completion
```

### Status Management
- **Status 1**: User replied/accepted
- **Status 2**: Received/in progress
- **Status 3**: Skipped/completed

### Points Distribution
- Points awarded only upon survey completion
- Configurable per campaign
- Recorded in points_transaction table
- Push notifications sent for rewards

## Error Handling

### Common Errors
- `ERROR_BAD_REQUEST_BODY` (400): Invalid parameters
- `ERROR_NOT_FOUND_CARD` (403): Survey card not found
- `ERROR_UNKNOWN` (502): Processing failure

### Validation
- Card ID existence and user access
- Answer format and choice validation
- Campaign status and timing checks

## Integration Points

### Campaign Handler
```python
import campaign as CampaignHandler

# Status management
CampaignHandler.ms_change_status(user_id, campaign_id, status, accept)

# Next card generation
CampaignHandler.get_microsurvey_card(user_id, step_id, timestamp, points)

# Response recording
CampaignHandler.microsurvey_record(user_id, campaign_id, card_id, step_no, answer, points, status)
```

### SQS Messaging
```python
from sqs_helper import send_sqs_task

# Send push notification for next survey step
send_sqs_task('cloud_message', card_data)
```

### Points System
```python
# Award points upon survey completion
balance, pt_id = points_transaction(
    user_id, 
    POINTS_ACTIVITY_TYPE_MICROSURVEY, 
    points, 
    notify=True
)
```

## Security Features
- JWT authentication required for all endpoints
- User-specific card access validation
- Input sanitization and type checking
- Campaign timing and status verification

## Performance Considerations
- Database queries optimized with joins
- Response caching for campaign data
- Asynchronous notification processing
- Efficient status tracking

## Monitoring and Logging
- Debug logging for API failures
- User response tracking
- Campaign completion metrics
- Error rate monitoring

## Configuration
- Survey expiration timeouts
- Points reward amounts
- Notification delivery settings
- Campaign flow definitions

## Dependencies
- `campaign`: Core campaign management
- `sqs_helper`: AWS SQS integration
- `json_response`: Response formatting
- `auth`: JWT authentication
- `points_transaction`: Reward distribution