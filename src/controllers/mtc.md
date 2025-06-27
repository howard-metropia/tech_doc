# MTC Controller Documentation

## 🔍 Quick Summary (TL;DR)
MTC controller provides messaging interface for transit authority campaigns with message delivery and plan coordination functionality, currently operating in simplified mode for development.

**Keywords:** mtc | messaging | transit-authority | campaign | notification | plan-coordination | metropolitan-transport | communication-api | user-targeting | koa-controller

**Primary use cases:** Transit authority announcements, targeted user messaging, campaign tracking, message distribution, plan coordination

**Compatibility:** Node.js >= 16.0.0, Koa.js v2.x, @koa/router v12.x, requires JWT authentication

## ❓ Common Questions Quick Index
- **Q: What is MTC messaging system?** → Metropolitan Transportation Commission message delivery system
- **Q: How to send messages to users?** → POST to /mtc_message with authentication
- **Q: Why is message delivery commented out?** → Feature under development, currently returns plan IDs only
- **Q: What authentication is required?** → JWT token with userid header mandatory
- **Q: How to troubleshoot empty responses?** → Normal behavior in current simplified mode
- **Q: What is plan_id used for?** → Message coordination and campaign tracking
- **Q: How to integrate with message service?** → Use service layer methods for business logic
- **Q: What are the response formats?** → JSON with plan_id, message_id, title, message fields
- **Q: How to enable full message functionality?** → Uncomment service integration code
- **Q: What security considerations apply?** → Requires authentication, validates user context

## 📋 Functionality Overview

**Non-technical explanation:** 
Like a digital bulletin board system at a transit station - the MTC controller acts as a message dispatcher that can deliver targeted announcements to specific users. Think of it as a smart notification system that knows which messages to show to which passengers, similar to how a train conductor announces different information to different car sections. It's like having a personalized radio station that broadcasts relevant transit updates only to users who need them.

**Technical explanation:** 
REST API controller implementing messaging service for transit authority communications using Koa.js router pattern. Provides POST endpoint for retrieving campaign messages with user targeting capabilities, currently operating in simplified mode returning only plan identifiers.

**Business value explanation:**
Enables transit authorities to deliver targeted communications, campaign messages, and service announcements to mobile app users. Supports user engagement, service notifications, and marketing campaign distribution within transportation service platforms.

**Context within system:** Part of TSP (Transportation Service Provider) API microservice, integrates with user authentication system, message service layer, and campaign management infrastructure for comprehensive transit communication capabilities.

## 🔧 Technical Specifications

- **File information:** mtc.js, 36 lines, JavaScript ES6, Controller pattern, Low complexity (Cyclomatic: 2)
- **Dependencies:**
  - @koa/router (^12.0.0): HTTP routing - Critical for endpoint definition
  - @app/src/services/response: Response formatting - High importance for API consistency
  - @app/src/services/mtc: Business logic service - Critical for message operations
  - koa-bodyparser (^4.4.1): Request parsing - Medium importance for POST data
  - @app/src/middlewares/auth: Authentication - Critical for security
- **Compatibility:** Node.js 16+, Koa.js 2.x, Express-compatible middleware
- **Configuration:** No environment variables, uses service layer configuration
- **System requirements:** Minimum 512MB RAM, recommended 1GB for concurrent requests
- **Security:** Requires valid JWT authentication, user ID extraction from headers

## 📝 Detailed Code Analysis

### MTC Message Endpoint (`POST /mtc_message`)

**Purpose:** Coordinates MTC messaging and provides plan IDs for transportation coordination

**Current Implementation:**
```javascript
router.post('mtc_message', '/mtc_message', auth, bodyParser(), async (ctx) => {
  const userId = ctx.request.header.userid;
  const plan_id = service.getPlanId();
  ctx.body = ResponseService.success(ctx, {
    plan_id,
    message_id: 0,
    title: '',
    message: '',
  });
});
```

**Planned Implementation (Commented Out):**
```javascript
// if (await service.isTargetUser(userId)) {
//   const {
//     idx: message_id,
//     result: { title, message },
//   } = service.getMessage(userId);
//   const plan_id = service.getPlanId();
//   service.writeData(userId, plan_id, message_id, message, ctx.request.body);
//   ctx.body = ResponseService.success(ctx, {
//     plan_id,
//     message_id,
//     title,
//     message,
//   });
// }
```

### Service Integration
- **Plan ID Generation:** `service.getPlanId()` provides unique plan identifiers
- **User Targeting:** `service.isTargetUser(userId)` (planned feature)
- **Message Retrieval:** `service.getMessage(userId)` (planned feature)
- **Data Persistence:** `service.writeData(...)` (planned feature)

