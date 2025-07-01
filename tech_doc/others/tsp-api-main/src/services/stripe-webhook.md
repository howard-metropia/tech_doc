# TSP API Stripe Webhook Service Documentation

## 🔍 Quick Summary (TL;DR)
The Stripe Webhook service handles payment dispute events from Stripe, automatically blocking users who initiate disputes, sending alert notifications to administrators, and maintaining comprehensive audit trails for payment fraud prevention.

**Keywords:** stripe-webhooks | payment-disputes | user-blocking | fraud-prevention | email-alerts | charge-retrieval | customer-mapping | administrative-notifications

**Primary use cases:** Handling Stripe payment disputes, automatically blocking fraudulent users, sending administrator alerts, maintaining payment security

**Compatibility:** Node.js >= 16.0.0, Stripe API integration, email notification system, database models for user blocking and wallet management

## ❓ Common Questions Quick Index
- **Q: What triggers user blocking?** → Stripe payment disputes automatically trigger user blocks
- **Q: Who gets notified?** → Configured administrator emails receive dispute alerts
- **Q: What information is tracked?** → User details, dispute IDs, charge IDs, and blocking reasons
- **Q: How are users identified?** → Through Stripe customer ID mapping to user wallets
- **Q: What happens if user not found?** → Warning logged but no blocking action taken
- **Q: Is blocking reversible?** → Block records created with is_deleted flag for potential reversal

## 📋 Functionality Overview

**Non-technical explanation:** 
Think of this as a **payment security guard** that watches for customers who try to get their money back after receiving services. When someone disputes a payment through their bank, this system automatically prevents them from using the service again and alerts the administrators to investigate.

**Technical explanation:** 
A payment fraud prevention service that processes Stripe webhook events for payment disputes, maps Stripe customer IDs to internal users, automatically creates blocking records, and sends comprehensive email notifications to administrators with user and dispute details.

**Business value explanation:**
Protects revenue by preventing repeat fraud, reduces manual monitoring overhead, provides immediate response to payment disputes, maintains detailed audit trails for investigations, and ensures administrators are promptly informed of potential fraud cases.

## 🔧 Technical Specifications

- **File:** `allrepo/connectsmart/tsp-api/src/services/stripe-webhook.js`
- **Language:** JavaScript (ES2020)
- **Framework:** Node.js with Stripe SDK and Objection.js ORM
- **Type:** Payment Dispute Handling and Fraud Prevention Service
- **File Size:** ~2.0 KB
- **Complexity Score:** ⭐⭐⭐ (Medium-High - Payment processing and security logic)

**Dependencies:**
- `stripe`: Stripe payment processing SDK (**Critical**)
- `moment-timezone`: Date/time formatting for notifications (**High**)
- `@app/src/models/UserWallets`: User wallet and Stripe customer mapping (**Critical**)
- `@app/src/models/BlockUsers`: User blocking system (**Critical**)
- `@app/src/models/AuthUsers`: User authentication data (**High**)
- `@app/src/helpers/send_mail`: Email notification system (**High**)

## 📝 Detailed Code Analysis

### Dispute Processing Pipeline

### disputeHandler Function
**Purpose:** Processes Stripe payment disputes and implements fraud prevention measures

```javascript
const disputeHandler = async (dispute) => {
  try {
    // Retrieve the charge to get the customer ID
    const charge = await stripe.charges.retrieve(dispute.charge);
    const customerId = charge.customer;
    
    const wallet = await UserWallets.query()
      .where('stripe_customer_id', customerId)
      .first();
      
    if (!wallet || !customerId) {
      logger.warn(`Could not find user with stripe customerId: ${customerId}`);
    } else {
      logger.info(
        `The userId: ${wallet.user_id} associated stripe customerId: ${customerId}`,
      );
      
      // Block the user
      await BlockUsers.query().insert({
        user_id: wallet.user_id,
        block_type: 1,
        reason: `Stripe dispute, disputeId:${dispute.id} chargeId:${dispute.charge}`,
        is_deleted: 'F',
      });
      
      // Send email notification
      await sendEmailNotify(wallet.user_id, dispute.id);
    }
  } catch (error) {
    logger.error(`Error retrieving charge: ${error.message}`);
  }
};
```

