# TSP API Gift Cards Controller Documentation

## 🔍 Quick Summary (TL;DR)
The gift cards controller provides an endpoint for retrieving available gift card categories and items that users can purchase with loyalty points earned through the TSP platform.

**Keywords:** gift-cards | rewards | loyalty-points | redemption | categories | digital-rewards | user-incentives | points-system

**Primary use cases:** Displaying available rewards in mobile app, loyalty program integration, points redemption system

**Compatibility:** Node.js >= 16.0.0, Koa.js v2.x, @koa/router v10.x

## ❓ Common Questions Quick Index
- **Q: How do I get available gift cards?** → [Get Gift Cards Endpoint](#get-gift-cards-endpoint)
- **Q: What gift card categories are available?** → [Gift Card Categories](#gift-card-categories)
- **Q: How are points calculated for gift cards?** → [Points Calculation](#points-calculation)
- **Q: What authentication is required?** → JWT authentication with userid header
- **Q: How does event tracking work?** → [Event Tracking](#event-tracking)
- **Q: What's the currency format?** → All amounts are multiplied by 100 (cents)

## 📋 Functionality Overview

**Non-technical explanation:** 
Think of this as a **digital rewards catalog** in a customer loyalty program. When users earn points through using transportation services, they can "shop" for gift cards from various retailers. This controller acts like the catalog display, showing all available gift cards organized by category (like "Coffee Shops", "Gas Stations", "Restaurants") with their point costs and values.

**Technical explanation:** 
A simple Koa.js REST controller that retrieves gift card categories and associated gift card items from the database, formats the response for mobile consumption, and tracks user engagement with the rewards system through event logging.

**Business value explanation:**
This controller enables the rewards/loyalty program feature that incentivizes user engagement with the MaaS platform. By offering tangible rewards (gift cards), it encourages continued platform usage and helps with user retention.

## 🔧 Technical Specifications

- **File:** `allrepo/connectsmart/tsp-api/src/controllers/gift-cards.js`
- **Language:** JavaScript (ES2020)
- **Framework:** Koa.js v2.x with @koa/router
- **Type:** REST API Controller
- **File Size:** ~1.2 KB
- **Complexity Score:** ⭐ (Low - Simple data retrieval and formatting)

**Dependencies:**
- `@koa/router`: HTTP routing framework (**Critical**)
- `koa-bodyparser`: Request body parsing (**Critical**)
- `@maas/core/response`: Standardized success response formatting (**High**)
- `@app/src/middlewares/auth`: JWT authentication middleware (**Critical**)
- `@app/src/models/GiftCardCategory`: Category data model (**Critical**)
- `@app/src/models/GiftCards`: Gift card items model (**Critical**)
- `@app/src/helpers/send-event`: Event tracking helper (**Medium**)

## 📝 Detailed Code Analysis

### Get Gift Cards Endpoint (`GET /giftcards`)

**Authentication:** Requires JWT token and userid header

**Execution Flow:**
1. **Category Retrieval:** Fetches all gift card categories from `GiftCardCategory` table
2. **Item Aggregation:** For each category, retrieves associated gift card items
3. **Data Formatting:** 
   - Sets `display_rate` to 100% for all items
   - Converts amounts to cents (multiplies by 100)
   - Parses points as float values
4. **Event Tracking:** Logs a `visit_rewards` event for analytics
5. **Response:** Returns structured gift card data grouped by category

**Data Transformation:**
```javascript
// Amount conversion (dollars to cents)
item.amount *= 100;

// Points parsing
item.points = parseFloat(item.points);

// Display rate standardization
item.display_rate = 100;
```

**Category Structure:**
```javascript
{
  category_id: number,
  name: string,
  image: string,
  items: [{
    id: number,
    currency: string,
    amount: number, // in cents
    points: number,
    display_rate: 100
  }]
}
```

## 🚀 Usage Methods

### Basic Gift Cards Retrieval
```bash
curl -X GET "https://api.tsp.example.com/api/v1/giftcards" \
  -H "Authorization: Bearer <JWT_TOKEN>" \
  -H "userid: usr_12345"
```

### JavaScript Fetch Example
```javascript
async function getGiftCards() {
  const response = await fetch('/api/v1/giftcards', {
    headers: {
      'Authorization': `Bearer ${authToken}`,
      'userid': userId
    }
  });
  
  if (response.ok) {
    const data = await response.json();
    return data.data.giftcards;
  }
}
```

## 📊 Output Examples

### Successful Response
```json
{
  "result": "success",
  "data": {
    "giftcards": [
      {
        "category_id": 1,
        "name": "Coffee & Food",
        "image": "https://example.com/coffee-category.jpg",
        "items": [
          {
            "id": 101,
            "currency": "USD",
            "amount": 500,
            "points": 50.0,
            "display_rate": 100
          },
          {
            "id": 102,
            "currency": "USD", 
            "amount": 1000,
            "points": 100.0,
            "display_rate": 100
          }
        ]
      },
      {
        "category_id": 2,
        "name": "Gas Stations",
        "image": "https://example.com/gas-category.jpg",
        "items": [
          {
            "id": 201,
            "currency": "USD",
            "amount": 2500,
            "points": 250.0,
            "display_rate": 100
          }
        ]
      }
    ]
  }
}
```

### Authentication Error (401)
```json
{
  "error": "AuthenticationError",
  "message": "Invalid or expired JWT token",
  "code": "AUTH_TOKEN_INVALID"
}
```

## ⚠️ Important Notes

### Currency Handling
- All monetary amounts are returned in cents (multiplied by 100)
- Frontend applications must divide by 100 for display purposes
- Supports multiple currencies but currently defaults to USD

### Event Tracking
The endpoint automatically tracks user engagement:
- **Event Name:** `visit_event`
- **Event Meta:** `{ action: 'visit_rewards' }`
- **Purpose:** Analytics for rewards program optimization

### Data Consistency
- `display_rate` is hardcoded to 100 for all items
- Points values are parsed as floats for precision
- Categories without items will still appear in the response with empty items array

### Performance Considerations
- Uses `Promise.all` for concurrent database queries per category
- Single database round trip for categories, then parallel fetching of items
- Lightweight data transformation suitable for mobile clients

## 🔗 Related File Links

- **Database Models:** 
  - `allrepo/connectsmart/tsp-api/src/models/GiftCardCategory.js`
  - `allrepo/connectsmart/tsp-api/src/models/GiftCards.js`
- **Authentication:** `allrepo/connectsmart/tsp-api/src/middlewares/auth.js`
- **Event Tracking:** `allrepo/connectsmart/tsp-api/src/helpers/send-event.js`

---
*This controller provides the foundation for the loyalty rewards system, enabling users to redeem earned points for gift cards.*