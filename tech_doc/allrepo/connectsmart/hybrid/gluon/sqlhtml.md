# SQLHTML Module

## Overview
The SQLHTML module provides powerful form generation and data presentation components for web2py applications. It bridges the gap between database operations and HTML presentation, offering SQLFORM for database-driven forms, SQLTABLE for data display, and a comprehensive widget system for input elements. This module is central to web2py's rapid development philosophy.

## Core Components

### SQLFORM
Database-backed form generator that automatically creates HTML forms based on table definitions.

**Key Features:**
- Automatic form generation from DAL tables
- Built-in validation and processing
- Support for record creation, editing, and deletion
- Configurable field inclusion/exclusion
- Custom widget assignment
- File upload handling

### SQLTABLE
Generates HTML tables from database records with sorting, pagination, and formatting capabilities.

**Key Features:**
- Automatic column generation
- Custom representers for data formatting
- Sortable columns
- Pagination support
- Row selection and actions
- Export capabilities

### Widget System
Comprehensive set of input widgets for different data types and user interface patterns.

## Widget Classes

### Base Widget Classes

#### FormWidget
Abstract base class for all widgets.

```python
class FormWidget(object):
    _class = "generic-widget"
    
    @classmethod
    def _attributes(cls, field, widget_attributes, **attributes):
        # Build common attributes
        attr = dict(
            _id="%s_%s" % (field.tablename, field.name),
            _class=cls._class,
            _name=field.name,
            requires=field.requires
        )
        return attr
    
    @classmethod  
    def widget(cls, field, value, **attributes):
        raise NotImplementedError
```

### Input Widgets

#### StringWidget
Basic text input for string fields.

```python
@classmethod
def widget(cls, field, value, **attributes):
    default = dict(
        _type="text",
        value=(value is not None and str(value)) or ""
    )
    attr = cls._attributes(field, default, **attributes)
    return INPUT(**attr)
```

#### TextWidget
Multi-line text input using TEXTAREA.

```python
@classmethod
def widget(cls, field, value, **attributes):
    default = dict(value=value)
    attr = cls._attributes(field, default, **attributes)
    return TEXTAREA(**attr)
```

#### PasswordWidget
Secure password input with masking.

```python
@classmethod
def widget(cls, field, value, **attributes):
    default = dict(
        _type="password",
        _value=(value and DEFAULT_PASSWORD_DISPLAY) or ""
    )
    # Add entropy checking for strong passwords
    if is_strong:
        attr['_data-w2p_entropy'] = entropy_value
    return INPUT(**attr)
```

### Selection Widgets

#### OptionsWidget
Single-selection dropdown from defined options.

```python
@classmethod
def widget(cls, field, value, **attributes):
    requires = field.requires
    if hasattr(requires[0], 'options'):
        options = requires[0].options()
    opts = [OPTION(v, _value=k) for (k, v) in options]
    return SELECT(*opts, **attr)
```

#### MultipleOptionsWidget
Multi-selection widget with size control.

```python
@classmethod
def widget(cls, field, value, size=5, **attributes):
    attributes.update(_size=size, _multiple=True)
    return OptionsWidget.widget(field, value, **attributes)
```

#### RadioWidget
Radio button group for single selection.

```python
@classmethod  
def widget(cls, field, value, **attributes):
    # Generate radio buttons in table/ul/div layout
    wrappers = dict(
        table=(TABLE, TR, TD),
        ul=(DIV, UL, LI), 
        divs=(DIV, DIV, DIV)
    )
    parent, child, inner = wrappers[attributes.get('style', 'table')]
    
    for k, v in options:
        checked = {"_checked": "checked"} if k == value else {}
        tds.append(inner(
            INPUT(_type="radio", _value=k, **checked),
            LABEL(v, _for="%s%s" % (field.name, k))
        ))
```

#### CheckboxesWidget
Multiple checkbox selection.

