# test_router.py

## Overview
Comprehensive unit tests for Web2py's URL routing system (rewrite.py), testing various router configurations including null routers, default applications, and app-specific routing rules.

## Imports
```python
import logging
import os
import shutil
import tempfile
import unittest
from gluon._compat import PY2, to_bytes
from gluon.html import URL
from gluon.http import HTTP
from gluon.rewrite import filter_err, filter_url, get_effective_router, load, map_url_out
from gluon.settings import global_settings
from gluon.storage import Storage
```

## Module Setup/Teardown

### setUpModule()
Creates a temporary application tree for testing:

#### make_apptree(root)
Builds test application structure:
```
applications/
├── admin/
│   ├── controllers/
│   │   ├── appadmin.py
│   │   ├── default.py
│   │   ├── gae.py
│   │   ├── mercurial.py
│   │   ├── shell.py
│   │   └── wizard.py
│   └── static/
├── examples/
│   ├── controllers/
│   │   ├── ajax_examples.py
│   │   ├── appadmin.py
│   │   ├── default.py
│   │   ├── global.py
│   │   └── spreadsheet.py
│   ├── static/
│   │   ├── en/file
│   │   └── it/file
│   └── routes.py
└── welcome/
    ├── controllers/
    │   ├── admin.py
    │   ├── appadmin.py
    │   ├── default.py
    │   └── other.py
    └── static/
```

**Special Features:**
- Examples app has app-specific routes.py with `default_function='exdef'`
- Welcome app includes `admin.py` controller (collision with admin app)
- Language directories in examples app

### tearDownModule()
Restores original settings and removes temporary directory.

## Test Class: TestRouter

### Helper Methods

#### myassertRaisesRegex()
Python 2/3 compatibility wrapper for regex assertion methods.

#### norm_root()
Normalizes path separators for cross-platform testing.

### Test Methods

#### test_router_syntax()
Tests router configuration syntax validation:
- Invalid syntax in data string
- Unknown keys in router dict
- BASE-only keys used in app-specific config
- Temporarily disables logging to avoid noise

#### test_router_null()
Tests the null (empty) router configuration:

**App Resolution:**
- `/welcome` → `"welcome"` (app name)
- `/` → `"init"` (default app)

**Incoming URL Mapping:**
- `/favicon.ico` → static file path
- `/abc` → `/init/default/abc`
- `/index/abc` → `/init/default/index ['abc']`
- Static file validation (rejects invalid characters)

**Outgoing URL Mapping:**
- `/init/default/index` → `/`
- `/init/default/abc` → `/abc`
- Controller collision handling

#### test_router_specific()
Tests app-specific routes.py files:
- Welcome app uses default routing
- Examples app uses custom default_function from routes.py

#### test_router_defapp()
Tests default application configuration:

**Router Config:**
```python
routers = dict(BASE=dict(default_application='welcome'))
```

**Effects:**
- Root URL maps to welcome app
- Static files resolve to welcome app
- Shortened URLs for default app/controller/function

#### test_router_nodef()
Tests configurations with various defaults disabled:

**Test Cases:**

1. **No Default Function**
   - Controllers list set to None
   - `/welcome/default/index` → `/default`
   - Function name always required in URL

2. **No Default Application**
   - `default_application=None`
   - Root URL raises HTTP 400 error
   - App name always required

3. **No Applications List**
   - `applications=None`
   - Unknown apps raise HTTP 400
   - Strict application validation

4. **Combined Restrictions**
   - Multiple defaults disabled
   - Maximum URL verbosity

## URL Routing Patterns

### Incoming URL Processing (filter_url)
Maps external URLs to internal paths:
- Domain stripping
- Static file resolution
- Controller/function mapping
- Argument parsing

### Outgoing URL Processing (filter_url with out=True)
Shortens internal URLs for external use:
- Removes defaults (app/controller/function)
- Preserves necessary components
- Handles static URLs

### Special Cases

#### Static Files
- Direct file system mapping
- Security validation (no `~` characters)
- Path traversal prevention

#### Controller Collisions
- `admin` controller in welcome app
- Proper disambiguation in URLs

#### Arguments
- Space encoding/decoding (`%20`)
- List notation for extra arguments

## Router Configuration Options

### BASE Configuration
Global settings affecting all apps:
- `default_application`: Root URL app
- `applications`: Allowed apps list
- Other BASE-only keys

### App-Specific Configuration
Per-app routing rules:
- `default_controller`: Default controller name
- `default_function`: Default function name
- `controllers`: Allowed controllers list

### App-Specific routes.py
Alternative configuration method:
- Python file in app directory
- Overrides global router settings
- Example: `routers=dict(examples=dict(default_function='exdef'))`

## Error Handling

### HTTP Exceptions
- 400 Bad Request for invalid apps
- 400 Bad Request for invalid static files
- Detailed error messages with regex matching

### Syntax Errors
- Invalid router syntax
- Unknown configuration keys
- Misplaced BASE-only keys

## Testing Strategy

### Comprehensive Coverage
- All router configuration combinations
- Edge cases and error conditions
- Both incoming and outgoing URLs

### Isolation
- Temporary directory for tests
- No interference with actual apps
- Logger level management

### Cross-Platform
- Path separator normalization
- OS-independent assertions

## Notes
- Tests demonstrate URL shortening strategies
- Router provides flexible URL mapping
- Security checks prevent path traversal
- App-specific routes allow customization
- Extensive test coverage ensures routing reliability