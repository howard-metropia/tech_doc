# Microsurvey Controller Documentation

## 🔍 Quick Summary (TL;DR)
This controller implements an intelligent microsurvey system using XState state machines to manage multi-step survey flows with AI-powered push notifications for Houston ConnectSmart mobility platform. Core functionality: `XState | StateMachine | Survey | PushNotification | GoogleForms | WalletIntegration | AI | Rewards | Consent | Scheduler | UserEngagement`. Primary use cases include automated survey deployment, smart timing for notifications, and reward distribution. Compatible with Node.js 20+ and Koa.js framework.

## ❓ Common Questions Quick Index
- **Q: How does the AI determine optimal push notification timing?** → [AI Push Time](#ai-push-time-generation)
- **Q: What happens if a user cancels a survey?** → [Cancel Logic](#cancel-behavior)  
- **Q: How are survey rewards distributed?** → [Rewards System](#wallet-integration)
- **Q: Can users restart incomplete surveys?** → [State Persistence](#state-management)
- **Q: What if Google Forms integration fails?** → [Error Handling](#error-handling)
- **Q: How to monitor system memory usage?** → [Memory Metrics](#memory-monitoring)
- **Q: What security measures protect survey data?** → [Security](#security-considerations)
- **Q: How to troubleshoot state machine issues?** → [Troubleshooting](#troubleshooting)
- **Q: What database tables are used?** → [Database Schema](#database-tables)
- **Q: How to add new survey questions?** → [Configuration](#survey-configuration)

## 📋 Functionality Overview
**Non-technical explanation:** Like a smart personal assistant for surveys that remembers where you left off, knows the best time to remind you based on your lifestyle, and rewards you for participation. It's similar to how Netflix suggests shows at optimal times, or how fitness apps send motivational notifications when you're most likely to exercise.

**Technical explanation:** A stateful microsurvey orchestration system using XState finite state machines with AI-driven scheduling, persistent state management, and integrated reward distribution. Implements event-driven architecture with Google Forms integration and real-time notification delivery.

**Business value:** Increases survey completion rates through intelligent timing, reduces user fatigue with adaptive flows, and provides seamless reward distribution to enhance user engagement in mobility research.

**Context:** Core component of Houston ConnectSmart platform's user engagement system, interfacing with wallet services, notification systems, and external Google Forms for data collection.

## 🔧 Technical Specifications
- **File:** `microsurvey.js` (1134 lines, High complexity)
- **Framework:** Koa.js with @koa/router 
- **Dependencies:** 
  - `xstate` v5 (state machine core) - Critical
  - `@maas/core` (logging, database, response) - Critical  
  - `moment-timezone` (time handling) - High
  - `axios` (HTTP client) - High
  - `OpenAI API` (GPT-4 integration) - Medium
- **Database:** MySQL (portal), Redis (session caching)
- **Environment Variables:** `PROJECT_NAME`, `PROJECT_STAGE`, `OPENAI_API_KEY`
- **Memory Requirements:** 512MB+ recommended for state machine caching
- **Node.js:** v20.0.0+ (ES2022 features, XState v5 compatibility)

## 📝 Detailed Code Analysis

### Core State Machine Architecture
```javascript
// Main survey flow states
const states = {
  idle: { on: { START: 'wait_Consent' } },
  wait_Consent: { /* AI scheduling entry point */ },
  Consent: { /* User agreement handling */ },
  wait_Q1: { /* Question preparation */ },
  Q1-Q12: { /* Dynamic question states */ },
  done: { type: 'final' }
};
```

### AI Push Time Generation
The `askAIPushTime()` function uses GPT-4 to determine optimal notification timing:
- Considers Houston Central Time and Daylight Saving Time
- Avoids 10:30 PM - 7:00 AM quiet hours
- Analyzes user lifestyle patterns and weekend behaviors
- Fallback to +1 hour if AI API fails

### State Persistence
```javascript
async function persistState(userId, state) {
  const json = JSON.stringify(state);
  await knexHybrid.raw(
    `INSERT INTO state_store (user_id, state_json) VALUES (?, ?)`,
    [userId, json]
  );
}
```

### Memory Management
- Active actor monitoring with `getXStateMetrics()`
- Automatic cleanup on survey completion
- Google Chat integration for memory alerts
- Heap usage tracking per actor

## 🚀 Usage Methods

### Basic Survey Initialization
```javascript
POST /api/v2/trigger_microsurvey
{
  "userIds": [12345],
  "action": "start"
}
```

### Batch Survey Deployment
```javascript
POST /api/v2/trigger_microsurvey
{
  "action": "start_microsurvey",
  "limitation": 50,
  "settime": 5000
}
// Automatically selects active users with 5+ days activity in 6 months
```

### Survey State Check
```javascript
GET /api/v2/microsurvey
Headers: { userid: "12345" }
// Returns current survey state and question URL
```

### Google Form Response Processing
```javascript
POST /api/v2/received_googleform
{
  "answers": {
    "Response ID": "encrypted_user_data",
    "Share Your Thoughts & Earn Up to 15 Coins!": "Sure, I'd like to participate!"
  }
}
```

## 📊 Output Examples

### Successful Survey Status Response
```json
{
  "status": 2,
  "survey_id": 1,
  "info_url": "https://docs.google.com/forms/d/e/1FAIpQLSf2qNvMUQ2RKkLgne9A...Q1%2C12345%2C1",
  "auto_launch": true
}
```

### Memory Usage Metrics
```json
{
  "actorCount": 15,
  "memory": {
    "rss": "245.67 MB",
    "heapTotal": "123.45 MB",
    "heapUsed": "89.23 MB"
  },
  "avgHeapPerActor": "5.95 MB"
}
```

### Error Response
```json
{
  "status": "error",
  "message": "No duplicate bonuses.",
  "userId": 12345
}
```

## ⚠️ Important Notes

### Security Considerations
- Survey responses encrypted using AES-256-GCM
- User ID validation through `authAndApikey` middleware
- Rate limiting through natural survey flow constraints
- Sensitive data (OpenAI API key) should be in environment variables

### Performance Gotchas
- State machine actors consume ~6MB memory each
- AI API calls add 2-3 second latency
- Database writes on every state transition
- Consider actor cleanup for high-volume deployments

### Troubleshooting Common Issues
- **Memory leaks:** Check `services.size` and implement actor cleanup
- **State corruption:** Verify XState v5 snapshot format compatibility
- **AI timing failures:** Monitor fallback to +1 hour default
- **Duplicate rewards:** Database constraint prevents double payments

## 🔗 Related File Links
- **Database Models:** `@maas/core/mysql` (portal connection)
- **Wallet Service:** `@app/src/services/wallet` (points distribution)
- **Notification Helper:** `@app/src/helpers/send-notification`
- **AES Encryption:** `@app/src/services/aes-256-gcm`
- **Middleware:** `@app/src/middlewares/auth`, `authAndApikey`

## 📈 Use Cases

### Daily Operations
- **Survey Deployment:** HR teams deploy engagement surveys to 500+ active users
- **Reward Distribution:** Automatic point allocation upon survey completion
- **Progress Monitoring:** Real-time tracking of survey completion rates

### Development Scenarios  
- **A/B Testing:** Different survey flows for user segments
- **Load Testing:** Memory monitoring during high-volume deployments
- **Integration Testing:** Google Forms webhook validation

### Scaling Considerations
- Implement actor pooling for >1000 concurrent users
- Consider Redis for state persistence in distributed environments
- Monitor Google Chat webhook rate limits

## 🛠️ Improvements Suggestions

### Immediate Optimizations (Low effort, High impact)
- Implement actor pooling to reduce memory usage by 60%
- Add database connection pooling for better performance
- Cache AI responses for similar user patterns

### Feature Enhancements (Medium effort, High value)
- Multi-language survey support with i18n
- Advanced analytics dashboard for completion rates
- Survey A/B testing framework integration

### Technical Debt Reduction (High effort, High value)
- Migrate to TypeScript for better type safety
- Implement comprehensive unit test coverage (currently missing)
- Separate AI service into dedicated microservice

## 🏷️ Document Tags

**Keywords:** `microsurvey` `xstate` `state-machine` `ai-notifications` `google-forms` `wallet-integration` `koa-controller` `survey-automation` `push-notifications` `user-engagement` `rewards-system` `houston-connectsmart` `mobility-platform` `gpt4-integration` `survey-scheduling` `user-consent` `points-distribution` `memory-monitoring` `survey-flow` `async-processing`

**Technical Tags:** `#koa-api` `#xstate-v5` `#mysql-integration` `#ai-scheduling` `#state-persistence` `#memory-management` `#webhook-processing` `#survey-orchestration`

**Target Roles:** Backend Developers ⭐⭐⭐, DevOps Engineers ⭐⭐, Product Managers ⭐, QA Engineers ⭐⭐

**Difficulty Level:** ⭐⭐⭐⭐ (Complex state management, AI integration, multiple async flows)

**Maintenance Level:** High (Active state machine monitoring, AI API management, user engagement metrics)

**Business Criticality:** High (Core user engagement platform component)

**Related Topics:** `survey-platforms` `user-analytics` `notification-systems` `reward-mechanisms` `mobility-research` `state-management-patterns` 