# PmParkingEvent Model

## 📋 Model Overview
- **Purpose:** Stores parking management events and transactions
- **Table/Collection:** pm_parking_event
- **Database Type:** MySQL (portal)
- **Relationships:** None defined

## 🔧 Schema Definition
*Schema fields are not explicitly defined in the model. Database table structure would need to be verified.*

## 🔑 Key Information
- **Primary Key:** Not explicitly defined (likely `id`)
- **Indexes:** Not specified
- **Unique Constraints:** Not specified
- **Default Values:** Not specified

## 📝 Usage Examples
```javascript
// Basic query example
const events = await PmParkingEvent.query().where('status', 'active');

// Get events by user
const userEvents = await PmParkingEvent.query().where('user_id', 123);
```

## 🔗 Related Models
- No explicit relationships defined
- Likely related to parking and user models

## 📌 Important Notes
- Minimal model with only table name definition
- Part of parking management system
- Uses Objection.js ORM with MySQL portal database
- PM prefix suggests "Parking Management"

## 🏷️ Tags
**Keywords:** parking, event, management, transaction
**Category:** #model #database #parking #event #management