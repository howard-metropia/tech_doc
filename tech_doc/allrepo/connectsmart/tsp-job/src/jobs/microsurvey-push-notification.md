# microsurvey-push-notification Job Documentation

## Overview
The microsurvey-push-notification job is an advanced AI-powered survey management system that uses XState state machines and OpenAI integration to intelligently schedule and deliver personalized micro-surveys to users, optimizing engagement through smart timing and contextual awareness.

## Core Architecture

### XState State Machine Integration
- **Finite State Management**: Uses XState v5 for robust survey flow control
- **State Persistence**: Database-backed state storage for session continuity
- **Event-Driven Flow**: Structured event handling for survey progression
- **Context Management**: User-specific data and progress tracking

### AI-Powered Scheduling
- **OpenAI Integration**: GPT-4 powered intelligent timing recommendations
- **Contextual Awareness**: Houston-specific lifestyle pattern recognition
- **Dynamic Optimization**: Real-time scheduling based on user behavior
- **Timezone Intelligence**: Multi-timezone support with DST awareness

## State Machine Architecture

### Survey Flow States
```javascript
const states = {
  idle: { on: { START: 'wait_Consent' } },
  wait_Consent: { entry: [/* AI timing logic */], on: { TRIGGER_NEXT: 'Consent' } },
  Consent: { on: { CONSENT_ACCEPT: 'wait_Q1', CONSENT_REJECT: 'done', CANCEL: [...] } },
  wait_Q1: { entry: [/* AI scheduling */], on: { TRIGGER_NEXT: 'Q1' } },
  // Dynamic Q1-Q12 generation
  done: { type: 'final', entry: [/* cleanup */] }
};
```

### Event System
- **ALLOWED_EVENTS**: Whitelisted event validation
- **User Actions**: START, NEXT, FINISH, CANCEL
- **Consent Management**: CONSENT_ACCEPT, CONSENT_REJECT
- **Flow Control**: TRIGGER_NEXT for AI-scheduled progression

## AI Scheduling System

### OpenAI Integration
```javascript
async function askAIPushTime(userId, prevQ, nextQ) {
  const prompt = [{
    role: 'system', 
    content: 'You are a person receiving a survey consultation.'
  }, {
    role: 'user',
    content: `Recommend three nearest suitable future push notification times...`
  }];
  
  const res = await axios.post(aiURL, {
    model: 'gpt-4',
    messages: prompt,
    temperature: 0.7,
    max_tokens: 200
  });
}
```

### Intelligent Timing Features
- **Lifestyle Awareness**: Houston-specific behavioral patterns
- **Relaxation Windows**: Targets periods of casual phone usage
- **Weekend Adaptation**: Different scheduling for weekends
- **Time Restrictions**: Avoids 10:30 PM - 7:00 AM sleep hours
- **DST Compliance**: Automatic daylight saving time adjustments

## Survey Configuration

### Question Bank Management
```javascript
const surveyQuestions = [
  { key: 'Q1', googleFormUrl: '...', points: 1 },
  { key: 'Q2', googleFormUrl: '...', points: 1 },
  // ... Q3-Q12 with varying point values (1-1.5)
];
```

### Dynamic Point Rewards
- **Variable Rewards**: Different point values per question (1-1.5 points)
- **Progressive Difficulty**: Higher rewards for complex questions
- **Engagement Incentives**: Points motivation for completion

## Database Management

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

### Schedule Management
- **AI Schedule Table**: `microsurvey_ai_schedule` for timing records
- **Status Tracking**: 'pending', 'done', 'failed' status management
- **Conflict Resolution**: Prevents race conditions in scheduling

## Notification System

### Push Notification Types
- **Consent Notifications** (Type 106): Survey participation invitations
- **Question Notifications** (Type 108): Individual question prompts
- **Reward Messaging**: Dynamic coin earning notifications

### Message Personalization
```javascript
const title = `Share Your Thoughts & Earn Up to 15 Coins!`;
const body = notification_type === 106 
  ? `Complete our quick survey.`
  : `Earn Coins for your valuable insights...`;
```

## Advanced Features

### Cancel Handling
- **Two-Strike System**: Allows one cancellation before progression
- **Graceful Degradation**: Maintains engagement after cancellations
- **Smart Rescheduling**: AI-powered retry timing

### Service Management
- **Actor Caching**: Efficient state machine instance management
- **Memory Optimization**: Automatic cleanup of completed sessions
- **Session Recovery**: Robust state restoration from database

## Performance Optimization

### Batch Processing
- **Limited Processing**: 100 records per execution cycle
- **Rate Limiting**: 1-second delays between notifications
- **Resource Management**: Efficient memory and connection usage

### Database Efficiency
- **Indexed Queries**: Optimized scheduling queries
- **Connection Pooling**: Efficient database resource usage
- **Bulk Operations**: Batch status updates

## Integration Points

### External Services
- **OpenAI API**: Intelligent scheduling recommendations
- **Google Forms**: Survey form hosting and management
- **Push Notifications**: Mobile notification delivery
- **Google Chat**: Administrative logging and monitoring

### Internal Systems
- **State Management**: XState integration for flow control
- **User Management**: Participant tracking and engagement
- **Analytics**: Survey completion and engagement metrics

## Error Handling and Recovery

### Robust Error Management
- **API Failure Recovery**: Graceful OpenAI API error handling
- **Database Rollback**: Transaction safety for critical operations
- **Notification Failures**: Status tracking for failed deliveries
- **State Corruption**: Recovery mechanisms for invalid states

### Monitoring and Alerting
- **Google Chat Integration**: Real-time administrative notifications
- **Performance Tracking**: Job execution time and success metrics
- **Error Logging**: Comprehensive error capture and analysis

## Security Considerations
- **API Key Management**: Secure OpenAI API key handling
- **Data Privacy**: User data protection in state persistence
- **Input Validation**: Event and parameter validation
- **Access Control**: Secure database operations

## Related Components
- **Survey Management**: Question bank and form integration
- **Reward System**: Point distribution and tracking
- **User Engagement**: Participation and retention analytics
- **AI Services**: Machine learning optimization platforms

## Future Enhancements
- **Advanced Personalization**: ML-based individual optimization
- **Multi-language Support**: Internationalization capabilities
- **Real-time Analytics**: Live engagement monitoring
- **A/B Testing**: Experimental scheduling optimization
- **Predictive Modeling**: Behavior-based timing predictions