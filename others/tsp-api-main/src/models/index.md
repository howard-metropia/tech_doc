# Models Index Documentation

## 📋 Model Overview
- **Purpose:** Centralized export module for all model files in the models directory
- **Table/Collection:** N/A (Module loader)
- **Database Type:** N/A
- **Relationships:** Provides access to all models via single import

## 🔧 Schema Definition
This is not a database model but a Node.js module loader that dynamically exports all models.

| **Export Name** | **Type** | **Description** |
|-----------------|----------|------------------|
| [filename] | Model | Each model file exported by its filename |

## 🔑 Key Information
- **Primary Key:** N/A
- **Indexes:** N/A
- **Unique Constraints:** N/A
- **Default Values:** N/A

## 📝 Usage Examples
```javascript
// Import all models at once
const models = require('./models');

// Access specific models
const { AuthUsers, UserWallets, TripRecords } = models;

// Alternative usage
const AuthUsers = models.AuthUsers;
const UserWallets = models.UserWallets;

// List all available models
console.log(Object.keys(models));
```

## 🔗 Related Models
- **All Models**: This module provides access to every model in the directory

## 📌 Important Notes
- Automatically discovers and loads all model files
- Excludes the index.js file itself from loading
- Provides convenient single-import access to all models
- Model names match their filename (without .js extension)
- Useful for controllers that need multiple models

## 🏷️ Tags
**Keywords:** module-loader, exports, models, convenience
**Category:** #utility #module #models #loader