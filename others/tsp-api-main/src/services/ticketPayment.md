# TSP API TicketPayment Service Documentation

## 🔍 Quick Summary (TL;DR)
The TicketPayment service manages Bytemark payment account integration by automatically creating accounts for users, handling authentication tokens, validating passwords, and providing seamless payment system access with comprehensive error handling and Slack monitoring.

**Keywords:** bytemark-integration | payment-accounts | auto-registration | token-management | password-validation | error-handling | slack-monitoring | account-authentication

**Primary use cases:** Automatically creating Bytemark payment accounts, managing authentication tokens, handling user payment access, providing payment system integration

**Compatibility:** Node.js >= 16.0.0, Bytemark payment system integration, MySQL database, Slack notifications, random password generation

## ❓ Common Questions Quick Index
- **Q: How are Bytemark accounts created?** → Automatically generated with unique email and validated password for each user
- **Q: What password requirements exist?** → Must contain both letters and numbers, generated with 12 characters
- **Q: How is authentication handled?** → OAuth tokens retrieved via login and stored for reuse
- **Q: What happens if account creation fails?** → Comprehensive error handling with fallback queries and specific error codes
- **Q: How are users identified in Bytemark?** → Unique email format: {prefix}.{userId}@mail.connectsmartx.com
- **Q: What monitoring exists?** → Slack integration for error notifications and comprehensive logging

## 📋 Functionality Overview

**Non-technical explanation:** 
Think of this as a **payment account manager** that automatically sets up payment accounts for users behind the scenes. When someone needs to make a payment, this service creates their account, generates a secure password, logs them in, and provides access to the payment system without the user having to manually register.

**Technical explanation:** 
A comprehensive Bytemark payment integration service that handles automatic account provisioning with password generation and validation, OAuth token management with persistence, error handling with Slack notifications, and seamless payment system access through standardized email formats and authentication flows.

**Business value explanation:**
Reduces user friction by eliminating manual payment account setup, ensures consistent payment system integration, provides seamless user experience for transit payments, maintains security through validated password generation, and enables comprehensive monitoring and error tracking.

## 🔧 Technical Specifications

- **File:** `allrepo/connectsmart/tsp-api/src/services/ticketPayment.js`
- **Language:** JavaScript (ES2020)
- **Framework:** Node.js with Knex.js and Bytemark SDK integration
- **Type:** Payment Account Management and Authentication Service
- **File Size:** ~4.3 KB
- **Complexity Score:** ⭐⭐⭐⭐ (High - Complex payment integration with error handling)

**Dependencies:**
- `@maas/services/BytemarkManager`: Bytemark payment system integration (**Critical**)
- `@maas/core/mysql`: Database connectivity (**Critical**)
- `@app/src/helpers/random_text`: Password generation utility (**High**)
- `@app/src/static/error-code`: Error handling definitions (**High**)
- `config`: Environment configuration management (**Critical**)

## 📝 Detailed Code Analysis

### Password Validation System

### validPass Function
**Purpose:** Validates generated passwords meet security requirements

```javascript
function validPass(str) {
  return /[A-Za-z]/.test(str) && /[0-9]/.test(str);
}
```
- **Letter Requirement:** Must contain at least one alphabetic character
- **Number Requirement:** Must contain at least one numeric character
- **Simple Validation:** Basic but effective password complexity check
- **Return Boolean:** True if password meets requirements

### Main Account Check Function

### bytemarkCheck Function
**Purpose:** Ensures user has valid Bytemark account and authentication token

```javascript
const bytemarkCheck = async (ctx) => {
  logger.info('[bytemarkCheck] enter');
  
  // Initialize Bytemark manager with configuration
  const bytemark = new BytemarkManager({
    project: config.portal.projectTitle,
    stage: config.portal.projectStage,
    accountApi: config.vendor.bytemark.url.accountApi,
    logger,
    slackToken: config.vendor.slack.token,
    slackChannelId: config.vendor.slack.channelId,
    originApi: '',
    clientId: config.vendor.bytemark.clientId,
  });
  
  const { userid: userId = -1 } = ctx.request.header;
}
```

