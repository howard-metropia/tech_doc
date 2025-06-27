# TSP API Local User Label Service Documentation

## 🔍 Quick Summary (TL;DR)
The Local User Label service manages user location-based labeling, automatically switching users between local and non-local status based on their geographic position relative to service area boundaries using state machines and geospatial validation.

**Keywords:** user-labeling | geospatial-validation | state-machine | service-area | location-based | user-categorization | polygon-checking | label-management

**Primary use cases:** Identifying local vs non-local users, managing user labels based on location, checking if users are within service boundaries, implementing location-based features and pricing

**Compatibility:** Node.js >= 16.0.0, MySQL database, Turf.js for geospatial operations, XState for state management

## ❓ Common Questions Quick Index
- **Q: What are the label IDs?** → Label ID 2 = Local User, Label ID 3 = Non-Local User
- **Q: How is service area determined?** → From market profile polygon configuration using WKT format
- **Q: Can users have both labels?** → No, they are mutually exclusive - having one removes the other
- **Q: Is the state machine necessary?** → Used for complex workflows and event-driven label transitions
- **Q: What coordinate system is used?** → Standard WGS84 (longitude, latitude) for point-in-polygon checks
- **Q: Are label changes immediate?** → Yes, database updates happen synchronously when conditions are met

## 📋 Functionality Overview

**Non-technical explanation:** 
Think of this as a **geographic membership system**. When users use the app, it checks if they're inside the local service area (like being inside city limits). If they are, they get marked as "local users" which might give them different features or pricing. If they're outside, they're marked as "non-local users."

**Technical explanation:** 
A geospatial user categorization service that uses point-in-polygon algorithms to determine if users are within defined service boundaries. Implements state machine patterns for managing label transitions and maintains user categorization in the database through the AuthUserLabel model. Integrates with market profiles for dynamic service area definitions.

**Business value explanation:**
Enables location-based service differentiation, supports regional pricing strategies, helps with market analysis and user segmentation, and allows for targeted feature rollouts. Critical for businesses operating in specific geographic markets with different service levels for local vs visiting users.

## 🔧 Technical Specifications

- **File:** `allrepo/connectsmart/tsp-api/src/services/localUserLabel.js`
- **Language:** JavaScript (ES2020)
- **Framework:** Node.js with XState state machines
- **Type:** Geospatial User Management Service
- **File Size:** ~4.1 KB
- **Complexity Score:** ⭐⭐⭐ (Medium - State machines and geospatial operations)

**Dependencies:**
- `@app/src/services/stateMachine`: State machine management (**High**)
- `@app/src/models/AuthUserLabel`: User label database model (**Critical**)
- `@maas/core/log`: Logging infrastructure (**High**)
- `wkt`: Well-Known Text parser for polygons (**High**)
- `@turf/turf`: Geospatial operations library (**Critical**)
- `@app/src/services/marketProfile`: Market configuration (**High**)

## 📝 Detailed Code Analysis

### Label ID Constants
- **Label ID 2:** Local User designation
- **Label ID 3:** Non-Local User designation

### switchToLocalUser Function

**Purpose:** Switches a user from non-local to local status

**Parameters:**
- `userId`: Number - User identifier

**Returns:** Boolean - Success status of the switch operation

**Logic Flow:**
1. Checks if user already has local label (ID: 2)
2. Checks if user has non-local label (ID: 3)
3. If not local, adds local label
4. If was non-local, removes non-local label
5. Returns false if already local or not previously non-local

**Implementation:**
```javascript
async function switchToLocalUser(userId) {
  const hasLocalUserLabel = await AuthUserLabel.query()
    .findOne({ user_id: userId, label_id: 2 });
  const hasNonLocalUserLabel = await AuthUserLabel.query()
    .findOne({ user_id: userId, label_id: 3 });
    
  if (!hasLocalUserLabel) {
    await AuthUserLabel.query().insert({ user_id: userId, label_id: 2 });
    
    if (hasNonLocalUserLabel) {
      await AuthUserLabel.query().delete()
        .where({ user_id: userId, label_id: 3 });
    } else {
      return false; // User wasn't non-local
    }
  } else {
    return false; // Already local
  }
  return true;
}
```

