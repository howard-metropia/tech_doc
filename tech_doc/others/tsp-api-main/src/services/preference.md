# TSP API Preference Service Documentation

## 🔍 Quick Summary (TL;DR)
The Preference service manages user preferences for transportation options, including transport modes, single trip preferences, and parking preferences. It provides default settings, personalized storage, and preference updates with type validation and JSON serialization.

**Keywords:** user-preferences | transportation-settings | preference-management | default-preferences | transport-modes | parking-preferences | user-customization | preference-storage

**Primary use cases:** Storing user transportation preferences, retrieving personalized settings, managing default preference templates, updating user preference configurations, preference validation and type checking

**Compatibility:** Node.js >= 16.0.0, MySQL database for preference storage, Moment.js for timezone handling, JSON serialization for preference data

## ❓ Common Questions Quick Index
- **Q: What preference types are supported?** → Transport, single trip, and parking preferences
- **Q: How are preferences stored?** → JSON serialized in database with type-specific columns
- **Q: Are there default preferences?** → Yes, comprehensive defaults for all preference types and modes
- **Q: Can preferences be reset?** → Yes, by setting change_data to empty object
- **Q: What transport modes exist?** → Normal, family, travel, work for transport type
- **Q: How is the normal transport mode handled?** → Always returns default settings, cannot be customized

## 📋 Functionality Overview

**Non-technical explanation:** 
Think of this as your **travel preferences profile** in the app. It remembers how you like to travel - whether you prefer driving, public transit, walking, etc. You can have different preferences for different situations (work trips vs family trips) and the app will suggest transportation options based on what you've set up.

**Technical explanation:** 
A user preference management service that handles personalized transportation and parking settings through JSON-serialized database storage. Provides flexible preference types with default templates, user-specific customization, and validation for different travel modes and scenarios.

**Business value explanation:**
Enhances user experience through personalization, increases user engagement by remembering preferences, enables targeted transportation recommendations, supports different user personas (work/family/travel), and provides data insights for service optimization and feature development.

## 🔧 Technical Specifications

- **File:** `allrepo/connectsmart/tsp-api/src/services/preference.js`
- **Language:** JavaScript (ES2020)
- **Framework:** Node.js with Objection.js ORM
- **Type:** User Preference Management Service
- **File Size:** ~2.2 KB
- **Complexity Score:** ⭐⭐ (Low-Medium - JSON handling with validation)

**Dependencies:**
- `moment-timezone`: Date/time handling (**Medium**)
- `@app/src/models/Preference`: Preference database model (**Critical**)
- `@app/src/static/error-code`: Error code definitions (**High**)
- `@app/src/static/defines`: Default preference configurations (**Critical**)

## 📝 Detailed Code Analysis

### Core Functions

### get Function

**Purpose:** Retrieves user preferences with fallback to defaults

**Parameters:**
- `userId`: Number - User identifier
- `type`: String - Preference type ('transport', 'single', 'parking')

**Returns:** Promise resolving to preference object

**Logic Flow:**
```javascript
const preference = await Preference.query()
  .where('user_id', userId)
  .first();

if (preference) {
  if (preference[type] !== null) {
    result = JSON.parse(preference[type]);
  } else {
    result = DEFAULT_PREFERENCE[type];
  }
  // Special case: transport normal type is always default
  if (type === 'transport') {
    result.normal = DEFAULT_PREFERENCE.transport.normal;
  }
} else {
  result = DEFAULT_PREFERENCE[type];
}
```

**Key Features:**
- **Graceful Fallback:** Returns defaults when user preferences don't exist
- **JSON Deserialization:** Automatically parses stored JSON preferences
- **Normal Mode Override:** Transport normal mode always uses defaults
- **Type Safety:** Ensures correct preference structure returned

### update Function

**Purpose:** Updates or creates user preferences

**Parameters:**
- `inputData.userId`: Number - User identifier
- `inputData.type`: String - Preference type to update
- `inputData.change_data`: Object - New preference data

**Returns:** Promise resolving to updated preference data

