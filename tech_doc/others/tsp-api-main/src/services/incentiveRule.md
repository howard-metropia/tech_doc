# TSP API Incentive Rule Service Documentation

## 🔍 Quick Summary (TL;DR)
The Incentive Rule service manages date-based incentive rule updates for the HCS market, providing versioned configuration changes for reward calculations, travel mode parameters, and campaign settings.

**Keywords:** incentive-rules | configuration-management | rule-versioning | market-configuration | reward-parameters | travel-mode-settings | campaign-management | database-migration

**Primary use cases:** Updating incentive parameters for campaigns, managing travel mode reward configurations, applying time-based rule changes, maintaining reward system evolution

**Compatibility:** Node.js >= 16.0.0, MongoDB integration, versioned rule management system

## ❓ Common Questions Quick Index
- **Q: What market do these rules apply to?** → HCS (Houston Community Services) market exclusively
- **Q: How are rule versions managed?** → Date-based function names (rule_YYYYMMDD) for chronological tracking
- **Q: Can rules be rolled back?** → No automatic rollback - each function represents a forward migration
- **Q: What parameters control rewards?** → D (budget), L (limit), W (welcome bonus), plus per-mode mean/min/max/beta values
- **Q: How often are rules updated?** → As needed for campaigns - historically every few weeks/months
- **Q: Are rules applied retroactively?** → No, rules apply from their effective start date forward

## 📋 Functionality Overview

**Non-technical explanation:** 
Think of this as a **rules update system** for the rewards program. Just like how a store might change its loyalty program benefits or offer special promotions, this service updates the rules that determine how many points people get for different types of trips. Each update is dated and carefully tracks what changed when.

**Technical explanation:** 
A versioned configuration management service that provides time-based rule updates for the incentive system. Each function represents a specific rule version with date-based naming, handling both creation of new rules and updates to existing ones. Manages complex nested configurations for travel modes, budget limits, and statistical parameters.

**Business value explanation:**
Essential for dynamic campaign management and A/B testing of incentive programs. Enables data-driven optimization of reward structures, supports marketing campaigns with adjusted incentives, and provides audit trail for business performance analysis. Critical for maintaining competitive and cost-effective incentive programs.

## 🔧 Technical Specifications

- **File:** `allrepo/connectsmart/tsp-api/src/services/incentiveRule.js`
- **Language:** JavaScript (ES2020)
- **Framework:** MongoDB with Mongoose ODM
- **Type:** Configuration Management Service
- **File Size:** ~20.3 KB
- **Complexity Score:** ⭐⭐ (Low-Medium - Repetitive configuration functions)

**Dependencies:**
- `@maas/core/log`: Logging infrastructure (**High**)
- `@app/src/models/TripIncentiveRules`: MongoDB model for rule storage (**Critical**)

## 📝 Detailed Code Analysis

### Rule Structure Schema

**Standard Parameters:**
- `market`: String - Market identifier ("HCS")
- `D`: Number - Daily budget limit in cents
- `h`: Number - Time window hours for rule application
- `d1/d2`: Numbers - Distance thresholds (meters)
- `L`: Number - Maximum trips per user per week
- `W`: Number - Welcome bonus for first trip ($0.99)
- `MC`: Boolean - Market campaign flag
- `start/end`: Numbers - Unix timestamps for rule validity period
- `created_on/modified_on`: Numbers - Audit timestamps

**Travel Mode Configuration:**
Each mode contains:
- `distance`: Number - Minimum distance multiplier
- `mean`: Number - Target mean reward value
- `min`: Number - Minimum reward value
- `max`: Number - Maximum reward value  
- `beta`: Number - Gamma distribution scale parameter

### Rule Evolution Timeline

**rule_20240819 Function:**
- Initial comprehensive rule set
- L: 20 trips per week limit
- MC: false (no special campaign)
- Ridehail: High rewards (mean: 15, max: 5)

**rule_20240823 Function:**
- L: Reduced to 5 trips per week
- MC: true (campaign activated)
- Ridehail: Disabled (mean: 0.01, max: 0)

**rule_20240912 Function:**
- L: Increased back to 20 trips
- MC: false (campaign ended)  
- Ridehail: Re-enabled (mean: 15, max: 5)

**rule_20240920 Function:**
- L: Reduced to 5 trips again
- MC: true (new campaign)
- Ridehail: Disabled again

**rule_20241002 Function:**
- D: Increased budget from 300 to 50,000 cents
- Enhanced driving/duo rewards (mean: 0.8, max: 1.0)
- Reduced biking rewards (mean: 0.2, max: 0.4)
- MC: false, L: 5

