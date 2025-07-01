# TSP API Transit Payment Service Documentation

## 🔍 Quick Summary (TL;DR)
The Transit Payment service manages transit ticket activation through Bytemark integration with OAuth token management, transaction logging, cache management, and scheduled refresh operations, currently disabled but maintaining full infrastructure for future activation.

**Keywords:** transit-tickets | bytemark-integration | oauth-tokens | ticket-activation | payment-processing | cache-management | scheduled-refresh | ticket-logging

**Primary use cases:** Activating transit tickets via Bytemark API, managing OAuth tokens, logging ticket usage, scheduling ticket refresh operations

**Compatibility:** Node.js >= 16.0.0, Bytemark API integration, MySQL database transactions, cache management system, event tracking

## ❓ Common Questions Quick Index
- **Q: Is the service currently active?** → No, passUse function throws error - service disabled but infrastructure maintained
- **Q: How does ticket activation work?** → OAuth token-based activation through Bytemark API with transaction logging
- **Q: What happens after activation?** → Sends events, updates cache, schedules refresh operations at 3h and 24h intervals
- **Q: How are errors handled?** → Database transactions with rollback, comprehensive error logging and Slack notifications
- **Q: What tokens are managed?** → OAuth tokens stored in bytemark_tokens table for user authentication
- **Q: How is caching used?** → Ticket cache activation and immediate refresh checking for performance

## 📋 Functionality Overview

**Non-technical explanation:** 
Think of this as a **digital ticket validator** for public transit. When you want to use a transit ticket on your phone, this service talks to the transit company's system (Bytemark) to activate your ticket, keeps track of when you used it, and sets up automatic checks to make sure your ticket stays valid. Currently, the system is turned off but ready to be activated when needed.

**Technical explanation:** 
A comprehensive transit payment processing service that integrates with Bytemark's ticket management API through OAuth authentication, implements database transaction management for ticket activation tracking, provides cache management for performance optimization, schedules automatic refresh operations, and maintains complete audit trails with event tracking and error monitoring.

**Business value explanation:**
Enables seamless digital transit ticket activation, provides reliable payment processing infrastructure, supports user engagement through transit services, maintains detailed transaction records for compliance, and offers scalable foundation for multi-transit operator integration.

## 🔧 Technical Specifications

- **File:** `allrepo/connectsmart/tsp-api/src/services/transit-payment.js`
- **Language:** JavaScript (ES2020)
- **Framework:** Node.js with Knex.js ORM and Bytemark integration
- **Type:** Transit Payment Processing Service
- **File Size:** ~4.2 KB
- **Complexity Score:** ⭐⭐⭐⭐ (High - Transaction management with external API integration)

**Dependencies:**
- `@maas/services`: BytemarkManager for API integration (**Critical**)
- `@maas/core/mysql`: Database connection management (**Critical**)
- `@app/src/services/bytemarkCache`: Cache management operations (**High**)
- `@app/src/models/BytemarkTicketRefreshLog`: Refresh scheduling model (**High**)
- `@app/src/helpers/send-event`: Event tracking system (**Medium**)

## 📝 Detailed Code Analysis

### Bytemark Manager Configuration

### getBytemarkManager Function
**Purpose:** Creates configured BytemarkManager instance with project settings and monitoring

```javascript
function getBytemarkManager(ctx) {
  return new BytemarkManager({
    project: config.portal.projectTitle,
    stage: config.portal.projectStage,
    customerApi: config.vendor.bytemark.url.customerApi,
    accountApi: config.vendor.bytemark.url.accountApi,
    logger,
    slackToken: config.vendor.slack.token,
    slackChannelId: config.vendor.slack.channelId,
    originApi: `[${ctx.request.method}] ${ctx.request.path}`,
    clientId: config.vendor.bytemark.clientId,
  });
}
```

**Configuration Features:**
- **Environment-Aware:** Uses project title and stage for proper API routing
- **Dual API Support:** Separate customer and account API endpoints
- **Monitoring Integration:** Slack notifications for API failures and issues
- **Request Tracking:** Origin API tracking for debugging and analytics
- **Client Authentication:** Configured client ID for Bytemark API access

### Transit Ticket Activation System

### passUse Function (Currently Disabled)
**Purpose:** Handles transit ticket activation through Bytemark API with comprehensive transaction management

