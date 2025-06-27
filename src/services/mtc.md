# TSP API MTC Service Documentation

## 🔍 Quick Summary (TL;DR)
The MTC (Mobility Transportation Choice) service manages behavioral messaging experiments to influence user transportation choices through targeted environmental and cost-focused messages, with weighted random selection and user interaction tracking.

**Keywords:** behavioral-messaging | transportation-choice | environmental-nudging | user-experiments | weighted-random | cost-awareness | sustainability-messaging | behavior-modification

**Primary use cases:** Delivering personalized transportation choice messages, tracking user responses to environmental nudging, conducting behavioral experiments, promoting sustainable transportation modes

**Compatibility:** Node.js >= 16.0.0, MongoDB for message tracking, MySQL for user targeting, UUID generation support

## ❓ Common Questions Quick Index
- **Q: What does MTC stand for?** → Mobility Transportation Choice - a behavioral messaging system
- **Q: How are messages selected?** → Weighted random selection with 50% chance of no message
- **Q: What's the message focus?** → Environmental impact and cost awareness to discourage driving
- **Q: Who receives these messages?** → Users in the mtc_user_signup table (experiment participants)
- **Q: Are responses tracked?** → Yes, all user interactions and plan data are stored
- **Q: Can messages be personalized?** → Yes, some messages reference user's environmental preferences

## 📋 Functionality Overview

**Non-technical explanation:** 
Think of this as a **digital conscience for transportation choices**. When someone is about to drive somewhere, the app might show them a message saying "Wait! This trip will cost the planet $3 - consider taking the bus instead?" The system picks different messages randomly to see which ones work best at convincing people to choose greener transportation.

**Technical explanation:** 
A behavioral intervention service that implements weighted random message selection to deliver environmental and cost-awareness messages to experimental user groups. Tracks user responses and transportation decisions to measure the effectiveness of different messaging strategies in promoting sustainable mobility choices.

**Business value explanation:**
Supports sustainable transportation initiatives, provides data for behavioral research, helps organizations meet environmental goals, reduces traffic congestion through behavior modification, and enables evidence-based policy making for transportation planning.

## 🔧 Technical Specifications

- **File:** `allrepo/connectsmart/tsp-api/src/services/mtc.js`
- **Language:** JavaScript (ES2020)
- **Framework:** Node.js with Mongoose and Knex.js
- **Type:** Behavioral Messaging and Experiment Service
- **File Size:** ~2.4 KB
- **Complexity Score:** ⭐⭐ (Low-Medium - Simple weighted selection with data tracking)

**Dependencies:**
- `mongoose`: MongoDB object modeling (**High**)
- `uuid`: UUID generation for plan tracking (**Medium**)
- `@app/src/models/mtc`: MTC message results model (**Critical**)
- `@maas/core/mysql`: MySQL database connection (**High**)

## 📝 Detailed Code Analysis

### Core Functions Overview

### isTargetUser Function

**Purpose:** Determines if a user is enrolled in the MTC experiment

**Parameters:**
- `user_id`: Number - User identifier to check

**Returns:** Promise resolving to boolean indicating enrollment status

**Implementation:**
```javascript
isTargetUser: async function (user_id) {
  const found = await knex('hybrid.mtc_user_signup').where({
    user_id,
  });
  return found.length > 0;
}
```

**Database Query:** Checks `hybrid.mtc_user_signup` table for user enrollment

### getMessage Function

**Purpose:** Selects a message using weighted random selection

**Parameters:**
- `user_id`: Number - User identifier (currently unused in selection)

**Returns:** Object with message index and content

**Implementation:**
```javascript
getMessage: function (user_id) {
  return this.randomChoose(this.dataProvider(), this.spreadList())();
}
```

**Selection Logic:** Uses dataProvider for messages and spreadList for weights

### Message Content Analysis

**Message Distribution:**
- **50% chance:** No message (empty title/message)
- **12.5% each:** Four different environmental messaging variants

