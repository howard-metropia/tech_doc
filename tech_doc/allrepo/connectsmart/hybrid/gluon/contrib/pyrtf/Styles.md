# PyRTF Styles Module

**File**: `gluon/contrib/pyrtf/Styles.py`  
**Type**: RTF Style Definitions and Management  
**Framework**: Web2py Gluon Framework

## Overview

This module defines style classes and management systems for PyRTF documents. It provides paragraph styles, character styles, and style sheet management to enable consistent formatting and professional document appearance.

## Core Style Classes

### ParagraphStyle Class
Defines reusable paragraph formatting styles:

```python
class ParagraphStyle:
    def __init__(self, name, font=None, font_size=None, 
                 bold=None, italic=None, underline=None,
                 colour=None, alignment=None, 
                 first_line_indent=None, left_indent=None,
                 right_indent=None, space_before=None,
                 space_after=None, line_spacing=None):
        self.Name = name
        self.Font = font
        self.FontSize = font_size
        self.Bold = bold
        self.Italic = italic
        self.Underline = underline
        self.Colour = colour
        self.Alignment = alignment
        self.FirstLineIndent = first_line_indent
        self.LeftIndent = left_indent
        self.RightIndent = right_indent
        self.SpaceBefore = space_before
        self.SpaceAfter = space_after
        self.LineSpacing = line_spacing
```

### CharacterStyle Class
Defines reusable character formatting styles:

```python
class CharacterStyle:
    def __init__(self, name, font=None, font_size=None,
                 bold=None, italic=None, underline=None,
                 colour=None, background_colour=None):
        self.Name = name
        self.Font = font
        self.FontSize = font_size
        self.Bold = bold
        self.Italic = italic
        self.Underline = underline
        self.Colour = colour
        self.BackgroundColour = background_colour
```

### StyleSheet Class
Container for managing document styles:

```python
class StyleSheet:
    def __init__(self):
        self.ParagraphStyles = []
        self.CharacterStyles = []
    
    def append(self, style):
        if isinstance(style, ParagraphStyle):
            self.ParagraphStyles.append(style)
        elif isinstance(style, CharacterStyle):
            self.CharacterStyles.append(style)
    
    def get_style(self, name):
        # Find style by name
        for style in self.ParagraphStyles + self.CharacterStyles:
            if style.Name == name:
                return style
        return None
```

## Pre-defined Style Collections

### Standard Document Styles
```python
def create_standard_styles():
    """Create a collection of standard document styles"""
    from gluon.contrib import pyrtf
    
    styles = pyrtf.StyleSheet()
    
    # Heading styles
    heading1 = pyrtf.ParagraphStyle(
        'Heading 1',
        font_size=18 * 20,  # 18 points (20 twips per point)
        bold=True,
        colour=pyrtf.Colour('DarkBlue', 0, 0, 128),
        space_before=240,   # 12 points
        space_after=120     # 6 points
    )
    styles.append(heading1)
    
    heading2 = pyrtf.ParagraphStyle(
        'Heading 2',
        font_size=14 * 20,  # 14 points
        bold=True,
        colour=pyrtf.Colour('MediumBlue', 0, 0, 180),
        space_before=200,
        space_after=100
    )
    styles.append(heading2)
    
    heading3 = pyrtf.ParagraphStyle(
        'Heading 3',
        font_size=12 * 20,  # 12 points
        bold=True,
        space_before=160,
        space_after=80
    )
    styles.append(heading3)
    
    # Body text styles
    normal = pyrtf.ParagraphStyle(
        'Normal',
        font_size=12 * 20,
        line_spacing=1.15,
        space_after=120
    )
    styles.append(normal)
    
    body_indented = pyrtf.ParagraphStyle(
        'Body Text Indented',
        font_size=12 * 20,
        first_line_indent=360,  # 0.25 inch
        line_spacing=1.15,
        space_after=120
    )
    styles.append(body_indented)
    
    # Quote style
    quote = pyrtf.ParagraphStyle(
        'Quote',
        font_size=11 * 20,
        italic=True,
        left_indent=720,    # 0.5 inch
        right_indent=720,
        space_before=120,
        space_after=120
    )
    styles.append(quote)
    
    # Character styles
    emphasis = pyrtf.CharacterStyle(
        'Emphasis',
        italic=True,
        colour=pyrtf.Colour('DarkRed', 128, 0, 0)
    )
    styles.append(emphasis)
    
    strong = pyrtf.CharacterStyle(
        'Strong',
        bold=True
    )
    styles.append(strong)
    
    return styles
```