**Processing Steps:**
1. **Charge Retrieval:** Uses Stripe API to get charge details from dispute
2. **Customer Mapping:** Links Stripe customer ID to internal user via wallet records
3. **User Validation:** Checks if user exists in wallet system
4. **Blocking Action:** Creates block record with dispute details as reason
5. **Notification:** Sends email alert to administrators

### Email Notification System

### sendEmailNotify Function
**Purpose:** Sends comprehensive dispute alerts to administrators

```javascript
const sendEmailNotify = async (userId, disputeId) => {
  const emails = stripeConfig.alertNotifyEmail
    ? stripeConfig.alertNotifyEmail.split(',')
    : [];
    
  if (emails.length) {
    // User information retrieval
    const user = await AuthUsers.query()
      .select(['email', 'first_name', 'last_name'])
      .findById(userId);
      
    // Email subject construction
    const subject = `[${config.portal.projectTitle}] User blocking notification for Stripe dispute (user_id: ${userId})`;
    
    // Email content with comprehensive details
    const content = `Project: ${config.portal.projectTitle}<br />
      Time: ${moment.utc().format('YYYY-MM-DD HH:mm:ss')}(UTC)<br />
      user_id: ${userId}<br />
      Email: ${user.email}<br />
      First name: ${user.first_name}<br />
      Last name: ${user.last_name}<br />
      Dispute ID: ${disputeId}<br />
    `;
    
    // Send notification
    await sendMail(emails, subject, content, true);
  }
};
```

**Email Content Features:**
- **Project Identification:** Clear project context in subject and body
- **Timestamp:** UTC timestamp for accurate incident tracking
- **User Details:** Complete user identification information
- **Dispute Context:** Dispute ID for Stripe investigation tracking
- **HTML Formatting:** Structured email format for readability

### Error Handling and Logging

#### Comprehensive Error Management
```javascript
try {
  // Main dispute processing logic
} catch (error) {
  logger.error(`Error retrieving charge: ${error.message}`);
}

// User not found handling
if (!wallet || !customerId) {
  logger.warn(`Could not find user with stripe customerId: ${customerId}`);
} else {
  logger.info(`The userId: ${wallet.user_id} associated stripe customerId: ${customerId}`);
}
```
- **API Error Handling:** Catches Stripe API failures gracefully
- **Missing Data Handling:** Logs warnings for unmapped customers
- **Success Logging:** Confirms successful user mapping and actions

### Configuration and Security

#### Stripe Integration Setup
```javascript
const config = require('config');
const stripeConfig = config.vendor.stripe;
const stripe = require('stripe')(stripeConfig.apiKey);
```
- **API Key Management:** Secure configuration-based API key handling
- **Environment Configuration:** Flexible config for different environments
- **Email Recipients:** Configurable administrator notification lists

## 🚀 Usage Methods

### Basic Webhook Integration
```javascript
const stripeWebhookService = require('@app/src/services/stripe-webhook');

// Handle Stripe webhook event
app.post('/webhooks/stripe', express.raw({ type: 'application/json' }), async (req, res) => {
  const sig = req.headers['stripe-signature'];
  
  try {
    const event = stripe.webhooks.constructEvent(req.body, sig, endpointSecret);
    
    if (event.type === 'charge.dispute.created') {
      await stripeWebhookService.disputeHandler(event.data.object);
      console.log('Dispute processed successfully');
    }
    
    res.status(200).send('OK');
  } catch (error) {
    console.error('Webhook error:', error);
    res.status(400).send(`Webhook Error: ${error.message}`);
  }
});
```

