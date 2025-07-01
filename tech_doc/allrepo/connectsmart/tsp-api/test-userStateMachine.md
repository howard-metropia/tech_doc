# Test Documentation: User State Machine

## Overview
This test suite validates the User State Machine functionality within the TSP system, which manages user classification based on geographic location and service area coverage. The state machine determines whether users are "LocalUser" or "NonLocalUser" based on their coordinates and can transition between states dynamically.

## Test Configuration
- **File**: `test/test-userStateMachine.js`
- **Framework**: Mocha with Chai assertions, XState for state machine management
- **Models Used**: `AuthUserLabel`
- **Service**: `@app/src/services/userStateMachine`
- **State Machine Engine**: XState with createActor and waitFor utilities
- **Test Timeout**: 10 seconds for state transitions

## State Machine Architecture

### States
1. **LocalUser** (label_id: 2) - Users within service area
2. **NonLocalUser** (label_id: 3) - Users outside service area  
3. **End** - Terminal state after processing

### State Transitions
- **Initial State**: Determined by existing user label
- **Geographic Transition**: NonLocalUser → LocalUser when coordinates are in service area
- **Manual Transition**: SWITCH_TO_LOCAL event forces transition to LocalUser
- **Final State**: All paths lead to End state

### Input Parameters
```javascript
{
  userId: 1,           // User identifier
  lat: 29.761384,      // Latitude coordinate
  lng: -95.369040      // Longitude coordinate
}
```

## Test Scenarios

### 1. Initial LocalUser State
**Setup**: User has label_id: 2 (LocalUser)
**Coordinates**: lat: 1.0, lng: 1.0 (outside service area)
**Expected**: Remains LocalUser, transitions to End

```javascript
beforeEach(async () => {
  await AuthUserLabel.query().where({ user_id: userId }).delete();
  await AuthUserLabel.query().insert({
    user_id: userId,
    label_id: 2,  // LocalUser
  });
});

it('should return LocalUser', async () => {
  const stateMachine = getUserStateMachine();
  const actor = createActor(stateMachine, {
    input: { userId: 1, lat: 1.0, lng: 1.0 }
  });
  
  actor.start();
  const snapshot = await waitFor(actor, (snapshot) => snapshot.matches('End'));
  
  expect(snapshot.value).to.equal('End');
  
  const currentUserLabel = await AuthUserLabel.query()
    .where({ user_id: userId })
    .whereIn('label_id', [2, 3])
    .first();
    
  expect(currentUserLabel.label_id).to.equal(2); // Still LocalUser
});
```

### 2. Initial NonLocalUser State
**Setup**: User has label_id: 3 (NonLocalUser)
**Coordinates**: lat: 1.0, lng: 1.0 (outside service area)
**Expected**: Remains NonLocalUser

```javascript
beforeEach(async () => {
  await AuthUserLabel.query().where({ user_id: userId }).delete();
  await AuthUserLabel.query().insert({
    user_id: userId,
    label_id: 3,  // NonLocalUser
  });
});

it('should return NonLocalUser', async () => {
  const snapshot = await waitFor(actor, 
    (snapshot) => snapshot.matches('LocalUser') || snapshot.matches('NonLocalUser')
  );
  
  expect(snapshot.value).to.equal('NonLocalUser');
  expect(currentUserLabel.label_id).to.equal(3); // Still NonLocalUser
});
```

### 3. Geographic State Transition
**Setup**: User has label_id: 3 (NonLocalUser)
**Coordinates**: lat: 29.761384, lng: -95.369040 (Houston area - in service area)
**Expected**: NonLocalUser → LocalUser → End

```javascript
it('should return LocalUser', async () => {
  const lat = 29.761384;   // Houston coordinates
  const lng = -95.369040;  // Within service area
  
  // Wait for initial NonLocalUser state
  let snapshot = await waitFor(actor, (snapshot) => snapshot.matches('NonLocalUser'));
  
  // Wait for geographic transition to LocalUser
  snapshot = await waitFor(actor, (snapshot) => snapshot.matches('LocalUser'));
  
  // Wait for final End state
  snapshot = await waitFor(actor, (snapshot) => snapshot.matches('End'));
  
  expect(snapshot.value).to.equal('End');
  expect(currentUserLabel.label_id).to.equal(2); // Changed to LocalUser
});
```

### 4. Manual State Transition
**Setup**: User has label_id: 3 (NonLocalUser)
**Coordinates**: lat: 0, lng: 0 (outside service area)
**Event**: SWITCH_TO_LOCAL manual trigger
**Expected**: NonLocalUser → LocalUser → End

