# gluon/contrib/fpdf/fonts.py

## Overview

The fonts module provides comprehensive character width definitions for the FPDF library's core font set. This module defines precise character metrics for standard PDF fonts, enabling accurate text positioning and layout calculations within generated PDF documents.

## Key Components

### Font Width Dictionaries
The module defines a single dictionary `fpdf_charwidths` containing character width mappings for all supported fonts:
- **courier**: Fixed-width font family
- **helvetica**: Sans-serif proportional font family  
- **times**: Serif proportional font family
- **symbol**: Symbol font for special characters
- **zapfdingbats**: Decorative symbol font

### Font Variants
Each font family includes multiple style variants:
- Regular (base font)
- Bold (suffix 'B')
- Italic (suffix 'I')
- Bold Italic (suffix 'BI')

## Dependencies and Structure

### Character Encoding
- Uses ISO-8859-1 (Latin-1) encoding
- Character codes from 0x00 to 0xFF (0-255)
- Width values in 1/1000 of font size units

### Data Structure
```python
fpdf_charwidths = {
    'fontname': {
        '\x00': width_value,
        '\x01': width_value,
        ...
        '\xff': width_value
    }
}
```

## Functionality and Implementation

### Courier Font Family
```python
# Fixed-width font - all characters have same width
for i in range(0,256):
    fpdf_charwidths['courier'][chr(i)]=600
    fpdf_charwidths['courierB']=fpdf_charwidths['courier']
    fpdf_charwidths['courierI']=fpdf_charwidths['courier']
    fpdf_charwidths['courierBI']=fpdf_charwidths['courier']
```
- All characters uniformly 600 units wide
- Identical metrics for all style variants
- Ideal for code listings and tabular data

### Helvetica Font Family
Variable-width sans-serif font with distinct metrics per character:
- Regular characters vary from 222 (i) to 1000 units (\x85)
- Special handling for accented characters
- Different metrics for bold/italic variants

### Times Font Family
Variable-width serif font optimized for readability:
- More compact than Helvetica
- Distinct italic character angles
- Traditional newspaper/book typography metrics

### Symbol Font
Special mathematical and Greek characters:
- No standard ASCII mappings
- Width values only for symbol positions
- Zero width for undefined positions

### ZapfDingbats Font
Decorative symbols and bullets:
- Ornamental characters
- Wide variation in character widths
- Many undefined positions (width 0)

## Font Metrics Details

### Width Value Interpretation
- Values represent 1/1000 of the font size
- Example: Width 500 = half the font size
- Applied during text rendering calculations

### Character Coverage
Each font defines widths for:
- Control characters (0x00-0x1F)
- ASCII printable (0x20-0x7E)
- Extended Latin-1 (0x80-0xFF)

### Special Characters
Notable width definitions:
- Space (0x20): Variable per font
- Non-breaking space (0xA0): Usually matches space
- Currency symbols: Typically 556 units
- Punctuation: Highly variable

## Usage in PDF Generation

### Text Width Calculation
```python
def get_string_width(text, font, size):
    width = 0
    for char in text:
        char_width = fpdf_charwidths[font][char]
        width += char_width * size / 1000
    return width
```

### Line Breaking
Character widths enable:
- Automatic text wrapping
- Justified text alignment
- Precise positioning

### Font Selection
Width data supports:
- Optimal font choice for space constraints
- Mixed font documents
- Accurate layout preview

## Performance Considerations

### Memory Efficiency
- Pre-calculated static data
- No runtime computation needed
- Minimal memory footprint (~10KB)

### Lookup Performance
- O(1) dictionary access
- Direct character indexing
- No string manipulation required

## Font Characteristics

### Courier (Monospace)
- Width: 600 units uniform
- Use cases: Code, tables, forms
- Advantages: Predictable layout

### Helvetica (Sans-serif)
- Width range: 222-1000 units
- Use cases: Headers, modern documents
- Advantages: Clean, readable

### Times (Serif)
- Width range: 250-980 units
- Use cases: Body text, formal documents
- Advantages: Space-efficient, traditional

### Symbol
- Special characters only
- Mathematical symbols
- Greek alphabet

### ZapfDingbats
- Decorative elements
- Bullets and ornaments
- Visual separators

## Integration Notes

### FPDF Core Integration
- Referenced by fpdf.py for width calculations
- Critical for multi-cell text operations
- Enables accurate page layout

### Font File Coordination
- Metrics must match actual font files
- Standard PDF core fonts assumed
- No external font loading required

## Limitations and Constraints

### Character Set
- Limited to Latin-1 encoding
- No Unicode support in base implementation
- Extended characters require font embedding

### Font Variants
- Only four variants per family
- No light/medium/heavy weights
- No condensed/expanded variants

### Precision
- Integer width values only
- 1/1000 unit granularity
- Rounding may affect very small text

## Example Width Comparisons

### Character 'A' (0x41)
- Courier: 600
- Helvetica: 667
- Times: 722
- Symbol: 722

### Character 'i' (0x69)
- Courier: 600
- Helvetica: 222
- Times: 278
- Symbol: 329

### Space Character (0x20)
- Courier: 600
- Helvetica: 278
- Times: 250
- Symbol: 250

This demonstrates the significant width variations between fonts, particularly between fixed and proportional typefaces.