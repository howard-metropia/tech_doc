# TSP API Promocode Service Documentation

## 🔍 Quick Summary (TL;DR)
The Promocode service validates promotional codes for token campaigns, performing comprehensive checks for code validity, user eligibility, device restrictions, time constraints, and usage history to prevent abuse and ensure proper campaign distribution.

**Keywords:** promocode-validation | campaign-tokens | device-fraud-prevention | promo-campaigns | token-distribution | usage-validation | time-constraints | case-sensitive-codes

**Primary use cases:** Validating promotional codes, preventing duplicate usage, enforcing campaign time limits, checking user registration timing, device-based fraud prevention, token campaign management

**Compatibility:** Node.js >= 16.0.0, MySQL database with complex campaign tables, Moment.js for timezone handling, comprehensive validation logic

## ❓ Common Questions Quick Index
- **Q: How are promocodes validated?** → Multi-step validation including existence, timing, user eligibility, and device checks
- **Q: Can codes be used multiple times?** → No, strict one-time use per user and per device enforcement
- **Q: Are codes case-sensitive?** → Yes, uses BINARY comparison for exact case matching
- **Q: What time constraints exist?** → Campaign periods and user registration timing windows
- **Q: How is fraud prevented?** → Device ID tracking and user registration date validation
- **Q: What happens if validation fails?** → Specific error codes for different failure scenarios

## 📋 Functionality Overview

**Non-technical explanation:** 
Think of this as a **digital coupon validator** that checks if a promotional code is real, not expired, not already used, and if the person trying to use it is eligible. It's like a bouncer at an exclusive event - it checks your invitation, makes sure you haven't already entered, and verifies you meet all the requirements.

**Technical explanation:** 
A comprehensive promotional code validation service that performs multi-layered checks including code existence verification, campaign timing validation, user eligibility assessment, device-based fraud prevention, and usage history tracking. Integrates with campaign management and token distribution systems.

**Business value explanation:**
Enables secure promotional campaigns, prevents fraud and abuse, ensures fair token distribution, supports marketing initiatives with proper validation, protects campaign budgets from misuse, and provides detailed tracking for campaign analytics and compliance.

## 🔧 Technical Specifications

- **File:** `allrepo/connectsmart/tsp-api/src/services/promocode.js`
- **Language:** JavaScript (ES2020)
- **Framework:** Node.js with Knex.js query builder
- **Type:** Promotional Code Validation Service
- **File Size:** ~3.7 KB
- **Complexity Score:** ⭐⭐⭐⭐ (High - Complex validation logic with fraud prevention)

**Dependencies:**
- `moment-timezone`: Date/time handling with timezone support (**High**)
- `@maas/core/mysql`: Database connectivity (**Critical**)
- `@app/src/models/AuthUsers`: User authentication model (**Critical**)
- `@app/src/models/DeviceCheckTokens`: Device fraud prevention model (**High**)
- `@app/src/static/error-code`: Error code definitions (**High**)

## 📝 Detailed Code Analysis

### checkCode Function

**Purpose:** Validates promotional codes with comprehensive fraud prevention

**Parameters:**
- `userId`: Number - User identifier attempting to use code
- `promoCode`: String - Promotional code to validate (case-sensitive)

**Returns:** Promise resolving to campaign and token data

**Complex Validation Pipeline:**

### 1. User Validation
```javascript
const userData = await AuthUsers.query()
  .select('id', 'created_on', 'device_id')
  .where('id', userId)
  .first();

if (userData === undefined) {
  throw new MaasError(ERROR_CODE.ERROR_USER_NOT_FOUND, ...);
}

if (!userData.device_id) {
  throw new MaasError(ERROR_CODE.ERROR_PROMO_CODE_ALREADY_USED, ...);
}
```
- Verifies user exists in system
- Ensures device ID is available for fraud prevention
- Missing device ID treated as potential fraud attempt

### 2. Promocode Lookup with Case Sensitivity
```javascript
const tokenData = await knex('campaign_promo_code')
  .select(/* extensive field list */)
  .innerJoin('campaign_promo_code_settings', ...)
  .innerJoin('campaign', ...)
  .innerJoin('token_campaign', ...)
  .innerJoin('agency', ...)
  .where(knex.raw('BINARY campaign_promo_code.promo_code'), promoCode)
  .first();
```
- Uses BINARY comparison for exact case matching
- Complex multi-table join to gather campaign information
- Returns comprehensive campaign and token metadata