```javascript
async function passUse(ctx, data) {
  // Service currently disabled
  throw new MaasError(
    ERROR_CODE.ERROR_TRANSIT_TICKET_SYSTEM,
    'error',
    'ERROR_TRANSIT_TICKET_SYSTEM',
    400,
  );

  // OAuth token retrieval
  const tokenRow = await knex('bytemark_tokens').where({
    user_id: data.userId,
  });
  let oauthToken = '';
  if (tokenRow.length > 0) {
    oauthToken = tokenRow[0].token;
  }

  const nowTime = new Date().toISOString().replace('T', ' ').split('.')[0];
  logger.debug(
    `[passUse] oauth_token: ${oauthToken}, pass_uuid: ${data.pass_uuid}, event_uuid: ${data.event_uuid}`,
  );

  const trx = await knex.transaction();
  let bytemarkPassId = 0;
  
  try {
    // Bytemark API call
    const bytemark = getBytemarkManager(ctx);
    const response = await bytemark.usePass(oauthToken, data.pass_uuid);
    
    if (typeof response.errors !== 'undefined') {
      if (typeof response.errors[0] !== 'undefined') {
        logger.warn(
          `[passUse] bytemark error: ${JSON.stringify(response.errors)}`,
        );
        throw new MaasError(
          ERROR_CODE.ERROR_PASS_DATA,
          'error',
          'ERROR_PASS_DATA',
          400,
        );
      }
    }

    // Database transaction after successful API call
    const row = await trx('bytemark_pass')
      .where({ pass_uuid: data.pass_uuid })
      .first();
      
    if (!row) {
      const insertData = {
        oauth_token: oauthToken,
        pass_uuid: data.pass_uuid,
        event_uuid: data.event_uuid,
        time_used: nowTime,
      };
      [bytemarkPassId] = await trx('bytemark_pass').insert(insertData);
    } else {
      logger.info(`[passUse] pass_uuid: ${data.pass_uuid} has already been used`);
    }
    
    await trx.commit();
  } catch (e) {
    await trx.rollback();
    logger.error(`[passUse] error: ${e.message}`);
    logger.info(`[passUse] stack: ${e.stack}`);
    throw e;
  }
```

**Activation Process Features:**
- **OAuth Token Management:** Retrieves user-specific authentication tokens
- **API Error Handling:** Comprehensive error checking for Bytemark responses
- **Transaction Safety:** Database transactions with rollback on failure
- **Duplicate Prevention:** Checks for already-used passes to prevent double activation
- **Comprehensive Logging:** Debug, info, warn, and error level logging

### Post-Activation Operations

### Event Tracking and Scheduling
```javascript
  // Send activation event
  await sendEvent([
    {
      userIds: [data.userId],
      eventName: 'transit_ticket',
      eventMeta: {
        action: 'activate',
        bytemark_pass_id: bytemarkPassId,
      },
    },
  ]);

  // Log app usage data
  await insertAppData(data.userId, data.zone, 'ActivateTicket');
  
  // Create refresh log entry
  await BytemarkTicketRefreshLog.query().insert({
    user_id: data.userId,
    activity_type: 1,
    status: 0,
  });

  // Schedule refresh operations
  const p3h = new Date(new Date().getTime() + 1000 * 60 * 60 * 3)
    .toISOString()
    .replace('T', ' ')
    .split('.')[0];
    
  const p24h =
    new Date(new Date().getTime() + 1000 * 60 * 60 * 24)
      .toISOString()
      .split('T')[0] + ' 15:00:00';
      
  await knex('bytemark_ticket_refresh_log').insert([
    {
      user_id: data.userId,
      activity_type: 3,
      status: 0,
      scheduled_on: p3h,
    },
    {
      user_id: data.userId,
      activity_type: 3,
      status: 0,
      scheduled_on: p24h,
    },
  ]);

  // Cache management
  await activateCache(data.userId, data.pass_uuid);
  
  // Immediate cache refresh (non-blocking)
  setImmediate(async () => {
    try {
      await checkTicketCache(data.userId);
    } catch (e) {
      logger.warn(e.message);
      logger.warn(e.stack);
    }
  });

  return {};
```

