# TSP API Tier Service Documentation

## 🔍 Quick Summary (TL;DR)
The Tier service manages user loyalty tier benefits including raffle magnification, referral bonuses, and Uber ride benefits, with monthly tracking of benefit usage and integration with external incentive systems for tier level determination.

**Keywords:** loyalty-tiers | user-benefits | raffle-magnification | referral-bonuses | uber-benefits | monthly-tracking | tier-levels | incentive-integration

**Primary use cases:** Determining user tier levels and points, calculating tier-based benefit multipliers, tracking monthly Uber benefit usage, providing tier-specific rewards

**Compatibility:** Node.js >= 16.0.0, external incentive API integration, MySQL database with benefit tracking, moment.js for timezone handling

## ❓ Common Questions Quick Index
- **Q: What tier levels exist?** → Green (base), Bronze, Silver, Gold with increasing benefits
- **Q: How are tier benefits calculated?** → Multipliers for raffles (1x to 5x) and referrals (1x to 1.3x)
- **Q: What Uber benefits are provided?** → Monthly ride credits: Green $0, Bronze $4, Silver $6, Gold $8
- **Q: How is tier level determined?** → External incentive API call based on user tier points
- **Q: Are benefits monthly?** → Uber benefits reset monthly, other benefits are ongoing
- **Q: What happens if API fails?** → Defaults to green tier with base benefits

## 📋 Functionality Overview

**Non-technical explanation:** 
Think of this as a **loyalty rewards system** that gives users better benefits as they become more active. Like airline frequent flyer programs, users earn points and move up through Green, Bronze, Silver, and Gold levels, getting better rewards like extra raffle entries, bonus referral rewards, and monthly Uber ride credits.

**Technical explanation:** 
A comprehensive tier management system that integrates with external incentive APIs to determine user tier levels, applies tier-specific benefit multipliers for various reward activities, tracks monthly benefit consumption with timezone awareness, and provides standardized benefit rules for consistent reward calculation across the platform.

**Business value explanation:**
Drives user engagement through progressive reward tiers, encourages long-term platform usage, provides clear value proposition for active users, supports partnership benefits like Uber integration, and enables data-driven loyalty program optimization through benefit tracking.

## 🔧 Technical Specifications

- **File:** `allrepo/connectsmart/tsp-api/src/services/tier.js`
- **Language:** JavaScript (ES2020)
- **Framework:** Node.js with superagent HTTP client and moment.js
- **Type:** User Loyalty Tier Management Service
- **File Size:** ~4.1 KB
- **Complexity Score:** ⭐⭐⭐ (Medium-High - External API integration with benefit calculations)

**Dependencies:**
- `superagent`: HTTP client for external API calls (**Critical**)
- `moment-timezone`: Timezone-aware date calculations (**High**)
- `@app/src/models/UberBenefitTransaction`: Benefit usage tracking (**Critical**)
- `config`: External incentive API configuration (**Critical**)

## 📝 Detailed Code Analysis

### Tier Benefits Rule Structure

### Benefits Configuration
```javascript
const rule = {
  green: {
    raffle: { 
      magnification: 1,
      toast: {
        title: 'Congratulations!',
        message: 'You\'re entered into the giveaway. Good luck!',
      },
    },
    referral: {
      magnification: 1,
      toast: {
        title: 'Congratulations!',
        message: 'We've added {1} {2} to your Wallet!',
      }
    },
    uber: {
      benefit: 0,
    },
  },
  bronze: {
    raffle: {
      magnification: 2,
      toast: {
        title: 'Congratulations!',
        message: 'Bronze member! You\'ve earned 2x raffle tickets from contests and challenges!',
      },
    },
    referral: {
      magnification: 1.15,
      toast: {
        title: 'Congratulations!',
        message: 'Bronze member! You\'ve earned a 15% bonus on your referral incentive!',
      }
    },
    uber: {
      benefit: 4,
    },
  },
  // ... silver and gold tiers with progressive benefits
};
```

**Rule Structure Features:**
- **Progressive Benefits:** Increasing multipliers and monetary benefits across tiers
- **Toast Messages:** Tier-specific user notification templates
- **Multiple Benefit Types:** Raffle tickets, referral bonuses, and Uber credits
- **Standardized Format:** Consistent structure across all tier levels

### Uber Benefit Tracking

