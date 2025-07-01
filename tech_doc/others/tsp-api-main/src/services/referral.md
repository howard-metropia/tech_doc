# TSP API Referral Service Documentation

## 🔍 Quick Summary (TL;DR)
The Referral service manages user referral programs with sophisticated fraud prevention, geographic restrictions, tier-based rewards, dual reward systems (tokens/coins), and comprehensive validation to ensure fair distribution of referral bonuses.

**Keywords:** referral-system | fraud-prevention | geographic-restrictions | tier-based-rewards | device-tracking | time-limits | dual-rewards | houston-area-only

**Primary use cases:** Processing referral codes, preventing fraud through device/geographic validation, distributing rewards to both referrer and referee, managing tier-based bonus multipliers, tracking referral history

**Compatibility:** Node.js >= 16.0.0, MySQL database, Hashids for secure code generation, Houston geographic area restriction, 5-day time limit enforcement

## ❓ Common Questions Quick Index
- **Q: How are referral codes generated?** → Using Hashids with project title as salt, encoding user IDs
- **Q: What restrictions exist?** → 5-day registration limit, Houston area only, device tracking, no self-referral
- **Q: What rewards are available?** → Tokens or coins with tier-based multipliers
- **Q: How is fraud prevented?** → Device ID tracking, geographic boundaries, time limits, usage history
- **Q: Can codes be reused?** → No, strict one-time use per user and device
- **Q: Do both users get rewards?** → Yes, both referrer and referee receive tier-based rewards

## 📋 Functionality Overview

**Non-technical explanation:** 
Think of this as a **friend invitation system** with strict rules to prevent cheating. When you invite a friend, both of you get rewards, but only if your friend is new to the area, signs up quickly, and hasn't already been invited by someone else. The system checks your location, when you signed up, and your device to make sure everything is legitimate.

**Technical explanation:** 
A comprehensive referral program service with multi-layered fraud prevention including geographic restrictions, temporal validation, device fingerprinting, and tier-based reward distribution. Supports both token and coin reward systems with dynamic messaging and comprehensive audit trails.

**Business value explanation:**
Drives user acquisition through incentivized referrals, prevents fraud and abuse through sophisticated validation, supports business growth with geographic targeting, enables tier-based user engagement, and provides detailed analytics for campaign optimization.

## 🔧 Technical Specifications

- **File:** `allrepo/connectsmart/tsp-api/src/services/referral.js`
- **Language:** JavaScript (ES2020)
- **Framework:** Node.js with Objection.js ORM
- **Type:** Referral Program Management Service
- **File Size:** ~7.2 KB
- **Complexity Score:** ⭐⭐⭐⭐⭐ (Very High - Complex validation with fraud prevention)

**Dependencies:**
- `hashids`: Secure referral code generation (**Critical**)
- `moment-timezone`: Time validation and limits (**High**)
- `@app/src/services/tier`: Tier-based rewards (**Critical**)
- `@app/src/services/sendToken`: Token distribution (**High**)
- `@app/src/services/wallet`: Coin transactions (**High**)
- Multiple models for data tracking (**Critical**)

## 📝 Detailed Code Analysis

### Core Validation Pipeline

### create Function

**Purpose:** Processes referral code redemption with comprehensive fraud prevention

**Parameters:**
- `inputData.userId`: Number - User attempting to redeem code
- `inputData.referral_code`: String - Referral code to validate
- `inputData.reward_type`: String - 'token' or 'coin' reward type

**Returns:** Promise resolving to referral ID and toast message

**Complex Validation Flow:**

### 1. User Profile and Device Validation
```javascript
const userProfile = await AuthUsers.query()
  .select([
    'created_on',
    'registration_latitude',
    'registration_longitude', 
    'device_id',
    'register_device_id',
    'is_debug'
  ])
  .findById(userId);

const userDeviceId = userProfile.register_device_id || userProfile.device_id;
if (!userDeviceId) {
  throw new MaasError(ERROR_REFERRAL_CODE_DEVICE_ID_NOT_EXIST, ...);
}
```
- Retrieves comprehensive user profile data
- Ensures device ID is available for fraud prevention
- Supports debug mode for testing bypass

