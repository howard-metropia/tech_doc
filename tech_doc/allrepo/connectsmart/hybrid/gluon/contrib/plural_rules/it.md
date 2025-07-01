# Italian Plural Rules Module

**File**: `gluon/contrib/plural_rules/it.py`  
**Language**: Italian (it)  
**Type**: Pluralization Rules Implementation  
**Framework**: Web2py Gluon Framework

## Overview

This module implements pluralization rules for Italian language support in Web2py applications. Italian follows a binary pluralization system with complex morphological patterns.

## Language Profile

### Basic Information
- **Language Family**: Indo-European → Romance → Western Romance → Italo-Western → Gallo-Italic
- **ISO Code**: it
- **Native Name**: italiano
- **Regions**: Italy, San Marino, Vatican City, parts of Switzerland
- **Speakers**: ~65 million native speakers
- **Writing System**: Latin script

### Pluralization Pattern
Italian uses a **binary pluralization system** (2 forms):
1. **Singular** (n = 1): un elemento
2. **Plural** (n ≠ 1): due elementi

## Technical Implementation

### Configuration
```python
nplurals = 2  # Binary pluralization system
```

### Plural ID Calculation
```python
get_plural_id = lambda n: int(n != 1)
```

## Italian Grammar Rules

### Regular Plural Formation

**Masculine nouns** (-o → -i):
- libro → libri (book → books)
- ragazzo → ragazzi (boy → boys)

**Feminine nouns** (-a → -e):
- casa → case (house → houses)
- ragazza → ragazze (girl → girls)

**Nouns ending in -e** → **-i**:
- cane → cani (dog → dogs)
- fiore → fiori (flower → flowers)

### Gender and Articles
- **Masculine singular**: il libro, lo studente
- **Masculine plural**: i libri, gli studenti
- **Feminine singular**: la casa, l'amica
- **Feminine plural**: le case, le amiche

## Integration with Web2py

### Usage in Templates
```python
{{=T.plural(count, 'item', 'items')}}  # Uses Italian rules
```

### Message Files
```python
{
'item': 'elemento',
'items': 'elementi',
'book': 'libro',
'books': 'libri',
'house': 'casa',
'houses': 'case',
}
```

## Testing Examples

### Number Validation
```python
assert get_plural_id(0) == 1  # "zero elementi"
assert get_plural_id(1) == 0  # "un elemento"
assert get_plural_id(2) == 1  # "due elementi"
assert get_plural_id(10) == 1 # "dieci elementi"
```

This module enables proper Italian pluralization in Web2py applications, supporting the rich morphological patterns of this Romance language.