# Local User Label Service

## Overview

The Local User Label service manages user classification based on geographic service areas, implementing state machine logic to switch users between local and non-local status with geographic validation.

## Service Information

- **Service Name**: Local User Label
- **File Path**: `/src/services/localUserLabel.js`
- **Type**: User Classification Service
- **Dependencies**: State Machine, Turf.js, WKT Parser

## User Label Types

### Label Classifications
- **Label ID 2**: Local User (within service area)
- **Label ID 3**: Non-Local User (outside service area)

### State Management
- **LocalUser**: Final state for users within service area
- **NonLocalUser**: Initial state for users outside service area
- **Transition**: SWITCH_TO_LOCAL_USER event triggers classification change

## Functions

### switchToLocalUser(userId)

Switches user from non-local to local user status.

**Purpose**: Changes user classification when they enter service area
**Parameters**:
- `userId` (number): User ID to switch to local status
**Returns**: Boolean indicating success/failure

**Process Flow**:
1. Checks if user already has local user label
2. Verifies user has non-local user label
3. Adds local user label and removes non-local label
4. Returns success status

### switchToLocalUserSync(userId)

Synchronous wrapper for local user switching.

**Purpose**: Provides synchronous interface for state machine actions
**Parameters**:
- `userId` (number): User ID to process
**Returns**: Boolean result (may not reflect actual async result)

**Note**: Contains legacy commented code and incomplete synchronous implementation

### getStateMachine(userId)

Creates and configures state machine for user label management.

**Purpose**: Sets up state machine for automated user classification
**Parameters**:
- `userId` (number): User ID for state machine context
**Returns**: State machine actor instance

**State Configuration**:
- **Initial State**: NonLocalUser
- **Final State**: LocalUser
- **Transition**: SWITCH_TO_LOCAL_USER event
- **Action**: updateExternalService calls switchToLocalUserSync

### checkServiceArea(lat, lng)

Validates if coordinates are within service area polygon.

**Purpose**: Geographic validation for user location
**Parameters**:
- `lat` (number): Latitude coordinate
- `lng` (number): Longitude coordinate
**Returns**: Boolean indicating if point is within service area

**Geographic Processing**:
- Creates Turf.js point from coordinates
- Parses service area polygon from WKT format
- Uses boolean point-in-polygon calculation

### setNonLocalUser(userId)

Sets user as non-local if not already classified as local.

**Purpose**: Initial classification for users outside service area
**Parameters**:
- `userId` (number): User ID to classify
**Returns**: Boolean indicating if label was added

## State Machine Configuration

### State Definition
```javascript
{
  id: 'localUserStateMachine',
  initial: 'NonLocalUser',
  context: { userId: null },
  states: {
    LocalUser: { type: 'final' },
    NonLocalUser: {
      on: {
        SWITCH_TO_LOCAL_USER: {
          target: 'LocalUser',
          actions: [{ type: 'updateExternalService' }]
        }
      }
    }
  }
}
```

### Actions
- **updateExternalService**: Executes switchToLocalUserSync when transition occurs

## Service Area Management

### Geographic Data
- **Source**: Market profile service configuration
- **Format**: WKT (Well-Known Text) polygon
- **Processing**: Turf.js geographic calculations
- **Projection**: Uses PROJECT_TITLE environment variable

### Coordinate Validation
- **Input Validation**: Checks for valid lat/lng values
- **Boundary Detection**: Point-in-polygon algorithm
- **Error Handling**: Returns false for invalid coordinates

## Database Operations

### AuthUserLabel Table
- **Label Management**: Inserts and deletes user labels
- **Query Operations**: Finds existing labels by user and label ID
- **Transaction Safety**: Atomic operations for label changes

### Label Logic
- Users cannot have both local and non-local labels simultaneously
- Switching requires removing existing conflicting labels
- Returns false if user already has target label

## Error Handling

### Database Errors
- Comprehensive try-catch blocks
- Detailed error logging with stack traces
- Graceful failure returns

### Geographic Errors
- Validates input coordinates
- Handles parsing errors for WKT data
- Logs invalid coordinate attempts

### State Machine Errors
- Error handling in async/sync bridge
- Logging of state transition failures
- Fallback behavior for failed switches

## Integration Points

### Used By
- User onboarding processes
- Location-based service activation
- Geographic feature enablement
- Service area expansion tracking

### External Dependencies
- **State Machine Service**: State management
- **Market Profile Service**: Service area definition
- **AuthUserLabel Model**: Database operations
- **Turf.js**: Geographic calculations
- **WKT Parser**: Polygon parsing

## Performance Considerations

### Geographic Calculations
- Efficient point-in-polygon algorithms
- Cached polygon parsing
- Minimal coordinate validation overhead

### Database Operations
- Optimized queries by user ID and label ID
- Efficient insert/delete operations
- Minimal transaction overhead

## Security Considerations

- **User Privacy**: Location data handled securely
- **Service Boundaries**: Accurate geographic validation
- **Label Integrity**: Prevents conflicting labels
- **Data Validation**: Validates all input coordinates

## Usage Guidelines

1. **Coordinate Validation**: Always validate lat/lng before processing
2. **State Management**: Use state machine for automated transitions
3. **Error Handling**: Check return values for operation success
4. **Service Areas**: Ensure polygon data is current
5. **Performance**: Cache polygon parsing for frequent operations

## Dependencies

- **State Machine Service**: State management infrastructure
- **Turf.js**: Geographic calculation library
- **WKT Parser**: Well-Known Text format parsing
- **AuthUserLabel Model**: Database ORM model
- **Market Profile Service**: Service area configuration
- **@maas/core/log**: Centralized logging