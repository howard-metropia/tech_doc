# Gluon Contrib Heroku Module

## Overview
Heroku platform integration module for web2py applications. Provides automatic database configuration for Heroku PostgreSQL databases with optimized adapter that stores file uploads in database BLOBs instead of filesystem.

## Module Information
- **Module**: `gluon.contrib.heroku`
- **Purpose**: Heroku deployment support
- **Dependencies**: `pydal.adapters`, `pydal.helpers.classes`
- **Platform**: Heroku cloud platform

## Key Features
- **Auto-configuration**: Automatic detection of Heroku PostgreSQL databases
- **Custom Adapter**: Enhanced PostgreSQL adapter with BLOB file storage
- **Environment Integration**: Uses Heroku environment variables
- **Fallback Support**: SQLite fallback for local development
- **Session Integration**: Automatic session-database connection

## Custom Database Adapter

### HerokuPostgresAdapter
Enhanced PostgreSQL adapter optimized for Heroku deployment.

**Class Definition:**
```python
@adapters.register_for('postgres')
class HerokuPostgresAdapter(DatabaseStoredFile, PostgrePsyco):
    uploads_in_blob = True
```

**Features:**
- **DatabaseStoredFile**: File uploads stored in database BLOBs
- **PostgrePsyco**: PostgreSQL-specific optimizations
- **BLOB Storage**: `uploads_in_blob = True` forces file storage in database
- **Adapter Registration**: Registered as 'postgres' adapter

**Benefits:**
- **Heroku Compatibility**: No persistent filesystem on Heroku
- **Scalability**: Files stored with data for consistency
- **Backup Integration**: Files included in database backups

## Main Function

### get_db()
Automatically configure database connection based on Heroku environment.

**Signature:**
```python
def get_db(name=None, pool_size=10)
```

**Parameters:**
- `name`: Environment variable name for database URL (optional)
- `pool_size`: Database connection pool size (default: 10)

**Returns:**
- Configured DAL database instance

**Auto-detection Logic:**
1. If `name` not provided, searches for Heroku PostgreSQL environment variables
2. Looks for variables matching pattern: `HEROKU_POSTGRESQL_*_URL`
3. Uses first found PostgreSQL URL
4. Falls back to SQLite if no PostgreSQL found

## Environment Variable Detection

### Heroku PostgreSQL Pattern
Heroku PostgreSQL add-ons create environment variables like:
- `HEROKU_POSTGRESQL_BLUE_URL`
- `HEROKU_POSTGRESQL_RED_URL`
- `HEROKU_POSTGRESQL_GREEN_URL`
- etc.

### Detection Algorithm
```python
names = [n for n in os.environ.keys()
         if n[:18]+n[-4:]=='HEROKU_POSTGRESQL__URL']
```

This finds variables that:
- Start with `HEROKU_POSTGRESQL_`
- End with `_URL`
- Have any color name in between

## Usage Examples

### Basic Usage
```python
# In models/db.py
from gluon.contrib.heroku import get_db
db = get_db()

# Database is now configured automatically
# - PostgreSQL on Heroku
# - SQLite locally for testing
```

### Explicit Database Selection
```python
# Specify exact Heroku database
db = get_db(name='HEROKU_POSTGRESQL_BLUE_URL')

# Custom pool size for high-traffic apps
db = get_db(pool_size=20)
```

### Complete Application Setup
```python
# models/db.py
from gluon.contrib.heroku import get_db

# Get database connection
db = get_db()

# Define tables normally
db.define_table('users',
    Field('name', 'string'),
    Field('email', 'string'),
    Field('avatar', 'upload'),  # Will be stored in database BLOB
)

# Session will be connected to database automatically
```

## File Upload Handling

### BLOB Storage
With `uploads_in_blob = True`, file uploads are stored in database:

```python
# File upload field
db.define_table('documents',
    Field('title', 'string'),
    Field('document', 'upload'),  # Stored in PostgreSQL BLOB
    Field('image', 'upload'),     # Also stored in database
)

# Upload handling works normally
def upload_document():
    form = FORM(
        INPUT(_type='file', _name='document'),
        INPUT(_type='submit', _value='Upload')
    )
    
    if form.process().accepted:
        # File automatically stored in database
        doc_id = db.documents.insert(
            title=request.vars.title,
            document=request.vars.document
        )
        redirect(URL('view_document', args=[doc_id]))
    
    return dict(form=form)
```