### checkServiceArea Function

**Purpose:** Determines if coordinates are within the service area polygon

**Parameters:**
- `lat`: Number - Latitude coordinate
- `lng`: Number - Longitude coordinate

**Returns:** Boolean - True if point is within service area

**Process:**
1. Retrieves market profile for current project
2. Parses WKT polygon from profile
3. Creates Turf.js point from coordinates
4. Handles both Polygon and MultiPolygon types
5. Performs point-in-polygon check

**Implementation:**
```javascript
function checkServiceArea(lat, lng) {
  const serviceProfile = getServiceProfile(process.env.PROJECT_TITLE.toLowerCase());
  const point = turf.point([lng, lat]);
  const geoJson = parse(serviceProfile.polygon);
  
  let polygon;
  if (geoJson.type.toLowerCase() === 'polygon') {
    polygon = turf.polygon(geoJson.coordinates);
  }
  if (geoJson.type.toLowerCase() === 'multipolygon') {
    polygon = turf.multiPolygon(geoJson.coordinates);
  }
  
  return turf.booleanPointInPolygon(point, polygon);
}
```

### State Machine Configuration

**Purpose:** Manages label transition workflow

**States:**
- `NonLocalUser`: Initial state for users outside service area
- `LocalUser`: Final state for users inside service area

**Transitions:**
- `SWITCH_TO_LOCAL_USER`: Triggers label update and external service notification

**Context:**
- `userId`: User identifier
- `lat`: Latitude for location tracking
- `lng`: Longitude for location tracking

### setNonLocalUser Function

**Purpose:** Sets a user as non-local if they don't have a local label

**Parameters:**
- `userId`: Number - User identifier

**Returns:** Boolean - Success status

**Logic:**
- Prevents setting non-local if user is already local
- Adds non-local label if not already present
- Maintains mutual exclusivity of labels

## 🚀 Usage Methods

### Basic Label Management
```javascript
const localUserLabel = require('@app/src/services/localUserLabel');

async function handleUserLocation(userId, latitude, longitude) {
  try {
    // Check if user is in service area
    const isInServiceArea = localUserLabel.checkServiceArea(latitude, longitude);
    
    if (isInServiceArea) {
      // Switch to local user if in service area
      const switched = await localUserLabel.switchToLocalUser(userId);
      
      if (switched) {
        console.log(`User ${userId} is now a local user`);
        return { status: 'local', switched: true };
      } else {
        console.log(`User ${userId} was already a local user`);
        return { status: 'local', switched: false };
      }
    } else {
      // Set as non-local if outside service area
      const setNonLocal = await localUserLabel.setNonLocalUser(userId);
      
      if (setNonLocal) {
        console.log(`User ${userId} is now a non-local user`);
        return { status: 'non-local', set: true };
      } else {
        console.log(`User ${userId} status unchanged`);
        return { status: 'unchanged', set: false };
      }
    }
  } catch (error) {
    console.error('Error handling user location:', error);
    throw error;
  }
}
```

### State Machine Integration
```javascript
async function processUserWithStateMachine(userId, lat, lng) {
  const localUserLabel = require('@app/src/services/localUserLabel');
  
  try {
    // Get configured state machine
    const stateMachine = localUserLabel.getStateMachine(userId, lat, lng);
    
    // Check current state
    const currentState = stateMachine.getSnapshot().value;
    console.log(`User ${userId} current state: ${currentState}`);
    
    // Check if user should be local
    const isInServiceArea = localUserLabel.checkServiceArea(lat, lng);
    
    if (isInServiceArea && currentState === 'NonLocalUser') {
      // Trigger transition to local user
      stateMachine.send('SWITCH_TO_LOCAL_USER');
      
      console.log(`State machine transitioned user ${userId} to LocalUser`);
    }
    
    return {
      userId,
      previousState: currentState,
      newState: stateMachine.getSnapshot().value,
      location: { lat, lng },
      inServiceArea: isInServiceArea
    };
  } catch (error) {
    console.error('State machine processing failed:', error);
    throw error;
  }
}
```

