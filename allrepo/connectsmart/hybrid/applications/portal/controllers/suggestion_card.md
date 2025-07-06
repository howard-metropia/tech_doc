# Suggestion Card Controller

## Overview
The Suggestion Card Controller manages contextual travel suggestions and recommendations within the MaaS platform. It provides users with actionable travel advice through interactive cards, tracks user responses, and integrates with the campaign system for personalized engagement and points rewards.

## Technical Stack
- **Framework**: Web2py with RESTful API design
- **Authentication**: JWT-based authentication
- **Database**: MySQL with campaign management tables
- **Messaging**: AWS SQS for notification delivery
- **Response Format**: JSON

## Architecture

### Core Components
- **Card Information Retrieval**: Campaign and notification type mapping
- **Response Tracking**: User interaction recording
- **Points Integration**: Reward calculation and distribution
- **Campaign Integration**: Multi-step campaign workflow support
- **Status Management**: Card lifecycle and user response states

### Database Schema
```sql
-- Campaign steps and cards
cm_step (
  id: int,
  campaign_id: int,
  step_no: int,
  action_type: int,
  choices: json
)

-- Campaign definitions
cm_campaign (
  id: int,
  type_id: int,
  points: decimal(10,2),
  created_on: datetime
)

-- User campaign status
cm_campaign_user (
  id: int,
  user_id: int,
  campaign_id: int,
  step_id: int,
  status: int,
  points: decimal(10,2)
)
```

## API Endpoints

### GET /api/v1/suggestion_card/record/{card_id}
Retrieve suggestion card information and metadata.

**Response:**
```json
{
  "success": true,
  "data": {
    "notification_type": 2,
    "points": 10.0,
    "status": 1
  }
}
```

**Notification Types:**
- `1`: INFO - Informational card
- `2`: GO_EARLY - Early departure suggestion
- `3`: GO_LATER - Delayed departure suggestion
- `4`: CHANGE_MODE - Transportation mode change
- `5`: MICROSURVEY - Interactive survey card
- `6`: DUO - Carpool suggestion
- `7`: WTA_GO_LATER - When-to-arrive late suggestion
- `8`: WTA_GO_EARLY - When-to-arrive early suggestion
- `9`: WTA_CHANGE_MODE - When-to-arrive mode change

### DELETE /api/v1/suggestion_card/record/{card_id}
Mark suggestion card as dismissed/acknowledged.

**Response:**
```json
{
  "success": true
}
```

## Business Logic

### Notification Type Mapping
```python
def get_notification_type(action_type_id):
    """
    Map action types to notification type constants
    """
    type_mapping = {
        1: CampaignHandler.NOTIFICATION_TYPE['INFO'],
        2: CampaignHandler.NOTIFICATION_TYPE['GO_EARLY'], 
        3: CampaignHandler.NOTIFICATION_TYPE['GO_LATER'],
        4: CampaignHandler.NOTIFICATION_TYPE['CHANGE_MODE'],
        5: CampaignHandler.NOTIFICATION_TYPE['MICROSURVEY'],
        6: CampaignHandler.NOTIFICATION_TYPE['DUO'],
        7: CampaignHandler.NOTIFICATION_TYPE['WTA_GO_LATER'],
        8: CampaignHandler.NOTIFICATION_TYPE['WTA_GO_EARLY'],
        9: CampaignHandler.NOTIFICATION_TYPE['WTA_CHANGE_MODE']
    }
    
    return type_mapping.get(action_type_id, 1)
```

### Points Calculation
```python
def calculate_card_points(campaign_points, action_type, user_campaign_points):
    """
    Determine points value based on card type and campaign configuration
    """
    if action_type in (7, 8, 9):  # WTA (When-to-Arrive) types
        # Use user-specific campaign points
        return round(float(user_campaign_points or 0), 2)
    else:
        # Use standard campaign points
        return round(float(campaign_points or 0), 2)
```

### Card Status Management
```python
# Status values
STATUS_PENDING = 1      # Card delivered, awaiting response
STATUS_RESPONDED = 2    # User has responded
STATUS_DISMISSED = 3    # User dismissed card

def update_card_status(user_id, card_id, status):
    """
    Update campaign user status for card interaction
    """
    db(
        (db.cm_campaign_user.step_id == card_id) & 
        (db.cm_campaign_user.user_id == user_id)
    ).update(status=status)
```

## Card Types and Workflows

### Information Cards (Type 1)
- **Purpose**: Provide travel information and tips
- **Interaction**: Single acknowledgment ("Got it" button)
- **Points**: Fixed campaign points
- **Workflow**: Display → Acknowledge → Complete

### Travel Time Suggestions (Types 2, 3, 7, 8)
- **Purpose**: Recommend departure time adjustments
- **GO_EARLY**: Suggest earlier departure
- **GO_LATER**: Suggest delayed departure
- **WTA variants**: When-to-arrive focused suggestions
- **Points**: Variable based on user campaign status

### Mode Change Suggestions (Types 4, 9)
- **Purpose**: Recommend alternative transportation modes
- **Triggers**: Traffic conditions, service disruptions, efficiency
- **Points**: Campaign-based rewards
- **Integration**: Real-time transportation data

