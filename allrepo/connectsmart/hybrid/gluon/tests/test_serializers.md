# test_serializers.py

## Overview
This file contains unit tests for web2py's data serialization system. It tests various serialization formats including JSON, XML, CSV, and custom serializers for converting Python objects to different data interchange formats.

## Purpose
- Tests JSON serialization and deserialization
- Validates XML data conversion functionality
- Tests CSV export and import capabilities
- Verifies custom serializer functionality
- Tests database record serialization
- Ensures proper data type handling across formats

## Key Features Tested

### JSON Serialization
- **Object Conversion**: Python objects to JSON format
- **Database Records**: DAL records to JSON
- **Custom Types**: Date/time and decimal handling
- **Unicode Support**: Proper Unicode string handling

### XML Serialization
- **Structure Preservation**: Hierarchical data to XML
- **Attribute Handling**: XML attributes and elements
- **CDATA Support**: Raw data handling in XML
- **Namespace Support**: XML namespace handling

### CSV Serialization
- **Table Export**: Database tables to CSV
- **Custom Delimiters**: Configurable field separators
- **Header Handling**: Column header management
- **Data Escaping**: Proper CSV data escaping

### Custom Serializers
- **Extensibility**: Custom serialization formats
- **Format Registration**: Dynamic serializer registration
- **Type Conversion**: Custom type handling
- **Performance**: Efficient serialization algorithms

## Integration with web2py Framework

### Database Integration
- **Record Serialization**: Automatic DAL record conversion
- **Query Results**: Serializing query result sets
- **Relationship Handling**: Foreign key and reference serialization
- **Metadata Preservation**: Table and field metadata in serialized data

### API Development
- **REST APIs**: Automatic response serialization
- **Content Negotiation**: Format selection based on request headers
- **Error Serialization**: Structured error response formats
- **Pagination**: Serialized pagination metadata

### Data Exchange
- **Import/Export**: Application data exchange
- **Backup/Restore**: Database backup in various formats
- **Migration**: Data migration between systems
- **Integration**: Third-party system integration

## Usage Example
```python
from gluon.serializers import json, xml, csv
from gluon.dal import DAL, Field

# Database setup
db = DAL('sqlite://test.db')
db.define_table('users', Field('name'), Field('email'))
db.users.insert(name='John', email='john@example.com')

# JSON serialization
users = db(db.users).select()
json_data = users.as_json()
print(json_data)  # [{'id': 1, 'name': 'John', 'email': 'john@example.com'}]

# XML serialization
xml_data = users.as_xml()
print(xml_data)  # <users><user><name>John</name><email>john@example.com</email></user></users>

# CSV serialization
csv_data = users.as_csv()
print(csv_data)  # id,name,email\n1,John,john@example.com
```

This test suite ensures web2py's serialization system provides reliable, efficient data conversion capabilities for various interchange formats and integration scenarios.