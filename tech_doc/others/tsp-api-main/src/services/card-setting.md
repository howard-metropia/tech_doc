# Stripe Card Settings Service Documentation

## 🔍 Quick Summary (TL;DR)
This service is a comprehensive and critical wrapper for managing user payment methods (credit cards) via the Stripe payment gateway. It handles the full lifecycle of a user's card: adding a new card, retrieving the list of saved cards, updating card details (like expiration date), setting a default card, and deleting a card. The service is built with robust error handling and includes a Slack notification mechanism to immediately alert the team of any failures in the payment processing flow.

**Keywords:** stripe | payment | credit-card | wallet | crud | api-wrapper | payment-gateway

**Primary use cases:** 
- Allowing users to add, view, update, and delete their credit card information.
- Creating and managing `Customer` objects in the Stripe system.
- Securely handling all interactions with the Stripe API for payment methods.
- Providing real-time alerts to a Slack channel if any Stripe operations fail.

**Compatibility:** Node.js >= 16.0.0, Stripe Node.js library.

## ❓ Common Questions Quick Index
- **Q: What is this service for?** → It manages everything related to a user's saved credit cards using Stripe.
- **Q: Does this service store credit card numbers?** → **No.** It never touches or stores raw credit card numbers. It uses secure tokens provided by Stripe to manage payment methods, which is the correct and PCI-compliant way to handle payments.
- **Q: What is a "Stripe Customer"?** → It's an object in the Stripe system that represents one of our users. All their saved cards and payment information are attached to this Customer object. This service creates a Stripe Customer for a user the first time they add a card.
- **Q: What happens if something goes wrong?** → This service has excellent error handling. It logs the error and immediately sends a detailed alert to a Slack channel so the development team can investigate.

## 📋 Functionality Overview

**Non-technical explanation:** 
Think of this service as a **highly secure and diligent bank teller who manages the safety deposit boxes (Stripe) where customers keep their credit cards**.
- **`get` (Viewing a Customer's Cards):** A customer asks to see the credit cards they have on file. The teller looks up the customer's profile (the `UserWallets` record), finds their unique safety deposit box number (`stripe_customer_id`), opens the box with Stripe's help, and presents a formatted list of the cards inside.
- **`create` (Adding a New Card):** A new customer wants to add a card.
    - If they've never used the bank before, the teller first creates a new safety deposit box just for them (creates a new Stripe `Customer`).
    - The customer then hands over a special, single-use, sealed envelope (the Stripe `token`) containing the card details. The teller uses this envelope to add the card to the customer's box without ever seeing the card number themselves.
- **`update` (Updating Card Info):** A customer says, "My card has a new expiration date," or "Please make this my primary card." The teller finds the specific card in the safety deposit box and updates its information or marks it as the default.
- **`delete` (Removing a Card):** A customer wants to remove a card. The teller takes the card out of the safety deposit box and shreds it.

**Technical explanation:** 
This service encapsulates all interactions with the Stripe Node.js library for managing `Customer` and `PaymentMethod` objects.
- **`get`**: Retrieves the `stripe_customer_id` from the local `UserWallets` model. It then calls `stripe.customers.retrieve` and `stripe.customers.listPaymentMethods` to fetch the user's cards from Stripe and formats them into a simplified array of objects.
- **`create`**: Implements "lazy creation" of Stripe Customers. If a user doesn't have a `stripe_customer_id` in `UserWallets`, it first calls `stripe.customers.create`. Then, using a `token` from the client, it calls `stripe.customers.createSource` to attach the new payment method to the customer.
- **`update`**: Handles modifications to a card. It calls `stripe.customers.updateSource` to change card details (like `exp_year`) and `stripe.customers.update` to change the customer's `default_source`.
- **`delete`**: Removes a payment method by calling `stripe.customers.deleteSource`.
- All methods are wrapped in robust `try...catch` blocks that log errors and trigger `slackInstance.sendVendorFailedMsg` for immediate operational awareness.

**Business value explanation:**
This service is a cornerstone of the application's monetization strategy. By providing a secure, reliable, and well-architected interface for payment management, it builds user trust and enables all e-commerce and transaction-based features. The proactive Slack alerting mechanism is a critical business continuity feature, minimizing downtime and potential revenue loss by ensuring that payment processing failures are detected and addressed immediately.

## 🔧 Technical Specifications

- **File:** `allrepo/connectsmart/tsp-api/src/services/card-setting.js`
- **Language:** JavaScript (ES2017+)
- **Key Libraries:** `stripe`, `@maas/core/log`, `@maas/services` (SlackManager), Mongoose
- **Type:** Payment Gateway Service / API Wrapper
- **File Size:** ~10 KB
- **Complexity Score:** ⭐⭐⭐ (Medium. The logic is a direct mapping to the Stripe API, but the error handling, Slack integration, and coordination with the local database add layers of complexity.)

## 📝 Detailed Code Analysis

### Robust Error Handling and Alerting
The standout feature of this service is its error handling. Every external call to the Stripe API is wrapped in a `try...catch` block. Upon catching an error, it performs two actions:
1.  **Logging:** `logger.error` writes the technical details to the standard log output for later analysis.
2.  **Alerting:** `slackInstance.sendVendorFailedMsg` sends a formatted, real-time message to a Slack channel. This message includes the project name, stage, the specific vendor API that failed, the error message, and a JSON payload of the request metadata. This is a best-in-class approach for monitoring critical third-party integrations.

### Lazy Customer Creation
The `create` function only creates a Stripe `Customer` object when a user adds their *first* payment method. This is an efficient and common pattern. It avoids creating empty Stripe customer profiles for users who may never use paid features, keeping the Stripe account cleaner and potentially reducing costs if Stripe were to charge per customer object.

### Clear Separation of Concerns
The service does a good job of separating its concerns.
- It uses the `UserWallets` model from the local database only to store the link to the external system (the `stripe_customer_id`).
- All sensitive payment information and complex business logic reside within Stripe, which is the "source of truth."
- The service acts as a clean orchestrator between the two systems. Helper functions like `fetchStripeCustomer` and `fetchStripeCards` further improve the code's readability and maintainability.

## 🚀 Usage Methods

```javascript
const cardSettingService = require('@app/src/services/card-setting');
const userId = 123;

// To add a new card, where stripeToken is obtained from the frontend Stripe.js library
async function addNewCard(stripeToken) {
  try {
    const result = await cardSettingService.create({ 
      userId, 
      transaction_token: stripeToken,
      zone: 'user_profile' 
    });
    console.log('Card added successfully. New card list:', result.cards);
  } catch (error) {
    console.error('Failed to add card:', error.message);
  }
}

// To fetch all of a user's cards
async function getUserCards() {
    try {
        const result = await cardSettingService.get(userId);
        console.log('User cards:', result.cards);
        console.log('Last payment way:', result.last_payment_way);
    } catch (error) {
        console.error('Failed to get cards:', error.message);
    }
}
```

## ⚠️ Important Notes
- **Security:** This service correctly avoids handling raw card data by using Stripe's tokenization, adhering to PCI compliance standards.
- **Configuration:** The service is heavily dependent on correct API keys for Stripe and Slack being present in the application's configuration.

## 🔗 Related File Links
- **Payment Gateway Library:** `stripe` (npm module)
- **Alerting Service:** `@maas/services` (SlackManager)
- **Local DB Models:** `@app/src/models/AuthUsers`, `@app/src/models/UserWallets`

---
*This documentation was generated to explain the service's critical role in managing user payment methods via Stripe, highlighting its robust error handling and alerting features.* 