### getUserUberBenefit Function
**Purpose:** Calculates remaining Uber benefits for current month based on usage

```javascript
async function getUserUberBenefit(userId, level = 'green', zone = 'America/Chicago') {
  logger.info(`[getUserUberBenefit] userId: ${userId}`);
  let result = 0;
  
  // Calculate month start in user timezone
  const monthStart = moment().tz(zone).startOf('month').utc().format('YYYY-MM-DD HH:mm:ss');
  
  // Query total benefits used this month
  const transaction = await UberBenefitTransaction.query()
    .where('user_id', userId)
    .where('created_on', '>=', monthStart)
    .sum('benefit_amount as total_benefit')
    .first();
    
  if (!transaction || Number(transaction.total_benefit) === 0) {
    logger.info(`[getUserUberBenefit] no benefit transaction been used this month`);
    result = rule[level].uber.benefit;
  }
  
  return result;
}
```

**Benefit Calculation Features:**
- **Monthly Reset:** Benefits calculated from start of current month
- **Timezone Awareness:** Uses user's timezone for accurate month boundaries
- **Usage Tracking:** Sums all benefit transactions for the month
- **Remaining Calculation:** Returns full benefit if none used, zero if used
- **Database Aggregation:** Efficient sum query for performance

### External Tier Integration

### getUserTier Function
**Purpose:** Retrieves user tier information from external incentive system

```javascript
async function getUserTier(userId, zone = 'America/Chicago') {
  logger.info(`[getUserTier] userId: ${userId}`);
  let result = {
    points: 0,
    level: 'green',
    uber_benefit: 0,
  };
  
  try {
    const res = await superagent.get(`${url}/tier/${userId}`);
    if (res.body && res.body.data) {
      logger.info(`[getUserTier] data: ${JSON.stringify(res.body.data)}`);
      result.points = res.body.data.tier_points;
      result.level = res.body.data.tier_level;
      result.uber_benefit = await getUserUberBenefit(userId, result.level, zone);
    } else {
      logger.error(`[getUserTier] error: tier data not found`);
    }
  } catch(e) {
    logger.error(`[getUserTier] error: ${e.message}`);
    logger.info(`[getUserTier] stack: ${e.stack}`);
  }
  
  return result;
}
```

**Integration Features:**
- **External API Call:** Retrieves tier data from incentive service
- **Fallback Handling:** Returns default green tier on API failure
- **Data Validation:** Checks for valid response structure
- **Benefit Integration:** Combines tier level with Uber benefit calculation
- **Error Logging:** Comprehensive error tracking for debugging

### Benefit Rules Access

### getUserTierBenefits Function
**Purpose:** Retrieves complete benefit rules for specified tier level

```javascript
async function getUserTierBenefits(tierLevel) {
  logger.info(`[getUserTierBenefits] tierLevel: ${tierLevel}`);
  logger.info(`[getUserTierBenefits] rule: ${JSON.stringify(rule[tierLevel])}`);
  return rule[tierLevel] ?? rule.green;
}
```
- **Rule Lookup:** Direct access to tier-specific benefit configuration
- **Fallback Protection:** Defaults to green tier for invalid tier levels
- **Complete Benefits:** Returns all benefit types (raffle, referral, uber)
- **Logging:** Detailed logging for benefit rule access

## 🚀 Usage Methods

### Basic Tier Management
```javascript
const tierService = require('@app/src/services/tier');

// Get user tier information
const userTier = await tierService.getUserTier(12345, 'America/Chicago');
console.log('User tier:', userTier);
// { points: 150, level: 'bronze', uber_benefit: 4 }

// Get tier benefits configuration
const benefits = await tierService.getUserTierBenefits('bronze');
console.log('Bronze benefits:', benefits);
// { raffle: { magnification: 2, ... }, referral: { magnification: 1.15, ... }, uber: { benefit: 4 } }
```