### Advanced Webhook Management System
```javascript
class StripeWebhookManager {
  constructor() {
    this.stripeWebhookService = require('@app/src/services/stripe-webhook');
    this.eventHandlers = new Map();
    this.setupEventHandlers();
  }

  setupEventHandlers() {
    this.eventHandlers.set('charge.dispute.created', this.handleDisputeCreated.bind(this));
    this.eventHandlers.set('charge.dispute.updated', this.handleDisputeUpdated.bind(this));
    this.eventHandlers.set('invoice.payment_failed', this.handlePaymentFailed.bind(this));
  }

  async processWebhookEvent(event) {
    try {
      const handler = this.eventHandlers.get(event.type);
      
      if (handler) {
        await handler(event.data.object, event);
        return {
          success: true,
          eventType: event.type,
          eventId: event.id,
          processed: true
        };
      } else {
        console.log(`Unhandled event type: ${event.type}`);
        return {
          success: true,
          eventType: event.type,
          eventId: event.id,
          processed: false,
          reason: 'No handler configured'
        };
      }
    } catch (error) {
      console.error('Error processing webhook event:', error);
      return {
        success: false,
        eventType: event.type,
        eventId: event.id,
        error: error.message
      };
    }
  }

  async handleDisputeCreated(dispute, event) {
    console.log(`Processing dispute created: ${dispute.id}`);
    
    // Use the existing dispute handler
    await this.stripeWebhookService.disputeHandler(dispute);
    
    // Additional processing for dispute creation
    await this.logDisputeEvent(dispute, 'created');
    await this.updatePaymentAnalytics(dispute, 'dispute_created');
  }

  async handleDisputeUpdated(dispute, event) {
    console.log(`Processing dispute updated: ${dispute.id}`);
    
    // Handle dispute status changes
    if (dispute.status === 'won') {
      await this.handleDisputeWon(dispute);
    } else if (dispute.status === 'lost') {
      await this.handleDisputeLost(dispute);
    }
    
    await this.logDisputeEvent(dispute, 'updated');
  }

  async handlePaymentFailed(invoice, event) {
    console.log(`Processing payment failed: ${invoice.id}`);
    
    // Handle failed payment logic
    const customerId = invoice.customer;
    await this.handleFailedPayment(customerId, invoice);
  }

  async handleDisputeWon(dispute) {
    try {
      // Find user and potentially unblock them
      const charge = await stripe.charges.retrieve(dispute.charge);
      const customerId = charge.customer;
      
      const wallet = await UserWallets.query()
        .where('stripe_customer_id', customerId)
        .first();
        
      if (wallet) {
        // Consider unblocking user if dispute was won
        console.log(`Dispute won for user ${wallet.user_id}, consider unblocking`);
        
        // Update block record or create reversal record
        await this.updateBlockStatus(wallet.user_id, dispute.id, 'dispute_won');
      }
    } catch (error) {
      console.error('Error handling dispute won:', error);
    }
  }

  async handleDisputeLost(dispute) {
    try {
      console.log(`Dispute lost: ${dispute.id}`);
      // Additional penalties or permanent blocking logic
      await this.enhanceUserBlock(dispute);
    } catch (error) {
      console.error('Error handling dispute lost:', error);
    }
  }

  async handleFailedPayment(customerId, invoice) {
    try {
      const wallet = await UserWallets.query()
        .where('stripe_customer_id', customerId)
        .first();
        
      if (wallet) {
        // Handle failed payment - different from dispute
        console.log(`Payment failed for user ${wallet.user_id}`);
        await this.handlePaymentFailure(wallet.user_id, invoice);
      }
    } catch (error) {
      console.error('Error handling failed payment:', error);
    }
  }

  async logDisputeEvent(dispute, action) {
    // Log dispute events to database for analytics
    console.log(`Logging dispute event: ${dispute.id} - ${action}`);
    
    // Could insert into dispute_events table
    const eventRecord = {
      dispute_id: dispute.id,
      action,
      status: dispute.status,
      amount: dispute.amount,
      currency: dispute.currency,
      reason: dispute.reason,
      created_at: new Date(),
      raw_data: JSON.stringify(dispute)
    };
    
    // Insert event record (pseudo-code)
    // await DisputeEvents.query().insert(eventRecord);
  }

  async updatePaymentAnalytics(dispute, eventType) {
    // Update payment analytics and metrics
    console.log(`Updating analytics for dispute: ${dispute.id}`);
    
    // Could update analytics tables or send to analytics service
    const metrics = {
      eventType,
      amount: dispute.amount,
      currency: dispute.currency,
      timestamp: new Date()
    };
    
    // Send to analytics service (pseudo-code)
    // await analyticsService.recordEvent('payment_dispute', metrics);
  }

  async updateBlockStatus(userId, disputeId, reason) {
    // Update or reverse block status
    console.log(`Updating block status for user ${userId}: ${reason}`);
    
    // Could update is_deleted flag or add reversal record
    // await BlockUsers.query()
    //   .where({ user_id: userId, reason: { $like: `%${disputeId}%` } })
    //   .update({ is_deleted: 'T', reversal_reason: reason });
  }

  async enhanceUserBlock(dispute) {
    // Add permanent or enhanced blocking for lost disputes
    console.log(`Enhancing block for lost dispute: ${dispute.id}`);
    
    // Could add additional block types or permanent flags
  }

  async handlePaymentFailure(userId, invoice) {
    // Handle payment failures (different from disputes)
    console.log(`Handling payment failure for user ${userId}`);
    
    // Could implement retry logic, notifications, etc.
  }

  getEventStatistics() {
    // Return statistics about processed events
    return {
      supportedEvents: Array.from(this.eventHandlers.keys()),
      totalHandlers: this.eventHandlers.size
    };
  }
}

// Usage
const webhookManager = new StripeWebhookManager();

// Express webhook endpoint
app.post('/webhooks/stripe', express.raw({ type: 'application/json' }), async (req, res) => {
  const sig = req.headers['stripe-signature'];
  
  try {
    const event = stripe.webhooks.constructEvent(req.body, sig, process.env.STRIPE_WEBHOOK_SECRET);
    
    const result = await webhookManager.processWebhookEvent(event);
    
    console.log('Webhook processing result:', result);
    res.status(200).json(result);
  } catch (error) {
    console.error('Webhook signature verification failed:', error);
    res.status(400).send(`Webhook Error: ${error.message}`);
  }
});
```

