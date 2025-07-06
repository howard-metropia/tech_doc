# IncentiveUtility Service

## Quick Summary

The IncentiveUtility service provides a comprehensive collection of utility functions that support the ConnectSmart incentive system. This service acts as a foundational layer offering database operations, timezone management, market profile handling, random number generation, and campaign management capabilities. It serves as the backbone for incentive processing, user management, and promotional campaign execution.

**Key Features:**
- Multi-timezone support with automatic conversion utilities
- Market-based user segmentation and management
- Advanced random number generation for dynamic rewards
- Campaign and notification management system
- Database abstraction for user wallet operations
- Comprehensive data querying and filtering capabilities

## Technical Analysis

### Architecture Overview

The service is structured as a module export containing utility functions organized into distinct functional areas: user data management, timezone operations, market profile handling, wallet operations, and campaign management. Each function is designed to be stateless and reusable across different parts of the incentive system.

### Core Functional Areas

#### 1. User Data Management
```javascript
async getUserCompoundData() {
  return await knex.raw(`
    SELECT user_tb.id,
      user_tb.created_on,
      user_tb.registration_longitude,
      user_tb.registration_latitude,
      IFNULL(trip_f.trips,0) as trips,
      max(trip_f.last_trip_time) as last_trip_time,
      IFNULL(TIMESTAMPDIFF(day, user_tb.created_on, NOW()), 0) AS user_days,
      IFNULL(TIMESTAMPDIFF(day, max(trip_f.last_trip_time), NOW()),-1) AS trip_to_now
    FROM hybrid.auth_user user_tb
    left JOIN (SELECT trip_tb.user_id, count(trip_tb.user_id) as trips,
               MAX(trip_tb.started_on) as last_trip_time
               FROM (select * from hybrid.trip ori_trip where distance > 5) trip_tb 
               GROUP BY user_id) trip_f on trip_f.user_id = user_tb.id
    WHERE user_tb.created_on IS NOT NULL
    GROUP BY user_tb.id
  `);
}
```

#### 2. Timezone Management System
```javascript
getTargetTimeZone(allTimeZones, hourMinutes) {
  for (const t in allTimeZones) {
    const localDateTime = tz.tz(allTimeZones[t]).format('YYYY-MM-DD HH:mm:ss');
    const localHourMinutes = tz.tz(allTimeZones[t]).format('HH:mm');
    if (localHourMinutes == hourMinutes) {
      return allTimeZones[t];
    }
  }
}
```

#### 3. Market Profile Operations
```javascript
getMarketPolygon(targetMarket, data) {
  const marketInfo = data.Market_info;
  for (const k in marketInfo) {
    if (marketInfo[k].Market == targetMarket) {
      let coordinates = marketInfo[k].Polygon.length > 0 ? 
        parse(marketInfo[k].Polygon).coordinates : [];
      
      return {
        market: targetMarket,
        coordinates: coordinates,
        timezone: marketInfo[k].Timezone,
        random_incnetive: marketInfo[k].random_incnetive,
        info_tile_before_action: marketInfo[k].info_tile_before_action,
        retention_time: marketInfo[k].retention_time
      };
    }
  }
}
```

### Statistical Random Generation

The service implements sophisticated random number generation using gamma distribution:

```javascript
rgamma(alpha, beta) {
  const SG_MAGICCONST = 1 + Math.log(4.5);
  const LOG4 = Math.log(4.0);
  
  if (alpha > 1) {
    // R.C.H. Cheng algorithm for non-integral shape parameters
    const ainv = Math.sqrt(2.0 * alpha - 1.0);
    const bbb = alpha - LOG4;
    const ccc = alpha + ainv;
    // Advanced mathematical generation logic
  } else if (alpha == 1.0) {
    // Exponential distribution case
    return -Math.log(Math.random()) * beta;
  } else {
    // Algorithm GS for 0 < alpha < 1
    // Statistical Computing implementation
  }
}
```

### Campaign Management Architecture

The service provides comprehensive campaign creation and management:

```javascript
async addToActionTile(row, userId, module = '') {
  const campaignId = await knex('cm_campaign').insert({
    is_active: 1,
    name: row.name,
    description: row.description,
    type_id: 4, // Change Mode campaign type
    creater: 'sibu.wang@metropia.com',
    utc_setting: row.timezone,
    start_time: startDate,
    end_time: endDate,
    travel_modes: '[1]',
    change_mode_transport: row.changeModeTransport,
    points: row.points,
    status: 1
  });
  
  const stepId = await knex('cm_step').insert({
    campaign_id: campaignId,
    title: row.title,
    body: row.body,
    diff_time: 900,
    action_type: 4,
    step_no: 1,
    choice_type: 1,
    sys_question_id: 0
  });
  
  return campaignId;
}
```

