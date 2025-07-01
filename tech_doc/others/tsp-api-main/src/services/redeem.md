# TSP API Redeem Service Documentation

## 🔍 Quick Summary (TL;DR)
The Redeem service manages gift card redemption through Tango Card integration, including daily limit enforcement, balance validation, fraud detection, email alerting, and comprehensive transaction logging with automatic violation tracking and administrative notifications.

**Keywords:** gift-card-redemption | tango-card-integration | daily-limits | fraud-prevention | transaction-logging | email-alerts | violation-tracking | points-redemption

**Primary use cases:** Redeeming points for gift cards, enforcing daily redemption limits, preventing fraud through violation tracking, sending administrative alerts, managing Tango Card account balance, transaction processing

**Compatibility:** Node.js >= 16.0.0, Tango Card API integration, email templating with EJS, Slack notifications, comprehensive database logging

## ❓ Common Questions Quick Index
- **Q: What gift card provider is used?** → Tango Card for gift card fulfillment and delivery
- **Q: Are there redemption limits?** → Yes, daily limits with early warning and hard limits
- **Q: How is fraud prevented?** → Daily limits, violation tracking, and administrative alerts
- **Q: Who gets alerted for violations?** → System administrators via email with SOP documentation
- **Q: How are gift cards delivered?** → Email delivery through Tango Card's system
- **Q: What happens if account balance is low?** → Slack alerts for insufficient funds, errors for negative balance

## 📋 Functionality Overview

**Non-technical explanation:** 
Think of this as a **digital gift card store** where users can exchange their earned points for real gift cards. The system has built-in safety measures - it watches for people trying to redeem too many cards too quickly (which might be fraud), sends alerts to administrators when something suspicious happens, and makes sure there's enough money in the account to fulfill the gift cards.

**Technical explanation:** 
A comprehensive gift card redemption service that integrates with Tango Card's API for fulfillment, implements multi-tier daily limit enforcement, tracks violation patterns for fraud prevention, provides administrative alerting through email and Slack, and maintains detailed transaction logs for compliance and auditing.

**Business value explanation:**
Enables monetization of user engagement through reward redemption, provides fraud protection to prevent abuse, maintains compliance through detailed logging and alerting, reduces administrative overhead through automated monitoring, and ensures reliable gift card fulfillment through Tango Card integration.

## 🔧 Technical Specifications

- **File:** `allrepo/connectsmart/tsp-api/src/services/redeem.js`
- **Language:** JavaScript (ES2020)
- **Framework:** Node.js with Tango Card API integration
- **Type:** Gift Card Redemption and Fraud Prevention Service
- **File Size:** ~6.9 KB
- **Complexity Score:** ⭐⭐⭐⭐ (High - Complex fraud prevention and external API integration)

**Dependencies:**
- `ejs`: Email template rendering (**Medium**)
- `moment-timezone`: Date/time handling (**High**)
- `@maas/services`: TangoManager and SlackManager (**Critical**)
- Multiple database models for transaction tracking (**Critical**)
- Email and notification helpers (**High**)

## 📝 Detailed Code Analysis

### Alert Email Functions

### sendEarlyAlertEmail Function

**Purpose:** Sends early warning emails when approaching daily limits

**Parameters:**
- `mailParameters`: Object containing user and transaction details

**Implementation:**
```javascript
const sendEarlyAlertEmail = async (mailParameters) => {
  const sopLink = 'https://docs.google.com/document/d/1fz330HBxTwJVI5hb35gtFUfUdlv948GvPrriLtUKrfE';
  const time = moment().utc().format(TIME_FORMAT);
  const projectTitle = config.portal.projectTitle;
  const subject = `${projectTitle} Tango Gift Card Daily Alert Threshold of ${tangoConfig.redeemAlertLimit} exceeded. (user_id: ${mailParameters.userId})`;
  
  const parameters = {
    redeemLimit: tangoConfig.redeemAlertLimit,
    projectTitle,
    time,
    sopLink,
    ...mailParameters,
  };
  
  const mailData = await ejs.renderFile('src/static/templates/tango_early_alert_mail.ejs', parameters);
  
  if (tangoConfig.alertNotifyEmail) {
    const emailList = tangoConfig.alertNotifyEmail.split(',');
    await sendMail(emailList, subject, mailData);
  }
};
```

