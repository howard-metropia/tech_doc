# German Plural Rules Module

**File**: `gluon/contrib/plural_rules/de.py`  
**Language**: German (de)  
**Type**: Pluralization Rules Implementation  
**Framework**: Web2py Gluon Framework

## Overview

This module implements pluralization rules for German language support in Web2py applications. German follows a binary pluralization system with two forms: singular and plural.

## Language Profile

### Basic Information
- **Language Family**: Indo-European → Germanic → West Germanic
- **ISO Code**: de
- **Native Name**: Deutsch
- **Regions**: Germany, Austria, Switzerland, Luxembourg, parts of Belgium and Italy
- **Speakers**: ~100 million native speakers
- **Writing System**: Latin script with umlauts (ä, ö, ü, ß)

### Pluralization Pattern
German uses a **binary pluralization system** (2 forms):
1. **Singular** (n = 1): ein Element
2. **Plural** (n ≠ 1): zwei Elemente

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

### Examples
- n=0 → plural_id=1 (null Elemente)
- n=1 → plural_id=0 (ein Element)
- n=2 → plural_id=1 (zwei Elemente)
- n=5 → plural_id=1 (fünf Elemente)

## German Grammar Rules

### Complex Plural Formation
German has multiple plural patterns that cannot be handled by simple construction:

**-e ending**:
- der Hund → die Hunde (dog → dogs)
- das Jahr → die Jahre (year → years)

**-er ending**:
- das Kind → die Kinder (child → children)
- der Mann → die Männer (man → men)

**-en/-n ending**:
- die Frau → die Frauen (woman → women)
- der Student → die Studenten (student → students)

**-s ending** (foreign words):
- das Auto → die Autos (car → cars)
- das Hotel → die Hotels (hotel → hotels)

**No change**:
- der Lehrer → die Lehrer (teacher → teachers)
- das Mädchen → die Mädchen (girl → girls)

### Umlaut Changes
Many German nouns add umlauts in plural:
- der Vater → die Väter (father → fathers)
- das Buch → die Bücher (book → books)
- der Kopf → die Köpfe (head → heads)

### Gender and Articles
- **Masculine**: der → die
- **Feminine**: die → die  
- **Neuter**: das → die
- All plurals use "die" article

## Integration with Web2py

### Usage in Templates
```python
{{=T.plural(count, 'item', 'items')}}  # Uses German rules
```

### Message Files
Language files in `applications/*/languages/de.py`:
```python
{
'item': 'Element',
'items': 'Elemente',
'book': 'Buch',
'books': 'Bücher',
# German translations
}
```

## Character Encoding

### Special Characters
- **Umlauts**: ä, ö, ü, Ä, Ö, Ü
- **Eszett**: ß (sharp s)
- **UTF-8 encoding** required

### Template Integration
```html
<meta charset="utf-8">
<div lang="de">
    {{=T.plural(count, messages)}}
</div>
```

## Regional Variations

### Standard German (Hochdeutsch)
- Used in formal contexts
- Standard pluralization rules
- Media and education language

### Austrian German
- Some vocabulary differences
- Same pluralization rules
- Regional expressions

### Swiss German
- Spoken dialect very different
- Written form follows standard rules
- No ß character used

## Grammatical Context

### Declension System
German has four cases affecting article forms:
- **Nominativ**: die Bücher (subject)
- **Akkusativ**: die Bücher (direct object)
- **Dativ**: den Büchern (indirect object)
- **Genitiv**: der Bücher (possessive)

### Adjective Agreement
Adjectives must agree with plural nouns:
- gute Bücher (good books)
- kleine Kinder (small children)

## Testing Examples

### Number Validation
```python
assert get_plural_id(0) == 1  # "null Elemente"
assert get_plural_id(1) == 0  # "ein Element"
assert get_plural_id(2) == 1  # "zwei Elemente"
assert get_plural_id(10) == 1 # "zehn Elemente"
```

### Edge Cases
```python
assert get_plural_id(-1) == 1  # Negative numbers
assert get_plural_id(1.0) == 0 # Float equality
assert get_plural_id(1.1) == 1 # Non-integer
```

## Cultural Considerations

### Formal Address
- **Sie** (formal you) always uses plural verb forms
- Important for business applications
- Respect and politeness conventions

### Compound Words
German forms long compound words:
- Computerprogramm → Computerprogramme
- Pluralization affects final component

### Business Context
- Precise terminology important
- Technical documentation standards
- Legal and formal language requirements

## Related Components

### Other Germanic Languages
- **English** (en.py): Simplified Germanic system
- **Dutch** (nl.py): Related Germanic language
- **Afrikaans** (af.py): Germanic descendant

### Dependencies
- **gluon.languages**: Translation framework
- **Unicode**: Umlaut character support
- Language files in applications directory

This module enables proper German pluralization in Web2py applications, supporting the binary plural system while accommodating the complex morphological patterns of the German language.