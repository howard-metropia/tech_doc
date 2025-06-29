# CMCampaigns Model Documentation

## 📋 Model Overview
- **Purpose:** Manages campaign management (CM) system campaigns for user engagement and transportation mode changes
- **Table/Collection:** cm_campaign
- **Database Type:** MySQL
- **Relationships:** 
  - hasMany: CMCampaignUsers, CMSteps
  - belongsTo: CMGroups (via group_id)

## 🔧 Schema Definition
| Field Name | Type | Required | Description |
|------------|------|----------|-------------|
| id | int(11) | Yes | Primary key, auto-increment |
| is_active | int(11) | No | Campaign active status, default 1 |
| is_schedule | int(11) | No | Schedule sending flag, default 0 |
| name | varchar(255) | No | Campaign/card name |
| description | text | No | Campaign description |
| group_id | int(11) | No | Associated group ID |
| type_id | int(11) | Yes | Campaign/card type ID |
| creater | varchar(45) | No | Creator email address |
| utc_setting | varchar(255) | Yes | UTC timezone setting |
| start_time | datetime | No | Campaign start time |
| end_time | datetime | No | Campaign end/expiry time |
| from_time | varchar(255) | No | Daily from time |
| to_time | varchar(255) | No | Daily to time |
| start_time_0 | datetime | No | Alternative start time |
| end_time_0 | datetime | No | Alternative end time |
| from_time_0 | varchar(45) | No | Alternative from time |
| to_time_0 | varchar(45) | No | Alternative to time |
| travel_modes | text | No | Supported travel modes |
| change_mode_transport | int(2) | Yes | Transport mode change setting, default 5 |
| start_name | varchar(45) | No | Origin location name |
| start_address | varchar(200) | No | Origin address |
| start_center_lat | double | No | Origin center latitude |
| start_center_lng | double | No | Origin center longitude |
| start_range | float | No | Origin geofence range |
| end_center_lat | double | No | Destination center latitude |
| created_on | datetime | Yes | Creation timestamp |
| modified_on | datetime | Yes | Last modification timestamp |

## 🔑 Key Information
- **Primary Key:** id
- **Indexes:** None specified in schema
- **Unique Constraints:** None
- **Default Values:** 
  - is_active: 1
  - is_schedule: 0
  - change_mode_transport: 5

## 📝 Usage Examples
```javascript
// Get active campaigns
const activeCampaigns = await CMCampaigns.query().where('is_active', 1);

// Create a new campaign
const newCampaign = await CMCampaigns.query().insert({
  name: 'Public Transit Promotion',
  description: 'Encourage users to use public transport',
  type_id: 1,
  creater: 'admin@example.com',
  utc_setting: 'America/New_York',
  start_time: '2024-01-01 08:00:00',
  end_time: '2024-01-31 18:00:00'
});

// Get campaign with users
const campaignWithUsers = await CMCampaigns.query()
  .withGraphFetched('campaignUsers')
  .findById(1);
```

## 🔗 Related Models
- `CMCampaignUsers` - One-to-many relationship for campaign participants
- `CMSteps` - Campaign step configurations
- `CMGroups` - Campaign group associations
- `CMActivityLocation` - Location-based campaign activities

## 📌 Important Notes
- Supports geofenced campaigns with origin/destination targeting
- Timezone-aware campaign scheduling with UTC settings
- Multiple time configurations for flexible campaign timing
- Transportation mode change campaigns for behavior modification
- Campaign creator tracking via email address
- Active/inactive status for campaign lifecycle management

## 🏷️ Tags
**Keywords:** campaigns, marketing, engagement, transportation, geofencing, scheduling
**Category:** #model #database #campaigns #marketing #geolocation