## Usage Examples

### Creating Styled Documents
```python
def create_styled_document():
    from gluon.contrib import pyrtf
    
    # Create document with styles
    doc = pyrtf.Document()
    doc.StyleSheet = create_standard_styles()
    
    section = pyrtf.Section()
    doc.Sections.append(section)
    
    # Use heading style
    title = pyrtf.Paragraph(style=doc.StyleSheet.get_style('Heading 1'))
    title.append(pyrtf.Text("Document Title"))
    section.append(title)
    
    # Use body text style
    body = pyrtf.Paragraph(style=doc.StyleSheet.get_style('Normal'))
    body.append(pyrtf.Text("This is body text using the Normal style."))
    section.append(body)
    
    # Use quote style
    quote = pyrtf.Paragraph(style=doc.StyleSheet.get_style('Quote'))
    quote.append(pyrtf.Text("This is a quoted passage with special formatting."))
    section.append(quote)
    
    return pyrtf.dumps(doc)
```

### Dynamic Style Creation
```python
def create_custom_styles(theme='professional'):
    """Create styles based on theme"""
    from gluon.contrib import pyrtf
    
    styles = pyrtf.StyleSheet()
    
    if theme == 'professional':
        # Professional business theme
        colors = {
            'primary': pyrtf.Colour('BusinessBlue', 0, 51, 102),
            'secondary': pyrtf.Colour('BusinessGray', 64, 64, 64),
            'accent': pyrtf.Colour('BusinessGold', 204, 153, 0)
        }
        
        title_style = pyrtf.ParagraphStyle(
            'Professional Title',
            font_size=20 * 20,
            bold=True,
            colour=colors['primary'],
            alignment=pyrtf.ParagraphPropertySet.CENTER,
            space_after=300
        )
        
    elif theme == 'creative':
        # Creative/artistic theme
        colors = {
            'primary': pyrtf.Colour('CreativePurple', 102, 51, 153),
            'secondary': pyrtf.Colour('CreativeOrange', 255, 102, 0),
            'accent': pyrtf.Colour('CreativeGreen', 51, 153, 102)
        }
        
        title_style = pyrtf.ParagraphStyle(
            'Creative Title',
            font_size=24 * 20,
            bold=True,
            italic=True,
            colour=colors['primary'],
            space_after=400
        )
    
    elif theme == 'academic':
        # Academic/scholarly theme
        colors = {
            'primary': pyrtf.Colour('AcademicBlack', 0, 0, 0),
            'secondary': pyrtf.Colour('AcademicGray', 96, 96, 96),
            'accent': pyrtf.Colour('AcademicBlue', 0, 0, 153)
        }
        
        title_style = pyrtf.ParagraphStyle(
            'Academic Title',
            font_size=16 * 20,
            bold=True,
            colour=colors['primary'],
            alignment=pyrtf.ParagraphPropertySet.CENTER,
            space_after=240
        )
    
    styles.append(title_style)
    
    # Common body style for all themes
    body_style = pyrtf.ParagraphStyle(
        'Themed Body',
        font_size=12 * 20,
        colour=colors['secondary'],
        line_spacing=1.2,
        space_after=120
    )
    styles.append(body_style)
    
    return styles
```

