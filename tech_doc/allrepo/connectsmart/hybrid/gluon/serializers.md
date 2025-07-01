# Serializers Module

## Overview
The serializers module provides comprehensive data serialization capabilities for web2py applications. It handles conversion between Python objects and various output formats including JSON, XML, CSV, RSS, iCal, and YAML. The module includes special handling for web2py-specific types and implements security features for safe JSON embedding in HTML.

## Core Functions

### JSON Serialization

#### json()
Primary JSON serialization with HTML-safe encoding.

```python
def json(value, default=custom_json, indent=None, 
         sort_keys=False, cls=JSONEncoderForHTML)
```

**Features:**
- HTML-safe character escaping
- Custom object serialization
- Unicode handling
- Configurable formatting

**Example:**
```python
from gluon.serializers import json

data = {'user': 'John', 'tags': ['web2py', 'python']}
json_str = json(data)  # HTML-safe JSON
```

#### loads_json()
JSON deserialization with key type control.

```python
def loads_json(o, unicode_keys=True, **kwargs)
```

**Features:**
- Optional unicode key conversion
- Encoding specification
- Native json.loads wrapper

#### custom_json()
Default serializer for non-standard types.

**Handles:**
- datetime objects → ISO format
- Decimal → float
- bytes/bytearray → string
- lazyT → translated string
- XmlComponent → XML string
- Sets → lists
- Objects with as_list/as_dict methods

### XML Serialization

#### xml()
Convert Python structures to XML.

```python
def xml(value, encoding='UTF-8', key='document', quote=True)
```

**Example:**
```python
data = {
    'person': {
        'name': 'John',
        'age': 30,
        'tags': ['python', 'web2py']
    }
}
xml_output = xml(data)
```

**Output Structure:**
```xml
<?xml version="1.0" encoding="UTF-8"?>
<document>
  <person>
    <name>John</name>
    <age>30</age>
    <tags>
      <item>python</item>
      <item>web2py</item>
    </tags>
  </person>
</document>
```

#### xml_rec()
Recursive XML builder (internal).

**Features:**
- Dictionary → nested elements
- Lists → item elements
- Custom XML methods support
- Automatic escaping

### RSS Generation

#### rss()
Create RSS 2.0 feeds.

```python
def rss(feed)
```

**Feed Structure:**
```python
feed = {
    'title': 'My Blog',
    'link': 'http://example.com',
    'description': 'Latest posts',
    'entries': [
        {
            'title': 'Post 1',
            'link': 'http://example.com/post1',
            'description': 'Content',
            'created_on': datetime.now()
        }
    ]
}
rss_xml = rss(feed)
```

### iCalendar Generation

#### ics()
Create iCalendar events.

```python
def ics(events, title=None, link=None, 
        timeshift=0, calname=True)
```

**Event Format:**
```python
events = [
    {
        'id': 1,
        'title': 'Meeting',
        'start_datetime': datetime(2024, 1, 15, 10, 0),
        'stop_datetime': datetime(2024, 1, 15, 11, 0)
    }
]
calendar = ics(events, title='Work Calendar')
```

### YAML Serialization

#### yaml()
Serialize to YAML format.

```python
def yaml(data)
```

**Requirements:**
- Requires PyYAML installation
- Raises ImportError if unavailable

#### loads_yaml()
Deserialize from YAML.

```python
def loads_yaml(data)
```

## Utility Functions

### cast_keys()
Convert dictionary keys to specified type.

```python
def cast_keys(o, cast=str, encoding='utf-8')
```

**Use Cases:**
- Python 2.6.5 compatibility
- String key normalization
- Encoding consistency

**Example:**
```python
# Convert unicode keys to str
data = {u'key': u'value'}
normalized = cast_keys(data, cast=str)
```

### safe_encode()
Safely encode text to UTF-8.

```python
def safe_encode(text)
```

**Features:**
- Handles various input types
- Replace invalid characters
- Prevents encoding errors

## Special Classes

### JSONEncoderForHTML
Custom JSON encoder for HTML embedding.

**Security Features:**
- Escapes `&` → `\u0026`
- Escapes `<` → `\u003c`
- Escapes `>` → `\u003e`
- Escapes line/paragraph separators

