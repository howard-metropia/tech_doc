# DuoGroups Model Documentation

## 📋 Model Overview
- **Purpose:** Manages carpool/rideshare groups for duo transportation mode with geofencing and membership
- **Table/Collection:** duo_group
- **Database Type:** MySQL
- **Relationships:** 
  - hasMany: DuoGroupMembers, DuoReservations, GroupAdminProfiles
  - belongsTo: Enterprises (via enterprise_id)

## 🔧 Schema Definition
| Field Name | Type | Required | Description |
|------------|------|----------|-------------|
| id | int(11) | Yes | Primary key, auto-increment |
| creator_id | int(11) | Yes | User ID of group creator |
| name | varchar(512) | Yes | Group name |
| description | varchar(512) | No | Group description |
| is_private | varchar(1) | Yes | Private group flag ('F'/'T'), default 'F' |
| avatar | varchar(512) | No | Group avatar image URL |
| geofence | varchar(512) | Yes | Geofence boundary definition |
| geofence_radius | float | Yes | Geofence radius in meters |
| geofence_latitude | double | No | Geofence center latitude |
| geofence_longitude | double | No | Geofence center longitude |
| address | varchar(200) | No | Group address/location |
| banner | varchar(512) | No | Group banner image URL |
| enterprise_id | int(11) | No | Associated enterprise ID |
| client_id | int(11) | No | Client application ID |
| disabled | varchar(1) | Yes | Disabled status ('F'/'T'), default 'F' |

## 🔑 Key Information
- **Primary Key:** id
- **Indexes:** None specified in schema
- **Unique Constraints:** None
- **Default Values:** 
  - is_private: 'F'
  - disabled: 'F'

## 📝 Usage Examples
```javascript
// Get all active duo groups
const activeGroups = await DuoGroups.query().where('disabled', 'F');

// Create a new duo group
const newGroup = await DuoGroups.query().insert({
  creator_id: 123,
  name: 'Downtown Commuters',
  description: 'Carpool group for downtown workers',
  geofence: 'POLYGON((...))',
  geofence_radius: 1000,
  geofence_latitude: 40.7128,
  geofence_longitude: -74.0060
});

// Get group with related data
const groupWithMembers = await DuoGroups.query()
  .withGraphFetched('members')
  .findById(1);
```

## 🔗 Related Models
- `DuoGroupMembers` - Many-to-many relationship for group membership
- `DuoReservations` - Reservations associated with the group
- `GroupAdminProfiles` - Admin profiles for group management
- `Enterprises` - Enterprise association for corporate groups
- `AuthUsers` - Creator and member relationships

## 📌 Important Notes
- Geofencing is used to restrict group access to specific geographic areas
- Groups can be private (invitation only) or public
- Enterprise integration allows for corporate carpool groups
- Creator has special privileges for group management
- Disabled groups are soft-deleted rather than removed

## 🏷️ Tags
**Keywords:** carpool, rideshare, geofencing, groups, duo, transportation
**Category:** #model #database #transportation #geolocation