# Gluon Contrib Hypermedia Module

## Overview
Collection+JSON hypermedia API framework for web2py applications. This module implements the Collection+JSON specification to create RESTful APIs with hypermedia controls, providing self-describing APIs that support discovery and navigation.

## Module Information
- **Module**: `gluon.contrib.hypermedia`
- **Specification**: Collection+JSON (https://github.com/collection-json/spec)
- **Extensions**: Collection-Next-JSON compatible
- **Dependencies**: `gluon.URL`, `gluon.IS_SLUG`, `collections.OrderedDict`

## Key Features
- **Hypermedia API**: Self-describing RESTful APIs with navigation links
- **Policy-Driven**: Configurable field access and method permissions
- **Database Integration**: Direct web2py DAL integration
- **Query Support**: Rich query interface with filtering and pagination
- **Template Generation**: Automatic form templates from database schema
- **Link Generation**: Automatic relationship link discovery

## Main Class

### Collection
Primary class that processes HTTP requests and generates Collection+JSON responses.

**Constructor:**
```python
def __init__(self, db, extensions=True, compact=False)
```

**Parameters:**
- `db`: Web2py database instance
- `extensions`: Enable Collection+JSON extensions (default: True)
- `compact`: Use compact data representation (default: False)

**Constants:**
- `VERSION`: '1.0' - Collection+JSON version
- `MAXITEMS`: 100 - Maximum items per response

## Core Methods

### process()
Main request processing method that handles HTTP requests and generates JSON responses.

**Signature:**
```python
def process(self, request, response, policies=None)
```

**Parameters:**
- `request`: Web2py request object
- `response`: Web2py response object  
- `policies`: Dictionary defining table access policies

**Returns:**
- JSON response with Collection+JSON format

**HTTP Methods Supported:**
- GET: Retrieve resources
- POST: Create resources
- PUT: Update resources
- DELETE: Delete resources

### row2data()
Convert database row to Collection+JSON data representation.

**Signature:**
```python
def row2data(self, table, row, text=False)
```

**Parameters:**
- `table`: Database table object
- `row`: Database row object
- `text`: Include text fields (default: False)

**Returns:**
- List/dict of field data based on compact setting

**Compact Mode:**
- Returns simple list of values
- Excludes field metadata

**Standard Mode:**
- Returns list of objects with name, value, prompt, type
- Includes field metadata for client validation

### row2links()
Generate hypermedia links for database relationships.

**Signature:**
```python
def row2links(self, table, row)
```

**Parameters:**
- `table`: Database table object
- `row`: Database row object

**Returns:**
- List of link objects with rel, href, prompt, type

**Link Types:**
- **children**: Links to referencing tables
- **parent**: Links to referenced tables  
- **attachment**: Links to file uploads
- **custom**: Policy-defined custom links

### table2template()
Generate form template from database table schema.

**Signature:**
```python
def table2template(self, table)
```

**Includes:**
- Field validation rules
- Required field indicators
- POST/PUT writability flags
- Field type information
- Regular expression validators

### request2query()
Parse HTTP request parameters into database query.

**Supported Parameters:**
- `_offset`: Pagination offset
- `_limit`: Maximum items returned
- `_orderby`: Sort field
- `field`: Exact field match
- `field.eq`: Equal comparison
- `field.lt`: Less than comparison
- `field.le`: Less than or equal
- `field.gt`: Greater than comparison
- `field.ge`: Greater than or equal
- `field.contains`: String contains
- `field.startswith`: String starts with

## Policy Configuration

### Policy Structure
```python
policies = {
    'table_name': {
        'GET': {
            'query': None,  # Custom query filter
            'fields': ['id', 'name', 'description']  # Accessible fields
        },
        'POST': {
            'query': None,
            'fields': ['name', 'description']  # Writable fields
        },
        'PUT': {
            'query': None,
            'fields': ['name', 'description']
        },
        'DELETE': {
            'query': None
        }
    }
}
```

### Field Access Control  
- **GET fields**: Readable fields in responses
- **POST fields**: Writable fields for creation
- **PUT fields**: Writable fields for updates
- **DELETE**: No field restrictions

### Custom Links
```python
policies = {
    'users': {
        'GET': {
            'fields': ['id', 'name', 'email'],
            'links': {
                'profile': lambda row: URL('profile', args=[row.id]),
                'avatar': lambda row: URL('avatar', args=[row.id])
            }
        }
    }
}
```

## Usage Examples

### Basic Controller Setup
```python
def api():
    from gluon.contrib.hypermedia import Collection
    
    policies = {
        'users': {
            'GET': {'query': None, 'fields': ['id', 'name', 'email']},
            'POST': {'query': None, 'fields': ['name', 'email', 'password']},
            'PUT': {'query': None, 'fields': ['name', 'email']},
            'DELETE': {'query': None}
        },
        'posts': {
            'GET': {'query': None, 'fields': ['id', 'title', 'content', 'user']},
            'POST': {'query': None, 'fields': ['title', 'content', 'user']},
            'PUT': {'query': None, 'fields': ['title', 'content']},
            'DELETE': {'query': None}
        }
    }
    
    return Collection(db).process(request, response, policies)
```

### API Discovery
```bash
# GET /app/api
# Returns list of available resources
{
  "collection": {
    "version": "1.0",
    "href": "/app/api",
    "links": [
      {"rel": "users", "href": "/app/api/users", "model": "users"},
      {"rel": "posts", "href": "/app/api/posts", "model": "posts"}
    ]
  }
}
```

### Resource Collection
```bash
# GET /app/api/users
{
  "collection": {
    "version": "1.0", 
    "href": "/app/api/users",
    "items": [
      {
        "href": "/app/api/users/1",
        "data": [
          {"name": "id", "value": 1, "prompt": "ID"},
          {"name": "name", "value": "John", "prompt": "Name"},
          {"name": "email", "value": "john@example.com", "prompt": "Email"}
        ],
        "links": [
          {"rel": "current", "href": "/app/api/posts?user=1", "type": "children"}
        ]
      }
    ],
    "template": {
      "data": [
        {"name": "name", "prompt": "Name", "required": true},
        {"name": "email", "prompt": "Email", "required": true}
      ]
    }
  }
}
```

### Query Filtering
```bash
# GET /app/api/users?name.contains=john&_limit=10&_offset=0
# Returns users with names containing 'john', limited to 10 items

# GET /app/api/posts?created.gt=2023-01-01&_orderby=created
# Returns posts created after 2023-01-01, ordered by creation date
```

### Resource Creation
```bash
# POST /app/api/users
# Content-Type: application/json
{
  "template": {
    "data": [
      {"name": "name", "value": "Jane Doe"},
      {"name": "email", "value": "jane@example.com"}
    ]
  }
}
```

## Advanced Configuration

### Custom Query Filters
```python
policies = {
    'users': {
        'GET': {
            'query': lambda: db.users.active == True,
            'fields': ['id', 'name', 'email']
        }
    }
}
```

### Relationship Handling
```python
# Database setup
db.define_table('users',
    Field('name', 'string'),
    Field('email', 'string')
)

db.define_table('posts', 
    Field('title', 'string'),
    Field('content', 'text'),
    Field('user', 'reference users')
)

# API automatically generates:
# - Parent links from posts to users
# - Children links from users to posts
```

### File Upload Support
```python
db.define_table('documents',
    Field('title', 'string'),
    Field('file', 'upload')
)

# API automatically generates download links for upload fields
# Link type: 'attachment'
# href: /app/default/download/filename
```

## Response Format Details

### Collection Structure
```json
{
  "collection": {
    "version": "1.0",
    "href": "resource_url",
    "items": [...],
    "links": [...],
    "template": {...},
    "items_found": 42
  }
}
```

### Item Structure
```json
{
  "href": "item_url",
  "data": [
    {"name": "field", "value": "value", "prompt": "Label", "type": "string"}
  ],
  "links": [
    {"rel": "current", "href": "related_url", "type": "parent|children|attachment"}
  ]
}
```

### Template Structure
```json
{
  "data": [
    {
      "name": "field_name",
      "value": "",
      "prompt": "Field Label", 
      "type": "string",
      "required": true,
      "post_writable": true,
      "put_writable": true,
      "regexp": "validation_pattern"
    }
  ]
}
```

## Error Handling

### HTTP Status Codes
- **200**: Successful GET request
- **201**: Successful POST (creation)
- **204**: Successful PUT/DELETE
- **400**: Bad request (invalid query, missing fields)
- **404**: Resource not found
- **405**: Method not allowed

### Error Response Format
```json
{
  "collection": {
    "version": "1.0",
    "error": {
      "title": "Bad Request",
      "code": "400", 
      "message": "Invalid query parameters"
    }
  }
}
```

## Performance Considerations

### Pagination
- Default limit: 100 items
- Use `_offset` and `_limit` for pagination
- `items_found` indicates total matching records

### Field Filtering
- Only policy-defined fields are included
- Excludes text, blob, and reference fields by default
- Configurable through field policies

### Query Optimization
- Leverages web2py DAL query optimization
- Supports database-specific optimizations
- Uses limitby for efficient pagination

This module provides a complete hypermedia API framework that transforms web2py applications into self-describing REST APIs following the Collection+JSON specification.