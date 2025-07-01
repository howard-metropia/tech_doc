# Initial Database Seed

## 📋 Seed Overview
- **Purpose:** Core system initialization with essential data for application startup and testing
- **Environment:** All environments (development, testing, production)
- **Dependencies:** Must run after all migrations are applied
- **Idempotent:** Yes (deletes existing data before inserting)

## 🔧 Data Summary
```javascript
// Core system data categories
{
  app_update: [
    { app_version: '1.97.3', app_os: 'android', is_required: 'T' },
    { app_version: '1.3.2', app_os: 'ios', is_required: 'T' }
  ],
  activity_type: [
    { id: 1, name: 'adjustment', description: 'Adjust coin' },
    { id: 6, name: 'incentive', description: 'Incentive' },
    // ... 11 total activity types
  ],
  travel_mode: [
    { id: 1, name: 'driving' },
    { id: 2, name: 'public_transit' },
    { id: 100, name: 'duo' }
    // ... 8 total travel modes
  ],
  auth_user: [
    { id: 1001, email: 'test2@metropia.com' }
    // ... 4 test users
  ]
}
```

## 📝 Affected Tables
| Table | Records | Description |
|-------|---------|-------------|
| app_update | 2 | Android/iOS app version requirements |
| activity_type | 11 | Point transaction activity types |
| auth_user | 4 | Test user accounts |
| travel_mode | 8 | Transportation mode definitions |
| notification_type | 1 | Basic notification category |
| refill_plan | 1 | Wallet auto-refill configuration |
| user_wallet | 1 | Test user wallet with balance |
| points_transaction | 1 | Sample points transaction |
| token_transaction | 1 | Sample token transaction |

## ⚠️ Important Notes
- **Destructive:** Deletes all existing data in affected tables
- **Test Data:** Includes test users and sample transactions
- **Activity Types:** Must match PointsTransaction.activityTypes constants
- **Travel Modes:** Core transportation modes including 'duo' for carpool
- **Auto-Refill Setup:** Includes Stripe customer integration example
- **Sequential Dependencies:** Some operations depend on previous insertions

## 🏷️ Tags
**Keywords:** initialization, core-data, activity-types, travel-modes, test-users, app-versions
**Category:** #seed #data #initialization #core #test-data