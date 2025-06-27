# Send Event Helper Documentation

## 🔍 Quick Summary (TL;DR)
Asynchronous event batching helper that logs incentive events to database for mobility service user actions | event-sender | batch-processor | incentive-tracking | user-events | database-logger | async-handler | sqs-alternative
- Batches and logs user incentive events for mobility services
- Processes events in chunks of 500 to handle large volumes
- Database-based event storage with AWS SQS integration (currently disabled)
- Compatible with Node.js 16+, Koa.js framework

## ❓ Common Questions Quick Index
- **Q: What does this helper do?** → [Functionality Overview](#functionality-overview)
- **Q: How to send events in batches?** → [Usage Methods](#usage-methods)
- **Q: Why is SQS code commented out?** → [Technical Specifications](#technical-specifications)
- **Q: What happens if event sending fails?** → [Detailed Code Analysis](#detailed-code-analysis)
- **Q: How to handle large event volumes?** → [Performance and Scaling](#performance-and-scaling)
- **Q: What's the event data structure?** → [Output Examples](#output-examples)
- **Q: How to troubleshoot event logging?** → [Important Notes](#important-notes)
- **Q: When to use this helper?** → [Use Cases](#use-cases)
- **Q: How to optimize performance?** → [Improvement Suggestions](#improvement-suggestions)
- **Q: What are security considerations?** → [Important Notes](#important-notes)

## 📋 Functionality Overview

**Non-technical explanation:** 
- Like a mail sorting facility that groups letters by destination before sending them out in batches
- Similar to a restaurant kitchen that prepares multiple orders efficiently by batching similar tasks
- Acts as a logistics coordinator that organizes and tracks delivery of reward notifications to users

**Technical explanation:** 
Implements batch processing pattern for event logging with fallback from AWS SQS to database storage. Uses chunking algorithm to handle large datasets efficiently while maintaining logging integrity.

**Business value:** Enables scalable user incentive tracking for mobility platforms, supporting gamification and user engagement features through reliable event processing.

**System context:** Part of TSP API's helper layer, interfaces with SendEvent model for persistence and integrates with @maas/core logging infrastructure.

## 🔧 Technical Specifications

**File Information:**
- Name: send-event.js
- Path: /src/helpers/send-event.js  
- Language: JavaScript (ES6+)
- Type: Async Helper Module
- Complexity: Low-Medium (batch processing logic)

**Dependencies:**
- `@maas/core/log` (Critical) - Structured logging with Winston
- `@app/src/models/SendEvent` (Critical) - Database model for event persistence
- `@aws-sdk/client-sqs` (Optional) - AWS SQS integration (commented out)
- `config` (Optional) - Configuration management (commented out)

**Compatibility:**
- Node.js: 14.x+ (async/await support)
- Framework: Koa.js 2.x+
- Database: MongoDB (via SendEvent model)

**Configuration:**
- `limitMax`: 500 (batch size limit)
- AWS SQS: Currently disabled, configuration in config/vendor.aws

## 📝 Detailed Code Analysis

**Main Function Signature:**
```javascript
module.exports = async (eventDatas) => Promise<void>
// Parameters: eventDatas - Array of {eventName: string, eventMeta: object, userIds: array}
// Returns: Promise that resolves when all batches are processed
```

**Execution Flow:**
1. Calculate batches based on 500-item limit (O(1) complexity)
2. Iterate through batches with slice operations (O(n) total)
3. Log event details for each item (O(m) per batch)
4. Create database records via SendEvent model (O(1) per batch)
5. Handle errors with non-blocking logging (graceful degradation)

**Key Code Patterns:**
```javascript
// Batch calculation and processing
const limitMax = 500;
const loop = Math.ceil(eventDatas.length / limitMax);

// Error handling with continuation
try {
  // Processing logic
} catch (err) {
  logger.warn(`Send event Error:${err.message}`);
  // Continues processing other batches
}
```

**Design Patterns:**
- Batch Processing Pattern for scalability
- Error Isolation Pattern preventing cascade failures
- Template Method Pattern with AWS SQS fallback preparation

## 🚀 Usage Methods

**Basic Usage:**
```javascript
const sendEvent = require('@app/src/helpers/send-event');

// Single event
await sendEvent([{
  eventName: 'ride_completed',
  eventMeta: { distance: 5.2, duration: 1200 },
  userIds: ['user123', 'user456']
}]);

// Multiple events
await sendEvent([
  {
    eventName: 'trip_started',
    eventMeta: { mode: 'bike', location: 'downtown' },
    userIds: ['user789']
  },
  {
    eventName: 'points_earned',
    eventMeta: { points: 50, reason: 'eco_friendly' },
    userIds: ['user123', 'user789']
  }
]);
```

**Large Volume Processing:**
```javascript
// Handle 2000+ events efficiently
const largeEventBatch = Array.from({length: 2000}, (_, i) => ({
  eventName: 'bulk_update',
  eventMeta: { batch: Math.floor(i/500), index: i },
  userIds: [`user${i}`]
}));

await sendEvent(largeEventBatch); // Automatically batched into 4 chunks
```

## 📊 Output Examples

**Successful Execution:**
```
INFO: Send incentive event UserIds: user123,user456 Name:ride_completed Meta:{"distance":5.2,"duration":1200}
INFO: Send incentive event UserIds: user789 Name:trip_started Meta:{"mode":"bike","location":"downtown"}
```

**Error Condition:**
```
WARN: Send event Error:Connection timeout
WARN: Send event Error:Validation failed for eventMeta
```

**Database Record Structure:**
```json
{
  "action": "event",
  "data": [
    {
      "eventName": "ride_completed",
      "eventMeta": {"distance": 5.2, "duration": 1200},
      "userIds": ["user123", "user456"]
    }
  ],
  "createdAt": "2024-01-15T10:30:00Z"
}
```

## ⚠️ Important Notes

**Security Considerations:**
- Event data is logged in plaintext - avoid sensitive user information
- UserIds should be sanitized before logging
- Database access requires proper authentication

**Performance Gotchas:**
- Batch size of 500 optimized for memory usage vs. throughput
- Large userIds arrays can impact log readability
- Synchronous logging within async loops may cause blocking

**Troubleshooting:**
- **Symptom:** Events not appearing in database
  - **Diagnosis:** Check SendEvent model connection
  - **Solution:** Verify MongoDB connection and model configuration
- **Symptom:** Memory issues with large batches
  - **Solution:** Reduce input size or implement streaming

**Common Issues:**
- Missing eventName or eventMeta properties cause validation errors
- Empty userIds arrays are logged but may indicate upstream issues

## 🔗 Related File Links

**Direct Dependencies:**
- `/src/models/SendEvent.js` - Database model for event persistence
- `@maas/core/log/index.js` - Logging infrastructure
- `/config/default.js` - Application configuration (AWS settings)

**Related Controllers:**
- `/src/controllers/send_event.js` - HTTP endpoint wrapper
- `/src/controllers/user-actions.js` - User action tracking

**Integration Files:**
- `/src/services/incentive.js` - Business logic for incentive processing
- `/src/middleware/validation.js` - Input validation schemas

## 📈 Use Cases

**Daily Operations:**
- Mobility app tracking user ride completions
- Gamification system logging point awards
- Analytics pipeline capturing user behavior events

**Development Scenarios:**
- Testing incentive systems with bulk event creation
- Debugging user engagement tracking
- Performance testing event processing throughput

**Integration Patterns:**
- Microservice event publishing to shared event store
- Batch processing for end-of-day analytics
- Real-time user notification triggering

**Anti-patterns:**
- Don't use for real-time critical events (database latency)
- Avoid extremely large single-batch operations (>10k events)
- Don't include PII in eventMeta for compliance

## 🛠️ Improvement Suggestions

**Performance Optimization:**
- Implement streaming for memory efficiency (High Priority, 2-3 days)
- Add connection pooling for database operations (Medium Priority, 1 day)
- Consider parallel batch processing (Low Priority, 1 week)

**Feature Enhancements:**
- Add event deduplication logic (Medium Priority, 2 days)
- Implement retry mechanism for failed batches (High Priority, 1 day)
- Add metrics collection for monitoring (Medium Priority, 3 days)

**Code Quality:**
- Add input validation with Joi schemas (High Priority, 1 day)
- Implement unit tests with Mocha/Chai (High Priority, 2 days)
- Add TypeScript definitions (Low Priority, 1 week)

**Operational Improvements:**
- Add health check endpoint (Medium Priority, 1 day)
- Implement graceful shutdown handling (Medium Priority, 1 day)
- Add structured error reporting (High Priority, 1 day)

## 🏷️ Document Tags

**Keywords:** event-processing, batch-processing, incentive-tracking, user-events, database-logging, async-operations, sqs-integration, koa-helper, mobility-platform, gamification, event-batching, error-handling, performance-optimization, mongodb-storage, aws-sqs

**Technical Tags:** #event-processing #batch-processing #nodejs #koa #mongodb #aws-sqs #logging #async #helper #tsp-api

**Target Roles:** 
- Backend Developers (Intermediate) - Integration and debugging
- DevOps Engineers (Beginner) - Monitoring and deployment
- QA Engineers (Intermediate) - Testing event flows

**Difficulty Level:** ⭐⭐⭐ (3/5) - Moderate complexity due to batch processing logic and async error handling

**Maintenance Level:** Medium - Regular monitoring of batch sizes and error rates required

**Business Criticality:** High - Core component for user engagement and analytics

**Related Topics:** microservices-architecture, event-driven-systems, batch-processing-patterns, database-optimization, async-programming, error-handling-strategies