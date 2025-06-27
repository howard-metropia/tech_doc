# Job Documentation: change-trip-incentive-rule_20240912.js

## 📋 Job Overview
- **Purpose:** Applies trip incentive rule changes deployed on September 12, 2024
- **Type:** One-time migration
- **Schedule:** Manual trigger only
- **Impact:** Updates trip incentive rules in the database

## 🔧 Technical Details
- **Dependencies:** @app/src/services/incentiveRule service
- **Database Operations:** TripIncentiveRules table modifications
- **Key Operations:** Executes rule_20240912() function to update incentive configurations

## 📝 Code Summary
```javascript
const { rule_20240912 } = require('@app/src/services/incentiveRule');

module.exports = {
  inputs: {},
  fn: async function () {
    await rule_20240912();
  },
};
```

## ⚠️ Important Notes
- This is a one-time migration script for a specific date-based rule change
- Should only be run once in production environments
- No rollback mechanism built into this job - database backup recommended before execution
- Success depends on the incentiveRule service being properly configured

## 📊 Example Output
```
// Output depends on rule_20240912() implementation
// Typically logs rule updates and affected user counts
```

## 🏷️ Tags
**Keywords:** trip-incentive, rule-migration, 2024-09-12, incentive-rules
**Category:** #job #migration #trip-incentive #rule-update

---
Note: This job applies date-specific incentive rule changes and should be coordinated with product team deployment schedules.