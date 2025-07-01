# DuoValidatedResult Model Documentation

## 📋 Model Overview
- **Purpose:** Stores results of Duo (paired ride) validation processes
- **Table/Collection:** duo_validated_result
- **Database Type:** MySQL
- **Relationships:** Links to carpool/rideshare validation system

## 🔧 Schema Definition
Schema details not explicitly defined in model file. This table likely stores validation results for Duo (paired) ride requests.

## 🔑 Key Information
- **Primary Key:** Likely id (standard MySQL convention)
- **Indexes:** Not defined in model (handled at database level)
- **Unique Constraints:** Not defined in model
- **Default Values:** Not defined in model

## 📝 Usage Examples
```javascript
// Query validation results
const validationResults = await DuoValidatedResult.query()
  .where('trip_id', 12345);

// Find successful validations
const successfulValidations = await DuoValidatedResult.query()
  .where('validation_status', 'success')
  .orderBy('validated_at', 'desc');

// Create new validation result
const result = await DuoValidatedResult.query()
  .insert({
    trip_id: 12345,
    rider_id: 67890,
    driver_id: 54321,
    validation_status: 'success',
    validation_data: JSON.stringify({...}),
    validated_at: new Date()
  });
```

## 🔗 Related Models
- **Trip models** - Related to ride validation
- **User models** - Referenced by rider_id and driver_id
- **Carpool models** - Part of carpool matching system
- **EscrowDetail** - Related to payment processing (see ESCROW_ACTIVITY_DEC_DUO_VALIDATION_FAIL)

## 📌 Important Notes
- Missing Model import from 'objection' (implementation issue)
- Critical for Duo ride validation and verification
- Likely includes validation status, timestamps, and validation data
- Connected to 'portal' MySQL database
- Important for ride safety and fraud prevention
- Results may affect escrow transactions (see EscrowDetail activity types)

## 🏷️ Tags
**Keywords:** duo, validation, ride, carpool, verification, trip
**Category:** #model #database #mysql #validation #carpool