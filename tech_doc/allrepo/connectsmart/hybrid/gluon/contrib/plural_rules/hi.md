# Hindi Plural Rules Module

**File**: `gluon/contrib/plural_rules/hi.py`  
**Language**: Hindi (hi)  
**Type**: Pluralization Rules Implementation  
**Framework**: Web2py Gluon Framework

## Overview

This module implements pluralization rules for Hindi language support in Web2py applications. Hindi follows a binary pluralization system with two forms: singular and plural.

## Language Profile

### Basic Information
- **Language Family**: Indo-European → Indo-Iranian → Indo-Aryan → Central Zone
- **ISO Code**: hi
- **Native Name**: हिन्दी (hindī)
- **Regions**: India (official), Nepal, diaspora communities
- **Speakers**: ~600+ million total speakers (native + second language)
- **Writing System**: Devanagari script

### Pluralization Pattern
Hindi uses a **binary pluralization system** (2 forms):
1. **Singular** (n = 1): एक वस्तु (ek vastu)
2. **Plural** (n ≠ 1): दो वस्तुएं (do vastuen)

## Technical Implementation

### Configuration
```python
nplurals = 2  # Binary pluralization system
```

### Plural ID Calculation
```python
get_plural_id = lambda n: int(n != 1)
```

## Hindi Grammar Rules

### Gender-Based Plurals

**Masculine nouns**:
- लड़का → लड़के (laṛkā → laṛke) - boy → boys
- आदमी → आदमी (ādmī → ādmī) - man → men (no change)

**Feminine nouns**:
- लड़की → लड़कियां (laṛkī → laṛkiyān) - girl → girls
- औरत → औरतें (aurat → auratẽ) - woman → women

### Common Patterns

**-ā ending masculines** → **-e**:
- बच्चा → बच्चे (bachchā → bachche) - child → children

**-ī ending feminines** → **-iyān**:
- रोटी → रोटियां (roṭī → roṭiyān) - bread → breads

**Invariant forms**:
- आदमी → आदमी (ādmī → ādmī) - man → men
- औरत → औरतें (aurat → auratẽ) - woman → women

## Integration with Web2py

### Usage in Templates
```python
{{=T.plural(count, 'item', 'items')}}  # Uses Hindi rules
```

### Message Files
Language files in `applications/*/languages/hi.py`:
```python
{
'item': 'वस्तु',
'items': 'वस्तुएं',
'boy': 'लड़का',
'boys': 'लड़के',
'girl': 'लड़की', 
'girls': 'लड़कियां',
# Hindi translations in Devanagari
}
```

## Character Encoding

### Devanagari Script
- **Consonants**: क ख ग घ च छ ज झ ट ठ ड ढ त थ द ध न प फ ब भ म य र ल व श ष स ह
- **Vowels**: अ आ इ ई उ ऊ ऋ ए ऐ ओ औ
- **Vowel marks**: ा ि ी ु ू ृ े ै ो ौ
- **UTF-8 encoding** required

### Template Integration
```html
<meta charset="utf-8">
<div lang="hi">
    {{=T.plural(count, messages)}}
</div>
```

## Testing Examples

### Number Validation
```python
assert get_plural_id(0) == 1  # "शून्य वस्तुएं"
assert get_plural_id(1) == 0  # "एक वस्तु"
assert get_plural_id(2) == 1  # "दो वस्तुएं"
assert get_plural_id(10) == 1 # "दस वस्तुएं"
```

## Related Components

### Related Indo-Aryan Languages
- Similar binary patterns in related languages
- Complex morphological systems

### Dependencies
- **gluon.languages**: Translation framework
- **Unicode**: Devanagari script support
- Language files in applications directory

This module enables proper Hindi pluralization in Web2py applications, supporting the rich grammatical tradition of this major world language.