### Location-Based Feature Access
```javascript
class LocationBasedFeatures {
  constructor() {
    this.localUserLabel = require('@app/src/services/localUserLabel');
    this.AuthUserLabel = require('@app/src/models/AuthUserLabel');
  }

  async getUserLocationStatus(userId) {
    try {
      const labels = await this.AuthUserLabel.query()
        .where('user_id', userId)
        .whereIn('label_id', [2, 3]);
      
      if (labels.length === 0) {
        return { status: 'unknown', hasLabel: false };
      }
      
      const label = labels[0];
      return {
        status: label.label_id === 2 ? 'local' : 'non-local',
        hasLabel: true,
        labelId: label.label_id
      };
    } catch (error) {
      console.error('Error getting user location status:', error);
      throw error;
    }
  }

  async canAccessLocalFeature(userId, featureName) {
    const localOnlyFeatures = ['local-deals', 'neighborhood-events', 'resident-parking'];
    
    if (!localOnlyFeatures.includes(featureName)) {
      return { allowed: true, reason: 'Feature available to all users' };
    }
    
    const status = await this.getUserLocationStatus(userId);
    
    if (status.status === 'local') {
      return { allowed: true, reason: 'Local user access granted' };
    } else {
      return { 
        allowed: false, 
        reason: 'Feature restricted to local users',
        userStatus: status.status
      };
    }
  }

  async applyLocationBasedPricing(userId, basePrice, serviceType) {
    const status = await this.getUserLocationStatus(userId);
    
    const pricingRules = {
      local: {
        discount: 0.15, // 15% discount for locals
        services: ['transit', 'parking', 'bike-share']
      },
      'non-local': {
        discount: 0,
        surcharge: 0.10, // 10% surcharge for visitors
        services: ['parking', 'special-events']
      }
    };
    
    const rules = pricingRules[status.status] || pricingRules['non-local'];
    let finalPrice = basePrice;
    
    if (rules.services.includes(serviceType)) {
      if (rules.discount > 0) {
        finalPrice = basePrice * (1 - rules.discount);
      }
      if (rules.surcharge > 0) {
        finalPrice = basePrice * (1 + rules.surcharge);
      }
    }
    
    return {
      basePrice,
      finalPrice: Math.round(finalPrice * 100) / 100,
      userStatus: status.status,
      discount: rules.discount,
      surcharge: rules.surcharge || 0,
      appliedRule: rules.services.includes(serviceType)
    };
  }
}
```

