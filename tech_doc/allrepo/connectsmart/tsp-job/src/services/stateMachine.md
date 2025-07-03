# TSP Job Service: stateMachine.js

## Quick Summary

The `stateMachine.js` service provides a state management framework using XState v5 for managing complex business logic workflows within the ConnectSmart platform. It implements a factory pattern for state machine creation, supports configuration-based machine definitions, and includes a pre-configured user state machine for handling local vs non-local user transitions with external service integration.

## Technical Analysis

### Core Architecture

The service implements a sophisticated state management system using XState v5 with the following components:

- **Configuration Management**: Global storage for state machine configurations and options
- **Factory Pattern**: Dynamic state machine creation based on registered configurations
- **Actor Model**: XState v5 actor-based state management with subscription support
- **Async Action Support**: Promise-based actions for external service integration
- **Context Management**: Flexible context passing and merging capabilities

### Key Functions

#### setStateMachineConfig(key, config, options)
Registers state machine configurations globally:
```javascript
function setStateMachineConfig(key, config, options = {}) {
  globalStateMachineConfigs[key] = config;
  globalStateMachineOptions[key] = options;
}
```

#### getStateMachine(key, input)
Factory function for creating and starting state machine actors:
```javascript
function getStateMachine(key, input) {
  if (!globalStateMachineConfigs[key]) {
    throw new Error(`State machine config for key "${key}" not found.`);
  }

  let machineConfig = globalStateMachineConfigs[key];
  const machineOptions = globalStateMachineOptions[key] || {};
  
  // Merge input with existing context
  if (!machineConfig.context) machineConfig.context = {};
  machineConfig.context = { ...machineConfig.context, ...input };
  
  // Create machine using setup function
  const machine = setup(machineOptions).createMachine(machineConfig);
  const actor = createActor(machine);
  
  // Subscribe to state changes
  actor.subscribe(async (state) => {
    console.log('State changed:', state.value, state.context);
  });
  
  actor.start();
  return actor;
}
```

### Pre-configured State Machines

#### User State Machine
Handles local vs non-local user state transitions:
```javascript
setStateMachineConfig('userStateMachine', {
  id: 'userStateMachine',
  initial: 'LocalUser',
  context: {
    userId: null, // Initial context value
  },
  states: {
    LocalUser: {
      type: 'final',
    },
    NonLocalUser: {
      on: {
        SWITCH_TO_LOCAL: {
          target: 'LocalUser',
          actions: [
            { type: 'updateExternalService' },
          ]
        },
      },
    },
  },
});
```

#### Action Implementations
Asynchronous action handlers for external service integration:
```javascript
{
  actions: {
    updateExternalService: (context, eventType) => {
      console.log(`Calling external service for userId: ${context.userId}, eventType: ${eventType}`);
      new Promise((resolve) => setTimeout(resolve, 1000))
        .then(() => console.log('done')); // Simulate async operation
      console.log('External service call completed');
    },
  },
}
```

### XState v5 Integration

The service leverages XState v5 features:

- **setup()**: Modern XState v5 machine configuration
- **createActor()**: Actor-based state management
- **fromPromise()**: Promise-based async state handling
- **createMachine()**: State machine definition

### State Management Patterns

#### Context Merging
Dynamic context injection at machine creation:
```javascript
// Existing context
machineConfig.context = { userId: null };

// Input context
const input = { userId: 12345, userType: 'premium' };

// Merged context
machineConfig.context = { ...machineConfig.context, ...input };
// Result: { userId: 12345, userType: 'premium' }
```

#### State Subscription
Real-time state change monitoring:
```javascript
actor.subscribe(async (state) => {
  console.log('State changed:', state.value, state.context);
  // Can trigger additional business logic
  // Can log state changes for debugging
  // Can update external systems
});
```

## Usage/Integration

### Basic State Machine Creation

```javascript
const { getStateMachine } = require('./stateMachine');

// Create user state machine with context
const userActor = getStateMachine('userStateMachine', {
  userId: 12345,
  userName: 'john.doe@example.com'
});

// Send events to trigger transitions
userActor.send({ type: 'SWITCH_TO_LOCAL' });
```

### Custom State Machine Registration