### Monitoring and Analytics Integration
```javascript
class StripeDisputeMonitor {
  constructor() {
    this.stripeWebhookService = require('@app/src/services/stripe-webhook');
    this.disputeMetrics = {
      total: 0,
      won: 0,
      lost: 0,
      pending: 0
    };
  }

  async monitorDispute(dispute) {
    try {
      // Process the dispute
      await this.stripeWebhookService.disputeHandler(dispute);
      
      // Update metrics
      this.updateMetrics(dispute);
      
      // Check for patterns
      const analysis = await this.analyzeDisputePattern(dispute);
      
      if (analysis.riskLevel === 'high') {
        await this.alertHighRiskDispute(dispute, analysis);
      }
      
      return {
        processed: true,
        dispute_id: dispute.id,
        risk_level: analysis.riskLevel,
        metrics: this.disputeMetrics
      };
    } catch (error) {
      console.error('Error monitoring dispute:', error);
      return {
        processed: false,
        dispute_id: dispute.id,
        error: error.message
      };
    }
  }

  updateMetrics(dispute) {
    this.disputeMetrics.total++;
    
    switch (dispute.status) {
      case 'won':
        this.disputeMetrics.won++;
        break;
      case 'lost':
        this.disputeMetrics.lost++;
        break;
      default:
        this.disputeMetrics.pending++;
    }
  }

  async analyzeDisputePattern(dispute) {
    // Analyze dispute patterns for risk assessment
    const charge = await stripe.charges.retrieve(dispute.charge);
    const customerId = charge.customer;
    
    // Get customer's dispute history
    const customer = await stripe.customers.retrieve(customerId);
    
    // Simple risk analysis (could be more sophisticated)
    let riskLevel = 'low';
    
    if (dispute.amount > 10000) { // $100+
      riskLevel = 'high';
    } else if (dispute.reason === 'fraudulent') {
      riskLevel = 'high';
    }
    
    return {
      riskLevel,
      amount: dispute.amount,
      reason: dispute.reason,
      customerId
    };
  }

  async alertHighRiskDispute(dispute, analysis) {
    console.log(`HIGH RISK DISPUTE ALERT: ${dispute.id}`);
    
    // Send additional alerts for high-risk disputes
    const alertEmail = {
      subject: `[URGENT] High Risk Stripe Dispute: ${dispute.id}`,
      content: `
        HIGH RISK DISPUTE DETECTED
        Dispute ID: ${dispute.id}
        Amount: $${(dispute.amount / 100).toFixed(2)}
        Reason: ${dispute.reason}
        Risk Level: ${analysis.riskLevel}
        
        Immediate attention required.
      `
    };
    
    // Send to high-priority alert list
    // await sendUrgentAlert(alertEmail);
  }

  getDisputeReport() {
    const total = this.disputeMetrics.total;
    
    return {
      ...this.disputeMetrics,
      winRate: total > 0 ? (this.disputeMetrics.won / total * 100).toFixed(2) : 0,
      lossRate: total > 0 ? (this.disputeMetrics.lost / total * 100).toFixed(2) : 0
    };
  }
}

// Usage
const disputeMonitor = new StripeDisputeMonitor();

// Monitor disputes with enhanced analytics
const result = await disputeMonitor.monitorDispute(disputeObject);
console.log('Dispute monitoring result:', result);

const report = disputeMonitor.getDisputeReport();
console.log('Dispute report:', report);
```

