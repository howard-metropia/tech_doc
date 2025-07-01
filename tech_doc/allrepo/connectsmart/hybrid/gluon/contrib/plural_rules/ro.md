# Romanian Plural Rules Module

**File**: `gluon/contrib/plural_rules/ro.py`  
**Language**: Romanian (ro)  
**Type**: Pluralization Rules Implementation  
**Framework**: Web2py Gluon Framework

## Overview

This module implements pluralization rules for Romanian language support in Web2py applications. Romanian follows a binary pluralization system with two forms: singular and plural.

## Language Profile

### Basic Information
- **Language Family**: Indo-European → Romance → Eastern Romance
- **ISO Code**: ro
- **Native Name**: română
- **Regions**: Romania, Moldova (as Moldovan)
- **Speakers**: ~24 million native speakers
- **Writing System**: Latin script with Romanian orthography

### Pluralization Pattern
Romanian uses a **binary pluralization system** (2 forms):
1. **Singular** (n = 1): un element
2. **Plural** (n ≠ 1): două elemente

## Technical Implementation

### Configuration
```python
nplurals = 2  # Binary pluralization system
```

### Plural ID Calculation
```python
get_plural_id = lambda n: int(n != 1)
```

## Romanian Grammar Rules

### Complex Plural Formation

**Masculine nouns**:
- băiat → băieți (boy → boys)
- om → oameni (man → men)

**Feminine nouns**:
- casă → case (house → houses)
- fată → fete (girl → girls)

**Neuter nouns**:
- scaun → scaune (chair → chairs)

### Definite Article Integration
Romanian has postposed definite articles:
- casa → casele (the house → the houses)
- băiatul → băieții (the boy → the boys)

## Integration with Web2py

### Usage in Templates
```python
{{=T.plural(count, 'item', 'items')}}  # Uses Romanian rules
```

### Message Files
```python
{
'item': 'element',
'items': 'elemente',
'house': 'casă',
'houses': 'case',
}
```

## Character Encoding

### Romanian Diacritics
- **Special characters**: ă, â, î, ș, ț
- **UTF-8 encoding** required

## Testing Examples

### Number Validation
```python
assert get_plural_id(0) == 1  # "zero elemente"
assert get_plural_id(1) == 0  # "un element"
assert get_plural_id(2) == 1  # "două elemente"
assert get_plural_id(10) == 1 # "zece elemente"
```

This module enables proper Romanian pluralization in Web2py applications, supporting this Eastern Romance language's unique grammatical features.