```python
@classmethod
def widget(cls, field, value, **attributes):
    # Similar layout to RadioWidget but checkboxes
    for k, v in options:
        if k in values:
            r_value = k
        else:
            r_value = []
        tds.append(inner(
            INPUT(_type="checkbox", _value=k, value=r_value),
            LABEL(v, _for="%s%s" % (field.name, k))
        ))
```

### Special Widgets

#### UploadWidget
File upload with preview and deletion options.

```python
@classmethod
def widget(cls, field, value, download_url=None, **attributes):
    inp = INPUT(_type="file", **attr)
    
    if download_url and value:
        url = download_url + "/" + value
        if cls.is_image(value):
            image = IMG(_src=url, _width=cls.DEFAULT_WIDTH)
        
        # Add delete checkbox for existing files
        inp = DIV(
            inp,
            SPAN(
                "[", A("file", _href=url), "|",
                INPUT(_type="checkbox", 
                      _name=field.name + cls.ID_DELETE_SUFFIX),
                LABEL("delete"), "]"
            ),
            image
        )
    return inp
```

#### AutocompleteWidget
Ajax-powered autocomplete input.

```python
def __init__(self, request, field, id_field=None, db=None,
             orderby=None, limitby=(0, 10), distinct=False,
             keyword="_autocomplete_%(tablename)s_%(fieldname)s",
             min_length=2):
    # Setup autocomplete parameters
    self.url = URL(args=request.args, vars=urlvars)
    
def callback(self):
    # Handle AJAX requests
    if self.keyword in self.request.vars:
        kword = self.request.vars[self.keyword]
        # Query matching records
        # Return JSON response
```

#### JSONWidget
Special textarea for JSON data editing.

```python
@classmethod
def widget(cls, field, value, **attributes):
    if not isinstance(value, basestring):
        if value is not None:
            value = serializers.json(value)
    return TEXTAREA(value=value, **attr)
```

## Utility Functions

### Field Representation
```python
def represent(field, value, record):
    f = field.represent
    if not callable(f):
        return str(value)
    n = count_expected_args(f)
    if n == 1:
        return f(value)
    elif n == 2:
        return f(value, record)
```

### Cache Representer
```python
class CacheRepresenter(object):
    def __init__(self):
        self.cache = {}
    
    def __call__(self, field, value, row):
        # Cache representation results for performance
        if field not in cache:
            cache[field] = {}
        try:
            nvalue = cache[field][value]
        except KeyError:
            nvalue = field.represent(value, row)
            cache[field][value] = nvalue
        return nvalue
```

### Conditional Display
```python
def show_if(cond):
    """Generate JavaScript conditions for field visibility"""
    base = "%s_%s" % (cond.first.tablename, cond.first.name)
    if cond.op.__name__ == 'eq' and cond.second is True:
        return base, ":checked"
    elif cond.op.__name__ == 'eq':
        return base, "[value='%s']" % cond.second
    # ... handle various operators
```

## Usage Examples

### Basic Form Creation
```python
# Simple create form
form = SQLFORM(db.person)
if form.process().accepted:
    response.flash = 'Record created'
elif form.errors:
    response.flash = 'Form has errors'

# Edit form
record = db.person(1)
form = SQLFORM(db.person, record)
```

### Custom Widget Assignment
```python
# Use custom widgets
db.person.bio.widget = TextWidget.widget
db.person.country.widget = lambda f, v, **attr: SELECT(
    *[OPTION(c.name, _value=c.id) for c in countries],
    **attr
)

form = SQLFORM(db.person)
```

### Upload Handling
```python
# File upload field
db.define_table('document',
    Field('title'),
    Field('file', 'upload')
)

form = SQLFORM(db.document)
if form.process().accepted:
    # File automatically handled
    filename = form.vars.file
```

