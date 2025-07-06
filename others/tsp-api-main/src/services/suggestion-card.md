# TSP API Suggestion Card Service Documentation

## 🔍 Quick Summary (TL;DR)
The Suggestion Card service manages interactive campaign cards that provide travel suggestions to users, handles card retrieval with point calculations, processes card dismissals with status updates, and maintains user engagement records for campaign analytics.

**Keywords:** suggestion-cards | campaign-management | user-engagement | notification-types | point-calculations | card-dismissal | microsurveys | travel-recommendations

**Primary use cases:** Retrieving suggestion cards with points, dismissing cards and updating status, managing campaign user interactions, tracking engagement analytics

**Compatibility:** Node.js >= 16.0.0, MySQL database with campaign models, moment.js for timestamp handling, error handling with custom error codes

## ❓ Common Questions Quick Index
- **Q: What types of suggestion cards exist?** → Info cards, timing suggestions (early/later), mode changes, microsurveys, carpool matching, WTA options
- **Q: How are points calculated?** → From campaign points for most types, from user points for WTA (action types 7-9)
- **Q: What happens when cards are dismissed?** → Status updated to 3, user record created/updated with reply_status 1
- **Q: How are notification types mapped?** → Action types 1-9 map to specific notification types (SUGGESTION_INFO, SUGGESTION_GO_EARLY, etc.)
- **Q: What's special about action type 5?** → Microsurvey questions redirect to step 1 of the same campaign
- **Q: How is user engagement tracked?** → Through CMUserRecords with points, reply status, and action types

## 📋 Functionality Overview

**Non-technical explanation:** 
Think of this as a **smart suggestion system** that shows users helpful travel tips and recommendations. Users can see suggestions like "leave earlier" or "try carpooling" along with rewards points, and when they dismiss or interact with these suggestions, the system tracks their engagement for analytics.

**Technical explanation:** 
A campaign card management service that retrieves suggestion cards with dynamic point calculations based on action types, maps action types to notification categories, handles card dismissals with status updates, and maintains comprehensive user engagement records for campaign effectiveness tracking.

**Business value explanation:**
Drives user engagement through targeted travel suggestions, provides incentives through point rewards, enables data-driven campaign optimization through engagement tracking, supports behavior change initiatives, and facilitates user retention through interactive content.

## 🔧 Technical Specifications

- **File:** `allrepo/connectsmart/tsp-api/src/services/suggestion-card.js`
- **Language:** JavaScript (ES2020)
- **Framework:** Node.js with Objection.js ORM and moment.js
- **Type:** Campaign Card Management and User Engagement Service
- **File Size:** ~4.2 KB
- **Complexity Score:** ⭐⭐⭐ (Medium-High - Complex business logic with multiple models)

**Dependencies:**
- `moment-timezone`: Date/time handling for timestamps (**High**)
- `@app/src/models/CMSteps`: Campaign step data model (**Critical**)
- `@app/src/models/CMCampaignUsers`: User campaign participation (**Critical**)
- `@app/src/models/CMUserRecords`: User engagement tracking (**Critical**)
- `@app/src/static/defines`: Notification types and constants (**High**)
- `@app/src/static/error-code`: Error handling definitions (**Medium**)

## 📝 Detailed Code Analysis

### Card Retrieval System

### get Function
**Purpose:** Retrieves suggestion card details with notification type and point calculations

```javascript
get: async (userId, cardId) => {
  let cmStepId = cardId;
  
  // Fetch card with campaign details
  const card = await CMSteps.query()
    .where('id', cardId)
    .withGraphFetched('cmCampaign')
    .first();

  if (!card) {
    logger.warn(`Could not find the cm_step by id:${cardId}`);
    throw new MaasError(ERROR_CODE.ERROR_NOT_FOUND_CARD, 'warn', 'Not found card', 403);
  }

  // Base point calculation from campaign
  let addPoints = card.cmCampaign.points
    ? Math.round(card.cmCampaign.points * 100) / 100
    : 0;

  // Action type to notification type mapping
  const notificationTypeList = {
    1: SUGGESTION_INFO,
    2: SUGGESTION_GO_EARLY,
    3: SUGGESTION_GO_LATER,
    4: SUGGESTION_CHANGE_MODE,
    5: MICROSURVEY_MULTIPLE_CHOICE_QUESTION,
    6: SUGGESTION_CARPOOL_AUTO_MATCH,
    7: WTA_GO_LATER,
    8: WTA_GO_EARLY,
    9: WTA_CHANGE_MODE,
  };
  
  const notificationType = notificationTypeList[card.action_type] ?? GENERAL;
}
```

