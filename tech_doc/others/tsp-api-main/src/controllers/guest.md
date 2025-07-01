# TSP API Guest Controller Documentation

## 🔍 Quick Summary (TL;DR)
The guest controller provides authentication functionality for guest users who want to access TSP services without creating a full account, enabling temporary or trial access to platform features.

**Keywords:** guest-login | temporary-access | trial-authentication | anonymous-users | quick-access | guest-mode | lightweight-auth

**Primary use cases:** Trial app usage, temporary access, anonymous user authentication, quick onboarding without registration

**Compatibility:** Node.js >= 16.0.0, Koa.js v2.x, @koa/router v10.x

## ❓ Common Questions Quick Index
- **Q: How do guests authenticate without an account?** → [Guest Login Process](#guest-login-process)
- **Q: What credentials are needed for guest login?** → Minimal data validation through guest schema
- **Q: Do guest tokens expire?** → Yes, managed by service layer with shorter lifespans
- **Q: What services can guests access?** → Limited subset of platform features
- **Q: How is guest data handled?** → Temporary storage with privacy protection
- **Q: Can guests upgrade to full accounts?** → Through separate registration endpoints

## 📋 Functionality Overview

**Non-technical explanation:** 
Think of this as a **"try before you buy" entrance** to a premium service. Like how some stores let you browse or test products without signing up for a membership card, this controller lets people use basic transportation features without going through the full registration process. They get a temporary pass (token) that gives them limited access.

**Technical explanation:** 
A minimal Koa.js controller that handles guest authentication by validating basic input data and delegating to the guest service layer for token generation. It provides a lightweight authentication pathway for users who need immediate access without full account creation.

**Business value explanation:**
Reduces friction for new users by eliminating registration barriers, potentially increasing user acquisition and allowing people to experience platform value before committing to full registration. Critical for trial usage and user onboarding funnels.

## 🔧 Technical Specifications

- **File:** `allrepo/connectsmart/tsp-api/src/controllers/guest.js`
- **Language:** JavaScript (ES2020)
- **Framework:** Koa.js v2.x with @koa/router
- **Type:** Authentication Controller
- **File Size:** ~0.7 KB
- **Complexity Score:** ⭐ (Low - Single endpoint with basic validation and service delegation)

**Dependencies:**
- `@koa/router`: HTTP routing framework (**Critical**)
- `koa-bodyparser`: Request body parsing (**Critical**)
- `@maas/core/response`: Standardized response formatting (**High**)
- `@maas/core`: Core framework with MaasError (**Critical**)
- `@app/src/services/guest`: Guest authentication service (**Critical**)
- `@app/src/schemas/guest`: Input validation schemas (**Critical**)

## 📝 Detailed Code Analysis

### Guest Login Endpoint (`POST /guest_login`)

**Purpose:** Authenticates guest users and provides temporary access tokens

**Flow:**
1. **Input Validation:** Validates request body against `validator.guestLogin` schema
2. **Service Delegation:** Calls `service.guest_login(data)` for authentication logic
3. **Token Setting:** Sets `ACCESS-TOKEN` header with generated token
4. **Response:** Returns success response with authentication result
5. **Error Handling:** Logs and re-throws errors with appropriate HTTP status codes

**Error Handling Strategy:**
```javascript
// Differentiated logging based on error type
if (err.code === ERROR_USER_NOT_FOUND) {
  logger.warn(`Guest login failed: ${err.message}`);
} else {
  logger.error(`Guest login error: ${err.message}`);
}
```

**Security Features:**
- Input validation prevents malformed requests
- Error differentiation for security logging
- Token-based authentication with header setting
- Service layer handles credential verification

## 🚀 Usage Methods

### Basic Guest Login
```bash
curl -X POST "https://api.tsp.example.com/api/v2/guest_login" \
  -H "Content-Type: application/json" \
  -d '{
    "device_id": "mobile_device_123",
    "platform": "ios"
  }'
```

### JavaScript Client Example
```javascript
async function guestLogin(deviceInfo) {
  try {
    const response = await fetch('/api/v2/guest_login', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(deviceInfo)
    });
    
    if (response.ok) {
      const token = response.headers.get('ACCESS-TOKEN');
      const data = await response.json();
      
      // Store token for subsequent requests
      localStorage.setItem('guestToken', token);
      return data.data;
    }
  } catch (error) {
    console.error('Guest login failed:', error);
  }
}
```

## 📊 Output Examples

### Successful Guest Login
```json
{
  "result": "success",
  "data": {
    "user_id": "guest_abc123",
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "expires_in": 3600,
    "guest_mode": true,
    "available_features": ["basic_routing", "transit_info"]
  }
}
```

**Response Headers:**
```
ACCESS-TOKEN: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

### User Not Found Error
```json
{
  "error": "ERROR_USER_NOT_FOUND",
  "message": "Guest authentication failed",
  "code": 404
}
```

### Validation Error
```json
{
  "error": "ValidationError", 
  "message": "Invalid device information provided",
  "details": [
    {
      "field": "device_id",
      "message": "device_id is required"
    }
  ]
}
```

## ⚠️ Important Notes

### Guest Account Limitations
- **Temporary Access:** Guest tokens have shorter lifespans than regular user tokens
- **Feature Restrictions:** Limited access to platform features for security and business reasons
- **Data Persistence:** Guest data may be temporary and not permanently stored
- **No Profile:** Guests cannot access profile-specific features like favorites or history

### Security Considerations
- **Device Tracking:** Uses device information for basic identification
- **Rate Limiting:** Should be implemented to prevent abuse of guest authentication
- **Data Privacy:** Guest data handling should comply with privacy regulations
- **Token Security:** Guest tokens should have appropriate security measures

### Integration Patterns
- **Progressive Registration:** Guests can be prompted to create full accounts
- **Feature Gating:** Gradual feature unlocking based on engagement
- **Trial Periods:** Time-limited access to encourage full registration
- **Analytics Tracking:** Guest behavior analysis for conversion optimization

### Error Recovery
- **Retry Logic:** Client applications should implement retry mechanisms
- **Fallback Options:** Alternative authentication methods if guest login fails
- **User Guidance:** Clear messaging about guest vs. full account benefits

## 🔗 Related File Links

- **Service Layer:** `allrepo/connectsmart/tsp-api/src/services/guest.js`
- **Validation Schema:** `allrepo/connectsmart/tsp-api/src/schemas/guest.js`
- **Error Codes:** `allrepo/connectsmart/tsp-api/src/static/error-code.js`

---
*This controller provides essential guest access functionality for user acquisition and trial experiences.*