# Suggestion Card Controller Documentation

## 🔍 Quick Summary (TL;DR)
This controller manages user interactions with "suggestion cards," which are likely proactive recommendations or alerts shown in the UI. It provides endpoints for fetching the content of a specific card and for dismissing (deleting) a card.

**Keywords:** suggestion-card | recommendation | user-prompt | dismiss-card | proactive-ui | tsp-api | user-experience

**Primary use cases:** 
- Retrieving the details of a specific suggestion card to display to the user.
- Allowing a user to dismiss a suggestion card, effectively removing it from their view.

**Compatibility:** Node.js >= 16.0.0, Koa.js v2.x.

## ❓ Common Questions Quick Index
- **Q: How do I get the content of a suggestion card?** → [GET /:id](#get-id)
- **Q: How does a user dismiss a card?** → [DELETE /:id](#delete-id)
- **Q: Where does the logic for generating suggestions live?** → Not here. This controller only fetches and deletes. The logic is in the `suggestion-card` service.
- **Q: Can a user dismiss another user's card?** → No, all operations are scoped to the authenticated `userId`.
- **Q: What happens when a card is "deleted"?** → The `services.delete` function is called, which likely marks the card as dismissed for that user in the database.

## 📋 Functionality Overview

**Non-technical explanation:** 
Think of this controller as the manager of the little pop-up tips or suggestion boxes that appear in an app.
- **Showing a Tip (`GET /:id`):** When the app wants to show you a specific tip (e.g., "Did you know you can save your work address?"), it asks this manager for the content of that tip by its ID.
- **Closing a Tip (`DELETE /:id`):** When you click the "X" or "Dismiss" button on that tip, the app tells the manager you've seen it, and the manager makes sure it doesn't show up for you again.

**Technical explanation:** 
A simple Koa.js REST controller with two endpoints for managing the lifecycle of user-specific suggestion cards. The `GET /:id` endpoint retrieves the content of a single card by its ID, scoped to the authenticated user. The `DELETE /:id` endpoint allows a user to dismiss a card, also scoped to the user. Both endpoints validate input and delegate the core logic to the corresponding `get` and `delete` functions in the `suggestion-card` service layer. This controller is purely for presentation and interaction, not for the generation of the suggestions themselves.

**Business value explanation:**
Suggestion cards are a key tool for proactive user engagement and feature discovery. This controller provides the necessary API for the client to display these timely, contextual recommendations (e.g., "It looks like you're going to the airport, would you like to reserve parking?"). By enabling users to dismiss cards, it ensures the feature is helpful rather than annoying, which is crucial for a positive user experience. This mechanism helps guide users toward valuable features, improving user education and adoption of the platform's full capabilities.

## 🔧 Technical Specifications

- **File:** `allrepo/connectsmart/tsp-api/src/controllers/suggestion-card.js`
- **Language:** JavaScript (ES2020)
- **Framework:** Koa.js v2.x with @koa/router
- **Type:** REST API Controller
- **File Size:** ~1 KB
- **Complexity Score:** ⭐ (Very Low - A minimal controller with two standard endpoints.)

**Dependencies (Criticality Level):**
- `@koa/router`, `koa-bodyparser`: Core routing and body parsing (**Critical**).
- `@maas/core/response`: Standardized success response formatter (**High**).
- `@app/src/middlewares/auth`: JWT authentication middleware (**Critical**).
- `@app/src/helpers/fields-of-header`: Utility to extract user context from headers (**High**).
- `@app/src/schemas/suggestion-card`: Joi schemas for input validation (**Critical**).
- `@app/src/services/suggestion-card`: The service layer containing all business logic (**Critical**).

## 📝 Detailed Code Analysis

### `GET /:id`
- **Purpose**: Retrieve a single suggestion card.
- **Logic**: A standard, clean implementation.
    1. It combines the `userId` from the header and the card `id` from the URL parameters.
    2. It validates this combined object against the Joi schema.
    3. It calls `services.get(userId, cardId)`, passing the necessary identifiers to the service layer, which handles the database lookup.
    4. It wraps the result from the service in a standard `success` response.

### `DELETE /:id`
- **Purpose**: Dismiss/delete a suggestion card for the user.
- **Logic**: Identical in structure to the `GET` endpoint.
    1. It combines the `userId` and card `id`.
    2. It validates the input.
    3. It calls `services.delete(userId, cardId)` to perform the dismissal logic in the service layer.
    4. It returns a standard `success` response.

## 🚀 Usage Methods

**Base URL:** `https://api.tsp.example.com/api/v1/suggestion_card`
**Headers (for all requests):**
- `Authorization`: `Bearer <YOUR_JWT_TOKEN>`
- `userid`: `usr_...` (The user's ID)

### Get a Suggestion Card
```bash
curl -X GET "https://api.tsp.example.com/api/v1/suggestion_card/sug_abc123" \
  -H "Authorization: Bearer <TOKEN>" \
  -H "userid: usr_123"
```

### Dismiss a Suggestion Card
```bash
curl -X DELETE "https://api.tsp.example.com/api/v1/suggestion_card/sug_abc123" \
  -H "Authorization: Bearer <TOKEN>" \
  -H "userid: usr_123"
```

## 📊 Output Examples

### Successful GET Response
```json
{
  "result": "success",
  "data": {
    "id": "sug_abc123",
    "title": "Reserve Airport Parking",
    "body": "Heading to the airport? Tap here to reserve your parking spot in advance.",
    "action": "DEEP_LINK_TO_PARKING_RESERVATION",
    "priority": "high"
  }
}
```

### Successful DELETE Response
```json
{
  "result": "success",
  "data": {
    "message": "Suggestion card dismissed successfully."
  }
}
```

## ⚠️ Important Notes
- **Stateless Controller**: This controller is completely stateless. The logic for *which* suggestion cards to generate for a user resides entirely within the `suggestion-card` service and is not part of this file.
- **User-Scoped**: All actions are strictly tied to the `userId` from the authenticated session, ensuring a user can only interact with their own suggestions.

## 🔗 Related File Links
- **Business Logic Service:** `allrepo/connectsmart/tsp-api/src/services/suggestion-card.js`
- **Input Validation Schemas:** `allrepo/connectsmart/tsp-api/src/schemas/suggestion-card.js`
- **Authentication Middleware:** `allrepo/connectsmart/tsp-api/src/middlewares/auth.js`

---
*This documentation was generated to clarify the role of this simple controller in managing user interactions with proactive suggestion cards.* 