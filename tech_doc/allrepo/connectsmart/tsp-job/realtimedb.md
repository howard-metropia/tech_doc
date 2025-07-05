# RealtimeDB Service

## Quick Summary

The RealtimeDB service is a Firebase real-time database management system that handles the cleanup and maintenance of user incentive notification states. This service specifically manages the "red dot" notification system, automatically expiring outdated incentive tiles in the user interface to ensure users see only current and relevant incentive opportunities. The service operates as a scheduled cleanup job that queries user profiles and updates notification visibility based on expiration timestamps.

**Key Features:**
- Automated red dot notification cleanup for expired incentives
- Firebase Real-time Database integration for live UI updates
- Timestamp-based expiration management using Unix epoch time
- Safe connection handling with automatic cleanup
- Error handling and logging for operational monitoring
- User profile querying with conditional updates

## Technical Analysis

### Architecture Overview

The service is built around Firebase Admin SDK integration, providing a single-purpose cleanup function that queries user profiles, checks incentive expiration times, and updates notification states accordingly. The architecture follows a query-update pattern with automatic resource cleanup.

### Core Functionality

```javascript
const checkRedDotStatus = () => {
  try {
    admin.initializeApp({
      credential: admin.credential.cert(serviceAccount),
      databaseURL: firebaseConfig.realtimeDBUrl
    });
    
    const timestampInSeconds = Math.floor(Date.now() / 1000);
    const db = admin.database();
    
    db.ref("profile").orderByChild("incentive/available_tile").equalTo(true).once("value",(snapshot)=>{
      if (snapshot.exists()) {
        snapshot.forEach((childSnapshot) => {
          const userId = childSnapshot.key;
          const userInfo = childSnapshot.child("incentive").val();
          
          if (userInfo.end_date < timestampInSeconds) {
            db.ref(`profile/${userId}/incentive`).update({ available_tile: false })
          }
        });
      }
      return admin.app().delete();
    })    
  } catch (err) {
    logger.warn(err.message);
  }
}
```

### Firebase Integration Architecture

#### 1. Connection Management
The service establishes temporary Firebase connections for each cleanup operation:
- **Credential Management**: Uses service account JSON for authentication
- **Database URL Configuration**: Connects to environment-specific Firebase instance
- **Connection Cleanup**: Automatically deletes app instance after operations

#### 2. Query Pattern
```javascript
// Query users with active incentive tiles
db.ref("profile").orderByChild("incentive/available_tile").equalTo(true)
```

#### 3. Conditional Updates
```javascript
// Update only expired incentives
if (userInfo.end_date < timestampInSeconds) {
  db.ref(`profile/${userId}/incentive`).update({ available_tile: false })
}
```

### Data Structure

The service operates on Firebase user profiles with the following structure:
```javascript
{
  "profile": {
    "userId": {
      "incentive": {
        "available_tile": true,      // Boolean flag for UI notification
        "end_date": 1703980800       // Unix timestamp (seconds)
      }
    }
  }
}
```

### Error Handling Strategy

The service implements defensive programming patterns:
- **Try-catch blocks**: Comprehensive error catching for Firebase operations
- **Existence checks**: Validates snapshot data before processing
- **Connection cleanup**: Ensures Firebase connections are properly closed
- **Logging integration**: Error messages are logged for monitoring

## Usage/Integration

### Primary Integration Points

#### 1. Scheduled Cleanup Execution
```javascript
const { checkRedDotStatus } = require('@app/src/services/realtimedb');

// Execute red dot cleanup
await checkRedDotStatus();
console.log('Red dot status cleanup completed');
```

#### 2. Cron Job Integration
```javascript
const cron = require('node-cron');
const { checkRedDotStatus } = require('@app/src/services/realtimedb');

// Run cleanup every hour
cron.schedule('0 * * * *', () => {
  console.log('Starting red dot cleanup...');
  checkRedDotStatus();
});
```

#### 3. Manual Cleanup Triggers
```javascript
// Manual execution for testing or immediate cleanup
async function manualRedDotCleanup() {
  try {
    await checkRedDotStatus();
    console.log('Manual cleanup completed successfully');
  } catch (error) {
    console.error('Manual cleanup failed:', error);
  }
}
```

### Integration with Incentive System

