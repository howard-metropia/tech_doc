# TSP Job Service - Stripe Configuration

## Overview

The `config/vendor/stripe.js` file manages Stripe payment processing configuration for the TSP Job service's financial transaction handling. This configuration provides secure access to Stripe's payment APIs for processing payments, managing subscriptions, and handling financial operations within the MaaS platform.

## File Information

- **File Path**: `/config/vendor/stripe.js`
- **File Type**: JavaScript Configuration Module
- **Primary Purpose**: Stripe payment API configuration
- **Dependencies**: Environment variables for Stripe API credentials

## Configuration Structure

```javascript
module.exports = {
  apiKey: process.env.STRIPE_API_KEY,
};
```

## Configuration Components

### API Key Configuration
```javascript
apiKey: process.env.STRIPE_API_KEY
```

**Purpose**: Stripe secret API key for server-side payment processing
- **Format**: `sk_` prefixed secret key for production or `sk_test_` for testing
- **Security**: Server-side only credential for sensitive operations
- **Capabilities**: Full access to Stripe API including charges, customers, subscriptions

## Stripe Integration Implementation

### Stripe Client Setup
```javascript
const stripe = require('stripe');
const config = require('../config/vendor/stripe');

const stripeClient = stripe(config.apiKey, {
  apiVersion: '2023-10-16',
  timeout: 10000,
  telemetry: false
});

class StripePaymentService {
  static async createPaymentIntent(amount, currency = 'usd', options = {}) {
    try {
      const paymentIntent = await stripeClient.paymentIntents.create({
        amount: Math.round(amount * 100), // Convert to cents
        currency: currency,
        automatic_payment_methods: {
          enabled: true
        },
        metadata: options.metadata || {},
        description: options.description,
        receipt_email: options.email,
        ...options.paymentIntentOptions
      });
      
      return {
        success: true,
        paymentIntent: paymentIntent,
        clientSecret: paymentIntent.client_secret
      };
    } catch (error) {
      console.error('Stripe payment intent error:', error);
      throw error;
    }
  }
  
  static async confirmPaymentIntent(paymentIntentId, paymentMethodId) {
    try {
      const paymentIntent = await stripeClient.paymentIntents.confirm(paymentIntentId, {
        payment_method: paymentMethodId
      });
      
      return {
        success: true,
        paymentIntent: paymentIntent,
        status: paymentIntent.status
      };
    } catch (error) {
      console.error('Stripe payment confirmation error:', error);
      throw error;
    }
  }
  
  static async createCustomer(customerData) {
    try {
      const customer = await stripeClient.customers.create({
        email: customerData.email,
        name: customerData.name,
        phone: customerData.phone,
        metadata: customerData.metadata || {},
        description: customerData.description
      });
      
      return {
        success: true,
        customer: customer,
        customerId: customer.id
      };
    } catch (error) {
      console.error('Stripe customer creation error:', error);
      throw error;
    }
  }
  
  static async retrieveCustomer(customerId) {
    try {
      const customer = await stripeClient.customers.retrieve(customerId);
      
      return {
        success: true,
        customer: customer
      };
    } catch (error) {
      console.error('Stripe customer retrieval error:', error);
      throw error;
    }
  }
  
  static async attachPaymentMethod(paymentMethodId, customerId) {
    try {
      const paymentMethod = await stripeClient.paymentMethods.attach(paymentMethodId, {
        customer: customerId
      });
      
      return {
        success: true,
        paymentMethod: paymentMethod
      };
    } catch (error) {
      console.error('Stripe payment method attachment error:', error);
      throw error;
    }
  }
}
```

