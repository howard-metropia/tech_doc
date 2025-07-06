# Spanish Plural Rules Module

**File**: `gluon/contrib/plural_rules/es.py`  
**Language**: Spanish (es)  
**Type**: Pluralization Rules Implementation  
**Framework**: Web2py Gluon Framework

## Overview

This module implements pluralization rules for Spanish language support in Web2py applications. Spanish follows a binary pluralization system with two forms: singular and plural, along with specific construction rules for different word endings.

## Language Profile

### Basic Information
- **Language Family**: Indo-European → Romance → Western Romance → Ibero-Romance
- **ISO Code**: es
- **Native Name**: español, castellano
- **Regions**: Spain, Latin America, parts of US, Equatorial Guinea, Philippines
- **Speakers**: ~500 million native speakers (2nd most spoken language globally)
- **Writing System**: Latin script with Spanish orthography

### Pluralization Pattern
Spanish uses a **binary pluralization system** (2 forms):
1. **Singular** (n = 1): un elemento
2. **Plural** (n ≠ 1): dos elementos

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

### Automatic Plural Construction
```python
construct_plural_form = lambda word, plural_id: (
    word + 'es' if word[-1:] in ('s', 'x', 'y', 'l', 'r', 'n', 'd', 'z', 'j') or
                   word[-2:] == 'ch'
    else word + 's'
)
```

**Rules**:
- Add **-es** for words ending in: s, x, y, l, r, n, d, z, j, ch
- Add **-s** for all other words

### Examples
- n=0 → plural_id=1 (cero elementos)
- n=1 → plural_id=0 (un elemento)
- n=2 → plural_id=1 (dos elementos)
- n=5 → plural_id=1 (cinco elementos)

## Spanish Grammar Rules

### Regular Plurals

**Standard -s ending** (vowels):
- casa → casas (house → houses)
- libro → libros (book → books)
- estudiante → estudiantes (student → students)

**-es ending** (consonants and special cases):
- hospital → hospitales (hospital → hospitals)
- ciudad → ciudades (city → cities)
- reloj → relojes (watch → watches)
- rey → reyes (king → kings)

### Specific Patterns

**Words ending in -z**:
- luz → luces (light → lights)
- vez → veces (time → times)
- pez → peces (fish → fishes)

**Words ending in stressed vowel + -s**:
- autobús → autobuses (bus → buses)
- compás → compases (compass → compasses)

**Words ending in -ch**:
- sándwich → sándwiches (sandwich → sandwiches)

### Gender Agreement
Spanish nouns have gender that affects articles and adjectives:
- **Masculine**: el libro → los libros
- **Feminine**: la casa → las casas
- **Mixed groups**: Always use masculine plural

## Regional Variations

### Peninsular Spanish (Spain)
- Standard pluralization rules
- Distinction between tú/vosotros
- Some vocabulary differences

### Latin American Spanish
- Same pluralization rules
- Uses ustedes instead of vosotros
- Regional vocabulary variations

### Specific Regional Forms
- **Mexican Spanish**: Standard rules
- **Argentinian Spanish**: Standard rules + unique vocabulary
- **Colombian Spanish**: Standard rules
- **Caribbean Spanish**: Pronunciation differences, same written rules

## Integration with Web2py

### Usage in Templates
```python
{{=T.plural(count, 'item', 'items')}}  # Uses Spanish rules
```

### Automatic Construction
```python
# These will be automatically constructed:
{{=T.plural(count, 'casa')}}     # → "casa"/"casas"
{{=T.plural(count, 'hospital')}} # → "hospital"/"hospitales"
{{=T.plural(count, 'ciudad')}}   # → "ciudad"/"ciudades"
```

### Message Files
Language files in `applications/*/languages/es.py`:
```python
{
'item': 'elemento',
'items': 'elementos',
'house': 'casa',
'houses': 'casas',
'city': 'ciudad',
'cities': 'ciudades',
# Spanish translations
}
```

## Construction Testing

### Vowel Endings (add -s)
```python
assert construct_plural_form('casa', 1) == 'casas'
assert construct_plural_form('libro', 1) == 'libros'
assert construct_plural_form('estudiante', 1) == 'estudiantes'
```

### Consonant Endings (add -es)
```python
assert construct_plural_form('hospital', 1) == 'hospitales'
assert construct_plural_form('ciudad', 1) == 'ciudades'
assert construct_plural_form('reloj', 1) == 'relojes'
assert construct_plural_form('rey', 1) == 'reyes'
```

### Special Cases
```python
assert construct_plural_form('sándwich', 1) == 'sándwiches'
```

## Accent and Orthography

### Stress Patterns
Spanish stress rules affect plural formation:
- **Agudas** (stress on last syllable): add -es
- **Llanas** (stress on second-to-last): usually add -s
- **Esdrújulas** (stress on third-to-last): maintain stress

### Written Accents
Some words change accents in plural:
- joven → jóvenes (young person → young people)
- examen → exámenes (exam → exams)

### Template Integration
```html
<meta charset="utf-8">
<div lang="es">
    {{=T.plural(count, messages)}}
</div>
```

## Cultural Context

### Global Language
- Second most spoken language worldwide
- Growing digital presence
- Important for international business

### Digital Applications
- Major language for web content
- Mobile app localization
- E-commerce platforms

### Educational Context
- Widely taught as second language
- Academic and research applications
- Technical documentation

## Testing Examples

### Number Validation
```python
assert get_plural_id(0) == 1  # "cero elementos"
assert get_plural_id(1) == 0  # "un elemento"
assert get_plural_id(2) == 1  # "dos elementos"
assert get_plural_id(10) == 1 # "diez elementos"
```

### Edge Cases
```python
assert get_plural_id(-1) == 1  # Negative numbers
assert get_plural_id(1.0) == 0 # Float equality
assert get_plural_id(1.1) == 1 # Non-integer
```

## Related Components

### Other Romance Languages
- **French** (fr.py): Related Romance language
- **Italian** (it.py): Similar patterns
- **Portuguese** (pt.py): Close linguistic relative
- **Catalan** (ca.py): Ibero-Romance family

### Dependencies
- **gluon.languages**: Translation framework
- **Unicode**: Accent character support (á, é, í, ó, ú, ñ)
- Language files in applications directory

This module enables proper Spanish pluralization in Web2py applications, supporting the regular morphological patterns of Spanish while accommodating regional variations and cultural contexts across the Spanish-speaking world.