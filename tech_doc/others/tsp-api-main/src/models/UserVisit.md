# UserVisit Model

## 📋 Model Overview
- **Purpose:** Tracks user visit events with location and timing data
- **Table/Collection:** user_visit
- **Database Type:** MongoDB (cache)
- **Relationships:** None defined

## 🔧 Schema Definition
- **user_id** | **Number** | **Optional** | **User identifier**
- **arrival_date** | **Number** | **Optional** | **Visit arrival timestamp**
- **departure_date** | **Number** | **Optional** | **Visit departure timestamp**
- **longitude** | **String** | **Optional** | **Visit location longitude**
- **latitude** | **String** | **Optional** | **Visit location latitude**
- **os_type** | **String** | **Optional** | **User device OS type**

## 🔑 Key Information
- **Primary Key:** MongoDB ObjectId
- **Indexes:** Not specified
- **Unique Constraints:** Not specified
- **Default Values:** None specified

## 📝 Usage Examples
```javascript
// Create user visit record
const visit = new UserVisit({
  user_id: 123,
  arrival_date: Date.now(),
  latitude: '29.7604',
  longitude: '-95.3698',
  os_type: 'iOS'
});
await visit.save();

// Find user visits
const userVisits = await UserVisit.find({ user_id: 123 });
```

## 🔗 Related Models
- No explicit relationships defined
- Part of user analytics and tracking system

## 📌 Important Notes
- Tracks visit duration with arrival/departure timestamps
- Coordinates stored as strings instead of numbers
- Includes device OS information for analytics
- Cache database for performance

## 🏷️ Tags
**Keywords:** user, visit, location, tracking, analytics
**Category:** #model #database #user #visit #tracking #mongodb