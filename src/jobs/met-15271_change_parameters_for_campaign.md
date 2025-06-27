# MET-15271: Change Parameters for Campaign

## 📋 Job Overview
- **Purpose:** Activates enhanced incentive parameters for campaign promotion across all sustainable modes
- **Type:** One-time migration / Campaign activation trigger
- **Schedule:** Campaign start date with end date set to year 3000 (until manually changed)
- **Impact:** TripIncentiveRules table - increases incentives for sustainable transportation modes

## 🔧 Technical Details
- **Dependencies:** TripIncentiveRules model, @maas/core/log
- **Database Operations:** Updates all transportation mode incentives with campaign values
- **Key Operations:** Sets campaign-level incentives with extended end date for long-term promotion

## 📝 Code Summary
```javascript
const rule = await tripIncentiveRules.findOne({ market: 'HCS' });
rule.set('start', Math.floor(new Date().getTime() / 1000));
rule.set('end', Math.floor(new Date('3000-12-31T23:59:59.999Z').getTime() / 1000));
rule.modes.intermodal = { distance: 2, mean: 0.75, min: 0.5, max: 1, beta: 0.3 };
rule.modes.biking = { distance: 1, mean: 0.5, min: 0.25, max: 0.75, beta: 0.1 };
```

## ⚠️ Important Notes
- Sets campaign end date to year 3000 (effectively permanent until manually changed)
- Increases incentives for sustainable modes (intermodal, duo, biking, walking, public_transit)
- Maintains standard rates for driving and trucking
- Requires manual intervention to end campaign

## 📊 Example Output
```
Campaign incentives activated for all sustainable transportation modes
Enhanced modes: intermodal, duo, instant_duo, biking, walking, public_transit
Campaign end date: 3000-12-31 (manual intervention required to end)
Market: HCS
```

## 🏷️ Tags
**Keywords:** campaign-activation, enhanced-incentives, sustainable-transport, long-term, houston
**Category:** #job #campaign #incentive-management #sustainability #long-term