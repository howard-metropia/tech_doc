# PySimpleSOAP SimpleXML Module

**File**: `gluon/contrib/pysimplesoap/simplexml.py`  
**Type**: XML Manipulation and Processing  
**Framework**: Web2py Gluon Framework  
**License**: LGPL 3.0

## Overview

This module provides simplified XML manipulation capabilities similar to PHP's SimpleXML extension. It offers an intuitive interface for creating, parsing, and manipulating XML documents, with special support for SOAP-specific XML structures and namespace handling.

## Core Classes

### SimpleXMLElement Class
The main class for XML manipulation:

```python
class SimpleXMLElement(object):
    def __init__(self, text=None, elements=None, document=None,
                 namespace=None, prefix=None, namespaces_map={}, 
                 jetty=False):
        # Initialize XML element with optional content and namespace mapping
```

### Key Features
- **PHP-like Interface**: Familiar syntax for PHP developers
- **Namespace Support**: Full XML namespace handling
- **Type Conversion**: Automatic type marshalling/unmarshalling
- **SOAP Integration**: Specialized support for SOAP XML structures

## XML Creation and Manipulation

### Basic XML Creation
```python
from gluon.contrib.pysimplesoap import SimpleXMLElement

def create_basic_xml():
    """Create basic XML structure"""
    
    # Create root element
    root = SimpleXMLElement('<root></root>')
    
    # Add child elements
    root.add_child('name', 'John Doe')
    root.add_child('age', 30)
    root.add_child('email', 'john@example.com')
    
    # Add element with attributes
    address = root.add_child('address')
    address['type'] = 'home'
    address.add_child('street', '123 Main St')
    address.add_child('city', 'Anytown')
    address.add_child('state', 'CA')
    
    return str(root)  # Returns XML string
```

### XML Parsing
```python
def parse_xml_document():
    """Parse existing XML document"""
    
    xml_data = """
    <person xmlns:contact="http://example.com/contact">
        <name>Jane Smith</name>
        <contact:email>jane@example.com</contact:email>
        <contact:phone>555-1234</contact:phone>
        <addresses>
            <address type="work">
                <street>456 Business Ave</street>
                <city>Worktown</city>
            </address>
            <address type="home">
                <street>789 Home St</street>
                <city>Hometown</city>
            </address>
        </addresses>
    </person>
    """
    
    # Parse XML
    person = SimpleXMLElement(xml_data)
    
    # Access elements
    name = str(person.name)
    email = str(person('contact:email'))  # Namespace-aware access
    
    # Access attributes
    addresses = []
    for addr in person.addresses.address:
        addresses.append({
            'type': addr['type'],
            'street': str(addr.street),
            'city': str(addr.city)
        })
    
    return {
        'name': name,
        'email': email,
        'addresses': addresses
    }
```

### Namespace Handling
```python
def handle_namespaces():
    """Advanced namespace handling"""
    
    # Define namespace mappings
    namespaces = {
        'soap': 'http://schemas.xmlsoap.org/soap/envelope/',
        'web': 'http://example.com/webservice',
        'data': 'http://example.com/data'
    }
    
    # Create XML with namespaces
    envelope = SimpleXMLElement(
        '<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"></soap:Envelope>',
        namespaces_map=namespaces
    )
    
    # Add SOAP body
    body = envelope.add_child('soap:Body')
    
    # Add web service call
    service_call = body.add_child('web:GetUserInfo')
    service_call.add_child('web:UserId', '123')
    service_call.add_child('web:IncludeDetails', 'true')
    
    # Add data elements
    user_data = service_call.add_child('data:UserData')
    user_data.add_child('data:Name', 'John Doe')
    user_data.add_child('data:Department', 'Engineering')
    
    return str(envelope)
```

## Type Marshalling and Conversion

### Automatic Type Conversion
```python
def type_conversion_examples():
    """Demonstrate automatic type conversion"""
    from gluon.contrib.pysimplesoap.simplexml import SimpleXMLElement
    from gluon.contrib.pysimplesoap.helpers import TYPE_MAP
    
    # Create XML with various data types
    data = SimpleXMLElement('<data></data>')
    
    # Automatic type marshalling
    data.add_child('string_value', 'Hello World')
    data.add_child('integer_value', 42)
    data.add_child('float_value', 3.14159)
    data.add_child('boolean_value', True)
    data.add_child('date_value', datetime.date(2023, 12, 25))
    data.add_child('datetime_value', datetime.datetime.now())
    
    # Complex types
    person = data.add_child('person')
    person.add_child('id', 1001)
    person.add_child('name', 'Alice Johnson')
    person.add_child('active', True)
    person.add_child('salary', 75000.50)
    
    return str(data)

def parse_typed_xml():
    """Parse XML with type conversion"""
    
    xml_data = """
    <response>
        <user_id type="int">12345</user_id>
        <username type="string">alice_user</username>
        <is_active type="boolean">true</is_active>
        <balance type="float">1250.75</balance>
        <last_login type="datetime">2023-12-01T10:30:00</last_login>
    </response>
    """
    
    response = SimpleXMLElement(xml_data)
    
    # Automatic type conversion based on type attributes
    return {
        'user_id': int(response.user_id),
        'username': str(response.username),
        'is_active': response.is_active == 'true',
        'balance': float(response.balance),
        'last_login': str(response.last_login)
    }
```

