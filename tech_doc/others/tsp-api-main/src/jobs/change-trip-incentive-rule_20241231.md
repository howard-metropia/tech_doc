# Change Trip Incentive Rule - 20241231

## 📋 Job Overview
- **Purpose:** Applies specific incentive rule changes scheduled for December 31, 2024
- **Type:** Scheduled task / One-time migration
- **Schedule:** Intended for execution on 2024-12-31
- **Impact:** TripIncentiveRules table - applies rule_20241231 incentive configuration

## 🔧 Technical Details
- **Dependencies:** incentiveRule service, rule_20241231 function
- **Database Operations:** Updates trip incentive rules via service layer
- **Key Operations:** Delegates to incentiveRule.rule_20241231() service function

## 📝 Code Summary
```javascript
const { rule_20241231 } = require('@app/src/services/incentiveRule');

module.exports = {
  inputs: {},
  fn: async function () {
    await rule_20241231();
  }
};
```

## ⚠️ Important Notes
- Implementation details are contained in the incentiveRule service
- Part of a series of dated incentive rule changes
- Minimal job wrapper - actual logic in service layer
- Date-specific rule change likely tied to year-end adjustments

## 📊 Example Output
```
Incentive rule changes applied for 2024-12-31
(Specific output depends on rule_20241231 service implementation)
```

## 🏷️ Tags
**Keywords:** incentive-rules, scheduled-change, year-end, rule-20241231
**Category:** #job #incentive-management #scheduled-task #service-wrapper #temporal