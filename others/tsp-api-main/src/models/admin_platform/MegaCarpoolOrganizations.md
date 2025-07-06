# MegaCarpoolOrganizations Model Documentation

## 📋 Model Overview
- **Purpose:** Links organizations to mega-carpool programs managed through admin platform
- **Table/Collection:** mega_carpool_organizations
- **Database Type:** MySQL (admin database)
- **Relationships:** 
  - belongsTo: MegaCarpools (via mega_id)

## 🔧 Schema Definition
| Field Name | Type | Required | Description |
|------------|------|----------|-------------|
| id | int(11) | Yes | Primary key, auto-increment |
| mega_id | int(11) | Yes | Foreign key to mega_carpools |
| * | Mixed | - | Additional organization fields |

## 🔑 Key Information
- **Primary Key:** id
- **Indexes:** None specified
- **Unique Constraints:** None
- **Default Values:** None specified
- **Foreign Keys:** mega_id → mega_carpools.id

## 📝 Usage Examples
```javascript
// Add organization to mega carpool
const orgAssociation = await MegaCarpoolOrganizations.query().insert({
  mega_id: 1,
  organization_id: 456,
  joined_date: new Date()
});

// Get organizations in a mega carpool
const organizations = await MegaCarpoolOrganizations.query()
  .where('mega_id', 1);

// Remove organization from mega carpool
await MegaCarpoolOrganizations.query()
  .delete()
  .where({ mega_id: 1, organization_id: 456 });
```

## 🔗 Related Models
- `MegaCarpools` - Parent mega carpool programs
- Links organizations to large-scale carpool initiatives

## 📌 Important Notes
- Junction table for mega carpool and organization relationships
- Admin platform model for program management
- Enables multi-organization carpool coordination
- Part of large-scale transportation program infrastructure

## 🏷️ Tags
**Keywords:** organizations, mega-carpools, junction-table, admin-platform, associations
**Category:** #model #database #admin-platform #organizations #associations