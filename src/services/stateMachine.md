# TSP API StateMachine Service Documentation

## 🔍 Quick Summary (TL;DR)
The StateMachine service provides a centralized state management system using XState v5 for modeling complex user state transitions and workflow orchestration, with factory pattern for machine creation and global configuration management.

**Keywords:** state-machine | xstate-v5 | workflow-orchestration | user-state-management | configuration-factory | state-transitions | context-management | action-dispatching

**Primary use cases:** Managing user state transitions, orchestrating complex workflows, handling LocalUser vs NonLocalUser states, providing reusable state machine configurations

**Compatibility:** Node.js >= 16.0.0, XState v5 for state machine implementation, factory pattern for machine instantiation, global configuration registry

## ❓ Common Questions Quick Index
- **Q: What state machine library is used?** → XState v5 with createMachine, createActor, and setup functions
- **Q: How are configurations managed?** → Global registry with setStateMachineConfig for reusable patterns
- **Q: What user states exist?** → LocalUser (final state) and NonLocalUser with transition capabilities
- **Q: How are contexts handled?** → Merge input context with machine defaults for initialization
- **Q: What actions are supported?** → Custom actions like updateExternalService with async operation simulation
- **Q: How is state monitoring done?** → Built-in subscription system logs state changes and context

## 📋 Functionality Overview

**Non-technical explanation:** 
Think of this as a **workflow engine** that tracks where users are in different processes and what they can do next. Like a GPS that knows your current location and can guide you through valid route changes, this tracks user status and manages allowed transitions between different states.

**Technical explanation:** 
A sophisticated state management service built on XState v5 that provides centralized configuration for state machines, factory pattern for machine instantiation with context merging, subscription-based state monitoring, and custom action handling for complex workflow orchestration.

**Business value explanation:**
Enables complex user workflow management, provides predictable state transitions for business logic, supports scalable workflow patterns through reusable configurations, ensures consistency in user state handling, and facilitates debugging through comprehensive state logging.

## 🔧 Technical Specifications

- **File:** `allrepo/connectsmart/tsp-api/src/services/stateMachine.js`
- **Language:** JavaScript (ES2020)
- **Framework:** Node.js with XState v5 state machine library
- **Type:** State Management and Workflow Orchestration Service
- **File Size:** ~2.4 KB
- **Complexity Score:** ⭐⭐⭐⭐ (High - Complex state machine patterns and factory management)

**Dependencies:**
- `xstate`: State machine library with createMachine, createActor, fromPromise, setup (**Critical**)
- Global configuration registry system (**Critical**)
- Custom action handlers and context management (**High**)

## 📝 Detailed Code Analysis

### Global Configuration Management

### Configuration Registry
```javascript
const globalStateMachineConfigs = {};
const globalStateMachineOptions = {};

function setStateMachineConfig(key, config, options = {}) {
  globalStateMachineConfigs[key] = config;
  globalStateMachineOptions[key] = options;
}
```
- Centralized registry for reusable state machine configurations
- Separate storage for machine configs and options
- Supports dynamic registration of new machine types

### Factory Pattern Implementation

### getStateMachine Function
**Purpose:** Creates and initializes state machine actors with context merging

```javascript
function getStateMachine(key, input) {
  if (!globalStateMachineConfigs[key]) {
    throw new Error(`State machine config for key "${key}" not found.`);
  }

  let machineConfig = globalStateMachineConfigs[key];
  const machineOptions = globalStateMachineOptions[key] || {};
  
  // Context merging
  if (!machineConfig.context) machineConfig.context = {};
  machineConfig.context = { ...machineConfig.context, ...input };
  
  // Machine creation and actor setup
  const machine = setup(machineOptions).createMachine(machineConfig);
  const actor = createActor(machine);
  
  // State monitoring subscription
  actor.subscribe(async (state) => {
    console.log('State changed:', state.value, state.context);
  });
  
  actor.start();
  return actor;
}
```

