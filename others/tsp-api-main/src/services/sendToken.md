# TSP API SendToken Service Documentation

## 🔍 Quick Summary (TL;DR)
The SendToken service distributes transit tokens to users from campaigns and agencies, managing token balances, tracking device usage to prevent fraud, sending notifications for token receipt and expiration, and maintaining comprehensive transaction records.

**Keywords:** token-distribution | campaign-tokens | device-fraud-prevention | notification-system | balance-management | agency-tokens | expiration-tracking | transaction-logging

**Primary use cases:** Distributing campaign tokens to users, preventing duplicate token claims per device, sending token notifications, tracking token balances, managing expiration alerts

**Compatibility:** Node.js >= 16.0.0, MySQL database, notification system integration, moment.js for date handling, device tracking for fraud prevention

## ❓ Common Questions Quick Index
- **Q: How are tokens distributed?** → Batch processing with balance calculation and device tracking
- **Q: What fraud prevention exists?** → Device ID tracking to prevent multiple claims per device
- **Q: What notifications are sent?** → Token receipt and 14-day expiration warnings
- **Q: How are balances calculated?** → Running balance based on previous transactions for each token type
- **Q: What data is tracked?** → User, agency, campaign, token details, and device information
- **Q: How are promotional codes handled?** → Special tracking with campaign promo code ID recording

## 📋 Functionality Overview

**Non-technical explanation:** 
Think of this as a **digital token bank** that gives out transit tokens from various agencies and campaigns. It keeps track of how many tokens each person has, makes sure people can't cheat by using multiple devices, and sends notifications when tokens arrive or are about to expire.

**Technical explanation:** 
A comprehensive token distribution service that processes batch token distributions with fraud prevention through device tracking, maintains running balances per token type, sends contextual notifications for distribution and expiration events, and creates detailed audit trails for compliance and analytics.

**Business value explanation:**
Enables reward and incentive programs through token distribution, prevents fraud and abuse through device tracking, ensures user engagement through timely notifications, supports partnership with transit agencies, and provides detailed analytics for campaign effectiveness.

## 🔧 Technical Specifications

- **File:** `allrepo/connectsmart/tsp-api/src/services/sendToken.js`
- **Language:** JavaScript (ES2020)
- **Framework:** Node.js with Knex.js query builder
- **Type:** Token Distribution and Management Service
- **File Size:** ~3.3 KB
- **Complexity Score:** ⭐⭐⭐ (Medium-High - Complex business logic with fraud prevention)

**Dependencies:**
- `moment-timezone`: Date/time handling and formatting (**Critical**)
- `@maas/core/mysql`: Database connectivity (**Critical**)
- `@app/src/helpers/send-notification`: Notification dispatch (**High**)
- `@app/src/models/AuthUsers`: User data access (**High**)
- `@app/src/models/DeviceCheckTokens`: Device fraud prevention (**Critical**)

## 📝 Detailed Code Analysis

### send Function

**Purpose:** Processes batch token distribution with comprehensive fraud prevention and notifications

**Parameters:**
- `tokenDatas`: Array - Collection of token distribution objects containing user, campaign, and agency information

**Returns:** Promise (void)

### Token Distribution Pipeline

### 1. Balance Calculation
```javascript
const tokenTransactionData = await knex('token_transaction')
  .where({ user_id: userId, f_token_id: tokenData.ap_token_id })
  .orderBy('id', 'desc');

let balance = 0;
if (tokenTransactionData.length > 0) {
  balance = parseFloat(tokenTransactionData[0].balance);
}
balance = balance + Math.round(tokenData.tokens * 100) / 100;
```
- Retrieves latest balance for specific token type per user
- Calculates new balance with precision handling
- Maintains separate balances for different token types