### 3. Campaign Timing Validation
```javascript
const nowDate = moment().unix();

// Check if campaign has started
if (tokenData === undefined || nowDate < moment(tokenData.start_date).unix()) {
  throw new MaasError(ERROR_CODE.ERROR_PROMO_CODE_NOT_EXIST, ...);
}

// Check if campaign has expired
if (nowDate > moment(tokenData.end_date).unix()) {
  throw new MaasError(ERROR_CODE.ERROR_PROMO_CODE_EXPIRED, ...);
}
```
- Validates current time is within campaign period
- Treats early access attempts as non-existent codes
- Clear expiration handling

### 4. User Registration Timing Validation
```javascript
if (
  moment(userData.created_on).unix() > moment(tokenData.register_end_date).unix() ||
  moment(userData.created_on).unix() < moment(tokenData.register_start_date).unix()
) {
  throw new MaasError(ERROR_CODE.ERROR_PROMO_CODE_EXPIRED, ...);
}
```
- Validates user registration occurred within eligible window
- Prevents existing users from claiming codes meant for new users
- Prevents future registrations from claiming past codes

### 5. Device-Based Fraud Prevention
```javascript
const checkDevice = await DeviceCheckTokens.query()
  .select('id')
  .where({
    device_id: userData.device_id,
    ap_campaign_id: tokenData.ap_campaign_id,
  })
  .first();

if (checkDevice !== undefined) {
  throw new MaasError(ERROR_CODE.ERROR_PROMO_CODE_ALREADY_USED, ...);
}
```
- Prevents same device from claiming multiple codes
- Cross-references with device check tokens table
- Identifies potential device spoofing attempts

### 6. Usage History Validation
```javascript
const sendTokenRecord = await knex('token_transaction').select('id').where({
  user_id: userId,
  activity_type: 1,
  ap_campaign_id: tokenData.campaign_id,
});

if (sendTokenRecord.length > 0) {
  throw new MaasError(ERROR_CODE.ERROR_PROMO_CODE_ALREADY_USED, ...);
}
```
- Checks if user has already received tokens from this campaign
- Prevents multiple claims per user per campaign
- Activity type 1 indicates token distribution

### Database Schema Integration

**Key Tables Involved:**
- `campaign_promo_code`: Core promocode data
- `campaign_promo_code_settings`: Timing and timezone settings
- `campaign`: Campaign metadata and token allocation
- `token_campaign`: Token details and validity periods
- `agency`: Issuing agency information
- `device_check_tokens`: Device fraud prevention
- `token_transaction`: Usage history tracking

## 🚀 Usage Methods

### Basic Promocode Validation
```javascript
const promocodeService = require('@app/src/services/promocode');

async function validateUserPromocode(userId, code) {
  try {
    const validationResult = await promocodeService.checkCode(userId, code);
    
    console.log('Promocode validation successful:');
    console.log('Campaign:', validationResult.campaign_name);
    console.log('Tokens:', validationResult.tokens);
    console.log('Agency:', validationResult.agency_name);
    
    return {
      valid: true,
      campaignData: validationResult,
      message: 'Promocode is valid and ready for redemption'
    };
  } catch (error) {
    console.error('Promocode validation failed:', error.message);
    
    return {
      valid: false,
      errorCode: error.code,
      message: error.message,
      reason: this.getValidationFailureReason(error.code)
    };
  }
}

function getValidationFailureReason(errorCode) {
  const reasons = {
    'ERROR_USER_NOT_FOUND': 'User account not found',
    'ERROR_PROMO_CODE_NOT_EXIST': 'Promocode does not exist or has not started yet',
    'ERROR_PROMO_CODE_EXPIRED': 'Promocode has expired or user not eligible',
    'ERROR_PROMO_CODE_ALREADY_USED': 'Promocode has already been used or device not eligible'
  };
  
  return reasons[errorCode] || 'Unknown validation error';
}

// Usage
const result = await validateUserPromocode(12345, 'WELCOME2024');
```

