# Job Documentation: add-trip-incentive-rules.js

## 📋 Job Overview
- **Purpose:** Adds trip incentive rules for HCS market with predefined parameters
- **Type:** One-time migration / Setup task
- **Schedule:** Manual trigger only
- **Impact:** Creates new incentive rules in TripIncentiveRules table for HCS market

## 🔧 Technical Details
- **Dependencies:** @maas/core/log, @app/src/models/TripIncentiveRules
- **Database Operations:** Query and insert operations on TripIncentiveRules table
- **Key Operations:** Checks for existing HCS rule, creates new rule if not found

## 📝 Code Summary
```javascript
const rule = await tripIncentiveRules.findOne({ market: 'HCS' });
if (!rule) {
  await tripIncentiveRules.create({
    "market": "HCS",
    "D": 300, "h": 2, "d1": 500, "d2": 500, "L": 5, "W": 0.99,
    "modes": {
      "intermodal": { "distance": 2, "mean": 0.2, "min": 0.11, "max": 0.6, "beta": 0.1 },
      "driving": { "distance": 2, "mean": 0.1, "min": 0.055, "max": 0.5, "beta": 0.05 },
      // ... additional transport modes
    }
  });
}
```

## ⚠️ Important Notes
- Safe to run multiple times - checks for existing rules before creating
- Hardcoded incentive parameters specific to HCS market
- Covers multiple transport modes: intermodal, driving, duo, biking, walking, public transit, trucking
- No rollback mechanism - manual deletion required if rule needs removal
- Validate incentive parameters match business requirements before execution

## 📊 Example Output
```
[add-trip-incentive-rules] Adding new rule for market [HCS]
// OR
[add-trip-incentive-rules] Rule existed for market [HCS]
```

## 🏷️ Tags
**Keywords:** trip-incentive, hcs-market, incentive-rules, setup, transport-modes
**Category:** #job #migration #trip-incentive #setup #market-config

---
Note: This job sets up incentive parameters for HCS market across all supported transportation modes.