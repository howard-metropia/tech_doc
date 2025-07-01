# Campaign DAO - Database Table Definitions

🔍 **Quick Summary (TL;DR)**
- Database table class definitions for campaign management system using Web2py's PyDAL framework, providing structured schema for campaigns, steps, user interactions, locations, and survey responses.
- **Keywords:** dao | database | table | schema | campaign | step | user | location | microsurvey | record | pydal | web2py | field | validation | datetime | decimal | geography | survey-response
- **Primary use cases:** Database schema definition, table creation, data validation, ORM mapping, campaign data structure
- **Compatibility:** Python 2.7+, Web2py framework, PyDAL ORM, requires pydal.objects and gluon.validators

❓ **Common Questions Quick Index**
- **Q: What tables are defined in this DAO?** → See [Technical Specifications](#technical-specifications)
- **Q: How do I create a campaign table?** → See [Usage Methods](#usage-methods)
- **Q: What fields are required for campaigns?** → See [Detailed Code Analysis](#detailed-code-analysis)
- **Q: How do I validate field data?** → See [Output Examples](#output-examples)
- **Q: What's the relationship between tables?** → See [Related File Links](#related-file-links)
- **Q: How do I extend a table definition?** → See [Usage Methods](#usage-methods)
- **Q: What are the field types and constraints?** → See [Technical Specifications](#technical-specifications)
- **Q: How do I handle location data?** → See [Detailed Code Analysis](#detailed-code-analysis)
- **Q: What's the microsurvey data structure?** → See [Output Examples](#output-examples)
- **Q: How do I troubleshoot table creation errors?** → See [Important Notes](#important-notes)

📋 **Functionality Overview**
- **Non-technical explanation:** Like architectural blueprints for a database that define exactly how campaign information should be stored - what rooms (tables) exist, what furniture (fields) goes in each room, and what rules (constraints) must be followed. Think of it as a filing cabinet system specification that tells you exactly what folders to create and what information goes in each folder, or a recipe template that specifies all the ingredients and their measurements.
- **Technical explanation:** Data Access Object (DAO) layer implementing PyDAL table class inheritance pattern, providing structured database schema definitions with field validation, constraints, and relationship mappings for campaign management system.
- **Business value:** Ensures data integrity, standardizes database schema across environments, provides validation layer, enables ORM functionality, and facilitates database migration and maintenance.
- **System context:** Database abstraction layer for the ConnectSmart mobility platform's campaign system, defining the data structure foundation for all campaign-related operations.

🔧 **Technical Specifications**
- **File info:** `dao.py`, 207 lines, Database schema module, Python, ~8KB, Complexity: Medium (★★★☆☆)
- **Table classes:** 9 table definitions with comprehensive field specifications
- **Dependencies:**
  - `pydal.objects` (Critical): Table and Field classes from PyDAL ORM
  - `gluon.validators` (Critical): IS_LENGTH, IS_DATETIME validation functions
  - **Web2py framework** (Required): Version 2.14+
  - **Database backend** (Required): MySQL, PostgreSQL, SQLite, or other PyDAL-supported database

- **Table definitions:**
  - **CampaignTable:** Main campaign configuration with 24 fields
  - **StepTable:** Campaign step definitions with 11 fields  
  - **CampaignUserTable:** User-campaign associations with 19 fields
  - **LocationTable:** Geographic location data with 10 fields
  - **UserRecordTable:** User activity records with 7 fields
  - **MicrosurveyRecordTable:** Survey response data with 7 fields
  - **MicrosurveyQuestionTable:** Survey question definitions with 4 fields
  - **ActivityLocation:** User activity patterns with 7 fields
  - **VerifyPredictedLocationTable:** Location verification with 15 fields

- **Field types:** string, integer, double, decimal, datetime, text, with length and validation constraints
- **Validation rules:** IS_LENGTH for string fields, IS_DATETIME for datetime fields, required/notnull constraints

📝 **Detailed Code Analysis**
- **CampaignTable core fields:**
  ```python
  Field('name', type='string'),                    # Campaign identifier
  Field('type_id', type='integer', notnull=True), # Campaign type classification
  Field('start_time', type='datetime'),            # Campaign start timestamp
  Field('end_time', type='datetime'),              # Campaign end timestamp
  Field('points', type='decimal(10,2)', notnull=True), # Reward points
  Field('travel_modes', type='string'),            # Supported transport modes
  ```

- **Geographic data structure:**
  ```python
  # Location-based campaign targeting
  Field('start_center_lat', type='double'),        # Origin latitude
  Field('start_center_lng', type='double'),        # Origin longitude
  Field('start_range', type='integer'),            # Radius in meters
  Field('end_center_lat', type='double'),          # Destination latitude
  Field('end_center_lng', type='double'),          # Destination longitude
  Field('end_range', type='integer'),              # Radius in meters
  ```

- **Microsurvey data model:**
  ```python
  # Survey question structure
  Field('question', type='string'),                # Question text
  Field('choices', type='string'),                 # JSON-encoded choices
  # Survey response tracking
  Field('answer', type='string'),                  # User's answer
  Field('skip', type='integer'),                   # Skip indicator (0/1)
  Field('step_no', type='integer'),                # Question sequence number
  ```

- **Inheritance pattern:** All table classes inherit from `pydal.objects.Table`
- **Constructor pattern:** `__init__` method accepts additional fields and keyword arguments for extensibility
- **Validation strategy:** Field-level validation with gluon validators, required/notnull constraints
- **Timestamp management:** created_on and modified_on fields with automatic datetime validation

🚀 **Usage Methods**
- **Basic table creation:**
  ```python
  from dao import CampaignTable
  # Create campaign table instance
  campaign_table = CampaignTable(db, 'cm_campaign')
  ```

- **Extended table with custom fields:**
  ```python
  from dao import StepTable
  # Add custom fields to step table
  custom_step = StepTable(db, 'cm_step_extended', 
                         Field('custom_field', type='string'))
  ```

- **Web2py model integration:**
  ```python
  # In Web2py models/db.py
  from applications.portal.modules.campaign.dao import *
  
  # Define tables in Web2py
  db.define_table('cm_campaign', CampaignTable(db, 'cm_campaign'))
  db.define_table('cm_step', StepTable(db, 'cm_step'))
  db.define_table('cm_location', LocationTable(db, 'cm_location'))
  ```

- **Database record operations:**
  ```python
  # Insert new campaign
  campaign_id = db.cm_campaign.insert(
      name='Summer Mobility Challenge',
      type_id=1,
      start_time=datetime.now(),
      end_time=datetime.now() + timedelta(days=30),
      points=100.00,
      created_on=datetime.now(),
      modified_on=datetime.now()
  )
  
  # Query campaigns
  campaigns = db(db.cm_campaign.is_active == 1).select()
  ```

📊 **Output Examples**
- **CampaignTable field structure:**
  ```python
  >>> campaign = CampaignTable(db, 'cm_campaign')
  >>> print([f.name for f in campaign.fields])
  ['id', 'is_active', 'name', 'type_id', 'creater', 'start_time', 'end_time', 
   'from_time', 'to_time', 'travel_modes', 'change_mode_transport', 
   'start_center_lat', 'start_center_lng', 'start_range', 'end_center_lat', 
   'end_center_lng', 'end_range', 'geo_nation', 'poi_lat', 'poi_lng', 
   'poi_range', 'poi_range_unit', 'poi_name', 'poi_address', 'people_type', 
   'points', 'wta_ratio_user', 'status', 'created_on', 'modified_on']
  ```

- **LocationTable record example:**
  ```json
  {
    "id": 1,
    "user_id": 12345,
    "name": "Downtown Office",
    "address": "123 Main St, Seattle, WA",
    "latitude": 47.6062,
    "longitude": -122.3321,
    "fan_in": 5,
    "fan_out": 3,
    "status": 1,
    "created_on": "2024-01-15T08:30:00",
    "modified_on": "2024-01-15T08:30:00"
  }
  ```

- **MicrosurveyRecordTable structure:**
  ```json
  {
    "id": 101,
    "user_record_id": 55,
    "step_id": 201,
    "step_no": 1,
    "answer": "[\"Excellent\", \"On time\"]",
    "skip": 0,
    "created_on": "2024-01-15T14:22:00",
    "modified_on": "2024-01-15T14:22:00"
  }
  ```

- **Field validation errors:**
  ```
  ValidationError: IS_DATETIME: enter date and time as 2024-01-15 14:30:00
  ValidationError: IS_LENGTH: enter from 1 to 64 characters
  IntegrityError: NOT NULL constraint failed: cm_campaign.type_id
  ```

- **Table creation SQL output:**
  ```sql
  CREATE TABLE cm_campaign (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      is_active INTEGER DEFAULT 1,
      name VARCHAR(512),
      type_id INTEGER NOT NULL,
      points DECIMAL(10,2) NOT NULL,
      created_on TIMESTAMP NOT NULL,
      modified_on TIMESTAMP NOT NULL
  );
  ```

⚠️ **Important Notes**
- **Security considerations:**
  - All datetime fields use IS_DATETIME validator to prevent injection attacks
  - String fields have length limits to prevent buffer overflow attacks
  - No direct SQL execution; relies on PyDAL's parameterized queries
  - Geographic coordinates should be validated for reasonable ranges (-90 to 90 lat, -180 to 180 lng)

- **Data integrity:**
  - Foreign key relationships must be maintained manually (PyDAL doesn't enforce them)
  - Decimal fields for points ensure precise financial calculations
  - Required fields (notnull=True) prevent incomplete records
  - Timestamp fields should always be in UTC for consistency

- **Common troubleshooting:**
  - **Table creation fails:** Check database permissions, verify Web2py configuration
  - **Field validation errors:** Ensure data types match field definitions
  - **Missing fields:** Verify all required fields are provided during record creation
  - **Datetime issues:** Use proper datetime format (YYYY-MM-DD HH:MM:SS)
  - **Decimal precision:** Points field uses DECIMAL(10,2) for currency-accurate calculations

- **Performance considerations:**
  - Add database indexes on frequently queried fields (user_id, campaign_id, created_on)
  - Consider partitioning large tables by date ranges
  - Use appropriate field sizes to optimize storage space
  - Geographic queries may benefit from spatial indexes

🔗 **Related File Links**
- **Core dependencies:**
  - `__init__.py` - Module package initialization that exports these table classes
  - `define.py` - Campaign constants and configuration used with these tables
  - `campaign_handler.py` - Business logic that operates on these table structures
- **Database configuration:** Web2py database connection settings and model definitions
- **Migration scripts:** Database migration files that use these table definitions
- **API controllers:** Web2py controllers that perform CRUD operations on these tables
- **Test files:** Unit tests that validate table structure and constraints
- **Documentation:** API documentation that describes these table schemas

📈 **Use Cases**
- **Database schema definition:** Defining consistent database structure across development, staging, and production
- **ORM mapping:** Providing object-relational mapping for campaign data access
- **Data validation:** Ensuring data integrity through field-level validation
- **Migration management:** Creating and updating database schema during deployments
- **API development:** Providing structured data models for REST API endpoints
- **Testing:** Creating test databases with consistent schema for unit and integration tests
- **Documentation:** Serving as authoritative source for database schema documentation

🛠️ **Improvement Suggestions**
- **Code optimization:**
  - Add database indexes specification to table definitions (Medium complexity, improves query performance)
  - Implement field-level documentation with docstrings (Low complexity, improves maintainability)
  - Add custom validation functions for geographic coordinates (Medium complexity, improves data quality)

- **Feature enhancements:**
  - Implement foreign key relationships with proper constraints (High complexity, improves data integrity)
  - Add audit trail fields with automatic timestamping (Medium complexity, improves tracking)
  - Implement soft delete functionality with deleted_on field (Low complexity, improves data retention)

- **Schema improvements:**
  - Add compound indexes for common query patterns (Medium complexity, improves performance)
  - Implement table-level constraints for business rules (High complexity, ensures data consistency)
  - Add metadata fields for versioning and tracking (Low complexity, improves management)

- **Validation enhancements:**
  - Add custom validators for email, phone, and geographic data (Medium complexity, improves data quality)
  - Implement cross-field validation (end_time > start_time) (Medium complexity, prevents logical errors)
  - Add JSON schema validation for choice fields (High complexity, ensures structured data)

🏷️ **Document Tags**
- **Keywords:** dao, database, table, schema, pydal, web2py, field, validation, campaign, microsurvey, location, geography, decimal, datetime, orm, data-model
- **Technical tags:** #python #web2py #pydal #database #orm #schema #validation #data-model #campaign-management #geographic-data #survey-data
- **Target roles:** Database administrators (intermediate-senior), Backend developers (junior-senior), Data engineers (intermediate), System architects (senior)
- **Difficulty level:** ⭐⭐⭐☆☆ (Requires understanding of database concepts, PyDAL ORM, and Web2py framework)
- **Maintenance level:** Medium (periodic updates for new features and schema changes)
- **Business criticality:** High (foundation for all campaign data storage and retrieval)
- **Related topics:** Database design, ORM frameworks, Data validation, Schema migration, Geographic information systems, Survey data management