### Comprehensive Promocode Manager
```javascript
class PromocodeManager {
  constructor() {
    this.promocodeService = require('@app/src/services/promocode');
    this.knex = require('@maas/core/mysql')('portal');
  }

  async validateAndPrepareRedemption(userId, promoCode) {
    try {
      // Validate the promocode
      const campaignData = await this.promocodeService.checkCode(userId, promoCode);
      
      // Prepare redemption data
      const redemptionInfo = {
        userId,
        promoCode,
        campaign: {
          id: campaignData.campaign_id,
          name: campaignData.campaign_name,
          apCampaignId: campaignData.ap_campaign_id
        },
        tokens: {
          amount: campaignData.tokens,
          tokenId: campaignData.token_id,
          tokenName: campaignData.token_name,
          apTokenId: campaignData.ap_token_id
        },
        agency: {
          id: campaignData.agency_id,
          name: campaignData.agency_name,
          apAgencyId: campaignData.ap_agency_id
        },
        timing: {
          issuedOn: campaignData.issued_on,
          expiresOn: campaignData.expired_on,
          timezone: campaignData.timezone
        },
        validatedAt: new Date().toISOString()
      };
      
      return {
        success: true,
        redemptionInfo,
        readyForRedemption: true
      };
    } catch (error) {
      return {
        success: false,
        error: {
          code: error.code,
          message: error.message,
          details: this.analyzeValidationFailure(error)
        },
        readyForRedemption: false
      };
    }
  }

  analyzeValidationFailure(error) {
    const analysis = {
      category: 'unknown',
      userActionRequired: false,
      retryRecommended: false
    };

    switch (error.code) {
      case 'ERROR_USER_NOT_FOUND':
        analysis.category = 'user_issue';
        analysis.userActionRequired = true;
        analysis.recommendation = 'User needs to register or log in';
        break;
        
      case 'ERROR_PROMO_CODE_NOT_EXIST':
        analysis.category = 'code_issue';
        analysis.userActionRequired = true;
        analysis.recommendation = 'Check code spelling or wait for campaign to start';
        break;
        
      case 'ERROR_PROMO_CODE_EXPIRED':
        analysis.category = 'timing_issue';
        analysis.userActionRequired = false;
        analysis.recommendation = 'Code expired or user registration outside eligible period';
        break;
        
      case 'ERROR_PROMO_CODE_ALREADY_USED':
        analysis.category = 'usage_issue';
        analysis.userActionRequired = false;
        analysis.recommendation = 'Code already redeemed by user or device';
        break;
    }

    return analysis;
  }

  async getPromocodeUsageStats(promoCode) {
    try {
      // Get basic campaign info
      const campaignInfo = await this.knex('campaign_promo_code')
        .select('campaign_id', 'promo_code')
        .where(this.knex.raw('BINARY promo_code'), promoCode)
        .first();

      if (!campaignInfo) {
        return { exists: false };
      }

      // Get usage statistics
      const usageStats = await this.knex('token_transaction')
        .where({
          ap_campaign_id: campaignInfo.campaign_id,
          activity_type: 1
        })
        .count('* as total_redemptions')
        .sum('tokens as total_tokens_distributed')
        .first();

      // Get device check stats
      const deviceStats = await this.knex('device_check_tokens')
        .join('campaign', 'campaign.ap_campaign_id', 'device_check_tokens.ap_campaign_id')
        .where('campaign.id', campaignInfo.campaign_id)
        .count('* as blocked_devices')
        .first();

      return {
        exists: true,
        promoCode,
        campaignId: campaignInfo.campaign_id,
        usage: {
          totalRedemptions: parseInt(usageStats.total_redemptions || 0),
          totalTokensDistributed: parseInt(usageStats.total_tokens_distributed || 0),
          blockedDevices: parseInt(deviceStats.blocked_devices || 0)
        }
      };
    } catch (error) {
      console.error('Error getting promocode usage stats:', error);
      throw error;
    }
  }

  async checkUserEligibilityPreview(userId) {
    try {
      const userData = await this.knex('auth_user')
        .select('id', 'created_on', 'device_id')
        .where('id', userId)
        .first();

      if (!userData) {
        return {
          eligible: false,
          reason: 'User not found'
        };
      }

      const eligibilityChecks = {
        userExists: true,
        hasDeviceId: !!userData.device_id,
        registrationDate: userData.created_on,
        deviceBlocked: false
      };

      // Check if device is globally blocked
      if (userData.device_id) {
        const deviceBlocks = await this.knex('device_check_tokens')
          .where('device_id', userData.device_id)
          .count('* as block_count')
          .first();
        
        eligibilityChecks.deviceBlocked = parseInt(deviceBlocks.block_count) > 0;
      }

      const eligible = eligibilityChecks.userExists && 
                      eligibilityChecks.hasDeviceId && 
                      !eligibilityChecks.deviceBlocked;

      return {
        userId,
        eligible,
        checks: eligibilityChecks,
        recommendations: this.generateEligibilityRecommendations(eligibilityChecks)
      };
    } catch (error) {
      console.error('Error checking user eligibility:', error);
      throw error;
    }
  }

  generateEligibilityRecommendations(checks) {
    const recommendations = [];

    if (!checks.hasDeviceId) {
      recommendations.push('User needs to complete device registration');
    }

    if (checks.deviceBlocked) {
      recommendations.push('Device has been flagged - contact support');
    }

    if (recommendations.length === 0) {
      recommendations.push('User appears eligible for promocode redemption');
    }

    return recommendations;
  }
}
```

