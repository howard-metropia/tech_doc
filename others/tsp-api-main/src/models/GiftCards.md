# GiftCards Model Documentation

## 📋 Model Overview
- **Purpose:** Manages gift card products available for purchase and redemption in the platform
- **Table/Collection:** giftcard
- **Database Type:** MySQL
- **Relationships:** 
  - belongsTo: GiftCardCategory (via category_id)
  - hasMany: RedemptionTransactions (via giftcard_id)

## 🔧 Schema Definition
| Field Name | Type | Required | Description |
|------------|------|----------|-------------|
| id | int(11) | Yes | Primary key, auto-increment |
| category_id | int(11) | Yes | Gift card category ID |
| utid | varchar(50) | Yes | Unique transaction/product ID |
| points | decimal(10,2) | Yes | Points required for redemption |
| amount | int(11) | Yes | Gift card monetary value |
| currency | varchar(3) | Yes | Currency code (e.g., USD) |
| is_special_offer | tinyint(4) | No | Special offer flag, default 0 |

## 🔑 Key Information
- **Primary Key:** id
- **Indexes:** None specified in schema
- **Unique Constraints:** None
- **Default Values:** is_special_offer: 0

## 📝 Usage Examples
```javascript
// Get all available gift cards
const giftCards = await GiftCards.query()
  .withGraphFetched('category');

// Create a new gift card
const newCard = await GiftCards.query().insert({
  category_id: 1,
  utid: 'AMZN_25_001',
  points: 2500.00,
  amount: 25,
  currency: 'USD',
  is_special_offer: 1
});

// Find special offers
const specialOffers = await GiftCards.query()
  .where('is_special_offer', 1);

// Get gift cards by category
const restaurantCards = await GiftCards.query()
  .where('category_id', 2)
  .withGraphFetched('category');
```

## 🔗 Related Models
- `GiftCardCategory` - Categories for organizing gift cards
- `RedemptionTransaction` - Records of gift card redemptions
- `PointsTransaction` - Points deducted for redemptions

## 📌 Important Notes
- Points-based redemption system
- Support for multiple currencies
- Special offer flag for promotional campaigns
- UTID provides unique identification for external systems
- Category-based organization for better UX
- Monetary amounts stored as integers (cents)

## 🏷️ Tags
**Keywords:** gift-cards, rewards, redemption, points, ecommerce, loyalty
**Category:** #model #database #rewards #ecommerce #loyalty #gift-cards