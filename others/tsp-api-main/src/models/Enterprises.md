# Enterprises Model Documentation

## 📋 Model Overview
- **Purpose:** Manages enterprise/corporate accounts for organizational transportation programs
- **Table/Collection:** enterprise
- **Database Type:** MySQL
- **Relationships:** 
  - hasMany: DuoGroups, Teleworks, EnterpriseInvites, EnterpriseBlocks

## 🔧 Schema Definition
| Field Name | Type | Required | Description |
|------------|------|----------|-------------|
| id | int(11) | Yes | Primary key, auto-increment |
| name | varchar(255) | No | Enterprise name |
| code | varchar(45) | No | Enterprise code/identifier |
| created_on | datetime | Yes | Creation timestamp |
| modified_on | datetime | Yes | Last modification timestamp |

## 🔑 Key Information
- **Primary Key:** id
- **Indexes:** None specified in schema
- **Unique Constraints:** None
- **Default Values:** 
  - created_on: CURRENT_TIMESTAMP
  - modified_on: CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP

## 📝 Usage Examples
```javascript
// Create new enterprise
const enterprise = await Enterprises.query().insert({
  name: 'Tech Corp Inc.',
  code: 'TECH001'
});

// Get enterprise with related groups
const enterpriseWithGroups = await Enterprises.query()
  .withGraphFetched('duoGroups')
  .findById(1);

// Find enterprise by code
const enterprise = await Enterprises.query()
  .where('code', 'TECH001')
  .first();
```

## 🔗 Related Models
- `DuoGroups` - Corporate carpool groups
- `Teleworks` - Telework tracking for employees
- `EnterpriseInvites` - User invitations to join enterprise
- `EnterpriseBlocks` - Blocked users or restrictions

## 📌 Important Notes
- Supports corporate transportation programs
- Enables enterprise-specific carpool groups
- Code field provides unique identification
- Foundation for B2B features and reporting

## 🏷️ Tags
**Keywords:** enterprise, corporate, organizations, b2b, groups
**Category:** #model #database #enterprise #corporate #organizations