**Key Features:**
- **Graph Fetching:** Efficiently loads related campaign data
- **Error Handling:** Validates card existence with specific error codes
- **Point Precision:** Handles decimal points with proper rounding
- **Notification Mapping:** Maps action types to UI notification categories

### Special Action Type Handling

#### Microsurvey Redirection (Action Type 5)
```javascript
if (card.action_type === 5) {
  const cmStep = await CMSteps.query()
    .where({
      campaign_id: card.cmCampaign.id,
      step_no: 1,
    })
    .first();
  cmStepId = cmStep.id;
  logger.info(`Action Type is 5, Change card id to ${cmStep.id}`);
}
```
- **Redirection Logic:** Microsurvey questions redirect to step 1 of campaign
- **Step Number Lookup:** Finds first step of the same campaign
- **ID Substitution:** Changes effective card ID for user lookup

### User Campaign Validation

#### Campaign User Lookup
```javascript
const campaignUser = await CMCampaignUsers.query()
  .select(['points', 'status'])
  .where({ step_id: cmStepId, user_id: userId })
  .first();
  
if (!campaignUser) {
  logger.warn(`Could not find the cm_campaign_user by step_id:${cmStepId}`);
  throw new MaasError(ERROR_CODE.ERROR_NOT_FOUND_CARD, 'warn', 'Not found card', 200);
}
```
- **User Validation:** Ensures user is enrolled in campaign step
- **Status Tracking:** Retrieves current user status and points
- **Access Control:** Prevents unauthorized card access

### WTA Point Calculation

#### Special Point Logic for Action Types 7-9
```javascript
if (card.action_type >= 7 && card.action_type <= 9) {
  addPoints = campaignUser.points
    ? Math.round(campaignUser.points * 100) / 100
    : 0;
}
```
- **WTA Override:** Willingness-To-Accept actions use user-specific points
- **Individual Pricing:** Each user may have different point values
- **Precision Handling:** Maintains decimal precision for financial accuracy

### Card Dismissal System

### delete Function
**Purpose:** Handles card dismissal with status updates and engagement tracking

```javascript
delete: async (userId, cardId) => {
  // Find campaign user record
  const campaignUser = await CMCampaignUsers.query()
    .where({
      step_id: cardId,
      user_id: userId,
    })
    .first();
    
  if (!campaignUser) {
    logger.warn(`Could not find the cm_campaign_user by step_id:${cardId}`);
    throw new MaasError(ERROR_CODE.ERROR_SUGGESTION_CARD_ID_NOT_FOUND, 'warn', 'Invalid parameters', 400);
  }

  // Update card status to dismissed (3)
  const curTime = moment.utc().format(TIME_FORMAT);
  await CMCampaignUsers.query()
    .where({
      step_id: cardId,
      user_id: userId,
    })
    .update({ status: 3 });
}
```

**Processing Steps:**
1. **User Validation:** Confirms user has access to the card
2. **Status Update:** Changes status to 3 (dismissed)
3. **Timestamp Generation:** Uses UTC time for consistency

### User Engagement Tracking

#### Record Management
```javascript
const cmUserRecord = await CMUserRecords.query()
  .where({ user_id: userId, campaign_id: campaignUser.campaign_id })
  .first();

if (cmUserRecord) {
  // Update existing record
  await CMUserRecords.query()
    .where('user_id', userId)
    .where('campaign_id', campaignUser.campaign_id)
    .update({ points: 0, reply_status: 1 });
} else {
  // Create new record
  await CMUserRecords.query().insert({
    user_id: userId,
    campaign_id: campaignUser.campaign_id,
    action_type: 'infocard',
    points: 0,
    reply_status: 1,
    created_on: curTime,
    modified_on: curTime,
  });
}
```

**Record Logic:**
- **Upsert Pattern:** Updates existing records or creates new ones
- **Zero Points:** Dismissal actions don't award points
- **Reply Status:** Tracks user interaction (1 = dismissed)
- **Action Type:** Categorizes interaction as 'infocard' dismissal

## 🚀 Usage Methods

