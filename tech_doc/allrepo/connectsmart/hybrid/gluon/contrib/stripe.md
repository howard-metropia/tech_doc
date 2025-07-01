# Gluon Contrib Stripe Module

## Overview
Stripe payment processing integration for web2py applications. Provides a complete interface for Stripe's payment API, enabling credit card processing, subscription management, and webhook handling.

## Module Information
- **Module**: `gluon.contrib.stripe`
- **Purpose**: Stripe payment processing
- **Dependencies**: stripe-python library
- **Features**: Payments, subscriptions, webhooks

## Key Features
- **Payment Processing**: Credit card and ACH payments
- **Subscription Management**: Recurring billing support
- **Webhook Integration**: Real-time payment notifications
- **Customer Management**: Customer data and payment methods
- **Security**: PCI-compliant payment handling

## Basic Usage

### Payment Processing
```python
from gluon.contrib.stripe import StripePayment

# Initialize Stripe
stripe_payment = StripePayment(
    api_key=current.app_config.stripe_secret_key,
    publishable_key=current.app_config.stripe_publishable_key
)

def process_payment():
    """Process credit card payment"""
    
    # Create payment intent
    payment_intent = stripe_payment.create_payment_intent(
        amount=2000,  # $20.00 in cents
        currency='usd',
        customer_email=request.vars.email,
        description='Product purchase'
    )
    
    return dict(
        client_secret=payment_intent.client_secret,
        publishable_key=stripe_payment.publishable_key
    )

def confirm_payment():
    """Confirm payment completion"""
    
    payment_intent_id = request.vars.payment_intent_id
    
    # Retrieve payment intent
    payment_intent = stripe_payment.retrieve_payment_intent(payment_intent_id)
    
    if payment_intent.status == 'succeeded':
        # Payment successful - fulfill order
        order_id = db.orders.insert(
            customer_email=payment_intent.receipt_email,
            amount=payment_intent.amount / 100,
            payment_intent_id=payment_intent_id,
            status='paid'
        )
        
        return dict(success=True, order_id=order_id)
    else:
        return dict(success=False, error='Payment not completed')
```

### Subscription Management
```python
def create_subscription():
    """Create recurring subscription"""
    
    # Create customer
    customer = stripe_payment.create_customer(
        email=request.vars.email,
        name=request.vars.name,
        payment_method=request.vars.payment_method_id
    )
    
    # Create subscription
    subscription = stripe_payment.create_subscription(
        customer_id=customer.id,
        price_id='price_premium_monthly',  # Stripe price ID
        trial_period_days=14
    )
    
    # Store subscription in database
    db.subscriptions.insert(
        customer_id=customer.id,
        stripe_subscription_id=subscription.id,
        user_id=auth.user_id,
        status=subscription.status,
        current_period_start=subscription.current_period_start,
        current_period_end=subscription.current_period_end
    )
    
    return dict(
        success=True,
        subscription_id=subscription.id,
        client_secret=subscription.latest_invoice.payment_intent.client_secret
    )
```

### Webhook Handling
```python
def stripe_webhook():
    """Handle Stripe webhooks"""
    
    payload = request.body.read()
    sig_header = request.env.http_stripe_signature
    
    try:
        # Verify webhook signature
        event = stripe_payment.verify_webhook(
            payload,
            sig_header,
            current.app_config.stripe_webhook_secret
        )
        
        # Handle different event types
        if event.type == 'payment_intent.succeeded':
            handle_successful_payment(event.data.object)
        
        elif event.type == 'invoice.payment_succeeded':
            handle_subscription_payment(event.data.object)
        
        elif event.type == 'customer.subscription.deleted':
            handle_subscription_cancellation(event.data.object)
        
        return 'success'
    
    except Exception as e:
        logger.error(f"Webhook error: {str(e)}")
        raise HTTP(400, 'Webhook error')

def handle_successful_payment(payment_intent):
    """Handle successful payment"""
    
    # Update order status
    db(db.orders.payment_intent_id == payment_intent.id).update(
        status='completed',
        completed_at=datetime.datetime.now()
    )
    
    # Send confirmation email
    send_order_confirmation(payment_intent.receipt_email)

def handle_subscription_payment(invoice):
    """Handle subscription payment"""
    
    subscription_id = invoice.subscription
    
    # Update subscription status
    db(db.subscriptions.stripe_subscription_id == subscription_id).update(
        status='active',
        last_payment_date=datetime.datetime.now()
    )
    
    # Extend access period
    extend_user_access(subscription_id)
```

This module provides comprehensive Stripe payment integration for web2py applications, supporting both one-time payments and recurring subscriptions with proper webhook handling.