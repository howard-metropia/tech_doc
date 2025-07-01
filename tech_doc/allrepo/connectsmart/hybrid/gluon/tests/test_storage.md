# test_storage.py

## Overview
Unit tests for Web2py's storage classes that provide enhanced dictionary and list functionality with attribute access and special behaviors for web applications.

## Imports
```python
import unittest
from gluon._compat import pickle
from gluon.http import HTTP
from gluon.storage import List, Storage, StorageList
```

## Test Classes

### TestStorage
Tests the Storage class, which is an enhanced dictionary supporting attribute access.

#### test_attribute()
Tests basic attribute and dictionary access:
- **Initialization**: `Storage(a=1)` creates storage with initial values
- **Attribute Access**: `s.a` returns value like `s["a"]`
- **Missing Attributes**: `s.b` returns `None` for undefined attributes
- **Setting Values**: Both `s.b = 2` and `s["c"] = 3` work
- **Reference Identity**: `s.d is s["d"]` confirms same object reference

#### test_store_none()
Tests None value handling with special behavior:
- **Attribute Assignment**: `s.a = None` may delete the item (behavior unclear from test)
- **Dictionary Assignment**: `s["a"] = None` sets value to None and keeps key
- **Membership**: Key remains in storage when set via dictionary notation

#### test_item()
Tests item access and None handling:
- **Missing Items**: Both `s.d` and `s["d"]` return `None` for undefined keys
- **None Assignment**: Setting `s["a"] = None` preserves key with None value
- **Membership Check**: `"a" in s` returns True even when value is None

#### test_pickling()
Tests serialization support:
- **Pickle Support**: Storage objects can be pickled and unpickled
- **Data Preservation**: Values maintained through pickle cycle
- **Protocol**: Uses highest pickle protocol for efficiency

#### test_getlist()
Tests list conversion for HTTP form handling:
- **Single Values**: `s.x = "abc"` becomes `["abc"]` via `getlist()`
- **Multiple Values**: `s.y = ["abc", "def"]` remains as list
- **Missing Keys**: `getlist("z")` returns empty list `[]`

#### test_getfirst()
Tests first value extraction for HTTP forms:
- **Single Values**: Returns the value directly
- **Multiple Values**: Returns first item from list
- **Missing Keys**: Returns `None`

#### test_getlast()
Tests last value extraction:
- **Single Values**: Returns the value directly
- **Multiple Values**: Returns last item from list  
- **Missing Keys**: Returns `None`

### TestStorageList
Tests StorageList class combining Storage and list behaviors.

#### test_attribute()
Tests hybrid storage/list functionality:
- **Attribute Access**: Like Storage, supports `s.a` access
- **List Default**: Missing attributes return empty list `[]`
- **List Mutation**: Can append to automatically created lists
- **Example**: `s.b.append(1)` creates list and adds item

### TestList
Tests the List class, an enhanced list for Web2py request arguments.

#### test_listcall()
Tests callable list interface for safe argument access:

**Basic Access:**
- `a(1)` returns item at index 1 (like `a[1]`)
- `a(-1)` supports negative indexing
- `a(-5)` returns `None` for out-of-bounds (safe access)

**Default Values:**
- `a(-5, default="x")` returns default for missing indices
- Default takes precedence over other parameters

**Type Casting:**
- `a(-3, cast=str)` converts value to specified type
- `a(3, cast=int)` converts "1234" to integer 1234
- **Error Handling**: Invalid cast raises HTTP exception

**Advanced Parameters:**
- **default**: Fallback value for missing/invalid indices
- **cast**: Type conversion function
- **otherwise**: Callback function when no value and no default
- **Parameter Priority**: default > otherwise for fallback logic

**Edge Cases:**
```python
b = List()  # Empty list
b(0, cast=int, default=None)  # Returns None (default)
b(0, otherwise=lambda: "something")  # Calls function
b(0, default=0, otherwise=lambda: "x")  # Returns 0 (default wins)
```

#### test_listgetitem()
Tests standard list operations:
- **Index Access**: `a[0]` works like normal list
- **Slicing**: `a[::-1]` supports all slice operations
- **Compatibility**: Maintains standard list behavior

## Storage Classes Overview

### Storage
Enhanced dictionary with:
- Attribute access (`obj.key`)
- None-safe access (missing keys return None)
- HTTP form utilities (getlist, getfirst, getlast)
- Pickle support

### StorageList  
Hybrid Storage/list:
- Attribute access with list defaults
- Combines dictionary and list behaviors

### List
Enhanced list for request arguments:
- Callable interface for safe access
- Type casting and validation
- Default value handling
- HTTP error integration

## Web2py Integration

### Request Variables
These classes are used throughout Web2py for:
- `request.vars` - Form data as Storage
- `request.args` - URL arguments as List
- `request.get_vars` - GET parameters
- `request.post_vars` - POST parameters

### HTTP Form Handling
Special methods support multiple form values:
- HTML checkboxes can submit multiple values
- `getlist()` ensures consistent list format
- `getfirst()`/`getlast()` extract single values

### Safe Access Patterns
- Missing attributes/indices return None instead of raising errors
- Type casting with error handling
- Default values for robust form processing

## Notes
- Storage provides dict-like and object-like access patterns
- List provides safe indexed access for URL arguments
- All classes designed for web application data handling
- Pickle support enables session storage
- HTTP exception integration for type conversion errors