### Basic Card Operations
```javascript
const suggestionCardService = require('@app/src/services/suggestion-card');

// Get suggestion card details
const cardDetails = await suggestionCardService.get(12345, 678);
console.log('Card details:', cardDetails);
// { notification_type: 'SUGGESTION_GO_EARLY', points: 5.50, status: 1 }

// Dismiss a suggestion card
await suggestionCardService.delete(12345, 678);
console.log('Card dismissed successfully');
```

### Advanced Campaign Card Manager
```javascript
class CampaignCardManager {
  constructor() {
    this.suggestionCardService = require('@app/src/services/suggestion-card');
    this.activeCards = new Map();
  }

  async getUserActiveCards(userId) {
    try {
      // Get all active campaign users for this user
      const activeCampaignUsers = await CMCampaignUsers.query()
        .where('user_id', userId)
        .where('status', '!=', 3) // Not dismissed
        .withGraphFetched('[cmStep.cmCampaign]');

      const cards = [];
      
      for (const campaignUser of activeCampaignUsers) {
        try {
          const cardDetails = await this.suggestionCardService.get(userId, campaignUser.step_id);
          
          cards.push({
            cardId: campaignUser.step_id,
            campaignId: campaignUser.campaign_id,
            campaignName: campaignUser.cmStep?.cmCampaign?.name || 'Unknown Campaign',
            ...cardDetails,
            createdAt: campaignUser.created_on,
            stepNumber: campaignUser.cmStep?.step_no || 1
          });
        } catch (error) {
          console.error(`Error getting card ${campaignUser.step_id}:`, error.message);
        }
      }

      return {
        userId,
        totalCards: cards.length,
        cards: cards.sort((a, b) => new Date(b.createdAt) - new Date(a.createdAt))
      };
    } catch (error) {
      console.error('Error getting user active cards:', error);
      return {
        userId,
        totalCards: 0,
        cards: [],
        error: error.message
      };
    }
  }

  async interactWithCard(userId, cardId, action = 'dismiss') {
    try {
      const cardDetails = await this.suggestionCardService.get(userId, cardId);
      
      if (action === 'dismiss') {
        await this.suggestionCardService.delete(userId, cardId);
        
        return {
          success: true,
          action: 'dismissed',
          cardId,
          userId,
          pointsAwarded: 0 // Dismissal doesn't award points
        };
      } else if (action === 'engage') {
        // Custom engagement logic
        const result = await this.processCardEngagement(userId, cardId, cardDetails);
        return result;
      }
      
      return {
        success: false,
        error: `Unknown action: ${action}`
      };
    } catch (error) {
      console.error('Error interacting with card:', error);
      return {
        success: false,
        cardId,
        userId,
        error: error.message
      };
    }
  }

  async processCardEngagement(userId, cardId, cardDetails) {
    // Custom engagement processing based on notification type
    let pointsAwarded = cardDetails.points;
    let engagementType = 'general';

    switch (cardDetails.notification_type) {
      case 'SUGGESTION_GO_EARLY':
        engagementType = 'timing_adjustment';
        break;
      case 'SUGGESTION_CHANGE_MODE':
        engagementType = 'mode_change';
        break;
      case 'SUGGESTION_CARPOOL_AUTO_MATCH':
        engagementType = 'carpool_interest';
        break;
      case 'MICROSURVEY_MULTIPLE_CHOICE_QUESTION':
        engagementType = 'survey_response';
        pointsAwarded = 0; // Surveys handle points separately
        break;
      default:
        engagementType = 'information_viewed';
    }

    // Record engagement (would need custom implementation)
    await this.recordEngagement(userId, cardId, engagementType, pointsAwarded);

    return {
      success: true,
      action: 'engaged',
      cardId,
      userId,
      engagementType,
      pointsAwarded
    };
  }

  async recordEngagement(userId, cardId, engagementType, pointsAwarded) {
    // Custom engagement recording logic
    console.log(`Recording engagement: User ${userId}, Card ${cardId}, Type: ${engagementType}, Points: ${pointsAwarded}`);
    
    // Could update CMUserRecords with positive points and engagement type
    // await CMUserRecords.query().insert({
    //   user_id: userId,
    //   step_id: cardId,
    //   action_type: engagementType,
    //   points: pointsAwarded,
    //   reply_status: 2, // Engaged vs dismissed
    //   created_on: moment.utc().format(TIME_FORMAT)
    // });
  }

  async getCardAnalytics(campaignId) {
    try {
      // Get campaign card analytics
      const analytics = await CMUserRecords.query()
        .where('campaign_id', campaignId)
        .groupBy('action_type')
        .select('action_type')
        .count('id as count')
        .sum('points as total_points')
        .avg('points as avg_points');

      const campaignUsers = await CMCampaignUsers.query()
        .where('campaign_id', campaignId)
        .groupBy('status')
        .select('status')
        .count('id as count');

      return {
        campaignId,
        engagementBreakdown: analytics,
        statusDistribution: campaignUsers,
        totalEngagements: analytics.reduce((sum, item) => sum + parseInt(item.count), 0),
        totalPointsAwarded: analytics.reduce((sum, item) => sum + parseFloat(item.total_points || 0), 0)
      };
    } catch (error) {
      console.error('Error getting card analytics:', error);
      return {
        campaignId,
        error: error.message
      };
    }
  }

  async bulkDismissCards(userId, cardIds) {
    const results = [];
    
    for (const cardId of cardIds) {
      try {
        await this.suggestionCardService.delete(userId, cardId);
        results.push({
          cardId,
          success: true,
          action: 'dismissed'
        });
      } catch (error) {
        results.push({
          cardId,
          success: false,
          error: error.message
        });
      }
    }

    return {
      userId,
      totalCards: cardIds.length,
      successful: results.filter(r => r.success).length,
      failed: results.filter(r => !r.success).length,
      details: results
    };
  }
}

// Usage
const cardManager = new CampaignCardManager();

// Get user's active cards
const activeCards = await cardManager.getUserActiveCards(12345);
console.log('Active cards:', activeCards);

// Interact with a card
const interaction = await cardManager.interactWithCard(12345, 678, 'engage');
console.log('Interaction result:', interaction);

// Get campaign analytics
const analytics = await cardManager.getCardAnalytics(456);
console.log('Campaign analytics:', analytics);

// Bulk dismiss cards
const bulkResult = await cardManager.bulkDismissCards(12345, [678, 679, 680]);
console.log('Bulk dismissal result:', bulkResult);
```

