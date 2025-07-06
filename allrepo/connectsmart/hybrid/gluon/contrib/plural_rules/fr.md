# French Plural Rules Module

**File**: `gluon/contrib/plural_rules/fr.py`  
**Language**: French (fr)  
**Type**: Pluralization Rules Implementation  
**Framework**: Web2py Gluon Framework

## Overview

This module implements pluralization rules for French language support in Web2py applications. French follows a binary pluralization system but has complex morphological rules and extensive irregular plural forms.

## Language Profile

### Basic Information
- **Language Family**: Indo-European → Romance → Western Romance → Gallo-Romance
- **ISO Code**: fr
- **Native Name**: français
- **Regions**: France, Canada, Belgium, Switzerland, Africa, Pacific islands
- **Speakers**: ~280 million total speakers
- **Writing System**: Latin script with French orthography

### Pluralization Pattern
French uses a **binary pluralization system** (2 forms):
1. **Singular** (n = 1): un élément
2. **Plural** (n ≠ 1): deux éléments

## Technical Implementation

### Configuration
```python
nplurals = 2  # Binary pluralization system
```

### Plural ID Calculation
```python
get_plural_id = lambda n: int(n != 1)
```

### Complex Plural Construction
```python
def construct_plural_form(word, plural_id):
    if word in irregular:
        return irregular[word]
    if word[-1:] in ('s', 'x', 'z'):
        return word  # No change
    if word[-2:] in ('au', 'eu'):
        return word + 'x'
    if word[-2:] == 'al':
        return word[0:-2] + 'aux'
    return word + 's'
```

## French Grammar Rules

### Regular Plurals

**Standard -s ending**:
- chat → chats (cat → cats)
- maison → maisons (house → houses)
- livre → livres (book → books)

**No change for words ending in s, x, z**:
- nez → nez (nose → noses)
- prix → prix (price → prices)
- bas → bas (stocking → stockings)

**-x ending for -au, -eu**:
- château → châteaux (castle → castles)
- jeu → jeux (game → games)
- feu → feux (fire → fires)

**-aux for -al**:
- journal → journaux (newspaper → newspapers)
- animal → animaux (animal → animals)
- cheval → chevaux (horse → horses)

### Extensive Irregular Forms

**Family titles**:
- monsieur → messieurs (mister → misters)
- madame → mesdames (madam → madams)
- mademoiselle → mesdemoiselles (miss → misses)

**Body parts**:
- œil → yeux (eye → eyes)
- ciel → cieux (sky → skies)

**Special -ou words**:
- bijou → bijoux (jewel → jewels)
- caillou → cailloux (pebble → pebbles)
- chou → choux (cabbage → cabbages)
- genou → genoux (knee → knees)
- hibou → hiboux (owl → owls)
- joujou → joujoux (toy → toys)
- pou → poux (louse → lice)

**Work/material endings**:
- travail → travaux (work → works)
- corail → coraux (coral → corals)
- émail → émaux (enamel → enamels)
- vitrail → vitraux (stained glass → stained glasses)

## Integration with Web2py

### Usage in Templates
```python
{{=T.plural(count, 'item', 'items')}}  # Uses French rules
```

### Automatic Construction Examples
```python
# Regular patterns:
{{=T.plural(count, 'chat')}}    # → "chat"/"chats"
{{=T.plural(count, 'château')}} # → "château"/"châteaux"
{{=T.plural(count, 'journal')}} # → "journal"/"journaux"

# Irregular forms need dictionary entries:
{{=T.plural(count, 'œil')}}     # → "œil"/"yeux"
```

### Message Files
Language files need irregular forms:
```python
{
'item': 'élément',
'items': 'éléments',
'eye': 'œil',
'eyes': 'yeux',
'horse': 'cheval',
'horses': 'chevaux',
# All irregular forms must be explicitly defined
}
```

## Character Encoding and Accents

### French Accents
- **Acute**: é, É
- **Grave**: è, à, ù
- **Circumflex**: â, ê, î, ô, û
- **Diaeresis**: ë, ï, ü, ÿ
- **Cedilla**: ç

### Special Characters
- **Ligatures**: œ, æ
- **UTF-8 encoding** required

### Template Integration
```html
<meta charset="utf-8">
<div lang="fr">
    {{=T.plural(count, messages)}}
</div>
```

## Regional Variations

### Metropolitan French (France)
- Standard pluralization rules
- Base implementation

### Canadian French (Québec)
- Same pluralization rules
- Some vocabulary differences
- Different pronunciation but same written forms

### Belgian French
- Standard rules with regional vocabulary

### Swiss French
- Standard rules with some Germanic influences

### African French
- Standard rules in formal contexts
- Regional variations in informal speech

## Testing Examples

### Regular Construction
```python
assert construct_plural_form('chat', 1) == 'chats'
assert construct_plural_form('maison', 1) == 'maisons'
assert construct_plural_form('nez', 1) == 'nez'  # No change
assert construct_plural_form('château', 1) == 'châteaux'
assert construct_plural_form('journal', 1) == 'journaux'
```

### Irregular Forms
```python
assert construct_plural_form('œil', 1) == 'yeux'
assert construct_plural_form('monsieur', 1) == 'messieurs'
assert construct_plural_form('bijou', 1) == 'bijoux'
assert construct_plural_form('travail', 1) == 'travaux'
```

## Linguistic Complexity

### Historical Development
- Evolution from Latin caused irregular patterns
- Germanic influences in early French
- Standardization efforts over centuries

### Phonetic vs. Orthographic
- Silent letters in plurals
- Liaison rules in pronunciation
- Written vs. spoken differences

### Gender Agreement
French nouns have gender affecting articles:
- **Masculine**: le chat → les chats
- **Feminine**: la maison → les maisons

## Cultural Context

### Formal Language
- Académie française standards
- Formal vs. informal registers
- Literary and academic usage

### Global Francophonie
- International French-speaking community
- Diplomatic and cultural language
- Educational and business applications

## Related Components

### Other Romance Languages
- **Spanish** (es.py): Simpler rules
- **Italian** (it.py): Similar complexity
- **Portuguese** (pt.py): Related patterns
- **Catalan** (ca.py): Regional neighbor

### Dependencies
- **gluon.languages**: Translation framework
- **Unicode**: Accent and special character support
- **Irregular forms dictionary**: Built-in exceptions
- Language files in applications directory

This module enables proper French pluralization in Web2py applications, handling both regular morphological patterns and the extensive system of irregular plural forms that characterize the French language.