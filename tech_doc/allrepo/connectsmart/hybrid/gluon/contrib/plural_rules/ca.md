# Catalan Plural Rules Module

**File**: `gluon/contrib/plural_rules/ca.py`  
**Language**: Catalan (ca)  
**Type**: Pluralization Rules Implementation  
**Framework**: Web2py Gluon Framework

## Overview

This module implements pluralization rules for Catalan language support in Web2py applications. Catalan follows a binary pluralization system but has complex morphological rules for plural formation.

## Language Profile

### Basic Information
- **Language Family**: Indo-European → Romance → Western Romance
- **ISO Code**: ca
- **Native Name**: català
- **Regions**: Catalonia, Valencia, Balearic Islands, Andorra, parts of France and Italy
- **Speakers**: ~10 million native speakers
- **Writing System**: Latin script

### Pluralization Pattern
Catalan uses a **binary pluralization system** (2 forms):
1. **Singular** (n = 1): un element
2. **Plural** (n ≠ 1): dos elements

## Technical Implementation

### Configuration
```python
nplurals = 2  # Binary pluralization system
```

### Plural ID Calculation
```python
get_plural_id = lambda n: int(n != 1)
```

**Logic**:
- Returns `0` for singular (n = 1)
- Returns `1` for plural (n ≠ 1)

### Complex Plural Construction
```python
construct_plural_form = lambda word, plural_id: (
    word[:-2] + 'gues' if word[-2:] == 'ga' else
    word[:-2] + 'ques' if word[-2:] == 'ca' else
    word[:-2] + 'ces' if word[-2:] == 'ça' else
    word[:-2] + 'ges' if word[-2:] == 'ja' else
    word[:-2] + 'ües' if word[-3:] in ('gua', 'qua') else
    word[:-1] + 'es' if word[-1:] == 'a' else
    word if word[-1:] == 's' else
    word + 's'
)
```

## Catalan Grammar Rules

### Consonant Changes
- **-ga** → **-gues**: amiga → amigues (friend)
- **-ca** → **-ques**: biblioteca → biblioteques (library)
- **-ça** → **-ces**: peça → peces (piece)
- **-ja** → **-ges**: platja → platges (beach)

### Vowel + Consonant Groups
- **-gua** → **-gües**: llengua → llengües (language)
- **-qua** → **-qües**: pasqua → pasqües (easter)

### Regular Patterns
- **-a** → **-es**: casa → cases (house)
- **-e, -i, -o, -u** → **+s**: home → homes (man)
- Already ending in **-s**: no change

### Examples
- gat → gats (cat → cats)
- dona → dones (woman → women)
- nit → nits (night → nights)
- paraigua → paraigües (umbrella → umbrellas)

## Phonetic Considerations

### Pronunciation Rules
- Spelling changes maintain pronunciation
- Silent letters in plural forms
- Stress pattern preservation

### Dialectal Variations
- **Eastern Catalan**: Standard pluralization
- **Western Catalan**: Some pronunciation differences
- **Balearic**: Regional variations
- **Algherese**: Sardinian Catalan variants

## Integration with Web2py

### Usage in Templates
```python
{{=T.plural(count, 'item', 'items')}}  # Uses Catalan rules
```

### Message Files
Language files in `applications/*/languages/ca.py`:
```python
{
'item': 'element',
'items': 'elements',
'library': 'biblioteca',
'libraries': 'biblioteques',
# Catalan translations
}
```

## Cultural Context

### Official Status
- Co-official in Catalonia with Spanish
- Official in Andorra (sole official language)
- Protected minority language in France and Italy

### Digital Presence
- Growing online content
- Software localization
- Educational applications

### Usage Domains
- Education and academia
- Government and public services
- Media and publishing
- Technology and business

## Testing Examples

### Number Validation
```python
assert get_plural_id(0) == 1  # "zero elements"
assert get_plural_id(1) == 0  # "un element"
assert get_plural_id(2) == 1  # "dos elements"
assert get_plural_id(10) == 1 # "deu elements"
```

### Plural Construction Tests
```python
assert construct_plural_form('casa', 1) == 'cases'
assert construct_plural_form('amiga', 1) == 'amigues'
assert construct_plural_form('biblioteca', 1) == 'biblioteques'
assert construct_plural_form('platja', 1) == 'platges'
assert construct_plural_form('paraigua', 1) == 'paraigües'
```

### Edge Cases
```python
assert get_plural_id(-1) == 1  # Negative numbers
assert get_plural_id(1.0) == 0 # Float equality
assert get_plural_id(1.1) == 1 # Non-integer
```

## Linguistic Features

### Vowel System
- Open vs. closed vowels: è/é, ò/ó
- Neutral vowel (ə) in unstressed syllables
- Vowel reduction in plural forms

### Consonant Clusters
- Complex consonant combinations
- Gemination in some dialects
- Final consonant devoicing

### Morphophonology
- Automatic spelling adjustments
- Phonetic-based plural rules
- Stress preservation patterns

## Related Components

### Similar Romance Languages
- **Spanish** (es.py): Simpler pluralization
- **French** (fr.py): Similar complexity
- **Italian** (it.py): Related patterns
- **Portuguese** (pt.py): Romance family

### Dependencies
- **gluon.languages**: Translation framework
- **Unicode**: Special character support (ç, ü, à, è, etc.)
- Language files in applications directory

This module enables proper Catalan pluralization in Web2py applications, handling the complex morphological rules while supporting the rich linguistic heritage of the Catalan-speaking regions.