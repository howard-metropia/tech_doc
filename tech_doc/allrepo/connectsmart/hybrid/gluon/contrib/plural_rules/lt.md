# Lithuanian Plural Rules Module

**File**: `gluon/contrib/plural_rules/lt.py`  
**Language**: Lithuanian (lt)  
**Type**: Pluralization Rules Implementation  
**Framework**: Web2py Gluon Framework

## Overview

This module implements pluralization rules for Lithuanian language support in Web2py applications. Lithuanian follows a binary pluralization system with two forms: singular and plural.

## Language Profile

### Basic Information
- **Language Family**: Indo-European → Baltic
- **ISO Code**: lt
- **Native Name**: lietuvių kalba
- **Regions**: Lithuania
- **Speakers**: ~3 million native speakers
- **Writing System**: Latin script with Lithuanian orthography

### Pluralization Pattern
Lithuanian uses a **binary pluralization system** (2 forms):
1. **Singular** (n = 1): vienas elementas
2. **Plural** (n ≠ 1): du elementai

## Technical Implementation

### Configuration
```python
nplurals = 2  # Binary pluralization system
```

### Plural ID Calculation
```python
get_plural_id = lambda n: int(n != 1)
```

## Lithuanian Grammar Rules

### Complex Declension System
Lithuanian has a rich case system with multiple declension patterns:
- **Nominative**: kas/koks (who/what)
- **Genitive**: ko/kokio (whose/of what)
- **Dative**: kam/kokiam (to whom/what)
- **Accusative**: ką/kokį (whom/what)
- **Instrumental**: kuo/kokiu (with what)
- **Locative**: kame/kokiame (where)
- **Vocative**: addressing directly

### Plural Formation Examples
- namas → namai (house → houses)
- knyga → knygos (book → books)
- vaikas → vaikai (child → children)

## Integration with Web2py

### Usage in Templates
```python
{{=T.plural(count, 'item', 'items')}}  # Uses Lithuanian rules
```

### Message Files
```python
{
'item': 'elementas',
'items': 'elementai',
'house': 'namas',
'houses': 'namai',
}
```

## Character Encoding

### Lithuanian Diacritics
- **Special letters**: ą, č, ę, ė, į, š, ų, ū, ž
- **UTF-8 encoding** required

## Testing Examples

### Number Validation
```python
assert get_plural_id(0) == 1  # "nulis elementų"
assert get_plural_id(1) == 0  # "vienas elementas"
assert get_plural_id(2) == 1  # "du elementai"
assert get_plural_id(10) == 1 # "dešimt elementų"
```

This module enables proper Lithuanian pluralization in Web2py applications, supporting this Baltic language's rich grammatical heritage.