**Features:**
- EJS template rendering for professional email formatting
- Hardcoded SOP (Standard Operating Procedure) link for administrator guidance
- Configurable email recipient list
- Detailed user and transaction information

### sendAlertEmail Function

**Purpose:** Sends critical alerts for daily quota violations

**Similar Implementation:** Like sendEarlyAlertEmail but for hard limit violations

### Limit Checking Functions

### checkLimit Function

**Purpose:** Common logic for checking daily redemption limits

**Parameters:**
- `userId`: Number - User identifier
- `amount`: Number - Current redemption amount
- `limit`: Number - Daily limit to check against

**Returns:** Boolean indicating if limit would be exceeded

**Implementation:**
```javascript
const checkLimit = async (userId, amount, limit) => {
  const start = moment.utc().subtract(1, 'day').toISOString();
  const sumResult = await RedeemTransactions.query()
    .sum('amount as prevAmount')
    .where('user_id', userId)
    .where('created_on', '>', start)
    .first();

  if (sumResult) {
    const totalAmount = parseFloat(sumResult.prevAmount) + parseFloat(amount);
    if (totalAmount > parseFloat(limit)) {
      return true;
    }
  }
  return false;
}
```

**Logic:**
- Calculates total redemptions in the last 24 hours
- Adds current redemption amount to determine if limit exceeded
- Uses precise 24-hour rolling window

### checkRedeemAlertLimit and checkRedeemLimit Functions

**Purpose:** Specific implementations for early warning and hard limits

**Different Thresholds:**
- `checkRedeemAlertLimit`: Uses `tangoConfig.redeemAlertLimit` for early warnings
- `checkRedeemLimit`: Uses `tangoConfig.redeemLimit` for hard blocks

### Main Redemption Function

### create Function

**Purpose:** Processes complete gift card redemption with comprehensive validation

**Parameters:**
- `inputData.userId`: Number - User identifier
- `inputData.id`: Number - Gift card ID to redeem
- `inputData.zone`: String - User timezone
- `inputData.email`: String - Optional email override

**Returns:** Promise resolving to user's new balance

**Complex Processing Flow:**

### 1. Service Initialization
```javascript
const slack = new SlackManager();
const tango = new TangoManager(tangoConfig);
```

### 2. Tango Account Balance Monitoring
```javascript
const accountInfo = await tango.getAccounts('/redeem');

if (accountInfo.currentBalance < tangoConfig.insufficientLevel) {
  const warnMsg = `[23028] Now money is ${accountInfo.currentBalance}, less than ${tangoConfig.insufficientLevel}, vendor : TangoCard, account: ${accountInfo.accountIdentifier}`;
  slack.sendMessage(warnMsg, slackConfig.token, slackConfig.channelId);
}

if (accountInfo.currentBalance < 0) {
  throw new MaasError(ERROR_CODE.ERROR_REDEEMED_FAILED, ...);
}
```

### 3. User and Gift Card Validation
```javascript
const userProfile = await AuthUsers.query().findById(userId);
const email = inputData.email ?? userProfile.email;
const giftCard = await GiftCards.query().findById(giftCardId);

if (!giftCard) {
  throw new MaasError(ERROR_CODE.ERROR_BAD_REQUEST_BODY, ...);
}
```

### 4. Daily Limit Enforcement with Violation Tracking
```javascript
const isOverLimit = await checkRedeemLimit(userId, giftCard.amount);

if (isOverLimit) {
  const start = moment.utc().subtract(1, 'day').toISOString();
  
  // Check for repeated violations
  const overLimits = await CoinActivityLogs.query()
    .where({
      user_id: userId,
      activity_type: CoinActivityLogs.types.REDEEM_DAILY_LIMIT,
    })
    .where('created_on', '>', start);
    
  if (overLimits.length > 1) {
    // Check if twice violation already logged
    const twiceViolations = await CoinActivityLogs.query()
      .where({
        user_id: userId,
        activity_type: CoinActivityLogs.types.REDEEM_TWICE_VIOLATION_24HR,
      })
      .where('created_on', '>', start);
      
    if (twiceViolations.length === 0) {
      // Log violation and send alert
      await CoinActivityLogs.query().insert({
        user_id: userId,
        activity_type: CoinActivityLogs.types.REDEEM_TWICE_VIOLATION_24HR,
      });
      
      sendAlertEmail({...userDetails});
    }
  }
  
  throw new MaasError(ERROR_CODE.ERROR_REDEEM_DAILY_LIMIT, ...);
}
```

