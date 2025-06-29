# MET-15272: Update Parameters to Default

## 📋 Job Overview
- **Purpose:** Resets all transportation mode incentive parameters to default values
- **Type:** One-time migration / Manual trigger
- **Schedule:** On-demand execution for parameter reset
- **Impact:** TripIncentiveRules table - updates all mode incentives for HCS market to baseline

## 🔧 Technical Details
- **Dependencies:** TripIncentiveRules model, @maas/core/log
- **Database Operations:** Updates all transportation mode incentives in trip_incentive_rules table
- **Key Operations:** Sets standardized incentive parameters across all modes

## 📝 Code Summary
```javascript
const rule = await tripIncentiveRules.findOne({ market: 'HCS' });
rule.modes = {
  intermodal: { distance: 2, mean: 0.6, min: 0.3, max: 0.8, beta: 0.3 },
  driving: { distance: 2, mean: 0.5, min: 0.25, max: 0.75, beta: 0.25 },
  biking: { distance: 1, mean: 0.2, min: 0.1, max: 0.4, beta: 0.1 },
  walking: { distance: 0.5, mean: 0.1, min: 0.05, max: 0.25, beta: 0.05 }
};
```

## ⚠️ Important Notes
- Affects all transportation modes (intermodal, driving, duo, biking, walking, public_transit, trucking)
- Specific to HCS (Houston) market
- Use this job to reset parameters after campaigns or testing
- Updates both created_on and modified_on timestamps

## 📊 Example Output
```
All transportation mode incentives reset to default values
Modes updated: intermodal, driving, duo, instant_duo, biking, walking, public_transit, trucking
Market: HCS
```

## 🏷️ Tags
**Keywords:** incentive-reset, default-parameters, all-modes, houston, baseline
**Category:** #job #incentive-management #parameter-reset #maintenance #baseline