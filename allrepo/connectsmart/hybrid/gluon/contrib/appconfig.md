# appconfig.py

🔍 **Quick Summary (TL;DR)**
- High-performance configuration management system for Web2py applications supporting INI and JSON formats with intelligent caching and dot notation access
- Core functionality: configuration management | file parsing | caching | INI JSON support | dot notation | environment variables
- Primary use cases: Application configuration, environment-specific settings, cached config access, nested parameter retrieval
- Quick compatibility: Python 2.7+/3.x, Web2py framework, supports .ini and .json configuration files

❓ **Common Questions Quick Index**
- Q: What config formats are supported? A: [Technical Specifications](#technical-specifications) - INI and JSON formats
- Q: How to access nested configurations? A: [Usage Methods](#usage-methods) - Use dot notation like config.take('db.uri')
- Q: How does caching work? A: [Detailed Code Analysis](#detailed-code-analysis) - Thread-safe singleton with internal cache
- Q: How to reload configurations? A: [Usage Methods](#usage-methods) - Pass reload=True parameter
- Q: What about environment variables? A: [Detailed Code Analysis](#detailed-code-analysis) - INI parser supports os.environ substitution
- Q: How to cast configuration values? A: [Output Examples](#output-examples) - Use cast parameter in take() method
- Q: Where should config files be placed? A: [Technical Specifications](#technical-specifications) - app/private/appconfig.ini or .json
- Q: How to troubleshoot config errors? A: [Important Notes](#important-notes) - Check file path and format syntax

📋 **Functionality Overview**
- **Non-technical explanation:** Like a smart filing cabinet that remembers where you put documents and can quickly find them again - it reads configuration files once, remembers the contents, and lets you ask for specific settings using simple dot notation like "database.connection.host" instead of digging through nested folders.
- **Technical explanation:** Thread-safe configuration management system that provides cached access to application settings stored in INI or JSON files, with support for nested value retrieval via dot notation and automatic type conversion.
- Business value: Enables environment-specific configuration management, improves application performance through caching, simplifies configuration access patterns
- Context: Core Web2py contrib utility used throughout applications for database connections, API keys, feature flags, and environment-specific settings

🔧 **Technical Specifications**
- File: appconfig.py, /gluon/contrib/, Python, Configuration utility, ~4KB, Medium complexity
- Dependencies: json (Python standard), configparser (Python standard), gluon._compat, gluon.globals, thread module
- Compatibility: Python 2.7+/3.x, Web2py framework, cross-platform file system support
- Configuration: Default paths: app/private/appconfig.ini or app/private/appconfig.json
- System requirements: File system access to private folder, thread support for locking
- Security: File-based configuration storage, supports environment variable substitution

📝 **Detailed Code Analysis**
```python
class AppConfig:
    """Thread-safe singleton configuration loader with caching"""
    
    def __call__(*args, **vars):
        locker.acquire()  # Thread safety
        reload_ = vars.pop('reload', False)
        instance_name = 'AppConfig_' + current.request.application
        
        if reload_ or not hasattr(AppConfig, instance_name):
            setattr(AppConfig, instance_name, AppConfigLoader(*args, **vars))
        return getattr(AppConfig, instance_name).settings
```

**Dot Notation Access:**
```python
class AppConfigDict(dict):
    def take(self, path, cast=None):
        # Split path like "db.uri" into ["db", "uri"]
        parts = path.split('.')
        if path in self.int_cache:
            return self.int_cache[path]  # Return cached value
        
        # Walk through nested dictionary
        value = self
        for part in parts:
            if part not in value:
                raise BaseException("%s not in config" % part)
            value = value[part]
        
        # Apply type casting if specified
        if cast:
            value = cast(value)
        self.int_cache[path] = value  # Cache result
        return value
```

**Smart Type Conversion:**
```python
def get(self, path, default=None):
    value = self.take(path).strip()
    if value.lower() in ('none','null',''):
        return None
    elif value.lower() == 'true':
        return True
    elif value.lower() == 'false':
        return False
    elif value.isdigit():
        return int(value)
    elif ',' in value:
        return map(lambda x:x.strip(), value.split(','))  # List
    else:
        try:
            return float(value)
        except:
            return value
```

**Design Patterns:** Singleton pattern, Factory pattern, Caching pattern, Thread-safe access
**Performance:** O(1) cached access after first retrieval, O(n) for initial nested traversal
**Resource Management:** Thread locking for concurrent access, file handle management

🚀 **Usage Methods**
```python
# Basic usage - automatic file detection
from gluon.contrib.appconfig import AppConfig
myconfig = AppConfig()

# Access configuration values
db_uri = myconfig['db']['uri']
api_key = myconfig['external']['api_key']

# Dot notation access
db_uri = myconfig.take('db.uri')
timeout = myconfig.take('api.timeout', cast=int)

# With type casting
expiration = myconfig.take('auth.expiration', cast=int)
debug_mode = myconfig.take('app.debug', cast=bool)

# Force reload (development only)
myconfig = AppConfig(reload=True)

# Custom configuration file
myconfig = AppConfig('/path/to/custom/config.json')
```

**INI Configuration Format:**
```ini
# app/private/appconfig.ini
[db]
uri = mysql://user:pass@localhost/mydb
pool_size = 10

[api]
timeout = 30
base_url = https://api.example.com

[auth]
expiration = 3600
secret_key = ${SECRET_KEY}  # Environment variable
```

**JSON Configuration Format:**
```json
{
  "db": {
    "uri": "mysql://user:pass@localhost/mydb",
    "pool_size": 10
  },
  "api": {
    "timeout": 30,
    "base_url": "https://api.example.com"
  },
  "auth": {
    "expiration": 3600,
    "secret_key": "your-secret-key"
  }
}
```

📊 **Output Examples**
**Successful Configuration Access:**
```python
>>> from gluon.contrib.appconfig import AppConfig
>>> config = AppConfig()
>>> print(config.take('db.uri'))
'mysql://user:pass@localhost/mydb'

>>> print(config.take('api.timeout', cast=int))
30

>>> print(config.get('auth.debug'))  # Smart type detection
True
```

**Configuration Structure Display:**
```python
>>> config = AppConfig()
>>> print(config)
{
  'db': {
    'uri': 'mysql://user:pass@localhost/mydb',
    'pool_size': '10'
  },
  'api': {
    'timeout': '30',
    'base_url': 'https://api.example.com'
  }
}
```

**Error Scenarios:**
```python
>>> config.take('nonexistent.key')
BaseException: nonexistent not in config [nonexistent]

>>> config.take('api.timeout', cast=complex)
BaseException: 30 can't be converted to <class 'complex'>
```

**Performance Comparison:**
```python
# First access: ~0.1ms (file read + parse)
start = time.time()
value = config.take('db.uri')
print(f"First access: {(time.time() - start) * 1000:.2f}ms")

# Cached access: ~0.001ms
start = time.time()
value = config.take('db.uri')
print(f"Cached access: {(time.time() - start) * 1000:.2f}ms")
```

⚠️ **Important Notes**
- **Thread Safety:** Uses thread locking for concurrent access, but may cause bottlenecks under high load
- **Caching Behavior:** Values are cached permanently until process restart or reload=True
- **File Detection:** Automatically searches for appconfig.ini then appconfig.json in private folder
- **Environment Variables:** INI format supports ${VAR} substitution, JSON does not
- **Development vs Production:** Use reload=False in production for performance
- **Error Propagation:** Configuration errors raise BaseException, may crash application startup

**Common Troubleshooting:**
- Config file not found → Check file exists in app/private/ directory
- Parse errors → Validate INI/JSON syntax and format
- Key not found → Verify configuration key path and nesting
- Type casting errors → Check value format and target type compatibility
- Thread deadlocks → Avoid nested AppConfig calls within locked contexts

🔗 **Related File Links**
- `app/private/appconfig.ini` - Default INI configuration file location
- `app/private/appconfig.json` - Default JSON configuration file location  
- Web2py application models for database configuration usage
- Environment-specific configuration examples
- Configuration validation and schema documentation
- Web2py deployment guides for configuration management

📈 **Use Cases**
- **Database Configuration:** Store connection strings, pool settings, and database credentials
- **API Integration:** Manage external service URLs, API keys, and timeout settings
- **Feature Flags:** Control application features through configuration
- **Environment Management:** Different settings for development, staging, production
- **Security Settings:** Authentication parameters, session timeouts, encryption keys
- **Performance Tuning:** Cache settings, connection pools, resource limits

🛠️ **Improvement Suggestions**
- **Schema Validation:** Add JSON schema validation for configuration structure
- **Hot Reloading:** Implement file watching for automatic configuration updates
- **Encryption Support:** Add encrypted configuration value support for sensitive data
- **Environment Profiles:** Built-in support for environment-specific configuration sections
- **Configuration Merging:** Support for multiple configuration files with inheritance
- **Validation Rules:** Add type checking and value validation at load time
- **Performance Optimization:** Implement more granular caching and lazy loading

🏷️ **Document Tags**
- Keywords: configuration management, INI JSON parsing, dot notation access, caching, thread safety, environment variables, Web2py configuration, settings management, file parsing
- Technical tags: #configuration #web2py-contrib #caching #file-parsing #thread-safety #dot-notation
- Target roles: Backend developers (intermediate), DevOps engineers (intermediate), System administrators (basic)
- Difficulty level: ⭐⭐ - Requires understanding of configuration patterns and caching concepts  
- Maintenance level: Low - Stable configuration patterns, minimal updates needed
- Business criticality: High - Core infrastructure component for application configuration
- Related topics: Web2py configuration, file parsing, caching patterns, environment management, application settings