### Batch User Processing
```javascript
class UserLocationBatchProcessor {
  constructor() {
    this.localUserLabel = require('@app/src/services/localUserLabel');
  }

  async processUserLocations(userLocations) {
    const results = {
      processed: 0,
      switchedToLocal: 0,
      setToNonLocal: 0,
      unchanged: 0,
      errors: 0
    };
    
    for (const userLocation of userLocations) {
      try {
        const { userId, lat, lng } = userLocation;
        
        const isInServiceArea = this.localUserLabel.checkServiceArea(lat, lng);
        
        if (isInServiceArea) {
          const switched = await this.localUserLabel.switchToLocalUser(userId);
          if (switched) {
            results.switchedToLocal++;
          } else {
            results.unchanged++;
          }
        } else {
          const setNonLocal = await this.localUserLabel.setNonLocalUser(userId);
          if (setNonLocal) {
            results.setToNonLocal++;
          } else {
            results.unchanged++;
          }
        }
        
        results.processed++;
      } catch (error) {
        console.error(`Error processing user ${userLocation.userId}:`, error);
        results.errors++;
      }
    }
    
    return results;
  }

  async auditUserLabels() {
    const AuthUser = require('@app/src/models/AuthUser');
    const AuthUserLabel = require('@app/src/models/AuthUserLabel');
    
    // Get all users with their labels
    const users = await AuthUser.query()
      .select('auth_user.id', 'auth_user.last_latitude', 'auth_user.last_longitude')
      .leftJoin('auth_user_label', 'auth_user.id', 'auth_user_label.user_id')
      .whereIn('auth_user_label.label_id', [2, 3])
      .orWhereNull('auth_user_label.label_id');
    
    const audit = {
      totalUsers: users.length,
      correctLabels: 0,
      incorrectLabels: 0,
      missingLabels: 0,
      corrections: []
    };
    
    for (const user of users) {
      if (!user.last_latitude || !user.last_longitude) {
        audit.missingLabels++;
        continue;
      }
      
      const shouldBeLocal = this.localUserLabel.checkServiceArea(
        user.last_latitude, 
        user.last_longitude
      );
      
      const currentLabel = await AuthUserLabel.query()
        .findOne({ user_id: user.id })
        .whereIn('label_id', [2, 3]);
      
      if (!currentLabel) {
        audit.missingLabels++;
        audit.corrections.push({
          userId: user.id,
          action: shouldBeLocal ? 'add_local' : 'add_non_local'
        });
      } else {
        const isCurrentlyLocal = currentLabel.label_id === 2;
        
        if (shouldBeLocal === isCurrentlyLocal) {
          audit.correctLabels++;
        } else {
          audit.incorrectLabels++;
          audit.corrections.push({
            userId: user.id,
            currentLabel: isCurrentlyLocal ? 'local' : 'non-local',
            shouldBe: shouldBeLocal ? 'local' : 'non-local'
          });
        }
      }
    }
    
    return audit;
  }
}
```

### Service Area Analytics
```javascript
class ServiceAreaAnalytics {
  constructor() {
    this.localUserLabel = require('@app/src/services/localUserLabel');
    this.turf = require('@turf/turf');
  }

  generateServiceAreaGrid(gridSize = 0.01) {
    const marketProfile = require('@app/src/services/marketProfile');
    const { parse } = require('wkt');
    
    const serviceProfile = marketProfile(process.env.PROJECT_TITLE.toLowerCase());
    const geoJson = parse(serviceProfile.polygon);
    
    let polygon;
    if (geoJson.type.toLowerCase() === 'polygon') {
      polygon = this.turf.polygon(geoJson.coordinates);
    } else if (geoJson.type.toLowerCase() === 'multipolygon') {
      polygon = this.turf.multiPolygon(geoJson.coordinates);
    }
    
    const bbox = this.turf.bbox(polygon);
    const grid = this.turf.pointGrid(bbox, gridSize, { units: 'degrees' });
    
    const pointsInArea = [];
    const pointsOutArea = [];
    
    grid.features.forEach(point => {
      const coords = point.geometry.coordinates;
      const isInside = this.localUserLabel.checkServiceArea(coords[1], coords[0]);
      
      if (isInside) {
        pointsInArea.push(point);
      } else {
        pointsOutArea.push(point);
      }
    });
    
    return {
      totalPoints: grid.features.length,
      pointsInServiceArea: pointsInArea.length,
      pointsOutServiceArea: pointsOutArea.length,
      coveragePercentage: (pointsInArea.length / grid.features.length * 100).toFixed(2),
      boundingBox: bbox,
      serviceAreaPolygon: polygon
    };
  }

  async analyzeUserDistribution() {
    const AuthUser = require('@app/src/models/AuthUser');
    const AuthUserLabel = require('@app/src/models/AuthUserLabel');
    
    const localUsers = await AuthUserLabel.query()
      .where('label_id', 2)
      .count('* as count');
    
    const nonLocalUsers = await AuthUserLabel.query()
      .where('label_id', 3)
      .count('* as count');
    
    const totalUsers = await AuthUser.query().count('* as count');
    
    const localCount = parseInt(localUsers[0].count);
    const nonLocalCount = parseInt(nonLocalUsers[0].count);
    const totalCount = parseInt(totalUsers[0].count);
    const unlabeledCount = totalCount - localCount - nonLocalCount;
    
    return {
      totalUsers: totalCount,
      localUsers: localCount,
      nonLocalUsers: nonLocalCount,
      unlabeledUsers: unlabeledCount,
      percentages: {
        local: ((localCount / totalCount) * 100).toFixed(2),
        nonLocal: ((nonLocalCount / totalCount) * 100).toFixed(2),
        unlabeled: ((unlabeledCount / totalCount) * 100).toFixed(2)
      },
      insights: this.generateInsights(localCount, nonLocalCount, unlabeledCount)
    };
  }

  generateInsights(localCount, nonLocalCount, unlabeledCount) {
    const insights = [];
    
    if (unlabeledCount > localCount + nonLocalCount) {
      insights.push('Majority of users have not been categorized - consider running batch processing');
    }
    
    if (localCount > nonLocalCount * 2) {
      insights.push('Strong local user base - consider local-focused features');
    } else if (nonLocalCount > localCount) {
      insights.push('High visitor/tourist usage - consider visitor-friendly features');
    }
    
    const localRatio = localCount / (localCount + nonLocalCount);
    if (localRatio > 0.8) {
      insights.push('Very high local usage - potential for community features');
    } else if (localRatio < 0.2) {
      insights.push('Primarily visitor usage - focus on tourist amenities');
    }
    
    return insights;
  }
}
```