### 2. Referral Code Decoding and Sender Validation
```javascript
const referralHash = new Hashids(config.projectTitle, 10);
const senderId = referralHash.decode(referralCode)[0] || 0;

const sender = await AuthUsers.query().findById(senderId);
if (!sender) {
  throw new MaasError(ERROR_REFERRAL_CODE_NOT_EXIST, ...);
}

const senderDeviceId = sender.register_device_id || sender.device_id;
if (!senderDeviceId) {
  throw new MaasError(ERROR_REFERRAL_CODE_DEVICE_ID_NOT_EXIST, ...);
}
```
- Decodes referral code to extract sender user ID
- Validates sender exists and has valid device ID
- Uses project-specific salt for security

### 3. Duplicate Usage Prevention
```javascript
const referralLog = await ReferralHistory.query()
  .where((queryBuilder) => {
    queryBuilder
      .where('receiver_user_id', userId)
      .orWhere('receiver_device_id', userProfile.register_device_id);
  })
  .first();

if (!userProfile.is_debug && referralLog) {
  throw new MaasError(ERROR_REFERRAL_CODE_ALREADY_USED, ...);
}
```
- Checks both user ID and device ID for previous usage
- Prevents users from claiming multiple referral rewards
- Bypasses check for debug users

### 4. Self-Referral Prevention
```javascript
const selfCode = referralHash.encode(userId);
if (selfCode === referralCode) {
  throw new MaasError(ERROR_REFERRAL_CODE_CANNOT_BE_SELF, ...);
}
```
- Generates user's own referral code and compares
- Prevents users from referring themselves
- Simple but effective self-referral blocking

### 5. Time Limit Enforcement
```javascript
const dateLimit = moment.utc(userProfile.created_on).add(5, 'days');
if (!userProfile.is_debug && moment.utc().isAfter(dateLimit)) {
  throw new MaasError(ERROR_REFERRAL_CODE_FIVE_DAY, ...);
}
```
- Enforces 5-day limit from user registration
- Prevents late adoption of referral benefits
- Encourages immediate engagement

### 6. Geographic Restriction (Houston Area)
```javascript
// longitude: -98.378634 ~ -94.303447, latitude: 28.813255 ~ 30.945398
if (
  !userProfile.is_debug &&
  (userProfile.registration_longitude < -98.378634 ||
   userProfile.registration_longitude > -94.303447 ||
   userProfile.registration_latitude < 28.813255 ||
   userProfile.registration_latitude > 30.945398)
) {
  throw new MaasError(ERROR_REFERRAL_CODE_HOUSTON_AREA, ...);
}
```
- Restricts referrals to Houston metropolitan area
- Uses precise coordinate boundaries
- Prevents out-of-area referral abuse

### Reward System Implementation

### Tier-Based Reward Calculation
```javascript
const tier = await tierService.getUserTier(userId);
const tierBenefits = await tierService.getUserTierBenefits(tier.level);
const senderTier = await tierService.getUserTier(senderId);
const senderTierBenefits = await tierService.getUserTierBenefits(senderTier.level);

// For tokens
rewardValue = Math.round(campaign.tokens * tierBenefits.referral.magnification * 1000 / 10) / 100;
senderRewardValue = Math.round(campaign.tokens * senderTierBenefits.referral.magnification * 1000 / 10) / 100;

// For coins
rewardValue = Math.round(parseFloat(config.referralCoin) * tierBenefits.referral.magnification * 1000 / 10) / 100;
```
- Both users get rewards based on their individual tier levels
- Supports decimal precision with rounding
- Separate calculations for different reward types

### Token Reward Distribution
```javascript
if (rewardType === 'token') {
  const campaign = await Campaigns.query()
    .where('name', 'Referral Program')
    .orderBy('ap_campaign_id', 'desc')
    .first();
    
  const agency = await Agency.query()
    .where('name', 'Houston ConnectSmart')
    .orderBy('ap_agency_id', 'desc')
    .first();
    
  const tokenCampaign = await TokenCampaigns.query()
    .where('name', 'Referral Bonus')
    .orderBy('ap_token_id', 'desc')
    .first();

  // Create token data for both users
  const referral = { ...tokenData, userId };
  const referrer = { ...senderTokenData, userId: senderId };
  
  await sendToken.send([referral, referrer]);
}
```
- Fetches current referral campaign configuration
- Creates separate token distributions for both users
- Uses batch token sending for efficiency

