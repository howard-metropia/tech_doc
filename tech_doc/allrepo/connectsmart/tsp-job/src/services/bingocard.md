# TSP Job Service: bingocard.js

## Quick Summary

The `bingocard.js` service manages incentive bingo card challenges for the ConnectSmart platform. It handles automated enrollment of users into gamified reward campaigns based on specific criteria such as app usage, user preferences, and market segmentation. The service provides multiple enrollment strategies including notification-based, batch processing, and specialized testing modes.

## Technical Analysis

### Core Architecture

The service implements a comprehensive incentive management system with the following key components:

- **User Filtering System**: Multi-layered filtering based on app version, market, incentive type, and notification history
- **Campaign Management**: Integration with external incentive admin API for campaign retrieval and user enrollment
- **Persona Mapping**: Translation of user travel preferences to campaign personas
- **Batch Processing**: Support for both individual and bulk user enrollment operations

### Key Functions

#### addToChallenge(notifyUsers)
Primary function for enrolling users into bingo card challenges based on notification queue:
```javascript
// Filters users by incentive type and market (HCS only)
notifyUsers = notifyUsers.filter((user) => 
  user.incentive_type === 'incentive open app' && user.market === 'HCS'
);

// Ensures first-time users only
notifyUsers = await knex('incentive_notify_queue')
  .whereIn('user_id', notifyUsers.map((user) => user.user_id))
  .having(knex.raw('count(id)'), '=', 1);
```

#### addToChallengeBatch()
Batch processing function for users who opened the app with version 124+:
```javascript
const notifyUsers = await knex('auth_user')
  .leftJoin('user_config', 'user_config.user_id', 'auth_user.id')
  .join('app_data', 'app_data.user_id', 'user_config.user_id')
  .whereRaw('cast(regexp_substr(auth_user.app_version, \'[0-9]{2,}\') as float) >= 124')
  .where('app_data.user_action', 'OpenApp');
```

#### Travel Mode Persona Mapping
The service maps user preferences to campaign personas:
```javascript
const map = {
  'carpooling': 'carpool',
  'cycling': 'biking',
  'public_transit': 'transit',
  'driving': 'driving',
};
```

### Database Integration

The service interacts with multiple database tables:
- `incentive_notify_queue`: Tracks notification history
- `user_config`: Stores user preferences and travel modes
- `auth_user`: User authentication and app version data
- `app_data`: User activity tracking

### External API Integration

Communicates with the incentive admin service:
```javascript
// Get current campaigns
const resp = await superagent
  .get(`${config.incentiveAdminUrl}/campaigns/current`);

// Enroll users in specific bingo card
const resp = await superagent
  .post(`${config.incentiveAdminUrl}/bingocards/${campaign.bingocard_id}`)
  .send(targetUsers);
```

## Usage/Integration

### Scheduled Execution

The service functions are typically called by scheduled jobs:

1. **addToChallenge**: Processes notification-triggered enrollments
2. **addToChallengeBatch**: Handles bulk enrollments for active users
3. **addToChallengeSBTest**: Special testing mode for non-onboarding campaigns
4. **addToChallengePD**: Production deployment with enhanced filtering

### User Data Structure

Each enrolled user includes:
```javascript
{
  user_id: integer,
  persona: string, // 'carpool', 'biking', 'transit', 'driving'
  permissions: {
    calendar: boolean,
    notification: boolean,
  }
}
```

### Campaign Filtering

Campaigns are filtered by generation weight for targeting:
- Onboarding campaigns: `gen_weight` contains 'onboard'
- Regular campaigns: `gen_weight` does not contain 'onboard'

## Dependencies

### External Packages
- `@maas/core/mysql`: Database connectivity for portal database
- `config`: Configuration management for incentive settings
- `superagent`: HTTP client for external API communication
- `@maas/core/log`: Centralized logging system

### Configuration Requirements
```javascript
config.incentive = {
  incentiveAdminUrl: 'https://admin.example.com' // External incentive API endpoint
}
```

### Database Schema Dependencies
- **incentive_notify_queue**: User notification tracking
- **user_config**: User preferences and travel modes
- **auth_user**: User authentication and app version
- **app_data**: User activity logs

## Code Examples

### Basic User Enrollment
```javascript
const { addToChallenge } = require('./bingocard');

// Enroll users from notification queue
const notifyUsers = [
  {
    user_id: 12345,
    incentive_type: 'incentive open app',
    market: 'HCS',
    per_calendar: 1,
    per_push_notification: 1
  }
];

const results = await addToChallenge(notifyUsers);
console.log('Enrollment results:', results);
```

### Batch Processing
```javascript
// Process all eligible users in batch
const batchResults = await addToChallengeBatch();
console.log(`Processed ${batchResults.length} users`);
```

### Campaign Retrieval
```javascript
// Get current onboarding campaigns
const onboardCampaigns = await getCurrentCampaign('onboard');

// Get all current campaigns
const allCampaigns = await getCurrentCampaign();
```

### Error Handling Pattern
```javascript
try {
  const results = await addToChallenge(users);
  logger.info(`[addToChallenge] results: ${JSON.stringify(results)}`);
} catch (e) {
  logger.error(`[addToChallenge] error: ${e.message}`);
  logger.info(`[addToChallenge] stack: ${e.stack}`);
}
```

The bingocard service provides a robust foundation for managing user engagement through gamified incentive campaigns, with comprehensive filtering, error handling, and integration capabilities for the ConnectSmart platform's incentive system.