### 5. Early Warning System
```javascript
const isOverAlertLimit = await checkRedeemAlertLimit(userId, giftCard.amount);
if (isOverAlertLimit) {
  sendEarlyAlertEmail({...userDetails});
}
```

### 6. User Balance Validation
```javascript
const userWallet = await UserWallets.query().where('user_id', userId).first();

if (parseFloat(userWallet.balance) < parseFloat(giftCard.amount)) {
  throw new MaasError(ERROR_CODE.ERROR_POINT_INSUFFICIENT, ...);
}
```

### 7. Tango Card Order Processing
```javascript
const transactionId = await tango.createOrder(
  giftCard.utid,
  email,
  userProfile.first_name,
  userProfile.last_name,
  giftCard.amount,
  tangoConfig.emailTemplateId,
);
```

### 8. Transaction Recording and Balance Update
```javascript
// Record redemption transaction
await RedeemTransactions.query().insert({
  user_id: userId,
  giftcard_id: giftCardId,
  points: 0 - parseFloat(giftCard.points),
  amount: giftCard.amount,
  currency: giftCard.currency,
  transaction_id: transactionId,
  created_on: moment.utc().format('YYYY-MM-DD HH:mm:ss'),
});

// Update user points balance
const { balance } = await pointsTransaction(
  userId,
  PointsTransactions.activityTypes.redemption,
  0 - parseFloat(giftCard.points),
  transactionId,
  false,
  moment.utc().format('YYYY-MM-DD HH:mm:ss'),
);

// Record user activity
insertAppData(userId, zone, 'Redeem');
```

## 🚀 Usage Methods

### Basic Gift Card Redemption
```javascript
const redeemService = require('@app/src/services/redeem');

async function redeemGiftCard(userId, giftCardId, userZone, emailOverride = null) {
  try {
    const redemptionData = {
      userId: userId,
      id: giftCardId,
      zone: userZone
    };
    
    // Add email override if provided
    if (emailOverride) {
      redemptionData.email = emailOverride;
    }
    
    const result = await redeemService.create(redemptionData);
    
    console.log('Gift card redemption successful:');
    console.log('New balance:', result.balance);
    
    return {
      success: true,
      newBalance: result.balance,
      message: 'Gift card redeemed successfully'
    };
  } catch (error) {
    console.error('Redemption failed:', error.message);
    
    return {
      success: false,
      errorCode: error.code,
      message: error.message,
      userMessage: this.getUserFriendlyMessage(error.code)
    };
  }
}

function getUserFriendlyMessage(errorCode) {
  const messages = {
    'ERROR_REDEEM_DAILY_LIMIT': 'You have reached your daily redemption limit. Please try again tomorrow.',
    'ERROR_POINT_INSUFFICIENT': 'You do not have enough points for this redemption.',
    'ERROR_REDEEMED_FAILED': 'Redemption failed. Please try again later or contact support.',
    'ERROR_BAD_REQUEST_BODY': 'Invalid gift card selected.'
  };
  
  return messages[errorCode] || 'An error occurred during redemption.';
}

// Usage
const result = await redeemGiftCard(12345, 67890, 'UTC', 'custom@email.com');
```