**Implementation:**
```javascript
const updateData = {
  modified_on: moment.utc().toISOString(),
};
updateData[type] = 
  Object.keys(inputData.change_data).length > 0
    ? JSON.stringify(inputData.change_data)
    : null;

if (preference) {
  await Preference.query().where('user_id', userId).update(updateData);
} else {
  updateData.created_on = moment.utc().toISOString();
  updateData.user_id = userId;
  await Preference.query().insert(updateData);
}
```

**Features:**
- **Upsert Logic:** Creates record if doesn't exist, updates if exists
- **JSON Serialization:** Automatically serializes preference objects
- **Empty Data Handling:** Sets to null when change_data is empty
- **Timestamp Management:** Tracks creation and modification times

### getDefault Function

**Purpose:** Retrieves default preferences with optional mode specification

**Parameters:**
- `type`: String - Preference type
- `get_default`: String - Specific default mode (optional)

**Returns:** Promise resolving to default preference configuration

**Mode Validation:**
```javascript
if (defaultMode) {
  let isWrongDefaultMode = false;
  if (
    type === 'transport' &&
    ['normal', 'family', 'travel', 'work'].includes(defaultMode) === false
  ) {
    isWrongDefaultMode = true;
  } else if (
    type === 'single' &&
    ['vehicle', 'mass_transit'].includes(defaultMode) === false
  ) {
    isWrongDefaultMode = true;
  } else if (type === 'parking' && defaultMode !== 'parking') {
    isWrongDefaultMode = true;
  }

  if (isWrongDefaultMode) {
    throw new MaasError(ERROR_CODE.ERROR_BAD_REQUEST_PARAMS, ...);
  }
}
```

**Supported Modes:**
- **Transport:** normal, family, travel, work
- **Single:** vehicle, mass_transit
- **Parking:** parking (only mode)

## 🚀 Usage Methods

### Basic Preference Management
```javascript
const preferenceService = require('@app/src/services/preference');

async function getUserTransportPreferences(userId) {
  try {
    const transportPrefs = await preferenceService.get({
      userId: userId,
      type: 'transport'
    });
    
    console.log('User transport preferences:');
    console.log('Normal mode:', transportPrefs.normal);
    console.log('Family mode:', transportPrefs.family);
    console.log('Travel mode:', transportPrefs.travel);
    console.log('Work mode:', transportPrefs.work);
    
    return transportPrefs;
  } catch (error) {
    console.error('Error getting transport preferences:', error);
    throw error;
  }
}

async function updateUserParkingPreferences(userId, newSettings) {
  try {
    const result = await preferenceService.update({
      userId: userId,
      type: 'parking',
      change_data: newSettings
    });
    
    console.log('Parking preferences updated:', result);
    return result;
  } catch (error) {
    console.error('Error updating parking preferences:', error);
    throw error;
  }
}

// Usage
const userId = 12345;
const transportPrefs = await getUserTransportPreferences(userId);

const newParkingSettings = {
  maxWalkingDistance: 500,
  preferCoveredParking: true,
  maxHourlyRate: 5.00
};
await updateUserParkingPreferences(userId, newParkingSettings);
```

