# Campaign Handler - Business Logic Engine

🔍 **Quick Summary (TL;DR)**
- Campaign business logic engine that handles user engagement workflows including microsurveys, push notifications, location tracking, and incentive point management for mobility campaigns.
- **Keywords:** campaign | handler | business-logic | microsurvey | notification | push-notification | location | timeslot | points | mobility | engagement | user-record | carpool | goearly | infocard | resend | status-management
- **Primary use cases:** Campaign execution, user engagement tracking, push notification delivery, microsurvey management, location verification
- **Compatibility:** Python 2.7+, Web2py framework, requires notification module and current database context

❓ **Common Questions Quick Index**
- **Q: How do I send a campaign notification?** → See [Usage Methods](#usage-methods)
- **Q: What's the microsurvey workflow?** → See [Detailed Code Analysis](#detailed-code-analysis)
- **Q: How do I track user responses?** → See [Output Examples](#output-examples)
- **Q: What are the different campaign card types?** → See [Technical Specifications](#technical-specifications)
- **Q: How do I handle campaign resending logic?** → See [Usage Methods](#usage-methods)
- **Q: What happens when a campaign expires?** → See [Important Notes](#important-notes)
- **Q: How do I troubleshoot notification failures?** → See [Important Notes](#important-notes)
- **Q: What are the timeslot calculations?** → See [Detailed Code Analysis](#detailed-code-analysis)
- **Q: How do I integrate with location services?** → See [Related File Links](#related-file-links)
- **Q: What's the point calculation system?** → See [Output Examples](#output-examples)

📋 **Functionality Overview**
- **Non-technical explanation:** Like a smart campaign manager that automatically sends personalized mobility suggestions (go early, change transport mode, take surveys) to users at the right time, tracks their responses, awards points, and handles follow-up communications. Think of it as a personal mobility assistant that learns from user behavior and provides timely travel recommendations, or an automated marketing system that delivers contextual messages based on travel patterns.
- **Technical explanation:** Event-driven campaign orchestration engine implementing state machine patterns for user engagement workflows, featuring notification delivery, response tracking, point calculation, and retry mechanisms with location-aware timing logic.
- **Business value:** Enables automated user engagement campaigns, improves mobility behavior change through incentives, reduces manual campaign management overhead, and provides data-driven insights into user travel patterns.
- **System context:** Core business logic layer of the ConnectSmart mobility platform's campaign management system, interfacing with notification services, database layer, and location tracking components.

🔧 **Technical Specifications**
- **File info:** `campaign_handler.py`, 488 lines, Business logic module, Python, ~20KB, Complexity: High (★★★★☆)
- **Core functions:** 14 main functions with specialized campaign processing logic
- **Dependencies:**
  - `define` module (Critical): Campaign constants and notification types
  - `notification` module (Critical): Push notification delivery system
  - `gluon.current` (Critical): Web2py database context
  - `json`, `datetime`, `time`, `logging` (Required): Standard Python libraries
- **Database tables accessed:** `cm_campaign`, `cm_step`, `cm_campaign_user`, `cm_location`, `cm_user_record`, `cm_microsurvey_record`
- **Notification types:** 12 (INFO), 20 (MICROSURVEY), 21 (GO_EARLY), 24-26 (WTA variants)
- **Timeslot system:** 15-minute intervals, 96 slots per day (24 hours × 4)

📝 **Detailed Code Analysis**
- **Core functions breakdown:**
  - `uodtsGenerator(time)`: Generates time range for campaign delivery (±2 slots)
  - `cmPushNotification()`: Sends push notifications with validation and error handling
  - `microsurvey_next_card()`: Determines next survey question based on user responses
  - `change_status()`: Updates campaign user status and reply tracking
  - `microsurvey_record()`: Records survey responses and calculates points
  - `resend_card()`: Handles campaign retry logic with timing validation
  - `get_timeslot()`: Converts time string to 15-minute slot number

- **Timeslot calculation algorithm:**
  ```python
  def get_timeslot(time_str):
      timeArr = time_str.split(":")
      slot = round((int(timeArr[0]) * 60 + int(timeArr[1])) / 15)
      return int(slot)  # Returns 0-95 (96 slots per day)
  ```

- **Campaign card types:**
  - **Type 1 (Info Card):** Information delivery without user action required
  - **Type 2 (Go Early):** Travel time optimization suggestions with location data
  - **Type 5 (Microsurvey):** Interactive survey with branching logic

- **Error handling patterns:** Try-catch blocks with detailed logging, graceful degradation, status tracking
- **Memory management:** Efficient database queries with selective field loading
- **Performance characteristics:** Database-intensive operations, JSON parsing overhead, datetime calculations

🚀 **Usage Methods**
- **Send info card notification:**
  ```python
  from campaign_handler import infocard
  notification = infocard(step_obj, campaign_user_obj)
  # Returns formatted notification dict
  ```

- **Process microsurvey response:**
  ```python
  from campaign_handler import microsurvey_record, microsurvey_next_card
  # Record user response
  success = microsurvey_record(user_id, campaign_id, card_id, step_no, 
                               answer_list, points, status_id)
  # Get next question
  next_step = microsurvey_next_card(choices_dict, user_answers)
  ```

- **Campaign status management:**
  ```python
  from campaign_handler import change_status, ms_change_status
  # Update regular campaign status
  result = change_status(user_id, campaign_id, card_id, status_id, accept_flag)
  # Update microsurvey campaign status
  result = ms_change_status(user_id, campaign_id, status_id, accept_flag)
  ```

- **Resend campaign logic:**
  ```python
  from campaign_handler import resend_card
  # Check and resend expired campaigns
  card_data = resend_card(user_id, resend_duration_minutes)
  if card_data:
      # Process resend notification
      send_notification(card_data)
  ```

📊 **Output Examples**
- **Successful microsurvey card generation:**
  ```json
  {
    "silent": false,
    "user_list": [12345],
    "notification_type": 20,
    "ended_on": "2024-12-01 18:00:00",
    "title": {"en": "How was your trip?"},
    "body": {"en": "Please rate your experience"},
    "meta": {
      "expiration_date": 1733068800,
      "question": {"en": "How was your trip?"},
      "answers": ["Excellent", "Good", "Fair", "Poor"],
      "points": 5.0,
      "card_id": "789"
    }
  }
  ```

- **Go early notification structure:**
  ```json
  {
    "silent": false,
    "user_list": [12345],
    "notification_type": 21,
    "title": {"en": "Leave 15 minutes early?"},
    "body": {"en": "Beat traffic and earn points!"},
    "meta": {
      "expiration_date": 1733067840,
      "action": {
        "departure_time": 1733068800,
        "o_lat": 37.7749, "o_lon": -122.4194,
        "d_lat": 37.7849, "d_lon": -122.4094,
        "current_mode": 1
      },
      "points": 10.0,
      "card_id": "456"
    }
  }
  ```

- **Error handling examples:**
  ```
  [ERROR] change_status error: ValueError
  [DEBUG] db cm_campaign_user notFound!
  [DEBUG] [userRecordId] 12345
  ```

- **Timeslot calculation examples:**
  ```python
  get_timeslot("08:15:00") → 33  # (8*60 + 15) / 15 = 33
  get_timeslot("12:00:00") → 48  # (12*60 + 0) / 15 = 48
  get_timeslot("23:45:00") → 95  # (23*60 + 45) / 15 = 95
  ```

⚠️ **Important Notes**
- **Security considerations:**
  - Validate user permissions before processing campaign actions
  - Sanitize JSON input in choices and answer fields to prevent injection
  - Use parameterized database queries to prevent SQL injection
  - Verify notification recipient authorization

- **Performance gotchas:**
  - `resend_card()` queries can be expensive with large user bases; consider pagination
  - JSON parsing in `microsurvey_next_card()` should validate structure
  - Datetime calculations may cause timezone issues; ensure UTC consistency
  - Database connections should be properly managed in Web2py context

- **Common troubleshooting:**
  - **Notification not sent:** Check notification_type exists in database, verify user permissions
  - **Points not awarded:** Ensure campaign.points field is set, check decimal precision
  - **Timeslot errors:** Validate time format (HH:MM:SS), handle edge cases at midnight
  - **Resend not working:** Verify modified_on timestamps, check campaign status and end_time

- **Breaking changes:** Module relies on Web2py's current.db context; ensure proper initialization
- **Rate limiting:** No built-in rate limiting; implement at application level for high-volume campaigns

🔗 **Related File Links**
- **Core dependencies:**
  - `define.py` - Campaign constants and notification type definitions
  - `dao.py` - Database table definitions for campaign data
  - `../notification/` - Push notification delivery system
- **Database integration:** Web2py database models using campaign tables
- **API endpoints:** Controllers that call campaign handler functions
- **Configuration:** Web2py application configuration for notification settings
- **Testing files:** Unit tests for campaign business logic validation
- **Monitoring:** Logging configuration for campaign execution tracking

📈 **Use Cases**
- **Real-time campaign execution:** Automated delivery of mobility suggestions based on user travel patterns
- **User engagement tracking:** Recording and analyzing user responses to campaign interventions
- **Point-based incentive systems:** Calculating and awarding points for behavior change activities
- **A/B testing campaigns:** Different message variations with response tracking
- **Location-based targeting:** Delivering campaigns based on user origin/destination patterns
- **Retry mechanisms:** Handling failed notification deliveries with intelligent resend logic
- **Multi-step workflows:** Managing complex campaign sequences like multi-question surveys

🛠️ **Improvement Suggestions**
- **Code optimization:**
  - Implement connection pooling for database operations (High complexity, improves performance)
  - Add caching layer for frequently accessed campaign data (Medium complexity, reduces database load)
  - Optimize timeslot calculations with lookup tables (Low complexity, improves speed)

- **Feature enhancements:**
  - Add campaign scheduling with cron integration (Medium complexity, enables automated campaigns)
  - Implement user segmentation based on behavior patterns (High complexity, improves targeting)
  - Add real-time analytics dashboard for campaign performance (High complexity, business value)

- **Technical debt:**
  - Replace wildcard imports with specific imports (Low complexity, improves maintainability)
  - Add comprehensive error codes and structured logging (Medium complexity, improves debugging)
  - Implement async processing for high-volume notifications (High complexity, improves scalability)

- **Monitoring improvements:**
  - Add performance metrics for each campaign function (Low complexity, aids optimization)
  - Implement campaign delivery success rate tracking (Medium complexity, improves reliability)
  - Add user engagement analytics and reporting (Medium complexity, provides business insights)

🏷️ **Document Tags**
- **Keywords:** campaign-handler, business-logic, microsurvey, push-notification, user-engagement, mobility-incentive, timeslot-calculation, points-system, location-tracking, notification-delivery, workflow-engine, campaign-management
- **Technical tags:** #python #web2py #business-logic #campaign-management #push-notifications #microsurvey #location-services #incentive-system #workflow-engine #mobility-platform
- **Target roles:** Backend developers (intermediate-senior), Campaign managers (junior-intermediate), System architects (senior), Product managers (intermediate)
- **Difficulty level:** ⭐⭐⭐⭐☆ (Requires understanding of Web2py, database operations, notification systems, and campaign logic)
- **Maintenance level:** High (frequent updates for new campaign types and business rule changes)
- **Business criticality:** Critical (core component of user engagement and revenue generation)
- **Related topics:** Campaign management, User engagement systems, Push notification platforms, Location-based services, Incentive program management, Mobility behavior analytics