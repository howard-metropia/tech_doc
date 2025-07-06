# Trip Reservation Constants - Transportation Mode and Status Definitions

## 🔍 Quick Summary (TL;DR)
**Comprehensive constants definition file containing transportation modes, reservation statuses, carpool states, and business rules for the MaaS platform's trip reservation system.** Provides standardized enumeration for all transportation operations including driving, transit, walking, biking, carpooling, and complex multi-modal scenarios.

**Core functionality:** Transportation mode constants | Reservation status lifecycle | Carpool role definitions | Real-time status tracking | Escrow activity types | Trip completion states
**Primary use cases:** Mode validation, status management, business logic consistency, carpool coordination, payment processing, operational tracking
**Compatibility:** Python 2.7+, Web2py framework, multi-modal transportation systems

## ❓ Common Questions Quick Index
- **Q: What transportation modes are supported?** → See [Technical Specifications](#technical-specifications)
- **Q: How many reservation statuses exist?** → See [Output Examples](#output-examples)
- **Q: What's the difference between DUO and INSTANT_DUO?** → See [Detailed Code Analysis](#detailed-code-analysis)
- **Q: How does reservation status lifecycle work?** → See [Usage Methods](#usage-methods)
- **Q: What are escrow activity types for?** → See [Functionality Overview](#functionality-overview)
- **Q: How to validate transportation modes?** → See [Important Notes](#important-notes)
- **Q: What carpool real-time statuses exist?** → See [Use Cases](#use-cases)
- **Q: How to extend transportation modes?** → See [Improvement Suggestions](#improvement-suggestions)

## 📋 Functionality Overview
**Non-technical explanation:** Think of this as the "transportation dictionary" for a mobility platform. Like how traffic signs have standard meanings everywhere, this file defines what each transportation method means (car, bus, walking, carpooling) and what each status means (searching, matched, completed). It ensures everyone - the app, the servers, and the business logic - speaks the same language about transportation.

**Technical explanation:** Enumeration constants module implementing comprehensive transportation taxonomy, reservation lifecycle management, and carpool coordination states. Provides centralized definition of business rules, status transitions, and operational states for multi-modal transportation platform.

**Business value:** Ensures consistent transportation operations across all platform components, enables reliable carpool coordination and payment processing, provides clear operational states for business intelligence, and supports regulatory compliance through standardized categorization.

**System context:** Foundational configuration layer used by all transportation-related modules, APIs, mobile applications, and analytics systems to maintain consistent transportation mode identification and operational state management.

## 🔧 Technical Specifications
- **File:** `applications/portal/modules/trip_reservation/define.py`
- **Language:** Python 2.7+
- **Type:** Constants and enumeration definitions
- **Size:** ~111 lines
- **Complexity:** ⭐⭐⭐ (Medium - comprehensive transportation domain coverage)

**Transportation Mode Categories:**
1. **Individual Modes** (1-7): Personal transportation options
2. **Shared Modes** (100-101): Carpool and shared mobility
3. **Mode Mapping**: Bidirectional string-integer conversion dictionary

**Reservation Status Lifecycle (11 states):**
- Planning phase: NONE (0) → SEARCHING (1) → CHOOSING (2)
- Coordination phase: PENDING (3) → SUGGESTION (4) → ACCEPTED (5)
- Cancellation states: REPEALED (6) → REPEALED_CONFLICT (7)
- Execution phase: MATCHED (11) → RESERVED (50) → STARTED (60)
- Completion states: CANCELED (51-53)

**Carpool-Specific Systems:**
- **Role Definitions**: Driver (1) vs Passenger (2)
- **Real-time Status**: 19 detailed carpool coordination states
- **Escrow Activities**: 29 payment and transaction activity types
- **Trip Completion**: 3 different trip ending scenarios

## 📝 Detailed Code Analysis
**Transportation Mode Structure:**
```python
# Individual transportation modes
DRIVING = 1           # Personal vehicle
PUBLIC_TRANSIT = 2    # Bus, train, subway
WALKING = 3          # Pedestrian
BIKING = 4           # Bicycle, e-bike
INTERMODAL = 5       # Multi-modal trips
TRUCKING = 6         # Commercial/freight
PARK_AND_RIDE = 7    # Combined parking + transit

# Shared mobility modes  
DUO = 100            # Standard carpool
INSTANT_DUO = 101    # Real-time carpool matching
```

**Bidirectional Mode Mapping:**
```python
TRAVEL_MODES = {
    # String to integer mapping
    'driving': DRIVING,
    'public_transit': PUBLIC_TRANSIT,
    'duo': DUO,
    
    # Integer to string mapping
    DRIVING: 'driving',
    PUBLIC_TRANSIT: 'public_transit', 
    DUO: 'duo',
    # ... complete bidirectional mapping
}
```

**Reservation Status Lifecycle:**
```python
# Initial planning states
RESERVATION_STATUS_NONE = 0           # Draft or no request
RESERVATION_STATUS_SEARCHING = 1      # Actively searching for matches
RESERVATION_STATUS_CHOOSING = 2       # Evaluating options
RESERVATION_STATUS_PENDING = 3        # Waiting for confirmation

# Coordination states  
RESERVATION_STATUS_SUGGESTION = 4     # System suggestion
RESERVATION_STATUS_ACCEPTED = 5       # Mutual acceptance
RESERVATION_STATUS_MATCHED = 11       # Successfully matched

# Execution states
RESERVATION_STATUS_RESERVED = 50      # Confirmed reservation
RESERVATION_STATUS_STARTED = 60       # Trip in progress

# Cancellation handling
RESERVATION_STATUS_CANCELED = 51              # General cancellation
RESERVATION_STATUS_CANCELED_INACTION = 52     # Cancelled by initiator
RESERVATION_STATUS_CANCELED_PASSIVE = 53      # Cancelled by partner
```

**Carpool Real-time Coordination:**
```python
# Core carpool workflow states
DUO_REALTIME_STATUS_STARTED = 1              # Trip initiated
DUO_REALTIME_STATUS_ARRIVE_PICKUP_POINT = 3  # At pickup location
DUO_REALTIME_STATUS_PICKUP_MANUALLY = 4      # Manual pickup confirmation
DUO_REALTIME_STATUS_DROPOFF_MANUALLY = 8     # Manual dropoff confirmation
DUO_REALTIME_STATUS_ENDED = 11               # Trip completed

# Exception handling states
DUO_REALTIME_STATUS_NO_SHOW = 10             # Partner didn't appear
DUO_REALTIME_STATUS_RUNNING_LATE = 12        # Self running late
DUO_REALTIME_STATUS_PARTNER_RUNNING_LATE = 13 # Partner running late
```

**Escrow Payment Activities:**
```python
# Payment flow activities
ESCROW_ACTIVITY_INC_FEE_RIDER = 1         # Add passenger fee
ESCROW_ACTIVITY_INC_PREMIUM = 3           # Add premium service fee
ESCROW_ACTIVITY_DEC_PAY_TO_DRIVER = 17    # Pay driver
ESCROW_ACTIVITY_DEC_FEE_RIDER = 18        # Deduct passenger fee
ESCROW_ACTIVITY_DEC_FEE_DRIVER = 19       # Deduct driver fee
```

## 🚀 Usage Methods
**Transportation Mode Validation:**
```python
from applications.portal.modules.trip_reservation.define import *

def validate_travel_mode(mode):
    valid_modes = [DRIVING, PUBLIC_TRANSIT, WALKING, BIKING, 
                   INTERMODAL, TRUCKING, PARK_AND_RIDE, DUO, INSTANT_DUO]
    return mode in valid_modes

def get_mode_name(mode_id):
    return TRAVEL_MODES.get(mode_id, 'unknown')

# Usage
if validate_travel_mode(user_mode):
    mode_name = get_mode_name(user_mode)
    print(f"Valid mode: {mode_name}")
```

**Reservation Status Management:**
```python
def validate_status_transition(current_status, new_status):
    valid_transitions = {
        RESERVATION_STATUS_NONE: [RESERVATION_STATUS_SEARCHING],
        RESERVATION_STATUS_SEARCHING: [RESERVATION_STATUS_CHOOSING, RESERVATION_STATUS_MATCHED],
        RESERVATION_STATUS_CHOOSING: [RESERVATION_STATUS_PENDING, RESERVATION_STATUS_CANCELED],
        RESERVATION_STATUS_PENDING: [RESERVATION_STATUS_ACCEPTED, RESERVATION_STATUS_REPEALED],
        RESERVATION_STATUS_MATCHED: [RESERVATION_STATUS_STARTED, RESERVATION_STATUS_CANCELED],
        RESERVATION_STATUS_STARTED: [RESERVATION_STATUS_CANCELED]
    }
    return new_status in valid_transitions.get(current_status, [])
```

**Carpool Role and Status Management:**
```python
def is_carpool_mode(travel_mode):
    return travel_mode in [DUO, INSTANT_DUO]

def get_partner_role(current_role):
    if current_role == ROLE_DRIVER:
        return ROLE_PASSENGER
    elif current_role == ROLE_PASSENGER:
        return ROLE_DRIVER
    return None

def is_carpool_active(realtime_status):
    active_statuses = [
        DUO_REALTIME_STATUS_STARTED,
        DUO_REALTIME_STATUS_ARRIVE_PICKUP_POINT,
        DUO_REALTIME_STATUS_PICKUP_MANUALLY
    ]
    return realtime_status in active_statuses
```

**Business Logic Implementation:**
```python
def categorize_transportation(travel_mode):
    if travel_mode in [DRIVING, WALKING, BIKING]:
        return 'individual'
    elif travel_mode in [PUBLIC_TRANSIT, TRUCKING]:
        return 'public'
    elif travel_mode in [DUO, INSTANT_DUO]:
        return 'shared'
    elif travel_mode in [INTERMODAL, PARK_AND_RIDE]:
        return 'multimodal'
    else:
        return 'unknown'
```

## 📊 Output Examples
**Transportation Mode Enumeration:**
```python
>>> print("Individual Transportation:")
>>> for mode, name in [(DRIVING, 'Driving'), (WALKING, 'Walking'), (BIKING, 'Biking')]:
...     print(f"  {name}: {mode}")

Individual Transportation:
  Driving: 1
  Walking: 3
  Biking: 4
```

**Carpool System Constants:**
```python
>>> print("Carpool Modes:")
>>> print(f"Standard Carpool: {DUO}")
>>> print(f"Instant Carpool: {INSTANT_DUO}")
>>> print(f"Driver Role: {ROLE_DRIVER}")
>>> print(f"Passenger Role: {ROLE_PASSENGER}")

Carpool Modes:
Standard Carpool: 100
Instant Carpool: 101
Driver Role: 1
Passenger Role: 2
```

**Status Lifecycle Example:**
```python
>>> status_flow = [
...     RESERVATION_STATUS_SEARCHING,
...     RESERVATION_STATUS_MATCHED, 
...     RESERVATION_STATUS_STARTED
... ]
>>> print("Typical Reservation Flow:", status_flow)

Typical Reservation Flow: [1, 11, 60]
```

**Mode Mapping Usage:**
```python
>>> print("Mode Mapping Examples:")
>>> print(f"'duo' -> {TRAVEL_MODES['duo']}")
>>> print(f"{DUO} -> '{TRAVEL_MODES[DUO]}'")

Mode Mapping Examples:
'duo' -> 100
100 -> 'duo'
```

**Carpool Real-time Status Flow:**
```python
>>> carpool_workflow = [
...     DUO_REALTIME_STATUS_STARTED,
...     DUO_REALTIME_STATUS_ARRIVE_PICKUP_POINT,
...     DUO_REALTIME_STATUS_PICKUP_MANUALLY,
...     DUO_REALTIME_STATUS_DROPOFF_MANUALLY,
...     DUO_REALTIME_STATUS_ENDED
... ]
>>> print("Carpool Workflow:", carpool_workflow)

Carpool Workflow: [1, 3, 4, 8, 11]
```

## ⚠️ Important Notes
**Transportation Mode Considerations:**
- **Mode Separation**: Individual modes (1-7) vs shared modes (100+) for clear categorization
- **Carpool Distinction**: DUO (planned carpool) vs INSTANT_DUO (real-time matching)
- **Multi-modal Support**: INTERMODAL supports complex trip combinations
- **Business Logic**: Each mode requires different validation and processing rules

**Status Management Complexity:**
- **Lifecycle Dependencies**: Status transitions must follow valid business workflows
- **Carpool Coordination**: Shared trips require synchronized status management across multiple users
- **Cancellation Handling**: Multiple cancellation types for different business scenarios
- **Real-time Requirements**: Status updates must be processed and distributed quickly

**Payment and Escrow Integration:**
- **Activity Types**: 29 different escrow activities for comprehensive payment tracking
- **Fee Management**: Separate tracking for rider fees, driver fees, and premiums
- **Transaction Safety**: Escrow system ensures secure payment handling
- **Refund Logic**: Multiple cancellation scenarios require different refund processing

**System Integration Requirements:**
- **API Consistency**: All transportation APIs must use consistent mode and status values
- **Mobile App Sync**: Mobile applications must handle all status transitions gracefully
- **Analytics Alignment**: Reporting systems depend on consistent categorization
- **External Provider Integration**: Third-party transportation providers must map to standard modes

## 🔗 Related File Links
**Core Module Files:**
- `dao.py` - Database tables using these constants for schema definition
- `carpool_handler.py` - Business logic implementing carpool status management
- `__init__.py` - Module exports making constants available system-wide

**Business Logic Integration:**
- `../../../controllers/reservation.py` - Reservation management using status constants
- `../../../controllers/trip.py` - Trip execution using real-time status constants
- `../carpool/` - Carpool group management integration

**External Integration:**
- Mobile applications implementing transportation mode selection
- External transportation provider APIs mapping to standard modes
- Payment processing systems using escrow activity constants
- Analytics systems categorizing trips by mode and status

## 📈 Use Cases
**Multi-Modal Trip Planning:**
- Support complex trips combining multiple transportation modes
- Validate user selections against available transportation options
- Calculate pricing and timing for different mode combinations
- Optimize trip recommendations based on user preferences and constraints

**Carpool Coordination:**
- Manage complete carpool lifecycle from invitation to completion
- Handle real-time coordination between drivers and passengers
- Process payments and fees through comprehensive escrow system
- Track carpool performance and user satisfaction

**Operational Analytics:**
- Categorize trips by transportation mode for demand analysis
- Track reservation status distributions for operational insights
- Monitor carpool coordination efficiency and success rates
- Generate compliance reports for transportation authorities

**Platform Administration:**
- Configure transportation options for different markets and regions
- Manage business rules for different transportation modes
- Set pricing and fee structures for various service types
- Monitor system health through status distribution analysis

## 🛠️ Improvement Suggestions
**Extensibility Enhancements:**
- Convert to proper Python Enum classes for better type safety and IDE support
- Add hierarchical categorization for transportation modes (powered, manual, shared)
- Include carbon footprint and sustainability metrics for each transportation mode
- Add support for emerging transportation modes (autonomous vehicles, flying cars)

**Business Logic Improvements:**
- Add time-based status transitions with automatic expiration handling
- Include geographic constraints for transportation mode availability
- Add dynamic pricing models with mode-specific pricing rules
- Implement accessibility features for specialized transportation needs

**Integration Enhancements:**
- Add standardized external API mappings for transportation provider integration
- Include real-time capacity and availability tracking for different modes
- Add support for transportation network optimization algorithms
- Implement machine learning categorization for emerging transportation patterns

**Operational Excellence:**
- Add comprehensive validation functions for all constants and transitions
- Include automated testing for all transportation scenarios
- Add monitoring and alerting for unusual status distribution patterns
- Implement A/B testing framework for transportation mode recommendations

## 🏷️ Document Tags
**Keywords:** transportation-modes, reservation-status, carpool-coordination, travel-modes, status-lifecycle, escrow-activities, real-time-tracking, multi-modal, shared-mobility

**Technical Tags:** `#python` `#constants` `#transportation` `#carpool` `#status-management` `#multi-modal` `#shared-mobility` `#payment-processing` `#real-time`

**Target Roles:** Transportation engineers (intermediate), Backend developers (beginner), Business analysts (beginner), Mobile developers (beginner)
**Difficulty Level:** ⭐⭐⭐ (Medium complexity due to comprehensive transportation domain coverage)
**Maintenance Level:** Medium (stable transportation concepts but evolving with new mobility options)
**Business Criticality:** High (foundational constants affecting all transportation operations)
**Related Topics:** Transportation planning, shared mobility, status workflows, payment processing, multi-modal integration