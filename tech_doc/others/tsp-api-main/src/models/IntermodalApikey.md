# Model Documentation: IntermodalApikey

## 📋 Model Overview
- **Purpose:** Manages API keys for intermodal transportation service integrations
- **Table/Collection:** intermodal_api_key
- **Database Type:** MySQL
- **Relationships:** Not defined in model

## 🔧 Schema Definition
| **Field Name** | **Type** | **Required** | **Description** |
|----------------|----------|--------------|-----------------|
| *Schema not defined in model file* | - | - | Table structure exists in database |

## 🔑 Key Information
- **Primary Key:** Likely id (standard convention)
- **Indexes:** Database-defined
- **Unique Constraints:** API key field likely unique
- **Default Values:** Database-defined

## 📝 Usage Examples
```javascript
// Find API key by service name
const apiKey = await IntermodalApikey.query()
  .where('service_name', 'uber')
  .first();

// Get all active API keys
const activeKeys = await IntermodalApikey.query()
  .where('status', 'active');

// Create new API key
const newKey = await IntermodalApikey.query().insert({
  service_name: 'lyft',
  api_key: 'encrypted_key',
  status: 'active'
});

// Update API key
await IntermodalApikey.query()
  .patch({ api_key: 'new_encrypted_key' })
  .where('id', keyId);
```

## 🔗 Related Models
- May relate to various transportation service models
- Could reference partner/provider configurations

## 📌 Important Notes
- Uses MySQL 'portal' connection
- Stores API credentials for external services
- Part of Objection.js ORM system
- Likely includes encryption for sensitive API keys

## 🏷️ Tags
**Keywords:** api, intermodal, authentication, integration, credentials
**Category:** #model #database #integration #security #mysql

---