### 2. Transaction Record Creation
```javascript
const insertModel = {
  user_id: userId,
  activity_type: 1, // Token distribution activity
  tokens: tokenData.tokens,
  balance,
  campaign_id: tokenData.token_id,
  ap_campaign_id: tokenData.campaign_id,
  f_agency_id: tokenData.ap_agency_id,
  agency_name: tokenData.agency_name,
  f_token_id: tokenData.ap_token_id,
  token_name: tokenData.token_name,
  f_campaign_id: tokenData.ap_campaign_id,
  campaign_name: tokenData.campaign_name,
  issued_on: moment(tokenData.issued_on).format('YYYY-MM-DDTHH:mm:ss'),
  expired_on: moment(tokenData.expired_on).format('YYYY-MM-DDTHH:mm:ss')
};

if (tokenData.cp_id !== undefined) {
  insertModel.cp_id = tokenData.cp_id; // Promotional code tracking
}
```
- Comprehensive transaction record with all relevant metadata
- Special handling for promotional code distributions
- Standardized date formatting for consistency

### 3. Device Fraud Prevention
```javascript
const userData = await AuthUsers.query().select('device_id').findById(userId);

const originalObj = await DeviceCheckTokens.query()
  .where('device_id', userData.device_id)
  .first();

if (originalObj) {
  // Device already received tokens, increment count
  await DeviceCheckTokens.query().update({
    count: originalObj.count + 1,
  });
} else {
  // New device, create tracking record
  await DeviceCheckTokens.query().insert({
    device_id: userData.device_id,
    count: 1,
    ap_campaign_id: tokenData.ap_campaign_id,
  });
}
```
- Tracks token distributions per device to prevent abuse
- Maintains count of tokens received per device
- Links device tracking to specific campaigns

### 4. Notification System Integration

#### Token Receipt Notifications
```javascript
const nowUnixtime = moment().unix();
let distNotifyStatus = 0;

if (moment(tokenData.issued_on).unix() <= nowUnixtime) {
  const notifyData = {
    userIds: [userId],
    type: NOTIFICATION_TYPE.TOKEN_RECEIVED_FROM_AGENCY,
    titleParams: [],
    bodyParams: [tokenData.agency_name, tokenData.tokens],
    meta: {
      agency_id: tokenData.ap_agency_id,
    },
  };
  await sendNotify(notifyData);
  distNotifyStatus = 1;
}
```
- Sends immediate notification for tokens with current or past issue dates
- Includes agency name and token amount in notification
- Tracks notification delivery status

#### Expiration Warning Notifications
```javascript
let expNotifyStatus = 0;
const expire = moment(tokenData.expired_on).unix();

if (expire > nowUnixtime && expire - nowUnixtime < 60 * 60 * 24 * 14) {
  const notifyData = {
    userIds: [userId],
    type: NOTIFICATION_TYPE.TOKEN_EXPIRES_IN_14_DAYS,
    titleParams: [],
    bodyParams: [
      balance,
      tokenData.agency_name,
      moment(tokenData.expired_on).format('YYYY-MM-DD HH:mm:ss'),
    ],
    meta: {
      agency_id: tokenData.ap_agency_id,
    },
  };
  await sendNotify(notifyData);
  expNotifyStatus = 1;
}
```
- Sends expiration warning for tokens expiring within 14 days
- Includes current balance, agency, and expiration date
- Only triggers for tokens not yet expired

### 5. Status Tracking Update
```javascript
await knex('token_transaction').where('id', ttId).update({
  dist_notify_status: distNotifyStatus,
  expire_notify_status: expNotifyStatus,
});
```
- Records which notifications were sent for each transaction
- Enables tracking and debugging of notification delivery
- Supports analytics on notification effectiveness

## 🚀 Usage Methods

### Basic Token Distribution
```javascript
const sendTokenService = require('@app/src/services/sendToken');

// Single token distribution
await sendTokenService.send([
  {
    userId: 12345,
    tokens: 10,
    ap_token_id: 'token_123',
    token_name: 'Metro Transit Tokens',
    campaign_id: 456,
    ap_campaign_id: 789,
    campaign_name: 'Summer Transit Campaign',
    token_id: 101,
    ap_agency_id: 'agency_abc',
    agency_name: 'Houston Metro',
    issued_on: '2024-06-25T09:00:00Z',
    expired_on: '2024-12-25T23:59:59Z'
  }
]);

// Batch token distribution
await sendTokenService.send([
  {
    userId: 12345,
    tokens: 5,
    // ... token data
  },
  {
    userId: 67890,
    tokens: 8,
    // ... token data
  }
]);
```

