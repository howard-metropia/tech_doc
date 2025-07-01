# Activity Type Controller API Documentation

## Overview
The Activity Type Controller manages activity type metadata in the MaaS platform. It provides administrative functions for creating, reading, and updating activity type definitions that categorize different types of user activities within the system.

**File Path:** `/allrepo/connectsmart/hybrid/applications/portal/controllers/activity_type.py`

**Controller Type:** Administrative Portal Controller

**Authentication:** Requires Metropia role membership

## Features
- Activity type CRUD operations
- Administrative access control
- Pagination support for listing
- Duplicate name validation
- JSON response formatting

## API Endpoints

### Activity Type Management
**Endpoint:** `/activity_type/maintain`
**Methods:** GET, POST, PUT
**Authentication:** Login required, Metropia role

#### GET - List Activity Types
Retrieves activity types with optional filtering and pagination.

**Parameters:**
- `activity_id` (optional): Specific activity type ID to retrieve
- `offset` (optional): Starting offset for pagination (default: 0)
- `perpage` (optional): Items per page (default: 10)

**Response Format:**
```json
{
  "success": true,
  "data": {
    "activity_types": [
      {
        "id": 1,
        "name": "Commuting",
        "description": "Daily commute activities"
      }
    ],
    "total_count": 15,
    "next_offset": 10
  }
}
```

**Status Codes:**
- `200`: Success
- `400`: Invalid parameters

#### POST - Create Activity Type
Creates a new activity type definition.

**Required Fields:**
- `name`: Activity type name (must be unique)

**Optional Fields:**
- `description`: Activity type description

**Validation:**
- Checks for duplicate activity type names
- Validates required fields

**Response Format:**
```json
{
  "success": true,
  "data": {
    "id": 5
  }
}
```

**Status Codes:**
- `201`: Created successfully
- `400`: Invalid parameters or request body
- `403`: Duplicate activity type name

**Headers:**
- `Location`: URL of newly created resource

#### PUT - Update Activity Type
Updates an existing activity type.

**URL Parameter:**
- `activity_id`: ID of activity type to update

**Required Fields:**
- `name`: Updated activity type name
- `description`: Updated activity type description

**Validation:**
- Prevents duplicate names (excluding current record)
- Validates required fields

**Response Format:**
```json
{
  "success": true
}
```

**Status Codes:**
- `200`: Updated successfully
- `400`: Invalid parameters or request body
- `403`: Duplicate activity type name

## Data Model

### Activity Type Structure
```python
{
    "id": int,                    # Auto-generated primary key
    "name": str,                  # Unique activity type name
    "description": str,           # Activity type description
    "created_on": datetime,       # Creation timestamp
    "modified_on": datetime       # Last modification timestamp
}
```

## Database Schema

### Table: activity_type
- `id` (PRIMARY KEY): Auto-increment identifier
- `name` (UNIQUE): Activity type name
- `description`: Descriptive text
- `created_on`: Record creation timestamp
- `modified_on`: Record modification timestamp

## Authentication & Authorization

### Access Control
- **Login Required**: All endpoints require authenticated user
- **Role Required**: Metropia membership role
- **Scope**: Administrative functions only

### Security Features
- Parameter validation and sanitization
- SQL injection prevention through ORM
- Role-based access control
- Timestamp tracking for audit trails

## Error Handling

### Error Codes
- `ERROR_BAD_REQUEST_PARAMS`: Invalid URL parameters
- `ERROR_BAD_REQUEST_BODY`: Invalid request body
- `ERROR_DUPLICATE_ACTIVITY_TYPE`: Duplicate activity type name

### Error Response Format
```json
{
  "success": false,
  "error_code": "ERROR_DUPLICATE_ACTIVITY_TYPE",
  "message": "Duplicate activity type name"
}
```

## Implementation Details

### Key Functions
- **verify_required_fields()**: Validates required field presence
- **request.utcnow**: UTC timestamp generation
- **json_response**: Standardized JSON response formatting

### Database Operations
- **INSERT**: Creates new activity types with timestamps
- **SELECT**: Retrieves activity types with pagination
- **UPDATE**: Modifies existing records with timestamp update
- **COUNT**: Validates uniqueness constraints

### Pagination Logic
- Calculates `next_offset` based on total count and page size
- Handles edge cases when total count is less than requested page
- Provides consistent pagination across all list operations

## Usage Examples

### Create Activity Type
```bash
curl -X POST /activity_type/maintain \
  -H "Content-Type: application/json" \
  -d '{"name": "Recreation", "description": "Recreational activities"}'
```

### List Activity Types
```bash
curl -X GET "/activity_type/maintain?offset=0&perpage=5"
```

### Update Activity Type
```bash
curl -X PUT /activity_type/maintain/3 \
  -H "Content-Type: application/json" \
  -d '{"name": "Business Travel", "description": "Business-related travel activities"}'
```

## Integration Points

### Related Systems
- **Activity Tracking**: Used to categorize user activities
- **Analytics**: Provides grouping for activity reports
- **User Interface**: Populates activity type dropdowns

### Data Dependencies
- Links to user activity records
- Referenced by activity logging systems
- Used in reporting and analytics queries

## Performance Considerations

### Optimization Features
- Indexed name field for uniqueness checks
- Pagination to limit result set size
- Efficient duplicate validation queries

### Scalability Notes
- Simple table structure supports high-volume operations
- Caching recommended for frequently accessed types
- Consider read replicas for high-read scenarios

## Maintenance Notes

### Regular Tasks
- Monitor for duplicate creation attempts
- Review activity type usage patterns
- Archive unused activity types if needed

### Troubleshooting
- Check role permissions for access issues
- Validate uniqueness constraints for creation failures
- Monitor timestamp consistency for audit requirements