### Table Display
```python
# Basic table
rows = db(db.person).select()
table = SQLTABLE(rows)

# With custom headers and representation
table = SQLTABLE(rows,
    headers={'person.name': 'Full Name'},
    represent={'person.birthdate': lambda v, r: v.strftime('%Y-%m-%d')}
)
```

### Autocomplete Setup
```python
# In controller
def autocomplete_person():
    widget = AutocompleteWidget(
        request, db.person.name,
        orderby=db.person.name,
        limitby=(0, 10)
    )
    return widget.callback()

# In form
db.order.person_id.widget = AutocompleteWidget(
    request, db.person.name, db.person.id
).widget
```

## Advanced Features

### Form Factories
Create forms without database tables:

```python
from gluon.sqlhtml import form_factory

form = form_factory(
    Field('name', requires=IS_NOT_EMPTY()),
    Field('email', requires=IS_EMAIL()),
    Field('message', 'text')
)
```

### Custom Validators
```python
def IS_VALID_USERNAME(error_message='Invalid username'):
    def validator(value):
        if len(value) < 3:
            return (value, error_message)
        if not value.isalnum():
            return (value, error_message)
        return (value, None)
    return validator

db.person.username.requires = IS_VALID_USERNAME()
```

### Conditional Fields
```python
# Show field based on another field's value
db.person.spouse_name.show_if = db.person.married == True

# JavaScript will handle visibility
form = SQLFORM(db.person)
```

### Widget Customization
```python
class CustomSelectWidget(OptionsWidget):
    @classmethod
    def widget(cls, field, value, **attributes):
        # Add CSS classes
        attributes['_class'] = 'custom-select'
        attributes['_data-placeholder'] = 'Choose option...'
        return super().widget(field, value, **attributes)

# Apply to field
db.person.category.widget = CustomSelectWidget.widget
```

## Performance Optimization

### Representation Caching
```python
# Use cached representer for large datasets
representer = CacheRepresenter()

table = SQLTABLE(rows,
    represent={'person.company': representer}
)
```

### Lazy Loading
```python
# Process forms efficiently
if form.process(dbio=False).accepted:
    # Manual database operations
    id = db.person.insert(**form.vars)
    form.vars.id = id
```

### Widget Reuse
```python
# Define reusable widgets
country_widget = lambda f, v, **attr: SELECT(
    *get_country_options(),
    **attr
)

# Apply to multiple fields
db.person.birth_country.widget = country_widget
db.person.residence_country.widget = country_widget
```

## Security Considerations

### Input Validation
```python
# Always validate uploads
def secure_upload_widget(field, value, **attr):
    attr['_accept'] = '.jpg,.png,.pdf'  # Limit file types
    return UploadWidget.widget(field, value, **attr)
```

### XSS Prevention
```python
# Escape output in custom representers
def safe_representer(value, row):
    return XML(value) if value else ''
```

### CSRF Protection
Forms automatically include CSRF tokens when using `form.process()`.

## Testing

### Form Testing
```python
def test_form():
    form = SQLFORM(db.person)
    # Simulate form submission
    form.vars.name = 'Test User'
    form.vars.email = 'test@example.com'
    
    if form.validate():
        assert form.vars.name == 'Test User'
```

### Widget Testing
```python
def test_widget():
    field = db.person.name
    widget_html = StringWidget.widget(field, 'test value')
    assert 'value="test value"' in str(widget_html)
```

## Best Practices

### Form Design
1. Use appropriate widgets for data types
2. Implement proper validation
3. Provide clear error messages
4. Consider user experience

### Performance
1. Cache representations for large datasets
2. Use pagination for long tables
3. Minimize database queries
4. Optimize widget rendering

### Accessibility
1. Use proper labels and fieldsets
2. Implement keyboard navigation
3. Provide alternative text
4. Follow WCAG guidelines

## See Also
- DAL Field types and validators
- HTML helper documentation
- Web2py forms and validation guide
- JavaScript integration patterns