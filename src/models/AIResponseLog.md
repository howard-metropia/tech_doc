# AIResponseLog Model Documentation

## 📋 Model Overview
- **Purpose:** Logs AI model interactions, responses, and usage analytics for monitoring and debugging
- **Table/Collection:** ai_response_log
- **Database Type:** MongoDB
- **Relationships:** Standalone collection for AI analytics

## 🔧 Schema Definition
| Field Name | Type | Required | Description |
|------------|------|----------|-------------|
| feature | String | No | Feature/module that used AI |
| action_source | String | No | Source of the AI action/request |
| ai_model | String | No | AI model identifier used |
| message | String | No | AI response message |
| prompt | String | No | Input prompt sent to AI |
| parameters | Object | No | Request parameters and settings |
| datetime | Date | No | Timestamp of AI interaction |

## 🔑 Key Information
- **Primary Key:** _id (MongoDB ObjectId)
- **Indexes:** Default _id index
- **Unique Constraints:** None
- **Default Values:** None

## 📝 Usage Examples
```javascript
// Log AI interaction
const logEntry = await AIResponseLog.create({
  feature: 'trip_planning',
  action_source: 'user_request',
  ai_model: 'gpt-3.5-turbo',
  message: 'Best route from A to B is via public transit',
  prompt: 'Find optimal route from downtown to airport',
  parameters: {
    temperature: 0.7,
    max_tokens: 150
  },
  datetime: new Date()
});

// Query logs by feature
const tripPlanningLogs = await AIResponseLog.find({
  feature: 'trip_planning'
}).sort({ datetime: -1 });

// Get recent AI usage
const recentLogs = await AIResponseLog.find()
  .sort({ datetime: -1 })
  .limit(100);
```

## 🔗 Related Models
- Independent logging collection
- May reference various system features using AI
- Used for AI usage analytics and debugging

## 📌 Important Notes
- Comprehensive logging for AI interactions
- Stores both prompts and responses for analysis
- Parameters field captures model settings
- Essential for AI usage monitoring and optimization
- Supports debugging and performance analysis
- Feature-based categorization for analytics

## 🏷️ Tags
**Keywords:** ai-logging, analytics, monitoring, machine-learning, debugging, interactions
**Category:** #model #database #ai #logging #analytics #mongodb