**Message Variants:**
1. **Empty Message:** `{ title: '', message: '' }`
2. **$1 Cost Message:** Basic environmental impact messaging
3. **$3 Cost Message:** Higher cost environmental impact messaging  
4. **$1 + Personal:** Adds "You previously mentioned you care about environment"
5. **$3 + Personal:** Higher cost with personal environmental reference

### dataProvider Function

**Purpose:** Provides the array of available messages

**Returns:** Array of message objects with title and message fields

**Message Template:**
```javascript
{
  title: 'Wait',
  message: 'Wait! Driving is costly, leads to road congestion, and contributes to climate change. Driving for this trip will cost the planet $X. [Personal reference?] Will you consider using another mode of transportation instead?'
}
```

### spreadList Function

**Purpose:** Defines probability weights for message selection

**Returns:** Array of probability weights `[0.5, 0.125, 0.125, 0.125, 0.125]`

**Weight Interpretation:**
- 50% probability for no message (control group)
- 12.5% each for four message variants (experimental groups)

### randomChoose Function

**Purpose:** Implements weighted random selection algorithm

**Parameters:**
- `arr1`: Array - Items to choose from
- `arr2`: Array - Probability weights for each item

**Returns:** Function that performs weighted random selection

**Algorithm:**
```javascript
randomChoose: function (arr1, arr2) {
  // Validate input arrays
  if (!Array.isArray(arr1) || !Array.isArray(arr2))
    throw new TypeError('Arguments must be an array.');
  if (arr1.length !== arr2.length)
    throw new TypeError('arr1 and arr2 must have the same length.');
  
  // Create cumulative probability array
  const cuml = arr2.reduce((pre, cur, idx) => {
    if (idx > 0) {
      pre.push(pre[pre.length - 1] + cur);
    } else {
      pre.push(cur);
    }
    return pre;
  }, []);
  
  // Return selection function
  return function () {
    const seed = Math.random() * cuml[cuml.length - 1];
    const choosed = cuml.reduce((pre, cur, idx) => {
      if (seed > cur) pre = idx + 1;
      return pre;
    }, 0);
    
    return { idx: choosed, result: arr1[choosed] };
  };
}
```

### writeData Function

**Purpose:** Records user interaction and response data

**Parameters:**
- `user_id`: Number - User identifier
- `plan_id`: String - UUID for the trip plan
- `message_id`: Number - Index of selected message
- `message`: Object - Full message content
- `data`: Object - Additional interaction data

**Database Operations:**
1. Finds existing MessageResults document for user
2. Creates new document if none exists
3. Appends new record to user's records array
4. Saves updated document

**Data Structure:**
```javascript
{
  user_id,
  plan_id,
  message_id,
  created_on: new Date(),
  ...data // Additional tracking data
}
```

### getPlanId Function

**Purpose:** Generates unique identifier for trip plans

**Returns:** UUID v4 string

**Implementation:**
```javascript
getPlanId: function () {
  return uuidv4();
}
```

### test Function

**Purpose:** Testing utility to validate message distribution

**Parameters:**
- `n`: Number - Number of test selections to perform

**Returns:** Array showing count of each message selected

**Usage:** Validates that weighted random selection produces expected distribution

## 🚀 Usage Methods

### Basic Message Selection and Tracking
```javascript
const mtcService = require('@app/src/services/mtc');

async function handleUserTripRequest(userId, tripData) {
  try {
    // Check if user is part of MTC experiment
    const isTargetUser = await mtcService.isTargetUser(userId);
    
    if (!isTargetUser) {
      console.log(`User ${userId} not in MTC experiment`);
      return { showMessage: false, message: null };
    }
    
    // Generate plan ID for tracking
    const planId = mtcService.getPlanId();
    
    // Select message using weighted random selection
    const messageSelection = mtcService.getMessage(userId);
    const { idx: messageId, result: message } = messageSelection;
    
    // Check if message should be shown (empty message = control group)
    const showMessage = message.title !== '' && message.message !== '';
    
    if (showMessage) {
      console.log(`Showing message ${messageId} to user ${userId}`);
      
      // Track message display
      await mtcService.writeData(userId, planId, messageId, message, {
        trip_data: tripData,
        message_shown: true,
        display_timestamp: new Date().toISOString()
      });
    } else {
      console.log(`User ${userId} in control group - no message shown`);
      
      // Track control group
      await mtcService.writeData(userId, planId, messageId, message, {
        trip_data: tripData,
        message_shown: false,
        control_group: true
      });
    }
    
    return {
      planId,
      messageId,
      showMessage,
      message: showMessage ? message : null,
      experimentGroup: showMessage ? 'treatment' : 'control'
    };
  } catch (error) {
    console.error('Error handling MTC message:', error);
    throw error;
  }
}
```

