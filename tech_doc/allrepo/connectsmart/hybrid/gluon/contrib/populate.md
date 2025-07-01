# Gluon Contrib Populate Module

## Overview
Database table population utilities for web2py applications. Provides automated generation of realistic test data using various strategies including Markov chain text generation, random name selection, and custom field population patterns.

## Module Information
- **Module**: `gluon.contrib.populate`
- **Dependencies**: `pydal`, `pickle`, `random`, `datetime`, `re`
- **Purpose**: Test data generation and database population
- **Use Case**: Development, testing, demonstrations

## Key Features
- **Automatic Population**: Generate realistic test data for any web2py table
- **Text Generation**: Markov chain-based Lorem Ipsum text generation
- **Name Generation**: Random first/last name selection from extensive lists
- **Field Type Support**: Handles all web2py field types appropriately
- **Relationship Support**: Respects foreign key relationships
- **Configurable**: Flexible population parameters and options

## Main Functions

### populate()
Primary function to populate database tables with test data.

**Signature:**
```python
def populate(table, n=None, default=True, compute=False, contents=None, ell=None)
```

**Parameters:**
- `table`: Web2py table object to populate
- `n`: Number of records to generate (None returns generator)
- `default`: Use field default values (default: True)
- `compute`: Include computed fields (default: False)
- `contents`: Custom content generation dictionary
- `ell`: Learner instance for text generation

**Returns:**
- Generator if `n` is None
- List of inserted record IDs if `n` specified

**Example:**
```python
from gluon.contrib.populate import populate

# Populate 100 records
populate(db.users, n=100)

# Use generator for memory efficiency
for record_data in populate(db.users):
    # Process each record
    if some_condition:
        break
```

### populate_generator()
Generator version that yields individual record data.

**Signature:**
```python
def populate_generator(table, default=True, compute=False, contents=None, ell=None)
```

## Text Generation Classes

### Learner
Markov chain text generator that learns from sample text and generates similar content.

**Methods:**
- `learn(text)`: Learn patterns from input text
- `generate(length, prefix)`: Generate text of specified length
- `save(filename)`: Save learned patterns to file
- `load(filename)`: Load patterns from file

**Example:**
```python
from gluon.contrib.populate import Learner

# Create and train learner
learner = Learner()
learner.learn("Sample text to learn patterns from...")

# Generate text
generated_text = learner.generate(length=500)

# Save/load patterns
learner.save('patterns.pkl')
learner.load('patterns.pkl')
```

## Built-in Data Sources

### Names
The module includes extensive name lists:
- **FIRST_NAMES**: 200+ common first names
- **LAST_NAMES**: 200+ common last names

### Lorem Ipsum
- **IUP**: Pre-trained Markov chain dictionary for Lorem Ipsum generation

## Usage Examples

### Basic Table Population
```python
# Define table
db.define_table('users',
    Field('first_name', 'string'),
    Field('last_name', 'string'),
    Field('email', 'string'),
    Field('age', 'integer'),
    Field('created_on', 'datetime')
)

# Populate with 50 records
populate(db.users, n=50)

# Check results
print("Total users:", db(db.users).count())
```

### Custom Content Generation
```python
# Custom content patterns
contents = {
    'email': lambda: '%s@example.com' % da_du_ma(6),
    'age': lambda: random.randint(18, 80),
    'bio': lambda: learner.generate(length=100)
}

# Populate with custom content
populate(db.users, n=25, contents=contents)
```

### Large Dataset Generation
```python
# Memory-efficient population of large datasets
count = 0
for record_data in populate(db.large_table):
    # Insert in batches
    if count % 1000 == 0:
        db.commit()
        print(f"Inserted {count} records")
    
    count += 1
    if count >= 100000:  # Stop at 100k records
        break

db.commit()
```

### Multi-table Population with Relationships
```python
# Parent table
db.define_table('categories',
    Field('name', 'string'),
    Field('description', 'text')
)

# Child table with reference
db.define_table('products',
    Field('name', 'string'),
    Field('price', 'decimal(10,2)'),
    Field('category', 'reference categories')
)

# Populate parent first
populate(db.categories, n=10)

# Populate child with automatic foreign key assignment
populate(db.products, n=100)
```

## Field Type Handling

### Automatic Field Population
The module automatically generates appropriate data for each field type:

```python
# String fields
'string': random choice from appropriate word lists

# Integer fields  
'integer': random integers within reasonable ranges

# Decimal/Float fields
'decimal': random decimal values
'double': random floating point numbers

# Date/Time fields
'date': random dates within date ranges
'datetime': random datetime values
'time': random time values

# Boolean fields
'boolean': random True/False values

# Text fields
'text': generated using Markov chain text generation

# Reference fields
'reference': random selection from referenced table records

# Upload fields
'upload': placeholder filenames or None
```