### Comprehensive Preference Manager
```javascript
class UserPreferenceManager {
  constructor() {
    this.preferenceService = require('@app/src/services/preference');
    this.preferenceTypes = ['transport', 'single', 'parking'];
  }

  async getUserAllPreferences(userId) {
    try {
      const preferences = {};
      
      for (const type of this.preferenceTypes) {
        preferences[type] = await this.preferenceService.get({
          userId,
          type
        });
      }
      
      return {
        userId,
        preferences,
        lastUpdated: new Date().toISOString()
      };
    } catch (error) {
      console.error('Error getting all user preferences:', error);
      throw error;
    }
  }

  async setTransportModePreference(userId, mode, settings) {
    try {
      // Get current transport preferences
      const currentPrefs = await this.preferenceService.get({
        userId,
        type: 'transport'
      });
      
      // Update specific mode
      const updatedPrefs = { ...currentPrefs };
      updatedPrefs[mode] = { ...updatedPrefs[mode], ...settings };
      
      // Save updated preferences
      const result = await this.preferenceService.update({
        userId,
        type: 'transport',
        change_data: updatedPrefs
      });
      
      return {
        userId,
        mode,
        updatedSettings: settings,
        fullPreferences: result
      };
    } catch (error) {
      console.error(`Error setting ${mode} transport preferences:`, error);
      throw error;
    }
  }

  async resetPreferencesToDefaults(userId, type) {
    try {
      // Get default preferences for type
      const defaults = await this.preferenceService.getDefault({ type });
      
      // Update user preferences with defaults
      const result = await this.preferenceService.update({
        userId,
        type,
        change_data: defaults
      });
      
      return {
        userId,
        type,
        resetToDefaults: true,
        newPreferences: result
      };
    } catch (error) {
      console.error(`Error resetting ${type} preferences:`, error);
      throw error;
    }
  }

  async clonePreferencesFromUser(sourceUserId, targetUserId, types = null) {
    try {
      const typesToClone = types || this.preferenceTypes;
      const clonedPreferences = {};
      
      for (const type of typesToClone) {
        // Get source user preferences
        const sourcePrefs = await this.preferenceService.get({
          userId: sourceUserId,
          type
        });
        
        // Set for target user
        await this.preferenceService.update({
          userId: targetUserId,
          type,
          change_data: sourcePrefs
        });
        
        clonedPreferences[type] = sourcePrefs;
      }
      
      return {
        sourceUserId,
        targetUserId,
        clonedTypes: typesToClone,
        clonedPreferences
      };
    } catch (error) {
      console.error('Error cloning user preferences:', error);
      throw error;
    }
  }

  async compareUserPreferencesWithDefaults(userId) {
    try {
      const comparison = {};
      
      for (const type of this.preferenceTypes) {
        const userPrefs = await this.preferenceService.get({ userId, type });
        const defaults = await this.preferenceService.getDefault({ type });
        
        comparison[type] = {
          hasCustomizations: JSON.stringify(userPrefs) !== JSON.stringify(defaults),
          userPreferences: userPrefs,
          defaultPreferences: defaults,
          differences: this.findPreferenceDifferences(userPrefs, defaults)
        };
      }
      
      return {
        userId,
        comparison,
        hasAnyCustomizations: Object.values(comparison).some(c => c.hasCustomizations)
      };
    } catch (error) {
      console.error('Error comparing preferences with defaults:', error);
      throw error;
    }
  }

  findPreferenceDifferences(userPrefs, defaults) {
    const differences = {};
    
    for (const key in userPrefs) {
      if (JSON.stringify(userPrefs[key]) !== JSON.stringify(defaults[key])) {
        differences[key] = {
          user: userPrefs[key],
          default: defaults[key]
        };
      }
    }
    
    return differences;
  }
}
```