**rule_20241231 Function:**
- L: Increased to 30 trips per week
- Ridehail: Major increase (mean: 50, max: 20)

**rule_20250101 Function:**
- L: Back to 5 trips per week
- Ridehail: Disabled (mean: 0.01, max: 0)

### Implementation Pattern

```javascript
async function rule_YYYYMMDD() {
  const rule = await tripIncentiveRules.findOne({ market: 'HCS' });
  if (!rule) {
    // Create new rule with full configuration
    await tripIncentiveRules.create({ /* complete rule object */ });
  } else {
    // Update specific fields
    rule.set('L', newValue);
    rule.set('MC', newValue);
    rule.markModified('modes');
    await rule.save();
  }
}
```

## 🚀 Usage Methods

### Rule Application Service
```javascript
const incentiveRules = require('@app/src/services/incentiveRule');

class IncentiveRuleManager {
  constructor() {
    this.availableRules = {
      '2024-08-19': incentiveRules.rule_20240819,
      '2024-08-23': incentiveRules.rule_20240823,
      '2024-09-12': incentiveRules.rule_20240912,
      '2024-09-20': incentiveRules.rule_20240920,
      '2024-10-02': incentiveRules.rule_20241002,
      '2024-12-31': incentiveRules.rule_20241231,
      '2025-01-01': incentiveRules.rule_20250101
    };
  }

  async applyRule(ruleDate) {
    try {
      const ruleFunction = this.availableRules[ruleDate];
      
      if (!ruleFunction) {
        throw new Error(`Rule for date ${ruleDate} not found`);
      }

      console.log(`Applying incentive rule for ${ruleDate}...`);
      await ruleFunction();
      
      console.log(`Rule ${ruleDate} applied successfully`);
      return {
        success: true,
        ruleDate,
        appliedAt: new Date().toISOString()
      };
    } catch (error) {
      console.error(`Failed to apply rule ${ruleDate}:`, error);
      throw error;
    }
  }

  async applyLatestRule() {
    const sortedDates = Object.keys(this.availableRules).sort();
    const latestRule = sortedDates[sortedDates.length - 1];
    
    return await this.applyRule(latestRule);
  }

  async applyRulesInSequence() {
    const sortedDates = Object.keys(this.availableRules).sort();
    const results = [];
    
    for (const ruleDate of sortedDates) {
      try {
        const result = await this.applyRule(ruleDate);
        results.push(result);
        
        // Add delay between rule applications
        await new Promise(resolve => setTimeout(resolve, 1000));
      } catch (error) {
        results.push({
          success: false,
          ruleDate,
          error: error.message
        });
      }
    }
    
    return results;
  }

  listAvailableRules() {
    return Object.keys(this.availableRules).map(date => ({
      date,
      timestamp: new Date(date).getTime(),
      description: this.getRuleDescription(date)
    }));
  }

  getRuleDescription(ruleDate) {
    const descriptions = {
      '2024-08-19': 'Initial comprehensive rule set with high ridehail rewards',
      '2024-08-23': 'Campaign activation with reduced limits and disabled ridehail',
      '2024-09-12': 'Campaign end - restored limits and ridehail rewards',
      '2024-09-20': 'New campaign with reduced limits and disabled ridehail',
      '2024-10-02': 'Major budget increase with enhanced driving/duo rewards',
      '2024-12-31': 'Holiday campaign with increased limits and high ridehail rewards',
      '2025-01-01': 'New year reset with standard limits and disabled ridehail'
    };
    
    return descriptions[ruleDate] || 'Standard rule update';
  }
}
```

