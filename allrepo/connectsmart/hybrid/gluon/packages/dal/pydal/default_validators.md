# default_validators.py

## Overview
Automatic validation assignment system for PyDAL that generates appropriate validators based on field types, constraints, and relationships. This module bridges PyDAL's field definition system with the comprehensive validator framework.

## Core Function

### default_validators(db, field)
```python
def default_validators(db, field):
```

**Purpose**: Automatically generates validation rules for database fields based on their type and constraints.

**Parameters:**
- **db**: Database instance for reference validation
- **field**: Field object requiring validation

**Return Value**: Validator instance or list of validators, or None if no validation needed.

## Field Analysis

### Field Property Extraction
```python
field_type = field.type
field_unique = field.unique
field_notnull = field.notnull
```

The function examines three key field properties:
- **Type**: Determines the core validation logic
- **Unique**: Adds uniqueness constraint validation
- **Not Null**: Requires non-empty value validation

## Reference Field Validation

### Reference Type Detection
```python
is_ref = field_type.startswith("reference")
is_list = field_type.startswith("list:")
if is_ref or field_type.startswith("list:reference"):
```

**Supported Reference Types:**
- **reference table**: Single foreign key reference
- **reference table.field**: Reference to specific field
- **list:reference table**: Multiple foreign key references

### Reference Processing
```python
table_field = field_type[10 if is_ref else 15:].split(".", 1)
table_name = table_field[0]
field_name = table_field[-1]
```

**Steps:**
1. **Parse Reference**: Extract table and optional field name
2. **Validate Table**: Ensure referenced table exists in database
3. **Create Validator**: Generate IS_IN_DB validator with appropriate settings

### IS_IN_DB Configuration
```python
if table_name in db.tables:
    referenced = db[table_name]
    if len(table_field) == 1:
        # Reference to table's primary key
        requires = validators.IS_IN_DB(
            db,
            referenced._id,
            label=getattr(referenced, "_format", None),
            multiple=is_list,
        )
    elif field_name in referenced.fields:
        # Reference to specific field
        requires = validators.IS_IN_DB(
            db,
            getattr(referenced, field_name),
            label=getattr(referenced, "_format", None),
            multiple=is_list,
        )
```

**Features:**
- **Label Support**: Uses table's `_format` attribute for display
- **Multiple Selection**: Handles list:reference types
- **Field Validation**: Ensures referenced field exists

### Uniqueness for References
```python
if requires:
    if field_unique:
        requires._and = validators.IS_NOT_IN_DB(db, field)
```

Adds uniqueness validation to reference fields when unique=True.

## Options-Based Validation

### Predefined Options
```python
if isinstance(field.options, (list, tuple)):
    requires = validators.IS_IN_SET(field.options, multiple=is_list)
```

When field has predefined options, creates IS_IN_SET validator supporting:
- Static choice lists
- Multiple selection for list types
- Automatic option validation

## Type-Specific Validation

### String Fields
```python
if field_type in (("string", "text", "password")):
    requires.append(validators.IS_LENGTH(field.length))
```

**Validation:**
- **Length Constraint**: Enforces maximum field length
- **Applies to**: string, text, password fields

### Numeric Fields

#### Integer Types
```python
elif field_type == "integer":
    requires.append(validators.IS_INT_IN_RANGE(-(2**31), 2**31))
elif field_type == "bigint":
    requires.append(validators.IS_INT_IN_RANGE(-(2**63), 2**63))
```

**Features:**
- **Range Validation**: Prevents integer overflow
- **Type Conversion**: Automatically converts strings to integers
- **Database Compatibility**: Respects database integer limits

#### Floating Point
```python
elif field_type == "double" or field_type == "float":
    requires.append(validators.IS_FLOAT_IN_RANGE(-1e100, 1e100))
```

**Features:**
- **Scientific Notation**: Supports exponential format
- **Range Validation**: Prevents extreme values
- **Precision Handling**: Maintains decimal precision

#### Decimal Fields
```python
elif field_type.startswith("decimal"):
    requires.append(validators.IS_DECIMAL_IN_RANGE(-(10**10), 10**10))
```

**Features:**
- **Fixed-Point Math**: Precise decimal calculations
- **Scale Awareness**: Respects decimal precision settings
- **Financial Applications**: Suitable for monetary values

### Date and Time Fields
```python
elif field_type == "date":
    requires.append(validators.IS_DATE())
elif field_type == "time":
    requires.append(validators.IS_TIME())
elif field_type == "datetime":
    requires.append(validators.IS_DATETIME())
```