### Trip Payment Processing
```javascript
class TripPaymentProcessor {
  static async processRidePayment(tripData, paymentData) {
    try {
      // Calculate trip cost including fees
      const tripCost = this.calculateTripCost(tripData);
      
      // Create payment intent for the trip
      const paymentResult = await StripePaymentService.createPaymentIntent(
        tripCost.total,
        'usd',
        {
          description: `Trip payment - ${tripData.origin} to ${tripData.destination}`,
          email: tripData.userEmail,
          metadata: {
            tripId: tripData.tripId,
            userId: tripData.userId,
            origin: tripData.origin,
            destination: tripData.destination,
            distance: tripData.distance.toString(),
            duration: tripData.duration.toString()
          }
        }
      );
      
      // Store payment record
      await this.storePaymentRecord({
        tripId: tripData.tripId,
        paymentIntentId: paymentResult.paymentIntent.id,
        amount: tripCost.total,
        breakdown: tripCost.breakdown,
        status: 'pending'
      });
      
      return {
        success: true,
        paymentIntentId: paymentResult.paymentIntent.id,
        clientSecret: paymentResult.clientSecret,
        amount: tripCost.total,
        breakdown: tripCost.breakdown
      };
    } catch (error) {
      console.error('Trip payment processing error:', error);
      throw error;
    }
  }
  
  static calculateTripCost(tripData) {
    const baseFare = 2.50;
    const perMileRate = 1.25;
    const perMinuteRate = 0.35;
    
    const distanceCost = tripData.distance * perMileRate;
    const timeCost = (tripData.duration / 60) * perMinuteRate;
    const subtotal = baseFare + distanceCost + timeCost;
    
    // Apply surge pricing if applicable
    const surgeMultiplier = tripData.surgeMultiplier || 1.0;
    const surgedSubtotal = subtotal * surgeMultiplier;
    
    // Calculate fees
    const serviceFee = Math.max(1.75, surgedSubtotal * 0.05);
    const taxes = surgedSubtotal * 0.08; // 8% tax rate
    
    const total = surgedSubtotal + serviceFee + taxes;
    
    return {
      total: total,
      breakdown: {
        baseFare: baseFare,
        distanceCost: distanceCost,
        timeCost: timeCost,
        subtotal: subtotal,
        surgeMultiplier: surgeMultiplier,
        surgedSubtotal: surgedSubtotal,
        serviceFee: serviceFee,
        taxes: taxes
      }
    };
  }
  
  static async handlePaymentWebhook(event) {
    try {
      switch (event.type) {
        case 'payment_intent.succeeded':
          await this.handlePaymentSuccess(event.data.object);
          break;
        case 'payment_intent.payment_failed':
          await this.handlePaymentFailure(event.data.object);
          break;
        case 'charge.dispute.created':
          await this.handleDispute(event.data.object);
          break;
        default:
          console.log(`Unhandled event type: ${event.type}`);
      }
    } catch (error) {
      console.error('Webhook handling error:', error);
      throw error;
    }
  }
  
  static async handlePaymentSuccess(paymentIntent) {
    const tripId = paymentIntent.metadata.tripId;
    
    // Update payment record
    await this.updatePaymentRecord(paymentIntent.id, {
      status: 'succeeded',
      chargeId: paymentIntent.charges.data[0]?.id,
      completedAt: new Date()
    });
    
    // Update trip status
    await this.updateTripStatus(tripId, 'paid');
    
    // Send confirmation email
    await this.sendPaymentConfirmation(tripId, paymentIntent);
  }
  
  static async handlePaymentFailure(paymentIntent) {
    const tripId = paymentIntent.metadata.tripId;
    
    // Update payment record
    await this.updatePaymentRecord(paymentIntent.id, {
      status: 'failed',
      failureReason: paymentIntent.last_payment_error?.message,
      failedAt: new Date()
    });
    
    // Update trip status
    await this.updateTripStatus(tripId, 'payment_failed');
    
    // Send failure notification
    await this.sendPaymentFailureNotification(tripId, paymentIntent);
  }
}
```

### Subscription Management
```javascript
class SubscriptionManager {
  static async createSubscription(customerId, priceId, options = {}) {
    try {
      const subscription = await stripeClient.subscriptions.create({
        customer: customerId,
        items: [{
          price: priceId
        }],
        trial_period_days: options.trialDays,
        metadata: options.metadata || {},
        collection_method: 'charge_automatically',
        expand: ['latest_invoice.payment_intent']
      });
      
      return {
        success: true,
        subscription: subscription,
        subscriptionId: subscription.id
      };
    } catch (error) {
      console.error('Subscription creation error:', error);
      throw error;
    }
  }
  
  static async updateSubscription(subscriptionId, updates) {
    try {
      const subscription = await stripeClient.subscriptions.update(subscriptionId, updates);
      
      return {
        success: true,
        subscription: subscription
      };
    } catch (error) {
      console.error('Subscription update error:', error);
      throw error;
    }
  }
  
  static async cancelSubscription(subscriptionId, cancelAtPeriodEnd = true) {
    try {
      const subscription = await stripeClient.subscriptions.update(subscriptionId, {
        cancel_at_period_end: cancelAtPeriodEnd
      });
      
      return {
        success: true,
        subscription: subscription,
        canceledAt: subscription.canceled_at
      };
    } catch (error) {
      console.error('Subscription cancellation error:', error);
      throw error;
    }
  }
}
```