**Initialization Features:**
- **Configuration Integration:** Uses environment-specific settings
- **Slack Monitoring:** Integrated error notifications
- **Logger Integration:** Comprehensive logging throughout process
- **Origin Tracking:** Tracks API endpoints for monitoring

### User Data Retrieval

#### Database Query with Join
```javascript
const user = await knex('auth_user')
  .first(
    'auth_user.email',
    'first_name',
    'last_name',
    { bytemark_id: 'bytemark_tokens.id' },
    { bytemark_token: 'bytemark_tokens.token' },
    { bytemark_email: 'bytemark_tokens.email' },
    { bytemark_password: 'bytemark_tokens.password' },
  )
  .leftJoin('bytemark_tokens', 'auth_user.id', 'bytemark_tokens.user_id')
  .where('auth_user.id', userId);
```
- **Left Join Strategy:** Retrieves user data with optional Bytemark token information
- **Selective Fields:** Only fetches required fields for efficiency
- **Alias Usage:** Clear field naming for Bytemark-specific data
- **Single Query:** Efficient data retrieval in one database call

### Account Creation Process

#### Automatic Account Provisioning
```javascript
if (!user.bytemark_email) {
  logger.info('[bytemarkCheck] create account');
  
  // Generate validated password
  let password;
  do {
    password = randomText(12, 2);
  } while (!validPass(password));
  
  // Create unique email address
  const bytemarkEmail = `${config.vendor.bytemark.mailPrefix}.${userId}@mail.connectsmartx.com`;
  
  let inserted = 0;
  try {
    [inserted] = await knex('bytemark_tokens').insert({
      email: bytemarkEmail,
      user_id: userId,
      password,
      status: 'used',
    });
  } catch(error) {
    logger.warn(`[bytemarkCheck] ${error.message}`);
    logger.warn(`[bytemarkCheck] ${error.stack}`);
  }
}
```

**Account Creation Features:**
- **Password Generation Loop:** Ensures password meets validation requirements
- **Unique Email Format:** Standardized email pattern for system integration
- **Database Insertion:** Creates token record with initial status
- **Error Logging:** Comprehensive error tracking for debugging

### Error Recovery and Fallback

#### Insertion Failure Handling
```javascript
try {
  if (inserted === 0) {
    const tokenData = await knex('bytemark_tokens').where({ user_id: userId }).first();
    if (tokenData) {
      inserted = tokenData.id;
    } else {
      logger.warn(`[bytemarkCheck] inserted id not found, either not inserted or query not found.`);
      throw new MaasError(
        ERROR_CODE.ERROR_BYTEMARK_PASS_DATA,
        'warn',
        'ERROR_BYTEMARK_PASS_DATA',
        400,
      );
    }
  }
  
  // Update user object with Bytemark data
  bytemark.originApi = `[${ctx.request.method}] ${ctx.request.path}`;
  if (!user.first_name) user.first_name = 'FirstName';
  if (!user.last_name) user.last_name = 'LastName';
  
  Object.assign(user, {
    bytemark_id: inserted,
    bytemark_email: bytemarkEmail,
    bytemark_password: password,
  });
} catch (error) {
  // Comprehensive error handling
  logger.warn(`[bytemarkCheck] ${error.message}`);
  logger.warn(`[bytemarkCheck] ${error.stack}`);
  throw new MaasError(
    ERROR_CODE.ERROR_BYTEMARK_PASS_DATA,
    'warn',
    'ERROR_BYTEMARK_PASS_DATA',
    400,
  );
}
```

**Fallback Features:**
- **Query Fallback:** Attempts to retrieve existing record if insertion appears to fail
- **Data Validation:** Ensures required user data exists with defaults
- **Object Assignment:** Updates user object with Bytemark-specific information
- **Error Standardization:** Consistent error response format

### Authentication Token Management