### Custom Field Generators
```python
def custom_email_generator():
    """Generate realistic email addresses"""
    domains = ['gmail.com', 'yahoo.com', 'company.com']
    username = da_du_ma(random.randint(4, 8))
    domain = random.choice(domains)
    return f"{username}@{domain}"

def custom_phone_generator():
    """Generate phone numbers"""
    return f"({random.randint(100,999)}) {random.randint(100,999)}-{random.randint(1000,9999)}"

# Use with contents parameter
contents = {
    'email': custom_email_generator,
    'phone': custom_phone_generator
}

populate(db.contacts, n=100, contents=contents)
```

## Text Generation Utilities

### da_du_ma()
Generate random syllable-based strings.

**Signature:**
```python
def da_du_ma(n=4)
```

**Parameters:**
- `n`: Number of syllables (default: 4)

**Returns:**
- Random string of syllables

**Example:**
```python
# Generate random usernames
username = da_du_ma(3)  # e.g., 'maduposa'
email = f"{da_du_ma(4)}@example.com"
```

### Advanced Text Generation
```python
# Train custom learner with domain-specific text
learner = Learner()

# Learn from product descriptions
product_descriptions = """
High-quality wireless headphones with noise cancellation.
Premium leather wallet with RFID protection.
Comfortable running shoes with advanced cushioning.
"""

learner.learn(product_descriptions)

# Generate product descriptions
def generate_product_description():
    return learner.generate(length=50)

contents = {
    'description': generate_product_description
}

populate(db.products, n=50, contents=contents)
```

## Performance Considerations

### Memory Management
```python
# For large datasets, use generator to control memory usage
def populate_large_table(table, total_records, batch_size=1000):
    """Populate large table in batches"""
    count = 0
    batch = []
    
    for record_data in populate_generator(table):
        batch.append(record_data)
        count += 1
        
        if len(batch) >= batch_size:
            # Insert batch
            table.bulk_insert(batch)
            batch = []
            db.commit()
            print(f"Inserted {count} records")
        
        if count >= total_records:
            break
    
    # Insert remaining records
    if batch:
        table.bulk_insert(batch)
        db.commit()

# Usage
populate_large_table(db.large_table, 1000000, batch_size=5000)
```

### Database Optimization
```python
# Disable constraints for faster insertion
db.executesql('SET FOREIGN_KEY_CHECKS = 0;')  # MySQL
# or
db.executesql('PRAGMA foreign_keys = OFF;')   # SQLite

# Populate data
populate(db.table, n=10000)

# Re-enable constraints
db.executesql('SET FOREIGN_KEY_CHECKS = 1;')  # MySQL
# or  
db.executesql('PRAGMA foreign_keys = ON;')    # SQLite
```

## Testing and Development

### Development Data Setup
```python
def setup_development_data():
    """Setup realistic development data"""
    
    # Clear existing data
    db(db.users.id > 0).delete()
    db(db.posts.id > 0).delete()
    
    # Populate base data
    populate(db.users, n=25)
    populate(db.categories, n=5)
    populate(db.posts, n=100)
    
    db.commit()
    print("Development data setup complete")

def setup_demo_data():
    """Setup demonstration data with specific content"""
    demo_users = [
        {'first_name': 'John', 'last_name': 'Doe', 'email': 'john@demo.com'},
        {'first_name': 'Jane', 'last_name': 'Smith', 'email': 'jane@demo.com'},
    ]
    
    for user_data in demo_users:
        db.users.insert(**user_data)
    
    # Populate remaining with random data
    populate(db.users, n=23)
    populate(db.posts, n=50)
```

### Unit Testing
```python
def test_populate_function():
    """Test populate function"""
    
    # Test basic population
    initial_count = db(db.test_table).count()
    populate(db.test_table, n=10)
    final_count = db(db.test_table).count()
    
    assert final_count == initial_count + 10
    
    # Test generator
    generator = populate(db.test_table)
    record_data = next(generator)
    assert isinstance(record_data, dict)
    
    print("Populate tests passed")
```

## Configuration and Customization

### Custom Learners
```python
# Train domain-specific text generators
def create_technical_learner():
    """Create learner for technical documentation"""
    learner = Learner()
    
    technical_text = """
    The API endpoint accepts HTTP requests and returns JSON responses.
    Authentication is required using API keys in the authorization header.
    Rate limiting applies to prevent abuse of the service.
    """
    
    learner.learn(technical_text)
    return learner

tech_learner = create_technical_learner()

contents = {
    'documentation': lambda: tech_learner.generate(length=200)
}
```

### Field-Specific Patterns
```python
# Create realistic data patterns
def create_realistic_contents():
    """Create realistic content generators"""
    
    companies = ['TechCorp', 'DataSys', 'WebSolutions', 'CloudFirst']
    departments = ['Engineering', 'Marketing', 'Sales', 'Support']
    
    return {
        'company': lambda: random.choice(companies),
        'department': lambda: random.choice(departments),
        'salary': lambda: random.randint(40000, 120000),
        'hire_date': lambda: datetime.date.today() - datetime.timedelta(
            days=random.randint(30, 1825)
        )
    }

populate(db.employees, n=100, contents=create_realistic_contents())
```

This module provides comprehensive database population capabilities for web2py applications, enabling rapid generation of realistic test data for development, testing, and demonstration purposes.