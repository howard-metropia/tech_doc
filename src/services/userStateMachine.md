# User State Machine Service Documentation

## 🔍 Quick Summary (TL;DR)

**Purpose:** State machine service that automatically manages user classification (Local vs Non-Local) based on geographic location, ensuring users receive appropriate services and features based on their location relative to the service area.

**Keywords:** user state machine | xstate | geolocation | service area | local user | non-local user | geographic validation | location-based services | state management | user classification | geofencing | turf.js | WKT polygon | market profile

**Primary Use Cases:**
- Automatically classify new users based on their current location
- Transition users between Local/Non-Local status when they move in/out of service area
- Maintain user location status persistence in database
- Enable location-based feature availability and service restrictions

**Compatibility:** Node.js 14+ | XState v5 | Koa.js framework | MySQL/MariaDB

## ❓ Common Questions Quick Index

1. **Q: What determines if a user is Local or Non-Local?** → [See Functionality Overview](#functionality-overview)
2. **Q: How do I check a user's current location status?** → [See Usage Methods](#usage-methods)
3. **Q: What happens when a user moves from inside to outside the service area?** → [See Detailed Code Analysis](#detailed-code-analysis)
4. **Q: How to troubleshoot "user not updating location status" issues?** → [See Important Notes](#important-notes)
5. **Q: What are the label_id values and their meanings?** → [See Technical Specifications](#technical-specifications)
6. **Q: How does the state machine handle concurrent location updates?** → [See Performance & Scaling](#output-examples)
7. **Q: What if the service area polygon is invalid?** → [See Error Handling](#important-notes)
8. **Q: How to add custom logic for user classification?** → [See Improvement Suggestions](#improvement-suggestions)
9. **Q: Can I manually override a user's location status?** → [See Usage Methods](#usage-methods)
10. **Q: What database tables are involved?** → [See Technical Specifications](#technical-specifications)

## 📋 Functionality Overview

### Non-technical Explanation
Think of this service as a **digital bouncer** at a geographic club. Just like a bouncer checks IDs to determine who can enter the VIP area, this service checks user locations to determine who gets "Local" privileges. It's also like a **smart thermostat** that automatically adjusts based on whether you're home or away - the system automatically adjusts user privileges based on their location.

### Technical Explanation
This service implements an XState v5 finite state machine that manages user location classification. It uses Turf.js for geometric calculations to determine if a user's GPS coordinates fall within a predefined service area polygon (defined in WKT format). The state machine pattern ensures consistent state transitions and handles asynchronous database operations gracefully.

### Business Value
- **Automated user segmentation:** No manual intervention needed for user classification
- **Location-based features:** Enable/disable features based on user proximity
- **Compliance:** Meet geographic service restrictions and regulations
- **Resource optimization:** Allocate services efficiently based on user location

### System Context
This service integrates with the TSP API's authentication system, working alongside user registration and location tracking services. It's triggered during user sessions to ensure accurate location-based service delivery.

## 🔧 Technical Specifications

**File Information:**
- **Path:** `/allrepo/connectsmart/tsp-api/src/services/userStateMachine.js`
- **Type:** Service Module (State Machine)
- **Language:** JavaScript (ES6+)
- **Size:** ~160 lines
- **Complexity:** Medium (Cyclomatic Complexity: 8)

**Dependencies:**
| Package | Version | Purpose | Criticality |
|---------|---------|---------|-------------|
| xstate | ^5.x | State machine implementation | Critical |
| @turf/turf | Latest | Geospatial calculations | Critical |
| wkt | Latest | Parse WKT polygon strings | Critical |
| @maas/core/log | Internal | Logging infrastructure | Medium |
| Objection.js | Via models | Database ORM | Critical |

**Database Tables:**
- `auth_user_labels`: Stores user classification (label_id: 2=Local, 3=Non-Local)
- `user_labels`: Label definitions reference table

**Environment Variables:**
- `PROJECT_TITLE`: Project identifier for market profile lookup

**Configuration:**
- Market profile polygon defined in `marketProfile.polygon` (WKT format)

## 📝 Detailed Code Analysis

### Main Components

1. **getUserLabel(userId)**
   - Retrieves current user classification from database
   - Returns: 'SWITCH_TO_LOCAL' or 'SWITCH_TO_NON_LOCAL'
   - Creates Non-Local label if none exists (default behavior)

2. **setLocalUser(userId) / setNonLocalUser(userId)**
   - Database operations to update user labels
   - Handles label transitions with proper cleanup
   - Prevents duplicate labels

3. **checkServiceArea(lat, lng)**
   - Geometric validation using Turf.js
   - Converts WKT polygon to GeoJSON for calculation
   - Returns boolean indicating if point is inside service area

4. **getUserStateMachine()**
   - XState v5 machine factory
   - States: initial → LocalUser/NonLocalUser → End
   - Guards: nextStateLocal, nextStateNonLocal
   - Context: userId, lat, lng

### State Flow
```
initial (fetch current label)
  ├─→ LocalUser (if label_id=2)
  │     └─→ End
  └─→ NonLocalUser (if label_id=3)
        ├─→ Check location against service area
        └─→ LocalUser (if inside) → End
```

### Error Handling
- Database queries use async/await with implicit error propagation
- XState handles promise rejections in invoke actors
- No explicit try-catch blocks (relies on caller error handling)

## 🚀 Usage Methods

### Basic Integration
```javascript
const { getUserStateMachine } = require('./services/userStateMachine');
const { createActor } = require('xstate');

// Create and start the state machine
const machine = getUserStateMachine();
const actor = createActor(machine, {
  input: {
    userId: 12345,
    lat: 33.4484,
    lng: -112.0740
  }
});

actor.start();
actor.subscribe((state) => {
  console.log('Current state:', state.value);
});
```

### Manual Status Check
```javascript
// Direct database query for current status
const userLabel = await AuthUserLabel.query()
  .whereIn('label_id', [2, 3])
  .where('user_id', userId)
  .first();

const isLocal = userLabel?.label_id === 2;
```

### Environment Configuration
```bash
# Development
PROJECT_TITLE=phoenix npm run dev

# Production
PROJECT_TITLE=dallas npm run prod
```

## 📊 Output Examples

### Successful Classification
```
[checkServiceArea] lat: 33.4484, lng: -112.0740, isInServiceArea: true
[getUserStateMachine] Start: {"userId":12345,"lat":33.4484,"lng":-112.0740}
[getUserStateMachine] nextState: SWITCH_TO_LOCAL
[getUserStateMachine] LocalUser: {"lat":33.4484,"lng":-112.0740,"userId":12345}
```

### User Outside Service Area
```
[checkServiceArea] lat: 40.7128, lng: -74.0060, isInServiceArea: false
[getUserStateMachine] Not in service area
[getUserStateMachine] nextState: SWITCH_TO_NON_LOCAL
```

### Database State After Classification
```sql
-- Local User (label_id = 2)
SELECT * FROM auth_user_labels WHERE user_id = 12345;
+----+---------+----------+
| id | user_id | label_id |
+----+---------+----------+
| 1  | 12345   | 2        |
+----+---------+----------+
```

## ⚠️ Important Notes

### Security Considerations
- No direct user input validation for coordinates (trust upstream validation)
- Database operations use parameterized queries (SQL injection safe)
- No PII logging in console statements

### Permission Requirements
- Read/write access to `auth_user_labels` table
- Access to market profile configuration

### Common Troubleshooting

**Issue: User stuck in wrong classification**
- Check if coordinates are valid numbers
- Verify market profile polygon is properly formatted WKT
- Ensure database transactions are committing

**Issue: State machine not transitioning**
- Check XState actor is properly started
- Verify promises are resolving in invoke functions
- Check for database connection issues

### Performance Considerations
- Point-in-polygon calculation is O(n) where n = polygon vertices
- Database queries are indexed on user_id
- Consider caching for high-frequency checks

## 🔗 Related File Links

**Dependencies:**
- `/src/models/AuthUserLabel.js` - User label model
- `/src/models/UserLabel.js` - Label definitions
- `/src/services/marketProfile.js` - Market configuration

**Consumers:**
- User registration controllers
- Location update services
- Session management middleware

**Tests:**
- `/test/services/userStateMachine.test.js` (if exists)

## 📈 Use Cases

### New User Registration
1. User signs up with location permissions
2. State machine classifies based on current location
3. Appropriate features enabled/disabled

### User Relocation
1. Non-local user travels into service area
2. Location update triggers state machine
3. User gains access to local-only features

### Compliance Scenarios
- Restrict certain services to local users only
- Track user distribution for reporting
- Enforce geographic service boundaries

### Anti-patterns
- Don't manually modify label_id without state machine
- Avoid frequent re-classification (implement cooldown)
- Don't assume synchronous state transitions

## 🛠️ Improvement Suggestions

1. **Add Explicit Error Handling** (Priority: High, Effort: Low)
   - Wrap database operations in try-catch
   - Add specific error types for better debugging

2. **Implement Caching** (Priority: Medium, Effort: Medium)
   - Cache service area polygon parsing
   - Cache user labels with TTL

3. **Add Transition History** (Priority: Low, Effort: Medium)
   - Track when users change classification
   - Enable analytics on user movement patterns

4. **Performance Monitoring** (Priority: Medium, Effort: Low)
   - Add timing metrics for state transitions
   - Monitor database query performance

## 🏷️ Document Tags

**Keywords:** xstate | state-machine | geolocation | user-classification | local-user | non-local-user | turf.js | geofencing | location-services | wkt-polygon | market-profile | auth-user-labels | geographic-validation | service-area | user-segmentation

**Technical Tags:** #state-machine #xstate-v5 #geospatial #location-based-services #user-management #tsp-api

**Target Roles:** 
- Backend Developer (Mid-Senior level)
- DevOps Engineer (Location services)
- Product Manager (User segmentation features)

**Difficulty Level:** ⭐⭐⭐ (Medium - Requires understanding of state machines and geospatial concepts)

**Maintenance Level:** Medium (Occasional updates for new markets or classification rules)

**Business Criticality:** High (Core user segmentation affects feature availability)

**Related Topics:** Authentication | User Management | Geospatial Services | State Management | Location-Based Features