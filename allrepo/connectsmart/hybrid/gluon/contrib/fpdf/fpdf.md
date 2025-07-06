# gluon/contrib/fpdf/fpdf.py

## Overview

The fpdf.py module is the core implementation of the FPDF library for Python, providing comprehensive PDF generation capabilities. Originally ported from PHP FPDF by Olivier Plathey, this Python implementation enables creation of PDF documents programmatically with support for text, images, graphics, and complex layouts.

## Key Components

### Core Class: FPDF
The main PDF generation class that handles:
- Document creation and structure
- Page management
- Text and font operations
- Graphics drawing
- Image embedding
- Document metadata

### Global Configuration
```python
FPDF_VERSION = '1.7.2'
FPDF_FONT_DIR = os.path.join(os.path.dirname(__file__),'font')
FPDF_CACHE_MODE = 0  # 0 - in same folder, 1 - none, 2 - hash
FPDF_CACHE_DIR = None
SYSTEM_TTFONTS = None
```

### Page Format Constants
```python
PAGE_FORMATS = {
    "a3": (841.89, 1190.55),
    "a4": (595.28, 841.89),
    "a5": (420.94, 595.28),
    "letter": (612, 792),
    "legal": (612, 1008),
}
```

## Class Architecture

### Initialization
```python
def __init__(self, orientation='P', unit='mm', format='A4'):
    # Document state management
    self.page = 0                   # current page number
    self.n = 2                      # current object number
    self.buffer = ''                # in-memory PDF content
    self.pages = {}                 # pages and metadata
    self.state = 0                  # document state
    
    # Font management
    self.fonts = {}                 # used fonts
    self.font_files = {}            # font files
    self.core_fonts = {             # standard PDF fonts
        'courier', 'helvetica', 'times', 'symbol', 'zapfdingbats'
    }
    
    # Graphics state
    self.draw_color = '0 G'
    self.fill_color = '0 g'
    self.text_color = '0 g'
```

### Unit System Support
The module supports multiple measurement units:
- **pt**: Points (1/72 inch)
- **mm**: Millimeters
- **cm**: Centimeters
- **in**: Inches

Scale factor calculation:
```python
if unit == "pt":
    self.k = 1
elif unit == "mm":
    self.k = 72 / 25.4
elif unit == "cm":
    self.k = 72 / 2.54
elif unit == 'in':
    self.k = 72.
```

## Core Functionality

### Page Management
- **add_page()**: Create new page
- **set_margins()**: Configure page margins
- **set_auto_page_break()**: Automatic page breaking
- **page_no()**: Get current page number

### Text Operations
- **set_font()**: Select font family, style, and size
- **text()**: Output text at specific position
- **write()**: Output flowing text
- **cell()**: Output text in rectangular cell
- **multi_cell()**: Output text with automatic line breaks

### Graphics Operations
- **line()**: Draw line
- **rect()**: Draw rectangle
- **circle()**: Draw circle (via extension)
- **set_draw_color()**: Set line color
- **set_fill_color()**: Set fill color

### Image Support
- **image()**: Embed JPEG, PNG, GIF images
- Automatic format detection
- Scaling and positioning options

## Advanced Features

### Font Management
```python
def add_font(self, family, style='', fname='', uni=False):
    """Add a TrueType or Type1 font"""
    # Supports custom fonts
    # Unicode font support
    # Font subsetting capabilities
```

### Document Metadata
```python
def set_title(self, title)
def set_author(self, author)
def set_subject(self, subject)
def set_keywords(self, keywords)
def set_creator(self, creator)
```

### Compression
- Automatic content compression using zlib
- Configurable via set_compression()
- Reduces file size significantly

### Link Support
- Internal document links
- External URL links
- Clickable regions

## Implementation Details

### State Management
Document states:
- 0: No document
- 1: Document started
- 2: Page opened
- 3: Document closed

### Buffer Management
- In-memory PDF construction
- Efficient string concatenation
- Streaming output support

### Coordinate System
- Origin at top-left
- Y-axis increases downward
- Configurable units

### Error Handling
```python
def error(self, msg):
    """Fatal error handling"""
    raise RuntimeError('FPDF error: ' + msg)
```

## Performance Features

### Caching System
- Font metric caching
- Parsed font file caching
- Configurable cache modes

### Memory Optimization
- Lazy resource loading
- Efficient buffer management
- Minimal memory footprint

## Security Considerations

### Document Protection
- Password protection support
- Permission restrictions
- Encryption capabilities

### Input Validation
- Path traversal prevention
- Format validation
- Safe file operations

## Integration Features

### Decorator Pattern
```python
@check_page
def text(self, x, y, txt=''):
    """Output text at position"""
    # Ensures page is open
```

### Helper Functions
```python
def set_global(var, val):
    """Set global configuration"""
    globals()[var] = val

def load_cache(filename):
    """Load pickled cache data"""
    # Safe unpickling with error handling
```

## Output Options

### Output Destinations
- **'I'**: Send to browser inline
- **'D'**: Force download
- **'F'**: Save to file
- **'S'**: Return as string

### File Generation
```python
def output(self, name='', dest=''):
    """Generate PDF output"""
    # Finalize document
    # Apply compression
    # Handle destination
```

## Font Handling

### Core Fonts
Built-in support for 14 standard PDF fonts:
- Courier (4 variants)
- Helvetica (4 variants)
- Times (4 variants)
- Symbol
- ZapfDingbats

### Custom Fonts
- TrueType font support
- Type1 font support
- Unicode capabilities
- Font subsetting

## Error Recovery

### Validation Methods
```python
def _dochecks(self):
    """Perform environment checks"""
    # Verify dependencies
    # Check permissions
    # Validate configuration
```

### Graceful Degradation
- Missing font fallbacks
- Image format alternatives
- Encoding conversions

## Usage Patterns

### Basic Document
```python
pdf = FPDF()
pdf.add_page()
pdf.set_font('Arial', 'B', 16)
pdf.cell(40, 10, 'Hello World!')
pdf.output('document.pdf', 'F')
```

### Multi-page Document
```python
pdf = FPDF()
pdf.set_auto_page_break(True, margin=15)
for i in range(10):
    pdf.add_page()
    pdf.write(10, f'Page {i+1}')
```

### Graphics Example
```python
pdf.set_draw_color(255, 0, 0)
pdf.set_line_width(1.5)
pdf.line(10, 10, 100, 100)
pdf.rect(50, 50, 40, 30, 'D')
```

## Limitations

### Format Support
- Images: JPEG, PNG, GIF only
- Fonts: TrueType, Type1
- No SVG or vector graphics

### Text Features
- Limited RTL language support
- Basic text shaping only
- No advanced typography

### Performance
- Large file generation may be slow
- Memory usage scales with content
- Limited streaming capabilities