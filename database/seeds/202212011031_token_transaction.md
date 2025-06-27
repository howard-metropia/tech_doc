# 202212011031_token_transaction Seed Documentation

### 📋 Seed Overview
- **Purpose:** Populate token transaction records with related campaign, agency, and token information
- **Environment:** All environments (dev, staging, production)
- **Dependencies:** token_transaction, token_campaign, agency, campaign tables must exist with proper foreign keys
- **Idempotent:** Yes (update operation based on existing data)

### 🔧 Data Summary
```javascript
{
  operation: 'UPDATE token_transaction with related campaign data',
  fields_updated: [
    'f_agency_id', 'agency_name', 'f_token_id', 'token_name',
    'f_campaign_id', 'campaign_name', 'issued_on', 'expired_on',
    'dist_notify_status', 'expire_notify_status', 'subtitle'
  ],
  subtitle_logic: 'METRO for activity_type=2, empty otherwise'
}
```

### 📝 Affected Tables
| Table | Records | Description |
|-------|---------|-------------|
| token_transaction | all existing | Updates with denormalized campaign/agency data |

### ⚠️ Important Notes
- Data denormalization operation for performance
- Complex JOIN operation across multiple tables
- Adds subtitle field with METRO branding for transit activities
- Uses Promise.all for batch updates
- Idempotent - safe to run multiple times

### 🏷️ Tags
**Keywords:** token-transaction, denormalization, campaign-data, performance-optimization
**Category:** #seed #data #migration #denormalization #tokens #campaigns

---
Note: This seed denormalizes related campaign and agency data into token transactions for improved query performance.