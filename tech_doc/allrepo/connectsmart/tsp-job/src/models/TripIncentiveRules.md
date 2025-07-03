# TripIncentiveRules Model

## Overview
MongoDB-based model for managing trip incentive rules in the TSP Job system. Defines dynamic incentive calculation rules, market-specific configurations, and reward structures for various transportation modes and user behaviors.

## Model Definition
```javascript
const mongoose = require('mongoose');
const conn = require('@maas/core/mongo')('cache');

const schema = new mongoose.Schema({ market: String }, { strict: false });
const TripIncentiveRules = conn.model('trip_incentive_rules', schema);

module.exports = TripIncentiveRules;
```

## Database Configuration
- **Database**: Cache MongoDB instance
- **Collection**: `trip_incentive_rules`
- **ORM**: Mongoose with flexible schema
- **Connection**: Managed by @maas/core MongoDB connection
- **Schema**: Non-strict for dynamic rule structures

## Purpose
- Dynamic incentive rule management
- Market-specific reward configurations
- Transportation mode incentive definitions
- User behavior reward structures
- Campaign and promotion rule storage

## Key Features
- Flexible schema for diverse rule types
- Market-based rule segmentation
- Real-time rule updates
- Dynamic incentive calculations
- Multi-criteria reward structures

## Technical Implementation
The model uses MongoDB's flexible document structure to store complex incentive rules that can vary significantly across markets, transportation modes, and user segments. The non-strict schema allows for dynamic rule evolution without database migrations.

### Schema Structure
While using `strict: false`, typical rule documents contain:
```javascript
{
  market: "string",              // Market identifier
  rule_type: "string",           // Type of incentive rule
  transportation_modes: [],      // Applicable transport modes
  user_segments: [],             // Target user categories
  calculation_method: "object",  // Reward calculation logic
  conditions: {},                // Eligibility criteria
  reward_structure: {},          // Incentive amounts and types
  effective_dates: {},           // Rule validity period
  campaign_id: "string",         // Associated campaign
  priority: "number",            // Rule precedence
  status: "string",              // Active/inactive status
  metadata: {}                   // Additional rule properties
}
```

### Rule Operations
```javascript
// Retrieve market-specific rules
const marketRules = await TripIncentiveRules.find({
  market: marketId,
  status: 'active',
  'effective_dates.start': { $lte: new Date() },
  'effective_dates.end': { $gte: new Date() }
});

// Create new incentive rule
const newRule = new TripIncentiveRules({
  market: 'Austin',
  rule_type: 'carpool_incentive',
  transportation_modes: ['carpool', 'rideshare'],
  calculation_method: {
    base_reward: 5.0,
    distance_multiplier: 0.1,
    time_bonus: 2.0
  },
  conditions: {
    min_distance: 2.0,
    peak_hours_bonus: true,
    first_time_user_bonus: 10.0
  },
  effective_dates: {
    start: new Date(),
    end: new Date(Date.now() + 30 * 24 * 60 * 60 * 1000) // 30 days
  },
  status: 'active'
});
await newRule.save();

// Update rule conditions
await TripIncentiveRules.updateOne(
  { _id: ruleId },
  { 
    $set: { 
      'conditions.min_distance': 3.0,
      'reward_structure.peak_bonus': 3.0 
    } 
  }
);
```

## Rule Types
### Base Incentive Rules
- **Distance-based**: Rewards based on trip distance
- **Mode-specific**: Transportation mode incentives
- **Time-based**: Peak hour and time-of-day bonuses
- **Frequency**: Regular user loyalty rewards

### Campaign Rules
- **Promotional**: Limited-time special offers
- **Seasonal**: Holiday and event-based incentives
- **Corporate**: Enterprise program rewards
- **New User**: Onboarding and first-trip bonuses

### Behavioral Rules
- **Multi-modal**: Cross-transportation mode rewards
- **Efficiency**: Green transportation bonuses
- **Social**: Carpool and rideshare incentives
- **Consistency**: Regular usage pattern rewards

## Market Segmentation
The model supports market-specific rule customization:
- Geographic market boundaries
- Local transportation preferences
- Regional pricing structures
- Cultural behavior adaptations
- Regulatory compliance requirements

## Integration Points
- **Incentive Engine**: Rule evaluation and calculation
- **Trip Processing**: Real-time incentive determination
- **User Wallet**: Reward credit processing
- **Campaign Management**: Promotional rule coordination
- **Analytics**: Rule performance tracking

## Usage Context
Essential for:
- Dynamic incentive calculation
- Market-specific reward customization
- Campaign and promotion management
- User behavior modification
- Transportation mode encouragement
- Revenue optimization

## Performance Considerations
- MongoDB indexing for efficient rule queries
- Caching of frequently accessed rules
- Optimized rule evaluation algorithms
- Real-time rule update capabilities
- Scalable document storage

### Indexing Strategy
```javascript
// Recommended indexes for performance
db.trip_incentive_rules.createIndex({ market: 1, status: 1 });
db.trip_incentive_rules.createIndex({ "effective_dates.start": 1, "effective_dates.end": 1 });
db.trip_incentive_rules.createIndex({ rule_type: 1, priority: -1 });
db.trip_incentive_rules.createIndex({ transportation_modes: 1 });
```

## Rule Evaluation Logic
### Priority System
- Higher priority rules override lower priority
- Market-specific rules take precedence
- Campaign rules override base rules
- User-specific rules have highest priority

### Calculation Methods
- **Fixed Amount**: Static reward values
- **Percentage-based**: Proportional to trip metrics
- **Tiered Structure**: Progressive reward scales
- **Conditional Logic**: Complex eligibility criteria

## Security Features
- Rule modification audit logging
- Access control for rule management
- Data validation for rule integrity
- Secure rule evaluation processing
- Fraud prevention rule enforcement

## Related Models
- PointsTransaction: Incentive payment tracking
- UserWallet: Reward credit management
- Trips: Trip data for rule evaluation
- AuthUsers: User segmentation correlation
- Campaigns: Marketing campaign integration

## API Integration
Core for:
- Rule management endpoints
- Real-time incentive calculation
- Campaign configuration services
- Market customization APIs
- Performance analytics reporting

## Business Logic Support
- Dynamic pricing strategies
- Market penetration optimization
- User engagement enhancement
- Revenue management logic
- Competitive positioning rules

## Development Notes
- Flexible schema design for rule evolution
- Non-strict MongoDB schema for adaptability
- Optimized for real-time rule evaluation
- Compatible with A/B testing frameworks
- Supports complex business logic requirements

## Rule Management Workflow
### Rule Creation
1. Market analysis and segmentation
2. Business objective definition
3. Rule structure design
4. Testing and validation
5. Deployment and monitoring

### Rule Updates
- Version control for rule changes
- A/B testing for rule effectiveness
- Performance impact assessment
- Rollback capabilities
- User communication management

## Analytics and Monitoring
- Rule effectiveness tracking
- User behavior impact analysis
- Revenue optimization metrics
- Market penetration measurement
- Campaign performance evaluation

## Data Quality Management
- Rule validation and verification
- Consistency checks across markets
- Performance impact monitoring
- User satisfaction correlation
- Business objective alignment

## Scalability Considerations
- MongoDB horizontal scaling support
- Efficient rule caching strategies
- Distributed rule evaluation
- Real-time synchronization
- Load balancing for rule queries

## Maintenance and Operations
- Regular rule performance reviews
- Market-specific optimization
- Campaign effectiveness analysis
- System performance monitoring
- Business impact assessment