### Coin Reward Distribution
```javascript
else {
  // Send coin to referral(被推薦人) & referrer(推薦人)
  await pointsTransaction(
    userId,
    PointsTransaction.activityTypes.incentive,
    rewardValue,
    eventId,
    false,
  );
  
  await pointsTransaction(
    senderId,
    PointsTransaction.activityTypes.incentive,
    senderRewardValue,
    eventId,
    false,
  );
}
```
- Direct coin transactions for both users
- Uses wallet service for consistent accounting
- Separate transactions ensure individual tracking

### Dynamic Message Generation
```javascript
tierBenefits.referral.toast.message = tierBenefits.referral.toast.message.replace('{1}', rewardValue);
if (rewardValue !== 1) {
  tierBenefits.referral.toast.message = tierBenefits.referral.toast.message.replace('{2}', 'Tokens');
} else {
  tierBenefits.referral.toast.message = tierBenefits.referral.toast.message.replace('{2}', 'Token');
}
```
- Dynamic message templating with variable substitution
- Proper singular/plural handling for user experience
- Tier-specific messaging support

### Audit Trail and Event Tracking
```javascript
const insertData = {
  sender_user_id: senderId,
  receiver_user_id: userId,
  receiver_device_id: deviceId,
  ap_campaign_id: apCampaignId,
};

if (!userProfile.is_debug || !referralLog) {
  const newReferralLog = await ReferralHistory.query().insert(insertData);
  referralId = newReferralLog.id;
}

await sendEvent([
  {
    userIds: [senderId],
    eventName: 'refer_friend',
    eventMeta: {
      receiver_user_id: userId,
      referral_history_id: referralId,
    },
  },
]);
```
- Creates comprehensive referral history record
- Sends events for analytics and notifications
- Links to campaign for tracking purposes

## 🚀 Usage Methods

### Basic Referral Code Processing
```javascript
const referralService = require('@app/src/services/referral');

async function processReferralCode(userId, referralCode, rewardType = 'token') {
  try {
    const result = await referralService.create({
      userId: userId,
      referral_code: referralCode,
      reward_type: rewardType
    });
    
    console.log('Referral processed successfully:');
    console.log('Referral ID:', result.referral_id);
    console.log('Toast Message:', result.toast.message);
    
    return {
      success: true,
      referralId: result.referral_id,
      message: result.toast.message,
      icon: result.toast.icon
    };
  } catch (error) {
    console.error('Referral processing failed:', error.message);
    
    return {
      success: false,
      errorCode: error.code,
      message: error.message,
      reason: this.getReferralFailureReason(error.code)
    };
  }
}

function getReferralFailureReason(errorCode) {
  const reasons = {
    'ERROR_REFERRAL_CODE_CANNOT_BE_SELF': 'Cannot use your own referral code',
    'ERROR_REFERRAL_CODE_FIVE_DAY': 'Referral codes must be used within 5 days of registration',
    'ERROR_REFERRAL_CODE_HOUSTON_AREA': 'Referral codes only available in Houston area',
    'ERROR_REFERRAL_CODE_ALREADY_USED': 'This referral code has already been used',
    'ERROR_REFERRAL_CODE_NOT_EXIST': 'Invalid referral code',
    'ERROR_REFERRAL_CODE_DEVICE_ID_NOT_EXIST': 'Device information required for referral validation'
  };
  
  return reasons[errorCode] || 'Unknown referral error';
}

// Usage
const result = await processReferralCode(12345, 'ABC123XYZ', 'token');
```