### Rule Comparison and Analysis
```javascript
class IncentiveRuleAnalyzer {
  constructor() {
    this.tripIncentiveRules = require('@app/src/models/TripIncentiveRules');
  }

  async getCurrentRule() {
    return await this.tripIncentiveRules.findOne({ market: 'HCS' });
  }

  async analyzeRuleChanges(fromDate, toDate) {
    // This would require storing historical snapshots
    // For now, we'll analyze the differences between rule functions
    
    const changes = {
      budgetChanges: [],
      limitChanges: [],
      campaignChanges: [],
      modeChanges: []
    };

    // Example analysis of known changes
    if (fromDate === '2024-10-02' && toDate === '2024-12-31') {
      changes.budgetChanges.push({
        field: 'D',
        from: 50000,
        to: 50000,
        change: 'No change'
      });
      
      changes.limitChanges.push({
        field: 'L',
        from: 5,
        to: 30,
        change: '+500% increase in weekly trip limit'
      });
      
      changes.modeChanges.push({
        mode: 'ridehail',
        field: 'mean',
        from: 0.01,
        to: 50,
        change: '+499900% increase in ridehail rewards'
      });
    }

    return changes;
  }

  async predictRewardImpact(ruleChanges, historicalData) {
    // Simplified impact prediction
    const predictions = {
      budgetImpact: 0,
      userEngagement: 0,
      modeShift: {}
    };

    // Example prediction logic
    if (ruleChanges.limitChanges.some(c => c.change.includes('increase'))) {
      predictions.userEngagement = 25; // 25% increase predicted
    }

    if (ruleChanges.modeChanges.some(c => c.mode === 'ridehail' && c.change.includes('increase'))) {
      predictions.modeShift.ridehail = 40; // 40% increase in ridehail usage
      predictions.budgetImpact = 150; // 150% increase in budget usage
    }

    return predictions;
  }

  generateRuleReport() {
    const ruleHistory = [
      {
        date: '2024-08-19',
        changes: ['Initial rule set', 'L: 20', 'MC: false', 'Ridehail enabled'],
        purpose: 'Baseline configuration'
      },
      {
        date: '2024-08-23', 
        changes: ['L: 20→5', 'MC: false→true', 'Ridehail disabled'],
        purpose: 'Cost control campaign'
      },
      {
        date: '2024-09-12',
        changes: ['L: 5→20', 'MC: true→false', 'Ridehail re-enabled'],
        purpose: 'Campaign completion'
      },
      {
        date: '2024-09-20',
        changes: ['L: 20→5', 'MC: false→true', 'Ridehail disabled'],
        purpose: 'New cost control period'
      },
      {
        date: '2024-10-02',
        changes: ['D: 300→50000', 'Enhanced driving/duo rewards', 'Reduced biking rewards'],
        purpose: 'Major budget increase and mode optimization'
      },
      {
        date: '2024-12-31',
        changes: ['L: 5→30', 'Ridehail: major increase (mean: 50)'],
        purpose: 'Holiday promotion campaign'
      },
      {
        date: '2025-01-01',
        changes: ['L: 30→5', 'Ridehail disabled'],
        purpose: 'Post-holiday normalization'
      }
    ];

    return {
      totalRuleUpdates: ruleHistory.length,
      ruleHistory,
      patterns: {
        campaignCycles: 3,
        ridehailToggling: 4,
        limitAdjustments: 6,
        budgetIncrease: 1
      },
      insights: [
        'Ridehail rewards are frequently toggled for cost control',
        'Weekly limits vary between 5-30 trips based on campaign goals',
        'Major budget increase in October 2024 enabled enhanced rewards',
        'Campaign flag (MC) correlates with restrictive reward settings'
      ]
    };
  }
}
```