**Features:**
- **Format Validation**: Ensures proper date/time format
- **Type Conversion**: Converts strings to datetime objects
- **Timezone Awareness**: Handles timezone information

### JSON Fields
```python
elif field_type == "json":
    requires.append(validators.IS_EMPTY_OR(validators.IS_JSON()))
```

**Features:**
- **JSON Syntax**: Validates JSON format
- **Optional Values**: Allows empty/null values
- **Parse Validation**: Ensures valid JSON structure

## Constraint Handling

### Uniqueness Validation
```python
if field_unique:
    requires.insert(0, validators.IS_NOT_IN_DB(db, field))
```

**Features:**
- **Database Check**: Queries database for existing values
- **Insert Position**: Placed first in validation chain
- **Performance**: Optimized for duplicate detection

### Not Null Validation
```python
if (field_notnull or field_unique) and field_type not in (
    "boolean", "password", "string", "text", "upload",
):
    requires.insert(0, validators.IS_NOT_EMPTY())
```

**Logic:**
- **Required Fields**: field_notnull=True or field_unique=True
- **Type Exceptions**: Some types handle emptiness differently
- **Validation Order**: Checked before type-specific validation

### Null Handling
```python
elif not field_notnull and not field_unique and requires:
    null = "" if field.type == "password" else None
    requires[0] = validators.IS_EMPTY_OR(requires[0], null=null)
```

**Features:**
- **Optional Fields**: Allows null/empty values when permitted
- **Password Special Case**: Uses empty string instead of None
- **Wrapper Validation**: Wraps existing validators

## Validator Composition

### Single vs Multiple Validators
```python
if len(requires) == 1:
    requires = requires[0]
```

**Logic:**
- **Single Validator**: Returns validator directly
- **Multiple Validators**: Returns list for sequential validation
- **Optimization**: Avoids unnecessary list wrapping

### Validation Chain
When multiple validators are present, they execute in order:
1. **IS_NOT_EMPTY** (if required)
2. **IS_NOT_IN_DB** (if unique)
3. **Type-specific validator** (IS_LENGTH, IS_INT_IN_RANGE, etc.)

## Usage Examples

### Basic Field Types
```python
# String field with length validation
Field('name', 'string', length=100)
# Generates: IS_LENGTH(100)

# Required integer field
Field('age', 'integer', notnull=True)
# Generates: [IS_NOT_EMPTY(), IS_INT_IN_RANGE(-(2**31), 2**31)]

# Unique email field
Field('email', 'string', unique=True)
# Generates: IS_NOT_IN_DB(db, field)
```

### Reference Fields
```python
# Foreign key reference
Field('user_id', 'reference auth_user')
# Generates: IS_IN_DB(db, db.auth_user.id)

# Multiple references
Field('categories', 'list:reference category')
# Generates: IS_IN_DB(db, db.category.id, multiple=True)

# Unique reference
Field('profile_id', 'reference profile', unique=True)
# Generates: IS_IN_DB(db, db.profile.id)._and = IS_NOT_IN_DB(db, field)
```

### Optional Fields
```python
# Optional date field
Field('birthday', 'date')
# Generates: IS_EMPTY_OR(IS_DATE())

# Optional JSON field
Field('metadata', 'json')
# Generates: IS_EMPTY_OR(IS_JSON())
```

## Integration Points

### PyDAL Field System
- Automatically called during table definition
- Integrates with field constraint system
- Respects field properties and options

### Validation Framework
- Uses comprehensive validator library
- Supports custom validator chaining
- Enables form validation integration

### Database Adapters
- Works with all PyDAL database adapters
- Handles database-specific constraints
- Maintains referential integrity

## Benefits

### Automatic Validation
- **Zero Configuration**: Works out of the box
- **Type Safety**: Prevents invalid data entry
- **Database Integrity**: Maintains referential constraints

### Consistency
- **Standardized Rules**: Consistent validation across applications
- **Best Practices**: Implements common validation patterns
- **Error Prevention**: Reduces runtime database errors

### Flexibility
- **Override Support**: Can be overridden with custom validators
- **Extension Points**: Works with custom field types
- **Composition**: Supports complex validation scenarios

## Notes
- Central component of PyDAL's data integrity system
- Provides intelligent defaults for all field types
- Essential for maintaining database consistency
- Integrates seamlessly with web2py's form system
- Supports both simple and complex validation scenarios
- Critical for preventing invalid data entry