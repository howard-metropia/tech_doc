# Carpool Data Access Objects - Database Table Definitions

## 🔍 Quick Summary (TL;DR)
**Comprehensive database table definitions for carpool functionality in the MaaS platform using PyDAL ORM.** Defines 11 interconnected tables supporting group management, member tracking, matching statistics, penalties, and AI-driven suggestions for carpool operations.

**Core functionality:** Database schema | Table definitions | Field validation | Carpool entities | Relationship mapping | Data constraints
**Primary use cases:** Group creation, member management, matching algorithms, penalty tracking, pricing suggestions, statistics collection
**Compatibility:** PyDAL ORM, Web2py framework, MySQL/PostgreSQL databases

## ❓ Common Questions Quick Index
- **Q: What carpool tables are defined?** → See [Technical Specifications](#technical-specifications)
- **Q: How to create carpool database schema?** → See [Usage Methods](#usage-methods)
- **Q: What's the relationship between tables?** → See [Detailed Code Analysis](#detailed-code-analysis)
- **Q: How does group membership work?** → See [Output Examples](#output-examples)
- **Q: What validation rules apply?** → See [Technical Specifications](#technical-specifications)
- **Q: How to handle geofencing data?** → See [Important Notes](#important-notes)
- **Q: What are penalty mechanisms?** → See [Use Cases](#use-cases)
- **Q: How does matching statistics work?** → See [Functionality Overview](#functionality-overview)

## 📋 Functionality Overview
**Non-technical explanation:** Think of this as the blueprint for a comprehensive carpooling database. Like designing a filing system for a carpooling company, it defines separate folders for groups (like departments), members (like employees), blacklists (like blocked contacts), and statistics (like performance reports). Each folder has specific rules about what information goes where and how it's organized.

**Technical explanation:** PyDAL ORM table definitions implementing a complete carpool domain model with referential integrity, field validation, and optimized data structures for high-performance carpool matching and management operations.

**Business value:** Enables scalable carpool operations supporting thousands of users and groups, with robust tracking for matching success rates, user penalties, and AI-driven suggestions that improve rider experience and operational efficiency.

**System context:** Core data layer for the carpool module, supporting controllers, matching algorithms, and reporting systems within the broader MaaS platform ecosystem.

## 🔧 Technical Specifications
- **File:** `applications/portal/modules/carpool/dao.py`
- **Language:** Python 2.7+
- **Framework:** Web2py with PyDAL ORM
- **Type:** Database table definitions
- **Size:** ~155 lines
- **Complexity:** ⭐⭐⭐ (Medium - complex table relationships)

**Table Definitions (11 tables):**
1. **DuoGroupTable** - Carpool group entities with geofencing
2. **GroupMemberTable** - Member-group relationships with status tracking
3. **DuoTypeTable** - Group type classifications (15 char limit)
4. **GroupTypeTable** - Many-to-many group-type relationships
5. **BlacklistTable** - User blocking relationships
6. **GroupAdminProfileTable** - Enhanced admin profiles with social links
7. **MatchStatisticTable** - Matching performance metrics
8. **ReservationMatchTable** - Invitation and match counting
9. **PenaltyTable** - User penalty tracking with timestamps
10. **SuggestedDuoGroupTable** - AI-suggested groups with scoring
11. **SuggestedDuoPriceTable** - Dynamic pricing suggestions

**Key Dependencies:**
- `pydal.objects` (Required) - PyDAL Table and Field classes
- `gluon.validators` (Required) - IS_LENGTH, IS_DATETIME validators
- Database connection object (Runtime) - Passed during table instantiation

## 📝 Detailed Code Analysis
**Core Table Architecture:**
```python
class DuoGroupTable(Table):
    def __init__(self, db, tablename, *fields, **args):
        def_fields = (
            Field('creator_id', 'integer', required=True, notnull=True),
            Field('name', 'string', length=512, requires=IS_LENGTH(512)),
            Field('geofence', 'string', length=512, comment='WKT format'),
            Field('geofence_radius', 'float', comment='in meters'),
            Field('enterprise_id', 'integer', required=False),
            # ... additional fields
        )
```

**Key Design Patterns:**
- **Table Inheritance**: All tables extend PyDAL Table class
- **Field Composition**: Dynamic field addition with `fields + def_fields`
- **Validation Layer**: IS_LENGTH and IS_DATETIME validators on string/date fields
- **Referential Integrity**: Foreign key relationships with `db.table_name` syntax

**Critical Data Structures:**
- **Geofencing**: WKT format strings with radius and coordinate data
- **Status Tracking**: Integer-based member status with defined states
- **Social Integration**: URL fields for LinkedIn, Facebook, Twitter
- **Scoring System**: Double precision scoring for AI suggestions

**Memory Patterns:**
- Table definitions are lightweight metadata
- Actual data storage managed by underlying database
- Field validators cached in table metadata

## 🚀 Usage Methods
**Basic Table Creation:**
```python
from pydal import DAL
from applications.portal.modules.carpool.dao import DuoGroupTable

# Create database connection
db = DAL('mysql://user:pass@localhost/carpool_db')

# Define carpool group table
db.define_table('duo_group', DuoGroupTable(db, 'duo_group'))

# Create table in database
db.commit()
```

**Advanced Schema Setup:**
```python
# Define multiple related tables
db.define_table('duo_group', DuoGroupTable(db, 'duo_group'))
db.define_table('group_member', GroupMemberTable(db, 'group_member'))
db.define_table('blacklist', BlacklistTable(db, 'blacklist'))

# Add custom fields
custom_fields = [Field('custom_field', 'string')]
db.define_table('duo_group_extended', 
               DuoGroupTable(db, 'duo_group_extended', *custom_fields))
```

**Production Configuration:**
```python
# With connection pooling and optimization
db = DAL('mysql://user:pass@localhost/carpool_db',
         pool_size=10, migrate=False, fake_migrate=True)

# Define all carpool tables
for table_name, table_class in [
    ('duo_group', DuoGroupTable),
    ('group_member', GroupMemberTable),
    ('match_statistic', MatchStatisticTable)
]:
    db.define_table(table_name, table_class(db, table_name))
```

## 📊 Output Examples
**DuoGroup Record Structure:**
```python
# Sample group record
group_data = {
    'creator_id': 12345,
    'name': 'Downtown Commuters',
    'description': 'Daily commute to downtown business district',
    'is_private': False,
    'geofence': 'POLYGON((-122.4 37.8, -122.3 37.8, -122.3 37.7, -122.4 37.7, -122.4 37.8))',
    'geofence_radius': 500.0,
    'geofence_latitude': 37.7749,
    'geofence_longitude': -122.4194,
    'address': '123 Market St, San Francisco, CA',
    'enterprise_id': 1001,
    'disabled': False
}
```

**Member Status Values:**
```python
# Group member statuses (from define.py)
GROUP_MEMBER_STATUS_NONE = 0      # Not a member
GROUP_MEMBER_STATUS_PENDING = 1   # Invitation pending
GROUP_MEMBER_STATUS_MEMBER = 2    # Active member
GROUP_MEMBER_STATUS_MANAGEMENT = 3 # Admin privileges
```

**Matching Statistics Example:**
```python
# Match statistics record
match_stats = {
    'reservation_id': 67890,
    'match_reservation_id': 67891,
    'time_to_pickup': 300,    # 5 minutes in seconds
    'time_to_dropoff': 1800,  # 30 minutes in seconds
    'created_on': datetime.utcnow(),
    'modified_on': datetime.utcnow()
}
```

**Suggested Group Scoring:**
```python
# AI suggestion record
suggestion = {
    'user_id': 12345,
    'group_id': 1001,
    'score': 0.85,          # Confidence score 0-1
    'activity': 2,          # Activity type indicator
    'created_time': datetime.utcnow()
}
```

## ⚠️ Important Notes
**Security Considerations:**
- **Input Validation**: All string fields have IS_LENGTH validators to prevent overflow attacks
- **SQL Injection**: PyDAL provides automatic parameterization and escaping
- **Access Control**: No table-level security - implement in application layer
- **PII Data**: Social media URLs and email in GroupAdminProfileTable require privacy controls

**Geofencing Implementation:**
- **WKT Format**: Use standard Well-Known Text format for geofence polygons
- **Coordinate System**: Assumes WGS84 (EPSG:4326) coordinate reference system
- **Radius Validation**: Ensure geofence_radius values are positive and reasonable (< 50km)
- **Performance**: Consider spatial indexing for large-scale geofence queries

**Common Troubleshooting:**
- **Migration Issues**: Set `migrate=False` in production to avoid schema conflicts
- **Foreign Key Errors**: Ensure referenced tables exist before creating dependent tables
- **Validator Failures**: Check field length limits, especially for name fields (512 chars)
- **Unicode Issues**: Use UTF-8 encoding for international characters in names/descriptions

## 🔗 Related File Links
**Core Module Files:**
- `__init__.py` - Module exports and initialization
- `define.py` - Constants and enumeration values
- `matching_handler.py` - Business logic for carpool matching

**Database Configuration:**
- `../../models/db.py` - Database connection configuration
- `../../models/common.py` - Shared database utilities

**Business Logic:**
- `../../../controllers/carpools.py` - Carpool operations controller
- `../trip_reservation/dao.py` - Trip reservation table definitions

**Testing:**
- Unit tests for table validation and relationships
- Integration tests with actual database operations

## 📈 Use Cases
**Development Phase:**
- Database schema creation during application setup
- Migration scripts for production deployments
- Testing data generation with realistic field constraints

**Operational Scenarios:**
- Group creation and management by users and admins
- Member invitation and status tracking workflows
- Blacklist management for user safety and preferences
- Performance monitoring through matching statistics

**Analytics and AI:**
- Collecting matching success rates for algorithm improvement
- Tracking user penalties for behavior modification
- Generating group suggestions based on historical data
- Dynamic pricing based on demand and supply patterns

**Enterprise Integration:**
- Multi-tenant group management with enterprise_id segregation
- Admin profile management for corporate carpool programs
- Geofenced group creation for campus or office building carpools

## 🛠️ Improvement Suggestions
**Performance Optimizations:**
- Add database indexes on frequently queried fields (user_id, group_id, created_on)
- Implement table partitioning for large-scale matching statistics
- Consider read replicas for analytics queries on historical data
- Add caching layer for frequently accessed group information

**Feature Enhancements:**
- Add soft delete functionality instead of boolean 'disabled' flag
- Implement audit trail tables for tracking changes to groups and memberships
- Add support for recurring carpool schedules within group definitions
- Include group capacity limits and current member count fields

**Data Quality:**
- Add database constraints for referential integrity beyond PyDAL validations
- Implement data archiving strategy for old penalty and statistics records
- Add field-level encryption for sensitive social media URLs
- Include data retention policies for GDPR compliance

**Monitoring and Maintenance:**
- Add table-level metrics collection for database performance monitoring
- Implement automated data quality checks for geofence validity
- Create database backup and recovery procedures for carpool data
- Add logging for all table operations to support debugging

## 🏷️ Document Tags
**Keywords:** carpool, database, tables, PyDAL, ORM, groups, members, matching, statistics, penalties, suggestions, geofencing, validation, relationships, schema

**Technical Tags:** `#python` `#pydal` `#orm` `#database` `#carpool` `#table-definitions` `#schema-design` `#geospatial` `#validation` `#relationships`

**Target Roles:** Database developers (intermediate), Backend developers (intermediate), DevOps engineers (advanced)
**Difficulty Level:** ⭐⭐⭐ (Medium complexity with interconnected table relationships)
**Maintenance Level:** Medium (schema changes require careful migration planning)
**Business Criticality:** High (core data structures for carpool operations)
**Related Topics:** Database design, ORM patterns, geospatial data, carpool algorithms, data validation