**Key Features:**
- **Configuration Validation:** Throws error for missing configurations
- **Context Merging:** Combines default and input contexts for initialization
- **Actor Management:** Creates and starts XState actors with monitoring
- **State Subscription:** Automatic logging of state changes and context updates

### User State Machine Configuration

### UserStateMachine Definition
```javascript
setStateMachineConfig('userStateMachine', {
  id: 'userStateMachine',
  initial: 'LocalUser',
  context: {
    userId: null, // Initial context value
  },
  states: {
    LocalUser: {
      type: 'final', // Terminal state
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
}, {
  actions: {
    updateExternalService: (context, eventType) => {
      console.log(`Calling external service for userId: ${context.userId}, eventType: ${eventType}`);
      new Promise((resolve) => setTimeout(resolve, 1000))
        .then(() => console.log('done')); // Simulate async operation
      console.log('External service call completed');
    },
  },
});
```

### State Definitions

#### LocalUser State
- **Type:** Final state (terminal)
- **Behavior:** End state with no further transitions
- **Usage:** Represents users who have completed onboarding or are fully verified

#### NonLocalUser State
- **Transitions:** Can switch to LocalUser via SWITCH_TO_LOCAL event
- **Actions:** Triggers updateExternalService action during transition
- **Usage:** Represents users requiring verification or additional processing

### Action System

#### updateExternalService Action
**Purpose:** Handles external service calls during state transitions
```javascript
updateExternalService: (context, eventType) => {
  console.log(`Calling external service for userId: ${context.userId}, eventType: ${eventType}`);
  new Promise((resolve) => setTimeout(resolve, 1000))
    .then(() => console.log('done')); // Simulate async operation
  console.log('External service call completed');
}
```
- **Context Access:** Uses userId and other context data
- **Async Simulation:** Demonstrates async operation patterns
- **Logging:** Comprehensive logging for debugging and monitoring

## 🚀 Usage Methods

### Basic State Machine Usage
```javascript
const stateMachineService = require('@app/src/services/stateMachine');

// Create user state machine with context
const userMachine = stateMachineService.getStateMachine('userStateMachine', {
  userId: 12345
});

// Send events to trigger state transitions
userMachine.send({ type: 'SWITCH_TO_LOCAL' });

// Get current state
console.log('Current state:', userMachine.getSnapshot().value);
console.log('Current context:', userMachine.getSnapshot().context);
```

