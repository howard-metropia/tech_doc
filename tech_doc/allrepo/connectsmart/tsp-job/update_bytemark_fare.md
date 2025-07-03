# Update Bytemark Fare Job

## Quick Summary
**Purpose**: Synchronizes transit fare information from Bytemark's product catalog into the local database for pricing and ticketing operations.

**Key Features**:
- Fetches complete fare product catalog from Bytemark API
- Upserts fare data to maintain current pricing
- Comprehensive field mapping for all product attributes
- Error logging with Slack integration

**Functionality**: Periodically retrieves the full product catalog from Bytemark's API and updates the local MongoDB collection with current fare information, including prices, descriptions, GTFS mappings, and product configurations.

## Technical Analysis

### Code Structure
The job implements a comprehensive fare synchronization system:

```javascript
module.exports = {
  inputs: {},
  fn: async () => {
    await job();
  }
};
```

### Implementation Details

1. **Configuration Setup**:
   ```javascript
   const bytemarkConfig = {
     project: config.get('app.project'),
     stage: process.env.PROJECT_STAGE,
     customerApi: config.vendor.bytemark.url.customerApi,
     accountApi: config.vendor.bytemark.url.accountApi,
     logger,
     slackToken: process.env.SLACK_BOT_TOKEN,
     slackChannelId: process.env.SLACK_CHANNEL_ID,
     originApi: 'tsp-job/update_bytemark_fare',
     clientId: config.vendor.bytemark.clientId,
     clientSecret: config.vendor.bytemark.clientSecret,
   };
   ```

2. **Product Field Mapping**:
   The job maps 20+ fields from Bytemark's product API:
   - **Identifiers**: `uuid`, `base_product`, `legacy_product`
   - **Pricing**: `list_price`, `sale_price`, `cost_price`
   - **Descriptions**: `short_description`, `long_description`, `name`
   - **Configuration**: `entries`, `list_priority`, `theme`, `published`
   - **Features**: `requiresUserPhotoCheck`, `shipping_enabled`, `subscription`
   - **Transit Integration**: `gtfs_fare_id`
   - **UI Elements**: `product_image_path`, `alert_message`
   - **Type Classification**: `type`, `sub_type`

3. **Data Processing Flow**:
   ```javascript
   const job = async () => {
     try {
       const bytemark = new BytemarkManager(bytemarkConfig);
       const response = await bytemark.productSearch();
       
       if (response?.data?.results?.length > 0) {
         const fares = response.data.results;
         
         for (const fare of fares) {
           const fareData = {
             uuid: fare.uuid,
             entries: fare.entries,
             // ... all field mappings
           };
           
           await bytemarkFare.findOneAndUpdate(
             { uuid: fare.uuid }, 
             fareData, 
             { upsert: true }
           );
         }
       }
     } catch(e) {
       logger.warn(`[update_bytemark_fare] error: ${e.message}`);
       logger.debug(`[update_bytemark_fare] stack: ${e.stack}`);
     }
   };
   ```

### Database Operations

1. **Upsert Strategy**:
   - Uses `findOneAndUpdate` with `upsert: true`
   - Ensures no duplicate products by UUID
   - Updates existing records or creates new ones

2. **MongoDB Model**:
   - Model: `BytemarkFare`
   - Primary key: `uuid`
   - Full document replacement on update

## Usage/Integration

### Scheduling Configuration
- **Frequency**: Every 6 hours (recommended)
- **Timing**: Staggered to avoid API rate limits
- **Priority**: Medium - fare updates are important but not time-critical

### Cron Expression
```
0 */6 * * * // Every 6 hours
```

### Integration Points
1. **Bytemark API**: Product catalog endpoint
2. **MongoDB**: Fare data storage
3. **Slack**: Error notifications
4. **GTFS System**: Fare ID mappings

## Dependencies

### Required Modules
```javascript
const config = require('config');
const { logger } = require('@maas/core/log');
const { bytemarkFare } = require('@app/src/models/BytemarkFare');
const BytemarkManager = require('@maas/services/src/bytemark');
```

### External Services
1. **Bytemark API**: 
   - Customer API endpoint
   - Account API endpoint
   - OAuth2 authentication

2. **Slack Integration**:
   - Bot token for notifications
   - Channel ID for alerts

### Configuration Requirements
```javascript
// Required configuration
{
  app: {
    project: 'connectsmart'
  },
  vendor: {
    bytemark: {
      url: {
        customerApi: 'https://api.bytemark.com/customer',
        accountApi: 'https://api.bytemark.com/account'
      },
      clientId: 'YOUR_CLIENT_ID',
      clientSecret: 'YOUR_CLIENT_SECRET'
    }
  }
}

// Environment variables
PROJECT_STAGE=production
SLACK_BOT_TOKEN=xoxb-...
SLACK_CHANNEL_ID=C...
```

## Code Examples

### Manual Execution
```javascript
// Run fare update manually
const job = require('./update_bytemark_fare');
await job.fn();
```

### Fare Data Structure
```javascript
// Example fare object
{
  uuid: '123e4567-e89b-12d3-a456-426614174000',
  name: 'Day Pass',
  short_description: 'Unlimited rides for one day',
  long_description: 'Valid for unlimited rides on all routes for 24 hours',
  list_price: 5.00,
  sale_price: 4.50,
  cost_price: 3.00,
  entries: 'unlimited',
  gtfs_fare_id: 'DAY_PASS',
  type: 'pass',
  sub_type: 'daily',
  published: true,
  theme: 'standard',
  list_priority: 1,
  requiresUserPhotoCheck: false,
  shipping_enabled: false,
  subscription: false,
  input_field_required: false,
  product_image_path: '/images/day-pass.png',
  alert_message: null,
  base_product: true,
  legacy_product: false,
  organization: 'METRO'
}
```

### Error Handling Patterns
```javascript
// Comprehensive error handling
try {
  // API call and processing
} catch(e) {
  // Log warning level for operational issues
  logger.warn(`[update_bytemark_fare] error: ${e.message}`);
  
  // Debug level for stack traces
  logger.debug(`[update_bytemark_fare] stack: ${e.stack}`);
  
  // Slack notification through BytemarkManager
  // Automatic via configured slackToken and slackChannelId
}
```

### API Response Validation
```javascript
// Safe navigation for API responses
if (response && response.data && response.data.results && response.data.results.length > 0) {
  // Process fares
} else {
  logger.warn('[update_bytemark_fare] No data found from Bytemark');
}
```

### Performance Considerations

1. **Batch Processing**:
   - Processes fares sequentially to avoid overwhelming database
   - Could be optimized with bulk operations if needed

2. **Memory Management**:
   - Processes one fare at a time
   - No accumulation of large datasets in memory

3. **API Rate Limiting**:
   - Single API call per job execution
   - 6-hour schedule prevents rate limit issues

### Monitoring Recommendations
- Track number of fares updated per run
- Monitor API response times
- Alert on consecutive failures
- Validate fare price changes above thresholds
- Check for removed products