### Style Inheritance and Modification
```python
def create_style_variants(base_style, variants):
    """Create style variants from a base style"""
    from gluon.contrib import pyrtf
    import copy
    
    variant_styles = []
    
    for variant_name, modifications in variants.items():
        # Create copy of base style
        variant_style = copy.deepcopy(base_style)
        variant_style.Name = variant_name
        
        # Apply modifications
        for property_name, value in modifications.items():
            if hasattr(variant_style, property_name):
                setattr(variant_style, property_name, value)
        
        variant_styles.append(variant_style)
    
    return variant_styles

# Usage example
def create_heading_variants():
    from gluon.contrib import pyrtf
    
    # Base heading style
    base_heading = pyrtf.ParagraphStyle(
        'Base Heading',
        font_size=16 * 20,
        bold=True,
        space_before=200,
        space_after=100
    )
    
    # Define variants
    variants = {
        'Heading Large': {'FontSize': 20 * 20},
        'Heading Medium': {'FontSize': 16 * 20},
        'Heading Small': {'FontSize': 14 * 20},
        'Heading Centered': {
            'Alignment': pyrtf.ParagraphPropertySet.CENTER
        },
        'Heading Colored': {
            'Colour': pyrtf.Colour('HeadingBlue', 0, 0, 128)
        }
    }
    
    return create_style_variants(base_heading, variants)
```

## Advanced Style Management

### Style Repository
```python
class StyleRepository:
    """Centralized style management"""
    
    def __init__(self):
        self.styles = {}
        self.themes = {}
        
    def register_style(self, style):
        """Register a style in the repository"""
        self.styles[style.Name] = style
    
    def register_theme(self, theme_name, styles):
        """Register a collection of styles as a theme"""
        self.themes[theme_name] = styles
        
        # Also register individual styles
        for style in styles.ParagraphStyles + styles.CharacterStyles:
            self.register_style(style)
    
    def get_style(self, name):
        """Get style by name"""
        return self.styles.get(name)
    
    def get_theme(self, theme_name):
        """Get theme by name"""
        return self.themes.get(theme_name)
    
    def create_document_with_theme(self, theme_name):
        """Create document with specified theme"""
        from gluon.contrib import pyrtf
        
        doc = pyrtf.Document()
        theme_styles = self.get_theme(theme_name)
        
        if theme_styles:
            doc.StyleSheet = theme_styles
        
        return doc

# Global style repository
style_repo = StyleRepository()

# Register standard themes
style_repo.register_theme('standard', create_standard_styles())
style_repo.register_theme('professional', create_custom_styles('professional'))
style_repo.register_theme('creative', create_custom_styles('creative'))
style_repo.register_theme('academic', create_custom_styles('academic'))
```

## Integration with Web2py

### User-Configurable Styles
```python
def configurable_document_styles():
    """Allow users to configure document styles"""
    
    form = FORM(
        TABLE(
            TR("Document Theme:", SELECT(
                OPTION("Standard", _value="standard"),
                OPTION("Professional", _value="professional"),
                OPTION("Creative", _value="creative"),
                OPTION("Academic", _value="academic"),
                _name="theme"
            )),
            TR("Title Font Size:", INPUT(_name="title_size", _type="number", _value=18)),
            TR("Body Font Size:", INPUT(_name="body_size", _type="number", _value=12)),
            TR("Line Spacing:", SELECT(
                OPTION("Single", _value="1.0"),
                OPTION("1.15", _value="1.15"),
                OPTION("1.5", _value="1.5"),
                OPTION("Double", _value="2.0"),
                _name="line_spacing"
            )),
            TR("", INPUT(_type="submit", _value="Generate Document"))
        )
    )
    
    if form.process().accepted:
        # Create custom styles based on form input
        theme = form.vars.theme
        title_size = int(form.vars.title_size or 18)
        body_size = int(form.vars.body_size or 12)
        line_spacing = float(form.vars.line_spacing or 1.15)
        
        # Get base theme
        base_styles = style_repo.get_theme(theme)
        
        # Customize styles
        custom_styles = customize_styles(base_styles, {
            'title_size': title_size,
            'body_size': body_size,
            'line_spacing': line_spacing
        })
        
        # Create document
        doc = pyrtf.Document()
        doc.StyleSheet = custom_styles
        
        # Add sample content
        section = pyrtf.Section()
        doc.Sections.append(section)
        
        # Use customized styles
        title = pyrtf.Paragraph(style=doc.StyleSheet.get_style('Heading 1'))
        title.append(pyrtf.Text("Sample Document"))
        section.append(title)
        
        body = pyrtf.Paragraph(style=doc.StyleSheet.get_style('Normal'))
        body.append(pyrtf.Text("This document uses your custom style settings."))
        section.append(body)
        
        # Generate and return
        rtf_content = pyrtf.dumps(doc)
        response.headers['Content-Type'] = 'application/rtf'
        response.headers['Content-Disposition'] = 'attachment; filename=styled_document.rtf'
        return rtf_content
    
    return dict(form=form)

def customize_styles(base_styles, customizations):
    """Apply customizations to base styles"""
    import copy
    
    # Create copy of styles
    custom_styles = copy.deepcopy(base_styles)
    
    # Apply customizations
    for style in custom_styles.ParagraphStyles:
        if 'title_size' in customizations and 'Heading' in style.Name:
            style.FontSize = customizations['title_size'] * 20
        elif 'body_size' in customizations and 'Normal' in style.Name:
            style.FontSize = customizations['body_size'] * 20
        
        if 'line_spacing' in customizations:
            style.LineSpacing = customizations['line_spacing']
    
    return custom_styles
```

