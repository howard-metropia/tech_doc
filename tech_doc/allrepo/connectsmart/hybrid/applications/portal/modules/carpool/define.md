# Carpool Constants and Definitions - Configuration Values

## 🔍 Quick Summary (TL;DR)
**Central configuration file defining constants, enumerations, and status codes for carpool operations in the MaaS platform.** Provides standardized values for group member statuses, group types, suggestion algorithms, and business rules to ensure consistency across the carpool module.

**Core functionality:** Constants definition | Status enumerations | Group types | Configuration values | Business rules | System defaults
**Primary use cases:** Status validation, group categorization, member management, system configuration, business logic consistency
**Compatibility:** Python 2.7+, Web2py framework, cross-module consistency

## ❓ Common Questions Quick Index
- **Q: What member statuses are available?** → See [Technical Specifications](#technical-specifications)
- **Q: How many group types are supported?** → See [Output Examples](#output-examples)
- **Q: What's the suggestion group ID?** → See [Detailed Code Analysis](#detailed-code-analysis)
- **Q: How to validate member status?** → See [Usage Methods](#usage-methods)
- **Q: What are the available group categories?** → See [Functionality Overview](#functionality-overview)
- **Q: How to extend group types?** → See [Improvement Suggestions](#improvement-suggestions)
- **Q: What's the difference between status values?** → See [Important Notes](#important-notes)
- **Q: Where are transaction fees defined?** → See [Related File Links](#related-file-links)

## 📋 Functionality Overview
**Non-technical explanation:** Think of this as the "rules book" for a carpooling system. Just like how a game has rules that define what different moves mean, this file defines what different statuses and categories mean in carpooling. For example, it tells the system that "status 2" means someone is an active member, or that "type 2" means a work-related carpool group.

**Technical explanation:** Configuration constants module implementing enumeration patterns for carpool domain logic. Provides centralized definition of business rules, status codes, and categorical values used throughout the carpool system for data validation and business logic consistency.

**Business value:** Ensures consistent behavior across all carpool operations, simplifies maintenance by centralizing configuration values, and provides clear business rules that stakeholders can understand and modify as requirements evolve.

**System context:** Foundational configuration layer imported by DAO classes, business logic handlers, and controllers to maintain consistent status management and categorization across the carpool ecosystem.

## 🔧 Technical Specifications
- **File:** `applications/portal/modules/carpool/define.py`
- **Language:** Python 2.7+
- **Type:** Constants and enumeration definitions
- **Size:** ~24 lines
- **Complexity:** ⭐ (Very Low - simple constant definitions)

**Constants Categories:**
1. **Member Status Constants** (4 values):
   - `GROUP_MEMBER_STATUS_NONE = 0` - No membership
   - `GROUP_MEMBER_STATUS_PENDING = 1` - Invitation pending
   - `GROUP_MEMBER_STATUS_MEMBER = 2` - Active member
   - `GROUP_MEMBER_STATUS_MANAGEMENT = 3` - Management privileges

2. **Group Type Constants** (5 categories):
   - `GROUP_TYPE_SPORTS = 1` - Sports and recreation
   - `GROUP_TYPE_WORK = 2` - Work commuting
   - `GROUP_TYPE_SCHOOL = 3` - Educational institution
   - `GROUP_TYPE_EVENTS = 4` - Event-based carpools
   - `GROUP_TYPE_OTHERS = 5` - Miscellaneous categories

3. **System Configuration**:
   - `GROUP_TYPES` list - All valid group type values
   - `GROUP_ID_DUO_SUGGESTION = 1` - Special system suggestion group

**No Dependencies:** Pure Python constants with no external imports

## 📝 Detailed Code Analysis
**Constant Definition Pattern:**
```python
# Member status enumeration
GROUP_MEMBER_STATUS_NONE = 0        # Not a member
GROUP_MEMBER_STATUS_PENDING = 1     # Invitation sent, awaiting response
GROUP_MEMBER_STATUS_MEMBER = 2      # Active participating member
GROUP_MEMBER_STATUS_MANAGEMENT = 3  # Admin/management privileges
```

**Group Type Hierarchy:**
```python
# Business category enumeration
GROUP_TYPE_SPORTS = 1    # Recreational/fitness carpools
GROUP_TYPE_WORK = 2      # Professional commuting
GROUP_TYPE_SCHOOL = 3    # Educational institutions
GROUP_TYPE_EVENTS = 4    # Temporary event-based
GROUP_TYPE_OTHERS = 5    # Catch-all category

# Validation helper
GROUP_TYPES = [GROUP_TYPE_SPORTS, GROUP_TYPE_WORK, GROUP_TYPE_SCHOOL, 
               GROUP_TYPE_EVENTS, GROUP_TYPE_OTHERS]
```

**Special System Values:**
```python
# Internal system group for AI suggestions
GROUP_ID_DUO_SUGGESTION = 1
```

**Design Patterns:**
- **Constants Pattern**: Immutable values preventing magic numbers
- **Enumeration Simulation**: Integer constants with meaningful names
- **Validation Lists**: Centralized valid value collections
- **Namespace Organization**: Consistent naming conventions

**Memory Usage:** Minimal - only integer constants and small list
**Performance:** O(1) access for all constant lookups

## 🚀 Usage Methods
**Status Validation:**
```python
from applications.portal.modules.carpool.define import *

def validate_member_status(status):
    valid_statuses = [
        GROUP_MEMBER_STATUS_NONE,
        GROUP_MEMBER_STATUS_PENDING, 
        GROUP_MEMBER_STATUS_MEMBER,
        GROUP_MEMBER_STATUS_MANAGEMENT
    ]
    return status in valid_statuses

# Usage
if validate_member_status(user_status):
    print("Valid member status")
```

**Group Type Checking:**
```python
def is_valid_group_type(group_type):
    return group_type in GROUP_TYPES

def get_group_type_name(group_type):
    type_names = {
        GROUP_TYPE_SPORTS: 'Sports & Recreation',
        GROUP_TYPE_WORK: 'Work Commute',
        GROUP_TYPE_SCHOOL: 'School & Education',
        GROUP_TYPE_EVENTS: 'Events & Activities',
        GROUP_TYPE_OTHERS: 'Other'
    }
    return type_names.get(group_type, 'Unknown')
```

**Database Integration:**
```python
# In DAO usage
from .define import GROUP_MEMBER_STATUS_MEMBER

# Query active members
active_members = db(
    (db.group_member.group_id == group_id) &
    (db.group_member.member_status == GROUP_MEMBER_STATUS_MEMBER)
).select()
```

**Business Logic Implementation:**
```python
def promote_to_admin(db, user_id, group_id):
    # Update member status to management
    db(
        (db.group_member.user_id == user_id) &
        (db.group_member.group_id == group_id)
    ).update(member_status=GROUP_MEMBER_STATUS_MANAGEMENT)
```

## 📊 Output Examples
**Member Status Constants:**
```python
>>> from applications.portal.modules.carpool.define import *
>>> print("Member Status Values:")
>>> print(f"None: {GROUP_MEMBER_STATUS_NONE}")
>>> print(f"Pending: {GROUP_MEMBER_STATUS_PENDING}")
>>> print(f"Member: {GROUP_MEMBER_STATUS_MEMBER}")
>>> print(f"Management: {GROUP_MEMBER_STATUS_MANAGEMENT}")

Member Status Values:
None: 0
Pending: 1
Member: 2
Management: 3
```

**Group Type Enumeration:**
```python
>>> print("Available Group Types:")
>>> for group_type in GROUP_TYPES:
...     print(f"Type {group_type}: {get_group_type_name(group_type)}")

Available Group Types:
Type 1: Sports & Recreation
Type 2: Work Commute
Type 3: School & Education
Type 4: Events & Activities
Type 5: Other
```

**System Configuration:**
```python
>>> print(f"Suggestion Group ID: {GROUP_ID_DUO_SUGGESTION}")
>>> print(f"All Group Types: {GROUP_TYPES}")

Suggestion Group ID: 1
All Group Types: [1, 2, 3, 4, 5]
```

**Validation Examples:**
```python
>>> def validate_status(status):
...     return status in [0, 1, 2, 3]
>>> 
>>> print(validate_status(2))  # Valid member
>>> print(validate_status(5))  # Invalid status

True
False
```

## ⚠️ Important Notes
**Business Logic Considerations:**
- **Status Progression**: Members typically progress from PENDING (1) → MEMBER (2) → MANAGEMENT (3)
- **Permission Levels**: Higher status values generally indicate more privileges
- **Group Types**: Categories are mutually exclusive - groups belong to one type only
- **Special Groups**: GROUP_ID_DUO_SUGGESTION (1) is reserved for system use

**Development Guidelines:**
- **No Magic Numbers**: Always use named constants instead of raw integers
- **Backward Compatibility**: Adding new statuses/types should use higher numbers
- **Validation**: Always validate incoming status/type values against defined constants
- **Documentation**: Update documentation when adding new categories

**Security Notes:**
- **Input Validation**: Validate all status/type inputs against defined constants
- **Privilege Escalation**: Carefully control transitions to MANAGEMENT status
- **Data Integrity**: Ensure database constraints align with constant definitions

**Performance Considerations:**
- Constants are loaded once at module import time
- Use `in GROUP_TYPES` for O(1) validation instead of manual comparisons
- Consider caching validation results for high-frequency operations

## 🔗 Related File Links
**Core Module Files:**
- `dao.py` - Uses constants for field defaults and validation
- `matching_handler.py` - Implements business logic using status constants
- `__init__.py` - Exports all constants for external use

**Business Logic Integration:**
- `../../../controllers/carpools.py` - Controller implementing carpool operations
- `../../../controllers/duo_group.py` - Group management using status constants

**Database Models:**
- `../../models/db.py` - Database schema definitions
- `../../models/common.py` - Shared validation functions

**Configuration Management:**
- Application configuration files that may override default values
- Enterprise-specific configuration for custom group types

## 📈 Use Cases
**Member Lifecycle Management:**
- User invitation workflow: NONE → PENDING → MEMBER
- Admin promotion: MEMBER → MANAGEMENT
- Member removal: Any status → NONE
- Status-based access control in user interfaces

**Group Categorization:**
- Corporate carpool setup using WORK type
- University campus groups using SCHOOL type
- Sports club carpools using SPORTS type
- Event-specific groups using EVENTS type

**System Operations:**
- Automated group suggestions using GROUP_ID_DUO_SUGGESTION
- Bulk member operations filtered by status
- Analytics and reporting grouped by member status
- Permission checks based on management status

**Data Migration and Validation:**
- Validating imported data against defined constants
- Migrating legacy status codes to standardized values
- Ensuring data consistency during system upgrades

## 🛠️ Improvement Suggestions
**Code Organization:**
- Convert to proper Python Enum classes for Python 3+ compatibility
- Add docstrings documenting the purpose and valid transitions for each status
- Include type hints for better IDE support and documentation
- Create validation functions within the module

**Feature Enhancements:**
- Add more granular group types (e.g., HEALTHCARE, RETAIL, GOVERNMENT)
- Include status transition validation rules
- Add internationalization support for group type display names
- Implement configurable business rules through external configuration

**Business Logic Extensions:**
- Add time-based status changes (e.g., automatic pending expiration)
- Include member role hierarchies within management status
- Add group privacy levels and access controls
- Support for custom enterprise-specific group types

**Monitoring and Analytics:**
- Add status change logging for audit trails
- Include metrics collection for status distribution analysis
- Create reporting functions for membership statistics
- Implement alerting for unusual status transition patterns

## 🏷️ Document Tags
**Keywords:** carpool, constants, definitions, status, enumeration, group-types, member-status, configuration, business-rules, validation, categories, system-defaults

**Technical Tags:** `#python` `#constants` `#enumeration` `#configuration` `#carpool` `#status-management` `#business-logic` `#validation` `#group-types`

**Target Roles:** Backend developers (beginner), Business analysts (beginner), QA engineers (beginner)
**Difficulty Level:** ⭐ (Very simple constant definitions with clear business meaning)
**Maintenance Level:** Low (rarely changes, well-defined business rules)
**Business Criticality:** Medium (supports business logic but not directly user-facing)
**Related Topics:** Business rule management, status workflows, enumeration patterns, configuration management