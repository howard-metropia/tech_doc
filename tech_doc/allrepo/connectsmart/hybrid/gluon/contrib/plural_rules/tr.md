# Turkish Plural Rules Module

**File**: `gluon/contrib/plural_rules/tr.py`  
**Language**: Turkish (tr)  
**Type**: Pluralization Rules Implementation  
**Framework**: Web2py Gluon Framework

## Overview

This module implements pluralization rules for Turkish language support in Web2py applications. Turkish follows a binary pluralization system with agglutination.

## Language Profile

### Basic Information
- **Language Family**: Turkic → Oghuz → Western Oghuz
- **ISO Code**: tr
- **Native Name**: Türkçe
- **Regions**: Turkey, Northern Cyprus
- **Speakers**: ~80 million native speakers
- **Writing System**: Latin script (since 1928)

### Pluralization Pattern
Turkish uses a **binary pluralization system** (2 forms):
1. **Singular** (n = 1): bir öğe
2. **Plural** (n ≠ 1): iki öğe

## Technical Implementation

### Configuration
```python
nplurals = 2  # Binary pluralization system
```

### Plural ID Calculation
```python
get_plural_id = lambda n: int(n != 1)
```

## Turkish Grammar Rules

### Agglutination System
Turkish uses suffix -lar/-ler for plurals:
- ev → evler (house → houses)
- kitap → kitaplar (book → books)

### Vowel Harmony
- **Back vowels** (a, ı, o, u): use -lar
- **Front vowels** (e, i, ö, ü): use -ler

### Examples
- araba → arabalar (car → cars) - back harmony
- şehir → şehirler (city → cities) - front harmony

## Integration with Web2py

### Usage in Templates
```python
{{=T.plural(count, 'item', 'items')}}  # Uses Turkish rules
```

### Message Files
```python
{
'item': 'öğe',
'items': 'öğeler',
'house': 'ev',
'houses': 'evler',
}
```

## Character Encoding

### Turkish Characters
- **Special characters**: ç, ğ, ı, ö, ş, ü
- **UTF-8 encoding** required

## Testing Examples

### Number Validation
```python
assert get_plural_id(0) == 1  # "sıfır öğe"
assert get_plural_id(1) == 0  # "bir öğe"
assert get_plural_id(2) == 1  # "iki öğe"
assert get_plural_id(10) == 1 # "on öğe"
```

This module enables proper Turkish pluralization in Web2py applications, supporting this Turkic language's agglutinative morphology and vowel harmony system.