#### 1. Incentive Creation Flow
```javascript
// When creating new incentives, set expiration
async function createIncentiveTile(userId, incentiveData) {
  const expirationTime = Math.floor(Date.now() / 1000) + (24 * 60 * 60); // 24 hours
  
  await admin.database().ref(`profile/${userId}/incentive`).update({
    available_tile: true,
    end_date: expirationTime,
    ...incentiveData
  });
}
```

#### 2. Real-time UI Updates
```javascript
// Client-side listener for red dot state changes
database.ref(`profile/${userId}/incentive/available_tile`).on('value', (snapshot) => {
  const hasActiveTile = snapshot.val();
  updateUIRedDot(hasActiveTile);
});
```

#### 3. Monitoring Integration
```javascript
// Enhanced monitoring for cleanup operations
async function monitoredRedDotCleanup() {
  const startTime = Date.now();
  let processedUsers = 0;
  let expiredTiles = 0;
  
  try {
    // Custom implementation with metrics
    admin.initializeApp({
      credential: admin.credential.cert(serviceAccount),
      databaseURL: firebaseConfig.realtimeDBUrl
    });
    
    const timestampInSeconds = Math.floor(Date.now() / 1000);
    const db = admin.database();
    
    const snapshot = await db.ref("profile")
      .orderByChild("incentive/available_tile")
      .equalTo(true)
      .once("value");
    
    if (snapshot.exists()) {
      const updates = {};
      
      snapshot.forEach((childSnapshot) => {
        processedUsers++;
        const userId = childSnapshot.key;
        const userInfo = childSnapshot.child("incentive").val();
        
        if (userInfo.end_date < timestampInSeconds) {
          updates[`profile/${userId}/incentive/available_tile`] = false;
          expiredTiles++;
        }
      });
      
      if (Object.keys(updates).length > 0) {
        await db.ref().update(updates);
      }
    }
    
    await admin.app().delete();
    
    const metrics = {
      duration: Date.now() - startTime,
      processedUsers,
      expiredTiles,
      timestamp: new Date()
    };
    
    logger.info('Red dot cleanup completed:', metrics);
    return metrics;
    
  } catch (error) {
    logger.error('Red dot cleanup failed:', error);
    throw error;
  }
}
```

## Dependencies

### Firebase Dependencies
- **firebase-admin**: Firebase Admin SDK for server-side database operations
- **Google Service Account**: JSON credential file for Firebase authentication
- **Firebase Configuration**: Database URL and project configuration

### Configuration Dependencies
- **config**: Application configuration management for Firebase settings
- **google_credentials.json**: Service account credentials file
- **APP_PATH**: Application path environment variable for credential file location

### Utility Dependencies
- **@maas/core/log**: Centralized logging system for error tracking and monitoring
- **path**: Node.js path utilities for credential file resolution

### Runtime Dependencies
- **Node.js Environment**: Server-side JavaScript runtime
- **Network Connectivity**: Stable connection to Firebase services
- **File System Access**: Read access to credential files

## Code Examples

### Enhanced Red Dot Management System

