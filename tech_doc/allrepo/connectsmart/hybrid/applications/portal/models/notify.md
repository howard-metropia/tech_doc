# Portal Notification System - MaaS Push Messaging

## 🔍 Quick Summary (TL;DR)
Comprehensive notification management system for Portal MaaS platform providing templated push notifications, multi-language support, and SQS-based message delivery for carpooling, payments, and transportation services.

**Keywords**: `push-notifications | template-notifications | multi-language | sqs-messaging | carpooling-notifications | payment-notifications | maas-messaging | notification-templates`

**Use Cases**: Carpooling status updates, payment confirmations, trip notifications, group messaging, wallet alerts, validation results

**Compatibility**: Python 2.7+, Web2py framework, SQS messaging, multi-language support (EN/ZH/ES/VI)

## ❓ Common Questions Quick Index
- Q: How do I send a notification? → [Usage Methods](#usage-methods)
- Q: What notification types are available? → [Notification Templates](#notification-templates)
- Q: How does multi-language support work? → [Multi-Language System](#multi-language-system)
- Q: How do I hide/expire notifications? → [Notification Management](#notification-management)
- Q: What carpooling notifications exist? → [Carpooling Notifications](#carpooling-notifications)
- Q: How are payment notifications sent? → [Payment Notifications](#payment-notifications)
- Q: Can I customize notification content? → [Template Customization](#template-customization)
- Q: How do I handle notification failures? → [Error Handling](#error-handling)

## 📋 Functionality Overview
**Non-technical**: Like a smart messaging system for a transportation app - automatically sends you personalized messages in your preferred language about ride requests, payment confirmations, driver arrivals, and wallet updates, ensuring you never miss important transportation-related information.

**Technical**: Template-based notification system with multi-language support (EN/ZH-TW/ES/VI) providing 30+ predefined notification types for carpooling coordination, payment processing, and MaaS services, integrated with SQS messaging for reliable delivery and database tracking.

**Business Value**: Enhances user engagement through timely notifications, improves carpooling coordination efficiency, reduces customer support load through proactive messaging, and supports global markets with localized content.

**System Context**: Central messaging hub for ConnectSmart Portal, coordinating with notification delivery systems, user preference management, and external messaging services to provide comprehensive push notification functionality.

## 🔧 Technical Specifications
- **File**: `portal/models/notify.py` (168 lines)
- **Dependencies**: Web2py T() translation, datetime utilities, notification module
- **Languages**: English, Traditional Chinese, Spanish, Vietnamese
- **Notification Types**: 30+ predefined templates for MaaS services
- **Delivery**: SQS-based asynchronous message processing
- **Expiration**: Configurable notification lifecycle management

## 📝 Detailed Code Analysis

### Core Notification Functions

**Template Notification System**:
```python
def push_template_notification(notification_type, user_ids, msg_data=None, 
                             expiration=None, silent=False, no_push=False, 
                             image=None, **kwargs):
    """
    Send templated notifications with multi-language support
    - notification_type: Predefined notification constant
    - user_ids: List of target user IDs
    - msg_data: Template data for variable substitution
    - expiration: Notification lifecycle (default 30 days)
    - silent: Send without push notification sound
    - no_push: Queue only, don't send immediately
    """
```

**Notification Hiding/Management**:
```python
def hide_notification_api(db, notification_ids, ended_on=None):
    """
    Hide or expire notifications by setting ended_on timestamp
    Returns count of updated notifications
    """
```

### Notification Template System

**Carpooling Notifications**:
```python
template_key = {
    notif.DUO_GROUP_JOIN_REQUEST: (
        'Request to Join', 
        '%(first_name)s requests to join %(group_name)s carpooling group.'
    ),
    notif.DUO_OFFER_JOIN_ACCEPTED: (
        'Invitation is Accepted', 
        'Awesome! %(first_name)s has accepted your carpooling request.'
    ),
    notif.DUO_DRIVER_ARRIVE_SOON: (
        'Your Driver is Approaching',
        '%(first_name)s should arrive in 5 minutes in a %(vehicle_color)s %(vehicle_type)s.'
    )
}
```

**Payment Notifications**:
```python
notif.WALLET_AUTO_REFILL_SUCCESS: (
    'Auto refill completed!',
    '$%(amount)s Coins have been deposited in your Wallet.'
),
notif.DUO_CARPOOL_DRIVER_FEE_RECEIVED: (
    'Carpooling Chip-In',
    'You\'ve received %(chip_in)s Coins from your carpool passenger.'
)
```

### Multi-Language Processing
```python
# Generate messages in all supported languages
msg_title = dict(
    en=T(title_lang_key, kwargs, lazy=False, language='en'),
    zh_tw=T(title_lang_key, kwargs, lazy=False, language='zh-tw'),
    es=T(title_lang_key, kwargs, lazy=False, language='es'),
    vi=T(title_lang_key, kwargs, lazy=False, language='vi')
)
```

## 🚀 Usage Methods

### Basic Template Notification
```python
from applications.portal.models.notify import push_template_notification
import notification as notif

# Send carpooling request notification
notification_id = push_template_notification(
    notif.DUO_GROUP_JOIN_REQUEST,
    user_ids=[123, 456],
    first_name="John",
    group_name="Morning Commute"
)
```

### Payment Notification with Amount
```python
# Auto-refill success notification
push_template_notification(
    notif.WALLET_AUTO_REFILL_SUCCESS,
    user_ids=[user_id],
    amount=10.0
)

# Carpooling payment received
push_template_notification(
    notif.DUO_CARPOOL_DRIVER_FEE_RECEIVED,
    user_ids=[driver_id],
    chip_in=5.0
)
```

### Driver Arrival Notifications
```python
# Driver approaching notification
push_template_notification(
    notif.DUO_DRIVER_ARRIVE_SOON,
    user_ids=[passenger_id],
    first_name="Sarah",
    vehicle_color="blue",
    vehicle_type="Honda Civic",
    vehicle_plate="ABC123"
)
```

### Custom Notification with Expiration
```python
from datetime import datetime, timedelta

# Send notification with 7-day expiration
expiration = datetime.utcnow() + timedelta(days=7)
push_template_notification(
    notif.DUO_CARPOOL_MATCHING,
    user_ids=[user_id],
    expiration=expiration,
    silent=True  # No notification sound
)
```

### Hide Notifications
```python
from applications.portal.models.notify import hide_notification_api

# Hide specific notifications
notification_ids = [101, 102, 103]
count = hide_notification_api(db, notification_ids)
print(f"Hidden {count} notifications")
```

## 📊 Output Examples

**Successful Notification Send**:
```python
notification_id = push_template_notification(
    notif.DUO_GROUP_JOIN_REQUEST,
    user_ids=[123],
    first_name="John",
    group_name="Evening Commute"
)
# Returns: 15847 (notification ID)
```

**Multi-Language Message Generation**:
```json
{
    "title": {
        "en": "Request to Join",
        "zh_tw": "申請加入",
        "es": "Solicitud de Unirse",
        "vi": "Yêu cầu Tham gia"
    },
    "body": {
        "en": "John requests to join Evening Commute carpooling group.",
        "zh_tw": "John 申請加入 Evening Commute 共乘群組。",
        "es": "John solicita unirse al grupo de viaje compartido Evening Commute.",
        "vi": "John yêu cầu tham gia nhóm đi chung xe Evening Commute."
    }
}
```

**Hide Notification Result**:
```python
count = hide_notification_api(db, [101, 102, 103])
# Returns: 3 (number of notifications updated)
```

**Driver Arrival Notification**:
```
Title: "Your Driver is Approaching"
Body: "Sarah should arrive in 5 minutes in a blue Honda Civic. (License #ABC123)"
```

## ⚠️ Important Notes

### Notification Template Management
- **Template Consistency**: All templates must include placeholders for required data
- **Language Support**: Templates must be defined for all supported languages
- **Variable Validation**: Ensure all template variables are provided in kwargs
- **Special Characters**: Handle special characters properly in multi-language content

### Performance Considerations
- **Bulk Sending**: Use user_ids list for sending to multiple users efficiently
- **Queue Management**: Use no_push=True for batch processing scenarios
- **Expiration Management**: Set appropriate expiration times to avoid notification buildup
- **Database Load**: Hide notifications efficiently to prevent database bloat

### Localization Best Practices
- **Cultural Context**: Ensure translations are culturally appropriate
- **Text Length**: Consider varying text lengths across languages for UI design
- **Time Zones**: Handle time-sensitive notifications with proper timezone conversion
- **Character Encoding**: Ensure proper UTF-8 support for all languages

## 🔗 Related File Links
- **Notification Constants**: `/notification.py` (notification type definitions)
- **Database Schema**: `/portal/models/db.py` (notification tables)
- **Business Logic**: `/portal/models/common.py` (payment notification triggers)
- **Translation Files**: `/languages/` (multilingual message templates)
- **Datetime Utilities**: `/datetime_utils.py` (timestamp formatting)
- **SQS Integration**: `/sqs_helper.py` (message queue processing)

## 📈 Use Cases
- **Carpooling Coordination**: Real-time updates for ride requests, matches, and status changes
- **Payment Processing**: Transaction confirmations, auto-refill notifications, balance alerts
- **Trip Management**: Driver arrival alerts, trip completion confirmations
- **User Engagement**: Promotional messages, feature announcements, service updates
- **System Alerts**: Account security notifications, policy updates, service maintenance
- **Customer Support**: Automated responses, issue resolution updates
- **Marketing Campaigns**: Targeted promotional notifications with personalized content

## 🛠️ Improvement Suggestions
- **Rich Notifications**: Add support for images, buttons, and deep linking
- **Personalization**: Implement user preference-based notification customization
- **A/B Testing**: Add support for notification template experimentation
- **Analytics**: Implement notification delivery and engagement tracking
- **Performance Optimization**: Add notification batching and rate limiting
- **Template Management**: Create admin interface for notification template management
- **Push Notification Channels**: Support multiple delivery channels (FCM, APNS, SMS, email)

## 🏷️ Document Tags
**Keywords**: push-notifications, template-notifications, multi-language, carpooling-notifications, payment-notifications, sqs-messaging, notification-management, maas-messaging

**Technical Tags**: `#notifications #push-messaging #templates #multi-language #sqs #carpooling #payments #messaging`

**Target Roles**: Mobile developers (intermediate), Backend developers (intermediate), Product managers (beginner), UX designers (beginner)

**Difficulty**: ⭐⭐ (Moderate) - Template system with multi-language support

**Maintenance**: Medium - Regular template updates and language additions

**Business Criticality**: High - Essential for user engagement and service coordination

**Related Topics**: Push notifications, Multi-language support, Template systems, Message queuing, User engagement