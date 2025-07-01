# Campaign Definitions - Constants and Configuration

🔍 **Quick Summary (TL;DR)**
- Configuration constants file defining notification types, expiration times, and activity point types for the campaign management system's notification and incentive mechanisms.
- **Keywords:** define | constants | configuration | notification-type | expiration | points | activity-type | microsurvey | go-early | go-later | change-mode | duo-carpool | wta | timeout | campaign-config
- **Primary use cases:** Notification type mapping, timeout configuration, points system setup, campaign type definitions
- **Compatibility:** Python 2.7+, Used across campaign module and notification system

❓ **Common Questions Quick Index**
- **Q: What notification types are available?** → See [Technical Specifications](#technical-specifications)
- **Q: How long do campaign notifications last?** → See [Detailed Code Analysis](#detailed-code-analysis)
- **Q: What are the different point activity types?** → See [Output Examples](#output-examples)
- **Q: How do I add a new notification type?** → See [Usage Methods](#usage-methods)
- **Q: What's the difference between WTA and regular campaigns?** → See [Detailed Code Analysis](#detailed-code-analysis)
- **Q: How do I modify expiration times?** → See [Important Notes](#important-notes)
- **Q: What's the DUO notification system?** → See [Technical Specifications](#technical-specifications)
- **Q: How do I troubleshoot notification type errors?** → See [Important Notes](#important-notes)
- **Q: What are the timeout values for different campaigns?** → See [Output Examples](#output-examples)
- **Q: How do I integrate with the points system?** → See [Usage Methods](#usage-methods)

📋 **Functionality Overview**
- **Non-technical explanation:** Like a master reference book that defines all the rules, timeouts, and reward types for the campaign system - similar to a game's rule book that specifies point values, time limits, and action types. Think of it as a settings file that determines how long notifications stay active, what types of campaigns exist, and how many points users earn for different activities, or a configuration manual that standardizes all campaign behavior across the system.
- **Technical explanation:** Constants definition module implementing configuration management pattern, providing centralized parameter storage for notification types, timeout values, and activity classification used throughout the campaign management system.
- **Business value:** Centralizes campaign configuration, enables easy modification of business rules, ensures consistency across system components, simplifies maintenance of timeout and point values.
- **System context:** Configuration layer for the ConnectSmart mobility platform's campaign system, providing shared constants used by notification handlers, point calculation systems, and campaign workflow engines.

🔧 **Technical Specifications**
- **File info:** `define.py`, 26 lines, Constants module, Python, ~1KB, Complexity: Low (★☆☆☆☆)
- **Configuration categories:**
  - **NOTIFICATION_TYPE:** 7 notification type mappings (INFO, GO_EARLY, GO_LATER, CHANGE_MODE, WTA variants, MICROSURVEY, DUO)
  - **Expiration constants:** 6 timeout values in seconds (300-1800 range)
  - **POINTS_ACTIVITY_TYPE:** 5 point activity classifications (6-10 numeric range)

- **Notification type values:**
  - Regular campaigns: 12 (INFO), 13 (GO_LATER), 14 (CHANGE_MODE), 20 (MICROSURVEY), 21 (GO_EARLY)
  - WTA campaigns: 24 (WTA_GO_LATER), 25 (WTA_GO_EARLY), 26 (WTA_CHANGE_MODE)
  - Special: 63 (DUO carpool matching)

- **Timeout configurations:** Range from 5 minutes (300s) for microsurveys to 30 minutes (1800s) for action campaigns
- **Point activity types:** Sequential numbering (6-10) for different engagement activities
- **Dependencies:** None (pure constants module)

📝 **Detailed Code Analysis**
- **Notification type mapping structure:**
  ```python
  NOTIFICATION_TYPE = {
    "INFO": 12,           # Information card delivery
    "GO_EARLY": 21,       # Early departure suggestion
    "GO_LATER": 13,       # Late departure suggestion  
    "CHANGE_MODE": 14,    # Transport mode change
    "WTA_GO_LATER": 24,   # WTA (Willing to Accept) late departure
    "WTA_GO_EARLY": 25,   # WTA early departure
    "WTA_CHANGE_MODE": 26,# WTA mode change
    "MICROSURVEY": 20,    # Interactive survey
    "DUO": 63            # Duo carpool matching
  }
  ```

- **Expiration time hierarchy:**
  ```python
  # Short-term interactions (5 minutes)
  MICROSURVEY_EXPIRATION_TIME = 300
  EXPIRATION_MESSAGE_QUEUE = 300
  EXPIRATION_DUO_NOTIFICATION = 300
  
  # Medium-term actions (30 minutes)
  EXPIRATION_GO_LATER = 1800
  EXPIRATION_GO_EARLY = 1800
  EXPIRATION_CHANGE_MODE = 1800
  ```

- **Points activity classification:**
  ```python
  POINTS_ACTIVITY_TYPE_MICROSURVEY = 6   # Survey completion
  POINTS_ACTIVITY_TYPE_GOLATER = 7       # Late departure action
  POINTS_ACTIVITY_TYPE_CHANGEMODE = 8    # Mode change action
  POINTS_ACTIVITY_TYPE_DUOCARPOOL = 9    # Carpool participation
  POINTS_ACTIVITY_TYPE_GOEARLY = 10      # Early departure action
  ```

- **Design patterns:** Simple dictionary and constant definition pattern, no classes or functions
- **Memory footprint:** Minimal, constants loaded once at import time
- **Threading safety:** Read-only constants are inherently thread-safe

🚀 **Usage Methods**
- **Import specific notification types:**
  ```python
  from campaign.define import NOTIFICATION_TYPE
  # Use in notification handler
  notification_id = NOTIFICATION_TYPE["GO_EARLY"]  # Returns 21
  send_notification(user_id, notification_id, message_data)
  ```

- **Access expiration times:**
  ```python
  from campaign.define import EXPIRATION_GO_EARLY, MICROSURVEY_EXPIRATION_TIME
  # Set notification expiration
  import time
  expiry_time = int(time.time()) + EXPIRATION_GO_EARLY  # 30 minutes from now
  queue_notification(notification, expiry_time)
  ```

- **Points system integration:**
  ```python
  from campaign.define import POINTS_ACTIVITY_TYPE_MICROSURVEY
  # Record user activity with point type
  record_user_points(user_id, point_value, POINTS_ACTIVITY_TYPE_MICROSURVEY)
  ```

- **Campaign handler integration:**
  ```python
  from campaign.define import NOTIFICATION_TYPE, EXPIRATION_CHANGE_MODE
  # Create mode change campaign
  def create_mode_change_campaign(user_id, message):
      return {
          "notification_type": NOTIFICATION_TYPE["CHANGE_MODE"],
          "expiration": EXPIRATION_CHANGE_MODE,
          "user_id": user_id,
          "message": message
      }
  ```

- **WTA campaign handling:**
  ```python
  from campaign.define import NOTIFICATION_TYPE
  # Handle WTA vs regular campaigns
  if is_wta_user:
      notif_type = NOTIFICATION_TYPE["WTA_GO_EARLY"]
  else:
      notif_type = NOTIFICATION_TYPE["GO_EARLY"]
  ```

📊 **Output Examples**
- **Notification type lookup:**
  ```python
  >>> from campaign.define import NOTIFICATION_TYPE
  >>> print(NOTIFICATION_TYPE["MICROSURVEY"])
  20
  >>> print(NOTIFICATION_TYPE["DUO"])
  63
  >>> print(list(NOTIFICATION_TYPE.keys()))
  ['INFO', 'GO_EARLY', 'GO_LATER', 'CHANGE_MODE', 'WTA_GO_LATER', 
   'WTA_GO_EARLY', 'WTA_CHANGE_MODE', 'MICROSURVEY', 'DUO']
  ```

- **Expiration time calculations:**
  ```python
  >>> from campaign.define import *
  >>> print(f"Microsurvey expires in {MICROSURVEY_EXPIRATION_TIME} seconds")
  Microsurvey expires in 300 seconds
  >>> print(f"Go Early expires in {EXPIRATION_GO_EARLY/60} minutes")
  Go Early expires in 30.0 minutes
  ```

- **Points activity mapping:**
  ```python
  >>> from campaign.define import *
  >>> activity_types = {
  ...     "microsurvey": POINTS_ACTIVITY_TYPE_MICROSURVEY,
  ...     "go_later": POINTS_ACTIVITY_TYPE_GOLATER,
  ...     "change_mode": POINTS_ACTIVITY_TYPE_CHANGEMODE,
  ...     "duo_carpool": POINTS_ACTIVITY_TYPE_DUOCARPOOL,
  ...     "go_early": POINTS_ACTIVITY_TYPE_GOEARLY
  ... }
  >>> print(activity_types)
  {'microsurvey': 6, 'go_later': 7, 'change_mode': 8, 'duo_carpool': 9, 'go_early': 10}
  ```

- **Configuration validation:**
  ```python
  >>> # Validate notification type exists
  >>> campaign_type = "INVALID_TYPE"
  >>> if campaign_type in NOTIFICATION_TYPE:
  ...     print(f"Valid type: {NOTIFICATION_TYPE[campaign_type]}")
  ... else:
  ...     print(f"Invalid campaign type: {campaign_type}")
  Invalid campaign type: INVALID_TYPE
  ```

- **Timeout comparison:**
  ```python
  >>> from campaign.define import *
  >>> timeouts = [
  ...     ("Microsurvey", MICROSURVEY_EXPIRATION_TIME),
  ...     ("Go Early", EXPIRATION_GO_EARLY),
  ...     ("Change Mode", EXPIRATION_CHANGE_MODE),
  ...     ("Duo Notification", EXPIRATION_DUO_NOTIFICATION)
  ... ]
  >>> for name, timeout in sorted(timeouts, key=lambda x: x[1]):
  ...     print(f"{name}: {timeout}s ({timeout/60}min)")
  Microsurvey: 300s (5.0min)
  Duo Notification: 300s (5.0min)
  Go Early: 1800s (30.0min)
  Change Mode: 1800s (30.0min)
  ```

⚠️ **Important Notes**
- **Security considerations:**
  - Constants are read-only and pose no direct security risk
  - Validate notification types before using in database queries
  - Ensure timeout values don't allow indefinite message queuing
  - Consider rate limiting based on notification types

- **Configuration management:**
  - Changes to these constants affect all campaign functionality immediately
  - Test thoroughly before modifying expiration times in production
  - Document any changes to notification type mappings
  - Consider environment-specific overrides for different deployment stages

- **Common troubleshooting:**
  - **KeyError on notification type:** Verify the key exists in NOTIFICATION_TYPE dictionary
  - **Unexpected timeout behavior:** Check if expiration constants match business requirements
  - **Point calculation issues:** Ensure POINTS_ACTIVITY_TYPE values are unique and sequential
  - **Import errors:** Verify the define module is in the correct path and accessible

- **Performance considerations:**
  - Constants are loaded once at import time - no runtime performance impact
  - Dictionary lookups are O(1) operations
  - Consider caching if these values are accessed very frequently

- **Breaking changes:**
  - Changing notification type values breaks existing database records
  - Modifying expiration times affects active campaigns
  - Point activity type changes impact historical reporting

🔗 **Related File Links**
- **Core dependencies:**
  - `__init__.py` - Module package that imports these constants
  - `campaign_handler.py` - Business logic that uses notification types and timeouts
  - `dao.py` - Database tables that store notification type values
- **System integration:**
  - `../notification/` - Notification module that consumes these notification types
  - Web2py controllers that reference these constants for campaign management
  - Database migration scripts that use these values for schema setup
- **Configuration files:** Web2py application configuration that may override these defaults
- **API documentation:** REST API specs that reference these notification types
- **Test files:** Unit tests that validate these constant values

📈 **Use Cases**
- **Campaign configuration:** Setting up new campaign types with appropriate notification IDs and timeouts
- **Notification system integration:** Mapping campaign actions to specific notification delivery mechanisms
- **Points system management:** Classifying user activities for reward calculation and reporting
- **Timeout management:** Configuring how long different types of campaign notifications remain active
- **WTA (Willing to Accept) campaigns:** Distinguishing between regular and WTA campaign notifications
- **A/B testing:** Using different notification types to test campaign effectiveness
- **System monitoring:** Tracking campaign performance by notification type and timeout behavior

🛠️ **Improvement Suggestions**
- **Code organization:**
  - Group related constants into classes or modules (Low complexity, improves maintainability)
  - Add docstrings explaining each constant's purpose (Low complexity, improves documentation)
  - Implement environment-specific configuration overrides (Medium complexity, improves flexibility)

- **Feature enhancements:**
  - Add validation functions for notification types and timeouts (Medium complexity, improves reliability)
  - Implement configuration hot-reloading without system restart (High complexity, improves operations)
  - Add business rule validation for timeout relationships (Medium complexity, prevents configuration errors)

- **Monitoring improvements:**
  - Add configuration change tracking and auditing (Medium complexity, improves governance)
  - Implement metrics for notification type usage patterns (Low complexity, provides insights)
  - Add alerts for configuration inconsistencies (Medium complexity, improves reliability)

- **Documentation enhancements:**
  - Create configuration decision tree for choosing notification types (Low complexity, improves usability)
  - Add business context explanations for each constant (Low complexity, improves understanding)
  - Document the relationship between notification types and user experience (Medium complexity, improves design decisions)

🏷️ **Document Tags**
- **Keywords:** constants, configuration, notification-types, expiration-times, points-system, campaign-config, timeout-management, wta-campaigns, microsurvey-config, duo-carpool, activity-types
- **Technical tags:** #python #constants #configuration #campaign-management #notification-system #points-system #timeout-config #wta #microsurvey #carpool-matching
- **Target roles:** Backend developers (junior-senior), Campaign managers (junior-intermediate), System administrators (intermediate), Product managers (junior-intermediate)
- **Difficulty level:** ⭐☆☆☆☆ (Basic Python constants understanding required)
- **Maintenance level:** Low (occasional updates for new campaign types or timeout adjustments)
- **Business criticality:** Medium (affects campaign behavior but doesn't break core functionality if modified)
- **Related topics:** Configuration management, Campaign management systems, Notification systems, Points and rewards systems, Timeout and expiration management