### Campaign Analytics Service
```javascript
class PromocodeAnalytics {
  constructor() {
    this.knex = require('@maas/core/mysql')('portal');
  }

  async getCampaignPerformance(campaignId) {
    try {
      // Get campaign basic info
      const campaignInfo = await this.knex('campaign')
        .select('id', 'name', 'tokens', 'ap_campaign_id')
        .where('id', campaignId)
        .first();

      if (!campaignInfo) {
        throw new Error(`Campaign ${campaignId} not found`);
      }

      // Get promocode count
      const promocodeCount = await this.knex('campaign_promo_code')
        .where('campaign_id', campaignId)
        .count('* as total_codes')
        .first();

      // Get redemption stats
      const redemptions = await this.knex('token_transaction')
        .where({
          ap_campaign_id: campaignId,
          activity_type: 1
        })
        .select(
          this.knex.raw('COUNT(*) as total_redemptions'),
          this.knex.raw('SUM(tokens) as tokens_distributed'),
          this.knex.raw('COUNT(DISTINCT user_id) as unique_users'),
          this.knex.raw('MIN(created_on) as first_redemption'),
          this.knex.raw('MAX(created_on) as last_redemption')
        )
        .first();

      // Get device blocks
      const deviceBlocks = await this.knex('device_check_tokens')
        .where('ap_campaign_id', campaignInfo.ap_campaign_id)
        .count('* as blocked_attempts')
        .first();

      // Calculate metrics
      const totalCodes = parseInt(promocodeCount.total_codes);
      const totalRedemptions = parseInt(redemptions.total_redemptions || 0);
      const redemptionRate = totalCodes > 0 ? (totalRedemptions / totalCodes * 100) : 0;

      return {
        campaign: {
          id: campaignInfo.id,
          name: campaignInfo.name,
          tokensPerRedemption: campaignInfo.tokens
        },
        distribution: {
          totalPromocodes: totalCodes,
          totalRedemptions,
          redemptionRate: redemptionRate.toFixed(2) + '%',
          uniqueUsers: parseInt(redemptions.unique_users || 0),
          tokensDistributed: parseInt(redemptions.tokens_distributed || 0)
        },
        timeline: {
          firstRedemption: redemptions.first_redemption,
          lastRedemption: redemptions.last_redemption
        },
        security: {
          blockedAttempts: parseInt(deviceBlocks.blocked_attempts || 0),
          fraudRate: totalRedemptions > 0 ? 
            (parseInt(deviceBlocks.blocked_attempts || 0) / totalRedemptions * 100).toFixed(2) + '%' : '0%'
        }
      };
    } catch (error) {
      console.error('Error getting campaign performance:', error);
      throw error;
    }
  }

  async getRedemptionTimeline(campaignId, timeframe = '7d') {
    try {
      let dateFormat;
      let intervalSql;
      
      switch (timeframe) {
        case '24h':
          dateFormat = '%Y-%m-%d %H:00:00';
          intervalSql = 'DATE_SUB(NOW(), INTERVAL 24 HOUR)';
          break;
        case '7d':
          dateFormat = '%Y-%m-%d';
          intervalSql = 'DATE_SUB(NOW(), INTERVAL 7 DAY)';
          break;
        case '30d':
          dateFormat = '%Y-%m-%d';
          intervalSql = 'DATE_SUB(NOW(), INTERVAL 30 DAY)';
          break;
        default:
          throw new Error('Invalid timeframe. Use 24h, 7d, or 30d');
      }

      const timeline = await this.knex('token_transaction')
        .where({
          ap_campaign_id: campaignId,
          activity_type: 1
        })
        .where('created_on', '>=', this.knex.raw(intervalSql))
        .select(
          this.knex.raw(`DATE_FORMAT(created_on, '${dateFormat}') as time_period`),
          this.knex.raw('COUNT(*) as redemptions'),
          this.knex.raw('SUM(tokens) as tokens_distributed'),
          this.knex.raw('COUNT(DISTINCT user_id) as unique_users')
        )
        .groupBy('time_period')
        .orderBy('time_period', 'asc');

      return {
        campaignId,
        timeframe,
        dataPoints: timeline.length,
        timeline: timeline.map(point => ({
          period: point.time_period,
          redemptions: parseInt(point.redemptions),
          tokensDistributed: parseInt(point.tokens_distributed),
          uniqueUsers: parseInt(point.unique_users)
        }))
      };
    } catch (error) {
      console.error('Error getting redemption timeline:', error);
      throw error;
    }
  }

  async detectSuspiciousActivity(campaignId) {
    try {
      const suspiciousPatterns = [];

      // Check for rapid redemptions from same device
      const rapidRedemptions = await this.knex('token_transaction')
        .join('auth_user', 'auth_user.id', 'token_transaction.user_id')
        .where({
          'token_transaction.ap_campaign_id': campaignId,
          'token_transaction.activity_type': 1
        })
        .select('auth_user.device_id')
        .count('* as redemption_count')
        .groupBy('auth_user.device_id')
        .having('redemption_count', '>', 1);

      if (rapidRedemptions.length > 0) {
        suspiciousPatterns.push({
          type: 'multiple_redemptions_same_device',
          count: rapidRedemptions.length,
          details: rapidRedemptions
        });
      }

      // Check for redemptions clustered in time
      const timeCluster = await this.knex('token_transaction')
        .where({
          ap_campaign_id: campaignId,
          activity_type: 1
        })
        .select(
          this.knex.raw('DATE(created_on) as redemption_date'),
          this.knex.raw('COUNT(*) as daily_count')
        )
        .groupBy('redemption_date')
        .having('daily_count', '>', 100) // More than 100 per day
        .orderBy('daily_count', 'desc');

      if (timeCluster.length > 0) {
        suspiciousPatterns.push({
          type: 'high_volume_days',
          count: timeCluster.length,
          details: timeCluster
        });
      }

      return {
        campaignId,
        suspicious: suspiciousPatterns.length > 0,
        patterns: suspiciousPatterns,
        analysisDate: new Date().toISOString()
      };
    } catch (error) {
      console.error('Error detecting suspicious activity:', error);
      throw error;
    }
  }
}
```