## 📊 Output Examples

### Successful Dispute Processing
```javascript
// Log outputs
"The userId: 12345 associated stripe customerId: cus_abc123"
"User blocking notification sent for dispute: du_xyz789"

// Email notification sent to administrators
Subject: "[TSP Platform] User blocking notification for Stripe dispute (user_id: 12345)"
```

### User Not Found Response
```javascript
// Log output
"Could not find user with stripe customerId: cus_unknown123"

// No blocking action taken, only warning logged
```

### Webhook Processing Result
```javascript
{
  success: true,
  eventType: "charge.dispute.created",
  eventId: "evt_1234567890",
  processed: true
}
```

### Dispute Monitoring Analysis
```javascript
{
  processed: true,
  dispute_id: "du_xyz789",
  risk_level: "high",
  metrics: {
    total: 15,
    won: 8,
    lost: 3,
    pending: 4
  }
}
```

### Dispute Report Summary
```javascript
{
  total: 15,
  won: 8,
  lost: 3,
  pending: 4,
  winRate: "53.33",
  lossRate: "20.00"
}
```

## ⚠️ Important Notes

### Payment Security and Fraud Prevention
- **Automatic Blocking:** Users are immediately blocked upon dispute creation
- **Comprehensive Tracking:** All dispute details recorded for investigation
- **Administrator Alerts:** Real-time notifications ensure prompt response
- **Audit Trail:** Complete dispute history maintained for compliance

### Stripe Integration Requirements
- **Webhook Security:** Requires proper webhook signature verification
- **API Error Handling:** Graceful handling of Stripe API failures
- **Customer Mapping:** Depends on accurate Stripe customer ID tracking
- **Configuration Management:** Secure API key and email configuration

### User Impact and Recovery
- **Blocking Mechanism:** Users blocked with specific dispute-related reasons
- **Reversal Capability:** Block records include is_deleted flag for potential reversal
- **Data Preservation:** User data and transaction history preserved during blocks
- **Investigation Support:** Comprehensive information available for dispute resolution

### Operational Considerations
- **Email Configuration:** Requires configured administrator email list
- **Database Dependencies:** Multiple model dependencies for user and wallet data
- **Monitoring Requirements:** Should be monitored for webhook delivery failures
- **Scalability:** Designed for moderate dispute volume with potential for enhancement

## 🔗 Related File Links

- **User Blocking Models:** `allrepo/connectsmart/tsp-api/src/models/BlockUsers.js`
- **Wallet Models:** `allrepo/connectsmart/tsp-api/src/models/UserWallets.js`
- **Email Helper:** `allrepo/connectsmart/tsp-api/src/helpers/send_mail.js`
- **Payment Services:** Other Stripe and payment-related services

---
*This service provides automated payment dispute handling with user blocking and administrative notifications for fraud prevention in the TSP platform.*