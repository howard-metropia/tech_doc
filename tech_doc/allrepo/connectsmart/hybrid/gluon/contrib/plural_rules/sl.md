# Slovenian Plural Rules Module

**File**: `gluon/contrib/plural_rules/sl.py`  
**Language**: Slovenian (sl)  
**Type**: Pluralization Rules Implementation  
**Framework**: Web2py Gluon Framework

## Overview

This module implements pluralization rules for Slovenian language support in Web2py applications. Slovenian follows a binary pluralization system.

## Language Profile

### Basic Information
- **Language Family**: Indo-European → Slavic → South Slavic
- **ISO Code**: sl
- **Native Name**: slovenščina
- **Regions**: Slovenia
- **Speakers**: ~2.5 million native speakers
- **Writing System**: Latin script

### Pluralization Pattern
Slovenian uses a **binary pluralization system** (2 forms):
1. **Singular** (n = 1): en element
2. **Plural** (n ≠ 1): dva elementa

## Technical Implementation

### Configuration
```python
nplurals = 2  # Binary pluralization system
```

### Plural ID Calculation
```python
get_plural_id = lambda n: int(n != 1)
```

## Integration with Web2py

### Message Files
```python
{
'item': 'element',
'items': 'elementi',
}
```

## Character Encoding

### Slovenian Characters
- **Special characters**: č, š, ž
- **UTF-8 encoding** required

## Testing Examples

```python
assert get_plural_id(1) == 0   # "en element"
assert get_plural_id(2) == 1   # "dva elementa"
```

This module enables Slovenian pluralization in Web2py applications.