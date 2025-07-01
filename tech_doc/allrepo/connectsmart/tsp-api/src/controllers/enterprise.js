# Enterprise Controller Documentation

## 🔍 Quick Summary (TL;DR)
This controller manages functionality related to enterprise users, including a complex email verification flow for joining corporate carpool groups and CRUD operations for managing user telework (remote work) schedules.

**Keywords:** enterprise | corporate-carpool | email-verification | telework | remote-work | duo-group | employee-verification | corporate-program

**Primary use cases:** 
- Allowing users to join corporate/enterprise carpooling groups by verifying their company email address.
- Handling the entire email verification lifecycle, from sending the email to processing the confirmation link.
- Enabling users to manage and declare their telework/remote work days.
- Providing an administrative endpoint to search for user telework data.

**Compatibility:** Node.js >= 16.0.0, Koa.js v2.x.

## ❓ Common Questions Quick Index
- **Q: How does a user join their company's carpool group?** → By calling `POST /setting_carpool_email`.
- **Q: What is the purpose of the `/verify_carpool_email.html` endpoint?** → This is the endpoint the user clicks in the verification email they receive.
- **Q: What happens if a user's email is already verified?** → The system attempts to add them directly to the carpool group. See [Execution Flow](#execution-flow-post-setting_carpool_email).
- **Q: What is "Telework"?** → It refers to a user's remote work schedule.
- **Q: How do I set my remote work days?** → Use the `POST /telework` endpoint.
- **Q: Can an admin see other users' telework schedules?** → Yes, via the `GET /telework/search` endpoint.
- **Q: What prevents a user from using someone else's verified corporate email?** → The system checks if the email is already assigned to another user ID.
- **Q: Can a user be part of a group through an "invite" even if their email domain doesn't match?** → Yes, the logic explicitly handles invited domains.

## 📋 Functionality Overview

**Non-technical explanation:** 
Think of this controller as the **Corporate Benefits Administrator** for our transportation app.
1.  **Joining the Corporate Carpool Club (`/setting_carpool_email`):** To join your company's exclusive carpool group, you must prove you're an employee. You provide your work email. The administrator first checks its records. If you're already a known, verified employee, you're added to the group immediately. If not, the administrator sends a confirmation link to your work email.
2.  **Clicking the Confirmation Link (`/verify_carpool_email.html`):** When you click the link in your email, you're brought to the administrator's desk. They see the special code on your link, mark you as a verified employee in their files, and officially add you to the carpool group.
3.  **Managing Remote Work (`/telework`):** This administrator also keeps track of your remote work schedule. You can tell them which days you'll be working from home (`POST /telework`), and they'll keep it on file for you (`GET /telework`). Your manager can also ask the administrator for a list of everyone's remote work days (`GET /telework/search`).

**Technical explanation:** 
A Koa.js controller with two main functional areas. The first is a complex, multi-step business logic flow for enterprise email verification, initiated by `POST /setting_carpool_email` and completed by `GET /verify_carpool_email.html`. This flow interacts with multiple database tables (`Enterprises`, `DuoGroups`, `EnterpriseInvites`, `EnterpriseBlocks`) to validate a user's eligibility, check for blockages or duplicate usage, and either directly adds them to a carpool group or sends a verification email. The second area provides simple CRUD-like endpoints for managing user telework schedules, abstracting the logic into a service layer.

**Business value explanation:**
This controller is the gateway for corporate partnerships and programs. The email verification flow is critical for securely limiting access to enterprise-sponsored carpool groups, a key feature for B2B offerings. The telework functionality supports modern hybrid work models, enabling smarter trip planning and providing valuable data for corporate partners to understand their employees' commuting patterns, which can inform transportation demand management strategies and sustainability reporting.

## 🔧 Technical Specifications

- **File:** `allrepo/connectsmart/tsp-api/src/controllers/enterprise.js`
- **Language:** JavaScript (ES2020)
- **Framework:** Koa.js v2.x with @koa/router
- **Type:** REST API Controller
- **File Size:** ~7 KB
- **Complexity Score:** ⭐⭐⭐⭐ (High - The email verification endpoint contains very complex, stateful business logic.)

**Dependencies (Criticality Level):**
- `@koa/router`, `koa-bodyparser`: Core routing and body parsing (**Critical**).
- `@app/src/middlewares/auth`: JWT authentication (**Critical**).
- `@app/src/services/enterprise`: The service layer containing all business logic (**Critical**).
- Multiple DB Models (`DuoGroups`, `Enterprises`, etc.): For direct database queries within the controller (**Critical**).
- `@app/src/static/error-code`: Static error code definitions (**High**).
- `@app/src/schemas/enterprise`: Joi schemas for input validation (**Critical**).

