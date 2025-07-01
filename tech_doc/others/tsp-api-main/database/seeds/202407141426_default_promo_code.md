# 202407141426_default_promo_code.js Seed Documentation

## 📋 Seed Overview
- **Purpose:** Creates default promo code campaigns for Houston ConnectSmart
- **Environment:** Production and staging environments
- **Dependencies:** Both portal and admin databases, timezone configuration
- **Idempotent:** No (generates new IDs, avoid running multiple times)

## 🔧 Data Summary
```javascript
{
  campaigns: [
    { promoCode: 'TESTEXPIREDCODE', perToken: 10, expired: true },
    { promoCode: 'TESTPROMOCODE', perToken: 10, active: true },
    { promoCode: 'BACK2SCHOOL', perToken: 10, seasonal: true },
    { promoCode: 'LETSRIDE', perToken: 10, promotional: true }
  ]
}
```

## 📝 Affected Tables
| Table | Records | Description |
|-------|---------|-------------|
| campaigns (admin) | 4 | Admin platform campaign entries |
| tokens (admin) | 4 | Token definitions with 999999 cap |
| give_aways (admin) | 4 | Auto-dispatch prize distribution |
| agency | 4 | Houston ConnectSmart agency records |
| token_campaign | 4 | Token campaign configurations |
| campaign | 4 | Campaign records with token links |
| campaign_promo_code | 4 | Promo code to campaign mappings |

## ⚠️ Important Notes
- Creates both active and expired test campaigns
- Uses America/Chicago timezone for date handling
- Admin platform IDs auto-increment from 1000+
- Includes one expired campaign (TESTEXPIREDCODE) for testing
- All tokens have 999999 cap with auto-dispatch enabled
- Projects are auto-created if none exist

## 🏷️ Tags
**Keywords:** default-promo-codes, houston-connectsmart, campaigns, testing  
**Category:** #seed #campaigns #promo-codes #default-data

---
Note: Establishes baseline promo code campaigns for Houston ConnectSmart operations.