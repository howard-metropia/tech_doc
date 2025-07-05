# Check Bytemark Tickets Job

## Overview
Job that validates Bytemark transit ticket integrity by checking for abnormal passes that exist without corresponding orders.

## File Location
`/src/jobs/check-bytemark-tickets.js`

## Dependencies
- `config` - Configuration management
- `@maas/core/log` - Logging framework
- `@app/src/services/BytemarkTokens` - Bytemark token management
- `@app/src/helpers/bytemark-ticket-checker` - Ticket validation helpers
- `@maas/services/src/bytemark` - Bytemark service manager

## Job Configuration

### Inputs
```javascript
inputs: {}
```
No input parameters required.

### Bytemark Configuration
```javascript
const bytemarkConfig = {
  project: config.get('app.project'),
  stage: process.env.PROJECT_STAGE,
  customerApi: config.vendor.bytemark.url.customerApi,
  accountApi: config.vendor.bytemark.url.accountApi,
  logger,
  slackToken: process.env.SLACK_BOT_TOKEN,
  slackChannelId: process.env.SLACK_CHANNEL_ID,
  originApi: 'tsp-job/check-bytemark-tickets',
  clientId: config.vendor.bytemark.clientId,
  clientSecret: config.vendor.bytemark.clientSecret
};
```

## Core Functionality

### Validation Process
1. **Token Retrieval**
   ```javascript
   const tokens = await getUserTokens();
   ```
   - Gets all user tokens for Bytemark API access
   - Returns early if no tokens available

2. **Pass and Order Validation**
   ```javascript
   const passUuids = await getPassUuids(tokenItem.token);
   const orderUuids = await getOrderUuids(tokenItem.token);
   ```
   - Retrieves pass UUIDs for each user token
   - Retrieves order UUIDs for comparison

3. **Abnormal Ticket Detection**
   ```javascript
   if (!orderUuids || !orderUuids.length) {
     // if passes exist but no orders, it has to be abnormal passes
     const data = extractErrorData(tokenItem, passUuids);
     abnormalTickets.push(data);
   }
   ```

### Validation Logic

#### Case 1: Passes Without Orders
- **Condition**: Passes exist but no corresponding orders
- **Action**: Flag all passes as abnormal
- **Reason**: Valid passes should have associated purchase orders

#### Case 2: Orphaned Passes
```javascript
const abnormalPass = passUuids.filter(passUUID => !orderUuids.includes(passUUID));
```
- **Condition**: Pass UUIDs that don't match any order UUIDs
- **Action**: Flag mismatched passes as abnormal
- **Reason**: Each pass should correspond to a purchase order

### Error Reporting
```javascript
if (abnormalTickets.length > 0) {
  const msg = {
    content: 'we\'ve got abnormal Bytemark ticket(s)',
    data: abnormalTickets
  };
  logger.error(msg);
}
```

## Service Integration

### Bytemark Manager
- **Purpose**: Manages Bytemark API interactions
- **Configuration**: Uses environment-specific settings
- **Authentication**: Handles OAuth client credentials

### Helper Functions
- **setManager()**: Configures Bytemark manager instance
- **getOrderUuids()**: Retrieves order identifiers
- **getPassUuids()**: Retrieves pass identifiers
- **extractErrorData()**: Formats error data for reporting

## Data Validation

### Token Processing
- Processes all user tokens in parallel using Promise.all
- Handles missing or invalid tokens gracefully
- Continues processing if individual tokens fail

### UUID Matching
- Compares pass UUIDs against order UUIDs
- Identifies orphaned passes without purchase records
- Maintains data integrity for transit ticketing system

## Error Handling
- Validates Bytemark manager initialization
- Handles missing token scenarios
- Logs abnormal tickets for investigation
- Continues processing despite individual token failures

## Slack Integration
- **Token**: Uses SLACK_BOT_TOKEN for authentication
- **Channel**: Posts to configured SLACK_CHANNEL_ID
- **Notifications**: Alerts team to ticket anomalies

## Usage Context
- **Transit Ticketing**: Validates Bytemark transit pass integrity
- **Data Quality**: Ensures ticket-order relationship consistency
- **Fraud Detection**: Identifies potentially fraudulent passes
- **System Monitoring**: Monitors transit ticketing system health

## Related Components
- Bytemark API integration
- Transit ticketing system
- User token management
- Error monitoring and alerting

## Schedule Context
Typically scheduled to run regularly to monitor Bytemark ticket integrity and detect data inconsistencies in the transit ticketing system.