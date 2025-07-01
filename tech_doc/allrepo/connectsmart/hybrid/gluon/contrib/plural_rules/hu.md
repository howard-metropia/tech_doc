# Hungarian Plural Rules Module

**File**: `gluon/contrib/plural_rules/hu.py`  
**Language**: Hungarian (hu)  
**Type**: Pluralization Rules Implementation  
**Framework**: Web2py Gluon Framework

## Overview

This module implements pluralization rules for Hungarian language support in Web2py applications. Hungarian follows a binary pluralization system with two forms: singular and plural.

## Language Profile

### Basic Information
- **Language Family**: Uralic → Finno-Ugric → Ugric
- **ISO Code**: hu
- **Native Name**: magyar nyelv
- **Regions**: Hungary, parts of Romania, Slovakia, Serbia, Ukraine
- **Speakers**: ~13 million native speakers
- **Writing System**: Latin script with Hungarian orthography

### Pluralization Pattern
Hungarian uses a **binary pluralization system** (2 forms):
1. **Singular** (n = 1): egy elem
2. **Plural** (n ≠ 1): két elem

## Technical Implementation

### Configuration
```python
nplurals = 2  # Binary pluralization system
```

### Plural ID Calculation
```python
get_plural_id = lambda n: int(n != 1)
```

## Hungarian Grammar Rules

### Agglutination System
Hungarian uses suffixes for pluralization:
- ház → házak (house → houses)
- könyv → könyvek (book → books)
- ember → emberek (person → people)

### Vowel Harmony
Hungarian follows strict vowel harmony rules:
- **Back vowels**: a, á, o, ó, u, ú → -ak, -ok suffix
- **Front vowels**: e, é, i, í, ö, ő, ü, ű → -ek, -ök suffix

### Examples
- asztal → asztalok (table → tables) - back harmony
- szék → székek (chair → chairs) - front harmony
- autó → autók (car → cars) - back harmony

## Integration with Web2py

### Usage in Templates
```python
{{=T.plural(count, 'item', 'items')}}  # Uses Hungarian rules
```

### Message Files
Language files in `applications/*/languages/hu.py`:
```python
{
'item': 'elem',
'items': 'elemek',
'house': 'ház',
'houses': 'házak',
# Hungarian translations
}
```

## Testing Examples

### Number Validation
```python
assert get_plural_id(0) == 1  # "nulla elem"
assert get_plural_id(1) == 0  # "egy elem"
assert get_plural_id(2) == 1  # "két elem"
assert get_plural_id(10) == 1 # "tíz elem"
```

This module enables proper Hungarian pluralization in Web2py applications, supporting the agglutinative morphology and vowel harmony of this unique Uralic language.