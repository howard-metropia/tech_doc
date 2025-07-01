# TSP API Referral Controller Documentation

## 🔍 Quick Summary (TL;DR)
The referral controller manages user referral programs, allowing users to create referral invitations and track referral-based rewards within the TSP platform's user acquisition system.

**Keywords:** referral | referral-program | user-acquisition | invite-friends | referral-rewards | viral-growth | user-engagement | referral-tracking

**Primary use cases:** Creating referral invitations, tracking referral rewards, managing referral campaigns, viral user acquisition

**Compatibility:** Node.js >= 16.0.0, Koa.js v2.x, @koa/router v10.x

## ❓ Common Questions Quick Index
- **Q: How do I create a referral invitation?** → [Create Referral](#create-referral-post-)
- **Q: What information is needed to refer someone?** → Contact information and referral context via service validation
- **Q: How are referral rewards distributed?** → Managed by service layer based on successful sign-ups
- **Q: Can I track my referral history?** → Service layer provides referral tracking and analytics
- **Q: What authentication is required?** → JWT authentication with user context headers
- **Q: Are there limits on referrals?** → Limits and fraud prevention handled by service layer

## 📋 Functionality Overview

**Non-technical explanation:** 
Think of this as a **friend invitation system** for the transportation app. When you love using the app, you can invite your friends to join and both of you might get rewards. This controller handles the invitation process - it takes your friend's information, creates a proper invitation with your referral credit, and makes sure everything is tracked so you both get benefits when your friend signs up.

**Technical explanation:** 
A minimal Koa.js REST controller that provides referral creation functionality for viral user acquisition programs. It handles user authentication, input validation combining header context and request data, and delegates referral processing to the service layer for tracking and reward distribution.

**Business value explanation:**
Critical for organic user growth and acquisition cost reduction. Referral programs leverage existing user satisfaction to drive new user acquisition while providing rewards that increase user engagement and retention for both referrers and referees.

## 🔧 Technical Specifications

- **File:** `allrepo/connectsmart/tsp-api/src/controllers/referral.js`
- **Language:** JavaScript (ES2020)
- **Framework:** Koa.js v2.x with @koa/router
- **Type:** User Acquisition/Growth Controller
- **File Size:** ~0.5 KB
- **Complexity Score:** ⭐ (Low - Single endpoint with validation and service delegation)

**Dependencies:**
- `@koa/router`: HTTP routing framework (**Critical**)
- `koa-bodyparser`: Request body parsing (**Critical**)
- `@maas/core/response`: Standardized response formatting (**High**)
- `@app/src/middlewares/auth`: JWT authentication middleware (**Critical**)
- `@app/src/helpers/fields-of-header`: Header field extraction utility (**High**)
- `@app/src/schemas/referral`: Input validation schemas (**Critical**)
- `@app/src/services/referral`: Referral business logic service (**Critical**)

## 📝 Detailed Code Analysis

### Create Referral Endpoint (`POST /`)

**Purpose:** Creates referral invitations for user acquisition programs

**Flow:**
1. **Authentication:** JWT authentication via auth middleware
2. **Input Aggregation:** Combines header fields (user context) with request body (referral data)
3. **Input Validation:** Validates combined input against referral schema
4. **Service Delegation:** Passes validated data to referral service for processing
5. **Response:** Returns service result in standardized success format

**Input Processing Pattern:**
```javascript
const input = await inputValidator.create.validateAsync({
  ...fetchFieldsFromHeader(ctx.request.header),
  ...ctx.request.body,
});
```

This ensures:
- User context (userId, etc.) extracted from authentication headers
- Referral data (contact info, etc.) from request body
- Combined validation for complete referral creation

### Service Integration
- **Clean Delegation:** All business logic handled by service layer
- **User Context:** User ID and context passed for referral attribution
- **Validation:** Comprehensive input validation before service processing

## 🚀 Usage Methods

### Create Friend Referral
```bash
curl -X POST "https://api.tsp.example.com/api/v2/referral" \
  -H "Authorization: Bearer <JWT_TOKEN>" \
  -H "userid: usr_12345" \
  -H "Content-Type: application/json" \
  -d '{
    "referee_email": "friend@example.com",
    "referee_name": "John Smith",
    "message": "Check out this awesome transportation app!",
    "referral_type": "email_invitation"
  }'
```

### Create Social Media Referral
```bash
curl -X POST "https://api.tsp.example.com/api/v2/referral" \
  -H "Authorization: Bearer <JWT_TOKEN>" \
  -H "userid: usr_12345" \
  -H "Content-Type: application/json" \
  -d '{
    "referral_type": "social_share",
    "platform": "facebook",
    "message": "Join me on this great transportation app",
    "referral_code": "custom_code_123"
  }'
```

### JavaScript Client Example
```javascript
async function createReferral(authToken, userId, referralData) {
  try {
    const response = await fetch('/api/v2/referral', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${authToken}`,
        'userid': userId,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(referralData)
    });
    
    if (response.ok) {
      const result = await response.json();
      console.log('Referral created successfully:', result.data);
      return result.data;
    } else {
      const error = await response.json();
      throw new Error(error.message || 'Referral creation failed');
    }
  } catch (error) {
    console.error('Referral error:', error);
    throw error;
  }
}