### User Response Tracking
```javascript
async function trackUserResponse(userId, planId, responseData) {
  const mtcService = require('@app/src/services/mtc');
  
  try {
    // Track user's decision after seeing message
    await mtcService.writeData(userId, planId, null, null, {
      response_type: 'user_decision',
      chosen_mode: responseData.transportationMode,
      original_mode: responseData.originalMode,
      message_influenced: responseData.changedMind || false,
      response_time_seconds: responseData.responseTime,
      alternative_selected: responseData.alternativeMode,
      response_timestamp: new Date().toISOString()
    });
    
    return {
      tracked: true,
      userId,
      planId,
      decision: responseData.transportationMode,
      influenced: responseData.changedMind
    };
  } catch (error) {
    console.error('Error tracking user response:', error);
    throw error;
  }
}

// Usage
const responseData = {
  transportationMode: 'transit',
  originalMode: 'driving',
  changedMind: true,
  responseTime: 15.5,
  alternativeMode: 'bus'
};

const result = await trackUserResponse(12345, 'plan-uuid-123', responseData);
```

### Experiment Management
```javascript
class MTCExperimentManager {
  constructor() {
    this.mtcService = require('@app/src/services/mtc');
  }

  async enrollUser(userId, experimentGroup = 'standard') {
    const knex = require('@maas/core/mysql')('portal');
    
    try {
      // Check if user already enrolled
      const existing = await knex('hybrid.mtc_user_signup')
        .where('user_id', userId)
        .first();
      
      if (existing) {
        return {
          enrolled: false,
          reason: 'User already enrolled',
          existingGroup: existing.experiment_group
        };
      }
      
      // Enroll user in experiment
      await knex('hybrid.mtc_user_signup').insert({
        user_id: userId,
        experiment_group: experimentGroup,
        enrolled_at: new Date(),
        status: 'active'
      });
      
      return {
        enrolled: true,
        userId,
        experimentGroup,
        enrolledAt: new Date().toISOString()
      };
    } catch (error) {
      console.error('Error enrolling user in MTC experiment:', error);
      throw error;
    }
  }

  async getExperimentStats() {
    const knex = require('@maas/core/mysql')('portal');
    const { MessageResults } = require('@app/src/models/mtc');
    
    try {
      // Get enrollment stats
      const enrollmentStats = await knex('hybrid.mtc_user_signup')
        .select('experiment_group')
        .count('* as count')
        .groupBy('experiment_group');
      
      // Get message display stats
      const messageStats = await MessageResults.aggregate([
        { $unwind: '$records' },
        {
          $group: {
            _id: '$records.message_id',
            count: { $sum: 1 },
            users: { $addToSet: '$user_id' }
          }
        },
        {
          $project: {
            messageId: '$_id',
            displayCount: '$count',
            uniqueUsers: { $size: '$users' }
          }
        }
      ]);
      
      return {
        enrollment: enrollmentStats,
        messageDistribution: messageStats,
        totalUsers: enrollmentStats.reduce((sum, group) => sum + group.count, 0)
      };
    } catch (error) {
      console.error('Error getting experiment stats:', error);
      throw error;
    }
  }

  async analyzeMessageEffectiveness() {
    const { MessageResults } = require('@app/src/models/mtc');
    
    try {
      const results = await MessageResults.aggregate([
        { $unwind: '$records' },
        {
          $match: {
            'records.response_type': 'user_decision'
          }
        },
        {
          $group: {
            _id: '$records.message_id',
            totalResponses: { $sum: 1 },
            changedMind: {
              $sum: { $cond: ['$records.message_influenced', 1, 0] }
            },
            choseDriving: {
              $sum: { $cond: [{ $eq: ['$records.chosen_mode', 'driving'] }, 1, 0] }
            },
            choseAlternative: {
              $sum: { $cond: [{ $ne: ['$records.chosen_mode', 'driving'] }, 1, 0] }
            }
          }
        },
        {
          $project: {
            messageId: '$_id',
            totalResponses: 1,
            changedMind: 1,
            choseDriving: 1,
            choseAlternative: 1,
            influenceRate: {
              $cond: [
                { $gt: ['$totalResponses', 0] },
                { $divide: ['$changedMind', '$totalResponses'] },
                0
              ]
            },
            alternativeRate: {
              $cond: [
                { $gt: ['$totalResponses', 0] },
                { $divide: ['$choseAlternative', '$totalResponses'] },
                0
              ]
            }
          }
        }
      ]);
      
      return results.map(result => ({
        messageId: result.messageId,
        messageType: this.getMessageType(result.messageId),
        responses: result.totalResponses,
        influenced: result.changedMind,
        choseAlternative: result.choseAlternative,
        influenceRate: (result.influenceRate * 100).toFixed(2) + '%',
        alternativeRate: (result.alternativeRate * 100).toFixed(2) + '%'
      }));
    } catch (error) {
      console.error('Error analyzing message effectiveness:', error);
      throw error;
    }
  }

  getMessageType(messageId) {
    const types = {
      0: 'Control (No Message)',
      1: '$1 Environmental',
      2: '$3 Environmental', 
      3: '$1 Environmental + Personal',
      4: '$3 Environmental + Personal'
    };
    return types[messageId] || 'Unknown';
  }

  async generateExperimentReport(startDate, endDate) {
    const { MessageResults } = require('@app/src/models/mtc');
    
    try {
      const dateFilter = {
        'records.created_on': {
          $gte: new Date(startDate),
          $lte: new Date(endDate)
        }
      };
      
      // Overall statistics
      const overallStats = await MessageResults.aggregate([
        { $unwind: '$records' },
        { $match: dateFilter },
        {
          $group: {
            _id: null,
            totalInteractions: { $sum: 1 },
            uniqueUsers: { $addToSet: '$user_id' },
            messagesShown: {
              $sum: { $cond: ['$records.message_shown', 1, 0] }
            },
            controlGroup: {
              $sum: { $cond: [{ $eq: ['$records.message_id', 0] }, 1, 0] }
            }
          }
        }
      ]);
      
      // Message effectiveness
      const effectiveness = await this.analyzeMessageEffectiveness();
      
      // Daily trends
      const dailyTrends = await MessageResults.aggregate([
        { $unwind: '$records' },
        { $match: dateFilter },
        {
          $group: {
            _id: {
              $dateToString: {
                format: '%Y-%m-%d',
                date: '$records.created_on'
              }
            },
            interactions: { $sum: 1 },
            messagesShown: {
              $sum: { $cond: ['$records.message_shown', 1, 0] }
            }
          }
        },
        { $sort: { _id: 1 } }
      ]);
      
      return {
        reportPeriod: { startDate, endDate },
        overall: overallStats[0] || {},
        messageEffectiveness: effectiveness,
        dailyTrends,
        generatedAt: new Date().toISOString()
      };
    } catch (error) {
      console.error('Error generating experiment report:', error);
      throw error;
    }
  }
}
```