### Refund Processing
```javascript
class RefundProcessor {
  static async processRefund(chargeId, amount = null, reason = 'requested_by_customer', metadata = {}) {
    try {
      const refundData = {
        charge: chargeId,
        reason: reason,
        metadata: metadata
      };
      
      if (amount) {
        refundData.amount = Math.round(amount * 100); // Convert to cents
      }
      
      const refund = await stripeClient.refunds.create(refundData);
      
      return {
        success: true,
        refund: refund,
        refundId: refund.id,
        amount: refund.amount / 100, // Convert back to dollars
        status: refund.status
      };
    } catch (error) {
      console.error('Refund processing error:', error);
      throw error;
    }
  }
  
  static async getRefundStatus(refundId) {
    try {
      const refund = await stripeClient.refunds.retrieve(refundId);
      
      return {
        success: true,
        refund: refund,
        status: refund.status
      };
    } catch (error) {
      console.error('Refund status retrieval error:', error);
      throw error;
    }
  }
}
```

## Security and Compliance

### Webhook Signature Verification
```javascript
class StripeWebhookHandler {
  static async verifyWebhookSignature(payload, signature, endpointSecret) {
    try {
      const event = stripe.webhooks.constructEvent(payload, signature, endpointSecret);
      return event;
    } catch (error) {
      console.error('Webhook signature verification failed:', error);
      throw new Error('Invalid webhook signature');
    }
  }
  
  static async handleWebhook(req, res) {
    const payload = req.body;
    const signature = req.headers['stripe-signature'];
    const endpointSecret = process.env.STRIPE_WEBHOOK_SECRET;
    
    try {
      const event = await this.verifyWebhookSignature(payload, signature, endpointSecret);
      
      // Process the event
      await TripPaymentProcessor.handlePaymentWebhook(event);
      
      res.status(200).json({ received: true });
    } catch (error) {
      console.error('Webhook handling failed:', error);
      res.status(400).json({ error: error.message });
    }
  }
}
```

### PCI Compliance
```javascript
class PCIComplianceHelper {
  static sanitizeCardData(cardData) {
    // Never store full card numbers
    return {
      last4: cardData.last4,
      brand: cardData.brand,
      exp_month: cardData.exp_month,
      exp_year: cardData.exp_year,
      funding: cardData.funding
    };
  }
  
  static logPaymentEvent(eventType, paymentIntentId, sanitizedData) {
    // Log payment events for audit purposes
    const logEntry = {
      timestamp: new Date().toISOString(),
      eventType: eventType,
      paymentIntentId: paymentIntentId,
      data: sanitizedData
    };
    
    // Store in secure audit log
    console.log('Payment event:', logEntry);
  }
}
```

## Error Handling and Monitoring

### Stripe Error Handling
```javascript
class StripeErrorHandler {
  static handleStripeError(error) {
    switch (error.type) {
      case 'StripeCardError':
        return {
          type: 'card_error',
          message: 'Your card was declined.',
          decline_code: error.decline_code,
          charge_id: error.charge
        };
      case 'RateLimitError':
        return {
          type: 'rate_limit',
          message: 'Too many requests made to the API too quickly'
        };
      case 'StripeInvalidRequestError':
        return {
          type: 'invalid_request',
          message: 'Invalid parameters were supplied to Stripe API'
        };
      case 'StripeAPIError':
        return {
          type: 'api_error',
          message: 'An error occurred internally with Stripe API'
        };
      case 'StripeConnectionError':
        return {
          type: 'connection_error',
          message: 'Some kind of error occurred during the HTTPS communication'
        };
      case 'StripeAuthenticationError':
        return {
          type: 'authentication_error',
          message: 'Authentication with Stripe API failed'
        };
      default:
        return {
          type: 'unknown_error',
          message: 'An unknown error occurred'
        };
    }
  }
}
```

### Payment Monitoring
```javascript
class PaymentMonitor {
  static async trackPaymentMetrics(paymentEvent) {
    const metrics = {
      timestamp: new Date().toISOString(),
      eventType: paymentEvent.type,
      amount: paymentEvent.amount,
      currency: paymentEvent.currency,
      success: paymentEvent.success,
      processingTime: paymentEvent.processingTime
    };
    
    // Store metrics for analysis
    await this.storePaymentMetrics(metrics);
  }
  
  static async getPaymentStatistics(timeRange = '24h') {
    const metrics = await this.retrievePaymentMetrics(timeRange);
    
    return {
      totalTransactions: metrics.length,
      successRate: metrics.filter(m => m.success).length / metrics.length,
      totalVolume: metrics.reduce((sum, m) => sum + m.amount, 0),
      averageTransactionSize: metrics.reduce((sum, m) => sum + m.amount, 0) / metrics.length,
      averageProcessingTime: metrics.reduce((sum, m) => sum + m.processingTime, 0) / metrics.length
    };
  }
}
```

This Stripe configuration provides comprehensive payment processing capabilities for the TSP Job service, enabling secure transaction handling, subscription management, and financial operations with proper error handling, monitoring, and PCI compliance considerations.