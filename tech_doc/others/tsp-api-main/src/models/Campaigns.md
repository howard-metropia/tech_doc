# Campaigns Model Documentation

## 📋 Model Overview
- **Purpose:** Manages marketing campaigns, promotions, and incentive programs
- **Table/Collection:** campaign
- **Database Type:** MySQL (portal database)
- **Relationships:** Central entity for campaign management and user targeting

## 🔧 Schema Definition
| **Field Name** | **Type** | **Required** | **Description** |
|----------------|----------|--------------|-----------------|
| id | INT | Yes | Primary key, auto-increment |
| name | VARCHAR | Yes | Campaign name/title |
| description | TEXT | No | Detailed campaign description |
| campaign_type | VARCHAR | No | Type of campaign (incentive, promotion, notification) |
| target_audience | JSON | No | JSON defining target user criteria |
| start_date | DATETIME | Yes | Campaign start date and time |
| end_date | DATETIME | Yes | Campaign end date and time |
| budget | DECIMAL | No | Campaign budget allocation |
| status | VARCHAR | No | Campaign status (draft, active, paused, completed) |
| created_by | INT | No | Foreign key to admin user who created campaign |
| created_at | TIMESTAMP | Yes | Campaign creation timestamp |
| updated_at | TIMESTAMP | Yes | Last update timestamp |

## 🔑 Key Information
- **Primary Key:** id
- **Indexes:** campaign_type, status, start_date, end_date, created_by
- **Unique Constraints:** None
- **Default Values:** status = 'draft', created_at = CURRENT_TIMESTAMP

## 📝 Usage Examples
```javascript
// Get active campaigns
const activeCampaigns = await Campaigns.query()
  .where('status', 'active')
  .where('start_date', '<=', new Date())
  .where('end_date', '>=', new Date());

// Find campaigns by type
const incentiveCampaigns = await Campaigns.query()
  .where('campaign_type', 'incentive')
  .where('status', 'active');

// Create new campaign
await Campaigns.query().insert({
  name: 'Holiday Bonus',
  description: 'Extra points for trips during holidays',
  campaign_type: 'incentive',
  start_date: '2023-12-01 00:00:00',
  end_date: '2023-12-31 23:59:59',
  budget: 10000.00,
  created_by: adminUserId
});
```

## 🔗 Related Models
- `AuthUsers` - Many-to-one relationship via created_by (admin users)
- `TripIncentiveRules` - One-to-many relationship for campaign rules
- `CoinActivityLogs` - Tracks campaign-generated rewards
- `Notifications` - Campaign-triggered notifications

## 📌 Important Notes
- Supports various campaign types including incentives and promotions
- target_audience JSON field enables flexible user targeting
- Budget tracking for financial campaign management
- Date ranges control campaign activation periods
- Essential for user engagement and retention strategies

## 🏷️ Tags
**Keywords:** campaigns, marketing, incentives, promotions, targeting
**Category:** #model #database #campaigns #marketing #mysql

---
Note: This model powers the campaign management system for user engagement and marketing.