### Redemption Limit Checker
```javascript
class RedemptionLimitChecker {
  constructor() {
    this.knex = require('@maas/core/mysql')('portal');
    this.config = require('config').vendor.tango;
  }

  async checkUserRedemptionStatus(userId) {
    try {
      const start = moment.utc().subtract(1, 'day').toISOString();
      
      // Get today's redemptions
      const todaysRedemptions = await this.knex('redeem_transactions')
        .where('user_id', userId)
        .where('created_on', '>', start)
        .sum('amount as total_amount')
        .count('* as redemption_count')
        .first();
      
      const totalAmount = parseFloat(todaysRedemptions.total_amount || 0);
      const redemptionCount = parseInt(todaysRedemptions.redemption_count || 0);
      
      // Check violation history
      const violations = await this.knex('coin_activity_logs')
        .where('user_id', userId)
        .where('created_on', '>', start)
        .whereIn('activity_type', ['REDEEM_DAILY_LIMIT', 'REDEEM_TWICE_VIOLATION_24HR'])
        .select('activity_type', 'created_on');
      
      return {
        userId,
        currentStatus: {
          totalRedeemed: totalAmount,
          redemptionCount,
          remainingLimit: Math.max(0, this.config.redeemLimit - totalAmount),
          alertThresholdReached: totalAmount >= this.config.redeemAlertLimit,
          hardLimitReached: totalAmount >= this.config.redeemLimit
        },
        violations: violations.map(v => ({
          type: v.activity_type,
          timestamp: v.created_on
        })),
        recommendations: this.getRecommendations(totalAmount, violations)
      };
    } catch (error) {
      console.error('Error checking redemption status:', error);
      throw error;
    }
  }

  getRecommendations(totalAmount, violations) {
    const recommendations = [];
    
    if (violations.length > 0) {
      recommendations.push('User has recent violations - monitor closely');
    }
    
    if (totalAmount >= this.config.redeemAlertLimit) {
      recommendations.push('User approaching daily limit');
    }
    
    if (totalAmount >= this.config.redeemLimit) {
      recommendations.push('User has reached daily limit');
    }
    
    if (recommendations.length === 0) {
      recommendations.push('User within normal redemption limits');
    }
    
    return recommendations;
  }

  async predictRedemptionImpact(userId, giftCardAmount) {
    try {
      const currentStatus = await this.checkUserRedemptionStatus(userId);
      const newTotal = currentStatus.currentStatus.totalRedeemed + giftCardAmount;
      
      return {
        userId,
        giftCardAmount,
        prediction: {
          newTotal,
          wouldExceedAlertLimit: newTotal >= this.config.redeemAlertLimit,
          wouldExceedHardLimit: newTotal >= this.config.redeemLimit,
          allowedToRedeem: newTotal < this.config.redeemLimit,
          triggersEarlyAlert: !currentStatus.currentStatus.alertThresholdReached && 
                             newTotal >= this.config.redeemAlertLimit,
          triggersHardBlock: !currentStatus.currentStatus.hardLimitReached && 
                            newTotal >= this.config.redeemLimit
        }
      };
    } catch (error) {
      console.error('Error predicting redemption impact:', error);
      throw error;
    }
  }
}
```

### Tango Account Monitoring
```javascript
class TangoAccountMonitor {
  constructor() {
    this.TangoManager = require('@maas/services').TangoManager;
    this.SlackManager = require('@maas/services').SlackManager;
    this.config = require('config').vendor.tango;
    this.slack = new this.SlackManager();
  }

  async checkAccountBalance() {
    try {
      const tango = new this.TangoManager(this.config);
      const accountInfo = await tango.getAccounts('/redeem');
      
      const status = {
        currentBalance: accountInfo.currentBalance,
        accountIdentifier: accountInfo.accountIdentifier,
        status: 'healthy',
        warnings: [],
        actions: []
      };
      
      // Check various balance thresholds
      if (accountInfo.currentBalance < 0) {
        status.status = 'critical';
        status.warnings.push('Account balance is negative - redemptions will fail');
        status.actions.push('Immediate funding required');
      } else if (accountInfo.currentBalance < this.config.insufficientLevel) {
        status.status = 'warning';
        status.warnings.push(`Balance below insufficient level (${this.config.insufficientLevel})`);
        status.actions.push('Consider adding funds soon');
      } else if (accountInfo.currentBalance < this.config.insufficientLevel * 2) {
        status.status = 'watch';
        status.warnings.push('Balance getting low');
        status.actions.push('Monitor balance closely');
      }
      
      return status;
    } catch (error) {
      return {
        status: 'error',
        error: error.message,
        warnings: ['Unable to check account balance'],
        actions: ['Check Tango Card API connectivity']
      };
    }
  }

  async sendBalanceAlert(balanceInfo) {
    try {
      if (balanceInfo.status === 'critical' || balanceInfo.status === 'warning') {
        const message = `Tango Card Balance Alert: ${balanceInfo.currentBalance} (${balanceInfo.status.toUpperCase()}) - ${balanceInfo.warnings.join(', ')}`;
        
        await this.slack.sendMessage(
          message,
          this.config.slackToken,
          this.config.slackChannelId
        );
        
        return { alertSent: true, message };
      }
      
      return { alertSent: false, reason: 'Balance within normal range' };
    } catch (error) {
      console.error('Error sending balance alert:', error);
      return { alertSent: false, error: error.message };
    }
  }

  async scheduleRegularBalanceChecks(intervalMinutes = 60) {
    console.log(`Starting Tango balance monitoring every ${intervalMinutes} minutes`);
    
    setInterval(async () => {
      try {
        const balanceInfo = await this.checkAccountBalance();
        
        if (balanceInfo.status !== 'healthy') {
          await this.sendBalanceAlert(balanceInfo);
        }
        
        console.log(`Tango balance check: ${balanceInfo.currentBalance} (${balanceInfo.status})`);
      } catch (error) {
        console.error('Error in scheduled balance check:', error);
      }
    }, intervalMinutes * 60 * 1000);
  }
}
```