### Referral Code Generator and Validator
```javascript
class ReferralCodeManager {
  constructor() {
    this.config = require('config').portal;
    this.referralService = require('@app/src/services/referral');
    this.AuthUsers = require('@app/src/models/AuthUsers');
    this.Hashids = require('hashids');
  }

  generateReferralCode(userId) {
    const referralHash = new this.Hashids(this.config.projectTitle, 10);
    return referralHash.encode(userId);
  }

  decodeReferralCode(referralCode) {
    const referralHash = new this.Hashids(this.config.projectTitle, 10);
    const decoded = referralHash.decode(referralCode);
    return decoded.length > 0 ? decoded[0] : null;
  }

  async validateUserEligibility(userId) {
    try {
      const user = await this.AuthUsers.query()
        .select([
          'id',
          'created_on',
          'registration_latitude',
          'registration_longitude',
          'device_id',
          'register_device_id',
          'is_debug'
        ])
        .findById(userId);

      if (!user) {
        return { eligible: false, reason: 'User not found' };
      }

      const checks = {
        hasDeviceId: !!(user.register_device_id || user.device_id),
        withinTimeLimit: this.checkTimeLimit(user.created_on),
        inHoustonArea: this.checkHoustonArea(user.registration_latitude, user.registration_longitude),
        isDebugUser: user.is_debug
      };

      const eligible = checks.isDebugUser || (
        checks.hasDeviceId && 
        checks.withinTimeLimit && 
        checks.inHoustonArea
      );

      return {
        userId,
        eligible,
        checks,
        recommendation: this.getEligibilityRecommendation(checks)
      };
    } catch (error) {
      console.error('Error validating user eligibility:', error);
      return { eligible: false, reason: error.message };
    }
  }

  checkTimeLimit(createdOn) {
    const moment = require('moment-timezone');
    const dateLimit = moment.utc(createdOn).add(5, 'days');
    return moment.utc().isBefore(dateLimit);
  }

  checkHoustonArea(latitude, longitude) {
    if (!latitude || !longitude) return false;
    
    // Houston area boundaries
    return (
      longitude >= -98.378634 && longitude <= -94.303447 &&
      latitude >= 28.813255 && latitude <= 30.945398
    );
  }

  getEligibilityRecommendation(checks) {
    if (checks.isDebugUser) {
      return 'Debug user - all restrictions bypassed';
    }

    const issues = [];
    if (!checks.hasDeviceId) issues.push('Missing device ID');
    if (!checks.withinTimeLimit) issues.push('5-day time limit exceeded');
    if (!checks.inHoustonArea) issues.push('Outside Houston service area');

    return issues.length === 0 
      ? 'User eligible for referral program'
      : `Issues: ${issues.join(', ')}`;
  }

  async getReferralHistory(userId) {
    try {
      const ReferralHistory = require('@app/src/models/ReferralHistory');
      
      // Get referrals made by this user (as sender)
      const sentReferrals = await ReferralHistory.query()
        .where('sender_user_id', userId)
        .select('receiver_user_id', 'created_on', 'ap_campaign_id');

      // Get referrals received by this user (as receiver)
      const receivedReferrals = await ReferralHistory.query()
        .where('receiver_user_id', userId)
        .select('sender_user_id', 'created_on', 'ap_campaign_id');

      return {
        userId,
        referralsSent: sentReferrals.length,
        referralsReceived: receivedReferrals.length,
        sentHistory: sentReferrals,
        receivedHistory: receivedReferrals,
        canReceiveReferral: receivedReferrals.length === 0
      };
    } catch (error) {
      console.error('Error getting referral history:', error);
      throw error;
    }
  }

  async processReferralWithValidation(userId, referralCode, rewardType = 'token') {
    try {
      // Pre-validate user eligibility
      const eligibility = await this.validateUserEligibility(userId);
      
      if (!eligibility.eligible) {
        return {
          success: false,
          reason: eligibility.reason,
          recommendation: eligibility.recommendation
        };
      }

      // Validate referral code format
      const senderId = this.decodeReferralCode(referralCode);
      if (!senderId) {
        return {
          success: false,
          reason: 'Invalid referral code format'
        };
      }

      // Check if self-referral
      if (senderId === userId) {
        return {
          success: false,
          reason: 'Cannot use your own referral code'
        };
      }

      // Process the referral
      const result = await this.referralService.create({
        userId,
        referral_code: referralCode,
        reward_type: rewardType
      });

      return {
        success: true,
        referralId: result.referral_id,
        toast: result.toast,
        senderId
      };
    } catch (error) {
      return {
        success: false,
        errorCode: error.code,
        reason: error.message
      };
    }
  }
}
```