#### Token Retrieval and Storage
```javascript
if (!user.bytemark_token) {
  logger.info('[bytemarkCheck] login and get access token');
  bytemark.originApi = `[${ctx.request.method}] ${ctx.request.path}`;
  
  const loginInfo = await bytemark.login(
    user.bytemark_email,
    user.bytemark_password,
  );
  
  if (loginInfo.data) {
    await knex('bytemark_tokens')
      .update({
        token: loginInfo.data.oauth_token,
      })
      .where('id', user.bytemark_id);
      
    Object.assign(user, {
      bytemark_token: loginInfo.data.oauth_token,
    });
  } else {
    logger.warn(`[bytemarkCheck] bytemark login failed. ${JSON.stringify(loginInfo)}`);
    throw new MaasError(
      ERROR_CODE.ERROR_BYTEMARK_PASS_DATA,
      'warn',
      'ERROR_BYTEMARK_PASS_DATA',
      400,
    );
  }
}
```

**Token Management Features:**
- **Origin API Tracking:** Records which endpoint initiated the authentication
- **Login Integration:** Uses Bytemark SDK for authentication
- **Token Persistence:** Stores OAuth token in database for reuse
- **Login Validation:** Checks for successful authentication response
- **Error Handling:** Specific error handling for authentication failures

### Response Structure

#### Successful Response Format
```javascript
return {
  bytemark_email: user.email,
  bytemark_token_status: true,
  bytemark_payment_status: true,
  payment_url: config.vendor.bytemark.url.account,
  service_inbox: config.vendor.bytemark.inboxAddress,
  auth_status: 'success',
  error_data: {},
};
```
- **Email Reference:** Returns original user email (not Bytemark email)
- **Status Indicators:** Boolean flags for token and payment status
- **URL Provision:** Provides payment system access URL
- **Service Information:** Contact information for support
- **Standardized Response:** Consistent response structure for API clients

## 🚀 Usage Methods

### Basic Payment Account Check
```javascript
const ticketPaymentService = require('@app/src/services/ticketPayment');

// Middleware usage in route handler
app.get('/api/payment/check', async (ctx) => {
  try {
    const result = await ticketPaymentService.bytemarkCheck(ctx);
    ctx.body = {
      success: true,
      data: result
    };
  } catch (error) {
    ctx.status = error.status || 500;
    ctx.body = {
      success: false,
      error: error.message
    };
  }
});
```

