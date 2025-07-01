# Gluon Contrib OrderedDict Module

## Overview
Backward compatibility module that provides access to Python's standard library OrderedDict class. This module exists solely for legacy compatibility with applications that previously imported OrderedDict from gluon.contrib.ordereddict.

## Module Information
- **Module**: `gluon.contrib.ordereddict`
- **Purpose**: Backward compatibility for OrderedDict imports
- **Status**: Deprecated, scheduled for removal
- **Dependencies**: Python's standard `collections.OrderedDict`

## Key Features
- **Legacy Support**: Maintains compatibility with older web2py applications
- **Standard Library Proxy**: Directly imports from `collections.OrderedDict`
- **Zero Overhead**: Simple import redirection with no additional functionality
- **Deprecation Notice**: Marked for future removal

## Import Structure

### Current Implementation
```python
from collections import OrderedDict
```

The module consists of a single import statement that re-exports Python's built-in OrderedDict class.

## Usage

### Legacy Import Pattern
```python
# Old way (deprecated)
from gluon.contrib.ordereddict import OrderedDict

# Create ordered dictionary
od = OrderedDict()
od['first'] = 1
od['second'] = 2
od['third'] = 3

# Order is preserved
for key, value in od.items():
    print(key, value)  # Prints in insertion order
```

### Modern Import Pattern
```python
# New way (recommended)
from collections import OrderedDict

# Same functionality
od = OrderedDict()
od['first'] = 1
od['second'] = 2
od['third'] = 3
```

## Migration Guide

### Update Imports
Replace legacy imports with standard library imports:

**Before:**
```python
from gluon.contrib.ordereddict import OrderedDict
```

**After:**
```python
from collections import OrderedDict
```

### Code Changes Required
No other code changes are necessary - OrderedDict functionality remains identical.

### Search and Replace
```bash
# Find files using the legacy import
grep -r "from gluon.contrib.ordereddict import OrderedDict" .

# Replace with standard import
sed -i 's/from gluon.contrib.ordereddict import OrderedDict/from collections import OrderedDict/g' *.py
```

## OrderedDict Functionality

### Basic Operations
```python
from collections import OrderedDict

# Creation
od = OrderedDict()
od = OrderedDict([('a', 1), ('b', 2), ('c', 3)])
od = OrderedDict(a=1, b=2, c=3)

# Access
value = od['key']
value = od.get('key', default_value)

# Modification
od['new_key'] = 'new_value'
od.update({'key': 'value'})

# Deletion
del od['key']
removed_value = od.pop('key')
last_item = od.popitem()
od.clear()
```

### Order Preservation
```python
od = OrderedDict()
od['z'] = 1
od['y'] = 2
od['x'] = 3

# Iteration maintains insertion order
list(od.keys())    # ['z', 'y', 'x']
list(od.values())  # [1, 2, 3]
list(od.items())   # [('z', 1), ('y', 2), ('x', 3)]
```

### Key Operations
```python
# Move to end
od.move_to_end('key')           # Move to end
od.move_to_end('key', last=False)  # Move to beginning

# Reverse
reversed_od = OrderedDict(reversed(od.items()))
```

## Python Version Considerations

### Python 2.7+
OrderedDict available in `collections` module since Python 2.7.

### Python 3.7+
Regular dictionaries maintain insertion order, but OrderedDict still provides additional methods and explicit ordering guarantees.

### Compatibility
```python
import sys

if sys.version_info >= (2, 7):
    from collections import OrderedDict
else:
    # Fallback for very old Python versions
    try:
        from ordereddict import OrderedDict
    except ImportError:
        # OrderedDict not available
        OrderedDict = dict  # Fallback to regular dict
```

## Use Cases in Web2py

### Configuration Management
```python
from collections import OrderedDict

# Ordered configuration settings
config = OrderedDict([
    ('database_uri', 'sqlite://storage.sqlite'),
    ('debug', True),
    ('secret_key', 'your-secret-key'),
    ('mail_server', 'localhost'),
    ('mail_port', 587)
])

# Process in specific order
for key, value in config.items():
    configure_setting(key, value)
```

### Form Field Ordering
```python
from collections import OrderedDict

# Define form fields in specific order
fields = OrderedDict([
    ('first_name', Field('first_name', 'string')),
    ('last_name', Field('last_name', 'string')),
    ('email', Field('email', 'string')),
    ('phone', Field('phone', 'string'))
])

# Generate form with preserved field order
form = FORM(*[fields[name] for name in fields])
```

### Template Context
```python
from collections import OrderedDict

def controller():
    # Ensure consistent variable order in templates
    context = OrderedDict([
        ('title', 'Page Title'),
        ('user', auth.user),
        ('data', get_data()),
        ('form', create_form())
    ])
    return context
```

## Performance Considerations

### Memory Usage
OrderedDict uses more memory than regular dict due to maintaining insertion order information.

### Performance Comparison
```python
import timeit
from collections import OrderedDict

# Regular dict (Python 3.7+)
regular_dict = {'a': 1, 'b': 2, 'c': 3}

# OrderedDict
ordered_dict = OrderedDict([('a', 1), ('b', 2), ('c', 3)])

# Access performance is similar
# OrderedDict provides additional methods and guarantees
```

## Deprecation Timeline

### Current Status
- Module exists for backward compatibility
- Marked with TODO for removal
- No new features or bug fixes

### Migration Steps
1. **Audit Code**: Find all imports of `gluon.contrib.ordereddict`
2. **Update Imports**: Replace with `collections.OrderedDict`
3. **Test Applications**: Ensure no functionality changes
4. **Remove Dependencies**: Remove any references to the contrib module

### Future Removal
This module will be removed in future web2py versions. Applications should migrate to using the standard library import.

## Best Practices

### Modern Usage
```python
# Use standard library import
from collections import OrderedDict

# Consider regular dict for Python 3.7+
if sys.version_info >= (3, 7):
    # Regular dict maintains order in Python 3.7+
    data = {'first': 1, 'second': 2}
else:
    # Use OrderedDict for explicit ordering
    data = OrderedDict([('first', 1), ('second', 2)])
```

### Documentation
Update code documentation to reflect the change:
```python
# OLD documentation
"""
Uses OrderedDict from gluon.contrib.ordereddict for compatibility
"""

# NEW documentation  
"""
Uses OrderedDict from collections module for order preservation
"""
```

This module represents a simple compatibility layer that should be replaced with direct imports from Python's standard library collections module.