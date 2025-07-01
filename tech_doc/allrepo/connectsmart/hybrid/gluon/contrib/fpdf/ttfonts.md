# gluon/contrib/fpdf/ttfonts.py

## Overview

The ttfonts.py module provides TrueType font file parsing and processing capabilities for the FPDF library. It enables the use of custom TrueType fonts in PDF documents by extracting font metrics, character mappings, and generating font subsets for efficient PDF embedding.

## Key Components

### Main Class: TTFontFile
A comprehensive TrueType font parser that:
- Reads and parses TTF file structure
- Extracts font metrics and properties
- Handles character encoding mappings
- Supports font subsetting
- Generates PDF-compatible font descriptors

### Constants and Configuration
```python
# TrueType header selection
_TTF_MAC_HEADER = False  # Use Windows header format

# Glyph flags for composite glyphs
GF_WORDS = (1 << 0)      # Word arguments
GF_SCALE = (1 << 3)      # Scale values
GF_MORE = (1 << 5)       # More components follow
GF_XYSCALE = (1 << 6)    # Separate X/Y scales
GF_TWOBYTWO = (1 << 7)   # 2x2 transformation
```

## TrueType Font Structure

### Font Tables
The module handles standard TrueType tables:
- **head**: Font header information
- **hhea**: Horizontal header
- **maxp**: Maximum profile
- **hmtx**: Horizontal metrics
- **cmap**: Character to glyph mapping
- **name**: Font naming table
- **OS/2**: OS/2 and Windows metrics
- **post**: PostScript information
- **cvt**: Control value table
- **fpgm**: Font program
- **glyf**: Glyph data
- **loca**: Glyph location index
- **prep**: Control value program

### Table Reading
```python
def read_table(self, tag):
    """Read specific table from font file"""
    if tag not in self.tables:
        return None
    
    offset = self.tables[tag]['offset']
    length = self.tables[tag]['length']
    
    self.fh.seek(offset)
    return self.fh.read(length)
```

## Font Parsing Process

### Initialization
```python
class TTFontFile:
    def __init__(self):
        self.maxStrLenRead = 200000  # Maximum string length
        self.unitsPerEm = 0          # Font units per em
        self.bbox = []               # Font bounding box
        self.numTables = 0           # Number of tables
        self.tables = {}             # Table directory
        self.glyphPos = {}           # Glyph positions
        self.charWidths = {}         # Character widths
        self.glyphSet = {}           # Used glyphs
```

### Font File Reading
```python
def load_font(self, filename):
    """Load and parse TrueType font file"""
    with open(filename, 'rb') as self.fh:
        # Read header
        self.read_header()
        
        # Read table directory
        self.read_table_directory()
        
        # Extract required tables
        self.read_head_table()
        self.read_hhea_table()
        self.read_maxp_table()
        self.read_hmtx_table()
        self.read_cmap_table()
        self.read_name_table()
```

## Character Mapping

### CMAP Processing
```python
def read_cmap_table(self):
    """Read character to glyph mapping table"""
    cmap_offset = self.seek_table("cmap")
    
    # Read platform entries
    version = self.read_ushort()
    numTables = self.read_ushort()
    
    # Find Unicode or Windows Symbol mapping
    for i in range(numTables):
        platformID = self.read_ushort()
        encodingID = self.read_ushort()
        offset = self.read_ulong()
        
        if (platformID == 3 and encodingID == 1) or \
           (platformID == 0):  # Unicode
            self.read_cmap_subtable(cmap_offset + offset)
```

### Format 4 CMAP
```python
def read_format4_cmap(self, offset):
    """Read format 4 character mapping (most common)"""
    # Read segment count
    segCount = self.read_ushort() // 2
    
    # Read parallel arrays
    endCount = self.read_array('H', segCount)
    startCount = self.read_array('H', segCount)
    idDelta = self.read_array('h', segCount)
    idRangeOffset = self.read_array('H', segCount)
    
    # Build character to glyph map
    self.build_char_map(startCount, endCount, idDelta, idRangeOffset)
```

## Font Metrics Extraction

### Glyph Metrics
```python
def extract_glyph_info(self, glyph_id):
    """Extract metrics for specific glyph"""
    # Get glyph data offset
    offset = self.get_glyph_offset(glyph_id)
    
    if offset == self.get_glyph_offset(glyph_id + 1):
        # Empty glyph
        return {'width': 0, 'lsb': 0}
    
    # Read glyph header
    self.fh.seek(offset)
    numberOfContours = self.read_short()
    xMin = self.read_short()
    yMin = self.read_short()
    xMax = self.read_short()
    yMax = self.read_short()
    
    return {
        'width': self.get_hmtx_width(glyph_id),
        'lsb': self.get_hmtx_lsb(glyph_id),
        'xMin': xMin, 'yMin': yMin,
        'xMax': xMax, 'yMax': yMax
    }
```