### Custom Type Handling
```python
def custom_type_handling():
    """Handle custom data types"""
    from gluon.contrib.pysimplesoap.helpers import Struct, Date, Decimal
    
    # Create custom structures
    person = Struct()
    person.id = 1001
    person.name = "Bob Wilson"
    person.hire_date = Date(2020, 1, 15)
    person.salary = Decimal('85000.00')
    
    # Convert to XML
    xml_root = SimpleXMLElement('<employee></employee>')
    
    # Add structured data
    xml_root.add_child('id', person.id)
    xml_root.add_child('name', person.name)
    xml_root.add_child('hire_date', person.hire_date.isoformat())
    xml_root.add_child('salary', str(person.salary))
    
    # Add complex nested structure
    contact = xml_root.add_child('contact_info')
    contact.add_child('email', 'bob.wilson@company.com')
    contact.add_child('phone', '555-0123')
    
    address = contact.add_child('address')
    address.add_child('street', '123 Corporate Blvd')
    address.add_child('city', 'Business City')
    address.add_child('zip', '12345')
    
    return str(xml_root)
```

## Integration with Web2py

### XML Response Generation
```python
def xml_api_response():
    """Generate XML API responses in Web2py"""
    from gluon.contrib.pysimplesoap import SimpleXMLElement
    
    def get_user_xml(user_id):
        """Get user data as XML"""
        # Query database
        user = db.auth_user(user_id)
        if not user:
            # Error response
            error_xml = SimpleXMLElement('<error></error>')
            error_xml.add_child('code', 404)
            error_xml.add_child('message', 'User not found')
            response.status = 404
            return str(error_xml)
        
        # Success response
        user_xml = SimpleXMLElement('<user></user>')
        user_xml.add_child('id', user.id)
        user_xml.add_child('email', user.email)
        user_xml.add_child('first_name', user.first_name or '')
        user_xml.add_child('last_name', user.last_name or '')
        user_xml.add_child('registration_date', 
                          user.registration_key or '')
        
        # Add user profile if exists
        profile = db.user_profile(user.id)
        if profile:
            profile_xml = user_xml.add_child('profile')
            profile_xml.add_child('bio', profile.bio or '')
            profile_xml.add_child('location', profile.location or '')
            profile_xml.add_child('website', profile.website or '')
        
        response.headers['Content-Type'] = 'application/xml'
        return str(user_xml)
    
    return get_user_xml
```

### XML Form Processing
```python
def process_xml_form():
    """Process XML form data"""
    from gluon.contrib.pysimplesoap import SimpleXMLElement
    
    def handle_xml_submission():
        """Handle XML form submission"""
        if request.env.request_method != 'POST':
            raise HTTP(405, "Method not allowed")
        
        if request.env.content_type != 'application/xml':
            raise HTTP(400, "Content-Type must be application/xml")
        
        try:
            # Parse XML request body
            xml_data = request.body.read()
            form_data = SimpleXMLElement(xml_data)
            
            # Extract form fields
            user_data = {
                'first_name': str(form_data.first_name),
                'last_name': str(form_data.last_name),
                'email': str(form_data.email),
                'phone': str(form_data.phone) if form_data.phone else None
            }
            
            # Validate data
            errors = []
            if not user_data['email']:
                errors.append('Email is required')
            elif not IS_EMAIL()(user_data['email'])[1] is None:
                errors.append('Invalid email format')
            
            if not user_data['first_name']:
                errors.append('First name is required')
            
            if errors:
                # Return validation errors as XML
                error_response = SimpleXMLElement('<validation_errors></validation_errors>')
                for error in errors:
                    error_response.add_child('error', error)
                
                response.status = 400
                response.headers['Content-Type'] = 'application/xml'
                return str(error_response)
            
            # Save to database
            user_id = db.auth_user.insert(**user_data)
            db.commit()
            
            # Return success response
            success_response = SimpleXMLElement('<success></success>')
            success_response.add_child('user_id', user_id)
            success_response.add_child('message', 'User created successfully')
            
            response.headers['Content-Type'] = 'application/xml'
            return str(success_response)
            
        except Exception as e:
            # Return error response
            error_response = SimpleXMLElement('<error></error>')
            error_response.add_child('message', str(e))
            
            response.status = 500
            response.headers['Content-Type'] = 'application/xml'
            return str(error_response)
    
    return handle_xml_submission
```