```javascript
// Comprehensive red dot notification management
class RedDotManager {
  constructor() {
    this.admin = require('firebase-admin');
    this.firebaseConfig = require('config').firebase;
    this.serviceAccount = require(`${APP_PATH}/src/static/google_credentials.json`);
    this.logger = require('@maas/core/log').logger;
  }
  
  async initializeFirebase() {
    if (!this.admin.apps.length) {
      this.admin.initializeApp({
        credential: this.admin.credential.cert(this.serviceAccount),
        databaseURL: this.firebaseConfig.realtimeDBUrl
      });
    }
    return this.admin.database();
  }
  
  async cleanupExpiredTiles() {
    let db;
    const metrics = {
      startTime: Date.now(),
      processedUsers: 0,
      expiredTiles: 0,
      errors: []
    };
    
    try {
      db = await this.initializeFirebase();
      const currentTimestamp = Math.floor(Date.now() / 1000);
      
      const snapshot = await db.ref("profile")
        .orderByChild("incentive/available_tile")
        .equalTo(true)
        .once("value");
      
      if (snapshot.exists()) {
        const batchUpdates = {};
        
        snapshot.forEach((childSnapshot) => {
          try {
            metrics.processedUsers++;
            const userId = childSnapshot.key;
            const incentiveData = childSnapshot.child("incentive").val();
            
            if (incentiveData && incentiveData.end_date < currentTimestamp) {
              batchUpdates[`profile/${userId}/incentive/available_tile`] = false;
              batchUpdates[`profile/${userId}/incentive/expired_at`] = currentTimestamp;
              metrics.expiredTiles++;
              
              this.logger.debug(`Expiring red dot for user ${userId}`);
            }
          } catch (userError) {
            metrics.errors.push(`User processing error: ${userError.message}`);
            this.logger.warn(`Error processing user data:`, userError);
          }
        });
        
        // Batch update for performance
        if (Object.keys(batchUpdates).length > 0) {
          await db.ref().update(batchUpdates);
          this.logger.info(`Batch updated ${Object.keys(batchUpdates).length / 2} expired tiles`);
        }
      }
      
      metrics.duration = Date.now() - metrics.startTime;
      this.logger.info('Red dot cleanup completed:', metrics);
      
      return metrics;
      
    } catch (error) {
      metrics.errors.push(error.message);
      this.logger.error('Red dot cleanup failed:', error);
      throw error;
      
    } finally {
      // Ensure cleanup of Firebase connection
      if (this.admin.apps.length > 0) {
        await this.admin.app().delete();
      }
    }
  }
  
  async setUserRedDot(userId, incentiveData, durationHours = 24) {
    let db;
    
    try {
      db = await this.initializeFirebase();
      const expirationTime = Math.floor(Date.now() / 1000) + (durationHours * 60 * 60);
      
      const updateData = {
        available_tile: true,
        end_date: expirationTime,
        created_at: Math.floor(Date.now() / 1000),
        ...incentiveData
      };
      
      await db.ref(`profile/${userId}/incentive`).update(updateData);
      
      this.logger.info(`Set red dot for user ${userId}, expires in ${durationHours} hours`);
      
      return { success: true, expirationTime };
      
    } catch (error) {
      this.logger.error(`Failed to set red dot for user ${userId}:`, error);
      throw error;
      
    } finally {
      if (this.admin.apps.length > 0) {
        await this.admin.app().delete();
      }
    }
  }
  
  async getUserRedDotStatus(userId) {
    let db;
    
    try {
      db = await this.initializeFirebase();
      
      const snapshot = await db.ref(`profile/${userId}/incentive`).once('value');
      const incentiveData = snapshot.val();
      
      if (!incentiveData) {
        return { hasRedDot: false, status: 'no_incentive_data' };
      }
      
      const currentTime = Math.floor(Date.now() / 1000);
      const isExpired = incentiveData.end_date < currentTime;
      
      return {
        hasRedDot: incentiveData.available_tile && !isExpired,
        isExpired,
        endDate: incentiveData.end_date,
        timeRemaining: Math.max(0, incentiveData.end_date - currentTime),
        status: isExpired ? 'expired' : 'active'
      };
      
    } catch (error) {
      this.logger.error(`Failed to get red dot status for user ${userId}:`, error);
      throw error;
      
    } finally {
      if (this.admin.apps.length > 0) {
        await this.admin.app().delete();
      }
    }
  }
}
```

### Automated Red Dot Scheduler

```javascript
// Advanced scheduling system for red dot management
class RedDotScheduler {
  constructor() {
    this.redDotManager = new RedDotManager();
    this.cron = require('node-cron');
    this.logger = require('@maas/core/log').logger;
    this.isRunning = false;
  }
  
  startScheduler() {
    // Run cleanup every 30 minutes
    this.cron.schedule('*/30 * * * *', async () => {
      if (this.isRunning) {
        this.logger.warn('Previous cleanup still running, skipping this cycle');
        return;
      }
      
      await this.runCleanupCycle();
    });
    
    // Daily health check at 2 AM
    this.cron.schedule('0 2 * * *', async () => {
      await this.runHealthCheck();
    });
    
    this.logger.info('Red dot scheduler started');
  }
  
  async runCleanupCycle() {
    this.isRunning = true;
    
    try {
      const metrics = await this.redDotManager.cleanupExpiredTiles();
      
      // Alert if too many errors or low processing rate
      if (metrics.errors.length > 10) {
        await this.sendAlert('high_error_rate', { errors: metrics.errors.length });
      }
      
      if (metrics.processedUsers === 0 && metrics.duration > 5000) {
        await this.sendAlert('performance_issue', { duration: metrics.duration });
      }
      
      return metrics;
      
    } catch (error) {
      this.logger.error('Cleanup cycle failed:', error);
      await this.sendAlert('cleanup_failure', { error: error.message });
      
    } finally {
      this.isRunning = false;
    }
  }
  
  async runHealthCheck() {
    try {
      const startTime = Date.now();
      
      // Test Firebase connectivity
      await this.redDotManager.initializeFirebase();
      
      // Test read operations
      const testUserId = 'health_check_user';
      await this.redDotManager.getUserRedDotStatus(testUserId);
      
      const responseTime = Date.now() - startTime;
      
      this.logger.info(`Health check passed in ${responseTime}ms`);
      
      if (responseTime > 5000) {
        await this.sendAlert('slow_response', { responseTime });
      }
      
    } catch (error) {
      this.logger.error('Health check failed:', error);
      await this.sendAlert('health_check_failure', { error: error.message });
    }
  }
  
  async sendAlert(alertType, data) {
    // Integration with alerting system
    const alert = {
      service: 'realtimedb',
      type: alertType,
      timestamp: new Date(),
      data
    };
    
    this.logger.warn('Red dot service alert:', alert);
    
    // Could integrate with monitoring services like DataDog, NewRelic, etc.
    // await monitoringService.sendAlert(alert);
  }
}
```

