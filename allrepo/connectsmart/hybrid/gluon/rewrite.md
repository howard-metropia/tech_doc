# Gluon Rewrite Module Technical Documentation

## Module: `rewrite.py`

### Overview
The `rewrite` module provides comprehensive URL routing and rewriting functionality for the Gluon web framework. It supports two distinct URL routing systems: legacy regex-based routing (routes.py) and modern router-based routing (routers), with features for incoming URL parsing, outgoing URL generation, error handling, and multi-application support.

### Table of Contents
1. [Routing Systems](#routing-systems)
2. [Core Functions](#core-functions)
3. [Router Configuration](#router-configuration)
4. [URL Processing](#url-processing)
5. [Error Handling](#error-handling)
6. [Advanced Features](#advanced-features)
7. [Usage Examples](#usage-examples)

### Routing Systems

#### Legacy Regex Routing
Uses regular expressions defined in `routes.py`:
```python
routes_in = [
    ('/admin/$anything', '/admin/default/index/$anything'),
    ('/api/v1/$anything', '/api/default/api/$anything'),
]

routes_out = [
    ('/admin/default/index/$anything', '/admin/$anything'),
    ('/api/default/api/$anything', '/api/v1/$anything'),
]
```

#### Modern Router System
Uses declarative router configuration:
```python
routers = {
    'BASE': {
        'applications': ['admin', 'api', 'app'],
        'default_application': 'app',
        'domains': {
            'admin.example.com': 'admin',
            'api.example.com': 'api',
        }
    },
    'api': {
        'default_controller': 'default',
        'controllers': ['default', 'v1', 'v2'],
        'map_hyphen': True,
    }
}
```

### Core Functions

#### `url_in(request, environ)`
Main function for parsing and rewriting incoming URLs.

**Parameters:**
- `request`: Web2py request object
- `environ`: WSGI environment dictionary

**Returns:**
- `tuple`: (static_file_path, version, updated_environ) or (None, None, environ)

**Process:**
1. Determines routing system (regex vs router)
2. Parses URL components
3. Handles static file requests
4. Updates request object with parsed values

#### `url_out(request, environ, application, controller, function, args, other, scheme, host, port, language=None)`
Assembles and rewrites outgoing URLs for the HTML helper URL() function.

**Parameters:**
- `request`: Current request object
- `environ`: WSGI environment
- `application`, `controller`, `function`: URL components
- `args`: URL arguments list
- `other`: Query string and anchor
- `scheme`, `host`, `port`: URL scheme and host info
- `language`: Optional language parameter

**Returns:**
- `str`: Complete rewritten URL

### Router Configuration

#### Base Router Structure
```python
def _router_default():
    """Returns new copy of default base router"""
    router = Storage(
        default_application="init",
        applications="ALL",
        default_controller="default",
        controllers="DEFAULT",
        default_function="index",
        functions=dict(),
        default_language=None,
        languages=None,
        root_static=["favicon.ico", "robots.txt"],
        map_static=None,
        domains=None,
        exclusive_domain=False,
        map_hyphen=False,
        acfe_match=r"\w+$",  # legal app/ctlr/fcn/ext pattern
        file_match=r"([+=@$%\w-]|(?<=[+=@$%\w-])[./])*$",  # legal static files
        args_match=r"([\w@ =-]|(?<=[\w@ =-])\.)*$",  # legal args pattern
    )
    return router
```

#### Router Parameters

##### Application Level
- `applications`: List of valid applications or "ALL"
- `default_application`: Default app when none specified
- `domains`: Domain-to-application mapping
- `exclusive_domain`: Require domain-specific routing

##### Controller Level
- `controllers`: List of valid controllers or "DEFAULT"
- `default_controller`: Default controller when none specified
- `functions`: Controller-specific function mappings

##### Language Support
- `languages`: Supported language codes
- `default_language`: Default language for the application
- `map_hyphen`: Convert underscores to hyphens in URLs

##### Static Files
- `root_static`: Files served from application root
- `map_static`: Static file mapping configuration

##### Pattern Matching
- `acfe_match`: Pattern for app/controller/function/extension validation
- `file_match`: Pattern for static file path validation
- `args_match`: Pattern for URL arguments validation

### URL Processing

#### `MapUrlIn` Class
Handles incoming URL mapping with comprehensive parsing logic.

**Key Methods:**

##### `map_app()`
Determines application from URL and domain:
```python
def map_app(self):
    """Determines application name"""
    base = routers.BASE
    arg0 = self.harg0
    
    # Check domain mapping first
    if (self.host, self.port) in base.domains:
        self.application = base.domains[(self.host, self.port)][0]
    # Then check URL path
    elif base.applications and arg0 in base.applications:
        self.application = arg0
    else:
        self.application = base.default_application
```

##### `map_controller()`
Identifies controller from URL path:
```python
def map_controller(self):
    """Identifies controller"""
    arg0 = self.harg0  # with hyphen mapping
    if not arg0 or (self.controllers and arg0 not in self.controllers):
        self.controller = self.default_controller
    else:
        self.controller = arg0
```

##### `map_function()`
Handles function and extension parsing:
```python
def map_function(self):
    """Handles function.extension"""
    arg0 = self.harg0
    if not arg0 or functions and arg0.split(".")[0] not in functions:
        self.function = default_function
    else:
        func_ext = arg0.split(".")
        self.function = func_ext[0]
        if len(func_ext) > 1:
            self.extension = func_ext[-1]
```

#### `MapUrlOut` Class
Handles outgoing URL generation with optimization logic.

**Key Methods:**

##### `omit_acf()`
Optimizes URL by omitting default components:
```python
def omit_acf(self):
    """Omits what we can of a/c/f"""
    # Omit default application
    if self.application == self.default_application:
        self.omit_application = True
    
    # Omit default controller
    if self.controller == self.default_controller:
        self.omit_controller = True
    
    # Omit default function
    if self.function == self.default_function:
        self.omit_function = True
```

##### `build_acf()`
Constructs the final URL path:
```python
def build_acf(self):
    """Builds a/c/f from components"""
    acf = ""
    if not self.omit_application:
        acf += "/" + self.application
    if not self.omit_language:
        acf += "/" + self.language
    if not self.omit_controller:
        acf += "/" + self.controller
    if not self.omit_function:
        acf += "/" + self.function
    return acf or "/"
```

### Error Handling

#### Routes on Error
Handles HTTP errors with custom routing:
```python
routes_onerror = [
    ('init/400', '/init/default/error'),
    ('init/401', '/init/default/login'),
    ('init/403', '/init/default/forbidden'),
    ('init/*', '/init/default/error'),
    ('*/404', '/init/default/not_found'),
    ('*/*', '/init/default/error'),
]
```

#### Error Processing Function
```python
def try_rewrite_on_error(http_response, request, environ, ticket=None):
    """Called from main.wsgibase to rewrite the http response"""
    status = int(str(http_response.status).split()[0])
    if status >= 399 and THREAD_LOCAL.routes.routes_onerror:
        # Find matching error route
        for key, uri in THREAD_LOCAL.routes.routes_onerror:
            if key in keys:
                # Redirect to error handler
                return redirect_to_error_handler(uri, status, ticket)
    return http_response, environ
```

### Advanced Features

#### Language Support
```python
# Router with language support
routers = {
    'BASE': {
        'languages': ['en', 'es', 'fr'],
        'default_language': 'en',
    },
    'myapp': {
        'languages': ['en', 'es'],
        'default_language': 'en',
    }
}

# URLs with language:
# /en/myapp/controller/function
# /es/myapp/controller/function
```

#### Domain Routing
```python
routers = {
    'BASE': {
        'domains': {
            'admin.example.com': 'admin',
            'api.example.com': 'api/default',
            'blog.example.com': 'blog/posts/index',
        },
        'exclusive_domain': True,
    }
}

# Domain-specific routing:
# admin.example.com -> admin application
# api.example.com -> api application, default controller
# blog.example.com -> blog application, posts controller, index function
```

#### Hyphen Mapping
```python
routers = {
    'myapp': {
        'map_hyphen': True,  # Convert underscores to hyphens
    }
}

# URL mapping:
# /myapp/user-profile/edit-profile -> user_profile controller, edit_profile function
```

### Usage Examples

#### Basic Router Setup
```python
# applications/myapp/routes.py
routers = {
    'BASE': {
        'applications': ['myapp', 'admin'],
        'default_application': 'myapp',
    },
    'myapp': {
        'controllers': ['default', 'user', 'blog'],
        'default_controller': 'default',
        'default_function': 'index',
        'map_hyphen': True,
    }
}
```

#### API Routing
```python
# API-specific routing
routers = {
    'BASE': {
        'domains': {
            'api.example.com': 'api',
        }
    },
    'api': {
        'controllers': ['v1', 'v2', 'default'],
        'default_controller': 'v1',
        'functions': {
            'v1': ['users', 'posts', 'comments'],
            'v2': ['users', 'posts', 'media'],
        },
        'map_hyphen': False,  # Keep underscores for API
    }
}

# URLs:
# api.example.com/users -> api/v1/users
# api.example.com/v2/media -> api/v2/media
```

#### Legacy Regex Routes
```python
# applications/myapp/routes.py
routes_in = [
    # Blog-style URLs
    ('/blog/$year/$month/$slug', '/myapp/blog/post/$year/$month/$slug'),
    
    # API versioning
    ('/api/v1/$anything', '/myapp/api_v1/index/$anything'),
    ('/api/v2/$anything', '/myapp/api_v2/index/$anything'),
    
    # User profiles
    ('/user/$username', '/myapp/user/profile/$username'),
    
    # Admin area
    ('/admin/$anything', '/admin/default/index/$anything'),
]

routes_out = [
    # Reverse mappings
    ('/myapp/blog/post/$year/$month/$slug', '/blog/$year/$month/$slug'),
    ('/myapp/api_v1/index/$anything', '/api/v1/$anything'),
    ('/myapp/user/profile/$username', '/user/$username'),
]
```

#### Multi-Application Setup
```python
# Complex multi-app configuration
routers = {
    'BASE': {
        'applications': ['main', 'admin', 'api', 'blog'],
        'default_application': 'main',
        'domains': {
            'admin.mysite.com': 'admin',
            'api.mysite.com': 'api',
            'blog.mysite.com': 'blog',
        },
    },
    
    'main': {
        'controllers': ['default', 'user', 'contact'],
        'languages': ['en', 'es', 'fr'],
        'default_language': 'en',
        'map_hyphen': True,
    },
    
    'admin': {
        'controllers': ['default', 'users', 'content'],
        'exclusive_domain': True,
    },
    
    'api': {
        'controllers': ['v1', 'v2'],
        'default_controller': 'v1',
        'functions': {
            'v1': ['users', 'posts'],
            'v2': ['users', 'posts', 'media'],
        },
    },
    
    'blog': {
        'controllers': ['default', 'posts', 'admin'],
        'default_controller': 'posts',
        'languages': ['en', 'es'],
    }
}
```

#### Static File Handling
```python
routers = {
    'myapp': {
        'root_static': ['favicon.ico', 'robots.txt', 'sitemap.xml'],
        'map_static': True,  # Enable static file optimization
        'file_match': r'[\w\-./]+$',  # Allow specific characters in static paths
    }
}

# Static file URLs:
# /myapp/static/css/style.css -> served directly
# /favicon.ico -> myapp/static/favicon.ico
```

### Performance Optimization

#### URL Generation Optimization
```python
def optimize_url_generation():
    """Optimize URL generation for high-traffic applications"""
    
    # Cache compiled routers
    router_cache = {}
    
    def get_cached_router(app_name):
        if app_name not in router_cache:
            router_cache[app_name] = compile_router(routers[app_name])
        return router_cache[app_name]
    
    # Pre-compile common URL patterns
    common_urls = [
        ('myapp', 'default', 'index'),
        ('myapp', 'user', 'profile'),
        ('api', 'v1', 'users'),
    ]
    
    url_cache = {}
    for app, ctrl, func in common_urls:
        key = f"{app}/{ctrl}/{func}"
        url_cache[key] = generate_url(app, ctrl, func)
    
    return url_cache
```

#### Router Compilation
```python
def compile_router_patterns(router):
    """Pre-compile router patterns for better performance"""
    
    # Compile regex patterns
    router._acfe_match = re.compile(router.acfe_match)
    router._file_match = re.compile(router.file_match)
    router._args_match = re.compile(router.args_match)
    
    # Convert sets for faster lookup
    if isinstance(router.controllers, list):
        router.controllers = set(router.controllers)
    
    if isinstance(router.applications, list):
        router.applications = set(router.applications)
    
    return router
```

### Testing and Debugging

#### Route Testing
```python
def test_routes():
    """Test URL routing functionality"""
    
    test_cases = [
        # (input_url, expected_app, expected_controller, expected_function)
        ('/myapp/user/profile', 'myapp', 'user', 'profile'),
        ('/admin/', 'admin', 'default', 'index'),
        ('/api/v1/users', 'api', 'v1', 'users'),
    ]
    
    for url, exp_app, exp_ctrl, exp_func in test_cases:
        # Parse URL
        request = test_request(url)
        environ = test_environ(url)
        
        result = url_in(request, environ)
        
        assert request.application == exp_app
        assert request.controller == exp_ctrl
        assert request.function == exp_func
        
        print(f"✓ {url} -> {exp_app}/{exp_ctrl}/{exp_func}")
```

#### Debug Mode
```python
def enable_route_debugging():
    """Enable detailed routing debug information"""
    
    import logging
    logger = logging.getLogger('web2py.rewrite')
    logger.setLevel(logging.DEBUG)
    
    # Set debug logging
    params.logging = 'debug'
    
    # Log all route decisions
    def debug_url_in(request, environ):
        logger.debug(f"Processing URL: {environ['PATH_INFO']}")
        result = url_in(request, environ)
        logger.debug(f"Routed to: {request.application}/{request.controller}/{request.function}")
        return result
    
    return debug_url_in
```

### Best Practices

1. **Router Organization**: Use clear, hierarchical router structure
2. **Default Values**: Set sensible defaults for all routing parameters
3. **Validation Patterns**: Use restrictive regex patterns for security
4. **Language Support**: Plan language routing from the beginning
5. **Error Handling**: Implement comprehensive error routing
6. **Performance**: Cache compiled routers for high-traffic sites
7. **Testing**: Test all routing scenarios thoroughly
8. **Documentation**: Document custom routing rules clearly

### Security Considerations

1. **Input Validation**: Validate all URL components with strict patterns
2. **Path Traversal**: Prevent directory traversal attacks in static files
3. **Injection Attacks**: Sanitize URL parameters before processing
4. **Access Control**: Implement proper access controls in error handlers
5. **Information Disclosure**: Avoid exposing sensitive paths in error messages

### Module Metadata

- **License**: LGPLv3 (web2py framework)
- **Author**: Massimo Di Pierro
- **Thread Safety**: Yes (with thread-local storage)
- **Dependencies**: Standard library, Gluon components
- **Python**: 2.7+, 3.x compatible
- **Performance**: Optimized for high-traffic applications