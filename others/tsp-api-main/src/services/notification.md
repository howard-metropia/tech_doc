# TSP API Notification Service Documentation

## 🔍 Quick Summary (TL;DR)
The notification service manages notification lifecycle operations, specifically handling the dismissal and expiration of notifications by updating their end timestamps in the database.

**Keywords:** notification-management | notification-dismissal | notification-expiration | notification-lifecycle | database-updates | notification-hiding

**Primary use cases:** Hiding notifications from user view, setting notification expiration times, batch notification management, notification cleanup operations

**Compatibility:** Node.js >= 16.0.0, MySQL database, Knex.js query builder

## ❓ Common Questions Quick Index
- **Q: What does "hiding" notifications mean?** → Setting an end timestamp to remove from active view
- **Q: Can multiple notifications be hidden at once?** → Yes, supports batch operations
- **Q: How are notification end times set?** → Uses current timestamp or custom provided time
- **Q: Are notifications actually deleted?** → No, they're marked as ended for soft deletion
- **Q: What happens to empty notification arrays?** → Returns 0 without database operations
- **Q: How is the end time formatted?** → ISO string format converted to MySQL datetime

## 📋 Functionality Overview

**Non-technical explanation:** 
Think of this as a **notification manager** that helps control which notifications users see. When a notification needs to be dismissed (like when a user marks it as read or it expires), this service updates the database to "hide" it by marking when it ended, without actually deleting the notification record.

**Technical explanation:** 
A lightweight notification lifecycle management service that provides database operations for marking notifications as ended or expired. Uses Knex.js for MySQL operations to update notification records with end timestamps, supporting both single and batch notification management with automatic timestamp handling.

**Business value explanation:**
Essential for user experience management by controlling notification visibility. Supports clean notification interfaces, prevents notification spam, enables notification analytics through retention of historical data, and provides flexible notification lifecycle management for different business rules.

## 🔧 Technical Specifications

- **File:** `allrepo/connectsmart/tsp-api/src/services/notification.js`
- **Language:** JavaScript (ES2020)
- **Framework:** Knex.js query builder
- **Type:** Database Management Service
- **File Size:** ~0.5 KB
- **Complexity Score:** ⭐ (Low - Simple database update operations)

**Dependencies:**
- `@maas/core/mysql`: MySQL database connection (**Critical**)
- `@maas/core/log`: Logging infrastructure (**High**)

## 📝 Detailed Code Analysis

### hideNotificationApi Function

**Purpose:** Marks notifications as ended by setting their end timestamp

**Parameters:**
- `notificationIds`: Array - List of notification IDs to hide
- `endedOn`: String (optional) - Custom end timestamp, defaults to current time

**Returns:** Number - Count of updated notification records

**Processing Flow:**
1. **Empty Check:** Returns 0 immediately if no notification IDs provided
2. **Timestamp Generation:** Uses current time if no end time specified
3. **Database Update:** Updates notification records with end timestamp
4. **Result Logging:** Logs the update operation details
5. **Count Return:** Returns number of successfully updated records

**Implementation:**
```javascript
async function hideNotificationApi(notificationIds, endedOn = null) {
  if (notificationIds.length === 0) return 0;
  
  if (!endedOn)
    endedOn = new Date().toISOString().replace('T', ' ').split('.')[0];
    
  const count = await knex('notification')
    .whereIn('id', notificationIds)
    .update({ ended_on: endedOn }, ['id']);
    
  logger.debug(
    `Update the notifications: ${notificationIds}, ended_on=${endedOn}`,
  );
  
  return count.length;
}
```

### Timestamp Processing
- **Default Behavior:** Uses current timestamp when none provided
- **Format Conversion:** Converts ISO string to MySQL datetime format
- **Timezone Handling:** Uses server timezone for timestamp generation

## 🚀 Usage Methods

### Basic Notification Hiding
```javascript
const notificationService = require('@app/src/services/notification');

async function dismissNotification(notificationId) {
  try {
    const count = await notificationService.hideNotificationApi([notificationId]);
    
    if (count > 0) {
      console.log(`Successfully dismissed notification ${notificationId}`);
      return true;
    } else {
      console.log(`Notification ${notificationId} not found or already dismissed`);
      return false;
    }
  } catch (error) {
    console.error('Failed to dismiss notification:', error);
    throw error;
  }
}
```