### Firebase Real-time Analytics

```javascript
// Real-time analytics for red dot engagement
class RedDotAnalytics {
  constructor() {
    this.redDotManager = new RedDotManager();
  }
  
  async generateEngagementReport() {
    let db;
    const report = {
      timestamp: new Date(),
      totalUsers: 0,
      activeRedDots: 0,
      expiredRedDots: 0,
      engagementMetrics: {},
      expirationDistribution: {}
    };
    
    try {
      db = await this.redDotManager.initializeFirebase();
      const currentTime = Math.floor(Date.now() / 1000);
      
      // Query all user profiles with incentive data
      const snapshot = await db.ref("profile")
        .orderByChild("incentive")
        .once("value");
      
      if (snapshot.exists()) {
        snapshot.forEach((childSnapshot) => {
          report.totalUsers++;
          const incentiveData = childSnapshot.child("incentive").val();
          
          if (incentiveData) {
            const isActive = incentiveData.available_tile;
            const isExpired = incentiveData.end_date < currentTime;
            
            if (isActive && !isExpired) {
              report.activeRedDots++;
              
              // Calculate time until expiration
              const hoursUntilExpiration = Math.ceil((incentiveData.end_date - currentTime) / 3600);
              const bucket = this.getExpirationBucket(hoursUntilExpiration);
              report.expirationDistribution[bucket] = (report.expirationDistribution[bucket] || 0) + 1;
            }
            
            if (isExpired) {
              report.expiredRedDots++;
            }
          }
        });
      }
      
      // Calculate engagement metrics
      report.engagementMetrics = {
        activationRate: (report.activeRedDots / report.totalUsers) * 100,
        expirationRate: (report.expiredRedDots / (report.activeRedDots + report.expiredRedDots)) * 100,
        retentionScore: Math.max(0, 100 - report.engagementMetrics?.expirationRate || 0)
      };
      
      return report;
      
    } catch (error) {
      this.logger.error('Failed to generate engagement report:', error);
      throw error;
      
    } finally {
      if (this.admin.apps.length > 0) {
        await this.admin.app().delete();
      }
    }
  }
  
  getExpirationBucket(hours) {
    if (hours <= 1) return '0-1h';
    if (hours <= 6) return '1-6h';
    if (hours <= 24) return '6-24h';
    if (hours <= 72) return '1-3d';
    return '3d+';
  }
  
  async trackRedDotInteraction(userId, interactionType) {
    try {
      const timestamp = Math.floor(Date.now() / 1000);
      
      const interactionData = {
        type: interactionType, // 'view', 'click', 'dismiss'
        timestamp,
        userId
      };
      
      // Store interaction for analytics
      await db.ref(`analytics/red_dot_interactions`).push(interactionData);
      
      this.logger.info(`Red dot interaction tracked: ${interactionType} for user ${userId}`);
      
    } catch (error) {
      this.logger.error('Failed to track red dot interaction:', error);
    }
  }
}
```

This real-time database service provides essential functionality for managing user notification states in the ConnectSmart platform, ensuring users receive timely and relevant incentive notifications while automatically cleaning up expired content.