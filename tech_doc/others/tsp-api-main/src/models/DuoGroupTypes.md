# DuoGroupTypes Model Documentation

## 📋 Model Overview
- **Purpose:** Defines types and categories for duo/group features in the application
- **Table/Collection:** group_type
- **Database Type:** MySQL
- **Relationships:** Referenced by group/duo functionality

## 🔧 Schema Definition
| **Field Name** | **Type** | **Required** | **Description** |
|----------------|----------|--------------|------------------|
| id | Integer | Yes | Primary key (auto-increment) |
| type_name | String | - | Name of the group type |
| type_code | String | - | Unique code identifier |
| description | Text | - | Detailed description |
| max_members | Integer | - | Maximum group size |
| min_members | Integer | - | Minimum group size |
| permissions | JSON | - | Group permission settings |
| features | JSON | - | Available features for type |
| is_active | Boolean | - | Whether type is active |
| icon | String | - | Icon identifier |
| sort_order | Integer | - | Display order |
| created_at | DateTime | - | Record creation timestamp |
| updated_at | DateTime | - | Record update timestamp |

## 🔑 Key Information
- **Primary Key:** id
- **Indexes:** Likely on type_code, is_active, sort_order
- **Unique Constraints:** Possibly type_code
- **Default Values:** Auto-generated timestamps, is_active default true

## 📝 Usage Examples
```javascript
// Create new group type
const groupType = await DuoGroupTypes.query().insert({
  type_name: 'Carpool Group',
  type_code: 'CARPOOL',
  description: 'Groups for sharing rides',
  max_members: 4,
  min_members: 2,
  permissions: { can_invite: true, can_schedule: true },
  features: ['ride_sharing', 'cost_splitting'],
  is_active: true
});

// Get active group types
const activeTypes = await DuoGroupTypes.query()
  .where('is_active', true)
  .orderBy('sort_order');

// Find group type by code
const carpoolType = await DuoGroupTypes.query()
  .where('type_code', 'CARPOOL')
  .first();
```

## 🔗 Related Models
- **DuoGroups**: Groups are created based on these types
- **DuoGroupMembers**: Member limits defined by group type
- **GroupPermissions**: Permissions structure references these types

## 📌 Important Notes
- Configurable group size limits and permissions
- Feature flags for type-specific functionality
- Hierarchical display ordering system
- JSON fields for flexible configuration
- Used as reference data for group creation

## 🏷️ Tags
**Keywords:** groups, types, configuration, permissions
**Category:** #model #database #groups #configuration