### Testing and Validation
```javascript
class LocalUserLabelTester {
  constructor() {
    this.localUserLabel = require('@app/src/services/localUserLabel');
  }

  async testServiceAreaBoundaries() {
    // Test points at various locations
    const testPoints = [
      { name: 'Houston Downtown', lat: 29.7604, lng: -95.3698, expected: true },
      { name: 'Houston Airport', lat: 29.9844, lng: -95.3414, expected: true },
      { name: 'Austin', lat: 30.2672, lng: -97.7431, expected: false },
      { name: 'Dallas', lat: 32.7767, lng: -96.7970, expected: false }
    ];
    
    const results = [];
    
    for (const point of testPoints) {
      const isInArea = this.localUserLabel.checkServiceArea(point.lat, point.lng);
      const passed = isInArea === point.expected;
      
      results.push({
        location: point.name,
        coordinates: { lat: point.lat, lng: point.lng },
        expected: point.expected,
        actual: isInArea,
        passed
      });
    }
    
    return {
      totalTests: results.length,
      passed: results.filter(r => r.passed).length,
      failed: results.filter(r => !r.passed).length,
      results
    };
  }

  async testLabelTransitions(testUserId) {
    const transitions = [];
    
    try {
      // Test 1: Set as non-local
      const setNonLocal = await this.localUserLabel.setNonLocalUser(testUserId);
      transitions.push({
        action: 'setNonLocalUser',
        success: setNonLocal,
        timestamp: new Date()
      });
      
      // Test 2: Try to set as non-local again (should fail)
      const setNonLocalAgain = await this.localUserLabel.setNonLocalUser(testUserId);
      transitions.push({
        action: 'setNonLocalUser_duplicate',
        success: setNonLocalAgain,
        expected: false,
        timestamp: new Date()
      });
      
      // Test 3: Switch to local
      const switchToLocal = await this.localUserLabel.switchToLocalUser(testUserId);
      transitions.push({
        action: 'switchToLocalUser',
        success: switchToLocal,
        timestamp: new Date()
      });
      
      // Test 4: Try to switch to local again (should fail)
      const switchToLocalAgain = await this.localUserLabel.switchToLocalUser(testUserId);
      transitions.push({
        action: 'switchToLocalUser_duplicate',
        success: switchToLocalAgain,
        expected: false,
        timestamp: new Date()
      });
      
      return {
        testUserId,
        totalTransitions: transitions.length,
        successful: transitions.filter(t => t.success).length,
        transitions
      };
    } catch (error) {
      return {
        testUserId,
        error: error.message,
        transitions
      };
    }
  }

  async cleanupTestUser(testUserId) {
    const AuthUserLabel = require('@app/src/models/AuthUserLabel');
    
    await AuthUserLabel.query()
      .delete()
      .where('user_id', testUserId)
      .whereIn('label_id', [2, 3]);
    
    console.log(`Cleaned up test labels for user ${testUserId}`);
  }
}
```

