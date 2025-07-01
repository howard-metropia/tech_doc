# Job Documentation: change-trip-incentive-rule_202150101.js

## 📋 Job Overview
- **Purpose:** Applies trip incentive rule changes scheduled for January 1, 2025
- **Type:** One-time migration
- **Schedule:** Manual trigger only
- **Impact:** Updates trip incentive rules in the database for new year rollout

## 🔧 Technical Details
- **Dependencies:** @app/src/services/incentiveRule service
- **Database Operations:** TripIncentiveRules table modifications
- **Key Operations:** Executes rule_20250101() function to update incentive configurations

## 📝 Code Summary
```javascript
const { rule_20250101 } = require('@app/src/services/incentiveRule');

module.exports = {
  inputs: {},
  fn: async function () {
    await rule_20250101();
  },
};
```

## ⚠️ Important Notes
- This is a future-dated migration script for New Year 2025 rule changes
- Should only be run once in production environments on or after January 1, 2025
- No rollback mechanism built into this job - database backup recommended before execution
- Success depends on the incentiveRule service being properly configured
- Coordinate timing with New Year operational schedules

## 📊 Example Output
```
// Output depends on rule_20250101() implementation
// Typically logs rule updates and affected user counts
```

## 🏷️ Tags
**Keywords:** trip-incentive, rule-migration, 2025-01-01, incentive-rules, new-year
**Category:** #job #migration #trip-incentive #rule-update #future-dated

---
Note: This job applies New Year 2025 incentive rule changes and should be coordinated with product team deployment schedules.