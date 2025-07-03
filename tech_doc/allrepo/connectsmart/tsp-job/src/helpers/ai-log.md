# TSP Job Service - AI Log Helper

## Overview

The `src/helpers/ai-log.js` file provides AI interaction logging functionality for the TSP Job service. This helper module tracks AI model usage, API calls, and responses for monitoring, analytics, and debugging purposes within the MaaS platform.

## File Information

- **File Path**: `/src/helpers/ai-log.js`
- **File Type**: JavaScript Helper Module
- **Primary Purpose**: AI interaction logging and database storage
- **Dependencies**: @maas/core/log, AIResponseLog model, moment-timezone

## Implementation

### Dependencies
```javascript
const { logger } = require('@maas/core/log');
const AIResponseLog = require('@app/src/models/AIResponseLog');
const moment = require('moment-timezone');
```

### Core Functionality

#### logAIToDB Function
```javascript
const logAIToDB = async (feature, api, model, message, prompt, parameters, dateTime) => {
  try {
    const current = dateTime && typeof(dateTime) === 'string'? moment(dateTime) : moment.utc()
    await AIResponseLog.create({
      feature,
      action_source: api,
      ai_model: model,
      message,
      prompt,
      parameters,
      datetime: current.toDate()
    })
  } catch (error) {
    logger.error('[ai-log] failed to insert ai log to DB');
    logger.error(error);
  }
};
```

**Purpose**: Logs AI model interactions to the database for tracking and analysis

**Parameters**:
- `feature` (string): Feature or component that triggered the AI interaction
- `api` (string): API endpoint or action source identifier
- `model` (string): AI model name or identifier used
- `message` (string): Response message from the AI model
- `prompt` (string): Input prompt sent to the AI model
- `parameters` (object): Additional parameters used in the AI call
- `dateTime` (string, optional): Custom timestamp, defaults to current UTC time

**Database Schema**:
- `feature`: Application feature using AI
- `action_source`: Source API or endpoint
- `ai_model`: AI model identifier
- `message`: AI response content
- `prompt`: Input prompt text
- `parameters`: Serialized parameters object
- `datetime`: Timestamp of the interaction

## Usage Examples

### Basic AI Logging
```javascript
const { logAIToDB } = require('./helpers/ai-log');

// Log a route optimization AI call
await logAIToDB(
  'route-optimization',
  'POST /api/v1/routes/optimize',
  'gpt-4',
  'Optimized route found with 3 waypoints',
  'Optimize route from A to B via C with minimal travel time',
  {
    origin: 'Point A',
    destination: 'Point B',
    waypoints: ['Point C'],
    optimize_for: 'time'
  }
);

// Log a trip recommendation AI call
await logAIToDB(
  'trip-recommendations',
  'GET /api/v1/recommendations',
  'claude-3',
  'Found 5 alternative transportation options',
  'Suggest eco-friendly transport options for downtown commute',
  {
    user_preferences: ['eco-friendly', 'cost-effective'],
    location: 'downtown',
    time_of_day: 'morning_rush'
  }
);
```

### Advanced Usage with Custom Timestamp
```javascript
// Log with specific timestamp
const customTimestamp = '2024-01-15T10:30:00.000Z';
await logAIToDB(
  'chat-support',
  'POST /api/v1/chat/respond',
  'gpt-3.5-turbo',
  'I can help you book a ride. What\'s your destination?',
  'User asked: How do I book a ride?',
  {
    user_id: 12345,
    session_id: 'sess_abc123',
    context: 'customer_support'
  },
  customTimestamp
);
```

### Integration with AI Services
```javascript
class AIServiceLogger {
  static async logChatCompletion(feature, endpoint, model, prompt, response, metadata = {}) {
    const parameters = {
      model: model,
      temperature: metadata.temperature || 0.7,
      max_tokens: metadata.maxTokens || 150,
      ...metadata
    };
    
    await logAIToDB(
      feature,
      endpoint,
      model,
      response.choices[0].message.content,
      prompt,
      parameters
    );
  }
  
  static async logEmbeddingGeneration(feature, endpoint, model, text, embedding, metadata = {}) {
    const parameters = {
      model: model,
      input_length: text.length,
      embedding_dimensions: embedding.length,
      ...metadata
    };
    
    await logAIToDB(
      feature,
      endpoint,
      model,
      `Generated ${embedding.length}-dimensional embedding`,
      text,
      parameters
    );
  }
  
  static async logImageAnalysis(feature, endpoint, model, imageUrl, analysis, metadata = {}) {
    const parameters = {
      model: model,
      image_url: imageUrl,
      analysis_type: metadata.analysisType || 'general',
      ...metadata
    };
    
    await logAIToDB(
      feature,
      endpoint,
      model,
      analysis,
      `Analyze image: ${imageUrl}`,
      parameters
    );
  }
}
```

## Use Cases in TSP Job Service

