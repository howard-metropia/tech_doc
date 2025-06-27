# AI Log Helper Documentation

## 🔍 Quick Summary (TL;DR)
AI logging utility that asynchronously records AI service interactions to database for audit trails and analytics. This utility logs AI model responses, prompts, and metadata for the MaaS platform's AI features.

**Keywords:** AI logging | audit trail | database logging | AI response tracking | model interactions | asynchronous logging | error handling | moment timezone | AI analytics | service monitoring

**Use Cases:** AI interaction auditing, performance tracking, debugging AI features, compliance logging
**Compatibility:** Node.js 12+, Koa.js, Moment.js, @maas/core framework

## ❓ Common Questions Quick Index
- **Q: What does this helper do?** → [Functionality Overview](#functionality-overview)
- **Q: How to log AI responses?** → [Usage Methods](#usage-methods)
- **Q: What data gets stored?** → [Technical Specifications](#technical-specifications)
- **Q: How to handle logging errors?** → [Error Handling](#detailed-code-analysis)
- **Q: What if database insert fails?** → [Important Notes](#important-notes)
- **Q: How to debug AI logging issues?** → [Troubleshooting](#important-notes)
- **Q: What are the performance implications?** → [Performance Considerations](#important-notes)
- **Q: How to customize datetime handling?** → [Parameter Configuration](#usage-methods)
- **Q: What's the database schema?** → [Related Files](#related-file-links)
- **Q: How to integrate with other services?** → [Integration Patterns](#use-cases)

## 📋 Functionality Overview

**Non-technical explanation:** 
Like a detailed receipt system for AI conversations - every time the platform asks an AI service a question and gets an answer, this helper creates a permanent record with all the details (who asked, what was asked, what the AI said, when it happened).

Think of it as a librarian's logbook that tracks every book borrowed, who borrowed it, when, and for what purpose - but for AI interactions.

**Technical explanation:** 
Asynchronous database logging utility that captures AI service interactions using the AIResponseLog model. Implements error-safe logging with timezone-aware datetime handling and structured parameter storage.

**Business value:** Enables AI usage analytics, compliance auditing, debugging AI features, and tracking AI service performance across the MaaS platform.

**System context:** Core utility used by AI-enabled features across the TSP API to maintain audit trails and support data-driven AI service optimization.

## 🔧 Technical Specifications

**File Information:**
- Name: ai-log.js
- Path: /allrepo/connectsmart/tsp-api/src/helpers/ai-log.js
- Language: JavaScript (Node.js)
- Type: Utility Helper
- Size: ~25 lines
- Complexity: Low (single function, minimal logic)

**Dependencies:**
- `@maas/core/log` (Critical): Logging framework for error reporting
- `@app/src/models/AIResponseLog` (Critical): Database model for AI log storage
- `moment-timezone` (Required): Timezone-aware datetime handling

**Compatibility:**
- Node.js: 12.0+ (async/await support required)
- Moment.js: 2.24+ (timezone support)
- Database: Requires AIResponseLog model/table

**System Requirements:**
- Memory: Minimal footprint (<1MB)
- Database: Write access to AI response log table
- Network: None (local database operations)

## 📝 Detailed Code Analysis

**Main Function Signature:**
```javascript
logAIToDB(feature, api, model, message, prompt, parameters, dateTime) → Promise<void>
```

**Parameters:**
- `feature` (string): AI feature identifier (e.g., "route_optimization", "chat_assistant")
- `api` (string): Source API/service name
- `model` (string): AI model identifier (e.g., "gpt-4", "claude-3")
- `message` (string): AI response/output message
- `prompt` (string): User prompt/input sent to AI
- `parameters` (object): Additional AI service parameters
- `dateTime` (string|optional): Custom timestamp (ISO format)

**Execution Flow:**
1. **Datetime Processing:** Handles custom or current UTC timestamp using moment
2. **Database Insert:** Asynchronously creates AIResponseLog record
3. **Error Handling:** Catches and logs any database insertion failures

**Design Patterns:**
- **Fire-and-forget**: Async operation without return value
- **Error isolation**: Database failures don't break calling code
- **Flexible timestamping**: Supports both current and custom timestamps

**Error Handling:**
- Catches all database insertion errors
- Logs errors using @maas/core logger
- Continues execution without throwing (non-blocking)

## 🚀 Usage Methods

**Basic Usage:**
```javascript
const { logAIToDB } = require('@app/src/helpers/ai-log');

// Log AI interaction
await logAIToDB(
  'route_planning',           // feature
  'tsp-api',                 // api source
  'gpt-4',                   // AI model
  'Route found: 25.2 miles', // AI response
  'Find route from A to B',  // user prompt
  { maxRoutes: 3, mode: 'driving' }, // parameters
  '2024-01-15T10:30:00Z'     // custom datetime (optional)
);
```

**Real-time Logging:**
```javascript
// Log with current timestamp
logAIToDB(
  'chat_support',
  'customer-api',
  'claude-3',
  'I can help you with that request.',
  'How do I cancel my trip?',
  { userId: '12345', sessionId: 'abc123' }
  // dateTime omitted = uses current UTC time
);
```

**Error-Safe Integration:**
```javascript
// In AI service wrapper
async function callAIService(prompt, params) {
  try {
    const response = await aiService.generate(prompt, params);
    
    // Log AI interaction (non-blocking)
    logAIToDB(
      'content_generation',
      'content-api',
      'gpt-3.5-turbo',
      response.text,
      prompt,
      params
    ).catch(err => {
      // Additional error handling if needed
      console.warn('AI logging failed:', err.message);
    });
    
    return response;
  } catch (error) {
    // Log failed attempts too
    logAIToDB(
      'content_generation',
      'content-api',
      'gpt-3.5-turbo',
      `Error: ${error.message}`,
      prompt,
      { ...params, error: true }
    );
    throw error;
  }
}
```

## 📊 Output Examples

**Successful Execution:**
```javascript
// Function call
logAIToDB('trip_optimization', 'mobile-api', 'claude-3', 'Optimized route found', 'Optimize my commute', { userId: 456 });

// Database record created:
{
  id: 12345,
  feature: 'trip_optimization',
  action_source: 'mobile-api',
  ai_model: 'claude-3',
  message: 'Optimized route found',
  prompt: 'Optimize my commute',
  parameters: { userId: 456 },
  datetime: '2024-01-15T14:30:22.000Z',
  created_at: '2024-01-15T14:30:22.000Z'
}
```

**Error Scenario Output:**
```
[ERROR] [ai-log] failed to insert ai log to DB
[ERROR] Error: Table 'ai_response_logs' doesn't exist
    at Connection.execute (mysql/connection.js:123)
    at AIResponseLog.create (models/AIResponseLog.js:45)
```

**Performance Metrics:**
- Insert time: 5-15ms (typical database write)
- Memory usage: <100KB per operation
- No return value (fire-and-forget)

## ⚠️ Important Notes

**Security Considerations:**
- Logs may contain sensitive user prompts - ensure database security
- Consider data retention policies for AI interaction logs
- Sanitize parameters to prevent logging sensitive information

**Performance Gotchas:**
- Database writes can accumulate - monitor table growth
- Consider batching for high-volume AI usage
- No connection pooling management - relies on model layer

**Troubleshooting:**
- **Symptom:** Silent logging failures → **Solution:** Check database connectivity and table schema
- **Symptom:** Timezone issues → **Solution:** Verify moment-timezone configuration
- **Symptom:** Parameter serialization errors → **Solution:** Ensure parameters are JSON-serializable

**Common Issues:**
- Database table missing: Ensure AIResponseLog model migration is run
- Invalid datetime strings: Use ISO 8601 format for custom timestamps
- Large parameter objects: Consider size limits for JSON storage

## 🔗 Related File Links

**Core Dependencies:**
- `/src/models/AIResponseLog.js` - Database model definition and schema
- `@maas/core/log/index.js` - Logging framework configuration
- `/config/database.js` - Database connection configuration

**Integration Files:**
- `/src/controllers/*` - Controllers using AI services
- `/src/services/ai/*` - AI service wrappers
- `/src/middlewares/ai-audit.js` - Request-level AI auditing middleware

**Configuration:**
- `/config/default.js` - Environment configurations
- `/migrations/*_create_ai_response_logs.js` - Database migration

## 📈 Use Cases

**Development Scenarios:**
- Debug AI service responses during feature development
- Track AI model performance across different features
- Audit AI usage for billing and compliance

**Production Scenarios:**
- Monitor AI service reliability and response quality
- Analyze user interaction patterns with AI features
- Generate AI usage reports for business analytics

**Integration Patterns:**
- Middleware-level logging for all AI endpoints
- Service-specific logging in AI wrapper functions
- Batch processing for analytics and reporting

**Anti-patterns:**
- Don't use for real-time monitoring (async operation)
- Avoid logging large binary data in parameters
- Don't rely on successful logging for business logic

## 🛠️ Improvement Suggestions

**Code Optimization:**
- Add parameter size validation (prevent oversized JSON storage)
- Implement connection pooling awareness
- Add retry logic for transient database failures

**Feature Enhancements:**
- Batch logging for high-volume scenarios
- Structured parameter validation
- Automatic PII detection and masking

**Monitoring Improvements:**
- Add logging success/failure metrics
- Implement log retention policies
- Create alerting for logging failures

**Maintenance Recommendations:**
- Weekly: Monitor table growth and performance
- Monthly: Review logged parameter sizes and optimize
- Quarterly: Analyze AI usage patterns and update logging strategy

## 🏷️ Document Tags

**Keywords:** AI logging, audit trail, database logging, AI response tracking, model interactions, asynchronous logging, error handling, moment timezone, AI analytics, service monitoring, MaaS platform, Koa.js helper, database insert, fire-and-forget logging, timezone handling

**Technical Tags:** #ai #logging #database #helper #async #audit #nodejs #koa #moment #mysql #mongodb #error-handling #utilities #maas-platform

**Target Roles:** Backend Developers (⭐⭐), AI Engineers (⭐⭐), DevOps Engineers (⭐), QA Engineers (⭐⭐)

**Difficulty Level:** ⭐⭐ (Easy to use, moderate to integrate properly)

**Maintenance Level:** Low (stable utility, infrequent updates needed)

**Business Criticality:** Medium (important for compliance and debugging, not business-critical)

**Related Topics:** AI service integration, audit logging, database operations, error handling, timezone management, async operations, monitoring utilities