# Referral System Initial Data Seed

## 📋 Seed Overview
- **Purpose:** Initializes complete referral system with agency, token campaign, and reward program
- **Environment:** All environments (creates referral program infrastructure)
- **Dependencies:** Agency, TokenCampaigns, and Campaigns models must exist
- **Idempotent:** Yes (checks existence before creating)

## 🔧 Data Summary
```javascript
// Referral system components
{
  agency: {
    name: 'Houston ConnectSmart',
    ap_agency_id: '<next_available_id>'
  },
  token_campaign: {
    name: 'Referral Bonus',
    tokens: 5,
    issued_on: '2023-09-21 05:00:00',
    expired_on: '2024-01-03 05:59:59'
  },
  campaign: {
    name: 'Referral Program',
    tokens: 5
  }
}
```

## 📝 Affected Tables
| Table | Records | Description |
|-------|---------|-------------|
| agency | 1 | Houston ConnectSmart referral agency |
| token_campaigns | 1 | 5-token referral bonus campaign |
| campaigns | 1 | Main referral program campaign |

## ⚠️ Important Notes
- **ID Management:** Uses AP_DATA_START_IDX (1000) to separate hybrid vs admin platform data
- **Incremental IDs:** Automatically assigns next available ap_agency_id, ap_token_id, ap_campaign_id
- **Date-Limited:** Token campaign expires on 2024-01-03
- **Houston Specific:** Creates Houston ConnectSmart agency for referral program
- **5 Token Reward:** Standard referral bonus amount
- **Existence Checks:** Safe to run multiple times without duplication

## 🏷️ Tags
**Keywords:** referral-system, agency, token-campaign, rewards, houston-connectsmart
**Category:** #seed #data #referral #rewards #campaign #agency