### Preference Validation and Sanitization
```javascript
class PreferenceValidator {
  constructor() {
    this.preferenceService = require('@app/src/services/preference');
  }

  async validatePreferenceUpdate(userId, type, changeData) {
    const validation = {
      valid: true,
      errors: [],
      warnings: [],
      sanitizedData: null
    };

    try {
      // Get current preferences and defaults for reference
      const currentPrefs = await this.preferenceService.get({ userId, type });
      const defaults = await this.preferenceService.getDefault({ type });
      
      // Validate based on preference type
      switch (type) {
        case 'transport':
          validation.sanitizedData = this.validateTransportPreferences(changeData, defaults);
          break;
        case 'single':
          validation.sanitizedData = this.validateSinglePreferences(changeData, defaults);
          break;
        case 'parking':
          validation.sanitizedData = this.validateParkingPreferences(changeData, defaults);
          break;
        default:
          validation.valid = false;
          validation.errors.push(`Unknown preference type: ${type}`);
          return validation;
      }
      
      // Check for required fields
      const requiredFields = this.getRequiredFields(type);
      for (const field of requiredFields) {
        if (!(field in validation.sanitizedData)) {
          validation.errors.push(`Missing required field: ${field}`);
        }
      }
      
      // Validate against reasonable bounds
      const boundsCheck = this.validateBounds(type, validation.sanitizedData);
      if (!boundsCheck.valid) {
        validation.warnings.push(...boundsCheck.warnings);
      }
      
      validation.valid = validation.errors.length === 0;
      return validation;
    } catch (error) {
      validation.valid = false;
      validation.errors.push(`Validation error: ${error.message}`);
      return validation;
    }
  }

  validateTransportPreferences(changeData, defaults) {
    const sanitized = { ...defaults };
    
    // Validate each transport mode
    const validModes = ['normal', 'family', 'travel', 'work'];
    for (const mode of validModes) {
      if (changeData[mode]) {
        sanitized[mode] = this.sanitizeTransportModeSettings(changeData[mode]);
      }
    }
    
    return sanitized;
  }

  sanitizeTransportModeSettings(modeSettings) {
    const sanitized = {};
    
    // Validate transport types
    if (modeSettings.transportTypes && Array.isArray(modeSettings.transportTypes)) {
      const validTypes = ['driving', 'transit', 'walking', 'cycling', 'rideshare'];
      sanitized.transportTypes = modeSettings.transportTypes.filter(type => 
        validTypes.includes(type)
      );
    }
    
    // Validate preferences
    if (typeof modeSettings.avoidTolls === 'boolean') {
      sanitized.avoidTolls = modeSettings.avoidTolls;
    }
    
    if (typeof modeSettings.avoidHighways === 'boolean') {
      sanitized.avoidHighways = modeSettings.avoidHighways;
    }
    
    if (typeof modeSettings.maxWalkingDistance === 'number' && 
        modeSettings.maxWalkingDistance >= 0) {
      sanitized.maxWalkingDistance = Math.min(modeSettings.maxWalkingDistance, 5000);
    }
    
    return sanitized;
  }

  validateSinglePreferences(changeData, defaults) {
    const sanitized = { ...defaults };
    
    // Validate vehicle preferences
    if (changeData.vehicle) {
      sanitized.vehicle = {
        ...sanitized.vehicle,
        ...this.sanitizeVehicleSettings(changeData.vehicle)
      };
    }
    
    // Validate mass transit preferences
    if (changeData.mass_transit) {
      sanitized.mass_transit = {
        ...sanitized.mass_transit,
        ...this.sanitizeMassTransitSettings(changeData.mass_transit)
      };
    }
    
    return sanitized;
  }

  sanitizeVehicleSettings(vehicleSettings) {
    const sanitized = {};
    
    if (typeof vehicleSettings.fuelEfficiency === 'number' && 
        vehicleSettings.fuelEfficiency > 0) {
      sanitized.fuelEfficiency = Math.min(vehicleSettings.fuelEfficiency, 100);
    }
    
    if (typeof vehicleSettings.vehicleType === 'string') {
      const validTypes = ['car', 'truck', 'motorcycle', 'ev'];
      if (validTypes.includes(vehicleSettings.vehicleType)) {
        sanitized.vehicleType = vehicleSettings.vehicleType;
      }
    }
    
    return sanitized;
  }

  sanitizeMassTransitSettings(transitSettings) {
    const sanitized = {};
    
    if (typeof transitSettings.maxTransfers === 'number' && 
        transitSettings.maxTransfers >= 0) {
      sanitized.maxTransfers = Math.min(transitSettings.maxTransfers, 5);
    }
    
    if (typeof transitSettings.wheelchairAccessible === 'boolean') {
      sanitized.wheelchairAccessible = transitSettings.wheelchairAccessible;
    }
    
    return sanitized;
  }

  validateParkingPreferences(changeData, defaults) {
    const sanitized = { ...defaults.parking };
    
    if (typeof changeData.maxWalkingDistance === 'number' && 
        changeData.maxWalkingDistance >= 0) {
      sanitized.maxWalkingDistance = Math.min(changeData.maxWalkingDistance, 2000);
    }
    
    if (typeof changeData.maxHourlyRate === 'number' && 
        changeData.maxHourlyRate >= 0) {
      sanitized.maxHourlyRate = Math.min(changeData.maxHourlyRate, 50);
    }
    
    if (typeof changeData.preferCoveredParking === 'boolean') {
      sanitized.preferCoveredParking = changeData.preferCoveredParking;
    }
    
    return { parking: sanitized };
  }

  getRequiredFields(type) {
    const requiredFields = {
      transport: ['normal', 'family', 'travel', 'work'],
      single: ['vehicle', 'mass_transit'],
      parking: ['parking']
    };
    
    return requiredFields[type] || [];
  }

  validateBounds(type, data) {
    const warnings = [];
    
    // Add bounds checking logic
    if (type === 'parking' && data.parking) {
      if (data.parking.maxHourlyRate > 20) {
        warnings.push('Maximum hourly rate is unusually high');
      }
      if (data.parking.maxWalkingDistance > 1000) {
        warnings.push('Maximum walking distance is quite far');
      }
    }
    
    return {
      valid: warnings.length === 0,
      warnings
    };
  }
}
```

