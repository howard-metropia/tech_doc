# MegaCarpools Model Documentation

## 📋 Model Overview
- **Purpose:** Manages large-scale carpool programs and mega-carpool initiatives from admin platform
- **Table/Collection:** mega_carpools
- **Database Type:** MySQL (admin database)
- **Relationships:** 
  - hasMany: MegaCarpoolOrganizations (via mega_id)

## 🔧 Schema Definition
| Field Name | Type | Required | Description |
|------------|------|----------|-------------|
| id | int(11) | Yes | Primary key, auto-increment |
| * | Mixed | - | Schema not fully defined in model |

## 🔑 Key Information
- **Primary Key:** id
- **Indexes:** None specified
- **Unique Constraints:** None
- **Default Values:** None specified

## 📝 Usage Examples
```javascript
// Get mega carpool with organizations
const megaCarpool = await MegaCarpools.query()
  .withGraphFetched('orgs')
  .findById(1);

// Create new mega carpool program
const newProgram = await MegaCarpools.query().insert({
  name: 'City-wide Carpool Initiative',
  description: 'Large scale carpool program'
});

// Get all mega carpools
const allPrograms = await MegaCarpools.query()
  .withGraphFetched('orgs');
```

## 🔗 Related Models
- `MegaCarpoolOrganizations` - Organizations participating in mega carpools
- Managed from admin platform for large-scale programs

## 📌 Important Notes
- Admin platform model for managing large carpool programs
- Connects to admin database (not portal)
- Supports multi-organization carpool initiatives
- Relationship mapping defined for organization management

## 🏷️ Tags
**Keywords:** mega-carpools, admin-platform, large-scale, organizations, programs
**Category:** #model #database #admin-platform #carpools #large-scale