### Batch Notification Management
```javascript
async function dismissMultipleNotifications(notificationIds) {
  const notificationService = require('@app/src/services/notification');
  
  try {
    const count = await notificationService.hideNotificationApi(notificationIds);
    
    console.log(`Successfully dismissed ${count} out of ${notificationIds.length} notifications`);
    
    return {
      requested: notificationIds.length,
      updated: count,
      success: count === notificationIds.length
    };
  } catch (error) {
    console.error('Batch notification dismissal failed:', error);
    throw error;
  }
}

// Usage example
const notificationIds = [123, 456, 789];
dismissMultipleNotifications(notificationIds);
```

### Scheduled Notification Expiration
```javascript
async function expireNotificationAtTime(notificationIds, expirationTime) {
  const notificationService = require('@app/src/services/notification');
  
  try {
    // Format expiration time for database
    const endedOn = expirationTime.toISOString().replace('T', ' ').split('.')[0];
    
    const count = await notificationService.hideNotificationApi(
      notificationIds, 
      endedOn
    );
    
    console.log(`Scheduled ${count} notifications to expire at ${expirationTime}`);
    return count;
  } catch (error) {
    console.error('Failed to schedule notification expiration:', error);
    throw error;
  }
}

// Schedule notifications to expire in 24 hours
const tomorrow = new Date();
tomorrow.setHours(tomorrow.getHours() + 24);
expireNotificationAtTime([123, 456], tomorrow);
```

### Notification Cleanup Service
```javascript
class NotificationCleanupService {
  constructor() {
    this.notificationService = require('@app/src/services/notification');
  }

  async expireOldNotifications(daysOld = 30) {
    try {
      // Find notifications older than specified days
      const cutoffDate = new Date();
      cutoffDate.setDate(cutoffDate.getDate() - daysOld);
      
      const oldNotifications = await knex('notification')
        .where('created_at', '<', cutoffDate)
        .whereNull('ended_on')
        .select('id');
      
      if (oldNotifications.length === 0) {
        console.log('No old notifications found for cleanup');
        return 0;
      }
      
      const notificationIds = oldNotifications.map(n => n.id);
      const count = await this.notificationService.hideNotificationApi(notificationIds);
      
      console.log(`Expired ${count} notifications older than ${daysOld} days`);
      return count;
    } catch (error) {
      console.error('Notification cleanup failed:', error);
      throw error;
    }
  }

  async expireUserNotifications(userId, category = null) {
    try {
      let query = knex('notification')
        .where('user_id', userId)
        .whereNull('ended_on');
      
      if (category) {
        query = query.where('category', category);
      }
      
      const notifications = await query.select('id');
      
      if (notifications.length === 0) {
        console.log(`No active notifications found for user ${userId}`);
        return 0;
      }
      
      const notificationIds = notifications.map(n => n.id);
      const count = await this.notificationService.hideNotificationApi(notificationIds);
      
      console.log(`Dismissed ${count} notifications for user ${userId}`);
      return count;
    } catch (error) {
      console.error(`Failed to dismiss notifications for user ${userId}:`, error);
      throw error;
    }
  }

  async batchProcessNotifications(operations) {
    const results = [];
    
    for (const operation of operations) {
      try {
        const count = await this.notificationService.hideNotificationApi(
          operation.notificationIds,
          operation.endedOn
        );
        
        results.push({
          operation: operation.name || 'unnamed',
          success: true,
          count,
          notificationIds: operation.notificationIds
        });
      } catch (error) {
        results.push({
          operation: operation.name || 'unnamed',
          success: false,
          error: error.message,
          notificationIds: operation.notificationIds
        });
      }
    }
    
    return results;
  }
}
```

