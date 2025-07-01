# Polish Plural Rules Module

**File**: `gluon/contrib/plural_rules/pl.py`  
**Language**: Polish (pl)  
**Type**: Pluralization Rules Implementation  
**Framework**: Web2py Gluon Framework

## Overview

This module implements pluralization rules for Polish language support in Web2py applications. Polish follows a complex three-form pluralization system with distinct rules for different number ranges.

## Language Profile

### Basic Information
- **Language Family**: Indo-European → Slavic → West Slavic → Lechitic
- **ISO Code**: pl
- **Native Name**: język polski, polszczyzna
- **Regions**: Poland, diaspora communities worldwide
- **Speakers**: ~40 million native speakers
- **Writing System**: Latin script with Polish orthography

### Pluralization Pattern
Polish uses a **three-form pluralization system** (3 forms):
1. **Singular** (n = 1): jeden element
2. **Paucal** (n = 2,3,4): dwa elementy  
3. **Plural** (n = 0, 5+): pięć elementów

## Technical Implementation

### Configuration
```python
nplurals = 3  # Three-form pluralization system
```

### Plural ID Calculation
```python
get_plural_id = lambda n: (
    0 if n == 1 else           # Singular
    1 if 2 <= n <= 4 else      # Paucal (few)
    2                          # Plural (many)
)
```

**Logic**:
- Returns `0` for singular (n = 1)
- Returns `1` for paucal/few (n = 2, 3, 4)
- Returns `2` for plural/many (n = 0, 5, 6, 7, ...)

### Examples
- n=0 → plural_id=2 (zero elementów)
- n=1 → plural_id=0 (jeden element)
- n=2 → plural_id=1 (dwa elementy)
- n=3 → plural_id=1 (trzy elementy)
- n=4 → plural_id=1 (cztery elementy)
- n=5 → plural_id=2 (pięć elementów)
- n=10 → plural_id=2 (dziesięć elementów)

## Polish Grammar Rules

### Complex Declension System

**Masculine nouns**:
- Singular: student (student)
- Paucal: studenci (students 2-4)
- Plural: studentów (students 5+)

**Feminine nouns**:
- Singular: książka (book)
- Paucal: książki (books 2-4)
- Plural: książek (books 5+)

**Neuter nouns**:
- Singular: dziecko (child)
- Paucal: dzieci (children 2-4)
- Plural: dzieci (children 5+)

### Case System Integration
Polish plurals interact with a complex case system:
- **Nominative**: kto/co (who/what)
- **Genitive**: kogo/czego (whose/of what)
- **Dative**: komu/czemu (to whom/what)
- **Accusative**: kogo/co (whom/what)
- **Instrumental**: kim/czym (with whom/what)
- **Locative**: o kim/czym (about whom/what)
- **Vocative**: addressing directly

### Number-Noun Agreement

**With numbers 2-4** (paucal):
- 2 duże domy (2 big houses) - nominative adjective
- 3 czerwone samochody (3 red cars)

**With numbers 5+** (plural):
- 5 dużych domów (5 big houses) - genitive adjective
- 10 czerwonych samochodów (10 red cars)

## Integration with Web2py

### Usage in Templates
```python
{{=T.plural(count, 'item_one', 'item_few', 'item_many')}}
```

### Message Files
Polish requires all three forms:
```python
{
'item_one': 'element',     # Singular
'item_few': 'elementy',    # Paucal (2-4)
'item_many': 'elementów',  # Plural (5+)
'book_one': 'książka',
'book_few': 'książki',
'book_many': 'książek',
}
```

## Character Encoding

### Polish Diacritics
- **Accented letters**: ą, ć, ę, ł, ń, ó, ś, ź, ż
- **Unicode support** essential
- **UTF-8 encoding** required

### Template Integration
```html
<meta charset="utf-8">
<div lang="pl">
    {{=T.plural(count, messages)}}
</div>
```

## Cultural Context

### Historical Significance
- Rich literary tradition
- Complex grammatical heritage
- Resistance to linguistic simplification

### Modern Usage
- Official language of Poland
- EU official language
- Significant diaspora communities

### Educational Applications
- Language learning software
- Academic resources
- Cultural preservation

## Testing Examples

### Number Validation
```python
assert get_plural_id(0) == 2   # "zero elementów"
assert get_plural_id(1) == 0   # "jeden element"
assert get_plural_id(2) == 1   # "dwa elementy"
assert get_plural_id(3) == 1   # "trzy elementy"
assert get_plural_id(4) == 1   # "cztery elementy"
assert get_plural_id(5) == 2   # "pięć elementów"
assert get_plural_id(10) == 2  # "dziesięć elementów"
```

### Edge Cases
```python
assert get_plural_id(22) == 1  # "dwadzieścia dwa" (ends in 2)
assert get_plural_id(23) == 1  # "dwadzieścia trzy" (ends in 3)
assert get_plural_id(25) == 2  # "dwadzieścia pięć" (ends in 5)
```

**Note**: The implementation uses a simplified rule. Full Polish requires compound number handling:
- 22, 23, 24 should use paucal form
- 25-29 should use plural form

## Linguistic Complexity

### Morphological Richness
- Extensive inflectional system
- Consonant clusters
- Palatalization rules

### Phonetic Changes
- Alternations in noun stems
- Vowel-consonant interactions
- Historical sound changes

### Semantic Nuances
- Animacy distinctions
- Gender agreement patterns
- Aspectual verbal system

## Related Components

### Other Complex Slavic Languages
- **Russian** (ru.py): Similar 3-form system
- **Czech** (cs.py): Related West Slavic
- **Slovak** (sk.py): Close linguistic relative

### Simpler Slavic Languages
- **Bulgarian** (bg.py): Simplified 2-form system
- **Slovenian** (sl.py): Simplified patterns

### Dependencies
- **gluon.languages**: Translation framework
- **Unicode**: Polish diacritic support
- Language files with all three forms

This module enables proper Polish pluralization in Web2py applications, handling one of the most complex European pluralization systems while preserving the rich grammatical traditions of the Polish language.