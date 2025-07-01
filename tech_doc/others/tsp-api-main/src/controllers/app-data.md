# TSP API App-Data Controller Documentation

## 🔍 Quick Summary (TL;DR)
The `app-data` controller provides a secure endpoint for client applications to submit user-specific data, such as logs or analytics events, to the TSP API for backend processing. It acts as a fire-and-forget data ingestion point.

**Keywords:** app-data | user-data | analytics | logging | mobile-data | tsp-api | data-submission | REST-endpoint | koa-router | client-events | telemetry | event-tracking

**Primary use cases:** 
- Client-side event logging for user behavior analysis.
- User application state synchronization.
- Remote diagnostics and error data submission from mobile apps.
- Capturing user interaction data for feature improvement.

**Compatibility:** Node.js >= 16.0.0, Koa.js v2.x, @koa/router v10.x

## ❓ Common Questions Quick Index
- **Q: How do I send data to this endpoint?** → [Basic cURL Usage](#basic-curl-usage)
- **Q: What authentication is required to use this API?** → [Authentication and Authorization](#authentication-and-authorization)
- **Q: What are the mandatory HTTP headers?** → [Header Requirements](#header-requirements)
- **Q: What happens to the data I send? Where does it go?** → [Service Layer Integration](#service-layer-integration)
- **Q: What is the expected response on a successful submission?** → [Successful Response](#successful-response)
- **Q: Why am I getting a 401 Unauthorized error?** → [Troubleshooting Guide](#troubleshooting-guide)
- **Q: Is there any validation on the data payload I send?** → [Input Validation](#input-validation)
- **Q: How is the timezone handled for submitted data?** → [Execution Flow Analysis](#execution-flow-analysis)
- **Q: Can I send any JSON structure?** → [Data Schema](#data-schema)
- **Q: What is the performance impact of calling this endpoint frequently?** → [Performance Considerations](#performance-considerations)

## 📋 Functionality Overview

**Non-technical explanation:** 
Think of this controller as a secure digital **suggestion box** or a **mail drop-off point**. A mobile app can "drop off" packages of information (like user activity logs, feedback, or diagnostic reports). This controller acts as the trusted receptionist who only accepts packages from authenticated users (by checking their ID badge), notes down who sent it and when, and then passes the package to the back office (the service layer) for processing. The sender simply gets a receipt confirming the package was received, not details about what was done with it afterward.

**Technical explanation:** 
A minimalist Koa.js REST controller that exposes a single `POST /api/v2/appdata` endpoint. It leverages middleware for its core functionality: `@app/src/middlewares/auth` for JWT-based user authentication and `koa-bodyparser` for parsing the incoming JSON payload. The controller extracts user context (`userId`, `zone`) from the request headers and the entire request body, passing them to the `app-data` service layer for asynchronous processing. It then immediately returns a generic HTTP 200 success response, decoupling the client from the backend processing outcome.

**Business value explanation:**
This endpoint is a critical component for data-driven product development and operational support. It enables the collection of valuable client-side data, providing rich insights into user behavior, feature usage patterns, and application performance in the wild. This data is fundamental for making informed decisions to enhance user experience, for debugging client-side issues without direct user intervention, and for proactive problem-solving.

## 🔧 Technical Specifications

- **File:** `allrepo/connectsmart/tsp-api/src/controllers/app-data.js`
- **Language:** JavaScript (ES2020)
- **Framework:** Koa.js v2.x with @koa/router
- **Type:** REST API Controller
- **File Size:** ~0.8 KB
- **Complexity Score:** ⭐ (Low - A single endpoint where the core logic is delegated to middleware and services)

**Dependencies (Criticality Level):**
- `@koa/router`: HTTP routing framework (**Critical**)
- `koa-bodyparser`: Request body parsing middleware (**Critical**)
- `@maas/core/response`: Standardized success/error response formatting utility (**High**)
- `@maas/core/log`: Centralized logging utility for observability (**High**)
- `@app/src/middlewares/auth`: JWT authentication and user session middleware (**Critical**)
- `@app/src/services/app-data`: The business logic service layer that processes the submitted data (**Critical**)

**Security Requirements:**
- **Authentication:** A valid user-specific JSON Web Token (JWT) is mandatory for all requests.
- **Transport Security:** HTTPS must be enforced in production environments to protect the integrity and confidentiality of the submitted data and authentication tokens.
- **Data Handling:** The request body can contain sensitive user activity data and must be handled securely by the downstream `app-data` service.

## 📝 Detailed Code Analysis

### Main Route Definition

**`POST /appdata` Endpoint Signature:**
```javascript
router.post(
  'postAppData',           // Route Name
  '/appdata',              // Path
  auth,                    // Authentication Middleware
  bodyParser(),            // Body Parsing Middleware
  async (ctx) => { ... }   // Handler
)
```

**Parameters:**
- `ctx.request.header`: Must contain a valid `Authorization` bearer token and a `userid`. The `zone` header is optional.
- `ctx.request.body`: A JSON object of any structure, representing the data being sent by the client application.
- **Returns:** A generic success object, confirming receipt: `{ "result": "success", "data": {} }`.
- **Throws:** An `AuthenticationError` if the `auth` middleware fails due to an invalid or missing token. It may also propagate a `ServiceError` if the `app-data` service layer throws an unhandled exception.

### Execution Flow Analysis

1.  **Request Ingress**: A `POST` request to `/api/v2/appdata` is received by the Koa.js server.
2.  **Routing**: The `@koa/router` matches the path and method, triggering the associated middleware chain.
3.  **Authentication**: The `auth` middleware is executed first. It inspects the `Authorization` header, validates the JWT, and attaches user information to the context. If the token is invalid, missing, or expired, the middleware rejects the request with a `401 Unauthorized` error, and the handler is never reached.
4.  **Body Parsing**: The `koa-bodyparser` middleware parses the incoming request body (expected to be JSON), making it available on `ctx.request.body`.
5.  **Handler Execution**: The main asynchronous handler function is executed.
    - It logs the received request body for debugging and monitoring purposes using `logger.info`.
    - It extracts the `userId` from the `ctx.request.header.userid`.
    - It extracts the `zone` (IANA timezone format) from `ctx.request.header.zone`, providing a default value of `'America/Chicago'` if it's not supplied.
    - It delegates the core business logic by calling `await service.writeAppData(...)`, passing an object containing the request body, userId, and zone.
    - **Crucially**, the controller does not wait for a meaningful result from the service. It immediately sends back a generic success response using `ctx.body = success({})`. This signifies that the data was received successfully, not that it was fully processed.
6.  **Response**: The client receives an HTTP 200 OK status with the standard success payload.

### Input Validation
This controller does **not** perform any explicit validation on the `ctx.request.body`'s schema. The commented-out line `// const inputValidator = require('@app/src/schemas/app-version');` suggests that validation was considered but ultimately omitted at this layer. The responsibility for validating the structure and content of the submitted data is delegated entirely to the downstream `app-data` service. This design choice keeps the controller lightweight and focused on its primary roles of routing and authentication.

## 🚀 Usage Methods

### Basic cURL Usage
This example demonstrates sending a simple log event object to the endpoint.

```bash
# Replace <YOUR_JWT_TOKEN> with a valid user token
# The 'userid' header must correspond to the user in the token

curl -X POST "https://api.tsp.example.com/api/v2/appdata" \
  -H "Authorization: Bearer <YOUR_JWT_TOKEN>" \
  -H "userid: usr_7f8a9b2c1d3e4f5g" \
  -H "zone: America/New_York" \
  -H "Content-Type: application/json" \
  -d '{
    "eventType": "button_click",
    "eventDetails": {
      "buttonId": "confirm_purchase",
      "pageUrl": "/checkout",
      "sessionId": "session_xyz_123"
    },
    "timestamp": "2024-06-25T10:00:00Z"
  }'
```

### Header Requirements
- `Authorization`: (Required) The Bearer token for authentication. Example: `Bearer eyJhbGci...`
- `userid`: (Required) The public identifier of the user sending the data. This is used for data attribution. Example: `usr_...`
- `zone`: (Optional) The IANA time zone of the user, used for correct timestamp interpretation. Defaults to `America/Chicago`. Example: `America/Los_Angeles`

## 📊 Output Examples

### Successful Response
A successful request will always receive an HTTP 200 OK status code and this generic body, which serves as an acknowledgment of receipt.

```json
{
  "result": "success",
  "data": {}
}
```

### Authentication Error Response (401)
If the `Authorization` token is missing, expired, or invalid, the `auth` middleware will intercept the request and respond with an error similar to this:

```json
{
  "error": "AuthenticationError",
  "message": "Invalid or expired JWT token. Please re-authenticate.",
  "code": "AUTH_TOKEN_INVALID"
}
```

## ⚠️ Important Notes

### Asynchronous Processing (Fire-and-Forget)
The controller is designed to be highly responsive. It returns a success response as soon as it hands off the data to the service layer, without waiting for the actual data processing to complete. This "fire-and-forget" pattern means the client is only notified of receipt, not of final processing status. Any errors that occur during the processing within the `app-data` service must be handled asynchronously (e.g., through server-side monitoring, logging, and potentially a dead-letter queue).

### Data Schema
The controller accepts any valid JSON in the request body. The structure and schema of this data represent a contract between the client application and the `app-data` service, and this contract is not enforced at the controller level. Developers must ensure that clients send data in the format expected by the service.

### Performance Considerations
Since the controller does not wait for the service layer, its response time is very fast, primarily determined by network latency and the speed of the authentication middleware. This makes it suitable for high-frequency event logging from clients without impacting the user's perceived application performance.

### Troubleshooting Guide

1.  **Symptom: Getting a 401 Unauthorized error.**
    *   **Diagnosis:** The JWT in the `Authorization` header is either missing, malformed, or has expired.
    -   **Solution:** Ensure a valid, non-expired Bearer token is being included in the request header. Verify that the `userid` header is also present and corresponds to the authenticated user.

2.  **Symptom: The request succeeds (200 OK) but the data is not appearing in the backend systems (e.g., analytics dashboard).**
    *   **Diagnosis:** The controller successfully received the data, but an error occurred asynchronously within the `app-data` service during processing.
    *   **Solution:** This is not a controller issue. Check the server-side logs for errors related to the `app-data` service, filtering by the `userId`. The error could be due to malformed data, database connectivity issues, or other downstream problems.

## 🔗 Related File Links

- **Authentication Middleware:** `allrepo/connectsmart/tsp-api/src/middlewares/auth.js` (*The controller depends on this middleware for security and user context.*)
- **Business Logic Service:** `allrepo/connectsmart/tsp-api/src/services/app-data.js` (*The controller delegates all data processing tasks to this service.*)
- **Response Formatter:** `@maas/core/response` (*Provides the standard `success` function for generating consistent API responses.*)
- **Logging Utility:** `@maas/core/log` (*Provides the `logger` used for logging request information.*)

---
*This documentation was regenerated to provide more comprehensive details and context, based on the provided template and source file analysis.*