### Preference Analytics
```javascript
class PreferenceAnalytics {
  constructor() {
    this.preferenceService = require('@app/src/services/preference');
    this.knex = require('@maas/core/mysql')('portal');
  }

  async getPreferenceUsageStatistics() {
    try {
      // Get counts of users with custom preferences
      const stats = await this.knex('preference')
        .select([
          this.knex.raw('COUNT(*) as total_users_with_preferences'),
          this.knex.raw('SUM(CASE WHEN transport IS NOT NULL THEN 1 ELSE 0 END) as transport_customizations'),
          this.knex.raw('SUM(CASE WHEN single IS NOT NULL THEN 1 ELSE 0 END) as single_customizations'),
          this.knex.raw('SUM(CASE WHEN parking IS NOT NULL THEN 1 ELSE 0 END) as parking_customizations')
        ])
        .first();

      const totalUsers = await this.knex('auth_user').count('* as count').first();

      return {
        totalUsers: parseInt(totalUsers.count),
        usersWithPreferences: parseInt(stats.total_users_with_preferences),
        customizationRates: {
          transport: (parseInt(stats.transport_customizations) / parseInt(totalUsers.count) * 100).toFixed(2) + '%',
          single: (parseInt(stats.single_customizations) / parseInt(totalUsers.count) * 100).toFixed(2) + '%',
          parking: (parseInt(stats.parking_customizations) / parseInt(totalUsers.count) * 100).toFixed(2) + '%'
        },
        adoptionRate: (parseInt(stats.total_users_with_preferences) / parseInt(totalUsers.count) * 100).toFixed(2) + '%'
      };
    } catch (error) {
      console.error('Error getting preference usage statistics:', error);
      throw error;
    }
  }

  async analyzeMostCommonSettings(type) {
    try {
      const preferences = await this.knex('preference')
        .select(type)
        .whereNotNull(type);

      const settingCounts = {};
      
      for (const pref of preferences) {
        try {
          const parsed = JSON.parse(pref[type]);
          this.countSettings(parsed, settingCounts);
        } catch (error) {
          // Skip invalid JSON
        }
      }

      // Sort by frequency
      const sortedSettings = Object.entries(settingCounts)
        .sort(([,a], [,b]) => b - a)
        .slice(0, 10)
        .map(([setting, count]) => ({
          setting,
          count,
          percentage: (count / preferences.length * 100).toFixed(2) + '%'
        }));

      return {
        type,
        totalPreferences: preferences.length,
        mostCommonSettings: sortedSettings
      };
    } catch (error) {
      console.error(`Error analyzing ${type} settings:`, error);
      throw error;
    }
  }

  countSettings(obj, counts, prefix = '') {
    for (const [key, value] of Object.entries(obj)) {
      const fullKey = prefix ? `${prefix}.${key}` : key;
      
      if (typeof value === 'object' && value !== null && !Array.isArray(value)) {
        this.countSettings(value, counts, fullKey);
      } else {
        const settingKey = `${fullKey}: ${JSON.stringify(value)}`;
        counts[settingKey] = (counts[settingKey] || 0) + 1;
      }
    }
  }
}
```

