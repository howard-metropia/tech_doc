# Agency Model

## 📋 Model Overview
- **Purpose:** Manages transit agency information and metadata
- **Table/Collection:** agency
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
const agencies = await Agency.query().where('status', 'active');

// Get agency by name
const agency = await Agency.query().where('name', 'Metro Transit');
```

## 🔗 Related Models
- No explicit relationships defined
- Core model for transit system organization

## 📌 Important Notes
- Minimal model with only table name definition
- Central to transit agency management
- Uses Objection.js ORM with MySQL portal database
- Likely referenced by routes, stops, and other transit models

## 🏷️ Tags
**Keywords:** agency, transit, organization, provider
**Category:** #model #database #agency #transit #provider