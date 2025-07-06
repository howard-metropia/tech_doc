# TSP API Stripe Webhook Controller Documentation

## 🔍 Quick Summary (TL;DR)
The Stripe webhook controller handles payment-related events from Stripe's payment processing platform, particularly focusing on dispute/chargeback notifications for automated dispute management.

**Keywords:** stripe-webhook | payment-events | chargebacks | disputes | payment-processing | webhook-handler | stripe-integration | payment-notifications

**Primary use cases:** Processing Stripe payment events, handling chargebacks, managing payment disputes, real-time payment status updates

**Compatibility:** Node.js >= 16.0.0, Koa.js v2.x, Stripe API

## ❓ Common Questions Quick Index
- **Q: What Stripe events are handled?** → Currently handles charge.dispute.created events
- **Q: How is webhook security handled?** → Signature verification with webhook secret
- **Q: What happens if signature verification fails?** → Event is still processed but logged as warning
- **Q: How are disputes managed?** → Delegated to stripe-webhook service for handling
- **Q: Is this endpoint authenticated?** → No JWT required, uses Stripe signature verification
- **Q: What's the response format?** → Always returns {received: true} for Stripe acknowledgment

## 📋 Functionality Overview

**Non-technical explanation:** 
Think of this as a **payment alert system** for your app. When something happens with a payment (like a customer disputes a charge with their bank), Stripe sends a notification to this controller. It's like having a 24/7 assistant who listens for payment problems and immediately starts the process to handle them, ensuring your business can respond quickly to payment issues.

**Technical explanation:** 
A Koa.js webhook endpoint that receives and processes Stripe payment events. It implements signature verification for security, handles various payment event types (particularly disputes), and delegates event processing to appropriate service handlers while maintaining proper webhook acknowledgment patterns.

**Business value explanation:**
Critical for maintaining payment system integrity and automated dispute resolution. Enables real-time response to payment events, reduces manual intervention in dispute management, and ensures compliance with payment processor requirements for webhook handling.

## 🔧 Technical Specifications

- **File:** `allrepo/connectsmart/tsp-api/src/controllers/stripe-webHook.js`
- **Language:** JavaScript (ES2020)
- **Framework:** Koa.js v2.x with @koa/router
- **Type:** Payment Webhook Handler
- **File Size:** ~1.2 KB
- **Complexity Score:** ⭐⭐⭐ (Medium - External webhook handling with security verification)

**Dependencies:**
- `@koa/router`: HTTP routing framework (**Critical**)
- `koa-bodyparser`: Request body parsing (**Critical**)
- `stripe`: Stripe Node.js SDK (**Critical**)
- `@maas/core/log`: Logging infrastructure (**High**)
- `@app/src/services/stripe-webhook`: Webhook event processing service (**Critical**)
- `config`: Configuration management for Stripe settings (**Critical**)

## 📝 Detailed Code Analysis

### Webhook Endpoint (`POST /`)

**Purpose:** Receives and processes Stripe webhook events

**Security Flow:**
1. **Signature Extraction:** Gets Stripe signature from headers
2. **Event Construction:** Attempts to construct verified event using webhook secret
3. **Fallback Handling:** If signature fails, logs warning but continues processing
4. **Event Processing:** Routes events to appropriate handlers based on type

**Signature Verification:**
```javascript
try {
  event = stripe.webhooks.constructEvent(
    ctx.request.rawBody,
    sig,
    webHookSecret,
  );
} catch (err) {
  // Logs failure but continues processing
  logger.warn(`signature failed: ${err.message}`);
  event = ctx.request.body;
}
```

### Event Handling Pattern
```javascript
switch (event.type) {
  case 'charge.dispute.created':
    service.disputeHandler(event.data.object);
    break;
  default:
    logger.info(`Unhandled event type ${event.type}`);
}
```

### Response Format
Always returns standardized webhook acknowledgment:
```javascript
ctx.response.body = JSON.stringify({ received: true });
ctx.response.set('Content-Type', 'application/json');
```

## 🚀 Usage Methods

### Stripe Webhook Configuration
Configure in Stripe Dashboard:
- **Endpoint URL:** `https://api.tsp.example.com/api/v2/stripe/webhook`
- **Events to send:** Select relevant payment events
- **Webhook secret:** Store in configuration

### Testing Webhook Locally
```bash
# Using Stripe CLI for local testing
stripe listen --forward-to localhost:3000/api/v2/stripe/webhook

# Trigger test event
stripe trigger charge.dispute.created
```

### Manual Testing (Development)
```bash
# Simulate dispute event
curl -X POST "https://api.tsp.example.com/api/v2/stripe/webhook" \
  -H "stripe-signature: t=1234567890,v1=test_signature" \
  -H "Content-Type: application/json" \
  -d '{
    "type": "charge.dispute.created",
    "data": {
      "object": {
        "id": "dp_1234567890",
        "amount": 5000,
        "currency": "usd",
        "reason": "fraudulent",
        "status": "needs_response"
      }
    }
  }'
```

## 📊 Output Examples

### Webhook Acknowledgment
```json
{
  "received": true
}
```

### Logged Warnings (Signature Failure)
```
WARN: signature failed: No signatures found matching the expected signature for payload
WARN: stripe-signature: t=1234567890,v1=invalid_signature
WARN: btoa(ctx.request.rawBody):eyJ0eXBlIjoiY2hhcmdlLmRpc3B1dGUuY3JlYXRlZCIsImRhdGEiOnt9fQ==
```

### Logged Info (Unhandled Event)
```
INFO: Unhandled event type payment_intent.succeeded
```

## ⚠️ Important Notes

### Security Considerations
- **Signature Verification:** Critical but currently allows fallback for failed signatures
- **IP Whitelisting:** Consider restricting to Stripe IP addresses
- **HTTPS Required:** Webhooks must use secure connections
- **Replay Protection:** Stripe includes timestamp to prevent replay attacks

### Event Types to Consider
Common Stripe events for payment platforms:
- `charge.dispute.created`: Customer disputes/chargebacks
- `payment_intent.succeeded`: Successful payments
- `payment_intent.failed`: Failed payment attempts
- `customer.subscription.updated`: Subscription changes
- `invoice.payment_failed`: Failed recurring payments

### Webhook Best Practices
- **Idempotency:** Handle duplicate events gracefully
- **Async Processing:** Don't block webhook response
- **Quick Response:** Return acknowledgment immediately
- **Error Handling:** Log but don't fail on individual event errors

### Dispute Management
- **Automated Response:** Service layer handles dispute evidence submission
- **Time Sensitivity:** Disputes have response deadlines
- **Documentation:** Automatic evidence collection for disputes
- **Notification:** Alert relevant teams about disputes

### Configuration Requirements
```javascript
// Required configuration
vendor: {
  stripe: {
    apiKey: 'sk_live_...',
    webHookSecret: 'whsec_...'
  }
}
```

### Monitoring and Debugging
- **Webhook Logs:** Stripe dashboard shows delivery attempts
- **Signature Failures:** May indicate configuration issues
- **Event History:** Stripe retains event history for debugging
- **Retry Logic:** Stripe automatically retries failed deliveries

## 🔗 Related File Links

- **Webhook Service:** `allrepo/connectsmart/tsp-api/src/services/stripe-webhook.js`
- **Stripe Configuration:** Configuration files with Stripe settings
- **Error Codes:** `allrepo/connectsmart/tsp-api/src/static/error-code.js`

---
*This controller provides critical payment event handling for Stripe integration and automated dispute management.*