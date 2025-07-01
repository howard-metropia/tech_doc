# Myanmar (Burmese) Plural Rules Module

**File**: `gluon/contrib/plural_rules/my.py`  
**Language**: Myanmar/Burmese (my)  
**Type**: Pluralization Rules Implementation  
**Framework**: Web2py Gluon Framework

## Overview

This module implements pluralization rules for Myanmar (Burmese) language support in Web2py applications. Myanmar follows a binary pluralization system.

## Language Profile

### Basic Information
- **Language Family**: Sino-Tibetan → Tibeto-Burman
- **ISO Code**: my
- **Native Name**: မြန်မာဘာသာ (mranma bhasa)
- **Regions**: Myanmar (Burma)
- **Speakers**: ~33 million native speakers
- **Writing System**: Myanmar script

### Pluralization Pattern
Myanmar uses a **binary pluralization system** (2 forms):
1. **Singular** (n = 1): တစ်ခု (ta hku)
2. **Plural** (n ≠ 1): နှစ်ခု (hna hku)

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
'item': 'အရာ',
'items': 'အရာများ',
}
```

## Character Encoding

### Myanmar Script
- **UTF-8 encoding** required for Myanmar characters
- Complex script rendering needed

## Testing Examples

```python
assert get_plural_id(0) == 1
assert get_plural_id(1) == 0
assert get_plural_id(2) == 1
```

This module enables Myanmar language support in Web2py applications.