### Advanced Payment Integration Manager
```javascript
class PaymentIntegrationManager {
  constructor() {
    this.ticketPaymentService = require('@app/src/services/ticketPayment');
    this.userCache = new Map();
    this.cacheTimeout = 300000; // 5 minutes
  }

  async ensurePaymentAccess(ctx, options = {}) {
    try {
      const { userid: userId } = ctx.request.header;
      const cacheKey = `user_${userId}`;
      
      // Check cache first
      if (this.userCache.has(cacheKey) && !options.forceRefresh) {
        const cached = this.userCache.get(cacheKey);
        if (Date.now() - cached.timestamp < this.cacheTimeout) {
          console.log(`Using cached payment data for user ${userId}`);
          return {
            ...cached.data,
            fromCache: true
          };
        }
      }

      // Get fresh payment account data
      const paymentData = await this.ticketPaymentService.bytemarkCheck(ctx);
      
      // Cache the result
      this.userCache.set(cacheKey, {
        data: paymentData,
        timestamp: Date.now()
      });

      return {
        ...paymentData,
        fromCache: false,
        userId: parseInt(userId)
      };
    } catch (error) {
      console.error('Payment access failed:', error);
      
      // Return failure response with error details
      return {
        bytemark_email: null,
        bytemark_token_status: false,
        bytemark_payment_status: false,
        payment_url: null,
        service_inbox: null,
        auth_status: 'failed',
        error_data: {
          message: error.message,
          code: error.code || 'UNKNOWN_ERROR'
        }
      };
    }
  }

  async validatePaymentReadiness(userId) {
    try {
      // Create minimal context for validation
      const mockCtx = {
        request: {
          header: { userid: userId },
          method: 'GET',
          path: '/api/payment/validate'
        }
      };

      const result = await this.ticketPaymentService.bytemarkCheck(mockCtx);
      
      return {
        ready: result.bytemark_token_status && result.bytemark_payment_status,
        accountExists: !!result.bytemark_email,
        tokenValid: result.bytemark_token_status,
        paymentEnabled: result.bytemark_payment_status,
        paymentUrl: result.payment_url,
        supportContact: result.service_inbox
      };
    } catch (error) {
      console.error('Payment readiness validation failed:', error);
      return {
        ready: false,
        accountExists: false,
        tokenValid: false,
        paymentEnabled: false,
        error: error.message
      };
    }
  }

  async refreshPaymentToken(userId) {
    try {
      // Clear cache to force refresh
      this.userCache.delete(`user_${userId}`);
      
      const mockCtx = {
        request: {
          header: { userid: userId },
          method: 'POST',
          path: '/api/payment/refresh'
        }
      };

      const result = await this.ensurePaymentAccess(mockCtx, { forceRefresh: true });
      
      return {
        success: result.auth_status === 'success',
        tokenRefreshed: !result.fromCache,
        data: result
      };
    } catch (error) {
      console.error('Token refresh failed:', error);
      return {
        success: false,
        tokenRefreshed: false,
        error: error.message
      };
    }
  }

  async batchValidateUsers(userIds) {
    const results = [];
    
    // Process users in parallel
    const promises = userIds.map(async (userId) => {
      try {
        const validation = await this.validatePaymentReadiness(userId);
        return {
          userId,
          ...validation
        };
      } catch (error) {
        return {
          userId,
          ready: false,
          error: error.message
        };
      }
    });

    const validationResults = await Promise.all(promises);
    
    return {
      totalUsers: userIds.length,
      readyUsers: validationResults.filter(r => r.ready).length,
      failedUsers: validationResults.filter(r => r.error).length,
      results: validationResults
    };
  }

  getPaymentStatistics() {
    const cacheSize = this.userCache.size;
    let validTokens = 0;
    let expiredEntries = 0;
    const now = Date.now();

    this.userCache.forEach((entry) => {
      if (now - entry.timestamp < this.cacheTimeout) {
        if (entry.data.bytemark_token_status) {
          validTokens++;
        }
      } else {
        expiredEntries++;
      }
    });

    return {
      cacheSize,
      validTokens,
      expiredEntries,
      cacheHitRate: cacheSize > 0 ? ((cacheSize - expiredEntries) / cacheSize * 100).toFixed(2) : '0.00'
    };
  }

  clearExpiredCache() {
    const now = Date.now();
    let cleared = 0;

    this.userCache.forEach((entry, key) => {
      if (now - entry.timestamp >= this.cacheTimeout) {
        this.userCache.delete(key);
        cleared++;
      }
    });

    return {
      cleared,
      remaining: this.userCache.size
    };
  }
}

// Usage
const paymentManager = new PaymentIntegrationManager();

// Ensure payment access with caching
const paymentData = await paymentManager.ensurePaymentAccess(ctx);
console.log('Payment access result:', paymentData);

// Validate payment readiness
const readiness = await paymentManager.validatePaymentReadiness(12345);
console.log('Payment readiness:', readiness);

// Batch validate multiple users
const batchResult = await paymentManager.batchValidateUsers([12345, 67890, 11111]);
console.log('Batch validation result:', batchResult);

// Get statistics
const stats = paymentManager.getPaymentStatistics();
console.log('Payment statistics:', stats);
```