## 📝 Detailed Code Analysis

### `POST /setting_carpool_email`
This is by far the most complex endpoint in the controller.
**Execution Flow:**
1.  **Validation**: Validates input `email`, `verify_type`, `group_id`, etc.
2.  **Enterprise ID Lookup**: It first tries to find a matching enterprise ID based on the email's domain (e.g., `user@company.com` -> `company.com`).
3.  **Invite Check**: It then checks the `EnterpriseInvites` table to see if the user was explicitly invited, which might be for a different enterprise ID than their email domain suggests. Both enterprise IDs are collected.
4.  **Carpool Group Validation**: If the `verifyType` is `carpool`, it performs a critical check:
    - It finds all `DuoGroups` associated with the collected enterprise IDs.
    - It confirms that the `groupId` the user wants to join actually exists and belongs to one of those enterprises.
    - If no valid group is found, it throws a `403 Forbidden` error.
5.  **Existing Employee Check**: It checks the `Enterprises` table to see if this email has already been successfully verified (`email_verify_token: 'success'`).
    - **Crucially**, it also checks if that verified email belongs to a *different* user (`employee.user_id !== userId`). If so, it throws a `400 Bad Request` (duplicate email) error. This prevents account takeovers.
6.  **Blocklist Check**: It checks the `EnterpriseBlocks` table to see if the email has been explicitly blocked for that enterprise, throwing a `403` if it has.
7.  **Decision Point**:
    - **If Already Verified**: If the email is already verified for the correct user and enterprise, the controller calls `joinEnterpriseGroup` directly, adding the user to the group without sending an email.
    - **If Not Verified**: It calls `sendResponseMail`, which generates a unique verification token, saves it to the database, and sends the user an email containing the confirmation link.
8.  **Response**: Returns a generic success response. The client must wait for the email.

### `GET /verify_carpool_email.html`
**Execution Flow:**
1.  **Validation**: Validates the `verify_token` from the query string.
2.  **Service Delegation**: It passes the token to the `verifyEmail` service function. This service handles all the logic: finding the token in the database, updating the user's/enterprise's status to verified, adding them to the carpool group, and generating an HTML page to render as a response.
3.  **Response**: The controller's body is set to the HTML returned by the service, which is then rendered in the user's browser.

### Telework Endpoints (`/telework`, `/telework/search`)
These endpoints are standard, straightforward CRUD operations that follow the clean pattern seen in other controllers: validate input, call the corresponding service function (`getTelework`, `updateTelework`, `searchTelework`), and return the result.

## 🚀 Usage Methods

### Initiating Corporate Email Verification
```bash
curl -X POST "https://api.tsp.example.com/api/v1/setting_carpool_email" \
  -H "Authorization: Bearer <TOKEN>" -H "userid: usr_123" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test.user@company.com",
    "verify_type": "carpool",
    "group_id": 567
  }'
```
**Result:** HTTP 200 OK. The user `test.user@company.com` receives an email.

### Clicking the Verification Link
The user clicks a link in their email that looks like:
`https://api.tsp.example.com/api/v1/verify_carpool_email.html?verify_token=a1b2c3d4e5f6...`
**Result:** The browser displays a success or failure HTML page. The user is now verified.

### Updating Telework Schedule
```bash
curl -X POST "https://api.tsp.example.com/api/v1/telework" \
  -H "Authorization: Bearer <TOKEN>" -H "userid: usr_123" \
  -H "Content-Type: application/json" \
  -d '{
    "schedules": [
      { "week": 1, "day": 1, "telework": true },
      { "week": 1, "day": 2, "telework": true }
    ]
  }'
```
**Result:** HTTP 200 OK with the updated telework schedule.

## ⚠️ Important Notes
- **Controller Complexity**: Unlike most other controllers in this system, the `sendVerifyEmail` endpoint contains a significant amount of business and validation logic directly within the controller instead of abstracting it to the service layer. This makes it powerful but also more complex to maintain.
- **Security**: The email verification flow is a critical security boundary. The checks against duplicate email usage and the blocklist are essential for preventing unauthorized access to corporate groups.
- **HTML Response**: The `/verify_carpool_email.html` endpoint is unusual for a JSON API as it returns an HTML document. This is a common pattern for email verification links that are opened in a browser.

## 🔗 Related File Links
- **Core Logic:** `allrepo/connectsmart/tsp-api/src/services/enterprise.js`
- **Input Schemas:** `allrepo/connectsmart/tsp-api/src/schemas/enterprise.js`
- **Database Models:** `DuoGroups`, `Enterprises`, `AuthUsers`, `EnterpriseInvites`, `EnterpriseBlocks`.

---
*This documentation was generated to clarify the complex enterprise verification flow and the separate telework management functionality contained within this controller.* 