### Advanced State Machine Manager
```javascript
class WorkflowManager {
  constructor() {
    this.stateMachineService = require('@app/src/services/stateMachine');
    this.activeMachines = new Map();
  }

  createUserWorkflow(userId, initialState = 'NonLocalUser') {
    try {
      // Create machine with user context
      const machine = this.stateMachineService.getStateMachine('userStateMachine', {
        userId,
        createdAt: new Date().toISOString()
      });

      // Store active machine for later reference
      this.activeMachines.set(userId, machine);

      // Add custom subscription for business logic
      machine.subscribe((state) => {
        this.handleStateChange(userId, state);
      });

      return {
        success: true,
        userId,
        initialState: machine.getSnapshot().value,
        context: machine.getSnapshot().context
      };
    } catch (error) {
      console.error('Error creating user workflow:', error);
      return {
        success: false,
        userId,
        error: error.message
      };
    }
  }

  handleStateChange(userId, state) {
    console.log(`User ${userId} state changed to:`, state.value);
    
    // Business logic based on state changes
    switch (state.value) {
      case 'LocalUser':
        this.onUserBecameLocal(userId, state.context);
        break;
      case 'NonLocalUser':
        this.onUserBecameNonLocal(userId, state.context);
        break;
      default:
        console.log(`Unhandled state: ${state.value}`);
    }
  }

  onUserBecameLocal(userId, context) {
    console.log(`User ${userId} completed local verification process`);
    // Trigger welcome email, update permissions, etc.
    this.sendWelcomeNotification(userId);
    this.updateUserPermissions(userId, 'local');
  }

  onUserBecameNonLocal(userId, context) {
    console.log(`User ${userId} requires additional verification`);
    // Trigger verification emails, restrict access, etc.
    this.requestAdditionalVerification(userId);
    this.updateUserPermissions(userId, 'restricted');
  }

  triggerUserTransition(userId, eventType) {
    const machine = this.activeMachines.get(userId);
    
    if (!machine) {
      return {
        success: false,
        error: `No active workflow found for user ${userId}`
      };
    }

    try {
      machine.send({ type: eventType });
      const newState = machine.getSnapshot();
      
      return {
        success: true,
        userId,
        eventType,
        newState: newState.value,
        context: newState.context
      };
    } catch (error) {
      console.error('Error triggering transition:', error);
      return {
        success: false,
        userId,
        eventType,
        error: error.message
      };
    }
  }

  getUserState(userId) {
    const machine = this.activeMachines.get(userId);
    
    if (!machine) {
      return {
        exists: false,
        userId
      };
    }

    const snapshot = machine.getSnapshot();
    return {
      exists: true,
      userId,
      currentState: snapshot.value,
      context: snapshot.context,
      canTransition: Object.keys(snapshot.nextEvents || {}).length > 0,
      availableEvents: snapshot.nextEvents || []
    };
  }

  async sendWelcomeNotification(userId) {
    // Simulate welcome notification
    console.log(`Sending welcome notification to user ${userId}`);
  }

  async updateUserPermissions(userId, level) {
    // Simulate permission update
    console.log(`Updating user ${userId} permissions to level: ${level}`);
  }

  async requestAdditionalVerification(userId) {
    // Simulate verification request
    console.log(`Requesting additional verification for user ${userId}`);
  }

  getWorkflowSummary() {
    const summary = {
      totalActiveWorkflows: this.activeMachines.size,
      stateDistribution: {},
      workflows: []
    };

    this.activeMachines.forEach((machine, userId) => {
      const state = machine.getSnapshot();
      
      // Count state distribution
      if (!summary.stateDistribution[state.value]) {
        summary.stateDistribution[state.value] = 0;
      }
      summary.stateDistribution[state.value]++;

      // Add workflow details
      summary.workflows.push({
        userId,
        currentState: state.value,
        context: state.context
      });
    });

    return summary;
  }
}

// Usage
const workflowManager = new WorkflowManager();

// Create user workflow
const result = await workflowManager.createUserWorkflow(12345);
console.log('Workflow creation result:', result);

// Trigger state transition
const transition = await workflowManager.triggerUserTransition(12345, 'SWITCH_TO_LOCAL');
console.log('Transition result:', transition);

// Get current user state
const userState = workflowManager.getUserState(12345);
console.log('User state:', userState);

// Get workflow summary
const summary = workflowManager.getWorkflowSummary();
console.log('Workflow summary:', summary);
```

### Custom State Machine Configuration
```javascript
const stateMachineService = require('@app/src/services/stateMachine');

// Define custom onboarding state machine
stateMachineService.setStateMachineConfig('onboardingFlow', {
  id: 'onboardingFlow',
  initial: 'registration',
  context: {
    userId: null,
    completedSteps: [],
    currentStep: 'registration'
  },
  states: {
    registration: {
      on: {
        COMPLETE_REGISTRATION: {
          target: 'verification',
          actions: ['trackStep']
        }
      }
    },
    verification: {
      on: {
        VERIFY_EMAIL: {
          target: 'profileSetup',
          actions: ['trackStep']
        },
        FAIL_VERIFICATION: {
          target: 'registration',
          actions: ['resetFlow']
        }
      }
    },
    profileSetup: {
      on: {
        COMPLETE_PROFILE: {
          target: 'completed',
          actions: ['trackStep', 'notifyCompletion']
        }
      }
    },
    completed: {
      type: 'final'
    }
  }
}, {
  actions: {
    trackStep: (context, event) => {
      console.log(`Completed step: ${context.currentStep} for user ${context.userId}`);
      context.completedSteps.push(context.currentStep);
    },
    resetFlow: (context, event) => {
      console.log(`Resetting onboarding flow for user ${context.userId}`);
      context.completedSteps = [];
    },
    notifyCompletion: (context, event) => {
      console.log(`Onboarding completed for user ${context.userId}`);
      // Send completion notification
    }
  }
});

// Use custom onboarding machine
const onboardingMachine = stateMachineService.getStateMachine('onboardingFlow', {
  userId: 67890
});

// Step through onboarding process
onboardingMachine.send({ type: 'COMPLETE_REGISTRATION' });
onboardingMachine.send({ type: 'VERIFY_EMAIL' });
onboardingMachine.send({ type: 'COMPLETE_PROFILE' });
```

