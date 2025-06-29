# MET-15558: Bike Week Campaign Start

## 📋 Job Overview
- **Purpose:** Activates enhanced incentives for cycling during Bike Week campaign (May 13-17)
- **Type:** One-time migration / Scheduled campaign trigger
- **Schedule:** Executed on 2024-05-13 05:00:00 UTC to start campaign
- **Impact:** TripIncentiveRules table - updates cycling incentive parameters for HCS market

## 🔧 Technical Details
- **Dependencies:** TripIncentiveRules model, @maas/core/log
- **Database Operations:** Updates cycling mode incentives in trip_incentive_rules table
- **Key Operations:** Increases cycling incentive rates for campaign period

## 📝 Code Summary
```javascript
const rule = await tripIncentiveRules.findOne({ market: 'HCS' });
rule.modes.biking = {
  distance: 1,
  mean: 0.5,      // Increased from 0.2
  min: 0.25,      // Increased from 0.1
  max: 0.75,      // Increased from 0.4
  beta: 0.1
};
```

## ⚠️ Important Notes
- Only affects cycling incentives, other modes remain at default settings
- Specific to HCS (Houston) market
- Must be paired with corresponding campaign end job (met-15558_bike_week_campaign_end)
- Logs success/failure for monitoring

## 📊 Example Output
```
[met-15558_bike_week_campaign_start] incentives for cycling have been set to campaign values
Before: mean=0.2, min=0.1, max=0.4
After:  mean=0.5, min=0.25, max=0.75
```

## 🏷️ Tags
**Keywords:** bike-week, campaign, incentives, cycling, houston
**Category:** #job #campaign #incentive-management #cycling #temporal