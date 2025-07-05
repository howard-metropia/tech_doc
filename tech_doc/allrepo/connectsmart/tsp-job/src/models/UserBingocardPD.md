# UserBingocardPD Model

## Overview
User bingo card personal data model for the TSP Job system. Manages gamified transportation challenges, bingo card progress, and achievement tracking.

## Model Definition
```javascript
const knex = require('@maas/core/mysql')('portal');
class UserBingocardPD extends Model {
  static get tableName() {
    return 'user_bingocard_pd';
  }
}
module.exports = UserBingocardPD.bindKnex(knex);
```

## Database Configuration
- **Database**: Portal MySQL instance
- **Table**: `user_bingocard_pd`
- **ORM**: Objection.js with Knex query builder

## Purpose
- Bingo card challenge tracking
- Gamified transportation goals
- Achievement progress monitoring
- User engagement enhancement

## Bingo Card Features
- **Transportation Modes**: Multi-modal challenges
- **Sustainability Goals**: Environmental objectives
- **Social Challenges**: Community participation
- **Frequency Targets**: Regular usage goals
- **Distance Milestones**: Travel distance achievements

## Key Features
- Personal challenge tracking
- Progress visualization
- Completion rewards
- Social sharing capabilities

## Challenge Types
- **Mode Diversity**: Try different transport modes
- **Eco-Friendly**: Use sustainable options
- **Distance Goals**: Achieve travel distances
- **Social Transport**: Share rides with others
- **Regular Usage**: Maintain consistent usage patterns

## Integration Points
- **AuthUsers**: User identification
- **Trips**: Transportation activities
- **UserBadgeRelatedActivityLog**: Achievement tracking
- **CoinTransaction**: Reward distribution

## Gamification Elements
- Progress tracking
- Achievement unlocking
- Reward systems
- Social competition
- Personal challenges

## Related Models
- AuthUsers: User identification
- Trips: Activity tracking
- UserBadgeRelatedActivityLog: Achievements
- CoinTransaction: Rewards

## Development Notes
- Gamification system component
- User engagement focus
- Progress tracking essential
- Reward integration important