### Advanced Tier Management System
```javascript
class TierManagementSystem {
  constructor() {
    this.tierService = require('@app/src/services/tier');
    this.tierCache = new Map();
    this.cacheTimeout = 300000; // 5 minutes
  }

  async getUserTierWithCache(userId, zone = 'America/Chicago', forceRefresh = false) {
    try {
      const cacheKey = `tier_${userId}`;
      
      // Check cache first
      if (!forceRefresh && this.tierCache.has(cacheKey)) {
        const cached = this.tierCache.get(cacheKey);
        if (Date.now() - cached.timestamp < this.cacheTimeout) {
          console.log(`Using cached tier data for user ${userId}`);
          return {
            ...cached.data,
            fromCache: true
          };
        }
      }

      // Get fresh tier data
      const tierData = await this.tierService.getUserTier(userId, zone);
      
      // Cache the result
      this.tierCache.set(cacheKey, {
        data: tierData,
        timestamp: Date.now()
      });

      return {
        ...tierData,
        fromCache: false
      };
    } catch (error) {
      console.error('Error getting user tier:', error);
      
      // Return cached data if available, otherwise default
      const cacheKey = `tier_${userId}`;
      if (this.tierCache.has(cacheKey)) {
        const cached = this.tierCache.get(cacheKey);
        return {
          ...cached.data,
          fromCache: true,
          error: 'Using cached data due to API error'
        };
      }
      
      return {
        points: 0,
        level: 'green',
        uber_benefit: 0,
        fromCache: false,
        error: error.message
      };
    }
  }

  async calculateTierBenefits(userId, activity, baseAmount, zone = 'America/Chicago') {
    try {
      const tierData = await this.getUserTierWithCache(userId, zone);
      const benefits = await this.tierService.getUserTierBenefits(tierData.level);
      
      let finalAmount = baseAmount;
      let multiplier = 1;
      let benefitType = '';
      let message = '';

      switch (activity) {
        case 'raffle':
          multiplier = benefits.raffle.magnification;
          finalAmount = baseAmount * multiplier;
          benefitType = 'raffle_tickets';
          message = benefits.raffle.toast.message;
          break;
          
        case 'referral':
          multiplier = benefits.referral.magnification;
          finalAmount = baseAmount * multiplier;
          benefitType = 'referral_bonus';
          message = benefits.referral.toast.message;
          break;
          
        case 'uber_benefit':
          finalAmount = tierData.uber_benefit;
          multiplier = finalAmount > 0 ? 1 : 0;
          benefitType = 'uber_credit';
          message = `You have $${finalAmount} in Uber benefits available this month`;
          break;
          
        default:
          throw new Error(`Unknown activity type: ${activity}`);
      }

      return {
        success: true,
        tierLevel: tierData.level,
        tierPoints: tierData.points,
        baseAmount,
        finalAmount,
        multiplier,
        benefitType,
        message,
        toast: {
          title: benefits[activity]?.toast?.title || 'Congratulations!',
          message
        }
      };
    } catch (error) {
      console.error('Error calculating tier benefits:', error);
      return {
        success: false,
        tierLevel: 'green',
        tierPoints: 0,
        baseAmount,
        finalAmount: baseAmount,
        multiplier: 1,
        benefitType: activity,
        error: error.message
      };
    }
  }

  async batchGetUserTiers(userIds, zone = 'America/Chicago') {
    const results = [];
    
    // Process users in parallel
    const promises = userIds.map(async (userId) => {
      try {
        const tierData = await this.getUserTierWithCache(userId, zone);
        return {
          userId,
          success: true,
          ...tierData
        };
      } catch (error) {
        return {
          userId,
          success: false,
          points: 0,
          level: 'green',
          uber_benefit: 0,
          error: error.message
        };
      }
    });

    const tierResults = await Promise.all(promises);
    
    return {
      totalUsers: userIds.length,
      successful: tierResults.filter(r => r.success).length,
      failed: tierResults.filter(r => !r.success).length,
      results: tierResults
    };
  }

  async getTierDistribution(userIds, zone = 'America/Chicago') {
    try {
      const batchResult = await this.batchGetUserTiers(userIds, zone);
      
      const distribution = {
        green: 0,
        bronze: 0,
        silver: 0,
        gold: 0
      };

      let totalPoints = 0;
      let totalUberBenefits = 0;

      batchResult.results.forEach(result => {
        if (result.success) {
          distribution[result.level]++;
          totalPoints += result.points;
          totalUberBenefits += result.uber_benefit;
        }
      });

      const totalUsers = batchResult.successful;

      return {
        totalUsers,
        distribution,
        percentages: {
          green: totalUsers > 0 ? (distribution.green / totalUsers * 100).toFixed(2) : '0.00',
          bronze: totalUsers > 0 ? (distribution.bronze / totalUsers * 100).toFixed(2) : '0.00',
          silver: totalUsers > 0 ? (distribution.silver / totalUsers * 100).toFixed(2) : '0.00',
          gold: totalUsers > 0 ? (distribution.gold / totalUsers * 100).toFixed(2) : '0.00'
        },
        averagePoints: totalUsers > 0 ? (totalPoints / totalUsers).toFixed(2) : '0.00',
        totalUberBenefits,
        averageUberBenefit: totalUsers > 0 ? (totalUberBenefits / totalUsers).toFixed(2) : '0.00'
      };
    } catch (error) {
      console.error('Error getting tier distribution:', error);
      return {
        totalUsers: 0,
        distribution: { green: 0, bronze: 0, silver: 0, gold: 0 },
        percentages: { green: '0.00', bronze: '0.00', silver: '0.00', gold: '0.00' },
        averagePoints: '0.00',
        totalUberBenefits: 0,
        averageUberBenefit: '0.00',
        error: error.message
      };
    }
  }

  async simulateTierProgression(currentPoints, targetLevel) {
    const tierThresholds = {
      green: 0,
      bronze: 100,
      silver: 250,
      gold: 500
    };

    const targetPoints = tierThresholds[targetLevel];
    if (targetPoints === undefined) {
      throw new Error(`Invalid target level: ${targetLevel}`);
    }

    if (currentPoints >= targetPoints) {
      return {
        alreadyQualified: true,
        currentLevel: this.getLevel(currentPoints),
        targetLevel,
        pointsNeeded: 0
      };
    }

    const pointsNeeded = targetPoints - currentPoints;
    const currentLevel = this.getLevel(currentPoints);
    
    return {
      alreadyQualified: false,
      currentLevel,
      targetLevel,
      currentPoints,
      targetPoints,
      pointsNeeded,
      benefitUpgrade: this.calculateBenefitUpgrade(currentLevel, targetLevel)
    };
  }

  getLevel(points) {
    if (points >= 500) return 'gold';
    if (points >= 250) return 'silver';
    if (points >= 100) return 'bronze';
    return 'green';
  }

  calculateBenefitUpgrade(currentLevel, targetLevel) {
    const currentBenefits = this.tierService.benefitsRule[currentLevel];
    const targetBenefits = this.tierService.benefitsRule[targetLevel];

    return {
      raffle: {
        current: currentBenefits.raffle.magnification,
        target: targetBenefits.raffle.magnification,
        improvement: `${currentBenefits.raffle.magnification}x → ${targetBenefits.raffle.magnification}x`
      },
      referral: {
        current: currentBenefits.referral.magnification,
        target: targetBenefits.referral.magnification,
        improvement: `${(currentBenefits.referral.magnification * 100).toFixed(0)}% → ${(targetBenefits.referral.magnification * 100).toFixed(0)}%`
      },
      uber: {
        current: currentBenefits.uber.benefit,
        target: targetBenefits.uber.benefit,
        improvement: `$${currentBenefits.uber.benefit} → $${targetBenefits.uber.benefit}`
      }
    };
  }

  clearExpiredCache() {
    const now = Date.now();
    let cleared = 0;

    this.tierCache.forEach((entry, key) => {
      if (now - entry.timestamp >= this.cacheTimeout) {
        this.tierCache.delete(key);
        cleared++;
      }
    });

    return {
      cleared,
      remaining: this.tierCache.size
    };
  }

  getCacheStatistics() {
    return {
      cacheSize: this.tierCache.size,
      cacheTimeout: this.cacheTimeout / 1000, // in seconds
      supportedTiers: Object.keys(this.tierService.benefitsRule)
    };
  }
}

// Usage
const tierManager = new TierManagementSystem();

// Get user tier with caching
const tierData = await tierManager.getUserTierWithCache(12345);
console.log('User tier data:', tierData);

// Calculate tier benefits for activity
const benefits = await tierManager.calculateTierBenefits(12345, 'raffle', 1);
console.log('Raffle benefits:', benefits);

// Get tier distribution for user group
const distribution = await tierManager.getTierDistribution([12345, 67890, 11111]);
console.log('Tier distribution:', distribution);

// Simulate tier progression
const progression = await tierManager.simulateTierProgression(150, 'silver');
console.log('Tier progression:', progression);
```