### Card Type Specific Handlers
```javascript
class SpecializedCardHandlers {
  constructor() {
    this.suggestionCardService = require('@app/src/services/suggestion-card');
  }

  async handleMicrosurveyCard(userId, cardId) {
    try {
      const cardDetails = await this.suggestionCardService.get(userId, cardId);
      
      if (cardDetails.notification_type === 'MICROSURVEY_MULTIPLE_CHOICE_QUESTION') {
        // Special handling for microsurvey cards
        return {
          type: 'microsurvey',
          cardId,
          requiresResponse: true,
          pointsAvailable: cardDetails.points,
          instructions: 'Please complete the survey to earn points'
        };
      }
      
      return cardDetails;
    } catch (error) {
      return {
        error: error.message,
        cardId
      };
    }
  }

  async handleWTACard(userId, cardId) {
    try {
      const cardDetails = await this.suggestionCardService.get(userId, cardId);
      
      // Check if it's a WTA card (action types 7-9)
      const wtaTypes = ['WTA_GO_LATER', 'WTA_GO_EARLY', 'WTA_CHANGE_MODE'];
      
      if (wtaTypes.includes(cardDetails.notification_type)) {
        return {
          type: 'willingness_to_accept',
          cardId,
          offerAmount: cardDetails.points,
          acceptanceRequired: true,
          expirationTime: this.calculateWTAExpiration(),
          instructions: `Accept this offer to earn ${cardDetails.points} points`
        };
      }
      
      return cardDetails;
    } catch (error) {
      return {
        error: error.message,
        cardId
      };
    }
  }

  calculateWTAExpiration() {
    // WTA offers typically expire quickly
    return moment().add(15, 'minutes').toISOString();
  }

  async handleCarpoolCard(userId, cardId) {
    try {
      const cardDetails = await this.suggestionCardService.get(userId, cardId);
      
      if (cardDetails.notification_type === 'SUGGESTION_CARPOOL_AUTO_MATCH') {
        return {
          type: 'carpool_suggestion',
          cardId,
          pointsAvailable: cardDetails.points,
          requiresAction: true,
          actionType: 'carpool_matching',
          instructions: 'Tap to find carpool matches and earn points'
        };
      }
      
      return cardDetails;
    } catch (error) {
      return {
        error: error.message,
        cardId
      };
    }
  }
}

// Usage
const specializedHandlers = new SpecializedCardHandlers();

// Handle different card types
const microsurvey = await specializedHandlers.handleMicrosurveyCard(12345, 678);
const wtaOffer = await specializedHandlers.handleWTACard(12345, 679);
const carpoolSuggestion = await specializedHandlers.handleCarpoolCard(12345, 680);
```