### Referral Analytics and Tracking
```javascript
class ReferralAnalytics {
  constructor() {
    this.knex = require('@maas/core/mysql')('portal');
  }

  async getReferralCampaignStats(timeframe = '30d') {
    try {
      let startDate;
      const moment = require('moment-timezone');
      
      switch (timeframe) {
        case '7d':
          startDate = moment.utc().subtract(7, 'days').toISOString();
          break;
        case '30d':
          startDate = moment.utc().subtract(30, 'days').toISOString();
          break;
        case '90d':
          startDate = moment.utc().subtract(90, 'days').toISOString();
          break;
        default:
          startDate = moment.utc().subtract(30, 'days').toISOString();
      }

      const stats = await this.knex('referral_history')
        .where('created_on', '>', startDate)
        .select(
          this.knex.raw('COUNT(*) as total_referrals'),
          this.knex.raw('COUNT(DISTINCT sender_user_id) as unique_referrers'),
          this.knex.raw('COUNT(DISTINCT receiver_user_id) as unique_receivers'),
          this.knex.raw('COUNT(DISTINCT ap_campaign_id) as campaigns_used')
        )
        .first();

      const dailyBreakdown = await this.knex('referral_history')
        .where('created_on', '>', startDate)
        .select(
          this.knex.raw('DATE(created_on) as referral_date'),
          this.knex.raw('COUNT(*) as daily_count'),
          this.knex.raw('COUNT(DISTINCT sender_user_id) as daily_referrers')
        )
        .groupBy('referral_date')
        .orderBy('referral_date', 'asc');

      const topReferrers = await this.knex('referral_history')
        .where('created_on', '>', startDate)
        .select('sender_user_id')
        .count('* as referral_count')
        .groupBy('sender_user_id')
        .orderBy('referral_count', 'desc')
        .limit(10);

      return {
        timeframe,
        overview: {
          totalReferrals: parseInt(stats.total_referrals),
          uniqueReferrers: parseInt(stats.unique_referrers),
          uniqueReceivers: parseInt(stats.unique_receivers),
          campaignsUsed: parseInt(stats.campaigns_used)
        },
        dailyBreakdown: dailyBreakdown.map(day => ({
          date: day.referral_date,
          referrals: parseInt(day.daily_count),
          referrers: parseInt(day.daily_referrers)
        })),
        topReferrers: topReferrers.map(referrer => ({
          userId: referrer.sender_user_id,
          referralCount: parseInt(referrer.referral_count)
        }))
      };
    } catch (error) {
      console.error('Error getting referral campaign stats:', error);
      throw error;
    }
  }

  async getGeographicDistribution() {
    try {
      const distribution = await this.knex('referral_history')
        .join('auth_user', 'auth_user.id', 'referral_history.receiver_user_id')
        .select(
          this.knex.raw('ROUND(registration_latitude, 2) as lat_bucket'),
          this.knex.raw('ROUND(registration_longitude, 2) as lng_bucket'),
          this.knex.raw('COUNT(*) as referral_count')
        )
        .whereNotNull('auth_user.registration_latitude')
        .whereNotNull('auth_user.registration_longitude')
        .groupBy('lat_bucket', 'lng_bucket')
        .orderBy('referral_count', 'desc')
        .limit(50);

      const houstonAreaCount = await this.knex('referral_history')
        .join('auth_user', 'auth_user.id', 'referral_history.receiver_user_id')
        .where('auth_user.registration_longitude', '>=', -98.378634)
        .where('auth_user.registration_longitude', '<=', -94.303447)
        .where('auth_user.registration_latitude', '>=', 28.813255)
        .where('auth_user.registration_latitude', '<=', 30.945398)
        .count('* as houston_referrals')
        .first();

      const totalCount = await this.knex('referral_history')
        .join('auth_user', 'auth_user.id', 'referral_history.receiver_user_id')
        .whereNotNull('auth_user.registration_latitude')
        .count('* as total_referrals')
        .first();

      return {
        houstonAreaPercentage: (
          parseInt(houstonAreaCount.houston_referrals) / 
          parseInt(totalCount.total_referrals) * 100
        ).toFixed(2) + '%',
        geographicClusters: distribution.map(cluster => ({
          latitude: parseFloat(cluster.lat_bucket),
          longitude: parseFloat(cluster.lng_bucket),
          referralCount: parseInt(cluster.referral_count)
        }))
      };
    } catch (error) {
      console.error('Error getting geographic distribution:', error);
      throw error;
    }
  }

  async getReferralConversionMetrics() {
    try {
      const moment = require('moment-timezone');
      const last30Days = moment.utc().subtract(30, 'days').toISOString();

      // Users who registered in last 30 days
      const newUsers = await this.knex('auth_user')
        .where('created_on', '>', last30Days)
        .count('* as new_user_count')
        .first();

      // New users who used referral codes
      const referralUsers = await this.knex('referral_history')
        .join('auth_user', 'auth_user.id', 'referral_history.receiver_user_id')
        .where('auth_user.created_on', '>', last30Days)
        .count('* as referral_user_count')
        .first();

      const conversionRate = (
        parseInt(referralUsers.referral_user_count) / 
        parseInt(newUsers.new_user_count) * 100
      ).toFixed(2);

      return {
        timeframe: '30 days',
        newUsers: parseInt(newUsers.new_user_count),
        referralUsers: parseInt(referralUsers.referral_user_count),
        conversionRate: conversionRate + '%',
        organicUsers: parseInt(newUsers.new_user_count) - parseInt(referralUsers.referral_user_count)
      };
    } catch (error) {
      console.error('Error getting conversion metrics:', error);
      throw error;
    }
  }
}
```