## 📊 Output Examples

### Get Preferences Response
```json
{
  "normal": {
    "transportTypes": ["driving", "transit"],
    "avoidTolls": false,
    "avoidHighways": false
  },
  "family": {
    "transportTypes": ["driving"],
    "avoidTolls": true,
    "maxWalkingDistance": 200
  },
  "travel": {
    "transportTypes": ["transit", "walking"],
    "avoidTolls": false
  },
  "work": {
    "transportTypes": ["transit", "cycling"],
    "avoidTolls": true
  }
}
```

### Update Response
```json
{
  "maxWalkingDistance": 500,
  "preferCoveredParking": true,
  "maxHourlyRate": 5.00,
  "avoidMeterParking": false
}
```

### Default Preferences Response
```json
{
  "parking": {
    "maxWalkingDistance": 400,
    "maxHourlyRate": 10.00,
    "preferCoveredParking": false,
    "avoidMeterParking": false,
    "preferGroundLevel": false
  }
}
```

### Validation Result
```json
{
  "valid": true,
  "errors": [],
  "warnings": ["Maximum walking distance is quite far"],
  "sanitizedData": {
    "parking": {
      "maxWalkingDistance": 1000,
      "preferCoveredParking": true,
      "maxHourlyRate": 8.00
    }
  }
}
```

### Usage Statistics
```json
{
  "totalUsers": 10000,
  "usersWithPreferences": 3500,
  "customizationRates": {
    "transport": "25.50%",
    "single": "18.20%", 
    "parking": "12.80%"
  },
  "adoptionRate": "35.00%"
}
```

## ⚠️ Important Notes

### Preference Type System
- **Transport Preferences:** Multi-mode settings (normal, family, travel, work)
- **Single Preferences:** Vehicle and mass transit specific settings
- **Parking Preferences:** Parking-related preferences and constraints
- **Normal Mode Exception:** Transport normal mode always uses default settings

### Data Storage and Serialization
- **JSON Storage:** Preferences stored as JSON strings in database
- **Null Handling:** Null values trigger fallback to default preferences
- **Empty Data:** Empty change_data objects stored as null
- **Timestamp Tracking:** Creation and modification timestamps maintained

### Default Preference System
- **Comprehensive Defaults:** Default settings for all preference types
- **Mode-Specific Defaults:** Different defaults for different transport modes
- **Validation Integration:** Defaults used for validation and fallback
- **Dynamic Loading:** Defaults loaded from static configuration files

### Error Handling and Validation
- **Type Validation:** Strict validation of preference types and modes
- **Parameter Validation:** Comprehensive parameter checking
- **JSON Safety:** Safe JSON parsing with fallback handling
- **User-Friendly Errors:** Clear error messages for invalid requests

### Performance Considerations
- **Single Query Design:** Efficient single-query preference retrieval
- **JSON Efficiency:** Compact JSON storage for complex preference structures
- **Caching Opportunities:** Static defaults could be cached
- **Bulk Operations:** Support for batch preference updates

### Business Logic
- **User Personalization:** Support for detailed user customization
- **Default Fallbacks:** Graceful fallback to sensible defaults
- **Mode Flexibility:** Support for different travel scenarios
- **Preference Evolution:** Easy addition of new preference types

### Integration Points
- **Route Planning:** Preferences used in route calculation algorithms
- **Transportation Recommendations:** Preference-based service suggestions
- **UI Customization:** Frontend uses preferences for interface personalization
- **Analytics Integration:** Preference data feeds into user behavior analytics

## 🔗 Related File Links

- **Preference Model:** `allrepo/connectsmart/tsp-api/src/models/Preference.js`
- **Default Defines:** `allrepo/connectsmart/tsp-api/src/static/defines.js`
- **Error Codes:** `allrepo/connectsmart/tsp-api/src/static/error-code.js`
- **Preference Controllers:** API endpoints that use preference data

---
*This service provides essential user preference management capabilities with comprehensive validation, default handling, and personalization features for the TSP platform.*