### Width Calculation
```python
def get_char_width(self, char_code):
    """Get width of character in font units"""
    if char_code in self.charToGlyph:
        glyph_id = self.charToGlyph[char_code]
        return self.glyphWidths[glyph_id]
    return 0
```

## Font Subsetting

### Glyph Collection
```python
def add_glyph_subset(self, char_code):
    """Add character to font subset"""
    if char_code in self.charToGlyph:
        glyph_id = self.charToGlyph[char_code]
        self.glyphSet[glyph_id] = True
        
        # Handle composite glyphs
        if self.is_composite_glyph(glyph_id):
            self.add_composite_glyphs(glyph_id)
```

### Composite Glyph Handling
```python
def parse_composite_glyph(self, glyph_id):
    """Parse composite glyph components"""
    offset = self.get_glyph_offset(glyph_id)
    self.fh.seek(offset + 10)  # Skip header
    
    flags = GF_MORE
    while flags & GF_MORE:
        flags = self.read_ushort()
        glyphIdx = self.read_ushort()
        
        # Add component to subset
        self.glyphSet[glyphIdx] = True
        
        # Skip transformation data
        self.skip_composite_args(flags)
```

## PDF Font Descriptor Generation

### Font Descriptor Creation
```python
def make_font_descriptor(self):
    """Generate PDF font descriptor dictionary"""
    descriptor = {
        'Ascent': self.ascent,
        'Descent': self.descent,
        'CapHeight': self.capHeight,
        'Flags': self.flags,
        'FontBBox': f'[{self.bbox[0]} {self.bbox[1]} {self.bbox[2]} {self.bbox[3]}]',
        'ItalicAngle': self.italicAngle,
        'StemV': self.stemV,
        'MissingWidth': self.defaultWidth
    }
    return descriptor
```

### Font Embedding Data
```python
def get_font_program(self):
    """Extract font program for embedding"""
    # Collect required tables
    tables = ['cvt ', 'fpgm', 'prep', 'glyf', 'hmtx', 'loca', 'maxp', 'head']
    
    font_data = b''
    for table in tables:
        if table in self.tables:
            font_data += self.read_table(table)
    
    return font_data
```

## Utility Functions

### 32-bit Arithmetic
```python
def sub32(x, y):
    """32-bit subtraction with overflow handling"""
    xlo = x[1]
    xhi = x[0]
    ylo = y[1]
    yhi = y[0]
    
    if (ylo > xlo):
        xlo += 1 << 16
        xhi -= 1
    
    reslo = xlo - ylo
    reshi = xhi - yhi
    
    return (reshi, reslo)
```

### Data Reading Helpers
```python
def read_ushort(self):
    """Read unsigned 16-bit integer"""
    return struct.unpack('>H', self.fh.read(2))[0]

def read_short(self):
    """Read signed 16-bit integer"""
    return struct.unpack('>h', self.fh.read(2))[0]

def read_ulong(self):
    """Read unsigned 32-bit integer"""
    return struct.unpack('>L', self.fh.read(4))[0]
```

## Error Handling

### Validation
```python
def validate_font(self):
    """Validate font file structure"""
    # Check required tables
    required = ['head', 'hhea', 'maxp', 'hmtx', 'cmap']
    for table in required:
        if table not in self.tables:
            die(f"Required table '{table}' missing")
    
    # Validate version
    if self.version not in [0x00010000, 0x74727565]:
        die("Not a valid TrueType font file")
```

### Error Recovery
```python
def safe_read_table(self, tag):
    """Safely read table with error handling"""
    try:
        return self.read_table(tag)
    except Exception as e:
        warnings.warn(f"Failed to read table {tag}: {e}")
        return None
```

## Performance Optimization

### Caching Strategy
- Cache parsed table data
- Reuse glyph metrics
- Minimize file seeking

### Memory Management
- Stream large tables
- Release unused data
- Efficient data structures

## Integration with FPDF

### Font Registration
```python
# In FPDF
def add_font(self, family, style='', file=''):
    """Add TrueType font to PDF"""
    ttf = TTFontFile()
    ttf.load_font(file)
    
    # Extract metrics
    font_dict = ttf.make_font_descriptor()
    
    # Register with FPDF
    self.fonts[family + style] = font_dict
```

### Width Calculation
```python
# Get string width using TTF metrics
def get_ttf_string_width(self, text, font):
    """Calculate text width using TrueType metrics"""
    ttf = self.fonts[font]['ttf']
    width = 0
    
    for char in text:
        char_width = ttf.get_char_width(ord(char))
        width += char_width * self.font_size / ttf.unitsPerEm
    
    return width
```

## Best Practices

### Font Loading
1. Validate font files before use
2. Cache parsed font data
3. Handle missing glyphs gracefully
4. Use font subsetting for size optimization

### Error Handling
1. Validate table presence
2. Check data bounds
3. Provide meaningful error messages
4. Fall back to default fonts when needed

### Performance
1. Parse only required tables
2. Cache frequently used metrics
3. Use memory mapping for large files
4. Implement lazy loading where possible