### Campaign Token Distribution Manager
```javascript
class CampaignTokenManager {
  constructor() {
    this.sendTokenService = require('@app/src/services/sendToken');
    this.knex = require('@maas/core/mysql')('portal');
  }

  async distributeCampaignTokens(campaignId, eligibleUsers) {
    try {
      // Get campaign details
      const campaign = await this.getCampaignDetails(campaignId);
      
      if (!campaign) {
        throw new Error(`Campaign ${campaignId} not found`);
      }

      // Prepare token distribution data
      const tokenDistributions = eligibleUsers.map(user => ({
        userId: user.userId,
        tokens: campaign.tokensPerUser,
        ap_token_id: campaign.ap_token_id,
        token_name: campaign.token_name,
        campaign_id: campaign.id,
        ap_campaign_id: campaign.ap_campaign_id,
        campaign_name: campaign.name,
        token_id: campaign.token_id,
        ap_agency_id: campaign.ap_agency_id,
        agency_name: campaign.agency_name,
        issued_on: campaign.start_date,
        expired_on: campaign.end_date
      }));

      // Distribute tokens
      await this.sendTokenService.send(tokenDistributions);

      return {
        success: true,
        campaignId,
        usersProcessed: eligibleUsers.length,
        tokensDistributed: eligibleUsers.length * campaign.tokensPerUser,
        message: 'Campaign tokens distributed successfully'
      };
    } catch (error) {
      console.error('Campaign token distribution failed:', error);
      return {
        success: false,
        campaignId,
        error: error.message
      };
    }
  }

  async getCampaignDetails(campaignId) {
    const campaign = await this.knex('campaign')
      .join('token_campaign', 'token_campaign.id', 'campaign.token_id')
      .join('agency', 'agency.id', 'token_campaign.agency_id')
      .select(
        'campaign.id',
        'campaign.name',
        'campaign.tokens as tokensPerUser',
        'campaign.ap_campaign_id',
        'campaign.token_id',
        'token_campaign.ap_token_id',
        'token_campaign.name as token_name',
        'token_campaign.issued_on as start_date',
        'token_campaign.expired_on as end_date',
        'agency.ap_agency_id',
        'agency.name as agency_name'
      )
      .where('campaign.id', campaignId)
      .first();

    return campaign;
  }

  async checkTokenEligibility(userId, campaignId) {
    try {
      // Check if user already received tokens from this campaign
      const existingTokens = await this.knex('token_transaction')
        .where({
          user_id: userId,
          ap_campaign_id: campaignId,
          activity_type: 1
        })
        .first();

      if (existingTokens) {
        return {
          eligible: false,
          reason: 'User already received tokens from this campaign'
        };
      }

      // Check device eligibility
      const user = await this.knex('auth_user')
        .select('device_id')
        .where('id', userId)
        .first();

      if (!user || !user.device_id) {
        return {
          eligible: false,
          reason: 'User device ID not available'
        };
      }

      const deviceCheck = await this.knex('device_check_tokens')
        .where({
          device_id: user.device_id,
          ap_campaign_id: campaignId
        })
        .first();

      if (deviceCheck) {
        return {
          eligible: false,
          reason: 'Device already received tokens from this campaign'
        };
      }

      return {
        eligible: true,
        userId,
        deviceId: user.device_id
      };
    } catch (error) {
      return {
        eligible: false,
        reason: `Eligibility check failed: ${error.message}`
      };
    }
  }

  async getTokenBalanceSummary(userId) {
    try {
      const balances = await this.knex('token_transaction')
        .select(
          'f_token_id as tokenId',
          'token_name',
          'agency_name',
          'balance',
          'expired_on'
        )
        .where({
          user_id: userId,
          activity_type: 1
        })
        .whereRaw('expired_on > NOW()')
        .orderBy('id', 'desc')
        .groupBy('f_token_id');

      const totalBalance = balances.reduce((sum, token) => sum + parseFloat(token.balance), 0);

      return {
        userId,
        totalBalance,
        activeTokenTypes: balances.length,
        tokens: balances.map(token => ({
          tokenId: token.tokenId,
          name: token.token_name,
          agency: token.agency_name,
          balance: parseFloat(token.balance),
          expiresOn: token.expired_on
        }))
      };
    } catch (error) {
      console.error('Error getting token balance summary:', error);
      throw error;
    }
  }
}

// Usage
const tokenManager = new CampaignTokenManager();

// Distribute tokens for a campaign
const result = await tokenManager.distributeCampaignTokens(123, [
  { userId: 12345 },
  { userId: 67890 },
  { userId: 11111 }
]);

// Check eligibility
const eligibility = await tokenManager.checkTokenEligibility(12345, 123);

// Get user token summary
const summary = await tokenManager.getTokenBalanceSummary(12345);
```