## 📊 Output Examples

### Successful Validation Response
```json
{
  "cp_id": 123,
  "campaign_id": 456,
  "promo_code": "WELCOME2024",
  "timezone": "America/Chicago",
  "start_date": "2024-06-01T00:00:00.000Z",
  "end_date": "2024-12-31T23:59:59.000Z",
  "register_start_date": "2024-06-01T00:00:00.000Z",
  "register_end_date": "2024-12-31T23:59:59.000Z",
  "campaign_name": "Welcome Campaign 2024",
  "tokens": 100,
  "ap_campaign_id": 789,
  "token_id": 101,
  "token_name": "Welcome Tokens",
  "ap_token_id": 202,
  "issued_on": "2024-06-01T00:00:00.000Z",
  "expired_on": "2025-06-01T00:00:00.000Z",
  "agency_id": 303,
  "agency_name": "Metro Transit",
  "ap_agency_id": 404,
  "userId": 12345
}
```

### Validation Failure Response
```json
{
  "valid": false,
  "errorCode": "ERROR_PROMO_CODE_ALREADY_USED",
  "message": "Promocode has already been used or device not eligible",
  "reason": "Promocode has already been used or device not eligible"
}
```

### Campaign Performance Analysis
```json
{
  "campaign": {
    "id": 456,
    "name": "Welcome Campaign 2024",
    "tokensPerRedemption": 100
  },
  "distribution": {
    "totalPromocodes": 10000,
    "totalRedemptions": 2500,
    "redemptionRate": "25.00%",
    "uniqueUsers": 2500,
    "tokensDistributed": 250000
  },
  "timeline": {
    "firstRedemption": "2024-06-01T08:15:00.000Z",
    "lastRedemption": "2024-06-25T16:30:00.000Z"
  },
  "security": {
    "blockedAttempts": 150,
    "fraudRate": "6.00%"
  }
}
```