## Usage/Integration

### Primary Integration Patterns

#### 1. User Data Aggregation
```javascript
// Comprehensive user analytics with trip history
const userData = await getUserCompoundData();
userData.forEach(user => {
  console.log(`User ${user.id}: ${user.trips} trips, ${user.user_days} days active`);
});
```

#### 2. Timezone-Based Operations
```javascript
// Multi-market timezone management
const marketInfo = await getMarket('./config/markets.json');
const allTimezones = getAllTimeZones(marketInfo);
const targetTimezone = getTargetTimeZone(allTimezones, '09:00');
const marketUsers = await getTimeZoneUsers(
  getMarketsByTimeZone(targetTimezone, marketInfo)
);
```

#### 3. Dynamic Reward Generation
```javascript
// Statistical reward distribution
const rewardAmount = random_decimal_generator(
  maxReward,    // 10.0
  minReward,    // 1.0  
  meanReward,   // 5.0
  betaParam     // 2.0
);
console.log(`Generated reward: $${rewardAmount}`);
```

#### 4. Wallet Operations
```javascript
// Secure wallet transactions
const transactionId = await userWalletSync(userId, {
  activity_type: 6, // Incentive activity
  points: 5.0,
  note: 'Trip completion reward'
});
```

### Campaign Management Workflows

#### Info Tile Creation
```javascript
const campaignData = {
  name: 'Welcome Message',
  description: 'New user onboarding',
  title: 'Welcome to ConnectSmart!',
  body: 'Start earning rewards for your trips',
  timezone: 'America/Chicago',
  sendtime: '09:00:00'
};

const campaignId = await addToInfoTile(campaignData, userId, 'MTC');
```

#### Action Tile Configuration
```javascript
const actionCampaign = {
  name: 'Mode Change Challenge',
  description: 'Encourage transit usage',
  title: 'Try public transit today!',
  body: 'Earn extra points by taking the bus',
  timezone: 'America/Chicago',
  sendtime: '07:30:00',
  changeModeTransport: 2, // Transit mode
  points: 10,
  oid: originId,
  did: destinationId,
  departureTime: '08:00:00'
};

const actionCampaignId = await addToActionTile(actionCampaign, userId);
```

### Advanced Market Operations

```javascript
// Market polygon analysis for geographic targeting
const marketData = await getMarket('./markets.json');
const houstonMarket = getMarketPolygon('HCS', marketData);

if (houstonMarket.coordinates.length > 0) {
  console.log(`Houston market timezone: ${houstonMarket.timezone}`);
  console.log(`Random incentive enabled: ${houstonMarket.random_incnetive}`);
}
```

## Dependencies

### Core Framework Dependencies
- **knex**: SQL query builder for database operations across multiple schemas
- **moment-timezone**: Comprehensive timezone handling and date manipulation
- **@maas/core/log**: Centralized logging system for debugging and monitoring
- **@maas/core/mysql**: Database connection management and pooling

### External Service Dependencies
- **@app/src/services/wallet**: Points transaction system for reward processing
- **@app/src/services/queue**: Asynchronous task queue for notification delivery
- **@stdlib/random-base-gamma**: Advanced statistical random number generation

### Configuration Dependencies
- **Market JSON Files**: External configuration files defining market boundaries and rules
- **Database Schemas**: Multiple MySQL schemas (portal, hybrid) for data operations
- **Firebase Configuration**: Real-time database connection parameters

### Internal Model Dependencies
- **User Models**: Authentication and user profile management
- **Campaign Models**: Marketing campaign and notification systems
- **Transaction Models**: Financial and points transaction tracking

## Code Examples

### Comprehensive User Analysis System

```javascript
// Advanced user segmentation and analysis
async function analyzeUserBase() {
  const allUsers = await getUserCompoundData();
  
  const userSegments = {
    newUsers: allUsers.filter(u => u.user_days <= 7),
    activeUsers: allUsers.filter(u => u.trips > 5 && u.trip_to_now <= 7), 
    dormantUsers: allUsers.filter(u => u.trip_to_now > 30),
    powerUsers: allUsers.filter(u => u.trips > 50)
  };
  
  console.log('User Base Analysis:', {
    total: allUsers.length,
    newUsers: userSegments.newUsers.length,
    activeUsers: userSegments.activeUsers.length,
    dormantUsers: userSegments.dormantUsers.length,
    powerUsers: userSegments.powerUsers.length
  });
  
  return userSegments;
}
```

