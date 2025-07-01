# MET-15558: Bike Week Campaign End

## 📋 Job Overview
- **Purpose:** Reverts cycling incentives to default values after Bike Week campaign ends
- **Type:** One-time migration / Scheduled campaign trigger
- **Schedule:** Executed on 2024-05-18 06:00:00 UTC to end campaign
- **Impact:** TripIncentiveRules table - restores cycling incentive parameters for HCS market

## 🔧 Technical Details
- **Dependencies:** TripIncentiveRules model, @maas/core/log
- **Database Operations:** Updates cycling mode incentives in trip_incentive_rules table
- **Key Operations:** Restores cycling incentive rates to default values

## 📝 Code Summary
```javascript
const rule = await tripIncentiveRules.findOne({ market: 'HCS' });
rule.modes.biking = {
  distance: 1,
  mean: 0.2,      // Restored from 0.5
  min: 0.1,       // Restored from 0.25
  max: 0.4,       // Restored from 0.75
  beta: 0.1
};
```

## ⚠️ Important Notes
- Companion job to met-15558_bike_week_campaign_start
- Must run after campaign period to avoid ongoing elevated incentives
- Specific to HCS (Houston) market
- Logs success/failure for monitoring

## 📊 Example Output
```
[met-15558_bike_week_campaign_end] incentives for cycling have been reverted back to default values
Before: mean=0.5, min=0.25, max=0.75
After:  mean=0.2, min=0.1, max=0.4
```

## 🏷️ Tags
**Keywords:** bike-week, campaign, incentives, cycling, houston, revert
**Category:** #job #campaign #incentive-management #cycling #temporal #cleanup