# CMCampaignUsers Model

## 📋 Model Overview
- **Purpose:** Manages user participation in campaign management campaigns
- **Table/Collection:** cm_campaign_user
- **Database Type:** MySQL (portal)
- **Relationships:** None defined

## 🔧 Schema Definition
*Schema fields are not explicitly defined in the model. Database table structure would need to be verified.*

## 🔑 Key Information
- **Primary Key:** Not explicitly defined (likely `id`)
- **Indexes:** Not specified
- **Unique Constraints:** Not specified
- **Default Values:** Not specified

## 📝 Usage Examples
```javascript
// Basic query example
const campaignUsers = await CMCampaignUsers.query().where('campaign_id', 123);

// Get user campaigns
const userCampaigns = await CMCampaignUsers.query().where('user_id', 456);
```

## 🔗 Related Models
- No explicit relationships defined
- Likely related to CMCampaigns and user models

## 📌 Important Notes
- Minimal model with only table name definition
- Part of campaign management system
- Manages many-to-many relationship between campaigns and users
- Uses Objection.js ORM with MySQL portal database

## 🏷️ Tags
**Keywords:** campaign, user, participation, management
**Category:** #model #database #campaign #user #participation