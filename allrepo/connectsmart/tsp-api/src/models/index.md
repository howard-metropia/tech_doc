# Models Index - Dynamic Model Loading

## Overview
A dynamic model loader that automatically discovers and exports all database models in the models directory. This module provides a centralized way to access all TSP API data models through a single import.

## File Purpose
- **Primary Function**: Dynamic model discovery and export
- **Type**: Module loader and exporter
- **Role**: Centralized model registry for the TSP API

## Key Features

### Dynamic Model Discovery
- Automatically scans the models directory
- Loads all JavaScript files except the index file itself
- Creates a consolidated models object for easy access

### Implementation Details
```javascript
const fs = require('fs');
const path = require('path');
const baseName = path.basename(__filename);
const loadPath = path.join(__dirname);

const models = {};

fs.readdirSync(loadPath)
  .filter((file) => file.indexOf('.') !== 0 && file !== baseName)
  .forEach((file) => {
    const modelName = path.parse(file).name;
    const model = require(path.join(loadPath, file));
    models[modelName] = model;
  });
```

## Functionality

### File Discovery Logic
1. **Directory Scanning**: Uses `fs.readdirSync()` to read all files in the models directory
2. **File Filtering**: Excludes hidden files (starting with '.') and the index file itself
3. **Model Loading**: Dynamically requires each model file
4. **Name Extraction**: Uses filename (without extension) as the model key

### Model Registration
- **Key Generation**: Model name derived from filename using `path.parse(file).name`
- **Dynamic Require**: Each model loaded using `require(path.join(loadPath, file))`
- **Object Assembly**: All models collected into a single exported object

## Usage Examples

### Importing All Models
```javascript
const models = require('./models');

// Access specific models
const User = models.AuthUsers;
const Trip = models.Trips;
const Notification = models.Notifications;
```

### Using with Destructuring
```javascript
const { AuthUsers, Trips, Notifications } = require('./models');

// Use models directly
const user = await AuthUsers.query().findById(1);
const trips = await Trips.query().where('user_id', userId);
```

## Model Architecture

### Supported Models
The index loads all models in the directory, including but not limited to:
- **Authentication**: AuthUsers, AuthUserTokens, AuthUserBk
- **Transportation**: Trips, TripDetails, RidehailTrips
- **Notifications**: Notifications, NotificationUsers, NotificationMsgs
- **Campaigns**: Campaigns, TokenCampaigns
- **Payments**: PointsTransaction, RedeemTransactions
- **Location Services**: Favorites, Reservations
- **Enterprise**: Enterprises, EnterpriseBlocks

### Model Patterns
- **ORM Integration**: Models typically use Objection.js or Sequelize ORM
- **Database Abstraction**: Models provide database-agnostic interfaces
- **Relationship Management**: Models define associations and relationships

## Technical Specifications

### File System Operations
- **Synchronous Loading**: Uses `fs.readdirSync()` for immediate model availability
- **Path Resolution**: Uses `path.join()` for cross-platform compatibility
- **Error Handling**: Relies on Node.js module loading error handling

### Performance Considerations
- **Startup Loading**: All models loaded at application startup
- **Memory Usage**: All models kept in memory for fast access
- **Lazy Loading**: Not implemented - all models loaded immediately

## Integration Points

### Database Connections
- Models inherit database connections from their individual configurations
- Connection pooling managed at the model level
- Transaction support through ORM integration

### Service Layer Integration
- Models consumed by service layer for business logic
- Repository pattern implementation through model abstraction
- Data validation and transformation handled at model level

## Security Considerations

### Data Access Control
- Model-level security depends on individual model implementations
- Authentication and authorization handled by consuming services
- SQL injection protection through ORM parameterization

### Configuration Security
- Database credentials managed through environment variables
- Connection security configured at the ORM level
- Audit logging capabilities depend on individual model setup

## Error Handling

### Loading Errors
- Module loading errors bubble up through Node.js require system
- Invalid model files will cause application startup failure
- Missing dependencies handled by Node.js module resolution

### Runtime Errors
- Database connection errors handled by individual models
- Query errors managed through ORM error handling
- Model validation errors returned through model interfaces

## Maintenance Notes

### Adding New Models
1. Create new model file in the models directory
2. Ensure proper export structure
3. Model automatically available through index import
4. No manual registration required

### Model Organization
- Consider subdirectory organization for large model sets
- Maintain consistent naming conventions
- Document model relationships and dependencies

### Performance Monitoring
- Monitor model loading time during application startup
- Track memory usage of model registry
- Consider lazy loading for large model sets if needed