### 1. Route Optimization
```javascript
// Log AI-powered route optimization
async function optimizeRouteWithAI(routeData) {
  const prompt = `Optimize route with ${routeData.waypoints.length} waypoints for ${routeData.optimizeFor}`;
  
  try {
    const aiResponse = await callRouteOptimizationAI(prompt, routeData);
    
    await logAIToDB(
      'route-optimization',
      'POST /api/v1/routes/optimize',
      'custom-routing-model',
      aiResponse.optimizedRoute,
      prompt,
      {
        waypoints_count: routeData.waypoints.length,
        optimization_type: routeData.optimizeFor,
        estimated_savings: aiResponse.timeSavings
      }
    );
    
    return aiResponse;
  } catch (error) {
    await logAIToDB(
      'route-optimization',
      'POST /api/v1/routes/optimize',
      'custom-routing-model',
      `Error: ${error.message}`,
      prompt,
      {
        error: true,
        error_type: error.name
      }
    );
    throw error;
  }
}
```

### 2. Predictive Analytics
```javascript
// Log demand prediction AI calls
async function predictTripDemand(location, timeframe) {
  const prompt = `Predict trip demand for ${location} during ${timeframe}`;
  
  const prediction = await callDemandPredictionAI(prompt, { location, timeframe });
  
  await logAIToDB(
    'demand-prediction',
    'POST /api/v1/analytics/predict-demand',
    'demand-forecasting-model',
    `Predicted ${prediction.expectedTrips} trips with ${prediction.confidence}% confidence`,
    prompt,
    {
      location: location,
      timeframe: timeframe,
      predicted_trips: prediction.expectedTrips,
      confidence_score: prediction.confidence,
      factors: prediction.influencingFactors
    }
  );
  
  return prediction;
}
```

### 3. Customer Support
```javascript
// Log AI chatbot interactions
async function handleCustomerQuery(userId, query, sessionId) {
  const prompt = `Customer query: ${query}`;
  
  const aiResponse = await callChatbotAI(prompt, { userId, sessionId });
  
  await logAIToDB(
    'customer-support',
    'POST /api/v1/chat/respond',
    'customer-support-bot',
    aiResponse.message,
    prompt,
    {
      user_id: userId,
      session_id: sessionId,
      intent: aiResponse.detectedIntent,
      confidence: aiResponse.confidence,
      escalated: aiResponse.needsHumanSupport
    }
  );
  
  return aiResponse;
}
```

## Analytics and Monitoring

### Usage Statistics
```javascript
class AIUsageAnalytics {
  static async getUsageStatsByFeature(timeRange = '24h') {
    const logs = await AIResponseLog.query()
      .where('datetime', '>=', moment().subtract(24, 'hours').toDate())
      .groupBy('feature')
      .count('* as usage_count')
      .select('feature');
      
    return logs;
  }
  
  static async getModelPerformance(modelName, timeRange = '7d') {
    const logs = await AIResponseLog.query()
      .where('ai_model', modelName)
      .where('datetime', '>=', moment().subtract(7, 'days').toDate());
      
    return {
      totalCalls: logs.length,
      avgResponseTime: this.calculateAvgResponseTime(logs),
      errorRate: this.calculateErrorRate(logs),
      topFeatures: this.getTopFeatures(logs)
    };
  }
  
  static async getCostAnalysis(timeRange = '30d') {
    const logs = await AIResponseLog.query()
      .where('datetime', '>=', moment().subtract(30, 'days').toDate());
      
    return logs.reduce((acc, log) => {
      const cost = this.estimateCallCost(log.ai_model, log.parameters);
      acc.totalCost += cost;
      acc.byModel[log.ai_model] = (acc.byModel[log.ai_model] || 0) + cost;
      return acc;
    }, { totalCost: 0, byModel: {} });
  }
}
```

## Error Handling and Reliability

### Robust Logging with Fallbacks
```javascript
class RobustAILogger {
  static async safeLogAIToDB(feature, api, model, message, prompt, parameters, dateTime) {
    const maxRetries = 3;
    let attempt = 0;
    
    while (attempt < maxRetries) {
      try {
        await logAIToDB(feature, api, model, message, prompt, parameters, dateTime);
        return; // Success, exit retry loop
      } catch (error) {
        attempt++;
        
        if (attempt >= maxRetries) {
          // Log to alternative storage or file system as fallback
          await this.logToFallbackStorage({
            feature, api, model, message, prompt, parameters, dateTime,
            error: error.message,
            attempts: attempt
          });
        } else {
          // Wait before retry with exponential backoff
          await new Promise(resolve => setTimeout(resolve, Math.pow(2, attempt) * 1000));
        }
      }
    }
  }
  
  static async logToFallbackStorage(logData) {
    // Implement fallback logging (file system, alternative DB, etc.)
    const fs = require('fs').promises;
    const fallbackLog = {
      timestamp: new Date().toISOString(),
      type: 'ai_log_fallback',
      data: logData
    };
    
    try {
      await fs.appendFile('ai-logs-fallback.json', JSON.stringify(fallbackLog) + '\n');
    } catch (fallbackError) {
      console.error('Critical: Both primary and fallback AI logging failed', fallbackError);
    }
  }
}
```

## Module Export

```javascript
module.exports = {
  logAIToDB,
};
```

This AI logging helper provides comprehensive tracking of AI model usage within the TSP Job service, enabling monitoring, cost analysis, performance optimization, and debugging of AI-powered features across the MaaS platform.