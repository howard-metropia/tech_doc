# CMSteps Model

## 📋 Model Overview
- **Purpose:** Manages campaign management steps within the campaign workflow
- **Table/Collection:** cm_step
- **Database Type:** MySQL (portal)
- **Relationships:** BelongsTo CMCampaigns

## 🔧 Schema Definition
*Schema fields are not explicitly defined in the model. Database table structure would need to be verified.*
- **campaign_id** | **Integer** | **Required** | **Foreign key to cm_campaign**

## 🔑 Key Information
- **Primary Key:** Not explicitly defined (likely `id`)
- **Indexes:** campaign_id (foreign key)
- **Unique Constraints:** Not specified
- **Default Values:** Not specified

## 📝 Usage Examples
```javascript
// Basic query example
const steps = await CMSteps.query().where('campaign_id', 123);

// With campaign relation
const stepsWithCampaign = await CMSteps.query()
  .withGraphFetched('cmCampaign')
  .where('campaign_id', 123);
```

## 🔗 Related Models
- `CMCampaigns` - Many-to-one relationship via campaign_id

## 📌 Important Notes
- Part of campaign management system
- Uses Objection.js ORM with MySQL portal database
- Belongs to a specific campaign

## 🏷️ Tags
**Keywords:** campaign, steps, workflow, management
**Category:** #model #database #campaign #workflow