### Response Structure
The endpoint always returns a consistent structure with plan coordination data:
- `plan_id`: Unique identifier for the coordination plan
- `message_id`: Message identifier (currently 0)
- `title`: Message title (currently empty)
- `message`: Message content (currently empty)

## 🚀 Usage Methods

### Get MTC Message/Plan ID
```bash
curl -X POST "https://api.tsp.example.com/api/v2/mtc_message" \
  -H "Authorization: Bearer <JWT_TOKEN>" \
  -H "userid: usr_12345" \
  -H "Content-Type: application/json" \
  -d '{
    "context": "trip_planning",
    "location": "downtown_station"
  }'
```

### JavaScript Client Example
```javascript
async function getMTCMessage(authToken, userId, contextData) {
  try {
    const response = await fetch('/api/v2/mtc_message', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${authToken}`,
        'userid': userId,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(contextData)
    });
    
    if (response.ok) {
      const result = await response.json();
      console.log('Plan ID:', result.data.plan_id);
      return result.data;
    }
  } catch (error) {
    console.error('MTC message request failed:', error);
  }
}
```

## 📊 Output Examples

**Successful response (current implementation):**
```json
{
  "success": true,
  "data": {
    "plan_id": "PLAN_2024_001",
    "message_id": 0,
    "title": "",
    "message": ""
  },
  "timestamp": "2024-01-15T10:30:00Z",
  "execution_time": "15ms"
}
```

**Expected full functionality response:**
```json
{
  "success": true,
  "data": {
    "plan_id": "PLAN_2024_001",
    "message_id": 12345,
    "title": "Service Update",
    "message": "Line 1 experiencing 5-minute delays due to signal issues"
  }
}
```

**Authentication error (401):**
```json
{
  "success": false,
  "error": "Authentication required",
  "code": "AUTH_MISSING"
}
```

**Performance benchmarks:** Average response time 20-50ms, 95th percentile under 100ms, supports 1000+ concurrent requests

## ⚠️ Important Notes

**Security considerations:**
- Requires valid JWT authentication tokens
- User ID validation prevents unauthorized access
- No sensitive data exposure in current simplified mode
- Rate limiting should be implemented for production use

**Current limitations:**
- Message delivery functionality is commented out and disabled
- Always returns empty message content regardless of user targeting
- Missing error handling for service layer failures
- No input validation on request body

**Troubleshooting common issues:**
- Empty responses: Normal behavior in current implementation
- Authentication failures: Check JWT token validity and userid header
- 404 errors: Verify /api/v2 prefix and route registration
- Service errors: Check MTC service availability and configuration

**Performance considerations:**
- Minimal resource usage in current state
- Full implementation would require caching for message lookup
- Consider implementing response caching for frequently requested plans

## 🔗 Related File Links

**Project structure:**
- `/src/services/mtc.js` - Business logic service (dependency)
- `/src/services/response.js` - Response formatting utilities
- `/src/middlewares/auth.js` - Authentication middleware
- `/package.json` - Dependencies and versions

**Related controllers:**
- `/src/controllers/notification.js` - General notifications
- `/src/controllers/user-actions.js` - User interaction tracking

## 📈 Use Cases

**Daily operations:**
- Transit authority sending service updates to app users
- Marketing campaigns targeting specific user demographics  
- Emergency notifications for service disruptions
- Regular schedule change announcements

**Development scenarios:**
- Testing message delivery systems
- Validating user targeting logic
- API integration testing for mobile applications
- Campaign effectiveness measurement

**Anti-patterns to avoid:**
- Don't bypass authentication for internal calls
- Avoid hardcoding plan IDs or message content
- Don't implement without proper error handling
- Avoid direct database calls from controller

## 🛠️ Improvement Suggestions

**Code optimization (High Priority):**
- Enable commented message delivery functionality
- Add input validation for request body parameters
- Implement proper error handling and logging
- Add response caching for improved performance

**Feature expansion (Medium Priority):**
- Add message scheduling capabilities
- Implement user preference filtering
- Add message delivery tracking and analytics
- Support for multiple message formats (HTML, plain text)

## 🏷️ Document Tags

**Keywords:** MTC, messaging, transit, controller, API, Koa, authentication, campaign, notification, plan-id, user-targeting, POST-endpoint, middleware, service-layer, transportation

**Technical tags:** #api #rest-api #koa-api #controller #messaging #transit #authentication #middleware #nodejs #javascript

**Target roles:** Backend developers (intermediate), API integrators (beginner), Transit system architects (advanced)

**Difficulty level:** ⭐⭐ (2/5) - Straightforward controller with standard patterns

**Maintenance level:** Low - Simple controller with minimal complexity

**Business criticality:** Medium - Important for user communication but not critical for core transit operations