### Benefit Application System
```javascript
class BenefitApplicationSystem {
  constructor() {
    this.tierService = require('@app/src/services/tier');
    this.benefitHistory = new Map();
  }

  async applyRaffleBenefit(userId, baseTickets, zone = 'America/Chicago') {
    try {
      const tierData = await this.tierService.getUserTier(userId, zone);
      const benefits = await this.tierService.getUserTierBenefits(tierData.level);
      
      const finalTickets = Math.floor(baseTickets * benefits.raffle.magnification);
      
      this.recordBenefitUsage(userId, 'raffle', {
        tierLevel: tierData.level,
        baseAmount: baseTickets,
        finalAmount: finalTickets,
        multiplier: benefits.raffle.magnification
      });

      return {
        success: true,
        tierLevel: tierData.level,
        baseTickets,
        finalTickets,
        multiplier: benefits.raffle.magnification,
        bonusTickets: finalTickets - baseTickets,
        message: benefits.raffle.toast.message
      };
    } catch (error) {
      console.error('Error applying raffle benefit:', error);
      return {
        success: false,
        tierLevel: 'green',
        baseTickets,
        finalTickets: baseTickets,
        multiplier: 1,
        bonusTickets: 0,
        error: error.message
      };
    }
  }

  async applyReferralBenefit(userId, baseReward, zone = 'America/Chicago') {
    try {
      const tierData = await this.tierService.getUserTier(userId, zone);
      const benefits = await this.tierService.getUserTierBenefits(tierData.level);
      
      const finalReward = Math.round(baseReward * benefits.referral.magnification * 100) / 100;
      
      this.recordBenefitUsage(userId, 'referral', {
        tierLevel: tierData.level,
        baseAmount: baseReward,
        finalAmount: finalReward,
        multiplier: benefits.referral.magnification
      });

      return {
        success: true,
        tierLevel: tierData.level,
        baseReward,
        finalReward,
        multiplier: benefits.referral.magnification,
        bonusReward: Math.round((finalReward - baseReward) * 100) / 100,
        message: benefits.referral.toast.message.replace('{1}', finalReward).replace('{2}', 'coins')
      };
    } catch (error) {
      console.error('Error applying referral benefit:', error);
      return {
        success: false,
        tierLevel: 'green',
        baseReward,
        finalReward: baseReward,
        multiplier: 1,
        bonusReward: 0,
        error: error.message
      };
    }
  }

  recordBenefitUsage(userId, benefitType, details) {
    const userHistory = this.benefitHistory.get(userId) || [];
    
    const record = {
      benefitType,
      timestamp: new Date(),
      ...details
    };

    userHistory.push(record);
    this.benefitHistory.set(userId, userHistory.slice(-50)); // Keep last 50 records
  }

  getUserBenefitHistory(userId) {
    const history = this.benefitHistory.get(userId) || [];
    
    const stats = {
      totalBenefitsUsed: history.length,
      benefitTypes: {},
      totalBonusValue: 0,
      averageMultiplier: 0,
      recentBenefits: history.slice(-10)
    };

    history.forEach(record => {
      const type = record.benefitType;
      if (!stats.benefitTypes[type]) {
        stats.benefitTypes[type] = { count: 0, totalBonus: 0 };
      }
      
      stats.benefitTypes[type].count++;
      stats.benefitTypes[type].totalBonus += (record.finalAmount - record.baseAmount);
      stats.totalBonusValue += (record.finalAmount - record.baseAmount);
    });

    if (history.length > 0) {
      stats.averageMultiplier = history.reduce((sum, record) => sum + record.multiplier, 0) / history.length;
    }

    return stats;
  }

  getBenefitSystemStats() {
    let totalUsers = this.benefitHistory.size;
    let totalBenefits = 0;
    const tierDistribution = { green: 0, bronze: 0, silver: 0, gold: 0 };

    this.benefitHistory.forEach(history => {
      totalBenefits += history.length;
      
      // Get most recent tier level for user
      if (history.length > 0) {
        const recentTier = history[history.length - 1].tierLevel;
        tierDistribution[recentTier]++;
      }
    });

    return {
      totalUsers,
      totalBenefits,
      averageBenefitsPerUser: totalUsers > 0 ? (totalBenefits / totalUsers).toFixed(2) : '0.00',
      tierDistribution
    };
  }
}

// Usage
const benefitSystem = new BenefitApplicationSystem();

// Apply raffle benefit
const raffleResult = await benefitSystem.applyRaffleBenefit(12345, 3);
console.log('Raffle benefit result:', raffleResult);

// Apply referral benefit
const referralResult = await benefitSystem.applyReferralBenefit(12345, 10.00);
console.log('Referral benefit result:', referralResult);

// Get user benefit history
const history = benefitSystem.getUserBenefitHistory(12345);
console.log('User benefit history:', history);
```