// Usage examples
const emailReferral = {
  referee_email: 'friend@example.com',
  referee_name: 'Jane Doe',
  message: 'You should try this transportation app!',
  referral_type: 'email_invitation'
};

createReferral(authToken, userId, emailReferral);
```

## 📊 Output Examples

### Successful Referral Creation
```json
{
  "result": "success",
  "data": {
    "referral_id": "ref_abc123xyz",
    "referrer_id": "usr_12345",
    "referral_code": "FRIEND2024",
    "referral_link": "https://app.tsp.example.com/join?ref=FRIEND2024",
    "referee_email": "friend@example.com",
    "status": "pending",
    "created_at": "2024-06-25T14:30:00Z",
    "expires_at": "2024-07-25T14:30:00Z",
    "reward_details": {
      "referrer_reward": "500 points",
      "referee_reward": "Welcome bonus + 250 points"
    }
  }
}
```

### Email Invitation Response
```json
{
  "result": "success",
  "data": {
    "referral_id": "ref_email456",
    "invitation_sent": true,
    "email_status": "delivered",
    "tracking_code": "email_track_789",
    "referral_link": "https://app.tsp.example.com/join?ref=EMAIL456",
    "estimated_delivery": "2024-06-25T14:35:00Z"
  }
}
```

### Validation Error Response
```json
{
  "error": "ValidationError",
  "message": "Invalid referral request",
  "details": [
    {
      "field": "referee_email",
      "message": "referee_email must be a valid email address"
    },
    {
      "field": "referral_type",
      "message": "referral_type is required"
    }
  ]
}
```

## ⚠️ Important Notes

### Referral Program Features
- **Multiple Referral Types:** Email invitations, social sharing, direct links
- **Reward Systems:** Configurable rewards for both referrer and referee
- **Tracking:** Complete referral funnel tracking from invitation to conversion
- **Expiration Management:** Time-limited referral codes and invitations

### User Context Integration
- **Header Processing:** User context automatically extracted from authentication headers
- **Attribution:** All referrals properly attributed to the referring user
- **User Validation:** Ensures only authenticated users can create referrals

### Business Logic Features
- **Fraud Prevention:** Service layer handles duplicate prevention and abuse detection
- **Campaign Management:** Support for different referral campaigns and promotions
- **Analytics Integration:** Referral performance tracking and reporting
- **Reward Distribution:** Automated reward processing upon successful conversions

### Security Considerations
- **Authentication Required:** All referral creation requires valid user authentication
- **Input Validation:** Comprehensive validation prevents malformed referral requests
- **Rate Limiting:** Service layer may implement rate limiting to prevent spam
- **Privacy Protection:** Referee information handled securely

### Integration Possibilities
- **Email Services:** Integration with email providers for invitation delivery
- **Social Platforms:** Social media sharing integrations
- **Analytics:** Tracking pixel and conversion analytics
- **CRM Systems:** Customer relationship management integration for lead tracking

### Performance Considerations
- **Asynchronous Processing:** Email sending and external integrations handled asynchronously
- **Caching:** Referral codes and links may be cached for performance
- **Scalability:** Service layer designed to handle high-volume referral campaigns

## 🔗 Related File Links

- **Referral Service:** `allrepo/connectsmart/tsp-api/src/services/referral.js`
- **Validation Schemas:** `allrepo/connectsmart/tsp-api/src/schemas/referral.js`
- **Authentication:** `allrepo/connectsmart/tsp-api/src/middlewares/auth.js`
- **Header Helpers:** `allrepo/connectsmart/tsp-api/src/helpers/fields-of-header.js`

---
*This controller provides essential referral program functionality for viral user acquisition and growth.*