```javascript
const { setStateMachineConfig, getStateMachine } = require('./stateMachine');

// Define a custom carpool state machine
setStateMachineConfig('carpoolStateMachine', {
  id: 'carpoolStateMachine',
  initial: 'searching',
  context: {
    reservationId: null,
    driverId: null,
    passengerId: null,
  },
  states: {
    searching: {
      on: {
        MATCH_FOUND: 'matched',
        TIMEOUT: 'expired'
      }
    },
    matched: {
      on: {
        ACCEPT_INVITATION: 'accepted',
        REJECT_INVITATION: 'searching'
      }
    },
    accepted: {
      on: {
        START_TRIP: 'in_progress',
        CANCEL: 'canceled'
      }
    },
    in_progress: {
      on: {
        END_TRIP: 'completed'
      }
    },
    completed: {
      type: 'final'
    },
    expired: {
      type: 'final'
    },
    canceled: {
      type: 'final'
    }
  }
}, {
  actions: {
    notifyUsers: (context, event) => {
      console.log(`Notifying users for reservation ${context.reservationId}`);
      // External notification logic
    },
    processPayment: (context, event) => {
      console.log(`Processing payment for trip ${context.tripId}`);
      // Payment processing logic
    }
  }
});

// Use the custom state machine
const carpoolActor = getStateMachine('carpoolStateMachine', {
  reservationId: 67890,
  driverId: 12345,
  passengerId: 54321
});
```

### Job Integration

State machines can be integrated with job processing workflows:

```javascript
// Job: Process carpool matching
async function processCarpoolMatching(reservationId) {
  const carpoolActor = getStateMachine('carpoolStateMachine', {
    reservationId: reservationId
  });
  
  // Simulate matching process
  setTimeout(() => {
    carpoolActor.send({ type: 'MATCH_FOUND', matchId: 98765 });
  }, 5000);
  
  // Listen for state changes
  carpoolActor.subscribe((state) => {
    if (state.matches('completed')) {
      console.log('Carpool completed successfully');
      // Trigger cleanup jobs
    } else if (state.matches('expired')) {
      console.log('Carpool matching expired');
      // Trigger retry or notification jobs
    }
  });
}
```

## Dependencies

### External Packages
- `xstate`: State management library (v5) for complex workflow orchestration

### XState v5 Features Used
- `createMachine`: State machine definition
- `createActor`: Actor creation and management
- `fromPromise`: Promise-based state handling
- `setup`: Modern machine configuration approach

## Code Examples

### Simple State Machine Usage
```javascript
const stateMachine = require('./stateMachine');

// Create and start a user state machine
const userActor = stateMachine.getStateMachine('userStateMachine', {
  userId: 12345
});

// Check current state
console.log('Current state:', userActor.getSnapshot().value);

// Send transition event
userActor.send({ type: 'SWITCH_TO_LOCAL' });

// State will transition to 'LocalUser' and trigger updateExternalService action
```

### Complex Workflow Example
```javascript
// Define a trip processing state machine
stateMachine.setStateMachineConfig('tripProcessingMachine', {
  id: 'tripProcessing',
  initial: 'validating',
  context: {
    tripId: null,
    userId: null,
    validationErrors: []
  },
  states: {
    validating: {
      on: {
        VALIDATION_SUCCESS: 'processing',
        VALIDATION_FAILED: 'failed'
      }
    },
    processing: {
      on: {
        PROCESSING_COMPLETE: 'completed',
        PROCESSING_ERROR: 'failed'
      }
    },
    completed: {
      type: 'final'
    },
    failed: {
      on: {
        RETRY: 'validating'
      }
    }
  }
}, {
  actions: {
    validateTrip: async (context, event) => {
      console.log(`Validating trip ${context.tripId}`);
      // Validation logic
    },
    processTrip: async (context, event) => {
      console.log(`Processing trip ${context.tripId}`);
      // Processing logic
    },
    handleError: (context, event) => {
      console.log(`Error processing trip ${context.tripId}:`, event.error);
      // Error handling logic
    }
  }
});

// Use the state machine
const tripActor = stateMachine.getStateMachine('tripProcessingMachine', {
  tripId: 12345,
  userId: 67890
});

// Simulate workflow
tripActor.send({ type: 'VALIDATION_SUCCESS' });
setTimeout(() => {
  tripActor.send({ type: 'PROCESSING_COMPLETE' });
}, 2000);
```

### State Machine Monitoring
```javascript
// Monitor state machine execution
const actor = stateMachine.getStateMachine('userStateMachine', {
  userId: 12345
});

// Subscribe to all state changes
const subscription = actor.subscribe({
  next: (state) => {
    console.log('State:', state.value);
    console.log('Context:', state.context);
    console.log('Can transition to:', state.nextEvents);
  },
  error: (error) => {
    console.error('State machine error:', error);
  },
  complete: () => {
    console.log('State machine completed');
  }
});

// Clean up subscription when done
// subscription.unsubscribe();
```

### Error Handling
```javascript
try {
  // This will throw if the state machine config doesn't exist
  const actor = stateMachine.getStateMachine('nonexistentMachine', {});
} catch (error) {
  console.error('Error creating state machine:', error.message);
  // Handle missing configuration
}

// Proper error handling
if (stateMachine.globalStateMachineConfigs['myMachine']) {
  const actor = stateMachine.getStateMachine('myMachine', {});
} else {
  console.warn('State machine configuration not found');
}
```

The stateMachine service provides a robust foundation for managing complex business workflows in the ConnectSmart platform, enabling clear state management, async operation handling, and maintainable business logic organization.