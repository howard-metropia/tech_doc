# Notifications Controller Documentation

## 🔍 Quick Summary (TL;DR)
This controller is responsible for fetching a user's notification history (the "inbox") and for updating the status of a notification (e.g., marking it as "received" or "replied").

**Keywords:** notifications | push-notification | notification-inbox | message-center | user-alerts | tsp-api | notification-status

**Primary use cases:** 
- Populating the notification center/inbox screen in the client application.
- Allowing clients to filter notifications by status, type, or category (e.g., "incentive").
- Marking a notification as received after the client has processed it.
- Handling special notification interaction logic, such as for DUO carpool broadcasts.

**Compatibility:** Node.js >= 16.0.0, Koa.js v2.x.

## ❓ Common Questions Quick Index
- **Q: How do I get a user's notification list?** → [GET /notification](#get-notification)
- **Q: How do I mark a notification as read/received?** → [PUT /notification_receive/:id](#put-notification_receiveid)
- **Q: Can I get only unread notifications?** → Yes, use the `status` query parameter.
- **Q: Can I get only incentive-related notifications?** → Yes, use the `category=incentive` query parameter.
- **Q: What does the `PUT` endpoint do?** → It updates the `send_status` of a specific user notification record.
- **Q: Why are some notification types excluded from the list?** → To prevent system-level or non-displayable notifications (like microsurveys) from appearing in the user's inbox.
- **Q: How does pagination work?** → Using `offset` and `perpage` query parameters. The response includes `total_count` and `next_offset`.

## 📋 Functionality Overview

**Non-technical explanation:** 
Think of this controller as your **personal mail carrier and secretary**.
- **Fetching Your Mail (`GET /notification`):** You can ask the mail carrier for your mail. You can be specific: "Just show me my unread mail" (`status=0`), or "Only show me letters about my reward points" (`category=incentive`). The mail carrier will give you a stack of letters (`notifications`), tell you how many letters you have in total (`total_count`), and tell you where to start counting for the next stack (`next_offset`).
- **Processing Mail (`PUT /notification_receive/:id`):** When you receive a specific letter, your secretary (the client app) calls the mail carrier and says, "We've officially received letter #123." The mail carrier then makes a note in their records, marking that letter as "received." For very important letters (like a DUO carpool request), they might mark it as "replied" to show a stronger interaction.

**Technical explanation:** 
A Koa.js controller with two primary endpoints for managing the user-facing notification lifecycle. The `GET /notification` endpoint builds and executes a complex Knex query against multiple tables (`notification_user`, `notification_msg`, `notification`) to retrieve a paginated and filtered list of a user's notifications. It supports filtering by `status`, `type`, and a special `category`. It also explicitly excludes certain system-level notification types. The `PUT /notification_receive/:id` endpoint updates the `send_status` of a single `notification_user` record, effectively changing its state from "sent" to "received" or another status provided in the request body.

**Business value explanation:**
This controller provides the essential backend functionality for a rich, interactive notification inbox within the application. A reliable and filterable notification center is crucial for user engagement, allowing users to review important alerts, offers, and system messages they may have missed. The status update mechanism is key for tracking user interaction and ensuring that time-sensitive alerts (like carpool requests) are correctly processed and acknowledged, which is vital for the functionality of features like DUO.

## 🔧 Technical Specifications

- **File:** `allrepo/connectsmart/tsp-api/src/controllers/notifications.js`
- **Language:** JavaScript (ES2020)
- **Framework:** Koa.js v2.x with @koa/router
- **Type:** REST API Controller
- **File Size:** ~6 KB
- **Complexity Score:** ⭐⭐⭐⭐ (High - The `GET` endpoint involves a complex, multi-join Knex query with dynamic filtering.)

**Dependencies (Criticality Level):**
- `moment-timezone`: Date and time manipulation (**High**).
- `knex`: Used directly for building complex SQL queries (**Critical**).
- `@koa/router`, `koa-bodyparser`: Core routing and body parsing (**Critical**).
- `@app/src/middlewares/auth`: JWT authentication middleware (**Critical**).
- DB Models (`Notifications`, `NotificationMsgs`, `NotificationUsers`): Used for `PUT` endpoint logic (**Critical**).
- `@app/src/static/defines`: Contains critical constants for notification types and statuses (**Critical**).
- `@app/src/schemas/notifications`: Joi schemas for input validation (**Critical**).

## 📝 Detailed Code Analysis

### `GET /notification`
This is a complex read endpoint.
**Execution Flow:**
1.  **Validation**: Validates query parameters, including `offset`, `perpage`, `userId`, `status`, `type`, and `category`.
2.  **Filter Preparation**: It parses the comma-separated `status` and `type` strings into arrays of integers. It also checks for the special `category` filter and, if present, overrides the `notificationTypes` array with the relevant constants.
3.  **Count Query**: It builds and executes a Knex query to get the `total_count` of notifications matching the filters. This is done first to enable pagination logic. The query involves:
    - Joining three tables.
    - Filtering by `userId` and `sendStatus`.
    - Filtering out notifications that have expired (`ended_on`).
    - Explicitly excluding certain system-level types (`MICROSURVEY_*`).
    - Filtering by `notificationTypes` if provided.
    - Filtering out incentive types if the category is not 'incentive'.
4.  **Pagination Logic**: It calculates the `next_offset` based on the current offset, per-page count, and the total count.
5.  **Data Query**: It executes a second, nearly identical Knex query, but this time it includes `orderBy`, `offset`, and `limit` to fetch the actual data for the current page.
6.  **Response Formatting**: It maps over the `rows` returned from the database, transforming each row into a clean `notification` object for the client. This includes parsing a JSON string in `msg_data` into an object.
7.  **Final Response**: It returns a structured object containing `total_count`, `next_offset`, and the `notifications` array.

### `PUT /notification_receive/:id`
**Execution Flow:**
1.  **Validation**: Validates the notification `id` from the URL, `userId` from the header, and `status` from the body.
2.  **Data Fetching**: It performs a series of queries to ensure the entities exist:
    - Fetches the parent `notification` by `id`.
    - Fetches the `notification_msg` associated with that notification.
    - Fetches the specific `notification_user` record linking the message to the user.
3.  **Existence Checks**: If any of these are not found, it throws a `404 Not Found` error.
4.  **Special Case Logic**: It checks if the notification is a `DUO_CARPOOL_RIDER_REQUEST_BROADCASTING_TO_DRIVER` type. If it is, and the incoming status is "received," it overrides the status to "replied," handling a specific business rule for that flow.
5.  **Database Update**: It calls `.update({ send_status: status })` on the fetched `userSent` model instance, which updates the record in the database.
6.  **Response**: Returns a generic success response.

## 🚀 Usage Methods

**Base URL:** `https://api.tsp.example.com/api/v1`
**Headers:** All requests require `Authorization: Bearer <TOKEN>` and `userid: usr_...`

### Get First Page of Notifications
```bash
curl -X GET "https://api.tsp.example.com/api/v1/notification?offset=0&perpage=10" \
  -H "Authorization: Bearer <TOKEN>" \
  -H "userid: usr_123"
```

### Get Unread Incentive Notifications
```bash
curl -X GET "https://api.tsp.example.com/api/v1/notification?offset=0&perpage=10&status=0&category=incentive" \
  -H "Authorization: Bearer <TOKEN>" \
  -H "userid: usr_123"
```

### Mark a Notification as Received
```bash
curl -X PUT "https://api.tsp.example.com/api/v1/notification_receive/12345" \
  -H "Authorization: Bearer <TOKEN>" \
  -H "userid: usr_123" \
  -H "Content-Type: application/json" \
  -d '{
    "status": 2
  }'
```

## ⚠️ Important Notes
- **Complex Queries**: The `GET` endpoint relies on complex, manually written Knex queries. Any changes to the database schema or filtering logic require careful modification of these queries.
- **Performance**: Fetching the `total_count` with a separate query before fetching the data is a standard pagination pattern that is generally efficient. However, for very large tables, the `COUNT` query itself could become slow.
- **Constants**: The logic is tightly coupled to numeric constants defined in `defines.js` for notification types and statuses. Understanding these constants is essential to understanding the controller's behavior.

## 🔗 Related File Links
- **Database Query Builder:** `knex` (npm module)
- **Database Models:** `Notifications`, `NotificationMsgs`, `NotificationUsers`
- **Input Schemas:** `@app/src/schemas/notifications.js`
- **Constants:** `@app/src/static/defines.js`

---
*This documentation was regenerated to provide a detailed analysis of the complex notification retrieval logic and the status update mechanism.*