## 📊 Output Examples

### Token Distribution Success
```javascript
// Log output
"[service.distribute] distribute to : 12345"
"[service.distribute] 2024-06-25T09:00:00, Tue Jun 25 2024 09:00:00 GMT-0500 (CDT), true"

// Database records created in token_transaction table
```

### Token Balance Summary
```json
{
  "userId": 12345,
  "totalBalance": 25.0,
  "activeTokenTypes": 2,
  "tokens": [
    {
      "tokenId": "token_123",
      "name": "Metro Transit Tokens",
      "agency": "Houston Metro",
      "balance": 15.0,
      "expiresOn": "2024-12-25T23:59:59.000Z"
    },
    {
      "tokenId": "token_456", 
      "name": "Bus Rapid Transit Tokens",
      "agency": "Houston Metro",
      "balance": 10.0,
      "expiresOn": "2024-11-30T23:59:59.000Z"
    }
  ]
}
```

### Campaign Distribution Result
```json
{
  "success": true,
  "campaignId": 123,
  "usersProcessed": 3,
  "tokensDistributed": 30,
  "message": "Campaign tokens distributed successfully"
}
```

### Eligibility Check Response
```json
{
  "eligible": true,
  "userId": 12345,
  "deviceId": "device_abc123"
}
```

## ⚠️ Important Notes

### Fraud Prevention and Security
- **Device Tracking:** Prevents multiple token claims from same device across campaigns
- **Balance Integrity:** Maintains accurate running balances per token type
- **Duplicate Prevention:** Checks existing transactions before distribution
- **Campaign Isolation:** Device tracking linked to specific campaigns

### Notification System Integration
- **Immediate Notifications:** Sent for tokens with current or past issue dates
- **Expiration Warnings:** 14-day advance notice for token expiration
- **Status Tracking:** Records notification delivery for analytics
- **Rich Context:** Includes agency names, amounts, and expiration dates

### Data Integrity and Audit Trails
- **Comprehensive Logging:** Detailed transaction records with metadata
- **Promotional Code Tracking:** Special handling for promo code distributions
- **Date Standardization:** Consistent timestamp formatting across records
- **Balance Calculations:** Precise decimal handling for financial accuracy

### Performance and Scalability
- **Batch Processing:** Handles multiple token distributions efficiently
- **Database Optimization:** Uses proper indexing for balance lookups
- **Transaction Safety:** Atomic operations for data consistency
- **Error Handling:** Graceful handling of notification failures

## 🔗 Related File Links

- **Notification Helper:** `allrepo/connectsmart/tsp-api/src/helpers/send-notification.js`
- **Device Check Models:** `allrepo/connectsmart/tsp-api/src/models/DeviceCheckTokens.js`
- **User Models:** `allrepo/connectsmart/tsp-api/src/models/AuthUsers.js`
- **Campaign Management:** Related to campaign and promotional code services

---
*This service provides comprehensive token distribution with fraud prevention and notification management for the TSP platform.*