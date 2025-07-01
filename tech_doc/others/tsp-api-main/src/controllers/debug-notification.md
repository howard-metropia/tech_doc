# Debug Notification Controller Documentation

## 🔍 Quick Summary (TL;DR)
This controller provides endpoints specifically for testing the push notification system. It allows developers to trigger and verify different types of notifications to a specific user, and then confirm that the notification was correctly received and processed by the client.

**Keywords:** debug-notification | test-notification | push-notification | notification-system | integration-test | fcm | apns | user-notification | DUO-carpool

**Primary use cases:** 
- End-to-end testing of the push notification pipeline.
- Triggering specific carpool-related notifications for debugging client-side handling.
- Verifying that a client application correctly receives and reports back a specific notification.

**Compatibility:** Node.js >= 16.0.0, Koa.js v2.x.

## ❓ Common Questions Quick Index
- **Q: How do I send a test notification?** → [POST /](#post-)
- **Q: How do I confirm a notification was received?** → [PUT /](#put-)
- **Q: What notification types can I test?** → It supports several `DUO_CARPOOL` related types.
- **Q: How are the notification message contents generated?** → A unique debug string is injected into the message body. See [Execution Flow (POST)](#execution-flow-post-createnotification).
- **Q: Why does the `PUT` endpoint check the last 10 messages?** → To provide a reasonable search window for a recently sent notification.
- **Q: What does the `PUT` endpoint actually do?** → It finds the matching notification and updates its database status to "received".
- **Q: Who should use this controller?** → Developers and QA engineers testing the application's notification features.

## 📋 Functionality Overview

**Non-technical explanation:** 
Think of this controller as a **test dummy and sensor system for a car's alert system**. The `POST` endpoint is like a button in the lab that says "Send 'Lane Departure' alert to Test Car #5". This sends a specific, trackable test alert. The `PUT` endpoint is the sensor inside Test Car #5. When the car's computer sees the "Lane Departure" alert on its screen, it sends a signal back to the lab saying, "I can confirm I received the Lane Departure alert with tracking code XYZ." This allows engineers to confirm the entire alert system is working from start to finish.

**Technical explanation:** 
A Koa.js controller with two endpoints designed for debugging the notification service. The `POST` endpoint crafts and sends a push notification of a specific type to a target user ID. It injects a unique debug string into the notification body for tracking. The `PUT` endpoint simulates a client reporting back; it searches the target user's 10 most recent notifications for one matching a specific message body. If found, it updates that notification's status to `NOTIFY_STATUS_RECEIVED` in the database and confirms the match. This provides a closed loop for testing notification delivery and client-side processing.

**Business value explanation:**
A reliable notification system is critical for user engagement and for core functionality like carpooling. This debug controller is a vital internal tool that enables developers and QA teams to rigorously test and validate the notification pipeline without affecting real users or requiring complex manual setups. It significantly speeds up development, improves the reliability of a critical feature, and reduces the risk of notification-related bugs reaching production.

## 🔧 Technical Specifications

- **File:** `allrepo/connectsmart/tsp-api/src/controllers/debug-notification.js`
- **Language:** JavaScript (ES2020)
- **Framework:** Koa.js v2.x with @koa/router
- **Type:** REST API Controller (Internal/Debug Tool)
- **File Size:** ~3 KB
- **Complexity Score:** ⭐⭐⭐ (Medium - Involves specific business logic for different notification types and stateful checks across two endpoints.)

**Dependencies (Criticality Level):**
- `@koa/router`, `koa-bodyparser`: Core routing and body parsing (**Critical**).
- `@app/src/middlewares/auth`: JWT authentication (**Critical**).
- `@app/src/helpers/send-notification`: The core helper function that sends the notification via FCM/APNS (**Critical**).
- `@app/src/models/NotificationUsers`: The database model for user notification records (**Critical**).
- `@app/src/schemas/debug-notification`: Joi schemas for input validation (**Critical**).
- `@app/src/static/defines`: Contains notification type and status constants (**High**).

## 📝 Detailed Code Analysis

### `POST /` (createNotification)
**Execution Flow:**
1.  **Auth & Validation**: The endpoint is authenticated. It validates the request body, expecting a `receiver_user_id` and a `notification_type`.
2.  **Payload Preparation**: It initializes a `notifyData` object, setting the target `userIds` and the `type`.
3.  **Debug String Generation**: It creates a unique `debugStr` by combining the string "DEBUG-", the sender's user ID, and a timestamp. This makes the notification's content uniquely identifiable.
4.  **Content Switching**: A `switch` statement checks the `notification_type`. Based on the type (e.g., `DUO_DRIVER_STARTING_TRIP`, `DUO_CARPOOL_CANCELLED_WITH_REASON`), it populates the `bodyParams` array with the `debugStr` and other required parameters for the message template.
5.  **Error Handling**: If the `notification_type` is not supported by the switch block, `bodyParams` remains empty, and the controller throws a 400 Bad Request error.
6.  **Send Notification**: It calls `await sendNotify(notifyData)`, which triggers the actual push notification to the user's device(s).
7.  **Response**: It returns the `notification_id` generated by the system and the unique `debug_message` string so the client/tester knows what to look for.

### `PUT /` (updateDebugNotification)
**Execution Flow:**
1.  **Auth & Validation**: The endpoint is authenticated. It validates the request body, expecting a `body_message` which should be the unique `debugStr` received from the `POST` call.
2.  **Database Query**: It queries the `NotificationUsers` table (with a join to `notification_msg`) to retrieve the 10 most recent notifications for the authenticated user (`input.userId`).
3.  **Message Matching**: It iterates through the 10 fetched messages.
    - Inside the loop, it compares the `msg_body` from the database with the `body_message` provided in the request.
4.  **Match Found**: If a match is found:
    - It sets `is_match` to `true`.
    - It records the relevant IDs (`notification_id`, `notification_msg_id`, `notification_user_id`).
    - It performs a database `update` on the `NotificationUsers` table, setting the `send_status` to `NOTIFY_STATUS_RECEIVED` for the matched record.
    - It breaks the loop.
5.  **Response**: It returns the `matchData` object, which tells the caller whether a match was found (`is_match: true/false`) and includes the relevant IDs if successful.

## 🚀 Usage Methods

This controller is used in a two-step process for testing.

**Base URL:** `https://api.tsp.example.com/api/v2/debug_notification`
**Headers:**
- `Authorization`: `Bearer <YOUR_JWT_TOKEN>`
- `userid`: `usr_...` (The ID of the user *initiating* the test)
- `Content-Type`: `application/json`

### Step 1: Send a Test Notification
The tester sends a `POST` request to trigger the notification.

```bash
curl -X POST "https://api.tsp.example.com/api/v2/debug_notification" \
  -H "Authorization: Bearer <TOKEN>" \
  -H "userid: qa_user_001" \
  -H "Content-Type: application/json" \
  -d '{
    "receiver_user_id": "target_user_123",
    "notification_type": "DUO_CARPOOL_CANCELLED_IN_NAVIGATION"
  }'
```

**Expected Response from POST:**
```json
{
  "result": "success",
  "data": {
    "notification_id": 12345,
    "debug_message": "DEBUG-qa_user_001-1677610000123" 
  }
}
```
At this point, the `target_user_123` should receive a push notification containing the `debug_message` text.

### Step 2: Confirm Notification Receipt
The test client (or tester), having received the notification, takes the `debug_message` and uses it in the `PUT` request to confirm receipt.

```bash
curl -X PUT "https://api.tsp.example.com/api/v2/debug_notification" \
  -H "Authorization: Bearer <TOKEN>" \
  -H "userid: target_user_123" \
  -H "Content-Type: application/json" \
  -d '{
    "body_message": "DEBUG-qa_user_001-1677610000123"
  }'
```
**Note:** The `userid` in the header for the `PUT` call must be the user who *received* the notification.

**Expected Response from PUT:**
```json
{
  "result": "success",
  "data": {
    "is_match": true,
    "notification_id": 12345,
    "notification_msg_id": 67890,
    "notification_user_id": 99911
  }
}
```
If `is_match` is `true`, the end-to-end test was successful.

## ⚠️ Important Notes
- **Internal Tool**: This controller is not meant for production client use. Access should be limited to test users or internal systems.
- **Stateful Testing**: Unlike most controllers, this one is stateful by design. The `PUT` call's success is dependent on the state created by the `POST` call.
- **Race Conditions**: There is a potential race condition. The `PUT` call might be made before the notification message has been fully written and committed to the database, causing the query to fail to find it. The search window of 10 messages helps mitigate this but doesn't eliminate it.

## 🔗 Related File Links
- **Notification Sending Logic:** `@app/src/helpers/send-notification.js`
- **Database Model:** `@app/src/models/NotificationUsers.js`
- **Input Schemas:** `@app/src/schemas/debug-notification.js`
- **Notification Constants:** `@app/src/static/defines.js`

---
*This documentation was generated to provide a clear guide for developers and QA engineers on how to use this internal tool for testing the notification system.* 