### Redemption Analytics
```javascript
class RedemptionAnalytics {
  constructor() {
    this.knex = require('@maas/core/mysql')('portal');
  }

  async getDailyRedemptionStats(startDate, endDate) {
    try {
      const stats = await this.knex('redeem_transactions')
        .whereBetween('created_on', [startDate, endDate])
        .select(
          this.knex.raw('DATE(created_on) as redemption_date'),
          this.knex.raw('COUNT(*) as total_redemptions'),
          this.knex.raw('SUM(amount) as total_amount'),
          this.knex.raw('SUM(ABS(points)) as total_points'),
          this.knex.raw('COUNT(DISTINCT user_id) as unique_users'),
          this.knex.raw('AVG(amount) as avg_redemption_amount')
        )
        .groupBy(this.knex.raw('DATE(created_on)'))
        .orderBy('redemption_date', 'desc');

      return {
        period: { startDate, endDate },
        dailyStats: stats.map(stat => ({
          date: stat.redemption_date,
          redemptions: parseInt(stat.total_redemptions),
          totalAmount: parseFloat(stat.total_amount),
          totalPoints: parseInt(stat.total_points),
          uniqueUsers: parseInt(stat.unique_users),
          avgAmount: parseFloat(stat.avg_redemption_amount)
        }))
      };
    } catch (error) {
      console.error('Error getting daily redemption stats:', error);
      throw error;
    }
  }

  async getViolationAnalysis(days = 30) {
    try {
      const startDate = moment.utc().subtract(days, 'days').toISOString();
      
      // Get violation counts by type
      const violations = await this.knex('coin_activity_logs')
        .where('created_on', '>', startDate)
        .whereIn('activity_type', ['REDEEM_DAILY_LIMIT', 'REDEEM_TWICE_VIOLATION_24HR'])
        .select('activity_type')
        .count('* as count')
        .groupBy('activity_type');

      // Get users with violations
      const violatingUsers = await this.knex('coin_activity_logs')
        .where('created_on', '>', startDate)
        .whereIn('activity_type', ['REDEEM_DAILY_LIMIT', 'REDEEM_TWICE_VIOLATION_24HR'])
        .select('user_id')
        .count('* as violation_count')
        .groupBy('user_id')
        .orderBy('violation_count', 'desc')
        .limit(10);

      return {
        period: `${days} days`,
        violationSummary: violations.reduce((acc, v) => {
          acc[v.activity_type] = parseInt(v.count);
          return acc;
        }, {}),
        topViolatingUsers: violatingUsers.map(user => ({
          userId: user.user_id,
          violationCount: parseInt(user.violation_count)
        })),
        riskMetrics: {
          totalViolations: violations.reduce((sum, v) => sum + parseInt(v.count), 0),
          uniqueViolatingUsers: violatingUsers.length
        }
      };
    } catch (error) {
      console.error('Error analyzing violations:', error);
      throw error;
    }
  }

  async getPopularGiftCards(days = 30) {
    try {
      const startDate = moment.utc().subtract(days, 'days').toISOString();
      
      const popularCards = await this.knex('redeem_transactions')
        .join('gift_cards', 'gift_cards.id', 'redeem_transactions.giftcard_id')
        .where('redeem_transactions.created_on', '>', startDate)
        .select(
          'gift_cards.id',
          'gift_cards.title',
          'gift_cards.amount',
          'gift_cards.currency'
        )
        .count('* as redemption_count')
        .sum('redeem_transactions.amount as total_redeemed')
        .groupBy('gift_cards.id', 'gift_cards.title', 'gift_cards.amount', 'gift_cards.currency')
        .orderBy('redemption_count', 'desc')
        .limit(10);

      return {
        period: `${days} days`,
        popularGiftCards: popularCards.map(card => ({
          giftCardId: card.id,
          title: card.title,
          amount: parseFloat(card.amount),
          currency: card.currency,
          redemptionCount: parseInt(card.redemption_count),
          totalRedeemed: parseFloat(card.total_redeemed)
        }))
      };
    } catch (error) {
      console.error('Error getting popular gift cards:', error);
      throw error;
    }
  }
}
```