### Error Handling and Monitoring
```javascript
class PaymentErrorMonitor {
  constructor() {
    this.ticketPaymentService = require('@app/src/services/ticketPayment');
    this.errorCounts = new Map();
    this.recentErrors = [];
    this.maxRecentErrors = 100;
  }

  async monitoredPaymentCheck(ctx) {
    const startTime = Date.now();
    const { userid: userId } = ctx.request.header;
    
    try {
      const result = await this.ticketPaymentService.bytemarkCheck(ctx);
      const duration = Date.now() - startTime;
      
      this.recordSuccess(userId, duration);
      
      return {
        ...result,
        monitoring: {
          success: true,
          duration,
          userId: parseInt(userId),
          timestamp: new Date().toISOString()
        }
      };
    } catch (error) {
      const duration = Date.now() - startTime;
      
      this.recordError(userId, error, duration);
      
      throw {
        ...error,
        monitoring: {
          success: false,
          duration,
          userId: parseInt(userId),
          timestamp: new Date().toISOString(),
          errorCode: error.code,
          errorMessage: error.message
        }
      };
    }
  }

  recordSuccess(userId, duration) {
    console.log(`Payment check succeeded for user ${userId} in ${duration}ms`);
    
    // Could integrate with metrics collection
    this.updateMetrics('success', userId, duration);
  }

  recordError(userId, error, duration) {
    const errorKey = error.code || 'UNKNOWN_ERROR';
    
    // Update error counts
    const currentCount = this.errorCounts.get(errorKey) || 0;
    this.errorCounts.set(errorKey, currentCount + 1);
    
    // Add to recent errors
    const errorRecord = {
      userId: parseInt(userId),
      errorCode: errorKey,
      errorMessage: error.message,
      duration,
      timestamp: new Date().toISOString(),
      stack: error.stack
    };
    
    this.recentErrors.unshift(errorRecord);
    
    // Keep only recent errors
    if (this.recentErrors.length > this.maxRecentErrors) {
      this.recentErrors = this.recentErrors.slice(0, this.maxRecentErrors);
    }
    
    console.error(`Payment check failed for user ${userId}:`, error.message);
    
    // Send alert for critical errors
    if (this.isCriticalError(errorKey)) {
      this.sendCriticalAlert(errorRecord);
    }
  }

  updateMetrics(type, userId, duration) {
    // Placeholder for metrics integration
    console.log(`Metrics: ${type} for user ${userId}, duration: ${duration}ms`);
  }

  isCriticalError(errorCode) {
    const criticalErrors = [
      'ERROR_BYTEMARK_PASS_DATA',
      'DATABASE_CONNECTION_ERROR',
      'CONFIGURATION_ERROR'
    ];
    return criticalErrors.includes(errorCode);
  }

  async sendCriticalAlert(errorRecord) {
    console.log('CRITICAL PAYMENT ERROR:', errorRecord);
    
    // Integration with alerting system
    const alertMessage = `
      Critical payment system error detected:
      User: ${errorRecord.userId}
      Error: ${errorRecord.errorCode} - ${errorRecord.errorMessage}
      Time: ${errorRecord.timestamp}
      Duration: ${errorRecord.duration}ms
    `;
    
    // Could send to Slack, email, or other alerting systems
    // await slackNotifier.sendAlert(alertMessage);
  }

  getErrorReport() {
    const totalErrors = Array.from(this.errorCounts.values())
      .reduce((sum, count) => sum + count, 0);
      
    const errorBreakdown = {};
    this.errorCounts.forEach((count, errorCode) => {
      errorBreakdown[errorCode] = {
        count,
        percentage: totalErrors > 0 ? (count / totalErrors * 100).toFixed(2) : '0.00'
      };
    });
    
    return {
      totalErrors,
      errorBreakdown,
      recentErrorsCount: this.recentErrors.length,
      topErrors: this.getTopErrors(5),
      recentErrors: this.recentErrors.slice(0, 10) // Last 10 errors
    };
  }

  getTopErrors(limit = 5) {
    return Array.from(this.errorCounts.entries())
      .sort(([,a], [,b]) => b - a)
      .slice(0, limit)
      .map(([errorCode, count]) => ({ errorCode, count }));
  }

  clearErrorHistory() {
    this.errorCounts.clear();
    this.recentErrors = [];
    
    return {
      message: 'Error history cleared',
      timestamp: new Date().toISOString()
    };
  }
}

// Usage
const errorMonitor = new PaymentErrorMonitor();

// Monitored payment check
app.get('/api/payment/monitored-check', async (ctx) => {
  try {
    const result = await errorMonitor.monitoredPaymentCheck(ctx);
    ctx.body = {
      success: true,
      data: result
    };
  } catch (error) {
    ctx.status = error.status || 500;
    ctx.body = {
      success: false,
      error: error.monitoring || { message: error.message }
    };
  }
});

// Error reporting endpoint
app.get('/api/payment/error-report', (ctx) => {
  const report = errorMonitor.getErrorReport();
  ctx.body = {
    success: true,
    data: report
  };
});
```