**Post-Activation Features:**
- **Event Broadcasting:** Sends activation events for analytics and notifications
- **Usage Tracking:** Records app data for user engagement analysis
- **Scheduled Refresh:** Automatic refresh at 3 hours and daily at 3 PM
- **Cache Optimization:** Immediate cache activation and refresh checking
- **Non-Blocking Operations:** Uses setImmediate for performance optimization

## 🚀 Usage Methods

### Basic Transit Payment Integration (When Enabled)
```javascript
const transitPayment = require('@app/src/services/transit-payment');

// Activate transit ticket (currently disabled)
try {
  const activationData = {
    userId: 12345,
    pass_uuid: 'ab12cd34-ef56-7890-gh12-ijklmnop3456',
    event_uuid: 'ev78mn90-qr12-3456-st78-uvwxyz123456',
    zone: 'America/Chicago'
  };

  const result = await transitPayment.passUse(ctx, activationData);
  console.log('Ticket activated successfully:', result);
} catch (error) {
  console.error('Ticket activation failed:', error.message);
  // Currently throws ERROR_TRANSIT_TICKET_SYSTEM
}
```

### Advanced Transit Payment Management System
```javascript
class TransitPaymentManager {
  constructor() {
    this.transitPayment = require('@app/src/services/transit-payment');
    this.activationHistory = new Map();
    this.performanceMetrics = {
      totalActivations: 0,
      successfulActivations: 0,
      failedActivations: 0,
      averageActivationTime: 0
    };
  }

  async simulateTicketActivation(ticketData, options = {}) {
    // Simulation method since actual service is disabled
    try {
      const { 
        userId, 
        pass_uuid, 
        event_uuid, 
        zone = 'America/Chicago',
        simulateSuccess = true,
        simulateDelay = 1000
      } = { ...ticketData, ...options };

      const startTime = Date.now();

      // Simulate activation delay
      await this.delay(simulateDelay);

      if (!simulateSuccess) {
        throw new Error('Simulated activation failure');
      }

      const activationResult = {
        success: true,
        userId,
        pass_uuid,
        event_uuid,
        activatedAt: new Date().toISOString(),
        processingTime: Date.now() - startTime,
        simulation: true
      };

      // Track activation history
      this.recordActivation(userId, activationResult);
      
      // Update metrics
      this.performanceMetrics.totalActivations++;
      this.performanceMetrics.successfulActivations++;
      this.updateAverageActivationTime(Date.now() - startTime);

      return activationResult;
    } catch (error) {
      this.performanceMetrics.totalActivations++;
      this.performanceMetrics.failedActivations++;
      
      return {
        success: false,
        error: error.message,
        simulation: true
      };
    }
  }

  async batchActivateTickets(ticketBatch, options = {}) {
    const { 
      maxConcurrent = 5, 
      retryAttempts = 2,
      retryDelay = 2000 
    } = options;

    const results = [];
    const semaphore = new Array(maxConcurrent).fill(null);
    
    const processTicket = async (ticket, index) => {
      let lastError;
      
      for (let attempt = 1; attempt <= retryAttempts; attempt++) {
        try {
          const result = await this.simulateTicketActivation(ticket, {
            simulateSuccess: Math.random() > 0.1, // 90% success rate
            simulateDelay: 500 + Math.random() * 1000
          });
          
          return {
            index,
            ticket,
            result,
            attempt,
            success: result.success
          };
        } catch (error) {
          lastError = error;
          
          if (attempt < retryAttempts) {
            await this.delay(retryDelay * attempt);
          }
        }
      }
      
      return {
        index,
        ticket,
        result: { success: false, error: lastError.message },
        attempt: retryAttempts,
        success: false
      };
    };

    // Process tickets with concurrency control
    const promises = ticketBatch.map(async (ticket, index) => {
      // Wait for available slot
      await Promise.race(semaphore.map(async (_, i) => {
        while (semaphore[i] !== null) {
          await this.delay(10);
        }
        semaphore[i] = index;
        return i;
      }));

      try {
        const result = await processTicket(ticket, index);
        
        // Release slot
        const slotIndex = semaphore.indexOf(index);
        if (slotIndex !== -1) {
          semaphore[slotIndex] = null;
        }
        
        return result;
      } catch (error) {
        const slotIndex = semaphore.indexOf(index);
        if (slotIndex !== -1) {
          semaphore[slotIndex] = null;
        }
        throw error;
      }
    });

    const batchResults = await Promise.all(promises);
    
    return {
      totalProcessed: batchResults.length,
      successful: batchResults.filter(r => r.success).length,
      failed: batchResults.filter(r => !r.success).length,
      results: batchResults,
      processingTime: Math.max(...batchResults.map(r => r.result.processingTime || 0))
    };
  }

  async validateTokenAvailability(userId) {
    try {
      // Simulate token validation since service is disabled
      const hasValidToken = Math.random() > 0.2; // 80% have valid tokens
      
      if (!hasValidToken) {
        return {
          valid: false,
          error: 'No valid OAuth token found for user',
          requiresReauth: true
        };
      }

      return {
        valid: true,
        tokenExpiresIn: Math.floor(Math.random() * 86400), // Random seconds until expiry
        lastRefreshed: new Date(Date.now() - Math.random() * 86400000).toISOString()
      };
    } catch (error) {
      return {
        valid: false,
        error: error.message,
        requiresReauth: true
      };
    }
  }

  async scheduleTicketRefresh(userId, scheduleOptions = {}) {
    try {
      const {
        refreshIn3Hours = true,
        refreshDaily = true,
        dailyRefreshTime = '15:00:00'
      } = scheduleOptions;

      const scheduledOperations = [];

      if (refreshIn3Hours) {
        const refreshTime3h = new Date(Date.now() + 3 * 60 * 60 * 1000);
        scheduledOperations.push({
          userId,
          activityType: 3,
          scheduledOn: refreshTime3h.toISOString(),
          type: 'short_term_refresh'
        });
      }

      if (refreshDaily) {
        const tomorrow = new Date();
        tomorrow.setDate(tomorrow.getDate() + 1);
        const dailyRefresh = new Date(
          tomorrow.toISOString().split('T')[0] + 'T' + dailyRefreshTime + 'Z'
        );
        
        scheduledOperations.push({
          userId,
          activityType: 3,
          scheduledOn: dailyRefresh.toISOString(),
          type: 'daily_refresh'
        });
      }

      return {
        success: true,
        userId,
        scheduledOperations,
        message: `Scheduled ${scheduledOperations.length} refresh operations`
      };
    } catch (error) {
      return {
        success: false,
        error: error.message,
        userId
      };
    }
  }

  async getCacheStatus(userId) {
    try {
      // Simulate cache status check
      const cacheStatus = {
        userId,
        hasCachedTickets: Math.random() > 0.3, // 70% have cached tickets
        cacheSize: Math.floor(Math.random() * 10),
        lastUpdated: new Date(Date.now() - Math.random() * 3600000).toISOString(),
        needsRefresh: Math.random() > 0.8 // 20% need refresh
      };

      return {
        success: true,
        ...cacheStatus
      };
    } catch (error) {
      return {
        success: false,
        error: error.message,
        userId
      };
    }
  }

  recordActivation(userId, activationData) {
    const userHistory = this.activationHistory.get(userId) || [];
    userHistory.push({
      ...activationData,
      timestamp: new Date().toISOString()
    });
    
    // Keep only last 50 activations per user
    this.activationHistory.set(userId, userHistory.slice(-50));
  }

  getUserActivationHistory(userId) {
    const history = this.activationHistory.get(userId) || [];
    
    return {
      userId,
      totalActivations: history.length,
      recentActivations: history.slice(-10),
      firstActivation: history.length > 0 ? history[0].timestamp : null,
      lastActivation: history.length > 0 ? history[history.length - 1].timestamp : null,
      successRate: history.length > 0 
        ? (history.filter(h => h.success).length / history.length * 100).toFixed(2) + '%'
        : '0%'
    };
  }

  async performSystemHealthCheck() {
    try {
      const healthChecks = await Promise.all([
        this.checkDatabaseConnectivity(),
        this.checkBytemarkApiConnectivity(),
        this.checkCacheSystemHealth(),
        this.checkSchedulerHealth()
      ]);

      const overallHealth = healthChecks.every(check => check.status === 'healthy');

      return {
        overallStatus: overallHealth ? 'healthy' : 'degraded',
        timestamp: new Date().toISOString(),
        checks: {
          database: healthChecks[0],
          bytemarkApi: healthChecks[1],
          cacheSystem: healthChecks[2],
          scheduler: healthChecks[3]
        },
        metrics: this.performanceMetrics
      };
    } catch (error) {
      return {
        overallStatus: 'unhealthy',
        error: error.message,
        timestamp: new Date().toISOString()
      };
    }
  }

  async checkDatabaseConnectivity() {
    // Simulate database health check
    return {
      component: 'database',
      status: Math.random() > 0.05 ? 'healthy' : 'unhealthy',
      responseTime: Math.floor(Math.random() * 100) + 10,
      lastChecked: new Date().toISOString()
    };
  }

  async checkBytemarkApiConnectivity() {
    // Simulate Bytemark API health check
    return {
      component: 'bytemark_api',
      status: Math.random() > 0.1 ? 'healthy' : 'unhealthy',
      responseTime: Math.floor(Math.random() * 500) + 100,
      lastChecked: new Date().toISOString(),
      note: 'Service currently disabled'
    };
  }

  async checkCacheSystemHealth() {
    // Simulate cache system health check
    return {
      component: 'cache_system',
      status: Math.random() > 0.02 ? 'healthy' : 'unhealthy',
      responseTime: Math.floor(Math.random() * 50) + 5,
      lastChecked: new Date().toISOString()
    };
  }

  async checkSchedulerHealth() {
    // Simulate scheduler health check
    return {
      component: 'scheduler',
      status: Math.random() > 0.03 ? 'healthy' : 'unhealthy',
      pendingJobs: Math.floor(Math.random() * 100),
      lastChecked: new Date().toISOString()
    };
  }

  updateAverageActivationTime(processingTime) {
    const total = this.performanceMetrics.totalActivations;
    const currentAverage = this.performanceMetrics.averageActivationTime;
    
    this.performanceMetrics.averageActivationTime = 
      ((currentAverage * (total - 1)) + processingTime) / total;
  }

  async delay(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
  }

  getSystemStatistics() {
    return {
      ...this.performanceMetrics,
      successRate: this.performanceMetrics.totalActivations > 0
        ? (this.performanceMetrics.successfulActivations / this.performanceMetrics.totalActivations * 100).toFixed(2) + '%'
        : '0%',
      totalUsers: this.activationHistory.size,
      averageActivationsPerUser: this.activationHistory.size > 0
        ? (Array.from(this.activationHistory.values()).reduce((sum, history) => sum + history.length, 0) / this.activationHistory.size).toFixed(2)
        : '0'
    };
  }

  clearHistory() {
    this.activationHistory.clear();
    this.performanceMetrics = {
      totalActivations: 0,
      successfulActivations: 0,
      failedActivations: 0,
      averageActivationTime: 0
    };
    
    return { message: 'Transit payment history and metrics cleared' };
  }
}

// Usage
const transitManager = new TransitPaymentManager();

// Simulate ticket activation
const ticketData = {
  userId: 12345,
  pass_uuid: 'ab12cd34-ef56-7890-gh12-ijklmnop3456',
  event_uuid: 'ev78mn90-qr12-3456-st78-uvwxyz123456'
};

const activationResult = await transitManager.simulateTicketActivation(ticketData);
console.log('Activation result:', activationResult);

// Batch process tickets
const ticketBatch = [
  { userId: 12345, pass_uuid: 'uuid1', event_uuid: 'event1' },
  { userId: 12346, pass_uuid: 'uuid2', event_uuid: 'event2' },
  { userId: 12347, pass_uuid: 'uuid3', event_uuid: 'event3' }
];

const batchResult = await transitManager.batchActivateTickets(ticketBatch);
console.log('Batch activation results:', batchResult);

// Check system health
const healthCheck = await transitManager.performSystemHealthCheck();
console.log('System health:', healthCheck);

// Get user activation history
const userHistory = transitManager.getUserActivationHistory(12345);
console.log('User activation history:', userHistory);
```