### Rule Deployment Pipeline
```javascript
class IncentiveRuleDeployment {
  constructor() {
    this.ruleManager = new IncentiveRuleManager();
    this.analyzer = new IncentiveRuleAnalyzer();
  }

  async deployRule(ruleDate, options = {}) {
    const { dryRun = false, backup = true } = options;
    
    try {
      // Step 1: Backup current rule
      let currentRule = null;
      if (backup) {
        currentRule = await this.analyzer.getCurrentRule();
        console.log('Current rule backed up');
      }

      // Step 2: Dry run validation
      if (dryRun) {
        console.log(`DRY RUN: Would apply rule ${ruleDate}`);
        return {
          success: true,
          dryRun: true,
          ruleDate,
          currentRule: currentRule ? currentRule.toObject() : null
        };
      }

      // Step 3: Apply new rule
      const result = await this.ruleManager.applyRule(ruleDate);

      // Step 4: Verify deployment
      const newRule = await this.analyzer.getCurrentRule();
      const verification = await this.verifyRuleDeployment(newRule, ruleDate);

      if (!verification.valid) {
        throw new Error(`Rule verification failed: ${verification.errors.join(', ')}`);
      }

      return {
        success: true,
        ruleDate,
        appliedAt: result.appliedAt,
        verification,
        backup: currentRule
      };
    } catch (error) {
      console.error(`Rule deployment failed:`, error);
      
      // Attempt rollback if backup exists
      if (backup && currentRule) {
        console.log('Attempting rollback...');
        await this.rollbackRule(currentRule);
      }
      
      throw error;
    }
  }

  async verifyRuleDeployment(deployedRule, expectedRuleDate) {
    const verification = {
      valid: true,
      errors: [],
      checks: []
    };

    // Check 1: Rule exists
    if (!deployedRule) {
      verification.valid = false;
      verification.errors.push('No rule found after deployment');
      return verification;
    }

    // Check 2: Market is correct
    if (deployedRule.market !== 'HCS') {
      verification.valid = false;
      verification.errors.push(`Incorrect market: ${deployedRule.market}`);
    }

    // Check 3: All required modes exist
    const requiredModes = ['driving', 'public_transit', 'walking', 'biking', 'intermodal', 'trucking', 'duo', 'instant_duo', 'ridehail'];
    for (const mode of requiredModes) {
      if (!deployedRule.modes[mode]) {
        verification.valid = false;
        verification.errors.push(`Missing mode configuration: ${mode}`);
      }
    }

    // Check 4: Parameter ranges
    for (const [mode, config] of Object.entries(deployedRule.modes)) {
      if (config.min > config.max) {
        verification.valid = false;
        verification.errors.push(`Invalid range for ${mode}: min(${config.min}) > max(${config.max})`);
      }
      
      if (config.mean < config.min || config.mean > config.max) {
        verification.valid = false;
        verification.errors.push(`Mean outside range for ${mode}: ${config.mean} not in [${config.min}, ${config.max}]`);
      }
    }

    verification.checks.push('Market validation', 'Mode configuration', 'Parameter ranges');
    return verification;
  }

  async rollbackRule(backupRule) {
    try {
      await this.tripIncentiveRules.findOneAndUpdate(
        { market: 'HCS' },
        backupRule,
        { upsert: true }
      );
      console.log('Rule rollback completed successfully');
    } catch (error) {
      console.error('Rollback failed:', error);
      throw new Error('Critical: Rule deployment failed and rollback failed');
    }
  }

  async scheduleRuleDeployment(ruleDate, deploymentTime) {
    const now = new Date();
    const scheduledTime = new Date(deploymentTime);
    const delay = scheduledTime.getTime() - now.getTime();

    if (delay <= 0) {
      throw new Error('Deployment time must be in the future');
    }

    console.log(`Rule ${ruleDate} scheduled for deployment at ${scheduledTime.toISOString()}`);
    
    setTimeout(async () => {
      try {
        await this.deployRule(ruleDate);
        console.log(`Scheduled deployment of rule ${ruleDate} completed`);
      } catch (error) {
        console.error(`Scheduled deployment failed:`, error);
      }
    }, delay);

    return {
      ruleDate,
      scheduledFor: scheduledTime.toISOString(),
      delayMs: delay
    };
  }
}
```

### Testing and Validation
```javascript
class IncentiveRuleTester {
  constructor() {
    this.testDatabase = 'test_incentive_rules';
  }

  async testRuleFunction(ruleFunctionName) {
    const incentiveRules = require('@app/src/services/incentiveRule');
    const ruleFunction = incentiveRules[ruleFunctionName];
    
    if (!ruleFunction) {
      throw new Error(`Rule function ${ruleFunctionName} not found`);
    }

    try {
      // Mock the database for testing
      const originalModel = require('@app/src/models/TripIncentiveRules');
      const mockRule = this.createMockRule();
      
      // Test rule application
      await ruleFunction();
      
      return {
        success: true,
        ruleName: ruleFunctionName,
        testedAt: new Date().toISOString()
      };
    } catch (error) {
      return {
        success: false,
        ruleName: ruleFunctionName,
        error: error.message
      };
    }
  }

  createMockRule() {
    return {
      market: 'HCS',
      D: 300,
      h: 2,
      L: 20,
      W: 0.99,
      modes: {
        driving: { distance: 2, mean: 0.5, min: 0, max: 0.75, beta: 0.25 }
      },
      set: jest.fn(),
      markModified: jest.fn(),
      save: jest.fn()
    };
  }

  async validateRuleStructure(rule) {
    const requiredFields = ['market', 'D', 'h', 'L', 'W', 'modes', 'start', 'end'];
    const missingFields = requiredFields.filter(field => !(field in rule));
    
    if (missingFields.length > 0) {
      return {
        valid: false,
        errors: [`Missing required fields: ${missingFields.join(', ')}`]
      };
    }

    const requiredModes = ['driving', 'walking', 'biking', 'public_transit'];
    const missingModes = requiredModes.filter(mode => !(mode in rule.modes));
    
    if (missingModes.length > 0) {
      return {
        valid: false,
        errors: [`Missing required modes: ${missingModes.join(', ')}`]
      };
    }

    return { valid: true, errors: [] };
  }

  async runAllTests() {
    const incentiveRules = require('@app/src/services/incentiveRule');
    const ruleFunctions = Object.keys(incentiveRules);
    const results = [];

    for (const ruleName of ruleFunctions) {
      const result = await this.testRuleFunction(ruleName);
      results.push(result);
    }

    const successCount = results.filter(r => r.success).length;
    const failureCount = results.length - successCount;

    return {
      totalTests: results.length,
      successes: successCount,
      failures: failureCount,
      results
    };
  }
}
```

