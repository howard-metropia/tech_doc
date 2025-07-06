# _load.py

## Overview
Module loader for PyDAL that provides fallback mechanisms for modules that may not be available in all Python environments, ensuring compatibility across different installations.

## Import Strategy
Uses a fallback pattern for optional dependencies:
```python
try:
    # Try standard library or installed package
except:
    # Fall back to bundled contrib version
```

## OrderedDict Import

### Standard Library Attempt
```python
try:
    from collections import OrderedDict
except:
    from .contrib.ordereddict import OrderedDict
```

**Fallback Logic:**
- **Primary**: Use `collections.OrderedDict` (Python 2.7+ standard library)
- **Fallback**: Use bundled implementation in `contrib.ordereddict`

**Why OrderedDict is Critical:**
- Essential for maintaining field order in database schemas
- Required for consistent query result ordering
- Ensures predictable behavior across Python versions

**Compatibility Coverage:**
- **Python 2.6**: No built-in OrderedDict, uses contrib version
- **Python 2.7+**: Has built-in OrderedDict in collections
- **Python 3.x**: Native OrderedDict support

## Portalocker Import

### Current Implementation
```python
from .contrib import portalocker
```
Always uses the bundled contrib version for file locking.

### Future Implementation (Commented)
```python
# TODO: uncomment the lines below when contrib/portalocker will be
# inline with the one shipped with pip
# try:
#    import portalocker
# except ImportError:
#    from .contrib import portalocker
```

**Planned Fallback Strategy:**
- **Primary**: Use system-installed `portalocker` package
- **Fallback**: Use bundled `contrib.portalocker`

**Why Contrib Version is Used:**
- Ensures specific version compatibility
- Maintains control over file locking behavior
- Avoids dependency version conflicts

## File Locking Use Cases

### Database File Protection
- SQLite database file locking
- Prevents concurrent access corruption
- Ensures data integrity during operations

### Migration Safety
- Locks migration files during schema changes
- Prevents race conditions in deployment
- Ensures atomic migration operations

### Cache File Management
- Protects cache files from corruption
- Enables safe concurrent cache access
- Maintains cache consistency

## Compatibility Benefits

### Cross-Platform Support
- Works on Windows, Linux, macOS
- Handles different file locking mechanisms
- Provides consistent API across platforms

### Python Version Support
- Maintains compatibility from Python 2.6+
- Handles missing standard library modules
- Ensures consistent behavior across versions

### Deployment Flexibility
- Works in restricted environments
- No external dependencies required
- Reduces installation complexity

## Module Dependencies

### OrderedDict Usage in PyDAL
- **Table Definitions**: Maintains field order
- **Query Results**: Consistent column ordering
- **Schema Operations**: Predictable field processing
- **Metadata Storage**: Ordered configuration handling

### Portalocker Usage in PyDAL
- **Database Locking**: File-based database protection
- **Migration Locks**: Schema change synchronization
- **Cache Locking**: Thread-safe cache operations
- **Log File Protection**: Prevents log corruption

## Import Patterns

### Safe Import Strategy
The module demonstrates PyDAL's approach to optional dependencies:
1. Try standard library or well-known packages
2. Fall back to tested contrib versions
3. Maintain API compatibility regardless of source

### Contrib Package Philosophy
- Bundle critical dependencies that may be missing
- Maintain specific versions for stability
- Reduce external dependency requirements
- Ensure consistent behavior across environments

## Future Considerations

### Portalocker Migration
The TODO comment indicates plans to:
- Prefer system-installed portalocker when available
- Maintain fallback to contrib version
- Requires version compatibility verification
- May reduce bundle size when external package is available

### Dependency Management
- Balance between external dependencies and bundle size
- Maintain compatibility across deployment scenarios
- Consider security updates for bundled packages
- Plan migration paths for contrib modules

## Notes
- Critical for PyDAL's "batteries included" approach
- Ensures functionality without complex dependency management
- Provides fallback for older Python environments
- Demonstrates defensive programming for cross-platform compatibility
- Essential for maintaining PyDAL's deployment simplicity