## 📊 Output Examples

### Successful Ticket Activation (When Enabled)
```javascript
{
  // Currently returns empty object after successful activation
}
```

### Current Service Status
```javascript
// Throws MaasError
{
  code: "ERROR_TRANSIT_TICKET_SYSTEM",
  level: "error",
  message: "ERROR_TRANSIT_TICKET_SYSTEM",
  statusCode: 400
}
```

### Simulated Activation Result
```javascript
{
  success: true,
  userId: 12345,
  pass_uuid: "ab12cd34-ef56-7890-gh12-ijklmnop3456",
  event_uuid: "ev78mn90-qr12-3456-st78-uvwxyz123456",
  activatedAt: "2024-06-25T14:30:00.000Z",
  processingTime: 1250,
  simulation: true
}
```

### Batch Processing Results
```javascript
{
  totalProcessed: 3,
  successful: 2,
  failed: 1,
  results: [
    {
      index: 0,
      ticket: { userId: 12345, pass_uuid: "uuid1", event_uuid: "event1" },
      result: { success: true, processingTime: 1100 },
      attempt: 1,
      success: true
    },
    {
      index: 1,
      ticket: { userId: 12346, pass_uuid: "uuid2", event_uuid: "event2" },
      result: { success: false, error: "Simulated activation failure" },
      attempt: 2,
      success: false
    }
  ],
  processingTime: 1500
}
```

