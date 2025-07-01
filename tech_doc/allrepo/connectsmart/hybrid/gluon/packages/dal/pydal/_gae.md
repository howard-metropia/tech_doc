# _gae.py

## Overview
Google App Engine compatibility module for PyDAL that provides conditional imports for GAE-specific modules and handles environments where GAE is not available.

## Import Strategy
Uses try/except pattern to gracefully handle GAE availability:

```python
try:
    # GAE-specific imports
except ImportError:
    # Fallback for non-GAE environments
```

## GAE Imports (When Available)

### Core GAE Modules
- **`new.classobj`**: Dynamic class creation for legacy Python support
- **`google.appengine.ext.db as gae`**: Original GAE datastore API
- **`google.appengine.ext.ndb`**: Next-generation datastore API (NDB)

### GAE Services
- **`google.appengine.api.namespace_manager`**: Multi-tenancy namespace support
- **`google.appengine.api.rdbms`**: Google Cloud SQL integration
- **`google.appengine.api.datastore_types.Key`**: Datastore key handling

### Advanced Features
- **`google.appengine.ext.ndb.polymodel.PolyModel as NDBPolyModel`**: Inheritance support for NDB models

## Fallback Behavior (Non-GAE Environments)
When GAE modules are not available:
```python
gae = None
Key = None
```

Sets critical GAE objects to None, allowing PyDAL to:
- Detect GAE availability through None checks
- Gracefully disable GAE-specific functionality
- Continue operating in standard environments

## Usage in PyDAL

### Conditional GAE Support
Other PyDAL modules can check for GAE availability:
```python
from ._gae import gae, Key

if gae is not None:
    # Use GAE-specific functionality
    pass
else:
    # Use standard database adapters
    pass
```

### Adapter Selection
Enables PyDAL to automatically choose appropriate database adapter:
- **GAE Available**: Use GAE datastore adapter
- **GAE Not Available**: Use traditional SQL adapters

### Key Type Handling
The Key import enables proper handling of GAE datastore keys:
- Used for relationship queries (`belongs` operations)
- Enables proper key validation and conversion
- Supports GAE's unique key-based architecture

## GAE Integration Features

### Datastore APIs
- **Original DB API**: Legacy datastore interface
- **NDB API**: Modern datastore interface with async support
- **Polymodel Support**: Object inheritance in datastore

### Cloud Services
- **Namespace Manager**: Multi-tenant application support
- **Cloud SQL**: Relational database integration
- **Key Types**: Datastore-specific key handling

## Error Handling
The ImportError pattern ensures:
- No crashes in non-GAE environments
- Clean degradation of GAE features
- Compatibility across deployment platforms

## Notes
- Essential for PyDAL's multi-platform support
- Enables same codebase to run on GAE and traditional servers
- Provides foundation for GAE-specific database adapters
- Handles both legacy (db) and modern (ndb) GAE datastore APIs
- Critical for Google Cloud Platform deployment compatibility