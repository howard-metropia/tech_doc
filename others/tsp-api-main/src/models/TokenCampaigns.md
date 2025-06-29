# TokenCampaigns Model Documentation

## 📋 Model Overview
- **Purpose:** Manages token-based reward campaigns and promotional activities
- **Table/Collection:** token_campaign
- **Database Type:** MySQL
- **Relationships:** References campaigns and token reward systems

## 🔧 Schema Definition
| **Field Name** | **Type** | **Required** | **Description** |
|----------------|----------|--------------|------------------|
| id | Integer | Yes | Primary key (auto-increment) |
| campaign_name | String | - | Name of the token campaign |
| campaign_type | String | - | Type of campaign (referral, milestone, etc.) |
| token_reward | Integer | - | Number of tokens awarded |
| start_date | DateTime | - | Campaign start date |
| end_date | DateTime | - | Campaign end date |
| max_participants | Integer | - | Maximum number of participants |
| current_participants | Integer | - | Current participant count |
| is_active | Boolean | - | Whether campaign is active |
| conditions | JSON | - | Campaign participation conditions |
| description | Text | - | Campaign description |
| target_audience | String | - | Target user group |
| budget_limit | Decimal | - | Maximum token budget |
| tokens_distributed | Integer | - | Total tokens given out |
| created_by | Integer | - | Admin user who created campaign |
| created_at | DateTime | - | Record creation timestamp |
| updated_at | DateTime | - | Record update timestamp |

## 🔑 Key Information
- **Primary Key:** id
- **Indexes:** Likely on campaign_type, is_active, start_date, end_date
- **Unique Constraints:** Possibly campaign_name
- **Default Values:** Auto-generated timestamps, current_participants default 0

## 📝 Usage Examples
```javascript
// Create new token campaign
const campaign = await TokenCampaigns.query().insert({
  campaign_name: 'Summer Referral Bonus',
  campaign_type: 'referral',
  token_reward: 100,
  start_date: new Date(),
  end_date: new Date(Date.now() + 30*24*60*60*1000), // 30 days
  max_participants: 1000,
  is_active: true,
  conditions: { min_referrals: 3 }
});

// Get active campaigns
const activeCampaigns = await TokenCampaigns.query()
  .where('is_active', true)
  .where('start_date', '<=', new Date())
  .where('end_date', '>=', new Date());

// Update campaign participation
await TokenCampaigns.query()
  .where('id', campaignId)
  .increment('current_participants', 1)
  .increment('tokens_distributed', tokenReward);
```

## 🔗 Related Models
- **UserTokens**: Token rewards are distributed to users
- **CampaignParticipants**: Tracks who joined campaigns
- **Referrals**: Referral campaigns reference user referrals

## 📌 Important Notes
- Manages token-based incentive programs
- Supports various campaign types with flexible conditions
- Budget and participant limit controls
- Time-based campaign activation
- Tracks distribution metrics for analysis

## 🏷️ Tags
**Keywords:** tokens, campaigns, rewards, incentives
**Category:** #model #database #campaigns #rewards