## 📊 Output Examples

### Successful Referral Processing
```json
{
  "referral_id": 12345,
  "toast": {
    "message": "You've earned 50 Tokens for referring a friend!",
    "icon": "token_reward",
    "duration": 5000
  }
}
```

### User Eligibility Check
```json
{
  "userId": 12345,
  "eligible": true,
  "checks": {
    "hasDeviceId": true,
    "withinTimeLimit": true,
    "inHoustonArea": true,
    "isDebugUser": false
  },
  "recommendation": "User eligible for referral program"
}
```

### Referral Campaign Statistics
```json
{
  "timeframe": "30d",
  "overview": {
    "totalReferrals": 1250,
    "uniqueReferrers": 892,
    "uniqueReceivers": 1250,
    "campaignsUsed": 3
  },
  "dailyBreakdown": [
    {
      "date": "2024-06-01",
      "referrals": 45,
      "referrers": 38
    }
  ],
  "topReferrers": [
    {
      "userId": 12345,
      "referralCount": 15
    }
  ]
}
```

### Geographic Distribution Analysis
```json
{
  "houstonAreaPercentage": "94.8%",
  "geographicClusters": [
    {
      "latitude": 29.76,
      "longitude": -95.37,
      "referralCount": 125
    }
  ]
}
```

### Referral Conversion Metrics
```json
{
  "timeframe": "30 days",
  "newUsers": 2500,
  "referralUsers": 1250,
  "conversionRate": "50.00%",
  "organicUsers": 1250
}
```

## ⚠️ Important Notes

### Fraud Prevention Mechanisms
- **Device ID Tracking:** Prevents multiple redemptions from same device
- **Geographic Restrictions:** Houston area only with precise coordinate boundaries
- **Time Limits:** 5-day window from registration to prevent late adoption abuse
- **Self-Referral Prevention:** Users cannot refer themselves
- **Usage History:** Comprehensive tracking prevents duplicate claims

### Reward System Features
- **Tier-Based Multipliers:** Different rewards based on user tier levels
- **Dual Reward Types:** Supports both token and coin distributions
- **Both Users Rewarded:** Referrer and referee both receive benefits
- **Dynamic Messaging:** Proper singular/plural handling in notifications
- **Campaign Integration:** Links to broader marketing campaigns

### Geographic and Temporal Constraints
- **Houston Metropolitan Area:** Precise latitude/longitude boundaries
- **5-Day Registration Window:** Encourages immediate engagement
- **Registration Location Tracking:** Uses sign-up coordinates for validation
- **Debug Mode Bypass:** Allows testing without restrictions

### Security and Compliance
- **Hashids Encoding:** Secure, reversible ID encoding with project salt
- **Device Fingerprinting:** Multiple device ID sources for reliability
- **Audit Trails:** Comprehensive logging for compliance and analysis
- **Event Tracking:** Integration with analytics and notification systems

### Business Logic Implementation
- **Fair Distribution:** Prevents gaming the system through multiple restrictions
- **User Acquisition Focus:** Designed to drive new user growth
- **Regional Targeting:** Geographic restrictions support business expansion
- **Engagement Incentives:** Time limits encourage quick adoption

### Database Architecture
- **Referral History Table:** Comprehensive tracking of all referral activities
- **Cross-Table Validation:** Checks across multiple user and campaign tables
- **Campaign Integration:** Links to token and campaign management systems
- **Device Tracking:** Maintains device-based fraud prevention records

## 🔗 Related File Links

- **Tier Service:** `allrepo/connectsmart/tsp-api/src/services/tier.js`
- **Send Token Service:** `allrepo/connectsmart/tsp-api/src/services/sendToken.js`
- **Wallet Service:** `allrepo/connectsmart/tsp-api/src/services/wallet.js`
- **Referral History Model:** `allrepo/connectsmart/tsp-api/src/models/ReferralHistory.js`

---
*This service provides essential referral program management with sophisticated fraud prevention and tier-based reward distribution for the TSP platform.*