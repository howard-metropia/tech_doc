# TripIncentiveRules Model Documentation

## 📋 Model Overview
- **Purpose:** Defines dynamic incentive rules for trips based on market conditions and campaigns
- **Table/Collection:** trip_incentive_rules
- **Database Type:** MongoDB (cache database)
- **Relationships:** Referenced by trip validation and incentive calculation services

## 🔧 Schema Definition
| **Field Name** | **Type** | **Required** | **Description** |
|----------------|----------|--------------|-----------------|
| _id | ObjectId | Yes | MongoDB primary key |
| market | String | No | Market/region identifier |
| rules | Object | No | Dynamic rule definitions |
| incentive_type | String | No | Type of incentive (coins/points/discount) |
| travel_modes | Array | No | Applicable transportation modes |
| conditions | Object | No | Conditions for rule activation |
| reward_amount | Number | No | Base reward amount |
| multiplier | Number | No | Reward multiplier factor |
| valid_from | Date | No | Rule activation date |
| valid_until | Date | No | Rule expiration date |
| max_uses_per_user | Number | No | Usage limit per user |
| max_uses_total | Number | No | Total usage limit |
| status | String | No | Rule status (active/inactive/expired) |
| created_at | Date | No | Rule creation timestamp |
| updated_at | Date | No | Last modification timestamp |

## 🔑 Key Information
- **Primary Key:** _id (MongoDB ObjectId)
- **Indexes:** market, status, valid_from, valid_until
- **Unique Constraints:** None (flexible schema)
- **Default Values:** status = 'active'

## 📝 Usage Examples
```javascript
// Basic query example
const activeRules = await TripIncentiveRules.find({
  market: 'houston',
  status: 'active',
  valid_from: { $lte: new Date() },
  valid_until: { $gte: new Date() }
});

// Find rules for specific travel modes
const transitRules = await TripIncentiveRules.find({
  travel_modes: { $in: ['public_transit', 'intermodal'] },
  status: 'active'
});

// Get rules with high multipliers
const bonusRules = await TripIncentiveRules.find({
  multiplier: { $gte: 2.0 },
  max_uses_total: { $gt: 0 }
});
```

## 🔗 Related Models
- Trip validation services - Apply rules during trip processing
- Incentive calculation engines - Use rules for reward computation
- Market/region configuration tables

## 📌 Important Notes
- Flexible schema allows for complex rule definitions
- Rules can be market-specific or global
- Usage limits prevent abuse and control costs
- Conditions field enables sophisticated targeting logic

## 🏷️ Tags
**Keywords:** incentives, rules, rewards, campaigns, mongodb
**Category:** #model #database #incentives #mongodb

---
Note: Critical for dynamic incentive management and targeted user engagement campaigns.