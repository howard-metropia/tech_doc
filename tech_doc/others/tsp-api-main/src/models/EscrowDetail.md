# EscrowDetail Model Documentation

## 📋 Model Overview
- **Purpose:** Manages escrow transaction details for payment processing and activity tracking
- **Table/Collection:** escrow_detail or escrow_detail_upgrade (config-dependent)
- **Database Type:** MySQL
- **Relationships:** Links to payment transactions and user activities

## 🔧 Schema Definition
Dynamic table name based on configuration:
- Uses `escrow_detail` when config.pointsTransactionSchema === 'points_transaction'
- Uses `escrow_detail_upgrade` otherwise

Schema details not explicitly defined in model (handled by database).

## 🔑 Key Information
- **Primary Key:** Likely id (standard MySQL convention)
- **Indexes:** Not defined in model
- **Unique Constraints:** Not defined in model
- **Default Values:** Not defined in model

## Activity Types Constants
The model defines 26 different escrow activity types:
- **ESCROW_ACTIVITY_INIT** (0) - Initial escrow setup
- **ESCROW_ACTIVITY_INC_FEE_RIDER** (1) - Increase rider fee
- **ESCROW_ACTIVITY_INC_FEE_DRIVER** (2) - Increase driver fee
- **ESCROW_ACTIVITY_INC_PREMIUM** (3) - Increase premium
- **ESCROW_ACTIVITY_DEC_PAY_TO_DRIVER** (17) - Decrease payment to driver
- **ESCROW_ACTIVITY_DEC_EXPIRED** (22) - Decrease due to expiration
- **ESCROW_ACTIVITY_DEC_DUO_VALIDATION_FAIL** (25) - Decrease due to validation failure

## 📝 Usage Examples
```javascript
// Query escrow details
const escrowDetails = await EscrowDetail.query().where('user_id', 12345);

// Use activity type constants
const activityType = EscrowDetail.activityTypes.ESCROW_ACTIVITY_INIT;

// Filter by activity type
const initActivities = await EscrowDetail.query()
  .where('activity_type', EscrowDetail.activityTypes.ESCROW_ACTIVITY_INIT);
```

## 🔗 Related Models
- **User models** - Referenced through user_id fields
- **Transaction models** - Related to payment processing
- **Carpool/Rideshare models** - Many activity types relate to carpooling

## 📌 Important Notes
- Dynamic table selection based on configuration schema
- Extensive activity type enumeration for detailed transaction tracking
- Designed for complex escrow workflows with carpool/rideshare operations
- Activity types cover both increases and decreases in escrow amounts
- Critical for financial transaction auditing and reconciliation

## 🏷️ Tags
**Keywords:** escrow, payment, transaction, activity, financial, carpool
**Category:** #model #database #mysql #financial #transaction