### Testing and Validation
```javascript
class MTCTester {
  constructor() {
    this.mtcService = require('@app/src/services/mtc');
  }

  testMessageDistribution(iterations = 10000) {
    console.log(`Testing message distribution with ${iterations} iterations...`);
    
    const results = this.mtcService.test(iterations);
    const percentages = results.map(count => (count / iterations * 100).toFixed(2));
    
    return {
      iterations,
      results: {
        'No Message (Control)': { count: results[0], percentage: percentages[0] + '%' },
        '$1 Environmental': { count: results[1], percentage: percentages[1] + '%' },
        '$3 Environmental': { count: results[2], percentage: percentages[2] + '%' },
        '$1 + Personal': { count: results[3], percentage: percentages[3] + '%' },
        '$3 + Personal': { count: results[4], percentage: percentages[4] + '%' }
      },
      expectedDistribution: {
        'Control': '50.00%',
        'Each Treatment': '12.50%'
      }
    };
  }

  async testMessageSelection(userId = 999999) {
    try {
      const selections = [];
      
      for (let i = 0; i < 10; i++) {
        const selection = this.mtcService.getMessage(userId);
        selections.push({
          iteration: i + 1,
          messageId: selection.idx,
          messageType: selection.result.title || 'No Message',
          hasContent: selection.result.message !== ''
        });
      }
      
      return {
        userId,
        selections,
        summary: {
          withMessage: selections.filter(s => s.hasContent).length,
          withoutMessage: selections.filter(s => !s.hasContent).length
        }
      };
    } catch (error) {
      console.error('Error testing message selection:', error);
      throw error;
    }
  }

  async testDataWriting(userId = 999999) {
    try {
      const planId = this.mtcService.getPlanId();
      const testData = {
        test: true,
        timestamp: new Date().toISOString(),
        scenario: 'unit_test'
      };
      
      await this.mtcService.writeData(userId, planId, 1, 
        { title: 'Test', message: 'Test message' }, testData);
      
      // Verify data was written
      const { MessageResults } = require('@app/src/models/mtc');
      const result = await MessageResults.findOne({ user_id: userId });
      
      return {
        dataWritten: true,
        planId,
        recordsCount: result ? result.records.length : 0,
        lastRecord: result ? result.records[result.records.length - 1] : null
      };
    } catch (error) {
      console.error('Error testing data writing:', error);
      throw error;
    }
  }

  async runFullTestSuite() {
    console.log('Running MTC Service Test Suite...');
    
    const results = {
      testSuite: 'MTC Service',
      timestamp: new Date().toISOString(),
      tests: {}
    };
    
    // Test 1: Distribution
    try {
      results.tests.distribution = {
        passed: true,
        result: this.testMessageDistribution(1000)
      };
    } catch (error) {
      results.tests.distribution = {
        passed: false,
        error: error.message
      };
    }
    
    // Test 2: Message Selection
    try {
      results.tests.messageSelection = {
        passed: true,
        result: await this.testMessageSelection()
      };
    } catch (error) {
      results.tests.messageSelection = {
        passed: false,
        error: error.message
      };
    }
    
    // Test 3: Data Writing
    try {
      results.tests.dataWriting = {
        passed: true,
        result: await this.testDataWriting()
      };
    } catch (error) {
      results.tests.dataWriting = {
        passed: false,
        error: error.message
      };
    }
    
    const passedTests = Object.values(results.tests).filter(t => t.passed).length;
    const totalTests = Object.keys(results.tests).length;
    
    results.summary = {
      passed: passedTests,
      failed: totalTests - passedTests,
      total: totalTests,
      successRate: ((passedTests / totalTests) * 100).toFixed(2) + '%'
    };
    
    console.log(`Test Suite Complete: ${passedTests}/${totalTests} tests passed`);
    return results;
  }
}
```