## 📊 Output Examples

### User Tier Response
```javascript
{
  points: 275,
  level: "silver",
  uber_benefit: 6
}
```

### Tier Benefits Configuration
```javascript
{
  raffle: {
    magnification: 3,
    toast: {
      title: "Congratulations!",
      message: "Silver member! You've earned 3x raffle tickets from contests and challenges!"
    }
  },
  referral: {
    magnification: 1.2,
    toast: {
      title: "Congratulations!",
      message: "Silver member! You've earned a 20% bonus on your referral incentive!"
    }
  },
  uber: {
    benefit: 6
  }
}
```

### Benefit Calculation Result
```javascript
{
  success: true,
  tierLevel: "bronze",
  tierPoints: 150,
  baseAmount: 1,
  finalAmount: 2,
  multiplier: 2,
  benefitType: "raffle_tickets",
  message: "Bronze member! You've earned 2x raffle tickets from contests and challenges!",
  toast: {
    title: "Congratulations!",
    message: "Bronze member! You've earned 2x raffle tickets from contests and challenges!"
  }
}
```

### Tier Distribution Analysis
```javascript
{
  totalUsers: 1000,
  distribution: {
    green: 650,
    bronze: 200,
    silver: 100,
    gold: 50
  },
  percentages: {
    green: "65.00",
    bronze: "20.00", 
    silver: "10.00",
    gold: "5.00"
  },
  averagePoints: "125.50",
  totalUberBenefits: 1400,
  averageUberBenefit: "1.40"
}
```