## 📊 Output Examples

### Successful Payment Check Response
```javascript
{
  bytemark_email: "user@example.com",
  bytemark_token_status: true,
  bytemark_payment_status: true,
  payment_url: "https://account.bytemark.com",
  service_inbox: "support@bytemark.com",
  auth_status: "success",
  error_data: {}
}
```

### Payment Readiness Validation
```javascript
{
  ready: true,
  accountExists: true,
  tokenValid: true,
  paymentEnabled: true,
  paymentUrl: "https://account.bytemark.com",
  supportContact: "support@bytemark.com"
}
```

### Batch User Validation
```javascript
{
  totalUsers: 3,
  readyUsers: 2,
  failedUsers: 1,
  results: [
    {
      userId: 12345,
      ready: true,
      accountExists: true,
      tokenValid: true,
      paymentEnabled: true
    },
    {
      userId: 67890,
      ready: false,
      accountExists: false,
      error: "User not found"
    }
  ]
}
```

### Error Monitoring Report
```javascript
{
  totalErrors: 15,
  errorBreakdown: {
    "ERROR_BYTEMARK_PASS_DATA": {
      count: 8,
      percentage: "53.33"
    },
    "DATABASE_CONNECTION_ERROR": {
      count: 4,
      percentage: "26.67"
    }
  },
  recentErrorsCount: 15,
  topErrors: [
    { errorCode: "ERROR_BYTEMARK_PASS_DATA", count: 8 },
    { errorCode: "DATABASE_CONNECTION_ERROR", count: 4 }
  ],
  recentErrors: [
    {
      userId: 12345,
      errorCode: "ERROR_BYTEMARK_PASS_DATA",
      errorMessage: "Authentication failed",
      duration: 1250,
      timestamp: "2024-06-25T14:30:00.000Z"
    }
  ]
}
```

## ⚠️ Important Notes

### Security and Authentication
- **Password Generation:** Automatic generation with validation ensures secure passwords
- **Token Management:** OAuth tokens stored securely and reused to minimize authentication calls
- **Unique Email Format:** Standardized email pattern prevents conflicts and ensures uniqueness
- **Error Sanitization:** Sensitive information properly handled in error responses

### Database and Transaction Handling
- **Upsert Pattern:** Handles race conditions with insertion failure fallback queries
- **Transaction Safety:** Uses appropriate error handling for database operations
- **Foreign Key Relations:** Proper linking between auth_user and bytemark_tokens tables
- **Status Tracking:** Maintains token status for account lifecycle management

### Integration and Configuration
- **Environment Configuration:** Uses config-driven approach for different environments
- **Slack Integration:** Built-in error monitoring and alerting capabilities
- **Bytemark SDK:** Leverages official Bytemark SDK for payment system integration
- **Origin Tracking:** Records API endpoints for monitoring and debugging

### Error Handling and Monitoring
- **Comprehensive Logging:** Detailed logging throughout the account creation and authentication flow
- **Standardized Errors:** Uses consistent error codes and response formats
- **Fallback Recovery:** Multiple recovery strategies for common failure scenarios
- **Service Monitoring:** Integration with external monitoring systems for production use

## 🔗 Related File Links

- **Bytemark Services:** `@maas/services/BytemarkManager` - Payment system integration
- **Random Text Helper:** `allrepo/connectsmart/tsp-api/src/helpers/random_text.js`
- **Error Codes:** `allrepo/connectsmart/tsp-api/src/static/error-code.js`
- **Payment Controllers:** Controllers that use this service for payment functionality

---
*This service provides comprehensive Bytemark payment account management with automatic provisioning and authentication for seamless payment integration in the TSP platform.*