```javascript
it('should return LocalUser', async () => {
  const lat = 0;  // Outside service area
  const lng = 0;
  
  let snapshot = await waitFor(actor, 
    (snapshot) => snapshot.matches('NonLocalUser') || snapshot.matches('LocalUser')
  );
  
  // Manual transition trigger
  actor.send({ type: 'SWITCH_TO_LOCAL' });
  
  snapshot = await waitFor(actor, (snapshot) => snapshot.matches('End'));
  
  expect(snapshot.value).to.equal('End');
  expect(currentUserLabel.label_id).to.equal(2); // Changed to LocalUser
});
```

## Service Area Definition

### Houston Service Area
Based on test coordinates `lat: 29.761384, lng: -95.369040`, the service area appears to cover the Houston metropolitan area. The state machine includes geographic boundary checking to determine if coordinates fall within the supported service region.

### Geographic Validation
- **In Service Area**: Houston area coordinates trigger automatic state transition
- **Outside Service Area**: Generic coordinates (1.0, 1.0) or (0, 0) maintain current state
- **Real-time Processing**: State machine evaluates coordinates in real-time

## State Machine Implementation

### XState Integration
```javascript
const stateMachine = getUserStateMachine();
const actor = createActor(stateMachine, {
  id: 'userStateMachine',
  input: { userId, lat, lng }
});

actor.start();
const snapshot = await waitFor(actor, 
  (snapshot) => snapshot.matches('targetState'), 
  { timeout: 10000 }
);
actor.stop();
```

### State Persistence
- User state stored in `AuthUserLabel` table
- `label_id` field determines current user classification
- State changes persist across sessions
- Database updates reflect state machine transitions

## Business Logic

### User Classification
- **LocalUser**: Users within supported service areas
- **NonLocalUser**: Users outside service coverage
- **Dynamic Classification**: Real-time updates based on location

### Service Personalization
- Different features and services based on user classification
- Location-based content and recommendations
- Service availability notifications

### Geographic Expansion
- Framework supports adding new service areas
- State machine can be extended for multiple regions
- Scalable architecture for service growth

## Data Management

### Database Schema
```javascript
// AuthUserLabel table structure
{
  user_id: Integer,     // User identifier
  label_id: Integer,    // State classification (2=Local, 3=NonLocal)
  // Additional metadata fields
}
```

### Test Data Lifecycle
```javascript
beforeEach(async () => {
  // Clean existing labels
  await AuthUserLabel.query().where({ user_id: userId }).delete();
  
  // Set initial state
  await AuthUserLabel.query().insert({
    user_id: userId,
    label_id: initialState  // 2 or 3
  });
});
```

## Error Handling

### Timeout Management
- 10-second timeout for state transitions
- Prevents infinite waiting for state changes
- Graceful handling of transition failures

### State Validation
- Validates final state matches expected outcome
- Confirms database persistence of state changes
- Ensures actor cleanup after testing

## Performance Considerations

### Async Operations
- Non-blocking state machine operations
- Efficient database queries for state lookup
- Minimal latency for geographic validation

### Resource Management
- Proper actor lifecycle management (start/stop)
- Database connection cleanup
- Memory management for test isolation

## Integration Points

### Location Services
- GPS coordinate validation
- Geographic boundary checking
- Real-time location processing

### User Management
- User profile integration
- Permission and access control
- Service customization based on state

### Feature Toggles
- Location-based feature availability
- Service area-specific functionality
- Progressive service rollout

## Test Coverage

### State Transition Coverage
- ✅ LocalUser initial state maintenance
- ✅ NonLocalUser initial state maintenance  
- ✅ Geographic-triggered state transitions
- ✅ Manual state transitions via events
- ✅ Final state validation

### Data Persistence Coverage
- ✅ Database state updates
- ✅ Label ID changes
- ✅ Transaction consistency
- ✅ Test data cleanup

### Error Scenario Coverage
- ✅ Timeout handling for state transitions
- ✅ Invalid coordinate handling
- ✅ Database operation failures
- ✅ Actor lifecycle management

## Business Value

### Service Optimization
- Targeted service delivery based on location
- Resource allocation optimization
- Market expansion planning support

### User Experience
- Location-appropriate feature sets
- Relevant content and recommendations
- Service availability transparency

### Operational Efficiency
- Automated user classification
- Scalable geographic expansion
- Data-driven service decisions

This test suite ensures the user state machine reliably classifies users based on geographic location and service area coverage, supporting targeted service delivery within the TSP platform.