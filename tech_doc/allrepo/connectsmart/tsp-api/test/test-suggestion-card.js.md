# test-suggestion-card.js

## Overview
Test suite for the suggestion card system in the TSP API. Tests retrieval and status management of campaign-based suggestion cards that provide users with transportation recommendations and incentives.

## File Location
`/test/test-suggestion-card.js`

## Dependencies
- **@maas/core**: Core MaaS framework components
- **supertest**: HTTP assertions for API testing
- **chai**: BDD/TDD assertion library
- **Models**: AuthUsers, CMSteps, CMCampaignUsers, CMUserRecords

## Test Configuration

### Test User
```javascript
const userId = 1003;
const campaignId = 123456;
```

### Authentication Setup
- User ID: 1003
- Bearer token from AuthUsers table
- Content-Type: application/json

## Database Models

### Campaign Management (CM) Models
- **CMSteps**: Campaign step definitions
- **CMCampaignUsers**: User-campaign associations
- **CMUserRecords**: User interaction records

### Model Relationships
```
CMSteps (1) -> (N) CMCampaignUsers
CMCampaignUsers (N) -> (1) AuthUsers
CMUserRecords -> CMCampaignUsers (tracking)
```

## Test Data Setup

### Campaign Step Creation
```javascript
const { id } = await CMSteps.query().insert({
  title: 'unit tests',
  body: 'unit tests',
  campaign_id: campaignId,
  action_type: 1
});
```

### User Campaign Association
```javascript
await CMCampaignUsers.query().insert({
  campaign_id: campaignId,
  step_id: cardId,
  user_id: userId,
  departure_time: new Date().toISOString(),
  end_time: new Date().toISOString(),
  status: 1
});
```

## Test Suites

### 1. Get Suggestion Card
**Endpoint**: `GET /suggestion_card/{id}`

#### Successful Retrieval
**Test Case**: Get suggestion card by ID

**Expected Response**:
```json
{
  "result": "success",
  "data": {
    "notification_type": 12,
    "points": 0,
    "status": 1
  }
}
```

**Response Properties**:
- **notification_type**: 12 (suggestion card type)
- **points**: Reward points associated with card
- **status**: Current card status (1 = active)

#### Error Cases
1. **Authentication Error (10003)**:
   - Missing Authorization header
   - Returns "Token required" message

2. **Card Not Found (23027)**:
   - Invalid card ID
   - Returns "Not found card" message

### 2. Delete/Mark Suggestion Card
**Endpoint**: `DELETE /suggestion_card/{id}`

#### Status Update Process
1. **Mark as Received**: DELETE operation changes status
2. **Status Verification**: GET confirms status change
3. **Final Status**: Status becomes 3 (received)

#### Successful Deletion
**Test Flow**:
1. Send DELETE request to mark card as received
2. Verify empty response body
3. GET card to confirm status changed to 3

**Status Transition**:
```
Status 1 (active) -> Status 3 (received)
```

#### Error Cases
1. **Authentication Error (10003)**:
   - Missing Authorization header
   - Returns "Token required" message

2. **Invalid Parameters (90001)**:
   - Non-existent card ID
   - Returns "Invalid parameters" message

## Status Management

### Card Status Values
- **Status 1**: Active suggestion card
- **Status 3**: Received/acknowledged card

### Status Lifecycle
1. **Creation**: Card created with status 1
2. **Display**: User sees active suggestion
3. **Acknowledgment**: User "deletes" card (marks as received)
4. **Completion**: Status updated to 3

## Campaign Integration

### Campaign Components
- **Campaign ID**: Unique campaign identifier
- **Step ID**: Individual campaign step/card
- **Action Type**: Type of action required (1 = standard)
- **Time Tracking**: departure_time and end_time

### User Participation
- **User-Campaign Link**: CMCampaignUsers table
- **Record Tracking**: CMUserRecords for interactions
- **Points System**: Reward points for completion

## API Response Format

### Success Response
```json
{
  "result": "success",
  "data": {
    "notification_type": 12,
    "points": 0,
    "status": 1
  }
}
```

### Error Response
```json
{
  "result": "fail",
  "error": {
    "code": 23027,
    "msg": "Not found card"
  }
}
```

## Error Codes
- **10003**: Authentication required (missing token)
- **23027**: Card not found
- **90001**: Invalid parameters

## Data Cleanup

### Cleanup Process
```javascript
// Remove test data in proper order
await CMSteps.query().where('id', '=', cardId).delete();
await CMCampaignUsers.query()
  .where({ user_id: userId, step_id: cardId })
  .delete();
await CMUserRecords.query()
  .where({ user_id: userId, campaign_id: campaignId })
  .delete();
```

### Cleanup Order
1. Remove user records
2. Remove user-campaign associations
3. Remove campaign steps

## Business Logic

### Suggestion Card Purpose
- **User Engagement**: Encourage specific transportation behaviors
- **Gamification**: Points-based reward system
- **Campaign Management**: Track user participation
- **Notifications**: Type 12 notifications for suggestions

### User Experience Flow
1. **Receive Card**: User gets suggestion notification
2. **View Details**: User accesses card content
3. **Acknowledge**: User marks card as received
4. **Tracking**: System records user interaction

## Integration Points

### Campaign Management System
- **Step Definition**: CMSteps defines card content
- **User Assignment**: CMCampaignUsers links users to campaigns
- **Progress Tracking**: CMUserRecords tracks interactions

### Notification System
- **Type 12**: Suggestion card notification type
- **Status Management**: Tracks read/unread state
- **User Interface**: Cards displayed in app notifications

## Testing Best Practices

### Data Isolation
- **Unique IDs**: Test uses specific user and campaign IDs
- **Complete Cleanup**: All test data removed after execution
- **No Interference**: Tests don't affect production data

### Comprehensive Coverage
- **Happy Path**: Successful card retrieval and status update
- **Error Handling**: Authentication and validation errors
- **State Verification**: Confirms status changes persist

### Real-world Simulation
- **Complete Workflow**: Tests full card lifecycle
- **Authentication**: Proper JWT token handling
- **Database Integration**: Real model operations

This test suite ensures the suggestion card system functions correctly for user engagement campaigns, maintains proper status tracking, and provides appropriate error handling for the TSP API's gamification features.