### Database-Driven Style Management
```python
def create_database_driven_styles():
    """Create styles from database configuration"""
    
    # Define style configuration table
    db.define_table('style_config',
        Field('name', 'string', required=True, unique=True),
        Field('style_type', 'string', requires=IS_IN_SET(['paragraph', 'character'])),
        Field('font_size', 'integer', default=12),
        Field('bold', 'boolean', default=False),
        Field('italic', 'boolean', default=False),
        Field('underline', 'boolean', default=False),
        Field('color_red', 'integer', default=0),
        Field('color_green', 'integer', default=0),
        Field('color_blue', 'integer', default=0),
        Field('alignment', 'string', default='left'),
        Field('space_before', 'integer', default=0),
        Field('space_after', 'integer', default=0),
        Field('line_spacing', 'double', default=1.0),
        Field('active', 'boolean', default=True)
    )
    
    def load_styles_from_database():
        """Load styles from database"""
        from gluon.contrib import pyrtf
        
        styles = pyrtf.StyleSheet()
        
        # Query active styles
        style_configs = db(db.style_config.active == True).select()
        
        for config in style_configs:
            if config.style_type == 'paragraph':
                style = pyrtf.ParagraphStyle(
                    config.name,
                    font_size=config.font_size * 20,
                    bold=config.bold,
                    italic=config.italic,
                    underline=config.underline,
                    colour=pyrtf.Colour(f"{config.name}_color", 
                                      config.color_red, 
                                      config.color_green, 
                                      config.color_blue),
                    space_before=config.space_before,
                    space_after=config.space_after,
                    line_spacing=config.line_spacing
                )
                styles.append(style)
                
            elif config.style_type == 'character':
                style = pyrtf.CharacterStyle(
                    config.name,
                    font_size=config.font_size * 20,
                    bold=config.bold,
                    italic=config.italic,
                    underline=config.underline,
                    colour=pyrtf.Colour(f"{config.name}_color",
                                      config.color_red,
                                      config.color_green,
                                      config.color_blue)
                )
                styles.append(style)
        
        return styles
    
    return load_styles_from_database
```

## Best Practices

### Style Design Guidelines
1. **Consistency**: Use consistent naming conventions for styles
2. **Hierarchy**: Create clear visual hierarchy with different heading levels
3. **Readability**: Ensure adequate spacing and appropriate font sizes
4. **Reusability**: Design styles to be reusable across documents
5. **Maintainability**: Centralize style definitions for easy updates

### Performance Considerations
1. **Style Caching**: Cache compiled styles for better performance
2. **Minimal Styles**: Only include necessary styles in documents
3. **Style Inheritance**: Use style inheritance to reduce redundancy
4. **Lazy Loading**: Load styles only when needed for large style repositories

This module provides comprehensive style management capabilities for creating professional, consistent, and visually appealing RTF documents in Web2py applications.