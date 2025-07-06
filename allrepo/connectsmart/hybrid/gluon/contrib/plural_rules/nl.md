# Dutch Plural Rules Module

**File**: `gluon/contrib/plural_rules/nl.py`  
**Language**: Dutch (nl)  
**Type**: Pluralization Rules Implementation  
**Framework**: Web2py Gluon Framework

## Overview

This module implements pluralization rules for Dutch language support in Web2py applications. Dutch follows a binary pluralization system with two forms: singular and plural.

## Language Profile

### Basic Information
- **Language Family**: Indo-European → Germanic → West Germanic
- **ISO Code**: nl
- **Native Name**: Nederlands
- **Regions**: Netherlands, Belgium (Flanders), Suriname
- **Speakers**: ~24 million native speakers
- **Writing System**: Latin script

### Pluralization Pattern
Dutch uses a **binary pluralization system** (2 forms):
1. **Singular** (n = 1): een element
2. **Plural** (n ≠ 1): twee elementen

## Technical Implementation

### Configuration
```python
nplurals = 2  # Binary pluralization system
```

### Plural ID Calculation
```python
get_plural_id = lambda n: int(n != 1)
```

## Dutch Grammar Rules

### Regular Plural Formation

**Add -en (most common)**:
- huis → huizen (house → houses)
- boek → boeken (book → books)
- kind → kinderen (child → children)

**Add -s (newer pattern)**:
- auto → auto's (car → cars)
- café → café's (café → cafés)

### Spelling Changes
- **f → v**: brief → brieven (letter → letters)
- **s → z**: huis → huizen (house → houses)
- **Double vowel shortening**: boot → boten (boat → boats)

## Integration with Web2py

### Usage in Templates
```python
{{=T.plural(count, 'item', 'items')}}  # Uses Dutch rules
```

### Message Files
```python
{
'item': 'element',
'items': 'elementen',
'house': 'huis',
'houses': 'huizen',
}
```

## Testing Examples

### Number Validation
```python
assert get_plural_id(0) == 1  # "nul elementen"
assert get_plural_id(1) == 0  # "een element"
assert get_plural_id(2) == 1  # "twee elementen"
assert get_plural_id(10) == 1 # "tien elementen"
```

This module enables proper Dutch pluralization in Web2py applications, supporting this Germanic language's morphological patterns.