## 📊 Output Examples

### Service Area Check Result
```json
{
  "latitude": 29.7604,
  "longitude": -95.3698,
  "inServiceArea": true,
  "location": "Houston Downtown"
}
```

### Label Switch Response
```json
{
  "userId": 12345,
  "action": "switchToLocalUser",
  "success": true,
  "previousLabel": "non-local",
  "newLabel": "local",
  "timestamp": "2024-06-25T14:30:00Z"
}
```

### User Distribution Analysis
```json
{
  "totalUsers": 50000,
  "localUsers": 35000,
  "nonLocalUsers": 8000,
  "unlabeledUsers": 7000,
  "percentages": {
    "local": "70.00",
    "nonLocal": "16.00",
    "unlabeled": "14.00"
  },
  "insights": [
    "Strong local user base - consider local-focused features",
    "Very high local usage - potential for community features"
  ]
}
```

### State Machine Transition
```json
{
  "userId": 12345,
  "previousState": "NonLocalUser",
  "newState": "LocalUser",
  "event": "SWITCH_TO_LOCAL_USER",
  "context": {
    "userId": 12345,
    "lat": 29.7604,
    "lng": -95.3698
  }
}
```

## ⚠️ Important Notes

### Label System Design
- **Mutual Exclusivity:** Users can only have one label (local OR non-local)
- **Label IDs:** Hardcoded as 2 (local) and 3 (non-local)
- **No Default:** Users may have neither label until processed
- **State Persistence:** Labels stored in auth_user_label table

### Geospatial Considerations
- **Coordinate Order:** Turf.js uses [longitude, latitude] order
- **Polygon Types:** Supports both Polygon and MultiPolygon geometries
- **WKT Format:** Service area defined in Well-Known Text format
- **Precision:** Point-in-polygon checks are mathematically precise

### State Machine Integration
- **Event-Driven:** State changes triggered by explicit events
- **Side Effects:** Database updates happen via action handlers
- **Context Data:** Stores user ID and coordinates for reference
- **Final State:** LocalUser is a final state with no transitions out

### Performance Implications
- **Database Queries:** Each check involves 1-2 database queries
- **Geospatial Computation:** Point-in-polygon checks are CPU-intensive
- **Caching Opportunity:** Service area polygon could be cached
- **Batch Processing:** Consider batching for multiple users

### Error Handling
- **Silent Failures:** Some functions return false instead of throwing
- **Logging:** Extensive logging for debugging label transitions
- **Database Errors:** Wrapped in try-catch blocks
- **Sync Function Issues:** switchToLocalUserSync has promise handling issues

### Business Logic
- **One-Way Transitions:** Easy to become local, but no automatic reversion
- **Location Updates:** Requires external triggers to update labels
- **Service Boundaries:** Defined by market profile configuration
- **Feature Gating:** Labels can control feature access and pricing

### Security Considerations
- **User Privacy:** Location data should be handled securely
- **Label Manipulation:** Ensure proper authorization for label changes
- **Service Area:** Polygon data might reveal business strategy
- **Audit Trail:** Consider logging all label changes for compliance

## 🔗 Related File Links

- **User Label Model:** `allrepo/connectsmart/tsp-api/src/models/AuthUserLabel.js`
- **State Machine Service:** `allrepo/connectsmart/tsp-api/src/services/stateMachine.js`
- **Market Profile:** `allrepo/connectsmart/tsp-api/src/services/marketProfile.js`
- **User Model:** `allrepo/connectsmart/tsp-api/src/models/AuthUser.js`

---
*This service provides essential geographic user categorization for location-based features and market segmentation in the TSP platform.*