## 📊 Output Examples

### State Machine Creation
```javascript
// Console output from getStateMachine
"State changed: LocalUser { userId: 12345, createdAt: '2024-06-25T14:30:00.000Z' }"

// Machine creation result
{
  success: true,
  userId: 12345,
  initialState: "LocalUser",
  context: {
    userId: 12345,
    createdAt: "2024-06-25T14:30:00.000Z"
  }
}
```

### State Transition Response
```javascript
// Action execution output
"Calling external service for userId: 12345, eventType: { type: 'SWITCH_TO_LOCAL' }"
"External service call completed"
"done"

// Transition result
{
  success: true,
  userId: 12345,
  eventType: "SWITCH_TO_LOCAL",
  newState: "LocalUser",
  context: {
    userId: 12345,
    createdAt: "2024-06-25T14:30:00.000Z"
  }
}
```

### User State Information
```javascript
{
  exists: true,
  userId: 12345,
  currentState: "NonLocalUser",
  context: {
    userId: 12345,
    createdAt: "2024-06-25T14:30:00.000Z"
  },
  canTransition: true,
  availableEvents: ["SWITCH_TO_LOCAL"]
}
```

### Workflow Summary
```javascript
{
  totalActiveWorkflows: 3,
  stateDistribution: {
    "LocalUser": 1,
    "NonLocalUser": 2
  },
  workflows: [
    {
      userId: 12345,
      currentState: "LocalUser",
      context: { userId: 12345, createdAt: "2024-06-25T14:30:00.000Z" }
    },
    {
      userId: 67890,
      currentState: "NonLocalUser",
      context: { userId: 67890, createdAt: "2024-06-25T14:35:00.000Z" }
    }
  ]
}
```

## ⚠️ Important Notes

### XState v5 Integration
- **Modern API:** Uses XState v5 setup(), createMachine(), and createActor() functions
- **Actor Pattern:** State machines are instantiated as actors for independent execution
- **Subscription System:** Built-in state change monitoring and logging
- **Context Management:** Sophisticated context merging and initialization

### Configuration Management
- **Global Registry:** Centralized storage for reusable state machine configurations
- **Factory Pattern:** Dynamic machine creation with context injection
- **Error Handling:** Validation for missing configurations with descriptive errors
- **Options Support:** Separate storage for machine options and configurations

### State Design Patterns
- **Final States:** LocalUser as terminal state for completed workflows
- **Event-Driven Transitions:** SWITCH_TO_LOCAL event triggers state changes
- **Action Integration:** Custom actions executed during state transitions
- **Context Preservation:** User data maintained throughout state lifecycle

### Performance and Scalability
- **Memory Management:** Active machines stored in registry for reuse
- **Subscription Efficiency:** Built-in state change monitoring without polling
- **Configuration Reuse:** Global configs prevent redundant machine definitions
- **Error Isolation:** Individual machine failures don't affect global registry

## 🔗 Related File Links

- **User State Machine:** `allrepo/connectsmart/tsp-api/src/services/userStateMachine.js`
- **XState Documentation:** External XState v5 library documentation
- **State Management Controllers:** Controllers that interact with state machines

---
*This service provides sophisticated state management and workflow orchestration using XState v5 for complex user state transitions in the TSP platform.*