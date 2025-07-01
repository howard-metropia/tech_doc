# test_routes.py

## Overview
Unit tests for Web2py's regex-based URL routing system, testing pattern-based URL rewriting with routes_in and routes_out configurations.

## Imports
```python
import os
import shutil
import tempfile
import unittest
from gluon._compat import to_bytes
from gluon.html import URL
from gluon.http import HTTP
from gluon.rewrite import filter_err, filter_url, load, regex_filter_out
from gluon.settings import global_settings
from gluon.storage import Storage
```

## Module Setup/Teardown

### setUpModule()
Creates temporary application structure similar to test_router.py but with different routes.py content.

#### Application Structure
```
applications/
├── admin/
├── examples/
│   └── routes.py (contains: default_function='exdef')
└── welcome/
```

### tearDownModule()
Restores original settings and removes temporary directory.

## Test Class: TestRoutes

### Test Methods

#### test_routes_null()
Tests empty/null routes configuration.

**Default Behavior:**
- `/` → `/init/default/index`
- `/abc` → `/abc/default/index`
- `/abc/def` → `/abc/def/index`
- `/abc/def/ghi` → `/abc/def/ghi`
- `/abc/def/ghi/jkl` → `/abc/def/ghi ['jkl']`

**Key Points:**
- Assumes app/controller/function pattern
- Arguments after function become list
- URL encoding handled (`%20` → `_`)
- Static files served directly

#### test_routes_query()
Tests query string handling in route rewriting.

**Route Configuration:**
```python
routes_in = (
    ('/service/$model/create', '/app/default/call/json/create?model=$model'),
)
```

**Effects:**
- Captures URL parameters as query variables
- Preserves existing query strings
- Combines route and request query parameters

#### test_routes_specific()
Tests app-specific routes.py files.

**Route Configuration:**
```python
routes_app = [
    (r'/(?P<app>welcome|admin|examples)\b.*', r'\g<app>'),
    (r'$anything', r'welcome'),
    (r'/?$anything', r'welcome'),
]
```

**Results:**
- Examples app uses custom default function
- App-specific settings override global routes

#### test_routes_defapp()
Tests default application configuration.

**Configuration:**
```python
default_application = 'defapp'
```

**Effects:**
- Root URL maps to defapp
- Other apps still accessible by name
- Static files resolve correctly

#### test_routes_raise()
Tests URL validation and error conditions.

**Valid Patterns:**
- `/init/default/fcn.ext`
- `/init/default/fcn/arg`
- `/init/default/fcn_1`

**Invalid Patterns:**
- `/bad!ctl` - Invalid controller name
- `/ctl/bad!fcn` - Invalid function name
- `/ctl/fcn.bad!ext` - Invalid extension

#### test_routes_error()
Tests HTTP error code rewriting.

**Functionality:**
- Passes through standard HTTP codes
- Allows custom error routing

#### test_routes_args()
Complex test of URL argument handling.

**Route Tables:**
```python
routes_in = [
    # Domain-based routing
    ('.*:https?://(.*\.)?domain1.com:$method /$anything', '/app1/default/$anything'),
    # Default routes
    ('/$anything', '/welcome/default/$anything'),
]
routes_out = [
    # Simplify URLs
    ('/welcome/default/$anything', '/$anything'),
]
```

**Features Tested:**
- Empty arguments preservation
- Multiple consecutive slashes
- URL encoding/decoding
- Unicode handling
- Domain-based routing

#### test_routes_anchor()
Tests URL anchors (fragments) handling.

**Basic Anchors:**
- `URL(..., anchor="anchor")` → `#anchor`
- Works with args and vars

**Advanced Patterns:**
```python
routes_out = [
    (r'/init/default/index(?P<anchor>(#.*)?)', r'/\g<anchor>'),
]
```

**Results:**
- Anchors preserved in routing
- Special handling for index pages
- Query and anchor combination

#### test_routes_absolute()
Tests absolute URL generation.

**Request Setup:**
```python
r.env.http_host = "domain.com"
r.env.wsgi_url_scheme = "httpx"
```

**URL Options:**
- `host=True` - Include domain
- `scheme=True` - Include protocol
- `scheme="https"` - Force protocol
- `port=1234` - Include port

**Examples:**
- Basic: `/a/c/f`
- With host: `httpx://domain.com/a/c/f`
- Custom scheme: `https://domain.com/a/c/f`
- With port: `httpx://domain.com:1234/a/c/f`

#### test_request_uri()
Tests REQUEST_URI environment variable handling.

**Route Configuration:**
```python
routes_in = [
    ('/abc', '/init/default/abc'),
    ('/index/$anything', '/init/default/index/$anything'),
]
```

**Features:**
- Preserves query strings
- Handles URL encoding
- Sets proper REQUEST_URI

## Regex Routing Features

### Pattern Variables
- `$anything` - Matches any path
- `$model` - Named capture
- `(?P<name>...)` - Named groups
- `\g<name>` - Group references

### Route Tables
- **routes_in**: Incoming URL → Internal path
- **routes_out**: Internal path → External URL
- **routes_app**: App selection patterns

### Domain-based Routing
```python
'.*:https?://(.*\.)?domain.com:$method /$anything'
```
Routes based on:
- Protocol
- Domain/subdomain
- HTTP method
- Path

### Special Handling
- Static files bypass routing
- Admin interface protection
- Default app/controller/function
- Query string preservation

## Testing Patterns

### URL Components
- Application name
- Controller name
- Function name
- Arguments (list)
- Variables (dict)
- Anchor (fragment)

### Edge Cases
- Empty arguments (`//`)
- Unicode characters
- URL encoding
- Invalid characters
- Long paths

### Error Handling
- HTTP exceptions for invalid paths
- Validation of components
- Security checks

## Comparison with Router Tests

### Regex Routes (this file)
- Pattern-based matching
- More flexible
- Regular expressions
- Explicit configuration

### Router (test_router.py)
- Dictionary configuration
- Simpler syntax
- Less flexible
- Convention over configuration

## Notes
- Regex routing provides maximum flexibility
- Domain-based routing for multi-tenant apps
- Careful pattern ordering required
- Security validation prevents attacks
- Both routing systems can coexist