### Multi-Timezone Campaign Scheduler

```javascript
// Intelligent timezone-based campaign delivery
async function scheduleGlobalCampaign(campaignConfig, targetTime) {
  const marketData = await getMarket('./config/markets.json');
  const allTimezones = getAllTimeZones(marketData);
  
  for (const timezone of allTimezones) {
    const currentLocalTime = tz.tz(timezone).format('HH:mm');
    
    if (currentLocalTime === targetTime) {
      const markets = getMarketsByTimeZone(timezone, marketData);
      const targetUsers = await getTimeZoneUsers(markets);
      
      console.log(`Delivering campaign to ${targetUsers.length} users in ${timezone}`);
      
      for (const user of targetUsers) {
        await addToNotify({
          user_id: user.user_id,
          market: user.user_in_market,
          purpose: 'campaign',
          incentive_type: campaignConfig.type,
          notification_type: 1,
          msg_key: campaignConfig.key,
          msg_content: campaignConfig.message,
          timezone: timezone
        }, targetTime);
      }
    }
  }
}
```

### Advanced Random Reward System

```javascript
// Sophisticated reward distribution with statistical modeling
class DynamicRewardSystem {
  constructor() {
    this.rewardParams = {
      newUser: { max: 15, min: 5, mean: 10, beta: 2 },
      regularUser: { max: 10, min: 2, mean: 5, beta: 1.5 },
      powerUser: { max: 20, min: 8, mean: 12, beta: 3 }
    };
  }
  
  async generateReward(userId, userType = 'regularUser') {
    const params = this.rewardParams[userType];
    
    // Generate statistically distributed reward
    const baseReward = random_decimal_generator(
      params.max,
      params.min, 
      params.mean,
      params.beta
    );
    
    // Apply market-specific multipliers
    const marketUser = await getMarketUser(userId);
    const marketData = await getMarket('./config/markets.json');
    const marketProfile = getMarketPolygon(marketUser[0].user_in_market, marketData);
    
    const finalReward = marketProfile.random_incnetive ? 
      baseReward * 1.2 : baseReward;
    
    return Math.round(finalReward * 100) / 100; // Round to 2 decimal places
  }
  
  async distributeRewards(userList) {
    const results = [];
    
    for (const userId of userList) {
      const userStats = await getUserCompoundData();
      const userData = userStats.find(u => u.id === userId);
      
      const userType = this.classifyUser(userData);
      const reward = await this.generateReward(userId, userType);
      
      // Process wallet transaction
      const transactionId = await userWalletSync(userId, {
        activity_type: 6,
        points: reward,
        note: `Dynamic reward - ${userType}`
      });
      
      results.push({ userId, reward, userType, transactionId });
    }
    
    return results;
  }
  
  classifyUser(userData) {
    if (userData.user_days <= 7) return 'newUser';
    if (userData.trips > 50) return 'powerUser';
    return 'regularUser';
  }
}
```

### Campaign Performance Analytics

```javascript
// Comprehensive campaign tracking and analytics
async function analyzeCampaignPerformance(campaignId) {
  const campaignData = await knex('cm_campaign')
    .where('id', campaignId)
    .first();
  
  const campaignUsers = await knex('cm_campaign_user')
    .where('campaign_id', campaignId)
    .join('auth_user', 'auth_user.id', 'cm_campaign_user.user_id')
    .select('cm_campaign_user.*', 'auth_user.created_on as user_created');
  
  const deliveryStats = await knex('incentive_notify_queue')
    .where('msg_key', `campaign_${campaignId}`)
    .select(
      knex.raw('COUNT(*) as total_sent'),
      knex.raw('SUM(deliver) as delivered'),
      knex.raw('AVG(CASE WHEN deliver = 1 THEN 1 ELSE 0 END) as delivery_rate')
    )
    .first();
  
  const performance = {
    campaign: campaignData,
    targeting: {
      totalUsers: campaignUsers.length,
      newUsers: campaignUsers.filter(u => 
        moment().diff(moment(u.user_created), 'days') <= 7
      ).length,
      activeUsers: campaignUsers.filter(u => u.status === 1).length
    },
    delivery: deliveryStats,
    timezoneCoverage: [...new Set(campaignUsers.map(u => 
      moment.tz.guess(u.timezone)
    ))].length
  };
  
  return performance;
}
```

This utility service provides the essential infrastructure for the ConnectSmart incentive system, enabling sophisticated user management, dynamic reward distribution, and comprehensive campaign orchestration across multiple markets and timezones.