### Tier Progression Simulation
```javascript
{
  alreadyQualified: false,
  currentLevel: "bronze",
  targetLevel: "silver",
  currentPoints: 150,
  targetPoints: 250,
  pointsNeeded: 100,
  benefitUpgrade: {
    raffle: {
      current: 2,
      target: 3,
      improvement: "2x → 3x"
    },
    referral: {
      current: 1.15,
      target: 1.2,
      improvement: "115% → 120%"
    },
    uber: {
      current: 4,
      target: 6,
      improvement: "$4 → $6"
    }
  }
}
```

## ⚠️ Important Notes

### External API Integration
- **Incentive Service Dependency:** Requires external incentive API for tier determination
- **Fallback Handling:** Defaults to green tier when API is unavailable
- **Error Resilience:** Comprehensive error handling prevents service disruption
- **Configuration Driven:** API endpoints configured through environment settings

### Monthly Benefit Tracking
- **Timezone Awareness:** Uses user timezone for accurate month boundary calculations
- **Usage Tracking:** Comprehensive tracking of Uber benefit consumption
- **Monthly Reset:** Benefits automatically reset at start of each month
- **Database Queries:** Efficient aggregation queries for benefit calculations

### Tier Benefit Structure
- **Progressive Rewards:** Clear benefit increases across tier levels
- **Multiple Benefit Types:** Supports raffle, referral, and Uber benefits
- **Standardized Messages:** Consistent toast notification templates
- **Multiplier Logic:** Mathematical multipliers for various reward types

### Performance and Caching
- **API Rate Limiting:** Consider caching tier data to reduce external API calls
- **Database Optimization:** Efficient queries for monthly benefit calculations
- **Error Recovery:** Graceful degradation when external services fail
- **Scalability:** Designed for high-volume tier checking operations

## 🔗 Related File Links

- **Uber Benefit Models:** `allrepo/connectsmart/tsp-api/src/models/UberBenefitTransaction.js`
- **Incentive Services:** External incentive API integration
- **Referral Services:** Services that use tier-based referral multipliers
- **Raffle Services:** Services that apply tier-based raffle magnification

---
*This service provides comprehensive user loyalty tier management with progressive benefits and external system integration for the TSP platform.*