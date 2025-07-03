# AIResponseLog Model

## Overview
MongoDB model for logging AI service responses and interactions for monitoring and analytics.

## File Location
`/src/models/AIResponseLog.js`

## Database Configuration
- **Connection**: MongoDB cache database
- **Collection**: `ai_response_log`
- **Framework**: Mongoose ODM

## Schema Definition

```javascript
const schema = new mongoose.Schema({
    feature: String,        // AI feature identifier
    action_source: String,  // Source of the AI action
    ai_model: String,      // AI model used
    message: String,       // Response message
    prompt: String,        // Input prompt
    parameters: Object,    // Additional parameters
    datetime: Date         // Timestamp
});
```

## Fields

### feature
- **Type**: String
- **Purpose**: Identifies which AI feature generated the response
- **Examples**: "trip_recommendation", "route_optimization", "customer_support"

### action_source
- **Type**: String
- **Purpose**: Source system or component that triggered the AI action
- **Examples**: "mobile_app", "web_dashboard", "api_endpoint"

### ai_model
- **Type**: String
- **Purpose**: Identifies the specific AI model used
- **Examples**: "gpt-3.5-turbo", "custom_route_model", "recommendation_engine"

### message
- **Type**: String
- **Purpose**: The actual response message from the AI
- **Content**: Generated text, recommendations, or analysis results

### prompt
- **Type**: String
- **Purpose**: The input prompt sent to the AI model
- **Content**: User questions, system requests, or data inputs

### parameters
- **Type**: Object
- **Purpose**: Additional configuration or context parameters
- **Content**: Model settings, user preferences, system context

### datetime
- **Type**: Date
- **Purpose**: Timestamp of when the AI response was generated
- **Format**: ISO 8601 date format

## Usage Context
- **AI Monitoring**: Track AI service usage and performance
- **Analytics**: Analyze AI interaction patterns
- **Debugging**: Troubleshoot AI-related issues
- **Audit Trail**: Maintain records of AI decisions

## Related Components
- AI service integration modules
- Analytics and monitoring systems
- Customer support tools
- Performance tracking dashboards