## 📊 Output Examples

### Successful Redemption Response
```json
{
  "balance": 850.50
}
```

### User Redemption Status
```json
{
  "userId": 12345,
  "currentStatus": {
    "totalRedeemed": 45.00,
    "redemptionCount": 3,
    "remainingLimit": 55.00,
    "alertThresholdReached": false,
    "hardLimitReached": false
  },
  "violations": [],
  "recommendations": [
    "User within normal redemption limits"
  ]
}
```

### Redemption Impact Prediction
```json
{
  "userId": 12345,
  "giftCardAmount": 25.00,
  "prediction": {
    "newTotal": 70.00,
    "wouldExceedAlertLimit": true,
    "wouldExceedHardLimit": false,
    "allowedToRedeem": true,
    "triggersEarlyAlert": true,
    "triggersHardBlock": false
  }
}
```

### Tango Account Balance Status
```json
{
  "currentBalance": 1250.00,
  "accountIdentifier": "tango_account_123",
  "status": "warning",
  "warnings": [
    "Balance below insufficient level (1500)"
  ],
  "actions": [
    "Consider adding funds soon"
  ]
}
```

### Violation Analysis
```json
{
  "period": "30 days",
  "violationSummary": {
    "REDEEM_DAILY_LIMIT": 15,
    "REDEEM_TWICE_VIOLATION_24HR": 3
  },
  "topViolatingUsers": [
    {
      "userId": 12345,
      "violationCount": 5
    }
  ],
  "riskMetrics": {
    "totalViolations": 18,
    "uniqueViolatingUsers": 8
  }
}
```

## ⚠️ Important Notes

### Fraud Prevention and Security
- **Daily Limits:** Two-tier system with early warning and hard limits
- **Violation Tracking:** Detailed logging of limit violations and repeat offenses
- **Email Alerts:** Automatic administrative notifications for suspicious activity
- **Rolling Windows:** 24-hour rolling limits rather than calendar day limits

### Tango Card Integration
- **Account Monitoring:** Real-time balance checking with Slack alerts
- **Order Processing:** Direct integration with Tango Card's order creation API
- **Email Templates:** Configurable email templates for gift card delivery
- **Error Handling:** Comprehensive error handling for API failures

### Administrative Features
- **SOP Documentation:** Hardcoded links to Standard Operating Procedures
- **Multi-Channel Alerts:** Both email and Slack notifications
- **Configurable Recipients:** Email distribution lists for alerts
- **EJS Templating:** Professional email formatting with dynamic content

### Transaction Management
- **Atomic Operations:** Ensures data consistency across multiple database tables
- **Balance Validation:** Prevents overdrafts and insufficient balance redemptions
- **Transaction Logging:** Comprehensive audit trail for compliance
- **Points Integration:** Seamless integration with points/wallet system

### Performance and Reliability
- **Async Operations:** Non-blocking email sending and external API calls
- **Error Recovery:** Graceful handling of external service failures
- **Rate Limiting:** Daily limits prevent system overload
- **Monitoring Integration:** Built-in monitoring and alerting capabilities

### Business Logic
- **Flexible Limits:** Configurable daily limits for different scenarios
- **User Experience:** Clear error messages for different failure scenarios
- **Compliance:** Detailed logging for financial compliance requirements
- **Scalability:** Designed to handle high-volume redemption scenarios

### Configuration Management
- **Environment-Specific:** Different limits and settings per environment
- **Hot Configuration:** Most settings configurable without code changes
- **Alert Thresholds:** Configurable warning and critical thresholds
- **Email Templates:** Customizable email content and formatting

## 🔗 Related File Links

- **Wallet Service:** `allrepo/connectsmart/tsp-api/src/services/wallet.js`
- **Gift Cards Model:** `allrepo/connectsmart/tsp-api/src/models/GiftCards.js`
- **Redeem Transactions Model:** `allrepo/connectsmart/tsp-api/src/models/RedeemTransactions.js`
- **Email Templates:** `allrepo/connectsmart/tsp-api/src/static/templates/`

---
*This service provides essential gift card redemption capabilities with comprehensive fraud prevention, administrative monitoring, and reliable Tango Card integration for the TSP platform.*