### Interactive Surveys (Type 5)
- **Purpose**: Collect user feedback and preferences
- **Special Handling**: Redirects to microsurvey controller
- **Points**: Progressive rewards through survey completion
- **Workflow**: Multi-step survey process

### Carpool Suggestions (Type 6)
- **Purpose**: Promote ridesharing opportunities
- **Integration**: DUO carpool system
- **Points**: Participation-based rewards
- **Social Features**: Partner matching and coordination

## Integration Points

### Campaign Handler Integration
```python
import campaign as CampaignHandler

# Record user response
CampaignHandler.info_card_record(
    user_id=user_id,
    campaign_id=campaign_id, 
    step_no=0,
    reply_status=1  # User acknowledged
)
```

### SQS Notification System
```python
from sqs_helper import send_sqs_task

def _send_suggestion_card_status(card_id, user_id, status):
    """
    Send card status updates via SQS messaging
    """
    card_data = {
        'card_id': card_id,
        'user_id': user_id, 
        'status': status
    }
    send_sqs_task('cloud_message', card_data)
```

### Microsurvey Integration
```python
# Special handling for microsurvey cards
if action_type_id == 5:  # MICROSURVEY
    # Find first step of microsurvey campaign
    first_step = db(
        (db.cm_step.campaign_id == campaign_id) & 
        (db.cm_step.step_no == 1)
    ).select().first()
    
    if first_step:
        card_id = first_step.id  # Redirect to microsurvey first step
```

## Error Handling

### Common Errors
- `ERROR_BAD_REQUEST_PARAMS` (400): Invalid card ID parameter
- `ERROR_NOT_FOUND_CARD` (403): Card not found or access denied
- `ERROR_SUGGESTION_CARD_ID_NOT_FOUND` (400): Invalid suggestion card ID

### Validation Rules
- **Card Existence**: Verify card ID exists in database
- **User Access**: Ensure user has access to specific card
- **Campaign Status**: Validate campaign and user relationship
- **Action Type**: Ensure valid action type mapping

## Response Tracking

### User Interaction Logging
```python
def record_card_interaction(user_id, campaign_id, card_id, reply_status):
    """
    Log user interaction with suggestion card
    """
    CampaignHandler.info_card_record(
        user_id=user_id,
        campaign_id=campaign_id,
        step_no=0,
        reply_status=reply_status
    )
```

### Status Transitions
- **Initial**: Card delivered to user
- **Viewed**: User opened/viewed card
- **Responded**: User took action (accept/dismiss)
- **Completed**: Card workflow finished

## Points and Rewards

### Points Distribution Strategy
```python
def award_card_points(user_id, points, activity_type):
    """
    Award points for card interaction
    """
    if points > 0:
        balance, transaction_id = points_transaction(
            user_id=user_id,
            activity_type=activity_type,
            points=points,
            notify=True
        )
        return balance, transaction_id
    return None, None
```

### Activity Types
- `ACTIVITY_TYPE_SUGGESTION_CARD`: Standard card interaction
- `ACTIVITY_TYPE_TRAVEL_OPTIMIZATION`: Mode/time change suggestions
- `ACTIVITY_TYPE_SURVEY_COMPLETION`: Survey participation

## Performance Considerations

### Database Optimization
- Indexed queries on card_id and user_id
- Efficient campaign data retrieval
- Minimized database roundtrips

### Caching Strategy
- Campaign data caching
- Notification type mapping cache
- User status caching for frequent checks

## Security Features

### Authentication and Authorization
- JWT authentication for all card operations
- User-specific card access validation
- Campaign participation verification

### Data Privacy
- User interaction data protection
- Secure card content delivery
- Privacy-compliant tracking

## Analytics and Monitoring

### Engagement Metrics
- Card view rates by type
- User response patterns
- Points redemption effectiveness
- Campaign completion rates

### Performance Tracking
- Response time monitoring
- Error rate analysis
- User satisfaction indicators

## Configuration

### Notification Types
```python
NOTIFICATION_TYPE = {
    'INFO': 1,
    'GO_EARLY': 2,
    'GO_LATER': 3,
    'CHANGE_MODE': 4,
    'MICROSURVEY': 5,
    'DUO': 6,
    'WTA_GO_LATER': 7,
    'WTA_GO_EARLY': 8,
    'WTA_CHANGE_MODE': 9
}
```

### Status Constants
```python
SUGGESTION_CARD_STATUS_IGNORE = 0
SUGGESTION_CARD_STATUS_ACCEPT = 1
SUGGESTION_CARD_STATUS_CANCEL = 2
```

## Use Cases

### Personalized Travel Optimization
- Real-time route suggestions based on conditions
- Proactive departure time recommendations
- Mode switching for efficiency or cost savings

### User Engagement
- Interactive feedback collection
- Gamified travel behavior modification
- Educational content delivery

### Campaign Management
- Targeted promotional campaigns
- Behavioral incentive programs
- User retention initiatives

## Dependencies
- `json_response`: API response formatting
- `campaign`: Campaign management integration
- `sqs_helper`: AWS SQS messaging system
- `auth`: User authentication and authorization
- `points_transaction`: Points reward system