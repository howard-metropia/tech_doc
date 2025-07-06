# Notification Handler - Multi-language Push Notification System

## 🔍 Quick Summary (TL;DR)
**Comprehensive notification handler implementing multi-language push notification delivery with FCM/APNS integration, user targeting, language fallback, and delivery status tracking for the MaaS platform.** Supports complex notification types including carpool invitations, suggestions, microsurveys, and system alerts with sophisticated content localization.

**Core functionality:** Push notification delivery | Multi-language support | User targeting | Status tracking | SQS integration | Content localization | Device token management
**Primary use cases:** Carpool notifications, system alerts, user engagement, microsurveys, suggestion delivery, marketing campaigns, operational communications
**Compatibility:** Python 2.7+, FCM, APNS, AWS SQS, MongoDB, multi-timezone support

## ❓ Common Questions Quick Index
- **Q: How does multi-language notification work?** → See [Detailed Code Analysis](#detailed-code-analysis)
- **Q: What push services are supported?** → See [Technical Specifications](#technical-specifications)
- **Q: How to send carpool invitations?** → See [Usage Methods](#usage-methods)
- **Q: What happens if user's language isn't available?** → See [Important Notes](#important-notes)
- **Q: How does status tracking work?** → See [Output Examples](#output-examples)
- **Q: What's the SQS integration for?** → See [Functionality Overview](#functionality-overview)
- **Q: How to handle notification expiration?** → See [Use Cases](#use-cases)
- **Q: What are the performance implications?** → See [Improvement Suggestions](#improvement-suggestions)

## 📋 Functionality Overview
**Non-technical explanation:** Think of this as an advanced "message delivery service" for a transportation app. Like how a sophisticated postal service sorts mail by language, destination, and delivery method, this system takes a notification request, figures out what language each user speaks, gets their device information, formats the message appropriately, and delivers it through the right channel (Android or iPhone). It even tracks whether the message was delivered successfully.

**Technical explanation:** Multi-layered notification delivery system implementing language-aware content distribution, device-specific push notification routing, and comprehensive delivery tracking. Integrates with external push services (FCM/APNS) via SQS queuing for reliable delivery at scale.

**Business value:** Enables global user engagement through localized communications, ensures reliable delivery of critical carpool and system notifications, provides comprehensive analytics for notification effectiveness, and supports scalable push notification operations for millions of users.

**System context:** Core communication infrastructure bridging business logic, user preferences, device management, and external push notification services within the MaaS platform ecosystem.

## 🔧 Technical Specifications
- **File:** `applications/portal/modules/notification/notification_handler.py`
- **Language:** Python 2.7+
- **Framework:** Web2py with external service integration
- **Type:** Business logic handler with external API integration
- **Size:** ~319 lines
- **Complexity:** ⭐⭐⭐⭐ (High - complex multi-language and external service integration)

**Key Functions:**
1. **send_notification()** - Core notification delivery with SQS integration
2. **send_notification_api()** - High-level API with language processing
3. **update_to_replied()** - Status update for user responses

**Dependencies:**
- `json` (Standard) - Message data serialization
- `logging` (Standard) - Debug and error logging  
- `datetime` (Standard) - Timestamp management
- `sqs_helper` (Internal) - AWS SQS integration
- `utils` (Internal) - CDN URL utilities
- `datetime_utils` (Internal) - Date formatting utilities
- `trip_reservation.carpool_handler` (Internal) - Carpool data integration

**External Service Integration:**
- **FCM (Firebase Cloud Messaging)** - Android push notifications
- **APNS (Apple Push Notification Service)** - iOS push notifications
- **AWS SQS** - Message queuing for reliable delivery
- **CDN Services** - Media content delivery for rich notifications

**Supported Device Types:**
- Android devices via FCM tokens
- iOS devices via APNS tokens
- Automatic token type detection and routing

## 📝 Detailed Code Analysis
**Core Notification Function:**
```python
def send_notification(db, notification_type, data, messages, expire_time=None, 
                     silent=False, queue=False, to_production=None, image=None):
    # Data preparation
    msg_data = json.dumps(data)  # Serialize metadata
    now = datetime.datetime.utcnow()
    
    # Process message content
    all_users = list()
    for message in messages:
        all_users.extend(message['users'])
        title = message.pop('title')
        body = message.pop('body')
        
        # Handle silent notifications
        if silent:
            message['msg_title'] = ''
            message['msg_body'] = ''
        else:
            message['msg_title'] = title
            message['msg_body'] = body
    
    # Database cascade insertion
    notification_id = db.notification.cascade_insert(
        notification_type=notification_type,
        msg_data=msg_data,
        messages=messages,
        started_on=now,
        ended_on=expire_time,
        silent=silent
    )
```

**Multi-language Processing Algorithm:**
```python
def send_notification_api(db, notification_type, user_ids, language_title, 
                         language_body, extra_data, expiration, silent=False):
    # Fetch user device and language information
    user_rows = db(db.auth_user.id.belongs(user_ids)).select(
        db.auth_user.id, db.auth_user.device_token, 
        db.auth_user.device_language, db.auth_user.apns_device_token
    )
    
    # Process users and determine device type
    temp = []
    for user in user_rows:
        user_data = {'user_id': user.id, 'lang': user.device_language}
        
        # Normalize language code
        if user.device_language:
            user_data['lang'] = user.device_language.lower().replace('-', '_')
        
        # Determine device type and token
        if user.apns_device_token:
            user_data['token'] = user.apns_device_token
            user_data['token_type'] = 'apns'
        else:
            user_data['token'] = user.device_token
            user_data['token_type'] = 'fcm'
```

**Language Fallback Logic:**
```python
# Intelligent language fallback system
for t_user in temp:
    lang = t_user.pop('lang')
    if silent or not lang:
        lang = 'en'  # Default to English
    
    # Try exact language match
    if lang in language_body:
        text_info = language_body[lang]
    # Try base language (e.g., 'zh' from 'zh_tw')
    elif lang.split('_')[0] in language_body:
        text_info = language_body[lang.split('_')[0]]
    # Fallback to English
    else:
        text_info = language_body['en']
```

**Special Content Processing:**
```python
# Carpool suggestion with user profile data
if notification_type == define.SUGGESTION_CARPOOL:
    from trip_reservation import carpool_handler
    
    offer_id = extra_data['action']['offer_id']
    role = extra_data['action']['role']
    offer_info = carpool_handler.get_suggestion_carpool(db, offer_id)
    
    # Get partner user profile
    profile_others = db(db.auth_user.id == offer_info_others['user_id']).select(
        db.auth_user.first_name, db.auth_user.last_name,
        db.auth_user.rating, db.auth_user.avatar,
        db.auth_user.vehicle_type, db.auth_user.vehicle_color
    ).first()
    
    # Build suggested user information
    suggested_user = {
        'role': role_others,
        'name': {'first_name': profile_others.first_name, 'last_name': profile_others.last_name},
        'avatar': cdn_url(profile_others.avatar),
        'rating': profile_others.rating,
        'vehicle': {'type': profile_others.vehicle_type, 'color': profile_others.vehicle_color}
    }
```

**SQS Integration and Status Updates:**
```python
# Push notification via SQS
raw_data = {
    "silent": silent,
    "user_list": user_ids,
    "notification_type": notification_type,
    "ended_on": expire_time.strftime("%Y-%m-%d %H:%M:%S"),
    "title": title,
    "body": body,
    "notification_id": notification_id,
    "meta": data
}
if image is not None:
    raw_data['image'] = image

send_sqs_task('cloud_message', raw_data)

# Update delivery status
if len(user_ids) > 0:
    db(db.notification_user.id.belongs(user_ids)).update(
        send_status=define.NOTIFY_STATUS_SENT
    )
```

## 🚀 Usage Methods
**Basic Notification Sending:**
```python
from applications.portal.modules.notification.notification_handler import send_notification_api

# Send simple system notification
notification_id, success_users, failed_users = send_notification_api(
    db=db,
    notification_type=define.GENERAL,
    user_ids=[12345, 12346],
    language_title={
        'en': 'System Update',
        'zh_tw': '系統更新',
        'es': 'Actualización del Sistema'
    },
    language_body={
        'en': 'New features are now available!',
        'zh_tw': '新功能現已推出！',
        'es': '¡Nuevas funciones ya están disponibles!'
    },
    extra_data={'version': '2.1.0'},
    expiration=datetime.utcnow() + timedelta(days=7)
)
```

**Carpool Invitation with Rich Content:**
```python
# Send carpool invitation with user profile data
result = send_notification_api(
    db=db,
    notification_type=define.DUO_CARPOOL_INVITE,
    user_ids=[passenger_id],
    language_title={
        'en': 'Carpool Invitation',
        'zh_tw': '拼車邀請'
    },
    language_body={
        'en': 'You have a new carpool match!',
        'zh_tw': '您有新的拼車配對！'
    },
    extra_data={
        'action': {
            'offer_id': carpool_offer_id,
            'role': 'passenger'
        },
        'route': 'Downtown Business District'
    },
    expiration=datetime.utcnow() + timedelta(hours=24)
)
```

**Silent Notification for Background Updates:**
```python
# Send silent notification for app state sync
send_notification_api(
    db=db,
    notification_type=define.SUGGESTION_INFO,
    user_ids=[user_id],
    language_title={},  # Empty for silent
    language_body={
        'en': 'Traffic update available',
        'zh_tw': '交通更新可用'
    },
    extra_data={'traffic_data': traffic_info},
    expiration=datetime.utcnow() + timedelta(hours=1),
    silent=True  # Background notification
)
```

**Microsurvey with Multiple Choice:**
```python
# Send microsurvey notification
send_notification_api(
    db=db,
    notification_type=define.MICROSURVEY_MULTIPLE_CHOICE_QUESTION,
    user_ids=[user_id],
    language_title={
        'en': 'Quick Survey',
        'zh_tw': '快速調查'
    },
    language_body={
        'en': 'How was your recent trip?',
        'zh_tw': '您最近的行程如何？'
    },
    extra_data={
        'survey_id': 'trip_satisfaction_001',
        'answers': {
            'en': ['Excellent', 'Good', 'Average', 'Poor'],
            'zh_tw': ['優秀', '良好', '普通', '不佳']
        }
    },
    expiration=datetime.utcnow() + timedelta(days=3)
)
```

## 📊 Output Examples
**Successful Notification Result:**
```python
>>> notification_id, success_users, failed_users = send_notification_api(...)
>>> print(f"Notification created: {notification_id}")
>>> print(f"Successfully sent to: {success_users}")
>>> print(f"Failed deliveries: {failed_users}")

Notification created: 12345
Successfully sent to: [12345, 12346, 12347]
Failed deliveries: []
```

**SQS Message Structure:**
```json
{
    "silent": false,
    "user_list": [12345, 12346],
    "notification_type": 60,
    "ended_on": "2024-01-16 10:30:00",
    "title": "Carpool Invitation",
    "body": "You have a new carpool match!",
    "notification_id": 12345,
    "meta": {
        "offer_id": 789,
        "route": "Downtown",
        "action": {
            "offer_id": 789,
            "suggested_user": {
                "role": "driver",
                "name": {"first_name": "John", "last_name": "Doe"},
                "rating": 4.8,
                "vehicle": {"type": "sedan", "color": "blue"}
            }
        }
    },
    "image": "https://cdn.example.com/carpool_invite.jpg"
}
```

**Language Processing Result:**
```python
# Multiple language message structure
messages = [
    {
        'lang': 'en',
        'msg_title': 'System Update',
        'msg_body': 'New features available!',
        'users': [
            {'user_id': 12345, 'token': 'fcm_token_123', 'token_type': 'fcm'},
            {'user_id': 12346, 'token': 'apns_token_456', 'token_type': 'apns'}
        ]
    },
    {
        'lang': 'zh_tw',
        'msg_title': '系統更新',
        'msg_body': '新功能推出！',
        'users': [
            {'user_id': 12347, 'token': 'fcm_token_789', 'token_type': 'fcm'}
        ]
    }
]
```

**Status Update Log:**
```bash
[DEBUG] [DUO] Broadcasting notification id: 12345
[DEBUG] [Notification] User(12345) responded to the notification(12345)
[DEBUG] [Notification] User(12346) responded to the notification(12345)
```

**Database Records Created:**
```python
# Notification record
notification = {
    'id': 12345,
    'notification_type': 60,
    'msg_data': '{"offer_id": 789, "route": "Downtown"}',
    'started_on': '2024-01-15 10:30:00',
    'ended_on': '2024-01-16 10:30:00',
    'silent': False
}

# User status records
user_statuses = [
    {'notification_msg_id': 101, 'user_id': 12345, 'send_status': 2},  # SENT
    {'notification_msg_id': 101, 'user_id': 12346, 'send_status': 2}   # SENT
]
```

## ⚠️ Important Notes
**Language Processing Complexity:**
- **Fallback Chain**: Exact match → base language → English default
- **Language Normalization**: Converts hyphens to underscores (en-us → en_us)
- **Content Consistency**: Some notification types require special content processing
- **Missing Translations**: System defaults to English if translations unavailable

**External Service Dependencies:**
- **SQS Reliability**: Notification delivery depends on AWS SQS availability
- **Push Service Limits**: FCM and APNS have rate limits and payload size restrictions
- **Token Validity**: Device tokens can expire or become invalid
- **Network Connectivity**: Delivery success depends on user device connectivity

**Performance Considerations:**
- **Database Operations**: Multiple database queries for user data and cascade inserts
- **External API Calls**: SQS calls add latency but improve reliability
- **Memory Usage**: Large user lists consume significant memory during processing
- **Concurrent Operations**: No protection against concurrent notification sending

**Data Consistency Issues:**
- **Status Updates**: Status updates occur after SQS send, creating potential inconsistency
- **Failed Deliveries**: No automatic retry mechanism for failed notifications
- **Partial Failures**: Some users may receive notifications while others fail
- **Transaction Boundaries**: No explicit transaction management across operations

## 🔗 Related File Links
**Core Dependencies:**
- `define.py` - Notification type constants and status definitions
- `dao.py` - Database table definitions supporting cascade operations
- `__init__.py` - Module initialization exporting handler functions

**Integration Points:**
- `../sqs_helper.py` - AWS SQS integration for message queuing
- `../utils.py` - CDN URL utilities for media content
- `../datetime_utils.py` - Date/time formatting utilities
- `../trip_reservation/carpool_handler.py` - Carpool data integration

**Business Logic:**
- `../../../controllers/messenger.py` - API endpoints using notification handlers
- User management systems providing device tokens and language preferences
- Carpool matching algorithms triggering notifications

**External Services:**
- FCM (Firebase Cloud Messaging) service configuration
- APNS (Apple Push Notification Service) certificates and keys
- AWS SQS queue configuration and permissions

## 📈 Use Cases
**Real-time Carpool Operations:**
- Send immediate carpool match notifications with user profiles
- Deliver driver arrival and pickup notifications with location data
- Handle carpool cancellation notifications with rebooking options
- Support carpool invitation workflows with accept/reject actions

**User Engagement Campaigns:**
- Deliver personalized suggestions based on user behavior and location
- Send microsurvey notifications for feedback collection and service improvement
- Provide incentive notifications for user retention and engagement
- Support marketing campaigns with targeted user segmentation

**System Operations and Alerts:**
- Send maintenance notifications and service disruption alerts
- Deliver security notifications and account verification messages
- Provide feature update announcements and onboarding guidance
- Support customer service communications and help notifications

**Analytics and Optimization:**
- Track notification delivery rates and user engagement metrics
- A/B test notification content and timing for optimization
- Monitor language-specific engagement patterns
- Support conversion tracking for notification-driven actions

## 🛠️ Improvement Suggestions
**Performance Optimizations:**
- Implement connection pooling for database operations
- Add batch processing for large user notification campaigns
- Cache user device and language information for frequently targeted users
- Implement asynchronous processing for non-critical notifications

**Reliability Enhancements:**
- Add comprehensive error handling with automatic retry mechanisms
- Implement transaction management for atomic notification operations
- Add circuit breaker patterns for external service integration
- Include fallback mechanisms when external services are unavailable

**Feature Enhancements:**
- Add notification scheduling and delayed delivery capabilities
- Implement rich notification support with images, actions, and deep links
- Add notification grouping and threading for better user experience
- Include notification template management for reusable content

**Security and Privacy:**
- Add content sanitization and validation for notification data
- Implement user consent management for different notification types
- Add audit logging for all notification operations
- Include data encryption for sensitive notification content

**Monitoring and Operations:**
- Add comprehensive metrics collection for notification system performance
- Implement health checks for all external service dependencies
- Add alerting for notification delivery failures or performance degradation
- Create monitoring dashboard for real-time notification system status

**Code Quality:**
- Add comprehensive unit tests for all notification scenarios
- Implement proper error handling with detailed error messages
- Add type hints and documentation for better maintainability
- Refactor large functions into smaller, more focused operations

## 🏷️ Document Tags
**Keywords:** push-notifications, multi-language, FCM, APNS, SQS, user-targeting, carpool-notifications, status-tracking, localization, device-tokens, message-delivery

**Technical Tags:** `#python` `#push-notifications` `#FCM` `#APNS` `#SQS` `#multi-language` `#localization` `#user-engagement` `#carpool` `#status-tracking`

**Target Roles:** Backend developers (advanced), Mobile developers (intermediate), DevOps engineers (advanced), Localization engineers (intermediate)
**Difficulty Level:** ⭐⭐⭐⭐ (High complexity with multi-language processing and external service integration)
**Maintenance Level:** High (requires ongoing management of external services and language content)
**Business Criticality:** Critical (core infrastructure for user engagement and operational communications)
**Related Topics:** Push notification systems, multi-language support, external service integration, user engagement, mobile development