**Usage:**
```python
# Safe for <script> tags
safe_json = json(data, cls=JSONEncoderForHTML)
```

## Integration Examples

### Controller JSON Response
```python
def api():
    data = db(db.table).select().as_list()
    return json(data)
```

### XML Web Service
```python
def xml_api():
    response.headers['Content-Type'] = 'text/xml'
    data = {'status': 'ok', 'records': records}
    return xml(data)
```

### RSS Feed
```python
def blog_feed():
    posts = db(db.post).select(orderby=~db.post.created_on)
    
    feed = {
        'title': 'My Blog',
        'link': URL('default', 'index', scheme=True, host=True),
        'description': 'Latest blog posts',
        'entries': []
    }
    
    for post in posts:
        feed['entries'].append({
            'title': post.title,
            'link': URL('default', 'show', args=post.id, 
                       scheme=True, host=True),
            'description': post.body,
            'created_on': post.created_on
        })
    
    response.headers['Content-Type'] = 'application/rss+xml'
    return rss(feed)
```

### Calendar Export
```python
def export_calendar():
    events = []
    for event in db(db.events).select():
        events.append({
            'id': event.id,
            'title': event.name,
            'start_datetime': event.start_time,
            'stop_datetime': event.end_time
        })
    
    response.headers['Content-Type'] = 'text/calendar'
    response.headers['Content-Disposition'] = \
        'attachment; filename="events.ics"'
    return ics(events, title='My Events')
```

## Custom Serialization

### Adding Custom Types
```python
def my_custom_json(obj):
    if isinstance(obj, MyClass):
        return obj.to_dict()
    # Fallback to default
    return custom_json(obj)

# Use custom serializer
json_data = json(my_object, default=my_custom_json)
```

### Object Protocol
Objects can define serialization methods:

```python
class MyModel:
    def custom_json(self):
        return {'type': 'MyModel', 'data': self.data}
    
    def custom_xml(self):
        return '<mymodel>%s</mymodel>' % self.data
    
    def as_dict(self):
        return self.__dict__
    
    def as_list(self):
        return list(self.values)
```

## Performance Considerations

### Large Datasets
- Use generators for CSV export
- Implement pagination for JSON APIs
- Consider compression for large responses
- Cache serialized results when possible

### Memory Efficiency
```python
# Stream large results
def stream_json():
    def generate():
        yield '['
        first = True
        for row in db(query).iterselect():
            if not first:
                yield ','
            yield json(row.as_dict())
            first = False
        yield ']'
    return response.stream(generate())
```

## Security Best Practices

### JSON in HTML
Always use JSONEncoderForHTML when embedding in HTML:

```html
<script>
var data = {{=XML(json(data))}}; // Safe
</script>
```

### XML External Entities
The XML serializer doesn't parse input, avoiding XXE attacks.

### User Input
Always validate/sanitize before serialization:

```python
def api():
    # Validate input
    data = {}
    if request.vars.name:
        data['name'] = request.vars.name[:100]
    return json(data)
```

## Error Handling

### Type Errors
```python
try:
    result = json(complex_object)
except TypeError as e:
    # Handle non-serializable types
    result = json({'error': str(e)})
```

### YAML Availability
```python
try:
    yaml_data = yaml(data)
except ImportError:
    # Fallback to JSON
    yaml_data = json(data)
```

## Common Patterns

### API Versioning
```python
def api_response(data, version=1):
    envelope = {
        'version': version,
        'timestamp': datetime.now(),
        'data': data
    }
    return json(envelope)
```

### Error Responses
```python
def error_response(message, code=400):
    response.status = code
    return json({
        'error': True,
        'message': message,
        'code': code
    })
```

### Content Negotiation
```python
def multi_format():
    data = get_data()
    
    if request.extension == 'json':
        return json(data)
    elif request.extension == 'xml':
        return xml(data)
    elif request.extension == 'yaml':
        return yaml(data)
    else:
        return dict(data=data)  # HTML view
```

## See Also
- Python json module documentation
- XML standards and best practices
- RSS 2.0 specification
- iCalendar format reference
- PyYAML documentation