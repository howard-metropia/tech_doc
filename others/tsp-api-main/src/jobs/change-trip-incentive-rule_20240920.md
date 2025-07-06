# Change Trip Incentive Rule - 20240920

## 📋 Job Overview
- **Purpose:** Applies specific incentive rule changes scheduled for September 20, 2024
- **Type:** Scheduled task / One-time migration
- **Schedule:** Intended for execution on 2024-09-20
- **Impact:** TripIncentiveRules table - applies rule_20240920 incentive configuration

## 🔧 Technical Details
- **Dependencies:** incentiveRule service, rule_20240920 function
- **Database Operations:** Updates trip incentive rules via service layer
- **Key Operations:** Delegates to incentiveRule.rule_20240920() service function

## 📝 Code Summary
```javascript
const { rule_20240920 } = require('@app/src/services/incentiveRule');

module.exports = {
  inputs: {},
  fn: async function () {
    await rule_20240920();
  }
};
```

## ⚠️ Important Notes
- Implementation details are contained in the incentiveRule service
- Part of a series of dated incentive rule changes
- Minimal job wrapper - actual logic in service layer
- September date suggests possible back-to-school or seasonal adjustment

## 📊 Example Output
```
Incentive rule changes applied for 2024-09-20
(Specific output depends on rule_20240920 service implementation)
```

## 🏷️ Tags
**Keywords:** incentive-rules, scheduled-change, september, rule-20240920
**Category:** #job #incentive-management #scheduled-task #service-wrapper #temporal