### XML Data Transformation
```python
def xml_data_transformation():
    """Transform data between XML and other formats"""
    from gluon.contrib.pysimplesoap import SimpleXMLElement
    import json
    
    def json_to_xml(json_data):
        """Convert JSON to XML"""
        data = json.loads(json_data) if isinstance(json_data, str) else json_data
        
        def build_xml(obj, parent, name=None):
            if isinstance(obj, dict):
                element = parent.add_child(name) if name else parent
                for key, value in obj.items():
                    build_xml(value, element, key)
            elif isinstance(obj, list):
                for item in obj:
                    build_xml(item, parent, name or 'item')
            else:
                parent.add_child(name, str(obj))
        
        root = SimpleXMLElement('<root></root>')
        build_xml(data, root)
        return str(root)
    
    def xml_to_json(xml_data):
        """Convert XML to JSON"""
        def xml_to_dict(element):
            result = {}
            
            # Add attributes
            for attr_name, attr_value in element.attributes().items():
                result[f'@{attr_name}'] = attr_value
            
            # Add child elements
            for child in element.children():
                child_name = child.get_name()
                child_data = xml_to_dict(child)
                
                if child_name in result:
                    # Multiple children with same name - convert to list
                    if not isinstance(result[child_name], list):
                        result[child_name] = [result[child_name]]
                    result[child_name].append(child_data)
                else:
                    result[child_name] = child_data
            
            # Add text content
            text = str(element).strip()
            if text and not result:
                return text
            elif text:
                result['#text'] = text
            
            return result
        
        root = SimpleXMLElement(xml_data)
        return json.dumps(xml_to_dict(root), indent=2)
    
    return json_to_xml, xml_to_json
```

## Performance Optimization

### Efficient XML Processing
```python
def optimize_xml_processing():
    """Optimize XML processing for performance"""
    from gluon.contrib.pysimplesoap import SimpleXMLElement
    
    def process_large_xml_efficiently(xml_data):
        """Process large XML documents efficiently"""
        
        # Use streaming approach for large documents
        root = SimpleXMLElement(xml_data)
        
        # Batch process child elements
        results = []
        batch_size = 100
        current_batch = []
        
        for child in root.children():
            current_batch.append({
                'name': child.get_name(),
                'value': str(child),
                'attributes': dict(child.attributes())
            })
            
            if len(current_batch) >= batch_size:
                # Process batch
                results.extend(process_batch(current_batch))
                current_batch = []
        
        # Process remaining items
        if current_batch:
            results.extend(process_batch(current_batch))
        
        return results
    
    def process_batch(batch):
        """Process a batch of XML elements"""
        processed = []
        for item in batch:
            # Perform processing logic
            processed.append({
                'processed_name': item['name'].upper(),
                'processed_value': item['value'].strip(),
                'attribute_count': len(item['attributes'])
            })
        return processed
    
    return process_large_xml_efficiently
```

### XML Caching
```python
def xml_caching_strategy():
    """Implement XML caching for better performance"""
    from gluon.contrib.pysimplesoap import SimpleXMLElement
    import hashlib
    
    # XML cache
    xml_cache = {}
    
    def get_cached_xml(cache_key, generator_func, *args, **kwargs):
        """Get cached XML or generate new one"""
        
        # Check cache
        if cache_key in xml_cache:
            cache_entry = xml_cache[cache_key]
            if time.time() - cache_entry['timestamp'] < 300:  # 5 minutes
                return cache_entry['xml']
        
        # Generate new XML
        xml_result = generator_func(*args, **kwargs)
        
        # Cache result
        xml_cache[cache_key] = {
            'xml': xml_result,
            'timestamp': time.time()
        }
        
        return xml_result
    
    def generate_user_xml(user_id):
        """Generate user XML (expensive operation)"""
        user = db.auth_user(user_id)
        if not user:
            return None
        
        user_xml = SimpleXMLElement('<user></user>')
        user_xml.add_child('id', user.id)
        user_xml.add_child('email', user.email)
        # ... more processing
        
        return str(user_xml)
    
    # Usage with caching
    def get_user_xml_cached(user_id):
        cache_key = f"user_xml_{user_id}"
        return get_cached_xml(cache_key, generate_user_xml, user_id)
    
    return get_user_xml_cached
```

## Best Practices

### XML Processing Guidelines
1. **Namespace Awareness**: Always handle XML namespaces properly
2. **Type Safety**: Use appropriate type conversion methods
3. **Error Handling**: Validate XML structure and content
4. **Performance**: Use efficient processing techniques for large documents
5. **Security**: Validate and sanitize XML input to prevent XXE attacks

### Memory Management
1. **Streaming**: Use streaming approaches for large XML documents
2. **Caching**: Cache frequently accessed XML structures
3. **Resource Cleanup**: Properly dispose of XML objects
4. **Batch Processing**: Process large datasets in batches

### Security Considerations
1. **Input Validation**: Validate XML input against expected schemas
2. **XXE Prevention**: Disable external entity processing
3. **Size Limits**: Implement size limits for XML documents
4. **Content Filtering**: Filter potentially dangerous XML content

This module provides comprehensive XML manipulation capabilities for PySimpleSOAP and Web2py applications, enabling efficient processing of XML data while maintaining security and performance standards.