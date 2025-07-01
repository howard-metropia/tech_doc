# Portuguese Plural Rules Module

**File**: `gluon/contrib/plural_rules/pt.py`  
**Language**: Portuguese (pt)  
**Type**: Pluralization Rules Implementation  
**Framework**: Web2py Gluon Framework

## Overview

This module implements pluralization rules for Portuguese language support in Web2py applications. Portuguese follows a binary pluralization system with two forms: singular and plural.

## Language Profile

### Basic Information
- **Language Family**: Indo-European → Romance → Western Romance → Ibero-Romance
- **ISO Code**: pt
- **Native Name**: português
- **Regions**: Brazil, Portugal, Angola, Mozambique, and other Lusophone countries
- **Speakers**: ~260 million native speakers
- **Writing System**: Latin script

### Pluralization Pattern
Portuguese uses a **binary pluralization system** (2 forms):
1. **Singular** (n = 1): um elemento
2. **Plural** (n ≠ 1): dois elementos

## Technical Implementation

### Configuration
```python
nplurals = 2  # Binary pluralization system
```

### Plural ID Calculation
```python
get_plural_id = lambda n: int(n != 1)
```

## Portuguese Grammar Rules

### Regular Plural Formation

**Add -s (vowels)**:
- casa → casas (house → houses)
- livro → livros (book → books)

**Add -es (consonants)**:
- animal → animais (animal → animals)
- hospital → hospitais (hospital → hospitals)

**Special patterns**:
- -ão → -ões: coração → corações (heart → hearts)
- -al → -ais: animal → animais (animal → animals)

## Regional Variations

### Brazilian Portuguese
- Same pluralization rules
- Different pronunciation
- Some vocabulary differences

### European Portuguese
- Same pluralization rules
- Different pronunciation patterns
- Some grammatical preferences

## Integration with Web2py

### Usage in Templates
```python
{{=T.plural(count, 'item', 'items')}}  # Uses Portuguese rules
```

### Message Files
```python
{
'item': 'elemento',
'items': 'elementos',
'house': 'casa',
'houses': 'casas',
}
```

## Testing Examples

### Number Validation
```python
assert get_plural_id(0) == 1  # "zero elementos"
assert get_plural_id(1) == 0  # "um elemento"
assert get_plural_id(2) == 1  # "dois elementos"
assert get_plural_id(10) == 1 # "dez elementos"
```

This module enables proper Portuguese pluralization in Web2py applications, supporting this major Romance language across multiple continents.