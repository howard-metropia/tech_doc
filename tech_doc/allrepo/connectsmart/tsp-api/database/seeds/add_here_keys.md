# HERE API Keys Seed

## 📋 Seed Overview
- **Purpose:** Initializes HERE Maps API keys for location services and mapping functionality
- **Environment:** All environments (requires valid HERE API credentials)
- **Dependencies:** here_api_keys table must exist
- **Idempotent:** Yes (deletes existing keys before inserting)

## 🔧 Data Summary
```javascript
// HERE API key pool
{
  table: 'here_api_keys',
  data: [
    { key: 'ogrYTkzs5eCzieEw4YnLhK3T18w013cPgQwbQygJbKk' },
    { key: 'vQhhNhxUt6wSYbkT_fBqGriywLrUg3Vq346-zcv9oas' },
    // ... 11 total API keys
  ]
}
```

## 📝 Affected Tables
| Table | Records | Description |
|-------|---------|-------------|
| here_api_keys | 11 | HERE Maps API key pool for rotation |

## ⚠️ Important Notes
- **API Key Pool:** Provides multiple keys for load balancing and rate limit management
- **Transaction Safety:** Uses database transactions with rollback on error
- **Key Rotation:** Supports multiple keys to distribute API requests
- **Security:** Keys are production credentials - handle with care
- **Error Handling:** Includes transaction rollback on insertion failure
- **HERE Integration:** Required for geocoding, routing, and mapping services

## 🏷️ Tags
**Keywords:** here-maps, api-keys, location-services, geocoding, mapping, third-party
**Category:** #seed #data #api-keys #here-maps #location-services