## 📊 Output Examples

### Message Selection Result
```json
{
  "idx": 2,
  "result": {
    "title": "Wait",
    "message": "Wait! Driving is costly, leads to road congestion, and contributes to climate change. Driving for this trip will cost the planet $3. Will you consider using another mode of transportation instead?"
  }
}
```

### User Interaction Tracking
```json
{
  "planId": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "messageId": 2,
  "showMessage": true,
  "message": {
    "title": "Wait",
    "message": "Wait! Driving is costly..."
  },
  "experimentGroup": "treatment"
}
```

### Experiment Statistics
```json
{
  "enrollment": [
    { "experiment_group": "standard", "count": 1250 },
    { "experiment_group": "enhanced", "count": 875 }
  ],
  "messageDistribution": [
    { "messageId": 0, "displayCount": 5000, "uniqueUsers": 1200 },
    { "messageId": 1, "displayCount": 1250, "uniqueUsers": 300 },
    { "messageId": 2, "displayCount": 1200, "uniqueUsers": 295 }
  ],
  "totalUsers": 2125
}
```

### Message Effectiveness Analysis
```json
[
  {
    "messageId": 1,
    "messageType": "$1 Environmental",
    "responses": 300,
    "influenced": 45,
    "choseAlternative": 120,
    "influenceRate": "15.00%",
    "alternativeRate": "40.00%"
  },
  {
    "messageId": 2,
    "messageType": "$3 Environmental",
    "responses": 295,
    "influenced": 62,
    "choseAlternative": 135,
    "influenceRate": "21.02%",
    "alternativeRate": "45.76%"
  }
]
```

