# MatchStatistics Model

## 📋 Model Overview
- **Purpose:** Stores match statistics data for carpool or rideshare matching analysis
- **Table/Collection:** match_statistic
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
const stats = await MatchStatistics.query().where('status', 'active');

// Get all match statistics
const allStats = await MatchStatistics.query();
```

## 🔗 Related Models
- No explicit relationships defined

## 📌 Important Notes
- Minimal model with only table name definition
- Uses Objection.js ORM with MySQL portal database
- Schema structure not defined in model file

## 🏷️ Tags
**Keywords:** match, statistics, carpool, rideshare
**Category:** #model #database #statistics #matching