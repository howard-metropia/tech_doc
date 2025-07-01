# Notification Constants and Definitions - Type and Status Enumerations

## 🔍 Quick Summary (TL;DR)
**Comprehensive constants definition file containing 50+ notification type identifiers and status codes for the MaaS platform's notification system.** Provides standardized enumeration for carpool notifications, system alerts, microsurveys, suggestions, and delivery status tracking to ensure consistency across the notification infrastructure.

**Core functionality:** Notification type constants | Status enumerations | Carpool notifications | System alerts | Microsurvey types | Suggestion categories | Delivery status codes
**Primary use cases:** Notification categorization, status validation, business logic consistency, type identification, status tracking, system integration
**Compatibility:** Python 2.7+, Web2py framework, notification system components, external services

## ❓ Common Questions Quick Index
- **Q: What notification types are available?** → See [Technical Specifications](#technical-specifications)
- **Q: How many carpool notification types exist?** → See [Output Examples](#output-examples)
- **Q: What are the delivery status codes?** → See [Detailed Code Analysis](#detailed-code-analysis)
- **Q: How to validate notification status?** → See [Usage Methods](#usage-methods)
- **Q: What's the difference between notification types?** → See [Functionality Overview](#functionality-overview)
- **Q: How to extend notification types?** → See [Improvement Suggestions](#improvement-suggestions)
- **Q: What are microsurvey notification types?** → See [Use Cases](#use-cases)
- **Q: How does notification categorization work?** → See [Important Notes](#important-notes)

## 📋 Functionality Overview
**Non-technical explanation:** Think of this as the "catalog of message types" for a transportation app. Like how a postal service has different categories for mail (express, regular, certified), this system defines different types of notifications - from carpool invitations to system updates to survey requests. Each type has a unique number so the system knows how to handle it properly.

**Technical explanation:** Enumeration constants module implementing comprehensive notification type taxonomy and status lifecycle management. Provides centralized definition of business rules, categorization schemes, and state management for the notification subsystem.

**Business value:** Ensures consistent notification handling across all platform components, enables proper business logic implementation for different notification scenarios, and provides clear categorization for analytics and user experience optimization.

**System context:** Foundational configuration layer used by notification handlers, database tables, mobile applications, and analytics systems to maintain consistent notification type identification and status management.

## 🔧 Technical Specifications
- **File:** `applications/portal/modules/notification/define.py`
- **Language:** Python 2.7+
- **Type:** Constants and enumeration definitions
- **Size:** ~62 lines
- **Complexity:** ⭐⭐ (Low-Medium - extensive enumeration with categorization)

**Notification Categories (50+ types):**
1. **General Notifications** (1): System-wide announcements
2. **Carpool Group Management** (2-5): Group join/leave operations  
3. **Carpool Offer Management** (6-11): Ride offer interactions
4. **Suggestion System** (12-17, 21, 63): AI-driven user suggestions
5. **Trip Operations** (18, 27-29): Real-time trip status updates
6. **Microsurvey System** (19-20, 22-23): User feedback collection
7. **WTA (Willing to Accept)** (24-26): Incentive negotiations
8. **Carpool Matching** (60-78, 96, 100061-100067, 100074): Comprehensive carpool lifecycle
9. **Wallet Operations** (76-77): Payment and billing notifications

**Status Lifecycle (5 states):**
- `NOTIFY_STATUS_QUEUE = 0` - Queued for delivery
- `NOTIFY_STATUS_SEND_FAIL = 1` - Delivery failed
- `NOTIFY_STATUS_SENT = 2` - Successfully sent to device
- `NOTIFY_STATUS_RECEIVED = 3` - Confirmed received by device
- `NOTIFY_STATUS_REPLIED = 4` - User responded to notification

**Special Categories:**
- **High-Value Constants**: 100061-100067, 100074 for specific carpool scenarios
- **General Subtypes**: 1001 for specific general notification scenarios

## 📝 Detailed Code Analysis
**Core Notification Type Structure:**
```python
# Basic system notifications
GENERAL = 1

# Carpool group lifecycle
DUO_GROUP_JOIN_REQUEST = 2      # User requests to join group
DUO_GROUP_JOIN_ACCEPTED = 3     # Join request approved
DUO_GROUP_JOIN_REJECTED = 4     # Join request denied
DUO_GROUP_DISBANDED = 5         # Group dissolved

# Carpool offer lifecycle
DUO_OFFER_JOIN_REQUEST = 6      # Request to join specific ride
DUO_OFFER_JOIN_ACCEPTED = 7     # Join request approved
DUO_OFFER_JOIN_REJECTED = 8     # Join request denied
DUO_OFFER_NOT_AVAILABLE = 9     # Offer no longer available
DUO_OFFER_CANCELLED = 10        # Offer cancelled by driver
```

**Suggestion System Constants:**
```python
# AI-driven user suggestions
SUGGESTION_INFO = 12                    # General information suggestion
SUGGESTION_GO_LATER = 13               # Suggest delayed departure
SUGGESTION_CHANGE_MODE = 14            # Suggest alternative transport
SUGGESTION_CARPOOL = 15                # Suggest carpool option
SUGGESTION_CARPOOL_ACCEPTED = 16       # Carpool suggestion accepted
SUGGESTION_CARPOOL_REJECTED = 17       # Carpool suggestion declined
SUGGESTION_GO_EARLY = 21               # Suggest earlier departure
SUGGESTION_CARPOOL_AUTO_MATCH = 63     # Automatic carpool matching
```

**Advanced Carpool Matching:**
```python
# Comprehensive carpool notification system
DUO_CARPOOL_INVITE = 60                              # General invite
DUO_CARPOOL_MATCHING = 61                            # Basic matching
DUO_CARPOOL_MATCHING_RIDER = 100061                  # Rider-specific matching
DUO_CARPOOL_MATCHINGS_RIDER = 100062                 # Multiple rider matches
DUO_CARPOOL_MATCHING_DRIVER = 100063                 # Driver-specific matching
DUO_CARPOOL_MATCHINGS_DRIVER = 100064                # Multiple driver matches
DUO_CARPOOL_CANCELLED_WITH_REASON_IN_MATCHED_HAS_REMATCH = 100066  # Complex cancellation with rematch
DUO_CARPOOL_CANCELLED_WITH_REASON_IN_MATCHED_NO_REMATCH = 100067   # Complex cancellation without rematch
```

**Status Lifecycle Management:**
```python
# Notification delivery tracking
NOTIFY_STATUS_QUEUE = 0        # Waiting in delivery queue
NOTIFY_STATUS_SEND_FAIL = 1    # Push notification service failure
NOTIFY_STATUS_SENT = 2         # Successfully sent to device
NOTIFY_STATUS_RECEIVED = 3     # Device confirmed receipt
NOTIFY_STATUS_REPLIED = 4      # User interacted with notification
```

**Design Patterns:**
- **Enumeration Simulation**: Integer constants with meaningful names
- **Categorical Organization**: Grouped by functional domain
- **Hierarchical Numbering**: Related types use sequential numbers
- **Special Handling**: High-value constants for complex scenarios

## 🚀 Usage Methods
**Basic Type Validation:**
```python
from applications.portal.modules.notification.define import *

def is_carpool_notification(notification_type):
    carpool_types = [
        DUO_GROUP_JOIN_REQUEST, DUO_GROUP_JOIN_ACCEPTED, DUO_GROUP_JOIN_REJECTED,
        DUO_OFFER_JOIN_REQUEST, DUO_OFFER_JOIN_ACCEPTED, DUO_OFFER_JOIN_REJECTED,
        DUO_CARPOOL_INVITE, DUO_CARPOOL_MATCHING, DUO_CARPOOL_CANCELLED_WITH_REASON
    ]
    return notification_type in carpool_types

# Usage
if is_carpool_notification(notification_type):
    handle_carpool_notification(notification_data)
```

**Status Transition Validation:**
```python
def validate_status_transition(current_status, new_status):
    valid_transitions = {
        NOTIFY_STATUS_QUEUE: [NOTIFY_STATUS_SENT, NOTIFY_STATUS_SEND_FAIL],
        NOTIFY_STATUS_SEND_FAIL: [NOTIFY_STATUS_QUEUE, NOTIFY_STATUS_SENT],
        NOTIFY_STATUS_SENT: [NOTIFY_STATUS_RECEIVED],
        NOTIFY_STATUS_RECEIVED: [NOTIFY_STATUS_REPLIED]
    }
    return new_status in valid_transitions.get(current_status, [])

# Update status with validation
if validate_status_transition(current, new):
    update_notification_status(notification_id, new)
```

**Business Logic Implementation:**
```python
def handle_notification_by_type(notification_type, data):
    if notification_type == DUO_CARPOOL_INVITE:
        return process_carpool_invitation(data)
    elif notification_type in [SUGGESTION_GO_LATER, SUGGESTION_GO_EARLY]:
        return process_timing_suggestion(data)
    elif notification_type in [MICROSURVEY_MULTIPLE_CHOICE_QUESTION, MICROSURVEY_RATING_QUESTION]:
        return process_microsurvey(data)
    else:
        return process_general_notification(data)
```

**Category-Based Processing:**
```python
def get_notification_category(notification_type):
    if notification_type in range(2, 6):  # 2-5
        return 'carpool_group'
    elif notification_type in range(6, 12):  # 6-11
        return 'carpool_offer'
    elif notification_type in [12, 13, 14, 15, 16, 17, 21, 63]:
        return 'suggestion'
    elif notification_type in [19, 20, 22, 23]:
        return 'microsurvey'
    elif notification_type >= 100000:
        return 'advanced_carpool'
    else:
        return 'general'
```

## 📊 Output Examples
**Notification Type Categories:**
```python
>>> print("Carpool Group Types:")
>>> for i in [DUO_GROUP_JOIN_REQUEST, DUO_GROUP_JOIN_ACCEPTED, DUO_GROUP_JOIN_REJECTED, DUO_GROUP_DISBANDED]:
...     print(f"  {i}: {get_type_name(i)}")

Carpool Group Types:
  2: Join Request
  3: Join Accepted  
  4: Join Rejected
  5: Group Disbanded
```

**Suggestion System Types:**
```python
>>> suggestion_types = [
...     SUGGESTION_INFO, SUGGESTION_GO_LATER, SUGGESTION_CHANGE_MODE,
...     SUGGESTION_CARPOOL, SUGGESTION_GO_EARLY
... ]
>>> print("Suggestion Types:", suggestion_types)

Suggestion Types: [12, 13, 14, 15, 21]
```

**Status Progression Example:**
```python
>>> statuses = [NOTIFY_STATUS_QUEUE, NOTIFY_STATUS_SENT, NOTIFY_STATUS_RECEIVED, NOTIFY_STATUS_REPLIED]
>>> status_names = ['Queue', 'Sent', 'Received', 'Replied']
>>> for status, name in zip(statuses, status_names):
...     print(f"{name}: {status}")

Queue: 0
Sent: 2
Received: 3
Replied: 4
```

**Advanced Carpool Types:**
```python
>>> advanced_types = [
...     DUO_CARPOOL_MATCHING_RIDER, DUO_CARPOOL_MATCHINGS_RIDER,
...     DUO_CARPOOL_MATCHING_DRIVER, DUO_CARPOOL_MATCHINGS_DRIVER
... ]
>>> print("Advanced Carpool Types:", advanced_types)

Advanced Carpool Types: [100061, 100062, 100063, 100064]
```

**Microsurvey Types:**
```python
>>> microsurvey_types = [
...     MICROSURVEY_FIRST_TIME_NOTE, MICROSURVEY_MULTIPLE_CHOICE_QUESTION,
...     MICROSURVEY_RATING_QUESTION, MICROSURVEY_OPEN_ENDED_QUESTION
... ]
>>> print("Microsurvey Types:", microsurvey_types)

Microsurvey Types: [19, 20, 22, 23]
```

## ⚠️ Important Notes
**Business Logic Considerations:**
- **Type Uniqueness**: Each notification type requires unique handling logic
- **Status Transitions**: Not all status transitions are valid - implement validation
- **Category Grouping**: Related types should be processed similarly
- **Special Cases**: High-value constants (100061+) indicate complex scenarios requiring special handling

**Development Guidelines:**
- **Backward Compatibility**: Adding new types should use higher numbers
- **Documentation**: Each new type should have clear business meaning
- **Testing**: All notification types should have corresponding test cases
- **Localization**: Each type needs multi-language support in notification content

**System Integration:**
- **Mobile Apps**: Must handle all notification types appropriately
- **Analytics**: Type categorization affects reporting and metrics
- **External Services**: Push notification services need type-specific configuration
- **Database**: Status values must align with database constraints

**Performance Considerations:**
- **Constants Loading**: Values loaded once at module import time
- **Validation Performance**: Use sets or dictionaries for O(1) type checking
- **Memory Usage**: Minimal - only integer constants
- **Cache Friendly**: Constant values can be safely cached

## 🔗 Related File Links
**Core Module Files:**
- `dao.py` - Database tables using these constants for validation
- `notification_handler.py` - Business logic implementing type-specific handling
- `__init__.py` - Module exports making constants available system-wide

**Business Logic Integration:**
- `../../../controllers/messenger.py` - API endpoints using notification types
- `../trip_reservation/` - Carpool-related notification generation
- `../carpool/` - Group management notification triggers

**Mobile Applications:**
- iOS and Android apps implementing notification type handling
- Push notification service configuration for different types
- User interface logic for type-specific notification display

**Analytics and Reporting:**
- Business intelligence systems categorizing notifications by type
- Engagement metrics grouped by notification category
- A/B testing frameworks using type-based segmentation

## 📈 Use Cases
**Carpool Lifecycle Management:**
- Track complete carpool interaction flow from invitation to completion
- Handle complex matching scenarios with appropriate notification types
- Support group-based carpooling with membership management notifications
- Manage real-time trip updates and status changes

**User Engagement and Suggestions:**
- Deliver AI-driven suggestions for optimal travel timing and modes
- Support microsurvey campaigns for user feedback collection
- Implement incentive-based suggestion acceptance workflows
- Track user response patterns for suggestion optimization

**System Operations:**
- Send maintenance and update notifications to all users
- Handle emergency alerts and service disruptions
- Deliver account security and verification notifications
- Support customer service and help notifications

**Business Intelligence:**
- Categorize notifications for engagement analysis
- Track conversion rates for different suggestion types
- Monitor carpool adoption through notification response rates
- Analyze user preferences through notification interaction patterns

## 🛠️ Improvement Suggestions
**Code Organization:**
- Convert to proper Python Enum classes for Python 3+ compatibility
- Add docstrings explaining business logic for each notification type
- Group related constants into logical categories or sub-modules
- Include type-specific metadata (priority, expiration, etc.)

**Business Logic Enhancement:**
- Add notification priority levels for different types
- Include default expiration times for time-sensitive notifications
- Add notification frequency limits for different categories
- Implement user preference mapping for notification types

**Validation and Safety:**
- Add type validation functions for each category
- Include status transition validation rules
- Add deprecation markers for obsolete notification types
- Implement automatic testing for all notification type handlers

**Feature Extensions:**
- Add support for templated notification types
- Include rich notification support with actions and media
- Add notification scheduling and delayed delivery types
- Support for conditional notifications based on user state

**Monitoring and Analytics:**
- Add type-specific metrics collection
- Include success rate tracking by notification type
- Add performance monitoring for different notification categories
- Implement alerting for notification type usage anomalies

**Documentation and Maintenance:**
- Create comprehensive type catalog with business descriptions
- Add decision trees for choosing appropriate notification types
- Include migration guides for notification type changes
- Document integration requirements for each notification category

## 🏷️ Document Tags
**Keywords:** notification-types, constants, enumerations, carpool-notifications, status-codes, microsurvey, suggestions, delivery-status, type-validation, business-logic

**Technical Tags:** `#python` `#constants` `#enumerations` `#notifications` `#carpool` `#status-management` `#business-logic` `#type-system` `#categorization`

**Target Roles:** Backend developers (beginner), Mobile developers (beginner), Business analysts (beginner), QA engineers (intermediate)
**Difficulty Level:** ⭐⭐ (Low-Medium - extensive but well-organized enumeration)
**Maintenance Level:** Medium (requires updates as business requirements evolve)
**Business Criticality:** High (core configuration affecting all notification functionality)
**Related Topics:** Business rule management, notification systems, enumeration patterns, type systems, mobile development