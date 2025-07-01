# CMUserRecords Model Documentation

## 📋 Model Overview
- **Purpose:** Stores Campaign Management (CM) user records for marketing and engagement tracking
- **Table/Collection:** cm_user_record
- **Database Type:** MySQL (portal database)
- **Relationships:** Related to AuthUsers and campaign management systems

## 🔧 Schema Definition
| **Field Name** | **Type** | **Required** | **Description** |
|----------------|----------|--------------|-----------------|
| id | INT | Yes | Primary key, auto-increment |
| user_id | INT | Yes | Foreign key to auth_user table |
| campaign_id | INT | No | Campaign identifier |
| record_type | VARCHAR | No | Type of record (engagement/action/conversion) |
| event_name | VARCHAR | No | Specific event or action name |
| event_data | JSON | No | Additional event metadata |
| timestamp | TIMESTAMP | Yes | Event occurrence timestamp |
| session_id | VARCHAR | No | User session identifier |
| device_type | VARCHAR | No | Device type (mobile/web/tablet) |
| source | VARCHAR | No | Traffic source or referrer |
| created_at | TIMESTAMP | Yes | Record creation timestamp |

## 🔑 Key Information
- **Primary Key:** id
- **Indexes:** user_id, campaign_id, timestamp, event_name
- **Unique Constraints:** None
- **Default Values:** created_at = CURRENT_TIMESTAMP

## 📝 Usage Examples
```javascript
// Basic query example
const userRecords = await CMUserRecords.query()
  .where('user_id', userId)
  .orderBy('timestamp', 'desc');

// Get campaign engagement records
const campaignRecords = await CMUserRecords.query()
  .where('campaign_id', campaignId)
  .where('record_type', 'engagement')
  .whereRaw('timestamp >= DATE_SUB(NOW(), INTERVAL 30 DAY)');

// Track specific events
const conversions = await CMUserRecords.query()
  .where('event_name', 'trip_completed')
  .where('timestamp', '>=', startDate);
```

## 🔗 Related Models
- `AuthUsers` - Many-to-one relationship via user_id
- Campaign management tables - Related via campaign_id
- User analytics and behavior tracking systems

## 📌 Important Notes
- Used for marketing campaign effectiveness tracking
- Event_data field stores flexible JSON metadata
- Session tracking helps understand user journey
- Device and source fields support attribution analysis

## 🏷️ Tags
**Keywords:** campaigns, marketing, events, tracking, analytics
**Category:** #model #database #analytics #mysql

---
Note: Essential for measuring campaign performance and user engagement metrics.