## 📊 Output Examples

### Rule Application Result
```json
{
  "success": true,
  "ruleDate": "2025-01-01",
  "appliedAt": "2024-06-25T14:30:00Z",
  "verification": {
    "valid": true,
    "errors": [],
    "checks": ["Market validation", "Mode configuration", "Parameter ranges"]
  }
}
```

### Rule Comparison Analysis
```json
{
  "budgetChanges": [{
    "field": "D",
    "from": 300,
    "to": 50000,
    "change": "+16567% budget increase"
  }],
  "limitChanges": [{
    "field": "L", 
    "from": 5,
    "to": 30,
    "change": "+500% weekly trip limit increase"
  }],
  "modeChanges": [{
    "mode": "ridehail",
    "field": "mean",
    "from": 0.01,
    "to": 50,
    "change": "+499900% ridehail reward increase"
  }]
}
```

### Rule Evolution Report
```json
{
  "totalRuleUpdates": 7,
  "patterns": {
    "campaignCycles": 3,
    "ridehailToggling": 4,
    "limitAdjustments": 6,
    "budgetIncrease": 1
  },
  "insights": [
    "Ridehail rewards are frequently toggled for cost control",
    "Weekly limits vary between 5-30 trips based on campaign goals",
    "Major budget increase in October 2024 enabled enhanced rewards"
  ]
}
```

## ⚠️ Important Notes

### Rule Parameter Meanings
- **D (Budget):** Daily budget limit in cents (300 = $3.00, 50000 = $500.00)
- **L (Limit):** Maximum trips per user per week for reward eligibility
- **W (Welcome):** Fixed bonus for first trip ($0.99 standard)
- **MC (Campaign):** Boolean flag indicating special campaign mode
- **h (Hours):** Time window for rule application (typically 2 hours)

### Travel Mode Reward Structure
```json
{
  "driving": "0.5-0.8 mean, moderate variance",
  "duo/instant_duo": "0.6-0.8 mean, higher rewards for carpooling",
  "public_transit": "0.6 mean, encouraging transit use",
  "biking": "0.2-0.5 mean, lower but consistent rewards",
  "walking": "0.1 mean, minimal rewards for short trips",
  "ridehail": "Highly variable, 0.01-50 mean depending on campaign",
  "trucking": "0.5 mean, commercial vehicle support",
  "intermodal": "0.6 mean, multi-modal trip bonuses"
}
```

### Deployment Considerations
- **Sequential Application:** Rules must be applied in chronological order
- **Database Transactions:** Each rule update should be atomic
- **Backup Strategy:** Always backup current rule before applying changes
- **Verification:** Validate rule structure after deployment
- **Rollback Plan:** Maintain ability to revert to previous rule

### Campaign Pattern Analysis
- **Cost Control Cycles:** Rules alternate between generous and restrictive
- **Ridehail Toggle:** Most frequently adjusted parameter for budget control
- **Seasonal Adjustments:** Holiday periods show increased limits and rewards
- **Budget Scaling:** Major budget increases enable enhanced reward programs

### Performance Impact
- **Rule Lookup:** Frequent database queries for current rule parameters
- **Parameter Caching:** Consider caching rule parameters with TTL
- **Update Frequency:** Rule changes are infrequent but impactful
- **Validation Cost:** Complex rule structure requires thorough validation

### Business Intelligence
- **A/B Testing:** Different rule versions enable testing of incentive effectiveness
- **Cost Management:** Rule parameters directly control program costs
- **User Behavior:** Rule changes drive predictable changes in travel patterns
- **ROI Tracking:** Rule history enables analysis of incentive program ROI

### Error Scenarios
- **Rule Conflicts:** Multiple rules with overlapping time periods
- **Invalid Parameters:** Mean/min/max ranges that violate mathematical constraints
- **Missing Modes:** Incomplete mode configuration breaking reward calculations
- **Database Failures:** Rule application failures requiring rollback procedures

## 🔗 Related File Links

- **Incentive Model:** `allrepo/connectsmart/tsp-api/src/models/TripIncentiveRules.js`
- **Incentive Helper:** `allrepo/connectsmart/tsp-api/src/services/incentiveHelper.js`
- **Incentive Controller:** Controllers that apply these rules for reward calculations
- **Trip Models:** Database models that reference these rules for reward processing

---
*This service provides essential rule versioning and configuration management for dynamic incentive program optimization in the TSP platform.*