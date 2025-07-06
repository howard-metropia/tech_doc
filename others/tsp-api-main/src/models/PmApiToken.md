# PmApiToken Model Documentation

## 📋 Model Overview
- **Purpose:** Manages API tokens for ParkMobile integration and parking payment services
- **Table/Collection:** pm_api_token
- **Database Type:** MySQL
- **Relationships:** Standalone table for API token management

## 🔧 Schema Definition
| Field Name | Type | Required | Description |
|------------|------|----------|-------------|
| id | int(11) | Yes | Primary key, auto-increment |
| token | text | Yes | API token string |
| expires | datetime | Yes | Token expiration timestamp |
| created_at | datetime | Yes | Token creation timestamp |
| updated_at | datetime | Yes | Last update timestamp |

## 🔑 Key Information
- **Primary Key:** id
- **Indexes:** expires (for expiration queries)
- **Unique Constraints:** None
- **Default Values:** 
  - created_at: CURRENT_TIMESTAMP
  - updated_at: CURRENT_TIMESTAMP

## 📝 Usage Examples
```javascript
// Create new API token
const token = await PmApiToken.query().insert({
  token: 'pm_api_token_xyz123...',
  expires: new Date(Date.now() + 24 * 60 * 60 * 1000) // 24 hours
});

// Get valid tokens
const validTokens = await PmApiToken.query()
  .where('expires', '>', new Date())
  .orderBy('expires', 'desc');

// Clean up expired tokens
await PmApiToken.query()
  .delete()
  .where('expires', '<', new Date());

// Get latest valid token
const currentToken = await PmApiToken.query()
  .where('expires', '>', new Date())
  .orderBy('expires', 'desc')
  .first();
```

## 🔗 Related Models
- Used for ParkMobile parking payment integration
- Related to parking activity types in PointsTransaction
- Supports parking fee transactions

## 📌 Important Notes
- Manages API tokens for third-party parking services
- Token expiration tracking prevents stale API calls
- Index on expires field optimizes cleanup queries
- Associated with 'park-mobile' activity type (ID: 13)
- Supports automated token refresh workflows
- Essential for parking payment processing

## 🏷️ Tags
**Keywords:** api-tokens, parkmobile, parking, authentication, integration, expiration
**Category:** #model #database #api #authentication #parking #integration