### Integration with User Actions
```javascript
async function handleUserNotificationAction(userId, action, notificationIds) {
  const notificationService = require('@app/src/services/notification');
  
  try {
    switch (action) {
      case 'dismiss':
        const dismissCount = await notificationService.hideNotificationApi(notificationIds);
        await logUserAction(userId, 'notification_dismissed', { 
          count: dismissCount, 
          ids: notificationIds 
        });
        return { action: 'dismissed', count: dismissCount };
        
      case 'dismiss_all':
        // Get all active notifications for user
        const activeNotifications = await knex('notification')
          .where('user_id', userId)
          .whereNull('ended_on')
          .select('id');
        
        const allIds = activeNotifications.map(n => n.id);
        const allCount = await notificationService.hideNotificationApi(allIds);
        
        await logUserAction(userId, 'all_notifications_dismissed', { 
          count: allCount 
        });
        return { action: 'dismissed_all', count: allCount };
        
      case 'snooze':
        // Schedule to reappear in 1 hour
        const snoozeTime = new Date();
        snoozeTime.setHours(snoozeTime.getHours() + 1);
        const snoozeEndTime = snoozeTime.toISOString().replace('T', ' ').split('.')[0];
        
        const snoozeCount = await notificationService.hideNotificationApi(
          notificationIds, 
          snoozeEndTime
        );
        
        await logUserAction(userId, 'notification_snoozed', { 
          count: snoozeCount, 
          snoozeUntil: snoozeTime 
        });
        return { action: 'snoozed', count: snoozeCount, until: snoozeTime };
        
      default:
        throw new Error(`Unknown action: ${action}`);
    }
  } catch (error) {
    console.error(`Notification action failed for user ${userId}:`, error);
    throw error;
  }
}
```

## 📊 Output Examples

### Successful Single Dismissal
```javascript
// Input: hideNotificationApi([123])
// Output: 1
{
  success: true,
  dismissedCount: 1,
  notificationId: 123
}
```

### Successful Batch Operation
```javascript
// Input: hideNotificationApi([123, 456, 789])
// Output: 3
{
  requested: 3,
  updated: 3,
  success: true,
  notificationIds: [123, 456, 789]
}
```

### Partial Batch Success
```javascript
// Some notifications don't exist
{
  requested: 5,
  updated: 3,
  success: false,
  message: "Some notifications were not found or already dismissed"
}
```

### Empty Array Input
```javascript
// Input: hideNotificationApi([])
// Output: 0
{
  requested: 0,
  updated: 0,
  message: "No notifications to process"
}
```

### Cleanup Operation Results
```javascript
{
  operation: "expire_old_notifications",
  success: true,
  count: 45,
  criteria: "older than 30 days",
  processedAt: "2024-06-25T14:30:00Z"
}
```

## ⚠️ Important Notes

### Database Operations
- **Soft Deletion:** Notifications are not deleted, only marked as ended
- **Batch Updates:** Efficiently handles multiple notifications in single query
- **Transaction Safety:** Updates are atomic within single operation
- **Index Usage:** Queries use notification ID indexes for performance

### Timestamp Handling
- **Automatic Generation:** Current timestamp used when not provided
- **Format Conversion:** ISO strings converted to MySQL datetime format
- **Timezone Considerations:** Uses server timezone for timestamp generation
- **Precision:** Removes milliseconds for database compatibility

### Performance Considerations
- **Batch Operations:** More efficient than individual updates
- **Empty Array Handling:** Avoids unnecessary database queries
- **Logging Overhead:** Debug logging for troubleshooting
- **Return Value Processing:** Counts returned records for verification

### Error Scenarios
- **Database Connectivity:** Handle MySQL connection issues
- **Invalid IDs:** Non-existent notification IDs are silently ignored
- **Timestamp Errors:** Invalid date formats may cause SQL errors
- **Constraint Violations:** Rare but possible with foreign key constraints

### Integration Patterns
- **User Interface:** Support for notification dismissal buttons
- **Cleanup Jobs:** Scheduled maintenance for old notifications
- **Business Rules:** Custom expiration logic for different notification types
- **Analytics:** Track notification engagement and dismissal patterns

### Security Considerations
- **User Authorization:** Verify user can dismiss specific notifications
- **Input Validation:** Validate notification ID formats and ranges
- **Audit Logging:** Consider logging notification management actions
- **Rate Limiting:** Prevent abuse of batch operations

## 🔗 Related File Links

- **Notification Models:** Database models for notification entities
- **User Interface:** Controllers handling notification management endpoints
- **Cleanup Services:** Scheduled jobs for notification maintenance

---
*This service provides essential notification lifecycle management for clean user experience and effective notification systems.*