### System Health Check
```javascript
{
  overallStatus: "degraded",
  timestamp: "2024-06-25T14:30:00.000Z",
  checks: {
    database: {
      component: "database",
      status: "healthy",
      responseTime: 45,
      lastChecked: "2024-06-25T14:30:00.000Z"
    },
    bytemarkApi: {
      component: "bytemark_api", 
      status: "unhealthy",
      responseTime: 2500,
      lastChecked: "2024-06-25T14:30:00.000Z",
      note: "Service currently disabled"
    },
    cacheSystem: {
      component: "cache_system",
      status: "healthy",
      responseTime: 15,
      lastChecked: "2024-06-25T14:30:00.000Z"
    },
    scheduler: {
      component: "scheduler",
      status: "healthy",
      pendingJobs: 23,
      lastChecked: "2024-06-25T14:30:00.000Z"
    }
  },
  metrics: {
    totalActivations: 150,
    successfulActivations: 142,
    failedActivations: 8,
    averageActivationTime: 1125
  }
}
```

### User Activation History
```javascript
{
  userId: 12345,
  totalActivations: 25,
  recentActivations: [
    {
      success: true,
      pass_uuid: "recent-uuid-1",
      activatedAt: "2024-06-25T14:00:00.000Z",
      timestamp: "2024-06-25T14:00:00.000Z"
    }
  ],
  firstActivation: "2024-06-01T10:30:00.000Z",
  lastActivation: "2024-06-25T14:00:00.000Z",
  successRate: "96.00%"
}
```