### User Eligibility Check
```json
{
  "userId": 12345,
  "eligible": true,
  "checks": {
    "userExists": true,
    "hasDeviceId": true,
    "registrationDate": "2024-06-15T10:30:00.000Z",
    "deviceBlocked": false
  },
  "recommendations": [
    "User appears eligible for promocode redemption"
  ]
}
```

### Suspicious Activity Detection
```json
{
  "campaignId": 456,
  "suspicious": true,
  "patterns": [
    {
      "type": "multiple_redemptions_same_device",
      "count": 3,
      "details": [
        {
          "device_id": "ABC123",
          "redemption_count": 5
        }
      ]
    }
  ],
  "analysisDate": "2024-06-25T14:30:00.000Z"
}
```

## ⚠️ Important Notes

### Security and Fraud Prevention
- **Device ID Tracking:** Prevents multiple redemptions from same device
- **Case-Sensitive Codes:** Uses BINARY comparison for exact matching
- **Registration Window:** Validates user registration timing eligibility
- **Usage History:** Comprehensive tracking of redemption attempts

### Validation Complexity
- **Multi-Table Joins:** Complex database queries across campaign tables
- **Timezone Handling:** Proper timezone support for global campaigns
- **Time Window Validation:** Multiple date range checks for eligibility
- **State Management:** Tracks various states of promocode lifecycle

### Error Handling Strategy
- **Specific Error Codes:** Different errors for different failure scenarios
- **Security Through Obscurity:** Some failures return generic "already used" error
- **User-Friendly Messages:** Clear indication of why validation failed
- **Audit Trail:** Comprehensive logging for campaign analysis

### Database Architecture
- **Normalized Structure:** Complex relationships between campaigns, codes, and tokens
- **Performance Considerations:** Indexed queries for efficient validation
- **Data Integrity:** Foreign key relationships maintain consistency
- **Scalability:** Designed to handle large-scale promotional campaigns

### Campaign Management Integration
- **Agency Support:** Multi-agency campaign management
- **Token Distribution:** Integration with token allocation systems
- **Analytics Ready:** Data structure supports detailed campaign analytics
- **Compliance:** Audit trail for regulatory compliance

### Business Rules Implementation
- **One-Time Use:** Strict enforcement of single-use promotional codes
- **Eligibility Windows:** Flexible timing constraints for user eligibility
- **Fair Distribution:** Device-based prevention of multiple claims
- **Campaign Limits:** Built-in controls for campaign budget management

### Performance and Scalability
- **Efficient Queries:** Optimized database queries with proper indexing
- **Caching Opportunities:** Campaign data could be cached for better performance
- **Concurrent Usage:** Safe handling of concurrent validation attempts
- **Rate Limiting:** Consider implementing rate limiting for validation attempts

## 🔗 Related File Links

- **Error Codes:** `allrepo/connectsmart/tsp-api/src/static/error-code.js`
- **User Models:** `allrepo/connectsmart/tsp-api/src/models/AuthUsers.js`
- **Device Check Models:** `allrepo/connectsmart/tsp-api/src/models/DeviceCheckTokens.js`
- **Campaign Controllers:** API endpoints that use promocode validation

---
*This service provides essential promotional code validation with comprehensive fraud prevention and campaign management capabilities for the TSP platform.*