### File Retrieval
```python
def download():
    # Standard web2py download function works with BLOB storage
    return response.download(request, db)

def view_document():
    doc_id = request.args(0)
    document = db.documents[doc_id]
    
    # Generate download URL
    download_url = URL('download', args=[document.document])
    
    return dict(document=document, download_url=download_url)
```

## Deployment Configuration

### Heroku Setup
```bash
# Add PostgreSQL to Heroku app
heroku addons:create heroku-postgresql:hobby-dev

# Check database URL
heroku config:get DATABASE_URL

# The URL is automatically available as HEROKU_POSTGRESQL_*_URL
```

### Environment Variables
Heroku automatically provides:
```bash
DATABASE_URL=postgres://user:pass@host:port/db
HEROKU_POSTGRESQL_BLUE_URL=postgres://user:pass@host:port/db
```

### Local Development
```python
# Set environment variable for local testing
import os
os.environ['HEROKU_POSTGRESQL_BLUE_URL'] = 'postgres://localhost/myapp'

# Or use SQLite fallback
# Module automatically falls back to SQLite if no PostgreSQL found
```

## Session Integration

### Automatic Connection
The module automatically connects sessions to the database:
```python
current.session.connect(current.request, current.response, db=db)
```

This means:
- Sessions stored in database instead of filesystem
- Better for Heroku's ephemeral filesystem
- Scalable across multiple dynos

### Session Configuration
```python
# Additional session configuration
def configure_session():
    if current.session.db:
        # Session is database-backed
        current.session.forget()  # Optional: don't auto-save
```

## Performance Considerations

### Connection Pooling
```python
# Adjust pool size based on dyno type
# Standard dyno: pool_size=10
# Performance dynos: pool_size=20
db = get_db(pool_size=20)
```

### File Storage Trade-offs
**BLOB Storage Advantages:**
- No filesystem dependencies
- Consistent with database backups
- Transactional file operations

**BLOB Storage Disadvantages:**
- Larger database size
- Potential memory usage for large files
- Slower file serving compared to CDN

## Error Handling

### Database Connection Errors
```python
def get_db_safe():
    try:
        db = get_db()
        # Test connection
        db.executesql('SELECT 1')
        return db
    except Exception as e:
        # Log error and use fallback
        current.logger.error("Database connection failed: %s" % e)
        return DAL('sqlite://fallback.db')
```

### Environment Variable Issues
```python
def debug_heroku_vars():
    # Debug Heroku PostgreSQL variables
    pg_vars = [k for k in os.environ.keys() 
               if 'POSTGRESQL' in k]
    for var in pg_vars:
        print("%s = %s" % (var, os.environ[var]))
```

## Migration from Standard Setup

### Before (Standard web2py)
```python
# models/db.py
db = DAL('postgres://user:pass@localhost/myapp')
```

### After (Heroku-optimized)
```python
# models/db.py
from gluon.contrib.heroku import get_db
db = get_db()
```

### File Upload Migration
Existing file uploads on filesystem need migration:
```python
def migrate_uploads():
    # Migrate existing filesystem uploads to database
    for record in db(db.documents.document != None).select():
        if record.document:
            # File will be re-stored in database on next update
            record.update_record()
```

## Best Practices

### Configuration
```python
# Use environment-specific settings
if request.env.server_name == 'localhost':
    # Local development
    db = DAL('sqlite://local.db')
else:
    # Production on Heroku
    db = get_db()
```

### File Handling
```python
# Optimize for BLOB storage
db.define_table('files',
    Field('name', 'string'),
    Field('content', 'upload'),
    Field('size', 'integer'),  # Store file size for optimization
    Field('content_type', 'string'),  # Store MIME type
)
```

### Monitoring
```python
# Monitor database connections
def check_db_health():
    try:
        result = db.executesql('SELECT version()')
        return True
    except:
        return False
```

This module provides seamless Heroku deployment support for web2py applications with optimized PostgreSQL integration and automatic configuration based on Heroku's environment variables.