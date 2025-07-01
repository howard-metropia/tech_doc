# PyDAL Helper Classes

## Overview
Utility classes that provide reusable functionality for PyDAL operations, including data containers, iterators, and specialized data structures.

## Key Classes

### Data Container Classes
```python
class OrderedDict:
    """Ordered dictionary implementation for maintaining insertion order"""

class Rows:
    """Container for query result sets with iteration and manipulation"""

class Row:
    """Individual row representation with attribute access"""
```

### Utility Classes
```python
class LazySet:
    """Lazy evaluation set for efficient query operations"""

class Reference:
    """Foreign key reference handling"""

class SQLCustomType:
    """Custom data type definition support"""
```

### Iterator Classes
- **ResultIterator**: Efficient result set iteration
- **BatchIterator**: Batch processing support
- **LazyIterator**: Memory-efficient lazy loading

### Specialized Containers
- **FieldSet**: Collection of database fields
- **QuerySet**: Query operation container
- **ValidationSet**: Validation rule collection

These classes provide the building blocks for PyDAL's object-relational mapping and data manipulation capabilities.