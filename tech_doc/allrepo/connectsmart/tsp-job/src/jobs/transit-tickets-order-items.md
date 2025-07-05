# transit-tickets-order-items.js

## Overview
Job for synchronizing Bytemark transit ticket order items from external API to local database. Processes orders without associated items and retrieves detailed pass information for each order.

## File Location
- **Path**: `/allrepo/connectsmart/tsp-job/src/jobs/transit-tickets-order-items.js`
- **Module Type**: Scheduled Job
- **Export**: Job configuration with async function

## Key Dependencies
- `@maas/core/mysql` - MySQL database connection (portal)
- `@maas/core/log` - Logging utility
- `config` - Application configuration
- `axios` - HTTP client (imported but not directly used)
- `@maas/services` - BytemarkManager service

## Core Functions

### Main Processing Function
Synchronizes Bytemark order items for orders that lack detailed item records.

**Process Flow:**
1. Query orders missing item details
2. Group orders by user for efficient processing
3. Fetch order details from Bytemark API
4. Extract and store order item information

## Job Configuration

### Inputs
No input parameters required.

### Target Criteria
Processes orders that meet all conditions:
- Missing records in `bytemark_order_items` table
- Have `amount = 0` (free orders)
- Have valid OAuth tokens

## Processing Flow

### 1. Data Retrieval
```sql
SELECT bytemark_orders.id, bytemark_orders.order_uuid, 
       bytemark_orders.user_id, bytemark_orders.oauth_token
FROM bytemark_orders
JOIN bytemark_tokens ON bytemark_orders.user_id = bytemark_tokens.user_id
LEFT JOIN bytemark_order_items ON bytemark_orders.id = bytemark_order_items.order_id
WHERE bytemark_order_items.id IS NULL 
  AND bytemark_orders.amount = '0'
```

### 2. User-Based Grouping
```javascript
const data = rows.reduce((p, c) => {
  if (!p[c.user_id])
    p[c.user_id] = {
      oauth_token: c.oauth_token,
      orders: [],
    };
  p[c.user_id].orders.push({ id: c.id, order_uuid: c.order_uuid });
  return p;
}, {});
```

### 3. Bytemark API Integration
For each user:
- Initialize BytemarkManager with configuration
- Paginate through Bytemark API to find matching orders
- Extract order items and pass details

### 4. Data Storage
For each matched order:
- Extract product and pass information
- Insert records into `bytemark_order_items` table

## Bytemark Integration

### BytemarkManager Configuration
```javascript
const bytemark = new BytemarkManager({
  project: process.env.PROJECT_NAME || 'connectsmart',
  stage: process.env.PROJECT_STAGE || 'production',
  customerApi: config.vendor.bytemark.url.customerApi,
  accountApi: config.vendor.bytemark.url.accountApi,
  logger,
  slackToken: process.env.SLACK_BOT_TOKEN,
  slackChannelId: process.env.SLACK_CHANNEL_ID,
  originApi: 'tsp-job/transit-tickets-order-items',
  clientId: config.vendor.bytemark.clientId,
  clientSecret: config.vendor.bytemark.clientSecret
});
```

### API Pagination
- **Page Size**: 10 orders per request
- **Retry Logic**: Maximum 5 attempts per user
- **Matching Strategy**: Compare local order_uuid with API response

## Data Models

### bytemark_orders Table (Source)
```javascript
{
  id: number,
  order_uuid: string,
  user_id: number,
  amount: string,
  // Additional fields...
}
```

### bytemark_order_items Table (Target)
```javascript
{
  order_id: number,
  order_uuid: string,
  oauth_token: string,
  product_uuid: string,
  pass_uuid: string
}
```

### Bytemark API Response Structure
```javascript
{
  orders: [
    {
      uuid: string,
      order_items: [
        {
          product: {
            uuid: string
          },
          passes: [
            {
              uuid: string
            }
          ]
        }
      ]
    }
  ],
  total_count: number
}
```

## Business Logic

### Order Matching
- Compares local `order_uuid` with Bytemark API `uuid`
- Handles multiple orders per user efficiently
- Tracks matching progress to optimize API calls

### Item Extraction
```javascript
for (const orderItem of bytemarkOrder.order_items) {
  for (const pass of orderItem.passes) {
    const insert = {
      order_id: localOrderId,
      order_uuid: bytemarkOrder.uuid,
      oauth_token: oauthToken,
      product_uuid: orderItem.product.uuid,
      pass_uuid: pass.uuid
    };
    await knex('bytemark_order_items').insert(insert);
  }
}
```

### Processing Limits
- **Retry Limit**: 5 attempts per user
- **Pagination**: Handles large order lists through pagination
- **Performance**: Groups by user to minimize API calls

## Error Handling
- Try-catch wrapper around entire processing
- Comprehensive error logging
- Graceful handling of API failures
- Continuation of processing despite individual failures

## Performance Optimizations
- User-based grouping reduces API calls
- Pagination prevents memory issues with large datasets
- Retry logic handles temporary API failures
- Efficient matching algorithms

## Integration Points
- Bytemark transit ticket system
- OAuth token management
- Order management system
- Pass inventory tracking
- User account system

## Configuration Dependencies
- Bytemark API credentials and endpoints
- Slack integration for notifications
- Environment-specific settings
- OAuth token management

## Monitoring and Alerting
- Slack integration for error notifications
- Comprehensive logging of processing status
- Match success/failure tracking
- API response monitoring

## Usage Scenarios
- Daily synchronization of new orders
- Recovery processing for failed synchronizations
- Audit and reconciliation processes
- Transit pass inventory management

## Notes
- Focuses on free orders (amount = 0)
- Requires valid OAuth tokens for API access
- Designed for incremental processing
- Supports high-volume order processing
- Integrates with broader transit ticket management system