## ⚠️ Important Notes

### Service Status and Infrastructure
- **Currently Disabled:** Service throws ERROR_TRANSIT_TICKET_SYSTEM error but maintains full infrastructure
- **Complete Implementation:** All activation logic, database operations, and scheduling implemented
- **Ready for Activation:** Can be enabled by removing the error throw in passUse function
- **Infrastructure Maintained:** Database schemas, cache management, and monitoring systems operational

### Transaction Management and Safety
- **Database Transactions:** Full ACID compliance with rollback on API failures
- **API-First Approach:** Confirms Bytemark activation before database recording
- **Duplicate Prevention:** Checks for existing pass usage to prevent double activation
- **Comprehensive Error Handling:** Detailed error logging with stack traces

### OAuth Token and Authentication
- **User-Specific Tokens:** Individual OAuth tokens stored per user in bytemark_tokens table
- **Token Retrieval:** Automatic token lookup for API authentication
- **Authentication Flow:** Requires pre-existing OAuth tokens for activation
- **Security Considerations:** Tokens must be securely managed and refreshed

### Scheduling and Cache Management
- **Dual Refresh Schedule:** 3-hour and daily (3 PM) refresh operations
- **Immediate Cache Updates:** Non-blocking cache refresh after activation
- **Activity Logging:** Comprehensive refresh log for monitoring and debugging
- **Performance Optimization:** Cache activation and immediate refresh checking

## 🔗 Related File Links

- **Bytemark Cache:** `allrepo/connectsmart/tsp-api/src/services/bytemarkCache.js`
- **Refresh Log Model:** `allrepo/connectsmart/tsp-api/src/models/BytemarkTicketRefreshLog.js`
- **Event Helpers:** `allrepo/connectsmart/tsp-api/src/helpers/send-event.js`
- **App Data Helpers:** `allrepo/connectsmart/tsp-api/src/helpers/insert-app-data.js`

---
*This service provides comprehensive transit payment infrastructure with Bytemark integration, currently disabled but fully functional and ready for activation when needed.*