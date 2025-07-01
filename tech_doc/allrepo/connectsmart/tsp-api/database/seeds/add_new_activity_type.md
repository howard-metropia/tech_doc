# New Activity Type Seed

## 📋 Seed Overview
- **Purpose:** Adds ParkMobile transaction fee activity type for parking service integration
- **Environment:** All environments (extends core activity types)
- **Dependencies:** activity_type table and init.js seed must run first
- **Idempotent:** No (will fail if ID 14 already exists)

## 🔧 Data Summary
```javascript
// New activity type
{
  table: 'activity_type',
  data: {
    id: 14,
    name: 'park-mobile-transaction',
    description: 'ParkMobile on-street parking transaction fee'
  }
}
```

## 📝 Affected Tables
| Table | Records | Description |
|-------|---------|-------------|
| activity_type | 1 | Adds ParkMobile transaction fee type |

## ⚠️ Important Notes
- **Extension Seed:** Adds to existing activity types from init.js
- **ParkMobile Integration:** Specific to on-street parking payment processing
- **Transaction Fees:** Handles transaction fee charges separate from parking fees
- **ID Conflict:** Will fail if activity_type ID 14 already exists
- **Error Handling:** Throws errors on failure (does not rollback silently)
- **Order Dependency:** Must run after init.js establishes base activity types

## 🏷️ Tags
**Keywords:** activity-type, parkmobile, parking, transaction-fee, payment-processing
**Category:** #seed #data #activity-type #parkmobile #parking #fees