# CloudMessage Model Documentation

## 📋 Model Overview
- **Purpose:** Stores cloud messaging data for push notifications and communication services
- **Table/Collection:** cloud_message
- **Database Type:** MongoDB
- **Relationships:** Standalone collection with flexible schema

## 🔧 Schema Definition
| Field Name | Type | Required | Description |
|------------|------|----------|-------------|
| * | Mixed | No | Flexible schema allows any message fields |

## 🔑 Key Information
- **Primary Key:** _id (MongoDB ObjectId)
- **Indexes:** Default _id index
- **Unique Constraints:** None
- **Default Values:** None
- **Schema Options:** strict: false (allows any fields)

## 📝 Usage Examples
```javascript
// Store push notification message
const message = await CloudMessage.create({
  messageId: 'msg_123',
  userId: 456,
  title: 'Trip Reminder',
  body: 'Your trip starts in 10 minutes',
  data: {
    tripId: 789,
    action: 'trip_reminder'
  },
  timestamp: new Date(),
  platform: 'fcm',
  status: 'sent'
});

// Query messages by user
const userMessages = await CloudMessage.find({
  userId: 456
}).sort({ timestamp: -1 });

// Update message status
await CloudMessage.updateOne(
  { messageId: 'msg_123' },
  { $set: { status: 'delivered', deliveredAt: new Date() } }
);
```

## 🔗 Related Models
- May reference user data for messaging
- Integrates with notification systems
- Supports various messaging platforms

## 📌 Important Notes
- Extremely flexible schema for various message types
- Can store FCM, APNS, or other cloud messaging data
- Supports custom message properties and metadata
- No strict validation allows for evolving message formats
- Useful for debugging and message tracking
- Platform-agnostic message storage

## 🏷️ Tags
**Keywords:** cloud-messaging, notifications, push, mongodb, flexible-schema, communications
**Category:** #model #database #messaging #notifications #mongodb #communications