### Distribution Test Results
```json
{
  "iterations": 10000,
  "results": {
    "No Message (Control)": { "count": 4998, "percentage": "49.98%" },
    "$1 Environmental": { "count": 1251, "percentage": "12.51%" },
    "$3 Environmental": { "count": 1247, "percentage": "12.47%" },
    "$1 + Personal": { "count": 1252, "percentage": "12.52%" },
    "$3 + Personal": { "count": 1252, "percentage": "12.52%" }
  },
  "expectedDistribution": {
    "Control": "50.00%",
    "Each Treatment": "12.50%"
  }
}
```

## ⚠️ Important Notes

### Experimental Design
- **Control Group:** 50% of interactions show no message for baseline comparison
- **Treatment Groups:** Four different message variants with equal probability
- **Randomization:** True randomization ensures unbiased experimental conditions
- **Tracking:** Comprehensive data collection for statistical analysis

### Message Content Strategy
- **Environmental Focus:** All messages emphasize environmental impact of driving
- **Cost Framing:** Messages use monetary cost ($1, $3) to quantify impact
- **Personalization:** Some messages reference user's stated environmental preferences
- **Call to Action:** All messages ask user to consider alternative transportation

### Behavioral Science Elements
- **Nudging:** Gentle persuasion rather than forcing behavior change
- **Loss Framing:** Emphasizes cost/loss rather than benefits
- **Social Proof:** References environmental values user previously expressed
- **Timing:** Messages shown at moment of transportation decision

### Data Collection and Privacy
- **User Consent:** Assumes users consented to participate in experiment
- **Data Minimization:** Collects only data necessary for experiment analysis
- **Anonymization:** User data should be anonymized for analysis
- **Retention:** Consider data retention policies for experimental data

### Statistical Considerations
- **Sample Size:** Ensure adequate sample size for statistical significance
- **A/B Testing:** Proper control group maintains scientific validity
- **Randomization:** Weighted random selection prevents selection bias
- **Power Analysis:** Calculate required sample sizes for detecting effects

### Implementation Considerations
- **Performance:** Lightweight message selection for real-time use
- **Scalability:** MongoDB storage scales with user base growth
- **Error Handling:** Graceful fallback when systems unavailable
- **Monitoring:** Track message delivery success rates

### Business and Ethical Considerations
- **Transparency:** Users should know they're part of an experiment
- **Opt-out:** Provide mechanism for users to exit experiment
- **Effectiveness:** Measure actual behavior change, not just stated intentions
- **Unintended Effects:** Monitor for negative user experience impacts

## 🔗 Related File Links

- **MTC Models:** `allrepo/connectsmart/tsp-api/src/models/mtc.js`
- **User Enrollment:** Database tables for experiment participant management
- **Transportation Controllers:** API endpoints that trigger message display
- **Analytics Dashboard:** UI components for viewing experiment results

---
*This service provides essential behavioral intervention capabilities for promoting sustainable transportation choices through targeted messaging experiments in the TSP platform.*