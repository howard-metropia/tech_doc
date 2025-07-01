# Indonesian Plural Rules Module

**File**: `gluon/contrib/plural_rules/id.py`  
**Language**: Indonesian (id)  
**Type**: Pluralization Rules Implementation  
**Framework**: Web2py Gluon Framework

## Overview

This module implements pluralization rules for Indonesian language support in Web2py applications. Indonesian follows a binary pluralization system with two forms: singular and plural.

## Language Profile

### Basic Information
- **Language Family**: Austronesian → Malayo-Polynesian → Malayic
- **ISO Code**: id
- **Native Name**: Bahasa Indonesia
- **Regions**: Indonesia (official language)
- **Speakers**: ~200+ million total speakers
- **Writing System**: Latin script

### Pluralization Pattern
Indonesian uses a **binary pluralization system** (2 forms):
1. **Singular** (n = 1): satu item
2. **Plural** (n ≠ 1): dua item

## Technical Implementation

### Configuration
```python
nplurals = 2  # Binary pluralization system
```

### Plural ID Calculation
```python
get_plural_id = lambda n: int(n != 1)
```

## Indonesian Grammar Rules

### Reduplication for Plurals
Indonesian typically uses reduplication for plurals:
- buku → buku-buku (book → books)
- anak → anak-anak (child → children)
- rumah → rumah-rumah (house → houses)

### Context-Dependent Plurals
Often singular form used with numbers:
- dua buku (two book/books)
- lima anak (five child/children)

## Integration with Web2py

### Usage in Templates
```python
{{=T.plural(count, 'item', 'items')}}  # Uses Indonesian rules
```

### Message Files
```python
{
'item': 'item',
'items': 'item-item',
'book': 'buku',
'books': 'buku-buku',
}
```

## Testing Examples

### Number Validation
```python
assert get_plural_id(0) == 1  # "nol item"
assert get_plural_id(1) == 0  # "satu item"
assert get_plural_id(2) == 1  # "dua item"
assert get_plural_id(10) == 1 # "sepuluh item"
```

This module enables proper Indonesian pluralization in Web2py applications.