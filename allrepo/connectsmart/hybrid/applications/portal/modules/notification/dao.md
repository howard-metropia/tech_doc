# Notification Database Tables - Hierarchical Notification System

## 🔍 Quick Summary (TL;DR)
**Comprehensive database table definitions for hierarchical notification system supporting multi-language messages, user targeting, and delivery status tracking in the MaaS platform.** Implements four interconnected tables with cascade operations for efficient notification management and push delivery tracking.

**Core functionality:** Notification schema | Multi-language messages | User targeting | Status tracking | Cascade operations | Hierarchical structure
**Primary use cases:** Push notification storage, message localization, delivery tracking, user targeting, notification analytics, status management
**Compatibility:** PyDAL ORM, Web2py framework, MySQL/PostgreSQL databases, mobile push services

## ❓ Common Questions Quick Index
- **Q: What tables make up the notification system?** → See [Technical Specifications](#technical-specifications)
- **Q: How does cascade insertion work?** → See [Detailed Code Analysis](#detailed-code-analysis)
- **Q: What notification statuses are supported?** → See [Output Examples](#output-examples)
- **Q: How is multi-language support implemented?** → See [Technical Specifications](#technical-specifications)
- **Q: What validation rules apply?** → See [Important Notes](#important-notes)
- **Q: How to handle bulk notifications?** → See [Usage Methods](#usage-methods)
- **Q: What's the table relationship hierarchy?** → See [Functionality Overview](#functionality-overview)
- **Q: How does status tracking work?** → See [Use Cases](#use-cases)

## 📋 Functionality Overview
**Non-technical explanation:** Think of this as a multi-level filing system for a messaging center. Like how a postal service has different departments - one for mail types (letters, packages), one for individual mailings, one for different language versions, and one tracking who received what - this system organizes notifications the same way. Each level handles a specific aspect while working together seamlessly.

**Technical explanation:** Hierarchical database schema implementing four-tier notification architecture with type classification, message management, multi-language content, and per-user delivery tracking. Features cascade operations for atomic notification creation and status management.

**Business value:** Enables scalable notification management supporting millions of users with multi-language content, provides comprehensive delivery analytics for engagement optimization, and ensures reliable message delivery with full audit trails.

**System context:** Core data layer for notification infrastructure supporting push notification services, user engagement systems, and business intelligence within the MaaS platform ecosystem.

## 🔧 Technical Specifications
- **File:** `applications/portal/modules/notification/dao.py`
- **Language:** Python 2.7+
- **Framework:** Web2py with PyDAL ORM
- **Type:** Database table definitions with cascade operations
- **Size:** ~106 lines
- **Complexity:** ⭐⭐⭐ (Medium - complex relationships and cascade operations)

**Table Hierarchy (4 tables):**
1. **NotificationTypeTable** - Notification categories and types
2. **NotificationTable** - Individual notification instances with metadata
3. **NotificationMessageTable** - Language-specific message content
4. **NotificationUserTable** - Per-user delivery tracking and status

**Key Dependencies:**
- `define` module (Required) - Notification status constants
- `pydal.objects` (Required) - PyDAL Table and Field classes
- `gluon.validators` (Required) - IS_IN_SET validator for status validation

**Relationship Structure:**
```
NotificationTypeTable (1) ←→ (N) NotificationTable
NotificationTable (1) ←→ (N) NotificationMessageTable
NotificationMessageTable (1) ←→ (N) NotificationUserTable
```

**Cascade Operations:**
- `NotificationTable.cascade_insert()` - Creates notification with messages
- `NotificationMessageTable.cascade_insert()` - Creates messages with user targeting
- `NotificationUserTable.cascade_insert()` - Bulk user record creation

## 📝 Detailed Code Analysis
**NotificationTypeTable Structure:**
```python
class NotificationTypeTable(Table):
    def __init__(self, db, tablename, *fields, **args):
        def_fields = (
            Field('name', 'string', required=True, notnull=True),
        )
        # Simple table for notification type definitions
```

**NotificationTable with Cascade Logic:**
```python
class NotificationTable(Table):
    # Core notification fields
    Field('notification_type', db.notification_type, required=True, notnull=True)
    Field('msg_data', 'text')                    # JSON metadata storage
    Field('started_on', 'datetime', required=True, notnull=True)
    Field('ended_on', 'datetime')                # Expiration time
    Field('silent', 'boolean', default=False)   # Silent notification flag
    
    def cascade_insert(self, messages, **fields):
        """Atomic notification creation with messages"""
        _id = self.insert(**fields)              # Create notification record
        fields['id'] = _id
        
        # Prepare message records
        for message in messages:
            message['notification_id'] = fields['id']
        
        # Cascade to message creation
        self._db.notification_msg.cascade_insert(messages)
        return _id
```

**NotificationMessageTable with Language Support:**
```python
class NotificationMessageTable(Table):
    Field('notification_id', db.notification, required=True, notnull=True)
    Field('msg_title', 'string')               # Localized title
    Field('msg_body', 'text')                  # Localized content
    Field('lang', 'string', default="en")     # Language code
    
    def cascade_insert(self, messages):
        """Bulk message creation with user targeting"""
        _ids = self.bulk_insert(messages)      # Create all messages
        
        users = []
        for idx, obj in enumerate(messages):
            obj['id'] = _ids[idx]              # Assign generated IDs
            for user in (obj.get('users') or []):
                user['notification_msg_id'] = obj['id']
                users.append(user)
        
        # Cascade to user record creation
        self._db.notification_user.cascade_insert(users)
        return _ids
```

**NotificationUserTable with Status Validation:**
```python
class NotificationUserTable(Table):
    Field('notification_msg_id', db.notification_msg, required=True, notnull=True)
    Field('user_id', 'integer', required=True, notnull=True)
    Field('send_status', 'integer', default=define.NOTIFY_STATUS_QUEUE)
    
    # Status validation constraint
    self['send_status'].requires = IS_IN_SET([
        define.NOTIFY_STATUS_QUEUE,      # 0 - Queued for delivery
        define.NOTIFY_STATUS_SEND_FAIL,  # 1 - Delivery failed
        define.NOTIFY_STATUS_SENT,       # 2 - Successfully sent
        define.NOTIFY_STATUS_RECEIVED,   # 3 - Received by device
        define.NOTIFY_STATUS_REPLIED     # 4 - User responded
    ], error_message="Status must be 0~4")
```

**Performance Characteristics:**
- **Cascade Operations**: O(n) where n = number of users per notification
- **Bulk Inserts**: Optimized for high-volume user targeting
- **Memory Usage**: Linear with message count and user count
- **Transaction Safety**: Relies on database transaction management

## 🚀 Usage Methods
**Basic Notification Creation:**
```python
from pydal import DAL
from applications.portal.modules.notification.dao import *

# Setup database with notification tables
db = DAL('mysql://user:pass@localhost/notification_db')
db.define_table('notification_type', NotificationTypeTable(db, 'notification_type'))
db.define_table('notification', NotificationTable(db, 'notification'))
db.define_table('notification_msg', NotificationMessageTable(db, 'notification_msg'))
db.define_table('notification_user', NotificationUserTable(db, 'notification_user'))

# Create notification with cascade
messages = [{
    'lang': 'en',
    'msg_title': 'Carpool Invitation',
    'msg_body': 'You have a new carpool match!',
    'users': [
        {'user_id': 12345, 'token': 'fcm_token_123', 'token_type': 'fcm'},
        {'user_id': 12346, 'token': 'apns_token_456', 'token_type': 'apns'}
    ]
}]

notification_id = db.notification.cascade_insert(
    notification_type=60,  # DUO_CARPOOL_INVITE
    msg_data='{"offer_id": 789}',
    started_on=datetime.utcnow(),
    ended_on=datetime.utcnow() + timedelta(hours=24),
    silent=False,
    messages=messages
)
```

**Multi-language Notification:**
```python
# Create notification with multiple language versions
multilang_messages = [
    {
        'lang': 'en',
        'msg_title': 'System Update',
        'msg_body': 'New features available!',
        'users': [{'user_id': 12345}, {'user_id': 12346}]
    },
    {
        'lang': 'zh_tw',
        'msg_title': '系統更新',
        'msg_body': '新功能已推出！',
        'users': [{'user_id': 12347}, {'user_id': 12348}]
    }
]

notification_id = db.notification.cascade_insert(
    notification_type=1,  # GENERAL
    msg_data='{"version": "2.1.0"}',
    started_on=datetime.utcnow(),
    messages=multilang_messages
)
```

**Status Tracking and Updates:**
```python
# Update notification status when delivered
db(db.notification_user.user_id == 12345).update(
    send_status=define.NOTIFY_STATUS_SENT
)

# Query delivery statistics
stats = db(
    db.notification_user.notification_msg_id.belongs([101, 102])
).select(
    db.notification_user.send_status,
    db.notification_user.send_status.count(),
    groupby=db.notification_user.send_status
)

for stat in stats:
    print(f"Status {stat.notification_user.send_status}: {stat._extra['COUNT(notification_user.send_status)']}")
```

## 📊 Output Examples
**NotificationType Records:**
```python
# Sample notification types
notification_types = [
    {'id': 1, 'name': 'General'},
    {'id': 60, 'name': 'Carpool Invite'},
    {'id': 61, 'name': 'Carpool Matching'},
    {'id': 12, 'name': 'Suggestion Info'}
]
```

**Notification Instance:**
```python
# Main notification record
notification = {
    'id': 12345,
    'notification_type': 60,
    'msg_data': '{"offer_id": 789, "route": "Downtown"}',
    'started_on': datetime(2024, 1, 15, 10, 30, 0),
    'ended_on': datetime(2024, 1, 16, 10, 30, 0),
    'silent': False
}
```

**Multi-language Messages:**
```python
# Message content in different languages
messages = [
    {
        'id': 101,
        'notification_id': 12345,
        'msg_title': 'Carpool Invitation',
        'msg_body': 'You have a new carpool match available!',
        'lang': 'en'
    },
    {
        'id': 102,
        'notification_id': 12345,
        'msg_title': '拼車邀請',
        'msg_body': '您有新的拼車配對可用！',
        'lang': 'zh_tw'
    }
]
```

**User Delivery Tracking:**
```python
# Per-user delivery status records
user_notifications = [
    {
        'id': 1001,
        'notification_msg_id': 101,
        'user_id': 12345,
        'send_status': 2  # NOTIFY_STATUS_SENT
    },
    {
        'id': 1002,
        'notification_msg_id': 102,
        'user_id': 12346,
        'send_status': 3  # NOTIFY_STATUS_RECEIVED
    }
]
```

**Cascade Operation Result:**
```python
# Result of cascade_insert operation
>>> notification_id = db.notification.cascade_insert(messages=messages, ...)
>>> print(f"Created notification: {notification_id}")
>>> print(f"Messages created: {len(messages)}")
>>> print(f"Users targeted: {sum(len(msg.get('users', [])) for msg in messages)}")

Created notification: 12345
Messages created: 2
Users targeted: 4
```

## ⚠️ Important Notes
**Data Consistency Considerations:**
- **Transaction Safety**: Cascade operations should run within database transactions
- **Foreign Key Integrity**: Ensure proper foreign key constraints for referential integrity
- **Bulk Operation Limits**: Large user lists may hit database insertion limits
- **Rollback Complexity**: Failed cascade operations may leave partial data

**Performance Implications:**
- **Memory Usage**: Large user lists consume significant memory during cascade operations
- **Database Load**: Bulk inserts can impact database performance under high load
- **Index Requirements**: Need indexes on user_id, notification_id, and send_status for query performance
- **Connection Pooling**: High-volume notifications may exhaust database connections

**Status Management:**
- **Status Transitions**: No validation of valid status transition sequences
- **Concurrent Updates**: Race conditions possible with simultaneous status updates
- **Status Consistency**: No verification that external delivery matches database status
- **Audit Requirements**: Limited audit trail for status changes

**Language and Localization:**
- **Language Code Standards**: Uses underscore format (en_us) - ensure consistency
- **Content Validation**: No validation that required languages are provided
- **Fallback Strategy**: No automatic fallback when user's language unavailable
- **Character Encoding**: Ensure UTF-8 support for international characters

## 🔗 Related File Links
**Core Dependencies:**
- `define.py` - Notification type and status constants
- `notification_handler.py` - Business logic using these table definitions
- `__init__.py` - Module initialization exporting table classes

**Integration Points:**
- `../../models/db.py` - Database connection and schema configuration
- `../../../controllers/messenger.py` - API endpoints for notification management
- External push notification services (FCM, APNS) configuration

**Business Logic:**
- Carpool notification workflows using notification system
- User engagement campaigns and marketing notifications
- System alert and maintenance notifications

**Analytics and Reporting:**
- Notification delivery analytics and reporting systems
- User engagement metrics based on notification data
- A/B testing frameworks using notification targeting

## 📈 Use Cases
**High-Volume Notification Delivery:**
- Send system-wide announcements to all users
- Deliver targeted marketing campaigns to user segments
- Process emergency alerts and service disruptions
- Handle time-sensitive carpool matching notifications

**Multi-language Content Management:**
- Support international user base with localized content
- Manage translation workflows for notification content
- Handle cultural adaptations for different markets
- Support dynamic content localization based on user preferences

**Delivery Tracking and Analytics:**
- Monitor notification delivery success rates
- Track user engagement with different notification types
- Analyze optimal timing for notification delivery
- Support A/B testing for notification content and strategies

**User Targeting and Segmentation:**
- Target users based on location, behavior, or preferences
- Support personalized notification content
- Handle user opt-out and preference management
- Enable fine-grained user targeting for marketing campaigns

## 🛠️ Improvement Suggestions
**Performance Optimizations:**
- Implement database partitioning for notification_user table by date
- Add connection pooling and batch processing for high-volume operations
- Create database indexes on frequently queried columns
- Consider read replicas for analytics and reporting queries

**Data Integrity Enhancements:**
- Add proper foreign key constraints at database level
- Implement status transition validation logic
- Add audit logging for all notification operations
- Include data retention policies with automatic cleanup

**Feature Enhancements:**
- Add support for rich notifications with images and actions
- Implement notification scheduling and delayed delivery
- Add notification grouping and threading capabilities
- Include template management for reusable notification content

**Monitoring and Operations:**
- Add health checks for notification system components
- Implement metrics collection for delivery rates and performance
- Add alerting for notification failures or degraded performance
- Create monitoring dashboard for notification system health

**Security and Privacy:**
- Implement access controls for notification creation and management
- Add data encryption for sensitive notification content
- Include user consent management for notification preferences
- Add audit trails for compliance and security monitoring

**Code Quality:**
- Add comprehensive unit tests for cascade operations
- Implement proper error handling with detailed error messages
- Add type hints and documentation for better maintainability
- Create migration scripts for schema updates and data migration

## 🏷️ Document Tags
**Keywords:** notification-database, cascade-operations, multi-language, status-tracking, user-targeting, push-notifications, hierarchical-schema, PyDAL, delivery-tracking, localization

**Technical Tags:** `#python` `#pydal` `#database` `#notifications` `#multi-language` `#cascade-operations` `#status-tracking` `#user-targeting` `#schema-design`

**Target Roles:** Database developers (intermediate), Backend developers (intermediate), Mobile developers (intermediate)
**Difficulty Level:** ⭐⭐⭐ (Medium complexity with cascade operations and relationships)
**Maintenance Level:** Medium (requires careful schema evolution and performance monitoring)
**Business Criticality:** High (core infrastructure for user engagement and communications)
**Related Topics:** Database design, notification systems, multi-language support, user engagement, mobile development