## 📊 Output Examples

### Card Retrieval Response
```javascript
{
  notification_type: "SUGGESTION_GO_EARLY",
  points: 5.50,
  status: 1
}
```

### Card Dismissal Response
```javascript
{} // Empty object indicates successful dismissal
```

### User Active Cards Summary
```javascript
{
  userId: 12345,
  totalCards: 3,
  cards: [
    {
      cardId: 678,
      campaignId: 456,
      campaignName: "Morning Commute Optimization",
      notification_type: "SUGGESTION_GO_EARLY",
      points: 5.50,
      status: 1,
      createdAt: "2024-06-25T09:00:00Z",
      stepNumber: 2
    },
    {
      cardId: 679,
      campaignId: 457,
      campaignName: "Mode Choice Survey",
      notification_type: "MICROSURVEY_MULTIPLE_CHOICE_QUESTION",
      points: 2.00,
      status: 1,
      createdAt: "2024-06-25T08:30:00Z",
      stepNumber: 1
    }
  ]
}
```

### Campaign Analytics
```javascript
{
  campaignId: 456,
  engagementBreakdown: [
    { action_type: "infocard", count: "15", total_points: "0", avg_points: "0" },
    { action_type: "timing_adjustment", count: "8", total_points: "44.00", avg_points: "5.50" }
  ],
  statusDistribution: [
    { status: 1, count: "12" },
    { status: 3, count: "23" }
  ],
  totalEngagements: 23,
  totalPointsAwarded: 44.00
}
```

### Specialized Card Responses
```javascript
// Microsurvey Card
{
  type: "microsurvey",
  cardId: 678,
  requiresResponse: true,
  pointsAvailable: 2.00,
  instructions: "Please complete the survey to earn points"
}

// WTA Card
{
  type: "willingness_to_accept",
  cardId: 679,
  offerAmount: 8.75,
  acceptanceRequired: true,
  expirationTime: "2024-06-25T15:45:00.000Z",
  instructions: "Accept this offer to earn 8.75 points"
}
```

## ⚠️ Important Notes

### Action Type Mapping and Business Logic
- **Notification Types:** Nine action types map to specific UI notification categories
- **Point Calculations:** Base points from campaigns, user-specific points for WTA actions
- **Microsurvey Handling:** Action type 5 redirects to step 1 for question flow
- **Status Management:** Status 3 indicates dismissed cards

### User Engagement and Analytics
- **Record Tracking:** CMUserRecords maintains comprehensive engagement history
- **Upsert Pattern:** Updates existing records or creates new ones for user interactions
- **Zero Point Dismissals:** Card dismissals don't award points but track engagement
- **Reply Status:** Distinguishes between different interaction types

### Error Handling and Validation
- **Card Validation:** Ensures cards exist before processing
- **User Authorization:** Validates user access to specific campaign steps
- **Custom Error Codes:** Uses specific error codes for different failure scenarios
- **Graceful Degradation:** Continues processing even if individual cards fail

### Database Design and Performance
- **Graph Fetching:** Efficiently loads related campaign data in single queries
- **Selective Updates:** Only updates necessary fields to minimize database load
- **Time Consistency:** Uses UTC timestamps for cross-timezone consistency
- **Indexing Requirements:** Relies on proper indexing of user_id and step_id combinations

## 🔗 Related File Links

- **Campaign Models:** `allrepo/connectsmart/tsp-api/src/models/CMSteps.js`, `allrepo/connectsmart/tsp-api/src/models/CMCampaignUsers.js`
- **Record Models:** `allrepo/connectsmart/tsp-api/src/models/CMUserRecords.js`
- **Notification Definitions:** `allrepo/connectsmart/tsp-api/src/static/defines.js`
- **Error Handling:** `allrepo/connectsmart/tsp-api/src/static/error-code.js`

---
*This service provides comprehensive suggestion card management with user engagement tracking and analytics for campaign effectiveness in the TSP platform.*